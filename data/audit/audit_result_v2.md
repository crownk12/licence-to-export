# 코딩 검증 결과

검증일: 2026-10-25
검증 행 수: 60

검증 방법: 각 행의 `comments`만 먼저 읽고 지시문 규칙(1 > 2 > 3 > 0, 함정 표현 포함)에 따라 `my_tier`를 결정한 뒤, 그 다음에 자동 코딩 `lic_tier`와 대조함. `uncertain`/`partial` 플래그도 독립적으로 판정함.

## 1. 요약

| 자동 티어 | 행 수 | 일치 | 불일치 | 일치율 |
|---|---|---|---|---|
| 1 | 20 | 20 | 0 | 100.0% |
| 2 | 10 | 9 | 1 | 90.0% |
| 3 | 10 | 10 | 0 | 100.0% |
| 0 | 20 | 20 | 0 | 100.0% |
| 전체 | 60 | 59 | 1 | 98.3% |

불일치 유형별 집계:
- 자동 0 → 수동 1/2/3 (놓친 라이선스): 0건
- 자동 1/2/3 → 수동 0 (과잉 판정): 1건 (deal_id 26068)
- 티어 간 혼동 (1↔2, 2↔3 등): 0건
- 판정 불가(?): 0건

티어는 일치하지만 **플래그(`partial`)가 다른 행**: 2건 (deal_id 22981, 20109 — "most …" 표현인데 자동 `lic_partial`=0). 아래 표의 `partial` 열은 수동 판정값이며, 이 2건은 근거 열에 별도 표시함.

## 2. 행별 판정표 (60행 전체)

