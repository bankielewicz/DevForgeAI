# MVP Launch Checklist

This reference file provides a business-model-aware launch checklist covering five operational domains. The skill uses the user's detected business model type (SaaS, marketplace, service, or product) to adapt which items are presented, omitting irrelevant items and including model-specific items.

**Output path:** When the skill generates a personalized checklist for the user, write the result to `devforgeai/specs/business/operations/launch-checklist.md`.

---

## Business Model Adaptation

The checklist supports four business model types. Each domain section contains universal items applicable to all models, plus model-specific items that are tagged for conditional inclusion.

- **SaaS model specific** items focus on subscription billing, recurring payment infrastructure, and digital service delivery
- **Marketplace model specific** items focus on seller onboarding, buyer trust, and two-sided platform mechanics
- **Service model specific** items focus on client engagement, deliverable scoping, and capacity planning
- **Product model specific** items focus on supply chain, inventory management for product and marketplace models, and fulfillment logistics

When adapting for a specific model, include all universal items plus the items tagged for that model. Omit items tagged for other models.

---

## Legal Domain

- [ ] **Business Entity Registration** - Register your legal entity (LLC, Corp, sole proprietorship) to establish liability protection and enable contracts
- [ ] **Terms of Service Draft** - Define the legal agreement users accept when using your product, covering liability limits, acceptable use, and dispute resolution
- [ ] **Privacy Policy Creation** - Document how you collect, store, and process user data to comply with GDPR, CCPA, and other data protection regulations
- [ ] **Intellectual Property Protection** - File trademarks, copyrights, or patents to protect your brand name, logo, and core innovations from competitors
- [ ] **Cookie and Tracking Consent** - Implement cookie consent banners and tracking disclosures required by ePrivacy regulations in target markets
- [ ] **Compliance Checklist Review** - Verify industry-specific compliance requirements such as PCI-DSS for payments, HIPAA for health data, or SOC 2 for enterprise SaaS

## Financial Domain

- [ ] **Business Bank Account Setup** - Open a dedicated business account to separate personal and business finances for clean bookkeeping and tax filing
- [ ] **Pricing Model Validation** - Test your pricing tiers with target customers to confirm willingness to pay and validate unit economics before launch
- [ ] **Subscription Billing Infrastructure** - Set up recurring payment processing with automated invoicing, proration, and failed payment retry logic for SaaS models
- [ ] **Payment Gateway Integration** - Connect a payment processor (Stripe, PayPal, or equivalent) to accept customer payments securely at launch
- [ ] **Financial Forecasting Baseline** - Build a 12-month revenue and expense forecast to track burn rate, runway, and break-even targets post-launch
- [ ] **Tax Registration and Collection** - Register for sales tax or VAT collection in your operating jurisdictions to avoid post-launch tax liability surprises

## Marketing Domain

- [ ] **Landing Page with Value Proposition** - Create a clear, compelling landing page that communicates your unique value proposition and includes a call-to-action
- [ ] **Email List and Nurture Sequence** - Build a pre-launch email list and set up automated welcome and onboarding email sequences for new signups
- [ ] **Social Media Presence Established** - Claim brand handles on relevant platforms and publish foundational content that establishes credibility before launch
- [ ] **Launch Announcement Strategy** - Plan your launch communications across channels including email, social media, communities, and press outreach
- [ ] **Analytics and Attribution Setup** - Install tracking pixels, UTM conventions, and conversion funnels to measure marketing effectiveness from day one
- [ ] **Customer Testimonial or Beta Feedback** - Collect and publish testimonials, case studies, or beta user feedback to provide social proof at launch

## Technical Domain

- [ ] **Production Environment Deployment** - Deploy your application to a production-ready environment with proper DNS, SSL certificates, and CDN configuration
- [ ] **Monitoring and Alerting Setup** - Configure uptime monitoring, error tracking, and performance alerting to detect and respond to production issues within minutes
- [ ] **Backup and Recovery Verification** - Test database backup procedures and verify you can restore from backup within your target recovery time objective
- [ ] **Security Audit Completion** - Perform a security review covering authentication, authorization, input validation, and dependency vulnerability scanning
- [ ] **Load Testing and Capacity Planning** - Run load tests simulating expected launch traffic to confirm your infrastructure can handle initial demand without degradation
- [ ] **Seller Onboarding and Verification Flow** - Build and test the seller registration, identity verification, and storefront setup flow for marketplace models

## Operations Domain

- [ ] **Customer Support Channel Setup** - Establish support channels (email, chat, help center) with documented response time targets and escalation procedures
- [ ] **Onboarding Flow Documentation** - Create step-by-step onboarding guides, tooltips, and walkthrough content that helps new users reach their first success quickly
- [ ] **Incident Response Playbook** - Document procedures for handling outages, data breaches, and critical bugs including communication templates and escalation paths
- [ ] **Inventory Management for Product and Marketplace Models** - Set up stock tracking, reorder alerts, and fulfillment workflows for physical goods logistics
- [ ] **Feedback Collection Mechanism** - Implement in-app feedback forms, NPS surveys, or user interview scheduling to capture user sentiment immediately after launch
- [ ] **Operational Metrics Dashboard** - Build a dashboard tracking key operational metrics like active users, support ticket volume, churn rate, and time-to-resolution

---

## Progressive Disclosure and Micro-Task Chunking

This checklist uses progressive disclosure to prevent overwhelm by presenting a manageable, digestible number of items at a time. Research on cognitive load and ADHD-friendly design shows that attention management directly impacts task completion rates, particularly for solo founders.

### Chunking Configuration

- **Chunk size:** Present items in groups of 5 to 7 items at a time
- **Threshold:** When the checklist contains more than 20 items, activate micro-task chunking automatically
- **Pacing:** Use adaptive pacing prompts between chunks to let the user control their pace

### Chunking Logic

When the total item count exceeds the 20-item threshold, present items section by section rather than displaying the entire checklist at once. Group items by their domain section and show one domain at a time.

After completing each chunk, display an adaptive pacing prompt before continuing to the next section:

**Pacing prompt examples:**
- "Ready for the next section? We will move on to [domain name]."
- "Shall we continue to the next domain?"
- "Would you like to take a break or continue to the next section?"
- "Let us continue with the next group of items when you are ready."

### Fallback Behavior

If chunking fails or the user requests it, fall back to displaying the full list of all items at once. Users can also skip chunking entirely by requesting the complete checklist upfront via a "display all items" option.
