# 코딩 검증 결과

검증일: 2026-10-24  
검증 행 수: 120  
검증 방법: 각 행의 `comments`를 먼저 읽고 규칙에 따라 독립 판정(`my_tier`)한 뒤 자동 코딩 `lic_tier`와 비교. 자동 코딩 값은 판정 후에만 확인했습니다.

## 1. 요약

| 자동 티어 | 행 수 | 일치 | 불일치 | 일치율 |
|---|---|---|---|---|
| 1 | 40 | 40 | 0 | 100.0% |
| 2 | 20 | 18 | 2 | 90.0% |
| 3 | 20 | 18 | 2 | 90.0% |
| 0 | 40 | 38 | 2 | 95.0% |
| 전체 | 120 | 114 | 6 | 95.0% |

불일치 유형별 집계:
- 자동 0 → 수동 1/2/3 (놓친 라이선스): 2건 — 13522(0→1), 1418(0→3)
- 자동 1/2/3 → 수동 0 (과잉 판정): 0건
- 티어 간 혼동 (1↔2, 2↔3 등): 2건 — 8808(2→1), 13546(2→1)
- 판정 불가(?): 2건 — 28734(자동 3), 28733(자동 3)

티어는 일치하나 `partial`/`uncertain` 플래그만 다른 행: 5건 — 29732, 18362, 13595, 26600, 23668. (아래 표의 근거 열 참조; 일치율 계산에는 티어만 반영)

핵심 발견: 자동 코딩의 티어 1은 40/40 전부 정확했고, 과잉 판정(0으로 내려야 할 것을 1/2/3으로 올린 경우)은 한 건도 없었습니다. 불일치 6건은 모두 (a) "produced in [수입국]"이 코멘트 첫머리가 아닌 위치에 나와 놓친 경우(2건), (b) "assembly/production" 같은 명사형 변형(1건), (c) "components" 대신 "warheads"처럼 구체 부품명을 쓴 경우(1건), (d) 수입국이 unknown인데 국가 일치 검사 없이 3으로 판정한 경우(2건)입니다. 즉 규칙 자체보다 표현 패턴 매칭의 범위 문제입니다.

## 2. 행별 판정표 (120행 전체)

