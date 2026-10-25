# licence-to-export


Replication package for the manuscript below. Repository: https://github.com/crownk12/licence-to-export
Code and derived data for the manuscript *Does Licensed Production Build Arms Exporters? Evidence from 75 Years of Major-Arms Transfers* (submitted to *Defence and Peace Economics*).

**Authors.** Wonkyun Yim, Yoseob Cho, Seokjoong Kang (Graduate School of Management of Technology, Korea University). Corresponding author: Seokjoong Kang (sjkang64@korea.ac.kr); correspondence on this repository: Wonkyun Yim (yimwk88@korea.ac.kr).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23634082.svg)](https://doi.org/10.5281/zenodo.23634082)

**Citation.** Yim, Wonkyun, Yoseob Cho, and Seokjoong Kang. 2026. *licence-to-export: replication package for "Does Licensed Production Build Arms Exporters? Evidence from 75 Years of Major-Arms Transfers"* (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.23634082

## What is here

| Folder | Contents |
|---|---|
| `code/` | Python scripts that build the dataset and estimate every model in the paper (see *Reproduction order*) |
| `data/derived/` | Panels derived from the sources below: country × weapon-category panel, country × year panel, the annual pair-year file used by the Cox models, and the country-name mapping table |
| `data/audit/` | 120-record audit sample of the licensed-production coding, the independent coder's results, and the coding instructions |
| `output/tables/` | Estimation results as CSV (`tab_*.csv`) |
| `output/figures/` | Figures (`fig*.png`) |
| `docs/CODEBOOK.md` | Variable definitions, coding rules (v0.2), weapon-category classification, successor-state treatment |

## Source data (not redistributed)

The raw files are **not** included because their providers do not permit redistribution. Download them as described and place them in `data/raw/`:

| Source | File | Extraction used in the paper | Where |
|---|---|---|---|
| SIPRI Arms Transfers Database | Trade register, all suppliers → all recipients, deliveries any year; CSV export | 24 Oct 2026 (database update of 9 Mar 2026, data 1950–2025) | https://doi.org/10.55163/SAFC1241 |
| SIPRI Military Expenditure Database | `SIPRI-Milex-data-1949-2025.xlsx`, sheet "Constant (2024) US$" | 2026 edition, file revised 27 Apr 2026 | https://doi.org/10.55163/CQGC9685 |
| Maddison Project Database 2023 | `mpd2023_web.xlsx`, sheet "Full data" | Version 1.0 (Apr 2024) | https://doi.org/10.34894/INZBF2 |
| World Bank WDI | `API_NY.GDP.MKTP.KD_*.csv`, `API_NY.GDP.PCAP.KD_*.csv` | Database update of 8 Oct 2026 | https://data.worldbank.org/indicator/NY.GDP.MKTP.KD , …/NY.GDP.PCAP.KD |

SIPRI data are © SIPRI and used under SIPRI's terms (https://www.sipri.org/databases/terms). Maddison data are used under the GGDC attribution requirement. World Bank data are CC-BY-4.0.

## Reproduction order

Python 3.11+, `pandas`, `numpy`, `lifelines` (0.30), `statsmodels`, `matplotlib`, `openpyxl`.

```
python code/build_data.py           # raw trade register -> deals_clean.csv (not redistributed) + coding_audit.csv
python code/analysis.py             # country x category panel, Figs 1-6, pair-level Cox
python code/robustness.py           # yearly pair panel, robustness table, heterogeneity
python code/merge_external.py       # Milex + World Bank -> ext_panel.csv
python code/analysis_external.py    # external-controls Cox, country-year PPML, event study (1960+ sample)
python code/analysis_maddison.py    # same with Maddison GDP (1950+ sample)  -> Table 1 cols 4-5, Table 3, Table 4, Fig 1 (event study)
```

Scripts read the raw files from the paths set at the top of each script; edit those paths to `data/raw/` if you keep the structure above. Running the full chain takes about three minutes on a laptop.

The derived panels in `data/derived/` are what the estimation scripts produce; the Cox and PPML results in the paper can be reproduced from them alone (steps 3, 5 and 6) without the raw trade register.

## Coding of licensed production

Licensed production is not a structured field in the SIPRI register; it is coded from the free-text comment with the rules in `docs/CODEBOOK.md` §4 and §9. An independent blind audit of 120 records agreed with the rules on 114 (95%); the six disagreements and the rule changes they prompted are in `data/audit/audit_result.md`.

## Licence

Code: MIT. Documentation, derived data, tables and figures: CC-BY-4.0. Raw source data remain under their providers' terms.
