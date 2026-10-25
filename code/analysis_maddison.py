"""Extend external controls to 1950 with Maddison Project Database 2023 and re-estimate
the externally controlled Cox and PPML models on the full 1950-2025 sample."""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from lifelines import CoxTimeVaryingFitter
import statsmodels.api as sm
import statsmodels.formula.api as smf

END = 2025
cm = pd.read_csv("country_map.csv")
iso_lin = {r.iso3: r.lineage for r in cm.dropna(subset=['iso3']).drop_duplicates('lineage').itertuples()}
iso_lin.update({'RUS': 'Russia', 'CZE': 'Czechia', 'SRB': 'Serbia', 'YEM': 'Yemen', 'VNM': 'Vietnam', 'DEU': 'Germany'})

md = pd.read_excel("data/raw/mpd2023_web.xlsx", 'Full data')
md = md[md.year >= 1950].dropna(subset=['gdppc']).copy()
# successor lineages: use predecessor code up to break-up year, successor after
code_year = {('SUN', 1991), ('CSK', 1992), ('YUG', 1991)}
md['lineage'] = md.countrycode.map(iso_lin)
md.loc[md.countrycode == 'SUN', 'lineage'] = 'Russia'
md.loc[md.countrycode == 'CSK', 'lineage'] = 'Czechia'
md.loc[md.countrycode == 'YUG', 'lineage'] = 'Serbia'
md = md[~((md.countrycode == 'SUN') & (md.year > 1991)) & ~((md.countrycode == 'RUS') & (md.year <= 1991))
        & ~((md.countrycode == 'CSK') & (md.year > 1992)) & ~((md.countrycode == 'CZE') & (md.year <= 1992))
        & ~((md.countrycode == 'YUG') & (md.year > 1991)) & ~((md.countrycode == 'SRB') & (md.year <= 1991))]
md = md.dropna(subset=['lineage'])
md['gdp_m'] = md.gdppc * md['pop']            # 2011 int$ x thousands of people
md = md[['lineage', 'year', 'gdppc', 'gdp_m']].rename(columns={'gdppc': 'gdppc_m'})
md = md.drop_duplicates(['lineage', 'year'])

# extend 2023-2025 with World Bank growth rates where available, else carry forward
ext = pd.read_csv("ext_panel.csv")
wb = ext[['lineage', 'year', 'gdp', 'gdppc']].copy()
rows = []
for lin, g in md.groupby('lineage'):
    g = g.sort_values('year')
    last = g.iloc[-1]
    if last.year < END:
        w = wb[wb.lineage == lin].set_index('year')
        gm, pm = last.gdp_m, last.gdppc_m
        for y in range(int(last.year) + 1, END + 1):
            if y in w.index and (y - 1) in w.index and pd.notna(w.loc[y, 'gdp']) and pd.notna(w.loc[y - 1, 'gdp']):
                gm *= w.loc[y, 'gdp'] / w.loc[y - 1, 'gdp']; pm *= w.loc[y, 'gdppc'] / w.loc[y - 1, 'gdppc']
            rows.append(dict(lineage=lin, year=y, gdppc_m=pm, gdp_m=gm))