| # | deal_id | recipient | supplier | description | 자동 lic_tier | 수동 my_tier | 일치 | uncertain | partial | 근거 (불일치 시 필수) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 22244 | Singapore | France | frigate | 1 | 1 | O |  | Y |  |
| 2 | 19622 | Peru | South Korea | patrol ship | 1 | 1 | O |  |  |  |
| 3 | 25159 | Taiwan | United States | fighter/ground-attack aircraft | 1 | 1 | O |  |  |  |
| 4 | 7328 | Egypt | United States | tank | 1 | 1 | O |  |  |  |
| 5 | 29732 | Yugoslavia | Czechoslovakia | self-propelled anti-aircraft gun | 1 | 1 | O | Y |  | "production of compoents or production under licence" — 3과 1 중 하나로 표현이 양자택일(or)이라 최고 티어 적용, 다만 불확실 표시 |
| 6 | 25221 | Taiwan | United States | tank | 1 | 1 | O |  |  |  |
| 7 | 7213 | Egypt | China | towed gun | 1 | 1 | O |  |  | 괄호의 "possibly illegally copied"는 라이선스의 적법성에 대한 유보이지 이집트 내 생산 여부에는 영향 없음 |
| 8 | 26743 | Turkiye | Israel | tank | 1 | 1 | O |  |  |  |
| 9 | 20220 | Poland | Russia | tank | 1 | 1 | O |  |  |  |
| 10 | 26333 | Turkiye | Germany | submarine | 1 | 1 | O |  |  |  |
| 11 | 20113 | Poland | Russia | maritime patrol aircraft | 1 | 1 | O |  |  |  |
| 12 | 13161 | Italy | Germany | ship engine | 1 | 1 | O |  |  |  |
| 13 | 4011 | Canada | Norway | tank destroyer turret | 1 | 1 | O |  |  |  |
| 14 | 27636 | United Arab Emirates | Brazil | ground-attack aircraft | 1 | 1 | O |  |  |  |
| 15 | 3229 | Brazil | France | (armed) transport helicopter | 1 | 1 | O |  |  |  |
| 16 | 14113 | Kazakhstan | Turkiye | infantry fighting vehicle | 1 | 1 | O |  |  |  |
| 17 | 13560 | Japan | United States | anti-submarine helicopter | 1 | 1 | O |  | Y |  |
| 18 | 4731 | China | Russia | naval gun | 1 | 1 | O |  |  |  |
| 19 | 13183 | Italy | United States | helicopter | 1 | 1 | O |  |  |  |
| 20 | 28107 | United Kingdom | United States | anti-submarine torpedo | 1 | 1 | O |  |  |  |
| 21 | 10875 | India | United Kingdom | frigate | 1 | 1 | O |  |  |  |
| 22 | 1488 | Australia | Spain | amphibious assault ship | 1 | 1 | O |  |  |  |
| 23 | 3109 | Brazil | Israel | infantry fighting vehicle turret | 1 | 1 | O |  |  |  |
| 24 | 26467 | Turkiye | Germany | missile boat | 1 | 1 | O |  |  |  |
| 25 | 13600 | Japan | United Kingdom | ship engine | 1 | 1 | O |  |  |  |
| 26 | 1536 | Australia | Ireland | armoured personnel carrier | 1 | 1 | O |  |  |  |
| 27 | 27638 | United Arab Emirates | Brazil | trainer aircraft | 1 | 1 | O |  |  |  |
| 28 | 4901 | China | France | fire-control radar | 1 | 1 | O | Y |  |  |
| 29 | 13580 | Japan | United States | surface-to-air missile | 1 | 1 | O |  |  |  |
| 30 | 18362 | Norway | Sweden | air-search radar | 1 | 1 | O | Y |  | "assembly or production under licence" — 2/1 양자택일이라 최고 티어 적용, 불확실 표시 |
| 31 | 5900 | Czechoslovakia | Soviet Union | tank | 1 | 1 | O |  |  |  |
| 32 | 23566 | Spain | United Kingdom | minehunter | 1 | 1 | O |  |  |  |
| 33 | 6612 | East Germany (GDR) | Soviet Union | armoured personnel carrier | 1 | 1 | O |  |  |  |
| 34 | 26620 | Turkiye | Spain | transport aircraft | 1 | 1 | O |  |  | "50 assembled or produced under licence" — 총 주문 수가 코멘트에 없어 partial 판단 불가 |
| 35 | 5924 | Czechoslovakia | Soviet Union | fighter aircraft | 1 | 1 | O |  |  |  |
| 36 | 2964 | Brazil | United Kingdom | destroyer | 1 | 1 | O |  |  |  |
| 37 | 7221 | Egypt | China | reconnaissance drone | 1 | 1 | O |  |  |  |
| 38 | 2953 | Brazil | France | ship engine | 1 | 1 | O |  |  | "assembled or produced under licence in Brazil" — 2/1 양자택일, 최고 티어 |
| 39 | 11859 | Iran | China | armoured personnel carrier | 1 | 1 | O |  |  |  |
| 40 | 13595 | Japan | United States | anti-ballistic missile missile | 1 | 1 | O | Y |  | "production of components or production under licence" — 3/1 양자택일, 최고 티어, 불확실 표시 |
| 41 | 23613 | Spain | Chile | trainer aircraft | 2 | 2 | O |  |  |  |
| 42 | 13167 | Italy | United States | fighter/ground-attack aircraft | 2 | 2 | O |  |  |  |
| 43 | 7388 | Egypt | United States | patrol boat | 2 | 2 | O |  |  |  |
| 44 | 8808 | Germany | France | transport aircraft | 2 | 1 | X |  | Y | "incl 25 assembled from kits and 161 produced in FRG" — 161대가 수입국(FRG=Germany)에서 "produced"됨. 플랫폼 수식구가 아니라 이 무기 자체를 가리키므로 라이선스 생산(1). 자동 규칙은 "Produced in [수입국]"을 코멘트 첫머리에서만 인식 |
| 45 | 8497 | France | United States | helicopter | 2 | 2 | O |  |  |  |
| 46 | 26600 | Turkiye | Italy | (armed) trainer aircraft | 2 | 2 | O |  | Y | "incl some 30 assembled from kits" — 수량이 명시된 일부 해당이므로 partial=Y가 맞음(자동은 0) |
| 47 | 26623 | Turkiye | South Korea | trainer aircraft | 2 | 2 | O |  |  |  |
| 48 | 13546 | Japan | United States | self-propelled gun | 2 | 1 | X |  |  | "Incl assembly/production in Japan" — 명사형 "assembly/production in [수입국]"은 규칙의 "assembled/produced in [수입국]"(티어 1)과 동일 의미인데 자동 규칙은 "assembly"만 잡아 2로 판정 |
| 49 | 15537 | Malaysia | Turkiye | armoured personnel carrier | 2 | 2 | O |  |  |  |
| 50 | 15401 | Malaysia | Thailand | armoured personnel carrier | 2 | 2 | O |  | Y |  |
| 51 | 18880 | Pakistan | Italy | reconnaissance drone | 2 | 2 | O |  |  |  |
| 52 | 18943 | Pakistan | Italy | midget submarine | 2 | 2 | O |  |  |  |
| 53 | 23668 | Spain | France | transport helicopter | 2 | 2 | O |  | Y | "in 12 assembled in Spain"(incl의 오타) — 수량 명시 일부 해당이므로 partial=Y가 맞음(자동은 0) |
| 54 | 14687 | Latvia | Spain | infantry fighting vehicle | 2 | 2 | O |  |  |  |
| 55 | 15514 | Malaysia | Turkiye | armoured personnel carrier | 2 | 2 | O |  |  | "65 assembled from kits" — 총 주문 수가 코멘트에 없어 partial 판단 불가 |
| 56 | 1073 | Argentina | Germany | submarine | 2 | 2 | O |  |  |  |
| 57 | 17359 | Netherlands | Sweden | naval gun | 2 | 2 | O |  |  |  |
| 58 | 7280 | Egypt | China | trainer/combat aircraft | 2 | 2 | O |  |  |  |
| 59 | 22145 | Singapore | Russia | portable surface-to-air missile | 2 | 2 | O | Y |  |  |
| 60 | 11870 | Iran | North Korea | surface-to-surface missile | 2 | 2 | O |  |  |  |
| 61 | 20698 | Portugal | Brazil | transport aircraft | 3 | 3 | O |  |  |  |
| 62 | 4132 | Canada | Netherlands | electro-optical system | 3 | 3 | O |  |  |  |
| 63 | 22023 | Singapore | Germany | submarine | 3 | 3 | O |  |  |  |
| 64 | 28081 | United Kingdom | United States | fighter aircraft | 3 | 3 | O |  |  |  |
| 65 | 24573 | Switzerland | United Kingdom | surface-to-air missile | 3 | 3 | O |  |  |  |
| 66 | 20467 | Poland | Norway | coastal defence system | 3 | 3 | O |  |  |  |
| 67 | 18360 | Norway | United States | long-range air-to-air missile | 3 | 3 | O |  |  |  |
| 68 | 3089 | Brazil | France | anti-ship missile | 3 | 3 | O |  |  |  |
| 69 | 17227 | Netherlands | United States | surface-to-air missile system | 3 | 3 | O |  |  |  |
| 70 | 22246 | Singapore | Germany | submarine | 3 | 3 | O |  |  |  |
| 71 | 28734 | unknown recipient(s) | Germany | short-range air-to-air missile | 3 | ? | X | Y |  | 수입국이 "unknown recipient(s)"이고 코멘트는 "production of components in several NATO countries and final assembly in FRG"(FRG=공급국). 부품 생산국이 수입국인지 확인 불가. 3도 변호 가능하나 규칙상 "[수입국]에서" 확인 불가 → ? |
| 72 | 8715 | Germany | United States | surface-to-air missile | 3 | 3 | O |  |  |  |
| 73 | 1322 | Australia | United States | surface-to-air missile | 3 | 3 | O |  |  |  |
| 74 | 28063 | United Kingdom | Sweden | armoured personnel carrier | 3 | 3 | O |  |  |  |
| 75 | 6145 | Denmark | Norway | air-to-surface missile | 3 | 3 | O |  |  | "(with assembly in Norway)"는 제3국 조립이므로 2가 아님; 덴마크 부품 생산만 해당 → 3 (자동 판정 정확) |
| 76 | 18370 | Norway | Sweden | portable surface-to-air missile | 3 | 3 | O |  |  | "Norwegian production of components" — 형용사형 국가명인데 자동이 정확히 잡음 |
| 77 | 28473 | United States | Canada | armoured personnel carrier | 3 | 3 | O |  |  |  |
| 78 | 6537 | East Germany (GDR) | Czechoslovakia | armoured recovery vehicle | 3 | 3 | O |  |  |  |
| 79 | 20476 | Portugal | Brazil | transport aircraft | 3 | 3 | O |  |  |  |
| 80 | 28733 | unknown recipient(s) | United States | short-range air-to-air missile | 3 | ? | X | Y |  | 수입국이 "unknown recipient(s)"이고 "incl production of components in several NATO countries" — 어느 나라인지 특정 불가. 자동 규칙이 국가 일치 검사 없이 "production of components"만으로 3 판정 → ? |
| 81 | 2844 | Brazil | United States | turbofan | 0 | 0 | O |  |  |  |
| 82 | 3097 | Brazil | Italy | fire-control radar | 0 | 0 | O |  |  |  |
| 83 | 9594 | Greece | United Kingdom | turbofan | 0 | 0 | O |  |  |  |
| 84 | 13522 | Japan | United States | gas turbine | 0 | 1 | X |  |  | "... 1 Asuka research ship produced in Japan; produced in Japan" — 세미콜론 뒤 독립절 "produced in Japan"은 플랫폼이 아니라 이 가스터빈 자체가 일본에서 생산됨을 뜻함. 자동 규칙은 코멘트 첫머리의 "Produced in [수입국]"만 인식하고 중간/끝의 독립절은 놓침 |
| 85 | 15904 | Mexico | Germany | ship engine | 0 | 0 | O |  |  |  |
| 86 | 13611 | Japan | United States | air-search radar | 0 | 0 | O |  |  |  |
| 87 | 22918 | South Korea | United States | turbofan | 0 | 0 | O |  |  |  |
| 88 | 5784 | Czechia | United States | turbofan | 0 | 0 | O |  |  |  |
| 89 | 7572 | Egypt | Soviet Union | fighter aircraft | 0 | 0 | O |  |  |  |
| 90 | 26631 | Turkiye | United States | fighter/ground-attack aircraft | 0 | 0 | O |  |  |  |
| 91 | 2175 | Bangladesh | France | ship engine | 0 | 0 | O |  |  |  |
| 92 | 17557 | Nicaragua | Soviet Union | light transport aircraft | 0 | 0 | O |  |  | "Probably"가 붙었으나 제3국 생산라인 → 0이며 uncertain은 티어 판정과 무관 |
| 93 | 10743 | India | Israel | combat aircraft radar | 0 | 0 | O |  |  |  |
| 94 | 22733 | South Korea | United States | naval surface-to-air missile system | 0 | 0 | O |  |  |  |
| 95 | 16330 | Morocco | United States | patrol boat | 0 | 0 | O |  |  |  |
| 96 | 4853 | China | Russia | turbofan | 0 | 0 | O |  |  |  |
| 97 | 13255 | Italy | Canada | aircraft engine | 0 | 0 | O |  |  |  |
| 98 | 22975 | South Korea | United Kingdom | gas turbine | 0 | 0 | O |  |  |  |
| 99 | 12414 | Iraq | Australia | light aircraft | 0 | 0 | O |  |  | "assembled in Jordan" — 수입국 Iraq가 아닌 제3국 조립이므로 0 (자동 판정 정확) |
| 100 | 16251 | Montenegro | United States | light helicopter | 0 | 0 | O |  |  |  |
| 101 | 27619 | United Arab Emirates | Australia | infantry fighting vehicle turret | 0 | 0 | O |  |  | "produced in United Arab Emirates"는 탑재 플랫폼(Nimr IFV)을 수식 → 0 (자동 판정 정확) |
| 102 | 2571 | Belgium | France | anti-submarine rocket launcher | 0 | 0 | O |  |  |  |
| 103 | 4877 | China | United Kingdom | turbofan | 0 | 0 | O |  |  |  |
| 104 | 13500 | Japan | United States | anti-submarine rocket launcher | 0 | 0 | O |  |  |  |
| 105 | 22162 | Singapore | Australia | iinfantry fighting vehicle turret | 0 | 0 | O |  |  |  |
| 106 | 24351 | Sweden | Norway | anti-submarine sonar | 0 | 0 | O |  |  |  |
| 107 | 12156 | Iraq | Soviet Union | infantry fighting vehicle | 0 | 0 | O |  |  |  |
| 108 | 8310 | France | United States | aircraft engine | 0 | 0 | O |  |  |  |
| 109 | 28552 | United States | Canada | light helicopter | 0 | 0 | O |  |  | "US design produced in Canada for USA" — 생산지가 공급국 Canada이므로 0 (자동 판정 정확) |
| 110 | 22744 | South Korea | United States | ship engine | 0 | 0 | O |  |  |  |
| 111 | 28316 | United Kingdom | United States | naval gun | 0 | 0 | O |  |  |  |
| 112 | 22421 | Somalia | South Africa | armoured personnel carrier | 0 | 0 | O |  |  |  |
| 113 | 21457 | Saudi Arabia | United Kingdom | armoured personnel carrier | 0 | 0 | O |  |  |  |
| 114 | 23193 | South Korea | United States | gas turbine | 0 | 0 | O |  |  |  |
| 115 | 28228 | United Kingdom | United States | naval surface-to-air missile system | 0 | 0 | O |  |  |  |
| 116 | 23151 | South Korea | United States | light helicopter | 0 | 0 | O |  |  |  |
| 117 | 10306 | India | Russia | naval surface-to-air missile system | 0 | 0 | O |  |  |  |
| 118 | 1418 | Australia | Norway | anti-ship missile | 0 | 3 | X |  |  | "offsets incl production of warheads in Australia" — 탄두는 미사일의 부품이므로 오프셋 부품 생산(3). 자동 규칙은 "components"라는 단어만 찾고 "warheads" 등 구체적 부품명은 놓침 |
| 119 | 5994 | Denmark | Germany | armoured engineer/recovery vehicle | 0 | 0 | O |  |  |  |
| 120 | 17289 | Netherlands | United Kingdom | ship engine | 0 | 0 | O |  |  |  |