| deal_id | recipient | supplier | description | 자동 lic_tier | 수동 my_tier | 일치 | uncertain | partial | 근거 (불일치 시 필수) |
|---|---|---|---|---|---|---|---|---|---|
| 10347 | India | France | fighter/ground-attack aircraft | 3 | 3 | O | | | "50% offsets incl 20% as production of components in India" → 3 |
| 13100 | Italy | United States | anti-submarine sonar | 0 | 0 | O | | | "For 8 Minerva corvettes produced in Italy" — 플랫폼 함정 → 0 |
| 20152 | Poland | South Korea | self-propelled gun | 1 | 1 | O | | | "incl production under licence in Poland" → 1 |
| 12554 | Israel | United Kingdom | turbojet | 0 | 0 | O | | | 탑재 플랫폼(Ouragan)이 프랑스산, "produced in France" — 제3국 → 0 |
| 6672 | East Germany (GDR) | Soviet Union | self-propelled gun | 0 | 0 | O | | | "From Bulgarian production line" → 0 |
| 12875 | Israel | Italy | naval gun | 0 | 0 | O | | | "For 10 Saar-4 … missile boats produced in Israel" — 플랫폼 함정 → 0 |
| 24447 | Sweden | Finland | armoured personnel carrier | 3 | 3 | O | | | "incl production of components in Sweden" → 3 ("probably"는 납품 시기에 붙은 것이므로 uncertain 아님) |
| 10538 | India | Russia | multiple rocket launcher | 3 | 3 | O | | | "Incl production of components in India" → 3 |
| 9602 | Greece | United States | transport aircraft | 0 | 0 | O | | | 중고기 재판매, 현지 생산 언급 없음 → 0 |
| 10714 | India | Germany | submarine | 2 | 2 | O | | Y | "Incl 2 assembled from kits in India" → 2, 일부(2척)만 해당 → partial |
| 8497 | France | United States | helicopter | 2 | 2 | O | | | "Incl assembly from kits in France" → 2 |
| 8705 | Germany | United States | gas turbine | 0 | 0 | O | | | "For 8 Bremen (Type-122) frigates produced in Germany" — 플랫폼 함정 → 0 |
| 20870 | Qatar | France | armoured reconnaissance/fire-support vehicle | 0 | 0 | O | | | 프랑스군 생산분 전용, 현지 생산 없음 → 0 |
| 28386 | United States | Australia | transport ship | 1 | 1 | O | | | "produced under licence in USA" → 1 |
| 11764 | Iran | North Korea | surface-to-surface missile | 2 | 2 | O | | | "Including assembly from kits in Iran" → 2 ("Including" 철자 변형이지만 자동 규칙이 포착함) |
| 13084 | Italy | United States | short-range air-to-air missile | 3 | 3 | O | | | "from European production line in FRG"(0 함정)보다 "incl production of components in Italy"가 우선 → 3 |
| 29522 | Yemen | South Africa | armoured personnel carrier | 2 | 2 | O | | | "assembled in Yemen" → 2 |
| 4711 | China | France | anti-submarine sonar | 1 | 1 | O | Y | | 앞부분은 플랫폼 함정이지만 "probably produced under licence in China" → 1, probably → uncertain |
| 7259 | Egypt | Italy | helicopter | 0 | 0 | O | | | "from US production line" — 제3국 생산라인 → 0 |
| 11880 | Iran | China | surface-to-air missile | 1 | 1 | O | Y | | "possibly produced under licence in Iran as Shahab Thaqeb" → 1, possibly → uncertain |
| 3386 | Bulgaria | Soviet Union | naval gun | 0 | 0 | O | | | "For 1 Project-102 (Mesar) support ship produced in Bulgaria" — 플랫폼 함정 → 0 |
| 28381 | United States | Germany | ship engine | 0 | 0 | O | | | "for 19 LCS-2 frigates produced in USA" — 플랫폼 함정 → 0 |
| 23560 | Spain | Germany | trainer aircraft | 1 | 1 | O | | | "produced under licence in Spain" → 1 |
| 9527 | Greece | Germany | armoured recovery vehicle | 3 | 3 | O | | | "offsets incl 40% in production of components in Greece" → 3 |
| 8850 | Germany | United Kingdom | turbojet | 0 | 0 | O | | | "from production line in Italy" — 제3국 → 0 |
| 10523 | India | Israel | combat aircraft radar | 3 | 3 | O | | | "incl production of components in India" → 3 |
| 9055 | Ghana | United Kingdom | turbojet | 0 | 0 | O | | | "probably from Italian production line" — 제3국 → 0 (probably는 생산라인 위치에 붙은 것, 어느 쪽이든 0이라 uncertain 미표시) |
| 18238 | Norway | Italy | anti-submarine helicopter | 3 | 3 | O | | | "offsets incl production of components in Norway" → 3 (이후 취소·반환은 티어와 무관) |
| 13091 | Italy | United States | gas turbine | 0 | 0 | O | | | "For 2 De la Penne destroyers produced in Italy" — 플랫폼 함정 → 0 |
| 18024 | North Korea | China | multiple rocket launcher | 1 | 1 | O | | | "Incl production under licence as Type-75" — 국가명 없으나 수입국 명칭(Type-75)으로 수입국 생산임이 명백 → 1 |
| 26623 | Turkiye | South Korea | trainer aircraft | 2 | 2 | O | | | "incl assembly in Turkiye" → 2 |
| 11757 | Iran | Soviet Union | infantry fighting vehicle | 0 | 0 | O | | | "From Czechoslovakian production line" → 0 |
| 17303 | Netherlands | Sweden | infantry fighting vehicle | 3 | 3 | O | | | "incl production of components in Netherlands" → 3 ("not yet ordered"는 티어가 아닌 데이터 포함 여부 문제, §4 참조) |
| 1302 | Australia | United States | anti-submarine aircraft | 3 | 3 | O | | | "Incl production of components in Australia" → 3 |
| 26068 | Togo | South Africa | armoured personnel carrier | 2 | 0 | **X** | | | **과잉 판정.** "from assembly/production line in United Arab Emirates" — 조립·생산 장소가 수입국(Togo)이 아닌 제3국(UAE)이므로 "from [제3국] production line" 함정에 해당 → 0. 자동 규칙이 "assembly" 단어를 수입국 조립으로 오인한 것으로 보임 |
| 20961 | Romania | Soviet Union | short-range air-to-air missile | 1 | 1 | O | | | "incl assembly/production in Romania" — "assembled/produced in [수입국]" 변형 → 1 |
| 2249 | Bangladesh | China | armed drone | 1 | 1 | O | | | "Produced under licence in Bangladesh" → 1 (명칭 불확실은 티어와 무관) |
| 2338 | Belarus | Iran | one-way attack drone | 2 | 2 | O | Y | | "possibly assembled in Belarus" → 2, possibly → uncertain |
| 29265 | Viet Nam | Belarus | surface-to-air missile system | 2 | 2 | O | | | "assembled in Viet Nam" → 2 (기존 보유 S-125의 개수(改修) 건, §4 참조) |
| 11070 | India | Soviet Union | tank | 0 | 0 | O | | | "Probably incl from Czechoslovakian and/or Polish production line" — 제3국 → 0 |
| 22829 | South Korea | Germany | ship engine | 0 | 0 | O | | | "for 1 FFX-2 (Daegu) frigate produced in South Korea" — 플랫폼 함정 → 0 |
| 22981 | South Korea | United States | transport helicopter | 1 | 1 | O | | Y | "most assembled/produced under licence in South Korea" → 1. **플래그 불일치**: "most"는 전량이 아니므로 partial=Y가 맞는데 자동 lic_partial=0 |
| 16487 | Morocco | Germany | vehicle engine | 0 | 0 | O | | | "probably from production line in Siuth Africa"(오타=South Africa) — 제3국 → 0 |
| 7280 | Egypt | China | trainer/combat aircraft | 2 | 2 | O | | | "assembled from kits in Egypt" → 2 |
| 27701 | United Arab Emirates | Ukraine | infantry fighting vehicle | 2 | 2 | O | | | "Assembled from kits in United Arab Emirates" → 2 |
| 4050 | Canada | Australia | patrol boat | 1 | 1 | O | | | "produced under licence in Canada" → 1 |
| 17027 | Netherlands | France | anti-submarine sonar | 0 | 0 | O | | | "For 2 Walrus submarines produced in Netherlands" — 플랫폼 함정 → 0 |
| 8821 | Germany | Switzerland | armoured personnel carrier | 1 | 1 | O | | | "produced under licence in Germany" → 1 |
| 22710 | South Korea | United States | anti-submarine sonar | 0 | 0 | O | | | "For 9 Ulsan frigates produced in South Korea" — 플랫폼 함정 → 0 |
| 13382 | Japan | United States | helicopter | 1 | 1 | O | | | "produced under licence in Japan as UH-2" → 1 |
| 11765 | Iran | China | multiple rocket launcher | 1 | 1 | O | | | "Incl production under licence in Iran as Fadjr-1" → 1 |
| 20109 | Poland | Soviet Union | tank | 1 | 1 | O | | Y | "Most assembled/produced under licence in Poland" → 1. **플래그 불일치**: "Most"이므로 partial=Y가 맞는데 자동 lic_partial=0 |
| 11664 | Iran | Netherlands | transport craft | 1 | 1 | O | | Y | "Incl 4 assembled/produced under licence in Iran" → 1, 일부(4척) → partial |
| 16039 | Mexico | Netherlands | frigate | 1 | 1 | O | | | "produced in Mexico" — 코멘트 첫머리는 아니지만("'POLA' programme; produced in Mexico") 대상 무기(프리깃) 자체가 수입국에서 건조된 것이므로 → 1 (§4 참조) |
| 4543 | Chile | Germany | patrol ship | 1 | 1 | O | | | "produced in Chile" — 위와 동일 구조, 대상 함정 자체가 칠레 건조 → 1 |
| 10809 | India | Soviet Union | fighter aircraft | 1 | 1 | O | | | "produced under licence in India" → 1 |
| 27620 | United Arab Emirates | South Africa | guided bomb | 1 | 1 | O | | | "Produced under licence in United Arab Emirates as Thunder" → 1 |
| 22699 | South Korea | United States | naval gun | 1 | 1 | O | | | 앞부분 "frigates produced in South Korea"는 플랫폼 함정이지만 뒤에 "produced under licence in South Korea"가 명시 → 1 |
| 27386 | Ukraine | Germany | vehicle engine | 0 | 0 | O | | | "for 200 Bohdana self-propelled guns produced by Ukraine" — "produced by" 변형의 플랫폼 함정 → 0 |
| 1609 | Australia | United States | anti-submarine aircraft | 3 | 3 | O | | | "Incl production of components in Australia" → 3 |

