# Product Requirement Document (PRD)

## Myntra StyleGen & FitSense: AI-Powered Contextual Discovery & Fit-Confidence Engine

**Author:** Tamanna Singh Chandel (Candidate for Product Management Internship Jan – Jun 2027)  
**Target Tracks:** Storefront Product (Customer Experience & Search) & Outbound Supply Chain (Returns Reduction)  
**Status:** Ready for Engineering & Prototyping  
**Target Launch Window:** H1 2027  

---

## 1. Executive Summary
Fashion e-commerce platforms experience high top-of-funnel drop-offs and high return rates. At Myntra:
1. **Search & Discovery Friction:** Over 34% of searches represent high-intent, ambiguous queries (e.g., *"outdoor sundowner outfit under ₹2500"*, *"pastel wedding guest kurta"*). Traditional keyword-based search queries fail to understand multi-item context, forcing users to manually search, evaluate, and coordinate individual items. This leads to **18% search abandonment (zero-click sessions)**.
2. **Size & Fit Discrepancy (The Return Crisis):** Return rates across fashion e-commerce sit at **28% - 35%**, with **62% of returns attributed directly to size, fit, and silhouette mismatch**. Each return incurs ₹180 - ₹240 in reverse logistics, quality inspection, repackaging, and inventory depreciation costs.

**Myntra StyleGen & FitSense** solves both pain points in a unified product loop:
- **StyleGen:** A natural language contextual styling engine that parses customer intent (occasion, palette, silhouette, budget) and constructs complete, curated outfit bundles.
- **FitSense:** A cross-brand size normalization and confidence score widget (e.g., *"Based on your size M in Zara, we recommend size L in Roadster with 93% fit confidence"*).

### Projected Business Impact (Annualized for Myntra Scale):
- **+4.2% lift in Search-to-PDP Click-Through Rate (CTR)**.
- **+2.8% lift in Cart-to-Checkout Conversion Rate**.
- **-3.5 percentage point drop in Size-Related Return Rate (RTO)**, saving an estimated **₹42+ Crores** in reverse logistics and inventory turnaround expenses.

---

## 2. Customer Problem Statement & User Research

### 2.1 The "Why": 5-Whys Root Cause Analysis

#### Problem 1: High Search Drop-Off on Long-Tail Queries
1. *Why do users bounce after searching for specific looks?* Because the search results display disjointed single products rather than complete looks matching their prompt.
2. *Why do search results display disjointed single items?* Because existing keyword search engines rely on lexical token matching (e.g., searching for "sundowner dress" matches words in title/tags rather than semantic occasion context).
3. *Why can't users build the look themselves?* High cognitive load: finding matching footwear, jewelry, and outerwear across disparate categories takes 15+ minutes and multiple tabs.
4. *Why does this matter to business?* Session fatigue leads to cart abandonment, and users revert to competitors or social platforms (Instagram) for styling ideas.
5. **Root Cause:** Absence of an intent-aware styling intelligence layer that treats search as a conversational styling problem rather than an isolated catalog lookup.

#### Problem 2: Sizing Uncertainty Driving "Bracketing" & Returns
1. *Why do 32% of apparel orders get returned?* The delivered item does not fit the user's body shape or expectations.
2. *Why didn't the item fit?* Sizing standards vary drastically across brands (e.g., European fit vs. Indian relaxed fit; an 'M' in Vero Moda is often a 'L' in local private labels).
3. *Why didn't the static size chart prevent this?* Size charts display flat garment measurements (chest/waist in inches) that 78% of mobile shoppers do not measure with a tape while browsing.
4. *Why does the user still buy?* Users resort to "bracketing" (buying sizes M and L simultaneously with the intention of returning one) or guessing blindly.
5. **Root Cause:** Lack of contextual cross-brand size translation and dynamic confidence scoring based on customer purchase history and brand-specific sizing deltas.

---

### 2.2 Target Personas