불일치·플래그 차이 행의 원문 코멘트 (대조용):

- **29732** (Yugoslavia ← Czechoslovakia, self-propelled anti-aircraft gun; 자동 1 → 수동 1/u): `Incl production of compoents or production under licence in Yugoslavia`
- **18362** (Norway ← Sweden, air-search radar; 자동 1 → 수동 1/u): `Incl several versions; incl assembly or production under licence in Norway`
- **13595** (Japan ← United States, anti-ballistic missile missile; 자동 1 → 수동 1/u): `For Patriot Configuration-3 air-defence systems; incl production of components or production under licence in Japan`
- **8808** (Germany ← France, transport aircraft; 자동 2/p → 수동 1/p): `N-2501D version; incl 25 assembled from kits and 161 produced in FRG`
- **26600** (Turkiye ← Italy, (armed) trainer aircraft; 자동 2 → 수동 2/p): `SF-260D version; incl some 30 assembled from kits in Turkiye`
- **13546** (Japan ← United States, self-propelled gun; 자동 2 → 수동 1): `Incl assembly/production in Japan`
- **23668** (Spain ← France, transport helicopter; 자동 2 → 수동 2/p): `AS-332B version; in 12 assembled in Spain; designated HT-21 in Spain`
- **28734** (unknown recipient(s) ← Germany, short-range air-to-air missile; 자동 3 → 수동 ?/u): `Recipient uncertain; produced in FRG for export to NATO countries; part of European production line involving production of components in several NATO countries and final assembly in FRG`
- **28733** (unknown recipient(s) ← United States, short-range air-to-air missile; 자동 3 → 수동 ?/u): `Recipient is one or more NATO country; AIM-9L version; from European production line in FRG (incl production of components in several NATO countries)`
- **13522** (Japan ← United States, gas turbine; 자동 0 → 수동 1): `For 2 Hyuga helicopter carriers; 4 Kongou and 2 Atago destroyers; 5 Takanami and 9 Murasame frigates and 1 Asuka research ship produced in Japan; produced in Japan`
- **1418** (Australia ← Norway, anti-ship missile; 자동 0 → 수동 3): `AUD76 m ($36-49 m) 'Project Sea-1414 Phase-2' (offsets incl production of warheads in Australia); Penguin-2 Mod-7 version for SH-2G helicopters; delivered but stored after SH-2G cancelled`

