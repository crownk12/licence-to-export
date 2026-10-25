# 지시문: SIPRI 라이선스 생산 코딩 수작업 검증

아래 지시문을 새 LLM 세션에 그대로 붙여넣고, `coding_audit.csv` 파일을 함께 첨부하세요.

---

## 역할

당신은 국방경제학 논문의 데이터 코딩을 검증하는 독립 검증자입니다. SIPRI Arms Transfers Database 트레이드 레지스터의 자유 텍스트 코멘트(`comments` 열)에서 **수입국 측 라이선스 생산 여부**를 규칙 기반으로 자동 코딩한 결과가 첨부된 `coding_audit.csv`에 있습니다. 당신의 임무는 각 행의 코멘트를 직접 읽고 자동 코딩(`lic_tier`)이 맞는지 독립적으로 판정하는 것입니다.

자동 코딩 결과에 끌려가지 마세요. 먼저 코멘트만 읽고 스스로 판정한 뒤, 그다음 `lic_tier`와 비교하세요.

## 코딩 규칙 (이 규칙에 따라 판정)

각 행은 공급국(`supplier`)이 수입국(`recipient`)에 특정 무기(`description`)를 판매한 하나의 주문 건입니다. 질문은 하나입니다: **이 무기를 수입국이 자국 내에서 생산·조립·부품제작했는가?**

| lic_tier | 의미 | 해당 표현 예시 |
|---|---|---|
| **1** | 수입국이 해당 무기를 **라이선스 생산** | "produced under licence in [수입국]", "licensed production", "incl production under licence", "produced under Russian licence", "assembled/produced in [수입국]", 코멘트가 "Produced in [수입국]"으로 시작 |
| **2** | 수입국이 **키트 조립·현지 조립**만 | "assembled from kits in [수입국]", "assembled in [수입국]", "incl assembly in [수입국]", "most assembled" |
| **3** | 수입국이 **부품만 생산** (오프셋 포함) | "incl production of components in [수입국]", "offsets incl production of components", "X% of components produced in [수입국]" |
| **0** | 위에 해당 없음 (완제품 수입) | 아래 "티어 0인 함정 표현" 참조 |

우선순위: 1 > 2 > 3. 한 코멘트에 여러 표현이 있으면 가장 높은 티어를 적용합니다(예: 조립 + 부품생산 → 2).

### 티어 0인 함정 표현 (라이선스 생산이 아님)

- **"for N frigates/aircraft produced in [수입국]"** — 이 무기(예: 엔진, 레이더)가 탑재될 *플랫폼*이 수입국에서 건조된다는 뜻. 이 무기 자체는 완제품 수입 → **0**
- **"from [제3국] production line"**, "from Polish production line" — 공급국 쪽 생산 라인에서 나온 완제품 → **0**
- **"assembled/produced in [제3국]"** — 생산 장소가 수입국이 아니면 → **0** (예: 수입국 DR Congo, 코멘트 "probably assembled/produced in Italy")
- **"option on N more produced under licence … not used"** — 미행사 옵션 → **0**
- **"designed for production under licence in [수입국]"** — 라이선스 생산 *예정* → **1**로 인정 (주문 시점 기준 라이선스 계약이 체결된 것)
- "licence" 단어가 없더라도 "Produced in [수입국]"으로 코멘트가 시작하면 → **1**

### 판정이 애매한 경우

- 코멘트에 "probably", "possibly"가 붙어 있어도 해당 티어로 판정하되 `uncertain` 열에 Y 표시
- 주문 일부만 해당(예: "incl 89 assembled/produced under licence")이어도 해당 티어로 판정하되 `partial` 열에 Y 표시
- 정말 판정 불가하면 `my_tier`에 `?`를 쓰고 이유를 적으세요

## 작업 절차

1. `coding_audit.csv`를 읽습니다. 120행이며 열은 `deal_id, recipient, supplier, order_year, description, category, tier3, lic_tier, lic_uncertain, lic_partial, comments, manual_check`입니다.
2. **각 행마다** `comments`를 읽고 위 규칙으로 독립 판정합니다.
3. 자동 코딩 `lic_tier`와 비교해 일치/불일치를 기록합니다.
4. 불일치 건은 **왜** 다른지 한 문장으로 적습니다. 특히 자동 규칙이 놓친 표현 패턴이 있으면 그 표현을 따옴표로 정확히 인용하세요.
5. 결과를 아래 형식의 **마크다운 파일 `audit_result.md`**로 출력합니다. 파일로 저장해 다운로드할 수 있게 하세요.

## 출력 형식 (`audit_result.md`)

```markdown
# 코딩 검증 결과

검증일: YYYY-MM-DD
검증 행 수: 120

## 1. 요약

| 자동 티어 | 행 수 | 일치 | 불일치 | 일치율 |
|---|---|---|---|---|
| 1 | 40 | | | |
| 2 | 20 | | | |
| 3 | 20 | | | |
| 0 | 40 | | | |
| 전체 | 120 | | | |

불일치 유형별 집계:
- 자동 0 → 수동 1/2/3 (놓친 라이선스): N건
- 자동 1/2/3 → 수동 0 (과잉 판정): N건
- 티어 간 혼동 (1↔2, 2↔3 등): N건
- 판정 불가(?): N건

## 2. 행별 판정표 (120행 전체)

| deal_id | recipient | supplier | description | 자동 lic_tier | 수동 my_tier | 일치 | uncertain | partial | 근거 (불일치 시 필수) |
|---|---|---|---|---|---|---|---|---|---|
| ... | | | | | | O/X | Y/ | Y/ | |

## 3. 자동 규칙 개선 제안

불일치 건에서 발견한, 규칙에 추가하거나 수정해야 할 표현 패턴을 정확한 인용과 함께 나열:
- 패턴: "..." → 현재 자동 판정: N, 올바른 판정: M, 해당 deal_id: [...]

## 4. 규칙 자체에 대한 의견

규칙이 모호하거나 판단이 갈릴 수 있는 지점이 있으면 적으세요. 없으면 "없음".
```

## 주의

- 120행을 **빠짐없이** 판정하세요. 일부만 하고 "나머지도 비슷하다"고 쓰지 마세요.
- `comments`가 비어 있으면 티어 0입니다.
- 국가명 변형에 주의: USA=United States, UK=United Kingdom, FRG/West Germany=Germany, GDR=East Germany, Turkey=Turkiye, Czech Republic=Czechia, 오타(Itaky, Geramny, Soutk Korea, Syra)는 해당 국가로 간주.
- 본인의 판정을 먼저 내리고 자동 코딩과 비교하세요. 자동 코딩이 맞다고 가정하지 마세요.
