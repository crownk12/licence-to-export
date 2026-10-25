"""Build cleaned SIPRI trade-register dataset with licensed-production coding
and weapon-category classification.

Input : data/raw/trade-register.csv (SIPRI export, cp1252)
Output: deals_clean.csv, coding_audit.csv
"""
import re
import pandas as pd
import numpy as np

SRC = "data/raw/trade-register.csv"

df = pd.read_csv(SRC, encoding="cp1252", skiprows=11)
df.columns = ['recipient', 'supplier', 'order_year', 'order_unc', 'n_ordered', 'n_unc',
              'designation', 'description', 'n_delivered', 'deliv_unc', 'deliv_years',
              'status', 'comments', 'tiv_unit', 'tiv_order', 'tiv_delivered']
df['deal_id'] = np.arange(1, len(df) + 1)
for c in ['order_unc', 'n_unc', 'deliv_unc']:
    df[c] = (df[c].astype(str).str.strip() == '?').astype(int)
df['comments'] = df['comments'].fillna('')
df['status'] = df['status'].fillna('New')

# ---------------------------------------------------------------- countries
cm = pd.read_csv("country_map.csv")
cm_d = cm.set_index('sipri_name')


def actor_type(name):
    if name in cm_d.index:
        return cm_d.loc[name, 'actor_type']
    if name.endswith('**'):
        return 'intl_org'
    if name.endswith('*'):
        return 'nonstate'
    if name.startswith('unknown'):
        return 'unknown'
    return 'unmapped'


for side in ['recipient', 'supplier']:
    df[f'{side}_type'] = df[side].map(actor_type)
    df[f'{side}_ccode'] = df[side].map(cm_d['ccode'])
    df[f'{side}_iso3'] = df[side].map(cm_d['iso3'])
    df[f'{side}_lineage'] = df[side].map(cm_d['lineage']).fillna(df[side])

# first/last delivery year
yrs = df['deliv_years'].fillna('').str.findall(r'\d{4}')
df['first_delivery'] = yrs.map(lambda l: int(l[0]) if l else np.nan)
df['last_delivery'] = yrs.map(lambda l: int(l[-1]) if l else np.nan)

# ------------------------------------------------- licensed production coding
c = df['comments'].str.lower()
# normalise spelling
c = c.str.replace('license', 'licence', regex=False).str.replace('licenced', 'licensed', regex=False)

L1_PAT = (r'produc\w*\s+under\s+(?:\w+\s+)?licence'      # produced under (Russian) licence
          r'|licensed\s+produc'                          # licensed production
          r'|production\s+under\s+licence'               # incl production under licence
          r'|under\s+licence')                           # catch-all
# location-based forms: "assembled/produced in X", "Produced in X" (comment starts) -> count only if X == recipient
LOC_PAT = r'(?:assembled\s*(?:/|or)\s*produced\s+(?:in|on)\s+|^(?:probably\s+|possibly\s+)?produced\s+(?:in|on)\s+)([a-z]+(?: [a-z]+)?)'
L2_PAT = r'assembl'                                      # assembled from kits / assembled in / incl assembly
L3_PAT = r'production\s+of\s+(?:\w+\s+)?components|components?\s+produc|produc\w*\s+(?:of\s+)?(?:\w+\s+)?components'
NEG_PAT = r'option\s+on\s+\d+\s+more\s+produced\s+under\s+licence[^;]*not\s+used'

ALIAS = {'usa': 'united states', 'uk': 'united kingdom', 'frg': 'germany', 'west germany': 'germany',
         'gdr': 'east germany', 'turkey': 'turkiye', 'vietnam': 'viet nam', 'czech republic': 'czechia',
         'czechoslovakian': 'czechoslovakia', 'soutk korea': 'south korea', 'itaky': 'italy', 'geramny': 'germany',
         'syra': 'syria', 'south africa': 'south africa', 'new zealand': 'new zealand'}


def loc_is_recipient(loc, recipient):
    if not isinstance(loc, str):
        return False
    loc = ALIAS.get(loc, loc)
    rec = recipient.lower()
    toks = loc.split()
    return loc in rec or (toks[0][:5] in rec) or (len(toks) > 1 and ' '.join(toks[:2]) in rec)