## 3. 자동 규칙 개선 제안

**티어 오류 (1건)**

- 패턴: "from assembly/production line in [제3국]" → 현재 자동 판정: 2, 올바른 판정: 0, 해당 deal_id: [26068]
  - 원인 추정: 티어 2 규칙이 "assembl*"를 포착하되 그 뒤의 국가명이 수입국인지 검사하지 않거나, "from … production line" 함정 규칙이 "assembly/production line"처럼 슬래시가 끼어든 변형을 못 잡는 것으로 보임.
  - 수정안: (a) "from [X] production line" 정규식을 `from\s+\S+(/\S+)?\s+production line` 형태로 넓혀 "assembly/production line", "assembly/production line in [국가]"까지 포착하고, 이 패턴이 있으면 뒤따르는 국가가 수입국이 아닌 한 0으로 강제. (b) 모든 티어 1·2 매칭에 대해 "in [국가]" 뒤 국가명이 수입국(변형·오타 포함)과 일치하는지 반드시 확인.

**partial 플래그 누락 (2건, 티어는 일치)**

- 패턴: "most assembled/produced under licence in [수입국]" / "Most assembled/produced under licence in [수입국]" → 현재 lic_partial: 0, 올바른 값: 1, 해당 deal_id: [22981, 20109]
  - "incl N …"처럼 숫자가 있는 경우만 partial로 잡는 것으로 보임. "most", "majority", "some", "part of", "incl [숫자 없이] … of the" 같은 수량 한정어도 partial 트리거에 추가 권장. 반대로 "most assembled"는 티어 2 예시에도 있으므로, "most"를 티어 트리거로 쓰면서 partial 플래그는 안 켜는 불일치가 생기지 않도록 함께 처리.

