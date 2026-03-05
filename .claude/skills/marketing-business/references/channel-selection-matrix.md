# Channel Selection Matrix

**Purpose:** Scoring weights for distribution channels across business model types. Used by the go-to-market workflow to rank and recommend channels.

**Score Range:** 1-10 (10 = highest fit)

---

## Scoring Weights by Business Model

The matrix scores each channel for each business model type. Higher scores indicate better channel-model fit.

### SaaS B2B

| Channel | Score | Rationale |
|---------|-------|-----------|
| Content Marketing | 9 | Thought leadership drives B2B trust |
| SEO / Organic Search | 8 | High-intent keyword targeting |
| LinkedIn (Organic) | 9 | Primary B2B professional network |
| Email Marketing | 8 | Nurture long sales cycles |
| Paid Search (SEM) | 7 | Capture high-intent searches |
| Webinars / Events | 8 | Demonstrate product value |
| Developer Communities | 7 | Technical decision-maker reach |
| Partnership Programs | 7 | Co-marketing leverage |
| Display Advertising | 4 | Low conversion for B2B |
| Influencer Marketing | 5 | Niche B2B influencers only |
| Product Hunt / Directories | 6 | Initial visibility boost |
| Referral Programs | 7 | High-trust channel |

### SaaS B2C

| Channel | Score | Rationale |
|---------|-------|-----------|
| Social Media (Organic) | 9 | Consumer engagement hub |
| Paid Social Ads | 8 | Targeted consumer reach |
| Content Marketing | 7 | SEO and brand building |
| SEO / Organic Search | 8 | Consumer search behavior |
| Email Marketing | 7 | Retention and upsell |
| App Store Optimization | 8 | Mobile-first discovery |
| Influencer Marketing | 8 | Consumer trust signals |
| Referral Programs | 9 | Viral growth loops |
| Display Advertising | 5 | Brand awareness at scale |
| Product Hunt / Directories | 7 | Launch visibility |
| Paid Search (SEM) | 6 | Competition for broad terms |
| Video Marketing | 8 | Demonstration and engagement |

### Marketplace

| Channel | Score | Rationale |
|---------|-------|-----------|
| SEO / Organic Search | 9 | Aggregate listing pages rank well |
| Content Marketing | 7 | Category expertise content |
| Social Media (Organic) | 7 | Community of buyers and sellers |
| Paid Search (SEM) | 8 | High-intent transactional queries |
| Email Marketing | 7 | Engagement for both sides |
| Referral Programs | 9 | Network effects amplification |
| Partnership Programs | 8 | Supply-side partnerships |
| PR / Media Coverage | 7 | Credibility for both sides |
| Display Advertising | 5 | Broad awareness |
| Influencer Marketing | 6 | Category-specific influencers |
| App Store Optimization | 7 | Mobile marketplace discovery |
| Affiliate Marketing | 8 | Performance-based growth |

### D2C

| Channel | Score | Rationale |
|---------|-------|-----------|
| Social Media (Organic) | 9 | Brand storytelling |
| Paid Social Ads | 9 | Targeted product discovery |
| Email Marketing | 8 | Loyalty and repeat purchase |
| Influencer Marketing | 9 | Authentic product endorsements |
| Content Marketing | 7 | Lifestyle and brand content |
| SEO / Organic Search | 7 | Product and category searches |
| Referral Programs | 8 | Word-of-mouth amplification |
| Paid Search (SEM) | 7 | Branded and product searches |
| Affiliate Marketing | 7 | Performance-based sales |
| PR / Media Coverage | 7 | Brand credibility |
| Video Marketing | 8 | Product demonstration |
| Display Advertising | 5 | Retargeting for cart recovery |

### E-commerce

| Channel | Score | Rationale |
|---------|-------|-----------|
| SEO / Organic Search | 9 | Product and category pages |
| Paid Search (SEM) | 9 | High-intent shopping queries |
| Email Marketing | 8 | Cart recovery and promotions |
| Social Media (Organic) | 7 | Product showcasing |
| Paid Social Ads | 8 | Retargeting and lookalikes |
| Affiliate Marketing | 8 | Revenue-share partnerships |
| Content Marketing | 6 | Buying guides and reviews |
| Referral Programs | 7 | Customer advocacy |
| Influencer Marketing | 7 | Product reviews |
| Display Advertising | 6 | Retargeting focus |
| Comparison Shopping Engines | 8 | Price-comparison visibility |
| Video Marketing | 6 | Product demonstrations |