loc_hit = c.str.extract(LOC_PAT)[0]
loc_ok = pd.Series([loc_is_recipient(l, r) for l, r in zip(loc_hit, df['recipient'])], index=df.index)
# audit-driven additions (v0.2):
#  (a) clause-level "; produced in X" (independent clause after a semicolon, not a platform modifier)
#  (b) "N produced in X" (quantity directly modifying 'produced', parallel to 'assembled from kits')
#  (c) noun form "assembly/production in X", "assembly or/and production in X"
LOC2_PAT = (r'(?:;\s*(?:probably\s+|possibly\s+)?produced\s+(?:in|on)\s+'
            r'|\b\d+\s+produced\s+(?:in|on)\s+'
            r'|assembly\s*(?:/|or|and)\s*production\s+(?:in|on)\s+)([a-z]+(?: [a-z]+)?)')
loc2_hit = c.str.extract(LOC2_PAT)[0]
loc2_ok = pd.Series([loc_is_recipient(l, r) for l, r in zip(loc2_hit, df['recipient'])], index=df.index)
df['lic_L1'] = (c.str.contains(L1_PAT, regex=True) | loc_ok | loc2_ok).astype(int)
asm_loc = c.str.extract(r'assembl\w*(?:\s*/\s*produced|\s+or\s+produced)?(?:\s+from\s+kits)?\s+(?:in|on|at)\s+([a-z]+(?: [a-z]+)?)')[0]
asm_ok = pd.Series([loc_is_recipient(l, r) for l, r in zip(asm_loc, df['recipient'])], index=df.index)
df['lic_L2'] = (c.str.contains(L2_PAT, regex=True) & (asm_loc.isna() | asm_ok)).astype(int)
# L3: components, or a named part (warheads, hulls, sections, parts ...) produced in the recipient; when a location is
# named it must be the recipient (adjectival forms such as 'Norwegian production of components' are accepted)
L3_LOC_PAT = r'production\s+of\s+(?:\w+\s+){0,2}(?:components?|parts|warheads|hulls?|sections?|subsystems?|fuselages?|wings|electronics|engines?|turrets?)\s+(?:in|on)\s+([a-z]+(?: [a-z]+)?)'
l3_loc = c.str.extract(L3_LOC_PAT)[0]
l3_loc_ok = pd.Series([loc_is_recipient(l, r) for l, r in zip(l3_loc, df['recipient'])], index=df.index)
l3_generic = c.str.contains(L3_PAT, regex=True) & l3_loc.isna()          # no location named -> accept as before
df['lic_L3'] = (l3_generic | l3_loc_ok).astype(int)
df.loc[df.recipient.str.startswith('unknown'), ['lic_L1', 'lic_L2', 'lic_L3']] = 0   # unmappable recipients: no licence coding
neg = c.str.contains(NEG_PAT, regex=True)
df.loc[neg, 'lic_L1'] = 0
# India-produces-for-France type cases: licensed production located in a third country
loc = c.str.extract(r'produced under licence in ([a-z]+(?: [a-z]+)?)')[0]
third = loc.notna() & ~df.apply(lambda r: isinstance(loc[r.name], str) and (
    loc[r.name].split()[0][:4] in r['recipient'].lower() or loc[r.name] in {'usa', 'uk', 'turkey', 'frg', 'gdr', 'soutk korea', 'itaky', 'geramny', 'syra', 'czechoslovakian', 'india not'}
    or (loc[r.name] == 'india not')), axis=1)
# manual review showed only France<-India AVSIMAR rows are true third-country cases
avsimar = c.str.contains('for france') & c.str.contains('produced under licence in india')
df.loc[avsimar, 'lic_L1'] = 0

df['lic_tier'] = np.select([df.lic_L1 == 1, df.lic_L2 == 1, df.lic_L3 == 1], [1, 2, 3], default=0)
df['lic_any'] = (df.lic_tier > 0).astype(int)
df['lic_uncertain'] = (c.str.contains(r'(?:probably|possibly)\s+(?:\w+\s+){0,2}(?:produced|assembled|under licence)', regex=True) & (df.lic_any == 1)).astype(int)
# partial: only part of the order produced under licence ("incl 95 produced under licence")
df['lic_partial'] = (c.str.contains(r'(?:incl(?:uding)?|in)\s+(?:some\s+|about\s+|up to\s+)?\d+\s+(?:\w+\s+){0,2}(?:produced|assembled)', regex=True) & (df.lic_any == 1)).astype(int)
# 'A or B' forms where SIPRI could not tell the tier apart (e.g. 'production of components or production under licence'):
# flagged so that a conservative coding (lower tier) can be used in robustness checks
df['lic_either'] = (c.str.contains(r'(?:assembl\w*|compo\w+)\s+or\s+(?:produc\w*|production)', regex=True) & (df.lic_L1 == 1)).astype(int)
df['lic_tier_conservative'] = np.where(df.lic_either == 1, np.where(c.str.contains('compo'), 3, 2), df.lic_tier)
df['lic_L1_cons'] = (df.lic_tier_conservative == 1).astype(int)
# supplier-side: item exported from a licensed production line in the supplier (e.g. Polish-built Soviet designs)
df['from_production_line'] = c.str.contains(r'from\s+(?:\w+\s+){1,2}production\s+line', regex=True).astype(int)
df['design_origin_foreign'] = c.str.contains(r'(?:\w+)\s+design(?:ed)?\b|licence\s+from|designed\s+in', regex=True).astype(int)

