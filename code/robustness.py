"""Robustness & heterogeneity for licensed production -> first export.
Yearly country x category x year panel; Cox with time-varying licence exposure.
All specifications use SIPRI-internal variables only (external controls to be merged later)."""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from lifelines import CoxTimeVaryingFitter

END = 2025
df0 = pd.read_csv("deals_clean.csv")

WEST_EU = {'United Kingdom', 'France', 'Germany', 'Italy', 'Netherlands', 'Sweden', 'Switzerland', 'Spain', 'Belgium',
           'Austria', 'Norway', 'Denmark', 'Finland', 'Czechia', 'Poland'}


def build_panel(df, lic_col='lic_L1', merge_lineage=True, drop_uncertain=False, export_min_deals=1,
                export_state_only=False):
    d = df.copy()
    rc = 'recipient_lineage' if merge_lineage else 'recipient'
    sc = 'supplier_lineage' if merge_lineage else 'supplier'
    st = d[d.recipient_type == 'state']
    lic_mask = st[lic_col] == 1
    if drop_uncertain:
        lic_mask &= st.lic_uncertain == 0
    imp = st.groupby([rc, 'category']).order_year.min().rename('first_import')
    lic = st[lic_mask].groupby([rc, 'category']).order_year.min().rename('first_lic')
    # supplier bloc of first licence
    firstlic_rows = st[lic_mask].sort_values('order_year').drop_duplicates([rc, 'category'])
    bloc = firstlic_rows.set_index([rc, 'category'])['supplier_lineage'].map(
        lambda s: 'US' if s == 'United States' else ('USSR/Russia' if s == 'Russia' else ('W.Europe' if s in WEST_EU else 'Other'))).rename('lic_bloc')
    ex = d[d.supplier_type == 'state']
    if export_state_only:
        ex = ex[ex.recipient_type == 'state']
    ex = ex.sort_values('order_year')
    ex['k'] = ex.groupby([sc, 'category']).cumcount() + 1
    fe = ex[ex.k == export_min_deals].groupby([sc, 'category']).order_year.min().rename('first_export')
    fe.index.names = [rc, 'category']
    p = pd.concat([imp, lic, bloc, fe], axis=1).dropna(subset=['first_import']).reset_index()
    p = p.rename(columns={rc: 'country'})
    p['tier3'] = p.category.map(st.groupby('category').tier3.agg(lambda s: s.mode()[0]))
    p = p[~((p.first_export <= p.first_import))]  # drop pre-exporters
    p['event'] = (p.first_export.notna()).astype(int)
    p['exit'] = np.where(p.event == 1, p.first_export, END)
    p.loc[p.exit <= p.first_import, 'exit'] = p.first_import + 0.5
    # country-level yearly cumulative import TIV (all categories) and # categories imported -> internal capacity proxies
    tiv = st.groupby([rc, 'order_year']).tiv_order.sum().rename('tiv')
    cat_first = st.groupby([rc, 'category']).order_year.min().reset_index()
    return p, tiv, cat_first, rc


def expand_yearly(p, tiv, cat_first, rc):
    rows = []
    tiv_d = tiv.reset_index()
    tiv_d.columns = ['country', 'year', 'tiv']
    cum = {}
    for cty, g in tiv_d.groupby('country'):
        s = g.set_index('year').tiv.reindex(range(1940, END + 1), fill_value=0).cumsum()
        cum[cty] = s
    ncat = {}
    for cty, g in cat_first.groupby(rc):
        ncat[cty] = pd.Series(1, index=g.order_year).groupby(level=0).sum().reindex(range(1940, END + 1), fill_value=0).cumsum()
    for _, r in p.iterrows():
        years = np.arange(int(r.first_import), int(np.ceil(r.exit)))
        if len(years) == 0:
            years = np.array([int(r.first_import)])
        for y in years:
            lic_on = int(pd.notna(r.first_lic) and r.first_lic <= y)
            stop = y + 1 if y + 1 < r.exit else r.exit
            rows.append((f"{r.country}|{r.category}", r.country, r.category, r.tier3, y - r.first_import, stop - r.first_import,
                         lic_on, int(r.event == 1 and stop >= r.exit), r.first_import,
                         np.log1p(cum[r.country].get(y - 1, 0)), ncat[r.country].get(y - 1, 0), r.lic_bloc if lic_on else 'none'))
    tv = pd.DataFrame(rows, columns=['id', 'country', 'category', 'tier3', 't0', 't1', 'lic', 'ev', 'cohort', 'log_cum_tiv', 'n_cat', 'bloc'])
    tv = tv[tv.t1 > tv.t0].copy()
    tv['platform'] = (tv.tier3 == 'platform').astype(int)
    tv['weapon'] = (tv.tier3 == 'weapon').astype(int)
    tv['cohort_c'] = (tv.cohort - 1980) / 10
    tv['coldwar'] = (tv.cohort < 1991).astype(int)
    return tv


def fit(tv, covs, strata=None, label=''):
    m = CoxTimeVaryingFitter(penalizer=0)
    cols = ['id', 't0', 't1', 'ev'] + covs + ([strata] if strata else [])
    m.fit(tv[cols], id_col='id', start_col='t0', stop_col='t1', event_col='ev', strata=strata)
    s = m.summary
    out = {'spec': label, 'n_pairs': tv.id.nunique(), 'events': int(tv.ev.sum()),
           'HR_lic': s.loc['lic', 'exp(coef)'], 'lo': s.loc['lic', 'exp(coef) lower 95%'], 'hi': s.loc['lic', 'exp(coef) upper 95%'], 'p': s.loc['lic', 'p']}
    return out, s


