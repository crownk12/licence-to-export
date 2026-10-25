"""Exploratory analysis: licensed production -> subsequent exports.
Builds country(lineage) x weapon-category panel of first import, first licence, first export,
and produces descriptive figures + Kaplan-Meier curves."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

C = {'blue': '#2a78d6', 'orange': '#eb6834', 'aqua': '#1baf7a', 'yellow': '#eda100',
     'magenta': '#e87ba4', 'green': '#008300', 'violet': '#6250d6', 'red': '#e34948'}
INK, INK2, GRID = '#0b0b0b', '#52514e', '#e4e3df'
plt.rcParams.update({'font.size': 10, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6, 'axes.axisbelow': True,
                     'figure.dpi': 150, 'savefig.dpi': 200, 'savefig.bbox': 'tight', 'legend.frameon': False})
END = 2025

df = pd.read_csv("deals_clean.csv")
st = df[(df.recipient_type == 'state')].copy()               # state recipients
st_sup = df[(df.supplier_type == 'state')].copy()            # state suppliers (for exports)

# ------------------------------------------------------------ Fig 1: licensed deals by decade & tier
st['decade'] = (st.order_year // 10 * 10).clip(lower=1950)
tab = st[st.lic_tier > 0].groupby(['decade', 'lic_tier']).size().unstack(fill_value=0)
share = st.groupby('decade').lic_any.mean() * 100
fig, ax = plt.subplots(figsize=(7.5, 3.8))
bottom = np.zeros(len(tab))
labels = {1: 'Licensed production', 2: 'Local assembly / kits', 3: 'Component production / offsets'}
cols = {1: C['blue'], 2: C['orange'], 3: C['aqua']}
x = np.arange(len(tab))
for t in [1, 2, 3]:
    ax.bar(x, tab[t], bottom=bottom, color=cols[t], width=0.7, label=labels[t], edgecolor='white', linewidth=1)
    bottom += tab[t].values
for i, (d, s) in enumerate(share.items()):
    ax.text(i, bottom[i] + 6, f"{s:.1f}%", ha='center', color=INK2, fontsize=8.5)
ax.set_xticks(x); ax.set_xticklabels([f"{d}s" for d in tab.index])
ax.set_ylabel("Deals with local production content (orders)")
ax.set_title("Fig 1. Local-production deals by decade and tier (labels: % of all deals)", loc='left', fontsize=10.5, color=INK)
ax.legend(loc='upper left', fontsize=8.5)
fig.savefig("fig1_licensed_by_decade.png"); plt.close(fig)

# ------------------------------------------------------------ Fig 2: by weapon category (count + share)
cat = st.groupby('category').agg(n=('deal_id', 'size'), lic=('lic_L1', 'sum'), any=('lic_any', 'sum'))
cat['share_L1'] = cat.lic / cat.n * 100
cat['share_any'] = cat['any'] / cat.n * 100
cat = cat.sort_values('share_L1')
tier_of = st.groupby('category').tier3.agg(lambda s: s.mode()[0])
fig, ax = plt.subplots(figsize=(7.5, 4.2))
colors = [{'platform': C['blue'], 'weapon': C['orange'], 'subsystem': C['aqua']}[tier_of[c]] for c in cat.index]
ax.barh(cat.index, cat.share_L1, color=colors, height=0.65)
for i, (c_, r) in enumerate(cat.iterrows()):
    ax.text(r.share_L1 + 0.3, i, f"{r.share_L1:.1f}%  (n={int(r.lic)} of {int(r.n)})", va='center', fontsize=8.5, color=INK2)
ax.set_xlabel("Share of deals produced under licence by recipient (%)")
ax.set_xlim(0, cat.share_L1.max() * 1.45)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=C['blue'], label='Platform'), Patch(color=C['orange'], label='Complete weapon'),
                   Patch(color=C['aqua'], label='Subsystem / component')], loc='lower right', fontsize=8.5)
ax.set_title("Fig 2. Licensed-production intensity by weapon category, 1950-2025", loc='left', fontsize=10.5, color=INK)
fig.savefig("fig2_licence_share_by_category.png"); plt.close(fig)

# ------------------------------------------------------------ Fig 3: top recipients & suppliers of licensed production
l1 = st[st.lic_L1 == 1]
top_r = l1.groupby('recipient_lineage').size().sort_values().tail(15)
top_s = l1[l1.supplier_type == 'state'].groupby('supplier_lineage').size().sort_values().tail(10)
fig, axes = plt.subplots(1, 2, figsize=(9, 4))
axes[0].barh(top_r.index, top_r.values, color=C['blue'], height=0.65)
axes[0].set_title("Recipients (licensees)", loc='left', fontsize=10, color=INK)
axes[1].barh(top_s.index, top_s.values, color=C['orange'], height=0.65)
axes[1].set_title("Suppliers (licensors)", loc='left', fontsize=10, color=INK)
for ax, s in zip(axes, [top_r, top_s]):
    for i, v in enumerate(s.values):
        ax.text(v + 1, i, str(v), va='center', fontsize=8.5, color=INK2)
    ax.set_xlabel("Licensed-production deals")
fig.suptitle("Fig 3. Who licenses to whom, 1950-2025 (deals with recipient-side licensed production)", x=0.01, ha='left', fontsize=10.5, color=INK)
fig.tight_layout()
fig.savefig("fig3_top_licensees_licensors.png"); plt.close(fig)

# ------------------------------------------------------------ Panel: lineage x category
imp = st.groupby(['recipient_lineage', 'category']).agg(first_import=('order_year', 'min'),
                                                        n_import=('deal_id', 'size'),
                                                        tiv_import=('tiv_delivered', 'sum'))
lic = st[st.lic_L1 == 1].groupby(['recipient_lineage', 'category']).agg(first_lic=('order_year', 'min'), n_lic=('deal_id', 'size'))
lic_any = st[st.lic_any == 1].groupby(['recipient_lineage', 'category']).agg(first_lic_any=('order_year', 'min'))
exp = st_sup.groupby(['supplier_lineage', 'category']).agg(first_export=('order_year', 'min'), n_export=('deal_id', 'size'))
exp.index.names = ['recipient_lineage', 'category']
panel = imp.join(lic, how='left').join(lic_any, how='left').join(exp, how='left').reset_index()
panel = panel.rename(columns={'recipient_lineage': 'country'})
panel['tier3'] = panel.category.map(st.groupby('category').tier3.agg(lambda s: s.mode()[0]))
panel['licensed'] = panel.first_lic.notna().astype(int)
# event definition: first export strictly after first import (country was not already exporting in this category)
panel['pre_exporter'] = (panel.first_export <= panel.first_import).fillna(False).astype(int)
panel['event'] = ((panel.first_export > panel.first_import) & panel.first_export.notna()).astype(int)
panel['duration'] = np.where(panel.event == 1, panel.first_export - panel.first_import, END - panel.first_import)
# for licensed group: time from first licence
panel['dur_lic'] = np.where(panel.event == 1, panel.first_export - panel.first_lic, END - panel.first_lic)
panel['lic_before_export'] = ((panel.licensed == 1) & ((panel.first_export.isna()) | (panel.first_lic < panel.first_export))).astype(int)
panel.to_csv("panel_country_category.csv", index=False)

# analysis sample: not already exporting at first import; duration>0
S = panel[(panel.pre_exporter == 0) & (panel.duration >= 0)].copy()
S.loc[S.duration == 0, 'duration'] = 0.5
print("panel rows:", len(panel), " analysis sample:", len(S), " licensed:", S.licensed.sum(), " events:", S.event.sum())
print(S.groupby('licensed').event.agg(['size', 'sum', 'mean']))
print(S.groupby(['tier3', 'licensed']).event.agg(['size', 'sum', 'mean']))

# ------------------------------------------------------------ Fig 4: KM licensed vs non-licensed importers
kmf = KaplanMeierFitter()
fig, ax = plt.subplots(figsize=(7, 4))
for lab, g, col in [('Licensed production in category', S[S.licensed == 1], C['blue']),
                    ('Imports only (no licence)', S[S.licensed == 0], C['orange'])]:
    kmf.fit(g.duration, g.event, label=f"{lab} (n={len(g)})")
    kmf.plot_cumulative_density(ax=ax, color=col, linewidth=2, ci_alpha=0.12)
lr = logrank_test(S[S.licensed == 1].duration, S[S.licensed == 0].duration, S[S.licensed == 1].event, S[S.licensed == 0].event)
ax.set_xlabel("Years since first import in weapon category"); ax.set_ylabel("Cumulative probability of first export")
ax.set_xlim(0, 60); ax.set_ylim(0, 1)
ax.set_title(f"Fig 4. Time from first import to first export, by licensed production (log-rank p={lr.p_value:.2g})", loc='left', fontsize=10, color=INK)
ax.legend(loc='upper left', fontsize=8.5)
fig.savefig("fig4_km_licensed_vs_not.png"); plt.close(fig)

# ------------------------------------------------------------ Fig 5: KM by tier3 within licensed group
fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True)
for ax, t in zip(axes, ['platform', 'weapon', 'subsystem']):
    g = S[S.tier3 == t]
    for lab, gg, col in [('Licensed', g[g.licensed == 1], C['blue']), ('Imports only', g[g.licensed == 0], C['orange'])]:
        if len(gg) == 0:
            continue
        kmf.fit(gg.duration, gg.event, label=f"{lab} (n={len(gg)})")
        kmf.plot_cumulative_density(ax=ax, color=col, linewidth=2, ci_alpha=0.12)
    ax.set_title({'platform': 'Platforms', 'weapon': 'Complete weapons', 'subsystem': 'Subsystems / components'}[t], loc='left', fontsize=10, color=INK)
    ax.set_xlim(0, 60); ax.set_ylim(0, 1); ax.set_xlabel("Years since first import"); ax.legend(fontsize=8, loc='upper left')
axes[0].set_ylabel("Cum. probability of first export")
fig.suptitle("Fig 5. Same comparison by weapon tier", x=0.01, ha='left', fontsize=10.5, color=INK)
fig.tight_layout()
fig.savefig("fig5_km_by_tier.png"); plt.close(fig)

# ------------------------------------------------------------ Fig 6: country-level - first licence (any) -> first export (any), platform vs non-platform licensees
cl = st[st.lic_L1 == 1].groupby('recipient_lineage').agg(first_lic=('order_year', 'min'))
ce = st_sup.groupby('supplier_lineage').agg(first_export=('order_year', 'min'))
cl = cl.join(ce)
cl['event'] = (cl.first_export > cl.first_lic).fillna(False).astype(int)
cl['already'] = (cl.first_export <= cl.first_lic).fillna(False).astype(int)
cl['duration'] = np.where(cl.event == 1, cl.first_export - cl.first_lic, END - cl.first_lic)
cl2 = cl[cl.already == 0]
print("\ncountry-level licensees:", len(cl), " already exporting at first licence:", cl.already.sum(), " at risk:", len(cl2), " later exported:", cl2.event.sum())
print(cl2.sort_values('first_lic')[['first_lic', 'first_export', 'event', 'duration']].to_string())

# ------------------------------------------------------------ summary tables
st[st.lic_L1 == 1].groupby('category').size().rename('licensed_deals').to_csv("tab_licensed_by_category.csv")
pd.DataFrame({'share_L1_pct': cat.share_L1.round(1), 'share_any_pct': cat.share_any.round(1), 'n_deals': cat.n}).to_csv("tab_share_by_category.csv")
S.groupby(['tier3', 'licensed']).agg(n=('event', 'size'), exported=('event', 'sum'), median_years=('duration', 'median')).to_csv("tab_km_summary.csv")
print("\ndone")

# ============================================================ Correct exposure timing
# 79 of 223 licensed pairs exported BEFORE their first licence -> licence must be treated as time-varying.
S2 = S.copy()
S2['lic_before'] = ((S2.licensed == 1) & ((S2.first_export.isna()) | (S2.first_lic < S2.first_export))).astype(int)
print("\nExposure re-defined: licensed BEFORE export/censoring:", S2.lic_before.sum(), " licensed only after export:", ((S2.licensed == 1) & (S2.lic_before == 0)).sum())
print(S2.groupby('lic_before').event.agg(['size', 'sum', 'mean']))
print(S2.groupby(['tier3', 'lic_before']).event.agg(['size', 'sum', 'mean']))

fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True)
for ax, t in zip(axes, ['platform', 'weapon', 'subsystem']):
    g = S2[S2.tier3 == t]
    for lab, gg, col in [('Licence before any export', g[g.lic_before == 1], C['blue']), ('No prior licence', g[g.lic_before == 0], C['orange'])]:
        kmf.fit(gg.duration, gg.event, label=f"{lab} (n={len(gg)})")
        kmf.plot_cumulative_density(ax=ax, color=col, linewidth=2, ci_alpha=0.12)
    ax.set_title({'platform': 'Platforms', 'weapon': 'Complete weapons', 'subsystem': 'Subsystems / components'}[t], loc='left', fontsize=10, color=INK)
    ax.set_xlim(0, 60); ax.set_ylim(0, 1); ax.set_xlabel("Years since first import"); ax.legend(fontsize=8, loc='upper left')
axes[0].set_ylabel("Cum. probability of first export")
fig.suptitle("Fig 6. Exposure = licence obtained before first export (pairs exporting before licence moved to control)", x=0.01, ha='left', fontsize=10.5, color=INK)
fig.tight_layout(); fig.savefig("fig6_km_by_tier_licence_before.png"); plt.close(fig)

# --- Cox model with time-varying licence exposure (country-category pairs, calendar-year splits)
from lifelines import CoxTimeVaryingFitter
rows = []
for _, r in S2.iterrows():
    start, stop = r.first_import, r.first_import + r.duration
    if r.licensed == 1 and r.first_lic < stop and r.first_lic > start:
        rows.append(dict(id=f"{r.country}|{r.category}", t0=0, t1=r.first_lic - start, lic=0, ev=0, tier3=r.tier3, cohort=start))
        rows.append(dict(id=f"{r.country}|{r.category}", t0=r.first_lic - start, t1=stop - start, lic=1, ev=r.event, tier3=r.tier3, cohort=start))
    else:
        rows.append(dict(id=f"{r.country}|{r.category}", t0=0, t1=stop - start, lic=int(r.licensed == 1 and r.first_lic <= start), ev=r.event, tier3=r.tier3, cohort=start))
tv = pd.DataFrame(rows)
tv = tv[tv.t1 > tv.t0]
tv['platform'] = (tv.tier3 == 'platform').astype(int)
tv['weapon'] = (tv.tier3 == 'weapon').astype(int)
tv['lic_x_platform'] = tv.lic * tv.platform
tv['lic_x_weapon'] = tv.lic * tv.weapon
tv['cohort_c'] = (tv.cohort - 1980) / 10
ctv = CoxTimeVaryingFitter(penalizer=0)
ctv.fit(tv[['id', 't0', 't1', 'ev', 'lic', 'platform', 'weapon', 'cohort_c']], id_col='id', start_col='t0', stop_col='t1', event_col='ev')
print("\n=== Cox (time-varying licence), main effect ===")
print(ctv.summary[['coef', 'exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].round(3))
ctv2 = CoxTimeVaryingFitter(penalizer=0)
ctv2.fit(tv[['id', 't0', 't1', 'ev', 'lic', 'platform', 'weapon', 'lic_x_platform', 'lic_x_weapon', 'cohort_c']], id_col='id', start_col='t0', stop_col='t1', event_col='ev')
print("\n=== Cox (time-varying licence), interactions with tier (ref = subsystem) ===")
print(ctv2.summary[['coef', 'exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].round(3))
ctv.summary.to_csv("tab_cox_main.csv"); ctv2.summary.to_csv("tab_cox_interaction.csv")
tv.to_csv("panel_timevarying.csv", index=False)
