# SIPRI 라이선스 생산 분석 — 데이터 구축 코드북 (v0.1, 2026-10-24)

## 1. 원자료
- SIPRI Arms Transfers Database, Trade Register, 전체 공급국→전체 수입국, 생성일 2026-10-24. 29,916건(주문 단위), 주문연도 1940–2025.
- 분석은 **주문연도(Year of order)** 기준. 인도연도는 `first_delivery`, `last_delivery`로 보존.

## 2. 산출 파일
| 파일 | 내용 |
|---|---|
| `deals_clean.csv` | 거래 단위 정제 데이터(29,916행 × 41열). 아래 변수 정의 참조 |
| `country_map.csv` | SIPRI 국명 → COW 코드, ISO3, 계승국 계보(lineage), 행위자 유형 |
| `panel_country_category.csv` | 국가(lineage) × 무기범주 패널(1,318행): 최초 수입·최초 라이선스·최초 수출 연도 |
| `panel_timevarying.csv` | Cox 시변 공변량 모형용 분할 패널 |
| `coding_audit.csv` | 수작업 검증용 표본 120건(`manual_check` 열 비어 있음) |
| `tab_*.csv` | 요약표(범주별 비중, KM 요약, Cox 결과) |
| `fig1~6_*.png` | 그림 |

## 3. 국가 처리
- `*`로 끝나는 비국가 행위자, `**`로 끝나는 국제기구, `unknown`은 `actor_type`으로 구분하고 분석에서 제외(국가 간 거래만 사용).
- **계보(lineage) 결합**: 소련→러시아, 체코슬로바키아→체코, 유고슬라비아→세르비아, 북예멘→예멘을 하나의 분석 단위로 묶음. 동독, 남예멘, 남베트남은 별도 단위로 유지(계승국 없음). 이 선택은 논문 부록에 명시하고, 결합하지 않은 버전으로 강건성 검정 권장.

## 4. 라이선스 생산 코딩 (Comments 텍스트 기반)
`license`/`licence`/`licenced` 철자를 통일한 뒤 아래 규칙을 적용. 상위 티어가 우선.

| 변수 | 티어 | 규칙 | 건수 |
|---|---|---|---|
| `lic_L1` | 1 라이선스 생산 | `produced under (X) licence`, `licensed production`, `production under licence`, `under licence`; **위치 기반** `assembled/produced in X`, 코멘트 서두의 `Produced in/on X`는 **X가 수입국일 때만** 인정 | 1,076 |
| `lic_L2` | 2 현지조립 | `assembl*`(kits 포함). `assembled in X`의 X가 수입국이 아니면 제외 | 356 |
| `lic_L3` | 3 부품생산/오프셋 | `production of components`, `components produced`, 등 | 257 |
| `lic_tier` | 0–3 | 위 우선순위 적용 통합 변수 | |
| `lic_any` | | `lic_tier > 0` | 1,689 |
| `lic_uncertain` | | `probably/possibly` 수식어 동반 | |
| `lic_partial` | | `incl N produced under licence`처럼 주문 일부만 해당 | |
| `from_production_line` | | `from X production line`: **공급국 측** 라이선스 생산품 수출(수입국 생산 아님). 별도 분석용 | |

제외 규칙: `option on N more produced under licence … not used`(미행사 옵션), 인도가 프랑스를 위해 생산한 AVSIMAR 건(제3국 생산).  
알려진 한계: `for N frigates produced in X` 형태는 **탑재 플랫폼**이 현지 건조라는 뜻이므로 해당 부품 거래 자체는 라이선스가 아님 → 티어 0 처리. 코멘트 미기재로 누락된 라이선스 건이 존재할 수 있음(과소추정 방향).

