"""Build country(lineage) x year panel of external controls: SIPRI Milex (constant 2024 USD, millions),
World Bank GDP (constant 2015 USD) and GDP per capita."""
import pandas as pd
import numpy as np
import glob

cm = pd.read_csv("country_map.csv")
lineage_iso = cm.drop_duplicates('lineage').set_index('lineage')['iso3']
# WB codes for lineages: Russia -> RUS (post-1991 only), Czechia -> CZE, Serbia -> SRB, Yemen -> YEM, Vietnam -> VNM
lineage_iso.update({'Russia': 'RUS', 'Czechia': 'CZE', 'Serbia': 'SRB', 'Yemen': 'YEM', 'Vietnam': 'VNM', 'Germany': 'DEU',
                    'Kosovo': 'XKX', 'Timor-Leste': 'TLS', 'Eswatini': 'SWZ'})

# ---- Milex
x = pd.ExcelFile("data/raw/SIPRI-Milex-data-1949-2025.xlsx")
raw = pd.read_excel(x, 'Constant (2024) US$', header=None)
hdr = raw.index[raw.iloc[:, 0].astype(str).str.strip() == 'Country'][0]
mx = pd.read_excel(x, 'Constant (2024) US$', header=hdr)
mx = mx[mx['Country'].notna()].copy()
mx['Country'] = mx['Country'].astype(str).str.strip()
MILEX_MAP = {'Cape Verde': 'Cabo Verde', 'Congo, DR': 'DR Congo', 'Congo, Republic': 'Republic of the Congo', 'Gambia, The': 'Gambia',
             'German Democratic Republic': 'East Germany', 'Korea, North': 'North Korea', 'Korea, South': 'South Korea',
             'Kyrgyz Republic': 'Kyrgyzstan', 'Timor Leste': 'Timor-Leste', 'Türkiye': 'Turkiye', 'USSR': 'Russia',
             'United States of America': 'United States', 'Yemen, North': 'Yemen', 'Viet Nam': 'Vietnam'}
mx['lineage'] = mx['Country'].map(lambda s: MILEX_MAP.get(s, s))
yrs = [c for c in mx.columns if isinstance(c, (int, np.integer))]
ml = mx.melt(id_vars=['lineage'], value_vars=yrs, var_name='year', value_name='milex')
ml['milex'] = pd.to_numeric(ml['milex'], errors='coerce')   # '...' and 'xxx' -> NaN
ml = ml.dropna(subset=['milex'])
# Russia lineage: USSR rows (<=1991) and Russia rows (>=1992) both map to 'Russia'; keep one per year (prefer non-missing, larger)
ml = ml.sort_values('milex', ascending=False).drop_duplicates(['lineage', 'year'])

# ---- World Bank
def wb(path_glob, name):
    f = glob.glob(path_glob)[0]
    d = pd.read_csv(f, skiprows=4)
    ycols = [c for c in d.columns if c.isdigit()]
    m = d.melt(id_vars=['Country Code'], value_vars=ycols, var_name='year', value_name=name)
    m['year'] = m.year.astype(int)
    return m.dropna(subset=[name]).rename(columns={'Country Code': 'iso3'})

gdp = wb("data/raw/API_NY.GDP.MKTP.KD*.csv", 'gdp').merge(wb("data/raw/API_NY.GDP.PCAP.KD*.csv", 'gdppc'), on=['iso3', 'year'], how='outer')
iso_lin = {v: k for k, v in lineage_iso.dropna().items()}
gdp['lineage'] = gdp.iso3.map(iso_lin)
gdp = gdp.dropna(subset=['lineage'])

ext = ml.merge(gdp[['lineage', 'year', 'gdp', 'gdppc']], on=['lineage', 'year'], how='outer')
ext['year'] = ext.year.astype(int)
ext = ext.sort_values(['lineage', 'year'])
ext['log_milex'] = np.log(ext.milex.where(ext.milex > 0))
ext['log_gdp'] = np.log(ext.gdp)
ext['log_gdppc'] = np.log(ext.gdppc)
ext.to_csv("ext_panel.csv", index=False)
print(ext.shape, ext.lineage.nunique())
print("coverage by var:", ext[['milex', 'gdp', 'gdppc']].notna().sum().to_dict())
print(ext.groupby(ext.year // 10 * 10)[['milex', 'gdp', 'gdppc']].apply(lambda g: g.notna().sum()))
