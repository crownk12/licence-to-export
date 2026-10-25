"""Part A: category-level Cox with external controls (GDP, GDP pc, Milex), lagged one year.
Part B: country-year spillover design: export activity (all categories) vs licence stock, country & year FE, PPML.
Part C: licensor-bloc heterogeneity within country-stratified model."""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from lifelines import CoxTimeVaryingFitter
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COL = {'blue': '#2a78d6', 'orange': '#eb6834', 'aqua': '#1baf7a'}
INK, INK2, GRID = '#0b0b0b', '#52514e', '#e4e3df'
plt.rcParams.update({'font.size': 10, 'axes.edgecolor': INK2, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6, 'axes.axisbelow': True,
                     'figure.dpi': 150, 'savefig.dpi': 200, 'savefig.bbox': 'tight', 'legend.frameon': False})

END = 2025
ext = pd.read_csv("ext_panel.csv")
ext_l = ext.copy(); ext_l['year'] = ext_l.year + 1      # lag 1: value at t-1 attached to year t
ext_l = ext_l[['lineage', 'year', 'log_milex', 'log_gdp', 'log_gdppc']].rename(columns={'lineage': 'country'})

# ============================================================ Part A
tv = pd.read_csv("panel_yearly_base.csv")
tv['year'] = (tv.cohort + tv.t0).astype(int)
tv = tv.merge(ext_l, on=['country', 'year'], how='left')
tv['lic_US'] = ((tv.bloc == 'US')).astype(int)
tv['lic_nonUS'] = ((tv.lic == 1) & (tv.bloc != 'US')).astype(int)


def fit(d, covs, strata=None, label='', key='lic'):
    m = CoxTimeVaryingFitter(penalizer=0)
    cols = ['id', 't0', 't1', 'ev'] + covs + ([strata] if strata else [])
    d = d.dropna(subset=covs)
    m.fit(d[cols], id_col='id', start_col='t0', stop_col='t1', event_col='ev', strata=strata)
    s = m.summary
    rows = []
    for k in ([key] if isinstance(key, str) else key):
        rows.append(dict(spec=label, var=k, n_pairs=d.id.nunique(), events=int(d.ev.sum()), HR=round(s.loc[k, 'exp(coef)'], 2),
                         lo=round(s.loc[k, 'exp(coef) lower 95%'], 2), hi=round(s.loc[k, 'exp(coef) upper 95%'], 2), p=round(s.loc[k, 'p'], 3)))
    return rows, s


