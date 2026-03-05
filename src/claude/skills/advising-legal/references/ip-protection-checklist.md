# IP Protection Checklist for Software and SaaS Companies

A progressive-disclosure reference for understanding intellectual property protection strategies relevant to software developers, SaaS founders, and technology startups.

---

## How to Use This Checklist

This checklist covers four categories of intellectual property (IP) protection. Each section progresses from foundational concepts to actionable steps. Use it as a starting point, then consult a qualified attorney for advice tailored to your situation.

---

# Copyright

## Overview

Copyright protection is **automatic** upon creation of an original work fixed in a tangible medium. For software, this means your source code, documentation, UI designs, and other creative works are protected the moment you write them. No filing is required for basic protection.

## Copyright Notice

Adding a **copyright notice** to your work is recommended but not legally required in most jurisdictions. A standard notice follows this format:

```
Copyright (c) 2026 [Your Name or Company]. All rights reserved.
```

Place copyright notices in:
- Source file headers
- README and LICENSE files
- Application footer or about page
- API documentation

## Registration

**Registration** with the U.S. Copyright Office is **voluntary** and **not required** for copyright to exist. However, registration does **strengthen** your legal position significantly:

- Enables pursuit of **statutory damages** (up to $150,000 per work for willful infringement)
- Provides stronger **remedies** in court, including attorney fee recovery
- Creates a public record of ownership
- Required before filing an infringement lawsuit in the U.S.

