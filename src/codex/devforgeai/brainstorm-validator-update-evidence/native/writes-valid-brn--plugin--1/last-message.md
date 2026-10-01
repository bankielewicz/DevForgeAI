BRN-001 written to [docs/specs/brainstorm/BRN-001.md](/tmp/devforgeai-brn-trial-6dybx00e/project/docs/specs/brainstorm/BRN-001.md) (framework: diverge-converge)  
Problems: 4 · Ideas: 12 · Assumptions: 8  
Promoted: none confirmed yet; proposed priorities are in section 6.  
Open questions recorded: owner, current booking/reminder setup, appointment volumes, baseline accuracy, staffing/budget, patient barriers, local requirements, standby demand, and financial returns.

**My recommendation: start with three practical changes.**

1. **Make reminders actionable.** Trial reminders around three days and one day before appointments, with an easy confirmation or change route. Retain a phone option.
2. **Use selective personal follow-up.** Prioritize failed reminders and unresolved long appointments. Keep unconfirmed bookings in place while staff follow up.
3. **Create an opt-in short-notice list.** Match available patients to the correct clinician and appointment length, then confirm replacements when cancellations occur.

Reminders, easier appointment changes, and short-notice lists are supported by [NHS outpatient guidance](https://www.england.nhs.uk/long-read/reducing-did-not-attends-dnas-in-outpatient-services/); their effect in your clinic needs testing.

The write-up includes nine other options, tradeoffs, a sample reminder, and a **six-week pilot**. It recommends deferring deposits and software purchases and avoiding routine double-booking.

Measure both no-shows and unused chair time. An illustrative reduction from **12.5% to 8%** would mean **nine fewer no-shows per 200 appointments**; the financial gain depends on additional completed visits and program costs.

**Verification:** PASS for document validation, scoring, and decision labels. Model provenance verification: NOT_RUN because the host did not expose the model identifier.

**Next step:** use the six-week pilot as the starting plan. For formal requirements later, select the DevForgeAI PRD skill with `BRN-001`; its input is `docs/specs/brainstorm/BRN-001.md`.
