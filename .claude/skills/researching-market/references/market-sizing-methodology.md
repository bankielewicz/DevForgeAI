# Market Sizing Methodology Reference

This reference documents the three primary methodologies for estimating TAM, SAM, and SOM market sizes.

---

## Top-Down Methodology

The top-down approach starts with a large, known market figure and narrows it down to the target segment.

**Process:**
1. Find total industry revenue from published reports (e.g., Gartner, Statista, IBISWorld)
2. Apply geographic filters to narrow to target region
3. Apply segment filters to narrow to target customer type
4. Apply product/service category filters

**Best Used For:**
- TAM estimation when industry reports are available
- Markets with well-documented revenue figures
- Broad market categories with established research

**Confidence Impact:**
- High confidence when using multiple recent sources (< 2 years)
- Medium confidence with single source or older data
- Low confidence when extrapolating from adjacent industries

**Example:**
```
Global CRM software market = $69.1B (Source: Gartner 2025)
North America share = 45% = $31.1B
SMB segment = 30% = $9.3B (TAM)
```

---

## Bottom-Up Methodology

The bottom-up approach builds estimates from unit economics: number of potential customers multiplied by average revenue per customer.

**Process:**
1. Identify total number of potential customers in target segment
2. Determine average revenue per customer (ARPU, contract value, transaction size)
3. Multiply: Total Addressable Customers x Average Revenue = Market Size
4. Cross-validate against top-down figures when available

**Best Used For:**
- SAM and SOM estimation
- Markets where customer counts are known or estimable
- Businesses with clear pricing models

**Confidence Impact:**
- High confidence when customer counts are well-documented
- Medium confidence when estimating customer counts from proxies
- Low confidence when both customer count and ARPU are estimates

**Example:**
```
US small businesses in target segment = 2.1M (Source: SBA 2024)
Average annual software spend = $1,200
SAM = 2.1M x $1,200 = $2.52B
```

---

## Fermi Estimation Methodology

Fermi estimation breaks complex unknowns into smaller, estimable components. Named after physicist Enrico Fermi, this method is the fallback when external data is unavailable.

**Process:**
1. Decompose the market size question into 3-5 estimable sub-questions
2. Estimate each component independently using logic and available proxies
3. Multiply components together to reach an estimate
4. Validate the result against any known benchmarks
5. Document all assumptions explicitly

**Best Used For:**
- SOM estimation (realistic capture rates)
- Novel markets without published research
- Quick validation of top-down/bottom-up estimates
- Fallback when internet-sleuth returns no data

**Confidence Impact:**
- Fermi estimates typically receive Low or Medium confidence
- Can be upgraded to Medium if validated against independent data points
- Always document assumptions for transparency

**Example:**
```
How many coffee shops in a mid-size US city?
- City population: ~500,000
- Adults (70%): 350,000
- Daily coffee drinkers (60%): 210,000
- Average visits per week: 3
- Customers per shop per day: ~200
- Shops needed: (210,000 x 3/7) / 200 = 450 shops
```

For detailed Fermi estimation guidance, see: [fermi-estimation.md](fermi-estimation.md)

---

## Methodology Selection Guide

| Tier | Primary Method | Secondary Method | Fallback |
|------|---------------|-----------------|----------|
| TAM | Top-down (industry reports) | Bottom-up (total addressable customers) | Fermi estimation |
| SAM | Bottom-up (serviceable customers x ARPU) | Top-down (TAM with filters) | Fermi estimation |
| SOM | Bottom-up (realistic capture x ARPU) | Fermi estimation | N/A |

---

## Source Quality Guidelines

**Tier 1 Sources (High confidence):**
- Published industry reports (Gartner, McKinsey, Statista, IBISWorld)
- Government statistics (Census, BLS, SBA)
- Public company filings (10-K, annual reports)

**Tier 2 Sources (Medium confidence):**
- Industry association reports
- Trade publication analyses
- Academic research papers

**Tier 3 Sources (Low confidence):**
- Blog posts and opinion pieces
- Outdated reports (> 3 years old)
- Single-source estimates without corroboration

All sources must include attribution: URL, report name, author, and publication date when available.