res = []
BASE = ['lic', 'platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat']
EXT = ['log_gdp', 'log_gdppc', 'log_milex']
sub = tv.dropna(subset=EXT)
r, _ = fit(sub, BASE, label='(A1) Internal controls only, sample with external data (1960+)'); res += r
r, sA2 = fit(sub, BASE + EXT, label='(A2) + log GDP, log GDP pc, log Milex (t-1)'); res += r
print(sA2[['exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].round(3))
r, sA3 = fit(sub, ['lic', 'platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat'] + EXT, strata='country', label='(A3) + country-stratified'); res += r
r, _ = fit(tv.dropna(subset=['log_milex']), BASE + ['log_milex'], label='(A4) Milex only (1950+ sample)'); res += r
r, _ = fit(tv.dropna(subset=['log_milex']), BASE + ['log_milex'], strata='country', label='(A5) Milex only, country-stratified'); res += r
# Part C: US vs non-US licensor
r, sC = fit(sub, ['lic_US', 'lic_nonUS', 'platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat'] + EXT, label='(C1) US vs non-US licensor, pooled', key=['lic_US', 'lic_nonUS']); res += r
r, sC2 = fit(sub, ['lic_US', 'lic_nonUS', 'platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat'] + EXT, strata='country', label='(C2) US vs non-US licensor, country-stratified', key=['lic_US', 'lic_nonUS']); res += r
resA = pd.DataFrame(res)
print("\n=== Part A/C: category-level Cox ===")
print(resA.to_string(index=False))
resA.to_csv("tab_cox_external.csv", index=False)
sA2.to_csv("tab_cox_A2_full.csv")

# ============================================================ Part B: country-year spillover (PPML with FE)
df = pd.read_csv("deals_clean.csv")
st = df[df.recipient_type == 'state']
cm = pd.read_csv("country_map.csv")
countries = sorted(set(st.recipient_lineage))
years = range(1950, END + 1)
idx = pd.MultiIndex.from_product([countries, years], names=['country', 'year'])
cy = pd.DataFrame(index=idx).reset_index()
ex = df[df.supplier_type == 'state'].groupby(['supplier_lineage', 'order_year']).agg(exp_deals=('deal_id', 'size'), exp_tiv=('tiv_order', 'sum'),
                                                                                      exp_cats=('category', 'nunique'))
ex.index.names = ['country', 'year']
im = st.groupby(['recipient_lineage', 'order_year']).agg(imp_deals=('deal_id', 'size'), imp_tiv=('tiv_order', 'sum'))
im.index.names = ['country', 'year']
lc = st[st.lic_L1 == 1].groupby(['recipient_lineage', 'order_year']).size().rename('lic_deals')
lc.index.names = ['country', 'year']
cy = cy.merge(ex, on=['country', 'year'], how='left').merge(im, on=['country', 'year'], how='left').merge(lc, on=['country', 'year'], how='left').fillna(0)
cy = cy.sort_values(['country', 'year'])
g = cy.groupby('country')
cy['lic_stock'] = g.lic_deals.cumsum()
cy['imp_stock'] = g.imp_tiv.cumsum()
cy['lic_stock_l5'] = g.lic_stock.shift(5).fillna(0)
cy['imp_stock_l5'] = g.imp_stock.shift(5).fillna(0)
cy['ever_lic_l5'] = (cy.lic_stock_l5 > 0).astype(int)
cy['log_lic_stock_l5'] = np.log1p(cy.lic_stock_l5)
cy['log_imp_stock_l5'] = np.log1p(cy.imp_stock_l5)
cy = cy.merge(ext_l, on=['country', 'year'], how='left')
first_lic = st[st.lic_L1 == 1].groupby('recipient_lineage').order_year.min()
cy['first_lic'] = cy.country.map(first_lic)
cy['rel'] = cy.year - cy.first_lic
cy.to_csv("panel_country_year.csv", index=False)


def ppml(formula, data, label):
    m = smf.glm(formula, data=data, family=sm.families.Poisson()).fit(cov_type='cluster', cov_kwds={'groups': data.country})
    return m


specs = []
S = cy.copy()
m1 = ppml("exp_deals ~ log_lic_stock_l5 + log_imp_stock_l5 + C(country) + C(year)", S, 'B1')
S2 = cy.dropna(subset=EXT)
m2 = ppml("exp_deals ~ log_lic_stock_l5 + log_imp_stock_l5 + log_gdp + log_gdppc + log_milex + C(country) + C(year)", S2, 'B2')
m3 = ppml("exp_deals ~ ever_lic_l5 + log_imp_stock_l5 + log_gdp + log_gdppc + log_milex + C(country) + C(year)", S2, 'B3')
m4 = ppml("exp_cats ~ log_lic_stock_l5 + log_imp_stock_l5 + log_gdp + log_gdppc + log_milex + C(country) + C(year)", S2, 'B4')
print("\n=== Part B: country-year PPML, country & year FE, SE clustered by country ===")
for lab, m, k in [('(B1) export deals ~ log licence stock(t-5), import stock; FE only; 1950+', m1, 'log_lic_stock_l5'),
                  ('(B2) + GDP, GDP pc, Milex (t-1); 1960+', m2, 'log_lic_stock_l5'),
                  ('(B3) ever licensed by t-5 (dummy) instead of stock', m3, 'ever_lic_l5'),
                  ('(B4) outcome = # export categories', m4, 'log_lic_stock_l5')]:
    b, se, p = m.params[k], m.bse[k], m.pvalues[k]
    specs.append(dict(spec=lab, var=k, coef=round(b, 3), se=round(se, 3), p=round(p, 3), semi_elasticity_pct=round((np.exp(b) - 1) * 100, 1), n=int(m.nobs)))
    print(f"{lab}: coef={b:.3f} (se {se:.3f}, p={p:.3f})  n={int(m.nobs)}")
for k in ['log_imp_stock_l5', 'log_gdp', 'log_gdppc', 'log_milex']:
    print(f"   B2 {k}: {m2.params[k]:.3f} (p={m2.pvalues[k]:.3f})")
pd.DataFrame(specs).to_csv("tab_ppml_country_year.csv", index=False)

# ---- event study around first licence (country-year, FE), binned relative time
E = cy[cy.first_lic.notna() | True].copy()
E['relb'] = E.rel.clip(-10, 25)
E.loc[E.first_lic.isna(), 'relb'] = -999   # never-licensed = controls
E['relb'] = E.relb.astype(int)
E = E.dropna(subset=EXT)
E = E[E.country.isin(E.groupby('country').exp_deals.sum().loc[lambda x: x > 0].index)]
E['relb'] = np.where(E.relb == -999, -999, (E.relb // 3) * 3)   # 3-year bins
E['relb_c'] = pd.Categorical(E.relb, categories=sorted(E.relb.unique()))
me = smf.glm("exp_deals ~ C(relb_c, Treatment(reference=-3)) + log_imp_stock_l5 + log_gdp + log_gdppc + log_milex + C(country) + C(year)",
             data=E, family=sm.families.Poisson()).fit(cov_type='cluster', cov_kwds={'groups': E.country})
coefs = []
for k in sorted(E.relb.unique()):
    if k in (-3, -999):
        coefs.append((k, 0.0, 0.0, 0.0)); continue
    name = f"C(relb_c, Treatment(reference=-3))[T.{k}]"
    if name in me.params:
        coefs.append((k, me.params[name], me.conf_int().loc[name, 0], me.conf_int().loc[name, 1]))
es = pd.DataFrame(coefs, columns=['rel', 'coef', 'lo', 'hi'])
es = es[es.rel != -999]
es.to_csv("tab_event_study.csv", index=False)
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.axhline(0, color=INK2, linewidth=0.8); ax.axvline(-0.5, color=INK2, linewidth=0.8, linestyle='--')
ax.fill_between(es.rel, es.lo, es.hi, color=COL['blue'], alpha=0.15, linewidth=0)
ax.plot(es.rel, es.coef, color=COL['blue'], linewidth=2, marker='o', markersize=4)
ax.set_xlabel("Years relative to first licensed-production order"); ax.set_ylabel("Log change in export deals vs. years -3 to -1")
ax.set_title("Fig 7. Event study: export activity around first licence (country & year FE, GDP/Milex controls)", loc='left', fontsize=10, color=INK)
fig.savefig("fig7_event_study.png"); plt.close(fig)
print("\nevent study coefficients (log points):"); print(es.round(2).to_string(index=False))