## 5. 무기범주 (`category`, `tier3`)
Weapon description 키워드 규칙으로 SIPRI 11개 범주에 매핑(우선순위: Satellites → Ships 예외(aircraft carrier, missile boat) → Engines → Air defence → ASW weapons → Naval weapons → Missiles → Sensors → Artillery → Armoured vehicles → Aircraft → Ships).
- `tier3`: **platform**(Aircraft, Armoured vehicles, Ships) / **weapon**(Missiles, Artillery, Air defence, ASW weapons, Naval weapons) / **subsystem**(Engines, Sensors, Satellites, 그리고 turret·chassis 품목).
- `uav`: 드론·배회탄약·UGV 플래그.

## 6. 패널 변수 (`panel_country_category.csv`)
- `first_import`: 해당 국가가 해당 범주를 처음 수입(주문)한 연도
- `first_lic`: 티어1 라이선스 생산 최초 주문연도; `first_lic_any`: 티어1–3 포함
- `first_export`: 해당 국가가 **공급국**으로 해당 범주를 처음 수출한 연도
- `pre_exporter`: `first_export ≤ first_import`(이미 수출 중이던 쌍, 분석 제외)
- `event`: 최초 수입 이후 수출 발생 여부; `duration`: 최초 수입→최초 수출(또는 2025 중도절단)
- `lic_before`: 라이선스가 **수출보다 먼저** 발생(분석 섹션에서 정의)

## 7. 1차 분석 결과 요약
- 분석표본: 국가×범주 1,227쌍(기존 수출국 제외). 라이선스 보유 223쌍 중 **81쌍은 라이선스 이전에 이미 수출** → 라이선스를 시변 노출로 처리해야 함(Fig 4·5는 이를 무시해 효과 과대, Fig 6은 반대로 과소 가능).
- **Cox 시변 공변량 모형**(국가×범주 쌍, 코호트 통제): 라이선스 생산 HR = **3.10** (95% CI 2.41–3.99). 플랫폼 HR 2.34, 완성무기 HR 1.41(참조: 서브시스템). 최초수입 코호트가 10년 늦을수록 HR 0.72.
- 티어별 상호작용(라이선스×플랫폼, ×완성무기)은 양(+)이나 유의하지 않음 → 라이선스 효과는 범주 전반에 걸쳐 나타남. 서브시스템 표본(라이선스 26쌍)이 작아 검정력 부족.

## 8. 다음 단계 (논문용)
1. `coding_audit.csv` 120건 수작업 검증 → 일치율 보고.
2. 통제변수 병합: GDP·1인당 GDP(World Bank/Maddison), 군사비(SIPRI Milex), 국가 고정효과 또는 층화 Cox.
3. 강건성: (a) `lic_any`(티어1–3) 사용, (b) `lic_uncertain` 제외, (c) 계보 미결합, (d) 수출 정의를 "TIV 임계값 이상" 또는 "2건 이상"으로 강화, (e) 수출 대상이 비국가·국제기구인 건 제외.
4. 이질성: 공급국(미·유럽·소/러)별 라이선스 효과, 냉전/탈냉전 코호트.

## 9. 코딩 규칙 v0.2 (2026-10-24, 수작업 검증 반영)
검증(`audit_result.md`): 120건 중 114건 일치(95%), 티어1 40/40, 과잉판정 0건. 불일치 6건에서 나온 패턴을 반영:
- 티어1 추가: 세미콜론 뒤 독립절 `; produced in [수입국]`, 수량 수식 `N produced in [수입국]`, 명사형 `assembly/production in [수입국]`
- 티어3 추가: `production of (warheads|hulls|sections|parts|...) in [수입국]`; 위치가 명시되면 수입국 일치 요구
- unknown recipient 행은 라이선스 코딩 0으로 고정(분석에서 제외됨)
- partial 플래그: `incl some N`, `in N assembled`(오타) 포함
- 신규 변수 `lic_either`(A or B 표현, 52건), `lic_tier_conservative`·`lic_L1_cons`(낮은 티어 적용) → 강건성 검정용
결과: 티어1 1,076 → 1,142건. 모든 모형 재추정; 결론 불변(풀링 HR 3.2/2.1, 층화 1.3~1.4 ns, 스필오버 0, 미국 라이선스 무효과).
