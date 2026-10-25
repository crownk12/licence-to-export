"""Country-cluster bootstrap CIs for the licence HR in pooled Cox models (Table 1 cols 1, 2, 4)."""
import pandas as pd, numpy as np, warnings, sys
warnings.filterwarnings("ignore")
from lifelines import CoxTimeVaryingFitter
B = int(sys.argv[1]) if len(sys.argv) > 1 else 200
rng = np.random.default_rng(2026)
tv = pd.read_csv("panel_yearly_base.csv"); tv['cohort_c'] = (tv.cohort - 1980) / 10
tv['year'] = (tv.cohort + tv.t0).astype(int)
ext = pd.read_csv("ext_panel.csv").rename(columns={'lineage': 'country'})[['country', 'year', 'log_milex', 'log_gdp_m', 'log_gdppc_m']]; ext['year'] += 1
tv4 = tv.merge(ext, on=['country', 'year'], how='left').dropna(subset=['log_milex', 'log_gdp_m', 'log_gdppc_m'])
specs = {'col1': (tv, ['lic', 'platform', 'weapon', 'cohort_c']),
         'col2': (tv, ['lic', 'platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat']),
         'col4': (tv4, ['lic', 'platform', 'weapon', 'cohort_c', 'log_cum_tiv', 'n_cat', 'log_gdp_m', 'log_gdppc_m', 'log_milex'])}


def coef(d, covs):
    m = CoxTimeVaryingFitter(penalizer=0)
    m.fit(d[['id', 't0', 't1', 'ev'] + covs], id_col='id', start_col='t0', stop_col='t1', event_col='ev')
    return m.params_['lic']


out = {}
for name, (d, covs) in specs.items():
    countries = d.country.unique(); groups = {c: g for c, g in d.groupby('country')}
    point = coef(d, covs); draws = []
    for b in range(B):
        samp = rng.choice(countries, size=len(countries), replace=True)
        parts = []
        for k, c in enumerate(samp):
            g = groups[c].copy(); g['id'] = g['id'] + f"#{k}"; parts.append(g)
        try:
            draws.append(coef(pd.concat(parts), covs))
        except Exception:
            pass
    draws = np.array(draws); se = draws.std(ddof=1)
    lo, hi = np.exp(np.percentile(draws, [2.5, 97.5]))
    z = point / se
    from scipy.stats import norm
    p = 2 * (1 - norm.cdf(abs(z)))
    out[name] = dict(HR=np.exp(point), se_log=se, lo_pct=lo, hi_pct=hi, lo_norm=np.exp(point - 1.96 * se), hi_norm=np.exp(point + 1.96 * se), p=p, B=len(draws))
    print(name, {k: round(float(v), 3) for k, v in out[name].items()}, flush=True)
pd.DataFrame(out).T.to_csv("tab_cluster_bootstrap.csv")