| Persona | Demographics | Behaviors & Motivations | Core Pain Points |
| :--- | :--- | :--- | :--- |
| **Aarav (The Occasion Shopper)** | 23, Tech Analyst, Bangalore | Shops 3-4 days before events (parties, weddings). Values convenience and curated coordination over endless scrolling. | Doesn't know what accessories match a kurta or blazer; dreads receiving an ill-fitting outfit the day before an event. |
| **Priya (The Trend & Brand Explorer)** | 27, Marketing Lead, Delhi | High purchase frequency, buys fast fashion across diverse brands (Mango, Roadster, H&M, Libas). | Frustrated by inconsistent brand sizing; frequently initiates returns which locks up refund balances and wastes delivery time. |
| **Karan (The Value-Conscious Minimalist)** | 21, College Student, Pune | Budget-constrained (<₹2,000 per basket), looks for versatile capsule pieces that can be styled in multiple ways. | Struggles to find complete complementary pieces within budget; abandons search when items in recommendations exceed price ceiling. |

---

## 3. Product Vision & Principles

### Vision Statement
*"Transform Myntra from a transactional search-and-browse catalog into an intelligent personal stylist that understands intent and eliminates the anxiety of ill-fitting clothes."*

### Guiding Product Principles:
1. **Explainable Recommendations:** Never give a black-box recommendation. Always provide the *why* (e.g., *"Roadster runs slim on the shoulders—size up for regular comfort"*).
2. **Frictionless Zero-State:** Do not require users to enter tape measurements or complete a 10-step quiz before seeing value.
3. **Graceful Fallback:** If semantic confidence is low, fall back seamlessly to top-ranking catalog items without breaking the search experience.
4. **Data Privacy First:** Size preferences and body profile inferences must be opt-in, encrypted, and editable at any time.

---

## 4. Feature Prioritization & RICE Matrix

To ensure disciplined execution, candidate features are evaluated using the **RICE Framework** (Reach $\times$ Impact $\times$ Confidence $/$ Effort):
- **Reach:** Monthly active shoppers impacted (Scale: 1 - 10, where 10 = 20M+ users).
- **Impact:** Lift on conversion / return reduction (0.5 = Minimal, 1.0 = Moderate, 2.0 = High, 3.0 = Massive).
- **Confidence:** Data & user research confidence (50% = Medium, 80% = High, 100% = Proven).
- **Effort:** Person-months across PM, Engineering, and Design.

| Feature ID | Feature Name | Description | Reach (1-10) | Impact (0.5-3) | Confidence (%) | Effort (PM-Mo) | RICE Score | Release Phase |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **F-01** | **Contextual Intent Search** | Natural language intent extraction for occasion, silhouette, and budget | 8.5 | 2.0 | 80% | 2.5 | **5.44** | **P0 (v1.0)** |
| **F-02** | **FitSense Cross-Brand Size Matcher** | Translates reference brand size into current item recommendation with confidence % | 9.0 | 3.0 | 90% | 3.0 | **8.10** | **P0 (v1.0)** |
| **F-03** | **One-Click Outfit Bundling** | Dynamic "Complete The Look" bundle with 1-click add-to-cart & combo discount | 7.0 | 2.0 | 80% | 2.0 | **5.60** | **P0 (v1.0)** |
| **F-04** | **Post-Return Fit Feedback Loop** | Micro-survey on return flow feeding brand size delta calibrations | 6.0 | 1.0 | 85% | 1.5 | **3.40** | **P1 (v1.1)** |
| **F-05** | **Virtual AR 3D Try-On** | Real-time body mesh generation and cloth drape simulation | 4.0 | 2.5 | 50% | 8.0 | **0.62** | **P2 (v2.0)** |

---

## 5. Detailed Feature Specifications

### 5.1 Contextual Intent Search & Outfit Bundler (StyleGen)
- **Input:** Natural language search bar supporting queries such as:
  - *"College presentation formal look under ₹3000"*
  - *"Boho chic floral maxi dress with flats for brunch"*
  - *"Sangeet black sherwani look with footwear"*
- **Processing Flow:**
  1. Intent Extraction Layer parses: Occasion, Gender/Category, Color/Palette, Budget cap, Key garment.
  2. Inverted Index & Semantic Ranking scores matching items from catalog using TF-IDF and attribute vectors.
  3. Outfit Coordination Engine selects complementary items (e.g., Topwear + Bottomwear + Footwear + Accessory) within specified total budget.