## 3. 자동 규칙 개선 제안

불일치 건에서 확인한 패턴입니다. 괄호 안은 원문 그대로의 인용입니다.

1. 패턴: `"; produced in [수입국]"` — 세미콜론으로 구분된 **독립절**로서의 "produced in [수입국]" → 현재 자동 판정: 0, 올바른 판정: 1, 해당 deal_id: [13522]
   - 현재 규칙은 코멘트가 "Produced in [수입국]"으로 *시작*할 때만 1로 인식합니다. 13522는 "... 1 Asuka research ship produced in Japan; produced in Japan"처럼 플랫폼 수식구 뒤에 독립절로 다시 나옵니다. 제안: 세미콜론/문장 경계로 분할한 뒤 각 절이 "produced in [수입국]"으로 시작하면 1. "for N [플랫폼] produced in [수입국]" 수식구(명사구 뒤에 바로 붙는 경우)와는 절 단위 분리로 구분 가능합니다.

2. 패턴: `"N produced in [수입국]"` (수량 + produced in 수입국, "assembled from kits"와 병렬) → 현재 자동 판정: 2, 올바른 판정: 1 (partial=Y), 해당 deal_id: [8808]
   - "incl 25 assembled from kits and 161 produced in FRG". 수량이 직접 "produced in [수입국]"을 수식하면 플랫폼이 아니라 해당 무기 자체입니다. 제안: `\b\d+ (assembled|produced)[^;]* in [수입국]` 형태에서 "produced"가 있으면 1, 동시에 partial=Y. 1번 제안과 합치면 "produced in [수입국]"의 위치 제약을 "코멘트 시작"에서 "절 시작 또는 수량 바로 뒤"로 완화하는 것이 됩니다.