results = []
BASE = ['lic', 'platform', 'weapon', 'cohort_c']
CTRL = BASE + ['log_cum_tiv', 'n_cat']

# ---- baseline & internal controls
p, tiv, cf, rc = build_panel(df0)
tv = expand_yearly(p, tiv, cf, rc)
tv.to_csv("panel_yearly_base.csv", index=False)
r, s = fit(tv, BASE, label='(1) Baseline: tier-1 licence, cohort + tier'); results.append(r)
r, s_ctrl = fit(tv, CTRL, label='(2) + internal capacity controls (log cum. import TIV, # categories imported)'); results.append(r)
print(s_ctrl[['exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].round(3))
r, s_str = fit(tv, ['lic', 'platform', 'weapon', 'log_cum_tiv', 'n_cat'], strata='country', label='(3) Country-stratified Cox (within-country, across categories)'); results.append(r)
print("\nStratified:\n", s_str[['exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].round(3))

# ---- alternative exposure / coding
p2, tiv2, cf2, _ = build_panel(df0, lic_col='lic_any'); tv2 = expand_yearly(p2, tiv2, cf2, rc)
r, _ = fit(tv2, CTRL, label='(4) Exposure = tiers 1-3 (incl. assembly, components)'); results.append(r)
p3, tiv3, cf3, _ = build_panel(df0, drop_uncertain=True); tv3 = expand_yearly(p3, tiv3, cf3, rc)
r, _ = fit(tv3, CTRL, label='(5) Drop "probably/possibly" licence deals'); results.append(r)
p4, tiv4, cf4, rc4 = build_panel(df0, merge_lineage=False); tv4 = expand_yearly(p4, tiv4, cf4, rc4)
r, _ = fit(tv4, CTRL, label='(6) No successor-state merging (USSR/Russia etc. separate)'); results.append(r)

p2b, tiv2b, cf2b, _ = build_panel(df0, lic_col='lic_L1_cons'); tv2b = expand_yearly(p2b, tiv2b, cf2b, rc)
r, _ = fit(tv2b, CTRL, label="(5b) Conservative coding: 'A or B' forms assigned lower tier"); results.append(r)

# ---- alternative outcome
p5, tiv5, cf5, _ = build_panel(df0, export_min_deals=2); tv5 = expand_yearly(p5, tiv5, cf5, rc)
r, _ = fit(tv5, CTRL, label='(7) Outcome = 2nd export deal (sustained exporter)'); results.append(r)
p6, tiv6, cf6, _ = build_panel(df0, export_state_only=True); tv6 = expand_yearly(p6, tiv6, cf6, rc)
r, _ = fit(tv6, CTRL, label='(8) Exports to state recipients only'); results.append(r)

# ---- heterogeneity
tv['lic_x_platform'] = tv.lic * tv.platform; tv['lic_x_weapon'] = tv.lic * tv.weapon
_, s_int = fit(tv, CTRL + ['lic_x_platform', 'lic_x_weapon'], label='interaction')
tv['lic_x_coldwar'] = tv.lic * tv.coldwar
_, s_cw = fit(tv, CTRL + ['coldwar', 'lic_x_coldwar'], label='coldwar')
for b in ['US', 'W.Europe', 'USSR/Russia', 'Other']:
    tv[f'lic_{b}'] = ((tv.bloc == b)).astype(int)
_, s_bloc = fit(tv, ['lic_US', 'lic_W.Europe', 'lic_USSR/Russia', 'lic_Other', 'platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat'] if False else
                ['platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat', 'lic_US', 'lic_W.Europe', 'lic_USSR/Russia', 'lic_Other'], label='bloc') if False else (None, None)
# bloc model fitted separately because fit() expects a 'lic' column
m = CoxTimeVaryingFitter(penalizer=0)
m.fit(tv[['id', 't0', 't1', 'ev', 'platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat', 'lic_US', 'lic_W.Europe', 'lic_USSR/Russia', 'lic_Other']],
      id_col='id', start_col='t0', stop_col='t1', event_col='ev')
s_bloc = m.summary

res = pd.DataFrame(results)
res[['HR_lic', 'lo', 'hi']] = res[['HR_lic', 'lo', 'hi']].round(2); res['p'] = res.p.map(lambda x: f"{x:.1e}")
print("\n=== Robustness table (HR of licence) ===")
print(res.to_string(index=False))
res.to_csv("tab_robustness.csv", index=False)

print("\n=== Heterogeneity: tier interactions ===")
print(s_int.loc[['lic', 'lic_x_platform', 'lic_x_weapon'], ['exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].round(3))
print("\n=== Heterogeneity: Cold War vs post-1991 cohort ===")
print(s_cw.loc[['lic', 'coldwar', 'lic_x_coldwar'], ['exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].round(3))
print("\n=== Heterogeneity: licensor bloc (vs no licence) ===")
print(s_bloc.loc[['lic_US', 'lic_W.Europe', 'lic_USSR/Russia', 'lic_Other'], ['exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].round(3))
print("\nlicensed pair-years by bloc:", tv[tv.lic == 1].groupby('bloc').id.nunique().to_dict())
pd.concat({'tier': s_int, 'coldwar': s_cw, 'bloc': s_bloc}).to_csv("tab_heterogeneity.csv")
s_ctrl.to_csv("tab_cox_controls.csv"); s_str.to_csv("tab_cox_stratified.csv")