- **Output:** Search Result Page (SRP) displays an **"AI Curated Ensemble"** banner at the top, followed by individual filtered items.

### 5.2 FitSense Confidence Widget (Storefront PDP)
- **Placement:** Product Detail Page (PDP), adjacent to the Size Selector.
- **UX Components:**
  1. **Reference Size Anchor:** *"Your usual size: Zara [M]"* (inferred from past kept orders or selected via 1-tap dropdown).
  2. **Recommended Size Badge:** *"Recommended for you: Size [L]"*.
  3. **Confidence Meter:** Visual score (e.g., `92% Fit Confidence`).
  4. **Dynamic Explanation Tooltip:**
     - *"Roadster shirts feature a tapered European cut that measures 1.2 inches narrower at chest than Zara M. 87% of shoppers who wear Zara M preferred L in this item."*
  5. **Bracketing Friction Reducer:** If a user attempts to add both sizes M and L of the same item to cart, trigger a gentle nudge:
     - *"Unsure about size? FitSense predicts Size L is your ideal fit. Free 1-click exchange guaranteed if it doesn't fit!"*

---

## 6. Metrics Framework & Telemetry

### 6.1 Metric Tree

```
                      [ North Star Metric ]
                   GMV per Active Search Session
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
[ Top of Funnel (Discovery) ]               [ Bottom of Funnel (Quality & Post-Order) ]
- Search-to-PDP CTR (+4.2%)                 - Add-to-Cart Rate (+3.1%)
- Zero-Result Query Rate (-65%)             - Checkout Conversion Rate (+2.8%)
- Outfit Bundle Adoption Rate (14%)          - Apparel Return Rate (RTO) (-3.5%)
                                            - Size-Related Return Share (-18%)
```

### 6.2 Guardrail Metrics
- **P95 Search Latency:** Must remain $<180\text{ms}$ under peak concurrent loads.
- **Catalog Coverage:** At least 85% of active apparel catalog must have calibrated FitSense size mappings.
- **Return CSAT:** Post-order satisfaction for shoppers using FitSense must not drop below $4.4 / 5.0$.

---

## 7. Experimentation & A/B Testing Framework

### Test Design: 3-Cell Controlled Experiment

| Variant | Allocation | Experience Description |
| :--- | :---: | :--- |
| **Control (A)** | 33.3% | Standard Myntra keyword search + static brand size chart table. |
| **Variant B** | 33.3% | StyleGen Intent Search enabled; Standard static size chart. |
| **Variant C (Full Solution)** | 33.4% | StyleGen Intent Search + FitSense Confidence Widget on PDP. |

### Statistical Criteria:
- **Primary Hypothesis:** Variant C will decrease 30-day apparel return rate by $\ge 2.5\%$ while increasing average order value (AOV) by $\ge 5\%$ due to outfit bundling.
- **Sample Size:** $n = 120,000$ unique user sessions per variant to achieve $80\%$ statistical power at $\alpha = 0.05$ significance level.
- **Runtime:** 14 full days (accounting for day-of-week seasonality and weekend fashion shopping spikes).

---

## 8. Cross-Functional Operations & Program Management

### 8.1 Stakeholder Matrix (RACI)
- **Product Manager (Owner):** PRD, metric tracking, user stories, A/B test decision.
- **Engineering (Responsible):** Search indexing, NLP intent classification, PDP widget integration, latency optimization.
- **Catalog & Merchandising (Consulted):** Tagging taxonomy, brand measurement guidelines.
- **Customer Support & Returns (Informed):** Return reason categorization updates, agent training for FitSense queries.

### 8.2 Rollout Phases
1. **Sprint 1-2 (Alpha):** Internal dogfooding with Myntra employees across top 10 apparel brands.
2. **Sprint 3-4 (Beta):** 5% canary traffic release on Android App.
3. **Sprint 5-6 (Experiment):** 33% 3-cell A/B test over 14 days.
4. **Sprint 7 (GA):** 100% rollout to all users if guardrails pass and primary metrics show statistically significant lift.
