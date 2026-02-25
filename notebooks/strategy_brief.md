# Strategy Brief: GA360 Funnel Optimization
**Prepared for:** Executive Leadership & Growth Team  
**Date:** February 2026  
**Data Source:** Google Merchandise Store, 903,653 sessions (Aug 2016 -- Aug 2017)

---

## Current State
The Google Merchandise Store converts 1.28% of sessions end to end. Total
observed revenue is $1.78M. The funnel loses the majority of its volume at
two critical junctures, and performance varies dramatically by device type
and traffic source.

---

## Bottleneck 1: Homepage to Category View (86.2% Drop)
**The Problem.** 779,159 sessions land on the homepage and leave without
browsing a single product category. This is the largest absolute volume loss 
in the entire funnel. The homepage is failing to route visitors into the
catalog.

**Strategic Recommendation.** Redesign the homepage to surface category entry points
above the fold. Implement personalized product carousels based on traffic
source and return-visitor behavior. A/B test a "Shop by Category" grid
layout against the current hero-banner approach.

**Target:** reduce drop-off from 86.2% to 75%, which would add approximately
101,000 sessions to the Category View stage.

---

## Bottleneck 2: Product View to Add to Cart (59.6% Drop)
**The Problem.** The funnel from Category View to Product View is incredibly 
efficient (only a 0.2% drop) However, of the **124,188** sessions that reach 
a Product Detail Page, **59.6% (74,049 sessions)** leave without adding it to
their cart. Visitors are browsing but not committing. This suggests friction 
in the product detail page, due to: unclear pricing, insufficient imagery,
missing social proof, or poor calls to action.


**Strategic Recommendation.** Audit the product detail page for conversion barriers.  
Prioritize: adding customer reviews and ratings, improving product photography 
(multiple angles, lifestyle images), displaying inventory urgency signals 
("Only 3 left"), and simplifying the Add to Cart buttonplacement. Run heatmap
analysis (Hotjar or equivalent) on the product detail page to identify 
scroll-depth abandonment.

---

## Bottleneck 3: Mobile Conversion Gap (3.9x Behind Desktop)
**The Problem.** Mobile sessions convert at 0.41% versus 1.58% on desktop.
This gap is statistically significant (Chi-Squared p < 0.001). Mobile
represents 23% of all sessions (208,725) but only 7.4% of transactions.

At desktop-equivalent conversion rates, mobile would generate an
additional ~2,440 transactions.

**Strategic Recommendation.** Commission a mobile UX audit focused on the checkout
flow. The device funnel data shows that mobile drop-off accelerates at the
Add to Cart and Checkout stages. 
Priorities include: reducing form fields in mobile checkout, adding mobile
payment options (Apple Pay, Google Pay), improving page load speed on mobile
(target under 3 seconds), and ensuring tap-target sizes meet accessibility
standards. Measure progress via adedicated mobile conversion rate KPI on a 
weekly cadence.

---

## Bottleneck 4: Referral Traffic Quality (0.11% CR)
**The Problem.** Referral traffic accounts for 262,022 sessions (29% of
total) but converts at only 0.11%, generating just $47,149 in revenue.
Direct traffic (2.35% CR) outperforms referral by a factor of 21x. This
gap is statistically significant (p < 0.001). The referral channel is
delivering volume, not value.

**Strategic Recommendation.** Audit the top 20 referral sources by volume and
conversion rate. Identify which partners send engaged traffic versus
bot-like or misaligned traffic. Renegotiate or terminate partnerships
that produce sub-0.05% conversion rates. Redirect budget toward organic
search optimization (currently 0.91% CR with room to grow) and paid
search (1.86% CR, the third-highest converting channel). Implement UTM
discipline to track referral sub-sources.

---

## Bottleneck 5: International Revenue Leakage
**The Problem.** International sessions represent 59.6% of traffic but
only 2.4% of revenue ($42,627). The top 10 countries by session volume
outside the US (India, UK, Canada, Vietnam, Turkey, Thailand, Germany,
Brazil, Japan) collectively convert at less than 0.1%. Only Canada shows
meaningful traction (0.74% CR).

**Strategic Recommendation.** Determine whether the international traffic is
purchase-intent or informational. If the store does not ship internationally 
or price in local currencies, these sessions are structurally unable to convert. 
Two options: (a) invest in localized pricing, international shipping, and currency
conversion for the top 3 markets (Canada, UK, Germany) where some conversion 
signal exists, or (b) deprioritize international traffic acquisition to reduce 
wasted server costs and focus marketing spend exclusively on US audiences.

---

## Revenue Impact Model

| Initiative                          | Estimated Additional Transactions | Estimated Revenue Impact |
|-------------------------------------|:---------------------------------:|:------------------------:|
| Homepage redesign (86% to 75%)      |                 1,300             |           $200,000       |
| PDP optimization (60% to 50%)       |                   800             |           $123,000       |
| Mobile UX overhaul (0.41% to 0.80%) |                   810             |           $125,000       |
| Referral audit + reallocation       |                   200             |            $31,000       |
| **Total estimated impact**          |              **~2,463**           |        **~$379,500**     |

*Estimates based on current average transaction value of $154.10 and
observed funnel volumes. Actual results will depend on implementation
quality and market conditions.*

---

## Recommended Priority Order

1. **Homepage engagement redesign** - highest volume impact, lowest cost.
2. **Mobile checkout UX overhaul** - validated by statistical testing, clear ROI.
3. **Product detail page optimization** - second largest volume leak.
4. **Referral channel audit** - stops budget waste, quick to execute.
5. **International market decision** - strategic choice, longer timeline.

---

## Measurement Plan

All initiatives should be validated through controlled A/B testing before
full rollout.  
Primary KPIs: stage-specific conversion rate (weekly), end-to-end conversion
rate (weekly), revenue per session (weekly), mobile conversion rate (weekly).  
Secondary KPIs: average session pageviews, bounce rate by landing page, referral
source conversion by partner.