**정상 작동했지만 규칙 문서화가 필요한 변형 (오류 아님, 향후 회귀 방지용)**

- "produced by [수입국]" (deal_id 27386) — "produced in"의 변형. 이번엔 0으로 맞게 나왔지만, 플랫폼 함정 규칙이 "produced in"만 보고 있다면 "for N X produced by [수입국]"에 이어 다른 표현이 붙을 때 오작동 가능.
- "Including assembly from kits in" (11764) — "incl"의 풀어쓴 형태. 정상 포착됨.
- "assembly/production in [수입국]" (20961) — "assembled/produced in"의 명사형 변형. 정상 포착됨(1).
- "Incl production under licence as [수입국 명칭]" (18024) — 국가명 없이 "as [현지 명칭]"만 있는 형태. 정상 포착됨(1). 국가명 검사를 강화(위 (b))할 때 이 형태가 0으로 떨어지지 않도록 예외 처리 필요.
- "offsets incl 40% in production of components" (9527) — "offsets incl production of components" 사이에 "N% in"이 끼어든 형태. 정상 포착됨(3).
- 한 코멘트에 함정 표현과 유효 표현이 공존하는 경우 (4711, 13084, 22699) — 모두 올바르게 상위 티어로 판정됨. 우선순위 로직이 작동하고 있음.