### Subscription

| Channel | Score | Rationale |
|---------|-------|-----------|
| Content Marketing | 9 | Value demonstration |
| Email Marketing | 9 | Onboarding and retention |
| SEO / Organic Search | 8 | Problem-solution content |
| Social Media (Organic) | 7 | Community building |
| Paid Search (SEM) | 7 | Category search capture |
| Referral Programs | 9 | Incentivized sharing |
| Influencer Marketing | 6 | Subscription box unboxing |
| Partnership Programs | 7 | Bundle opportunities |
| Webinars / Events | 7 | Education-led growth |
| Paid Social Ads | 7 | Audience targeting |
| Free Trial / Freemium | 9 | Product-led growth |
| App Store Optimization | 6 | Mobile subscription discovery |

### Freemium

| Channel | Score | Rationale |
|---------|-------|-----------|
| Product Hunt / Directories | 9 | Free tool launch visibility |
| SEO / Organic Search | 9 | Free tool search demand |
| Content Marketing | 8 | How-to and comparison content |
| Social Media (Organic) | 8 | Viral sharing of free tools |
| Referral Programs | 9 | In-product referral loops |
| Developer Communities | 8 | Technical user acquisition |
| Email Marketing | 7 | Conversion from free to paid |
| Paid Search (SEM) | 6 | Cost-effective for free offers |
| Video Marketing | 7 | Tutorial and demo content |
| Influencer Marketing | 6 | Tool review and recommendation |
| App Store Optimization | 8 | Free app discovery |
| Partnership Programs | 6 | Integration partnerships |

### Agency

| Channel | Score | Rationale |
|---------|-------|-----------|
| LinkedIn (Organic) | 9 | Professional services network |
| Content Marketing | 9 | Thought leadership and case studies |
| SEO / Organic Search | 8 | Service-specific keyword targeting |
| Referral Programs | 9 | Client referral incentives |
| Email Marketing | 8 | Nurture and thought leadership |
| Webinars / Events | 8 | Expertise demonstration |
| Partnership Programs | 8 | Co-delivery and referral agreements |
| PR / Media Coverage | 7 | Industry recognition |
| Paid Search (SEM) | 6 | Service-specific ads |
| Social Media (Organic) | 6 | Portfolio and culture sharing |
| Clutch / G2 / Directories | 8 | Agency review platforms |
| Speaking / Conferences | 8 | Authority building |

---

## Channel Inventory

The full list of scored channels across all business models (12+ channels):

1. Content Marketing
2. SEO / Organic Search
3. Social Media (Organic)
4. Email Marketing
5. Paid Search (SEM)
6. Paid Social Ads
7. Influencer Marketing
8. Referral Programs
9. Partnership Programs
10. Video Marketing
11. Developer Communities
12. Product Hunt / Directories
13. App Store Optimization
14. Affiliate Marketing
15. Webinars / Events
16. PR / Media Coverage
17. Display Advertising
18. Comparison Shopping Engines

---

## Scoring Methodology

### Composite Score Calculation

```
composite_score = base_score × budget_modifier × audience_modifier
```

Where:
- **base_score**: Raw score from the business model table (1-10)
- **budget_modifier**: Adjusts for budget constraints (0.5-1.0 for paid channels)
- **audience_modifier**: Adjusts for audience-channel affinity (0.8-1.2)

### Budget Modifiers

| Budget Range | Paid Channel Modifier | Organic Channel Modifier |
|-------------|----------------------|------------------------|
| $0 (zero budget) | 0.0 (excluded) | 1.0 (no change) |
| $1 - $500/mo | 0.5 (heavily penalized) | 1.0 (no change) |
| $500 - $2,000/mo | 0.7 (moderately penalized) | 1.0 (no change) |
| $2,000 - $10,000/mo | 0.9 (slight penalty) | 1.0 (no change) |
| $10,000+/mo | 1.0 (no penalty) | 1.0 (no change) |

---

**Reference:** STORY-539, EPIC-075 (Marketing & Customer Acquisition)