3. 패턴: `"assembly/production in [수입국]"` (명사형) → 현재 자동 판정: 2, 올바른 판정: 1, 해당 deal_id: [13546]
   - 규칙 표에는 동사형 "assembled/produced in [수입국]"만 티어 1 예시로 있고, 자동 규칙은 명사형에서 "assembly"만 잡은 것으로 보입니다. 제안: "assembly/production", "assembly or production", "assembly and production" + "in [수입국]"을 "assembled/produced"와 동일하게 1로 처리. (18362 "incl assembly or production under licence in Norway"는 "under licence" 덕분에 잡혔지만, "under licence"가 없는 13546은 놓쳤습니다.)

4. 패턴: `"production of warheads in [수입국]"` 등 **구체 부품명** → 현재 자동 판정: 0, 올바른 판정: 3, 해당 deal_id: [1418]
   - "offsets incl production of warheads in Australia". 자동 규칙은 "components"라는 단어만 찾습니다. 제안: `production of (components|parts|warheads|engines|hulls|sections|subsystems|fuselages|wings|electronics|...) in [수입국]`로 확장하거나, 더 일반적으로 `production of \w+ in [수입국]`에서 목적어가 "N [플랫폼]"이 아니면 3. 오프셋(offsets) 맥락이면 더욱 확실합니다. 이 패턴은 표본 120행 중 1건이지만 전체 데이터에서는 "production of parts", "production of hull sections" 등 변형이 더 있을 가능성이 큽니다.