**How to register:**
- File online at [https://www.copyright.gov/registration/](https://www.copyright.gov/registration/)
- Fee is approximately $45-$65 per application
- Processing takes 3-6 months on average

## Software-Specific Considerations

- Source code is copyrightable as a literary work
- Object code and compiled binaries are also protected
- APIs may have limited copyright protection (see Oracle v. Google)
- Open-source licenses are copyright licenses -- choose carefully
- SaaS applications: the code is protected even if users never see it
- Copyright does NOT protect ideas, algorithms, or functionality -- only the specific expression

## Checklist

- [ ] Add copyright notices to all source files
- [ ] Include a LICENSE file in every repository
- [ ] Register key works with the Copyright Office
- [ ] Document authorship and creation dates
- [ ] Review open-source license compatibility before incorporating third-party code
- [ ] Ensure employee/contractor agreements include IP assignment clauses

**Resources:**
- [U.S. Copyright Office](https://www.copyright.gov/)
- [WIPO Copyright Treaty](https://www.wipo.int/treaties/en/ip/wct/)

---

# Trademark

## Overview

Trademarks protect brand identifiers: names, logos, slogans, and other marks that distinguish your software or SaaS product in the marketplace. Unlike copyright, trademark rights are built through use in commerce.

## What Can Be Trademarked

For software and SaaS companies:
- Product names (e.g., your application name)
- Company names and logos
- Service marks for SaaS offerings
- Distinctive UI elements (trade dress) in rare cases
- Domain names that function as brand identifiers

## Common Law vs. Registered Trademarks

- **Common law rights** arise automatically from use in commerce (limited to geographic area)
- **Federal registration** with the USPTO provides nationwide priority and legal presumptions
- Use the TM symbol for unregistered marks, the (R) symbol for registered marks

## Registration Process

1. Conduct a comprehensive trademark search (TESS database + common law)
2. File an application with the USPTO ([https://www.uspto.gov/trademarks](https://www.uspto.gov/trademarks))
3. Application is examined by a trademark attorney at the USPTO
4. If approved, mark is published for opposition (30-day window)
5. Registration issues if no opposition is filed

## Software-Specific Considerations

- SaaS product names should be distinctive (avoid generic/descriptive terms)
- App store listings create trademark use evidence
- International expansion requires separate filings in each jurisdiction (Madrid Protocol can simplify)
- Monitor for infringement in app stores, domain registrations, and social media
- API names and developer tool brands can be trademarked

## Checklist

- [ ] Search for conflicting marks before launching a product name
- [ ] File federal trademark applications for key product and company names
- [ ] Use proper trademark symbols (TM or R) consistently
- [ ] Monitor marketplaces and app stores for infringing uses
- [ ] Document first use in commerce dates
- [ ] Register trademarks in key international markets
- [ ] Include trademark usage guidelines in brand documentation

**Resources:**
- [USPTO Trademark Search (TESS)](https://tess2.uspto.gov/)
- [Madrid Protocol International Filing](https://www.wipo.int/madrid/en/)
- [INTA Trademark Basics](https://www.inta.org/topics/trademark-basics/)

---

# Patent Basics

## Overview

Patents protect inventions -- novel, non-obvious, and useful processes, machines, or compositions of matter. In software, patents can cover novel algorithms, technical processes, and system architectures. Patents require formal application and examination.

## What Is Patentable in Software

- Novel technical processes and methods
- Unique system architectures solving a technical problem
- Hardware-software integration innovations
- Data processing methods with concrete technical improvements
- Machine learning model training techniques (in some jurisdictions)

**Note:** Abstract ideas, mathematical formulas, and business methods without technical implementation are generally NOT patentable.

## The Patent Application Process

1. Document the invention thoroughly (date, description, drawings)
2. Conduct a prior art search ([https://patents.google.com/](https://patents.google.com/))
3. File a provisional application (12-month priority period, lower cost)
4. File a non-provisional application within 12 months
5. Examination by USPTO patent examiner (typically 18-36 months)
6. Respond to office actions as needed
7. Patent granted or abandoned

## Software-Specific Considerations

- Patent prosecution for software is complex -- work with a patent attorney
- Open-source contributions may trigger patent grant clauses (e.g., Apache 2.0)
- SaaS delivery model does not prevent patentability
- Consider defensive publication as an alternative (prevents others from patenting)
- Patent trolls are a real risk in the software industry -- defensive strategies matter
- Cross-licensing agreements are common in enterprise software

## Cost Considerations

- Provisional application: $1,500 - $5,000 (with attorney)
- Non-provisional application: $8,000 - $20,000+
- Maintenance fees over 20-year life: $5,000+
- International filings multiply costs significantly

## Checklist

- [ ] Maintain an invention disclosure log
- [ ] Conduct prior art searches before filing
- [ ] File provisional applications for promising inventions
- [ ] Evaluate patent vs. trade secret for each innovation
- [ ] Review competitor patents periodically
- [ ] Include patent assignment clauses in employment agreements
- [ ] Consider defensive patent strategies (e.g., LOT Network, OIN)

**Resources:**
- [Google Patents](https://patents.google.com/)
- [USPTO Patent Center](https://patentcenter.uspto.gov/)
- [WIPO Patent Cooperation Treaty](https://www.wipo.int/pct/en/)

---

# Trade Secrets

## Overview

Trade secrets protect confidential business information that derives economic value from being secret. For software and SaaS companies, this is often the most practical and immediately valuable form of IP protection. Protection lasts indefinitely -- as long as secrecy is maintained. However, if information is **publicly disclosed**, protection is permanently lost.

## What Qualifies as a Trade Secret in Software

Trade secrets in the software industry commonly include:

- **Algorithm** implementations and optimizations
- **Model weight** files and trained ML parameters
- **Database schema** designs and query optimization strategies
- **Business logic** rules and proprietary calculation methods
- Customer lists, pricing models, and sales strategies
- Internal tooling and build processes
- Security architecture and vulnerability assessments
- Deployment configurations and infrastructure-as-code details
- Performance benchmarking data and tuning parameters

## Protection Requirements

To maintain trade secret status, you must demonstrate reasonable efforts to keep the information secret:

### Administrative Controls
- **NDA** agreements with all employees, contractors, and partners who access sensitive information
- Clearly mark confidential documents and code repositories
- Include trade secret clauses in employment agreements
- Conduct exit interviews reminding departing employees of obligations
- Consult a qualified **attorney** or **legal counsel** experienced in trade secret law

### Technical Controls
- **Access control** mechanisms: role-based access, principle of least privilege
- Encryption at rest and in transit for sensitive data
- Audit logging for access to trade secret materials
- Secure code repositories with granular permissions
- Network segmentation isolating proprietary systems
- Secure deletion procedures for decommissioned systems

### Organizational Controls
- Classify information by sensitivity level
- Limit distribution to need-to-know basis
- Regular security training for all team members
- Incident response plan for potential trade secret misappropriation
- Periodic review of who has access to what

## Software-Specific Considerations

- SaaS delivery inherently protects server-side code (users cannot inspect it)
- API design should avoid exposing proprietary algorithms
- Open-sourcing code eliminates trade secret protection for that code
- Reverse engineering of publicly distributed software may be lawful
- Employee mobility is the #1 risk for trade secret loss in tech
- Consider code obfuscation for client-side distributed code
- Container images and deployment artifacts may contain trade secrets

## Trade Secret vs. Patent Decision

| Factor | Trade Secret | Patent |
|--------|-------------|--------|
| Duration | Indefinite (if secret maintained) | 20 years |
| Cost | Low (administrative) | High ($10K-$50K+) |
| Public disclosure required | No (must stay secret) | Yes (published) |
| Independent discovery | No protection | Still protected |
| Reverse engineering | No protection | Still protected |
| Best for | Business logic, data, processes | Novel inventions, algorithms |

## Checklist

- [ ] Identify and inventory all trade secrets
- [ ] Implement NDAs for all personnel with access
- [ ] Deploy access control systems with audit logging
- [ ] Mark confidential materials clearly
- [ ] Conduct regular access reviews
- [ ] Include trade secret clauses in all employment and contractor agreements
- [ ] Establish incident response procedures for potential misappropriation
- [ ] Review and update trade secret inventory quarterly
- [ ] Consult legal counsel on trade secret program adequacy

**Resources:**
- [Defend Trade Secrets Act (DTSA)](https://www.congress.gov/bill/114th-congress/senate-bill/1890)
- [WIPO Trade Secrets Overview](https://www.wipo.int/tradesecrets/en/)
- [Uniform Trade Secrets Act](https://www.uniformlaws.org/committees/community-home?CommunityKey=3a2538fb-e030-4e2d-a9e2-90373dc05b93)

---

# Cross-Cutting Concerns

## Employee and Contractor Agreements

Every software company should have:
- IP assignment agreements (ensure company owns what employees create)
- Non-disclosure agreements (protect trade secrets)
- Non-compete clauses (where enforceable -- varies by jurisdiction)
- Invention disclosure obligations

## Open Source Compliance

- Audit all third-party dependencies for license terms
- Maintain a software bill of materials (SBOM)
- Understand copyleft obligations (GPL, AGPL) vs. permissive licenses (MIT, Apache)
- AGPL is particularly relevant for SaaS -- it can trigger source code disclosure

## International Considerations

- IP rights are territorial -- protection must be sought in each jurisdiction
- The Berne Convention provides baseline copyright protection across 180+ countries
- Patent and trademark filing strategies should align with market expansion plans
- Consider the Madrid Protocol for international trademark registration
- Data protection laws (GDPR, CCPA) intersect with trade secret management

---

# Quick Reference Matrix

| IP Type | Protection Scope | Duration | Registration | Cost |
|---------|-----------------|----------|--------------|------|
| Copyright | Expression of code, docs, designs | Life + 70 years | Optional (recommended) | Low |
| Trademark | Brand names, logos, slogans | Indefinite (with use) | Recommended | Medium |
| Patent | Novel inventions, processes | 20 years | Required | High |
| Trade Secret | Confidential business info | Indefinite (if secret) | None | Low |