## 4. 규칙 자체에 대한 의견

1. **"Produced in [수입국]으로 코멘트가 시작하면 1" 조건이 너무 좁음.** deal_id 16039, 4543은 "'POLA' programme; produced in Mexico"처럼 프로그램명 뒤에 "; produced in [수입국]"이 오고 코멘트 시작이 아님. 자동 코딩은 1로 잡았고 실질적으로도 맞지만, 문서화된 규칙대로라면 0이 되어야 함. 규칙을 "**'for N [플랫폼] produced in' 구문에 속하지 않는** 'produced in [수입국]'이면 1"로 고쳐 쓰는 편이 자동 규칙의 실제 동작과 일치함. 핵심 구별 기준은 '문장 시작 여부'가 아니라 '해당 무기 자체 vs 탑재 플랫폼'임.

2. **"assembled/produced in [수입국]"을 1로 보는 근거.** 이 표현은 조립인지 생산인지 SIPRI 자체가 확정하지 못한 경우로 읽히는데, 규칙은 이를 1(라이선스 생산)로 정함. 20961("assembly/production in Romania")이 그 예. 보수적으로 보면 2에 가까울 수 있으므로, 논문에서 1과 2를 합산해 쓰는지 분리해 쓰는지에 따라 민감도 분석 대상으로 삼는 것을 권장.

3. **"incl"의 partial 처리 기준이 불명확.** "incl production under licence in Poland"(20152), "Incl production of components in India"(10538) 등 "incl" 뒤에 수량이 없는 경우, 주문 전체가 해당하는지 일부만 해당하는지 코멘트만으로는 알 수 없음. 현재 규칙(예시: "incl 89 …")은 숫자가 있을 때만 partial로 보는 듯하나, 명시적으로 "숫자 없는 incl은 partial 아님"이라고 적어 두는 것이 좋음. 동시에 "most"는 partial로 본다는 점도 명시 필요(§3 참조).

4. **uncertain 플래그의 적용 범위.** 9055, 16487, 11070은 "probably"가 붙어 있으나 그 불확실성은 '어느 제3국 생산라인인가'에 관한 것이고 티어는 어느 쪽이든 0임. 이번 검증에서는 라이선스 생산 여부 자체가 불확실한 경우(4711, 11880, 2338)에만 Y를 표시했고 자동 코딩도 동일했음. 규칙에 "uncertain은 티어 결정에 영향을 주는 불확실성에만 표시"라고 적어 두면 검증자 간 편차를 줄일 수 있음.

5. **개수(改修)·업그레이드 건의 취급.** 29265는 베트남이 이미 보유한 S-125를 벨라루스 기술로 S-125-VT로 개조하면서 "assembled in Viet Nam"이라고 된 건. 규칙상 2가 맞지만, 신규 무기의 현지 조립과 보유 장비의 현지 개조는 경제적 의미가 다를 수 있음. 논문의 연구 질문이 '생산 역량 이전'이라면 분리 코딩 또는 별도 플래그를 고려.

6. **미발주·취소 건.** 17303은 "selected 2025 but not yet ordered by end-2025", 18238은 2022년 취소·2025년 반환. 티어 판정은 규칙대로 했으나(3), 이런 건이 분석 표본에 들어가야 하는지는 코딩 규칙이 아닌 표본 선정 규칙의 문제이므로 별도로 정해 둘 것을 권장.

7. **국가명 변형 처리 확인.** "Siuth Africa"(16487) 같은 오타는 제3국이라 티어에 영향이 없었지만, 같은 오타가 수입국 자리에 나오면("assembled in Soutk Korea") 매칭 실패로 0이 될 위험이 있음. 지시문에 열거된 오타 목록 외에도 편집 거리 기반 매칭을 두는 것이 안전함.