5. 패턴: 수입국이 `"unknown recipient(s)"`인데 `"production of components in several NATO countries"` → 현재 자동 판정: 3, 올바른 판정: ? (판정 불가, 또는 보수적으로 0), 해당 deal_id: [28734, 28733]
   - 자동 규칙이 "production of components"를 잡을 때 **국가명이 수입국과 일치하는지** 검사하지 않은 것으로 보입니다 (같은 이유로 6145 "with assembly in Norway"는 운 좋게 2로 오판되지 않았지만, 규칙이 국가 일치를 확인하는지 점검 필요). 제안: (a) 수입국이 unknown/"one or more NATO country"인 행은 라이선스 변수를 결측(NA)으로 두고 분석에서 제외, (b) 부품 생산 매칭에도 `in [수입국]` 또는 `[수입국 형용사형] production` 조건을 강제.

6. 플래그 보정: `"incl some 30 assembled"`, `"in 12 assembled"`(incl의 오타) → partial=Y 누락, 해당 deal_id: [26600, 23668]
   - 자동 partial 규칙이 "incl N"만 잡고 "incl some N", "in N"(오타)은 놓친 것으로 보입니다. 제안: `incl(?:uding)? (?:some |about |up to )?\d+` 및 흔한 오타 "in \d+ assembled"도 포함. 티어 판정에는 영향 없음.