md = pd.concat([md, pd.DataFrame(rows)], ignore_index=True)
md['log_gdp_m'] = np.log(md.gdp_m); md['log_gdppc_m'] = np.log(md.gdppc_m)
ext = ext.drop(columns=[c for c in ['gdppc_m', 'gdp_m', 'log_gdp_m', 'log_gdppc_m'] if c in ext.columns]).merge(md, on=['lineage', 'year'], how='outer')
ext.to_csv("ext_panel.csv", index=False)
print("Maddison coverage by decade:", ext.groupby(ext.year // 10 * 10).log_gdppc_m.count().to_dict())

ext_l = ext.copy(); ext_l['year'] = ext_l.year + 1
ext_l = ext_l[['lineage', 'year', 'log_milex', 'log_gdp_m', 'log_gdppc_m']].rename(columns={'lineage': 'country'})

# ---------------- Part A with Maddison, 1950+
tv = pd.read_csv("panel_yearly_base.csv")
tv['year'] = (tv.cohort + tv.t0).astype(int)
tv = tv.merge(ext_l, on=['country', 'year'], how='left')
tv['lic_US'] = (tv.bloc == 'US').astype(int); tv['lic_nonUS'] = ((tv.lic == 1) & (tv.bloc != 'US')).astype(int)


def fit(d, covs, strata=None, label='', key='lic'):
    m = CoxTimeVaryingFitter(penalizer=0)
    d = d.dropna(subset=covs)
    m.fit(d[['id', 't0', 't1', 'ev'] + covs + ([strata] if strata else [])], id_col='id', start_col='t0', stop_col='t1', event_col='ev', strata=strata)
    s = m.summary
    return [dict(spec=label, var=k, n_pairs=d.id.nunique(), events=int(d.ev.sum()), HR=round(s.loc[k, 'exp(coef)'], 2),
                 lo=round(s.loc[k, 'exp(coef) lower 95%'], 2), hi=round(s.loc[k, 'exp(coef) upper 95%'], 2), p=round(s.loc[k, 'p'], 3))
            for k in ([key] if isinstance(key, str) else key)], s


BASE = ['lic', 'platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat']
EXTM = ['log_gdp_m', 'log_gdppc_m', 'log_milex']
res = []
sub = tv.dropna(subset=EXTM)
r, _ = fit(sub, BASE, label='(M1) Internal controls, Maddison sample 1950+'); res += r
r, sM2 = fit(sub, BASE + EXTM, label='(M2) + log GDP, log GDP pc (Maddison), log Milex'); res += r
r, _ = fit(sub, BASE + EXTM, strata='country', label='(M3) + country-stratified'); res += r
r, _ = fit(sub, ['lic_US', 'lic_nonUS', 'platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat'] + EXTM, label='(M4) US vs non-US, pooled', key=['lic_US', 'lic_nonUS']); res += r
r, _ = fit(sub, ['lic_US', 'lic_nonUS', 'platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat'] + EXTM, strata='country', label='(M5) US vs non-US, stratified', key=['lic_US', 'lic_nonUS']); res += r
resM = pd.DataFrame(res); print(resM.to_string(index=False)); resM.to_csv("tab_cox_maddison.csv", index=False)
print(sM2[['exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].round(3))

# ---------------- Part B with Maddison, 1950+
cy = pd.read_csv("panel_country_year.csv").drop(columns=['log_milex', 'log_gdp', 'log_gdppc'], errors='ignore')
cy = cy.merge(ext_l, on=['country', 'year'], how='left')
S2 = cy.dropna(subset=EXTM)
out = []
for lab, f, k in [('(MB2) export deals ~ log licence stock(t-5) + Maddison GDP, GDP pc, Milex; 1950+', "exp_deals ~ log_lic_stock_l5 + log_imp_stock_l5 + log_gdp_m + log_gdppc_m + log_milex + C(country) + C(year)", 'log_lic_stock_l5'),
                  ('(MB3) any licence by t-5', "exp_deals ~ ever_lic_l5 + log_imp_stock_l5 + log_gdp_m + log_gdppc_m + log_milex + C(country) + C(year)", 'ever_lic_l5'),
                  ('(MB4) outcome = # export categories', "exp_cats ~ log_lic_stock_l5 + log_imp_stock_l5 + log_gdp_m + log_gdppc_m + log_milex + C(country) + C(year)", 'log_lic_stock_l5')]:
    m = smf.glm(f, data=S2, family=sm.families.Poisson()).fit(cov_type='cluster', cov_kwds={'groups': S2.country})
    out.append(dict(spec=lab, var=k, coef=round(m.params[k], 3), se=round(m.bse[k], 3), p=round(m.pvalues[k], 3), n=int(m.nobs)))
    print(lab, f"coef={m.params[k]:.3f} se={m.bse[k]:.3f} p={m.pvalues[k]:.3f} n={int(m.nobs)}")
pd.DataFrame(out).to_csv("tab_ppml_maddison.csv", index=False)

# ---------------- event study 1950+
E = cy.dropna(subset=EXTM).copy()
E = E[E.country.isin(E.groupby('country').exp_deals.sum().loc[lambda x: x > 0].index)]
E['relb'] = E.rel.clip(-12, 25)
E['relb'] = np.where(E.first_lic.isna(), -999, (E.relb // 3) * 3).astype(int)
E['relb_c'] = pd.Categorical(E.relb, categories=sorted(E.relb.unique()))
me = smf.glm("exp_deals ~ C(relb_c, Treatment(reference=-3)) + log_imp_stock_l5 + log_gdp_m + log_gdppc_m + log_milex + C(country) + C(year)",
             data=E, family=sm.families.Poisson()).fit(cov_type='cluster', cov_kwds={'groups': E.country})
es = []
for k in sorted(E.relb.unique()):
    if k in (-3, -999): es.append((k, 0, 0, 0)); continue
    nm = f"C(relb_c, Treatment(reference=-3))[T.{k}]"
    if nm in me.params: es.append((k, me.params[nm], me.conf_int().loc[nm, 0], me.conf_int().loc[nm, 1]))
es = pd.DataFrame(es, columns=['rel', 'coef', 'lo', 'hi']); es = es[es.rel != -999]
es.to_csv("tab_event_study_maddison.csv", index=False)
print("\nevent study 1950+ (Maddison):"); print(es.round(2).to_string(index=False))
print("licensed countries in window:", E[E.first_lic.notna()].country.nunique())