# --------------------------------------------------- weapon category coding
d = df['description'].str.lower()
rules = [
    ('Satellites',          r'satellite'),
    ('Ships',               r'aircraft carrier|missile boat'),          # exceptions that would otherwise be caught below
    ('Engines',             r'\bengine\b|turbofan|turbojet|turboprop|gas turbine|nuclear reactor'),
    ('Air defence systems', r'surface-to-air missile system|anti-aircraft gun|air-defence system|anti-ballistic missile system|self-propelled air-defence'),
    ('Anti-submarine warfare weapons', r'torpedo(?! boat)|anti-submarine rocket|anti-submarine mortar|anti-submarine missile|naval mine'),
    ('Naval weapons',       r'naval gun|coastal defence gun|naval multiple rocket'),
    ('Missiles',            r'missile|guided bomb|guided glide bomb|guided rocket|guided shell|loitering munition|one-way attack drone|anti-radar|coastal defence system|land-attack'),
    ('Sensors',             r'radar|sonar|electro-optical|signals intelligence system|air-search system|reconnaissance system|surveillance system|signals intelligence.*system'),
    ('Artillery',           r'towed gun|self-propelled gun|mortar|multiple rocket launcher'),
    ('Armoured vehicles',   r'armoured|\btank\b|infantry fighting|fire-support vehicle|ugv'),
    ('Aircraft',            r'aircraft|helicopter|drone|airship|bomber|air refuel'),
    ('Ships',               r'ship|boat|frigate|destroyer|corvette|submarine|craft|cruiser|minesweeper|minehunter|minelayer|tug|tanker|carrier|icebreaker|gunboat|replenishment'),
]


def classify(desc):
    for cat, pat in rules:
        if re.search(pat, desc):
            return cat
    return 'Other'


df['category'] = d.map(classify)
# fix: turrets/chassis are subsystems even though matched to armoured vehicles/artillery
df['is_turret_chassis'] = d.str.contains(r'turret|chassis').astype(int)
df['uav'] = d.str.contains(r'drone|loitering|ugv').astype(int)

platform_cats = {'Aircraft', 'Armoured vehicles', 'Ships'}
weapon_cats = {'Missiles', 'Artillery', 'Air defence systems', 'Anti-submarine warfare weapons', 'Naval weapons'}
df['tier3'] = np.where(df.is_turret_chassis == 1, 'subsystem',
              np.where(df.category.isin(platform_cats), 'platform',
              np.where(df.category.isin(weapon_cats), 'weapon', 'subsystem')))
df['platform'] = (df.tier3 == 'platform').astype(int)

df.to_csv("deals_clean.csv", index=False)

# audit sample for manual validation of coding
rng = np.random.default_rng(42)
aud = pd.concat([
    df[df.lic_tier == 1].sample(40, random_state=1),
    df[df.lic_tier == 2].sample(20, random_state=1),
    df[df.lic_tier == 3].sample(20, random_state=1),
    df[(df.lic_tier == 0) & c.str.contains('produc|licen|assembl')].sample(40, random_state=1),
])[['deal_id', 'recipient', 'supplier', 'order_year', 'description', 'category', 'tier3', 'lic_tier', 'lic_uncertain', 'lic_partial', 'comments']]
aud['manual_check'] = ''
aud.to_csv("coding_audit.csv", index=False)

print(df.shape)
print(df.lic_tier.value_counts().sort_index())
print(df.category.value_counts())
print(df.tier3.value_counts())
print("recipient types:", df.recipient_type.value_counts().to_dict())
print("supplier types:", df.supplier_type.value_counts().to_dict())
print("unmapped:", sorted(set(df.loc[df.recipient_type == 'unmapped', 'recipient']) | set(df.loc[df.supplier_type == 'unmapped', 'supplier'])))