7. (선택) uncertain 플래그: `"X or Y"` 형태의 양자택일 표현 (29732, 18362, 13595) — "production of components or production under licence"처럼 SIPRI가 티어 3과 1 중 어느 쪽인지 확정하지 못한 경우입니다. 규칙대로 최고 티어(1)를 주되 uncertain=Y로 표시하면, 강건성 검사에서 이 행들을 낮은 티어로 바꿔 재추정할 수 있습니다.

## 4. 규칙 자체에 대한 의견

1. **"Produced in [수입국]"의 위치 조건이 너무 좁습니다.** 규칙은 코멘트 *첫머리*만 인정하지만, SIPRI 코멘트는 플랫폼 수식구("for N frigates produced in X")와 독립절("; produced in X")을 같은 코멘트에 함께 씁니다(13522, 13161, 13600). 판별 기준을 "문장 시작"이 아니라 "독립절인가, 플랫폼 명사구를 수식하는가"로 바꾸는 것이 규칙의 의도(이 무기 자체를 수입국이 생산했는가)에 더 맞습니다.

2. **"assembled or produced under licence" / "production of components or production under licence" 같은 양자택일 표현의 처리.** 규칙은 "가장 높은 티어"를 적용하라고 하지만, 이것은 한 코멘트에 *두 가지가 모두* 해당할 때("조립 + 부품생산")를 염두에 둔 문장입니다. "A or B"는 SIPRI가 둘 중 하나인지 모른다는 뜻이므로, 최고 티어 적용은 상향 편향을 만듭니다. 논문에서 보수적 코딩(낮은 티어)으로 강건성 검사를 하거나 최소한 uncertain으로 표시할 것을 권합니다. (해당: 29732, 18362, 2953, 26620, 13595 — 5/40의 티어 1이 이런 표현입니다.)

3. **부분 수량의 partial 기준.** "incl 5 produced under licence"(22244)는 partial=Y인데, "50 assembled or produced under licence"(26620), "65 assembled from kits"(15514)는 총 주문 수가 코멘트에 없어 일부인지 전부인지 판정할 수 없습니다. 규칙에 "총 수량 미기재 시 partial=N"으로 명시하거나, 원 데이터의 주문 수량(`number ordered`) 열과 대조해 결정하도록 하는 것이 좋습니다.

4. **개조/재생 사업과 신규 생산의 구분.** 26743(터키 M-60 → M-60T 개조, "produced under licence in Turkiye")과 4011(M-113 개조용 터렛)은 기존 보유 장비의 개조입니다. 규칙상 1이 맞지만, 라이선스 생산을 "산업 역량 이전"으로 해석하는 논문이라면 개조와 신규 생산을 구분하는 보조 변수가 유용할 수 있습니다.

5. **"possibly illegally copied"(7213).** 생산은 이집트에서 이루어졌으므로 1이 맞지만, "라이선스"라는 법적 관계가 불확실합니다. 변수의 개념이 "라이선스 계약"인지 "현지 생산 사실"인지에 따라 uncertain 표시 여부가 달라지므로 코드북에 명시해 두는 것이 좋습니다.

6. **unknown recipient 행.** 수입국이 특정되지 않은 행(28734, 28733)은 수입국 수준 분석에서 어차피 쓸 수 없으므로, 라이선스 코딩 이전 단계에서 제외하는 것이 깔끔합니다.

7. **티어 2 안에서 "assembled from kits"와 "assembled"의 구분.** 둘 다 2로 묶여 있는데, SIPRI는 "from kits"(CKD/SKD)와 단순 "assembled"를 구분해 쓰는 경향이 있습니다. 현재 규칙으로 문제는 없지만, 향후 세분화할 여지가 있습니다.

8. **국가명 변형.** 표본에서는 Turkey/Turkiye, FRG/Germany, GDR, USA/UK, Czech Republic/Czechia, 형용사형("Norwegian production", "Turkish")이 모두 등장했고 자동 규칙이 잘 처리했습니다. 다만 "Soviet Union"/"Russia"(20220: 공급국 Russia, "produced under Russian licence")처럼 공급국 쪽 변형도 규칙에 넣어두면 좋습니다.
