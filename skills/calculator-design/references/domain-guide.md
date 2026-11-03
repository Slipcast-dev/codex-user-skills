# Domain methods

Read only the sections relevant to the current task; this guide does not require every method on every invocation.

- [The calculator decision: when calculators earn investment](#the-calculator-decision-when-calculators-earn-investment)
- [Vanity-calculator vs lead-trap vs transparent-decision-tool](#vanity-calculator-vs-lead-trap-vs-transparent-decision-tool)
- [Input design](#input-design)
- [Calculation logic transparency](#calculation-logic-transparency)
- [Result presentation](#result-presentation)
- [Email-capture decision](#email-capture-decision)
- [Tiered-value structures](#tiered-value-structures)
- [Calculator anti-patterns](#calculator-anti-patterns)
- [Common failure modes](#common-failure-modes)
- [The framework: 12 considerations for calculator design](#the-framework-12-considerations-for-calculator-design)
- [Closing: calculators earn the email when they would have been worth paying for](#closing-calculators-earn-the-email-when-they-would-have-been-worth-paying-for)

## The calculator decision: when calculators earn investment

Before designing the calculator, decide whether a calculator is the right tool for the audience and the goal.

**Calculators earn investment when:**

- The audience faces a specific calculation as part of a decision. ROI on a software purchase, savings from a refinance, monthly cost of an expense, sizing for a service tier. Without a real calculation in the audience's actual workflow, the calculator becomes a vanity tool.
- The calculation is non-trivial. Multiplying two numbers does not need a calculator; calibrating across 5-10 inputs with branching logic does.
- The brand has methodology authority. The calculator's output has to be defensible. Brands without methodology authority (or unwilling to disclose methodology) often produce calculators audiences do not trust.
- The follow-up sequence has a real purpose for the lead. Calculators capture a specific signal (the inputs reveal the lead's situation); the sequence has to use that signal.

**Calculators do NOT earn investment when:**

- The audience does not actually run this calculation. A calculator solving a problem the audience does not have produces low usage.
- The calculation is trivial. A "savings calculator" that computes "monthly cost x 12" does not earn its build.
- The brand cannot disclose methodology honestly. If the math depends on assumptions the brand cannot defend, the calculator becomes a vanity tool by necessity.
- A simpler magnet would serve the same audience and goal. Templates and checklists are cheaper to build and maintain than calculators; choose the calculator only when the calculation is the value.

The decision is not "should we have a calculator"; it is "is the calculator the right next investment for this specific audience and goal."

Detail in [`references/calculator-investment-criteria.md`](calculator-investment-criteria.md).

---

## Vanity-calculator vs lead-trap vs transparent-decision-tool

The keystone framing.

**Vanity-calculator.** Inputs and outputs that do not actually help anyone decide anything. "Calculate your marketing ROI" with random multipliers; "estimate your savings" with no defensible methodology. Looks impressive in a screenshot; helps nothing in a real decision. Cost: leads downloaded the result, found it useless, and remember the brand as the source of the useless tool.

**Lead-trap.** Genuine calculation logic but the result is hidden behind an email gate. The user inputs 8 fields, hits "Calculate," and sees "enter your email to see your result." Manipulative; reader resents the friction; conversion drops below baseline because the audience can tell when the gate is bait rather than value-add.

**Transparent-decision-tool.** Genuine calculation that gives the result immediately. Email gate for advanced features (PDF report, custom analysis, save-and-compare across scenarios) where the additional value justifies the ask. The reader gets the answer they came for; the brand gets the email through demonstrated generosity.

The litmus test. After running the calculator, can a stranger in the target audience defend the result to a stakeholder? Can they cite the methodology behind the number? If yes, the calculator is a transparent-decision-tool. If they got a number with no defensible source, the calculator is vanity. If they could not see the result without giving an email, the calculator is a lead-trap.

---

## Input design

The calculator's inputs are the audience's first interaction. Bad input design loses the user before the calculation runs.

**The principle.** Each input should be necessary for the calculation, easy for the user to provide, and respectful of the user's time.

**Necessary.** If an input does not affect the output meaningfully, do not ask for it. Calculators that ask 18 inputs but only use 5 in the actual math signal that the form is collecting data for sales rather than for the calculation. The audience can tell.

**Easy to provide.** Use defaults from honest assumptions. "Average company size" preset to a reasonable industry baseline. "Typical conversion rate" preset to a defensible number. Defaults reduce the cognitive load and let the user adjust where their context differs.

**Respectful of time.** Group related inputs visually. Show only the fields the user is currently working through (progressive disclosure where it helps). Indicate progress so the user knows how many steps remain.

**Input types.**

- Numeric (revenue, customer count, monthly cost). The most common. Often warrants tooltip explaining what the number represents.
- Slider (percentage estimates, conversion rates). Good for ranges where exact values are not knowable.
- Dropdown (industry, company size, region). Good for predefined categories.
- Toggle (feature on/off, scenario A vs B). Good for binary choices.
- Free text (only when the value is genuinely user-specific and cannot be calculated). Use sparingly; free text is friction.

Detail in [`references/input-design-patterns.md`](input-design-patterns.md).

---

## Calculation logic transparency

The defensibility of the result is the calculator's credibility currency.

**The principle.** The audience should be able to inspect the methodology. Either the calculation is shown openly, or a methodology link explains it, or the team is willing to share the spec on request.

**Methodology disclosure options.**

- **Inline formulas.** "Your savings = (current cost x 12) - (our cost x 12) + implementation savings of $X." Explicit and verifiable.
- **Methodology page.** A link from the calculator to a page explaining the assumptions, sources, and formulas. The audience can read if they care; defaults are good for those who do not.
- **Source citations.** When inputs come from external benchmarks ("Industry Average: 14 percent"), cite the source. Uncited benchmarks erode trust.
- **Assumption list.** A list of the calculator's assumptions, plain-language. "We assume you are comparing month-over-month after a 3-month implementation period."

**The vanity-calculator failure.** Assumptions hidden, sources missing, formulas opaque. The audience uses the tool, gets a number, and cannot defend it. The brand is invisible in their next conversation about the decision because the calculator did not earn the credibility.

**The transparent-tool win.** Assumptions visible, sources cited, formulas inspectable. The audience uses the tool, gets a number, and can defend it. The brand is in the conversation because the audience cites the calculator as their source.

Detail in [`references/calculation-logic-transparency.md`](calculation-logic-transparency.md).

---

## Result presentation

The result is the calculator's product. Bad result presentation wastes the calculation work.

**The principle.** The result should be specific, contextualized, and actionable.

**Specific.** A number with units. "Estimated annual savings: $14,200." Not "Significant savings." Not "Up to 60 percent off."

**Contextualized.** Compare to a baseline the user can understand. "Based on your inputs, you would save $14,200 annually compared to your current configuration." The context makes the number interpretable.

**Actionable.** What does the user do with this number? "Use this estimate to make the case to your CFO" or "Save this scenario to compare against alternative configurations" or "Get a PDF report you can share." The next step is the calculator's bridge from result to action.

**Result-presentation patterns.**

- **Headline number.** The single most important output, large and prominent.
- **Breakdown.** Sub-results that explain how the headline number was calculated.
- **Visualization.** Bar chart, comparison table, or simple graphic that helps the user see the relationship.
- **Scenario comparison.** "Your current state vs the optimized state." Useful when the calculator is illustrating a delta.

**Avoid.**

- Burying the result. The result should be visible immediately, not after a scroll.
- Result followed by 5 paragraphs of marketing. The result is what the user came for; marketing belongs after, not before.
- Result that requires re-entering all inputs to view. Persist inputs and results within the session.

Detail in [`references/result-presentation-patterns.md`](result-presentation-patterns.md).

---

## Email-capture decision

What to gate, what to give freely.

**The principle.** Give the audience the result they came for. Gate the additional value (PDF report, custom analysis, save-and-compare, saved scenarios across visits).

**What to give freely.**

- The headline result.
- The breakdown of how the result was calculated.
- A visualization of the result.
- The methodology disclosure.

**What to gate (with email or account creation).**

- A formatted PDF report the user can share or save.
- A saved scenario the user can revisit and compare against alternatives.
- A custom analysis (a deeper version of the calculation, often delivered later).
- Email-based notifications when assumptions change or new benchmarks emerge.

**The lead-trap failure.** The headline result is gated. The user inputs 8 fields, hits Calculate, sees "enter your email to see your result." Conversion drops because the audience perceives the manipulation. The lead-trap pattern is short-term thinking.

**The transparent-tool win.** The result is free; the additional value is gated. Conversion is honest; lead quality is high because the lead opted in for the additional value, which signals real interest.

Detail in [`references/email-capture-decision-tree.md`](email-capture-decision-tree.md).

---

## Tiered-value structures

The architecture that lets calculators capture leads honestly.

**The principle.** The calculator delivers tiered value: free immediate result + gated advanced features.

**Tier 1 (free, no gate):** the headline result, the breakdown, the methodology, basic visualization.

**Tier 2 (email-gated):** a formatted PDF, a saved scenario, an emailed copy of the result.

**Tier 3 (account or sign-up gated):** save-and-compare across multiple scenarios over time, advanced analysis, integration with the brand's product or service.

**The tier-design discipline.**

- Each tier should add real value over the previous. If Tier 2 is just "the same result in a PDF," the tier does not justify the email ask.
- The gate at each tier should be matched to the value. Email for Tier 2; account creation only for Tier 3.
- The tier transitions should feel natural. The user gets the free result, sees the additional value visibly, and chooses whether to opt in for it.

**Worked example.**

A B2B SaaS pricing calculator.

- Tier 1 (free): the user enters team size and use case, sees the recommended plan and the estimated monthly cost. Methodology link explains tier breakpoints.
- Tier 2 (email-gated): a PDF showing the recommended plan, the calculation, and a comparison to alternative plans the user might consider.
- Tier 3 (account-gated): a saved scenario the user can revisit; ability to compare against historical pricing if the calculator is used periodically; option to receive notifications if pricing or recommended plans change.

Each tier earns its gate.

Detail in [`references/tiered-value-structures.md`](tiered-value-structures.md).

---

## Calculator anti-patterns

Patterns that look like calculators but degrade trust.

**The lead-trap.** Result hidden behind email. Detail in keystone framing.

**The vanity output.** A number that looks impressive but does not help any real decision. "Your marketing efficiency score is 87." 87 of what?

**The hidden-methodology calculator.** No way to see the math; no methodology page; no assumption list. The audience uses the tool, gets a number, and cannot defend it.

**The interrogation form disguised as calculator.** 18 input fields, of which 5 affect the math. The form is collecting sales-qualification data under cover of calculation.

**The misleading-baseline calculator.** "Industry Average" or "Typical Customer" baselines that are flattering to the brand and unsourced. The audience that knows the industry sees the gap.

**The misaligned-units calculator.** "Estimated savings: 14X" without a base value. Or "60 percent improvement" without saying improvement in what.

**The static-assumption calculator.** Assumptions hardcoded in 2022 that have not been updated. The calculator's outputs are stale.

**The mobile-broken calculator.** Calculator works fine on desktop, breaks on mobile. The mobile audience either bounces or gets a worse experience that misrepresents the brand.

Detail in [`references/calculator-anti-patterns.md`](calculator-anti-patterns.md).

---

## Common failure modes

Rapid-fire. Diagnoses in [`references/common-calculator-failures.md`](common-calculator-failures.md).

- "Conversion rate is high; downstream conversion is near zero." Lead-trap or vanity-output pattern; the audience captured did not get value, did not engage with the follow-up, did not convert.
- "Audience visits the calculator, runs it once, never returns." Calculator does not produce a save-worthy or share-worthy result; no reason to come back.
- "Sales team says the calculator-sourced leads are unqualified." Calculator's audience-fit weak; the calculation does not match the buyer's actual decision.
- "We get questions about how the calculator works; we have no answer." Methodology not documented; the team cannot defend the calculator's outputs.
- "We updated the product; the calculator outputs are now wrong." No update cadence; the calculator drifted out of sync with the actual offering.
- "The calculator works; nobody uses it." Calculator hidden in the site; no distribution; the audience does not know it exists.
- "Our calculator looks like our competitor's." Generic calculator-template patterns produce generic calculators; the brand differentiation absent.
- "The form has 12 fields and 4 percent conversion." Interrogation-form pattern; the calculator is collecting data, not delivering value.
- "Audience trusts our brand; the calculator outputs feel arbitrary." Methodology disclosure missing; the brand's credibility does not transfer to the tool because the tool does not show its work.

---

## The framework: 12 considerations for calculator design

When designing or auditing a calculator, walk these 12 considerations.

1. **The calculator decision.** Is a calculator the right investment, or would a simpler magnet serve?
2. **Transparent-decision-tool, not vanity or lead-trap.** Result is free; methodology is visible; gate is on additional value, not on the result.
3. **Inputs are necessary, easy, respectful of time.** Each input affects the math; defaults reduce friction; progressive disclosure where it helps.
4. **Calculation methodology disclosed.** Inline formulas, methodology page, source citations, or assumption list.
5. **Result is specific, contextualized, actionable.** Number with units; baseline for interpretation; clear next step.
6. **Tiered value structure.** Free immediate result; gated advanced features; each tier earns its gate.
7. **Email-capture decision honest.** Gate on real value-add (PDF, save-and-compare, custom analysis), not on the result the user came for.
8. **Source attribution clear.** Industry averages, benchmarks, and assumptions all cited or explained.
9. **Mobile experience tested.** Calculator works on the device the audience uses.
10. **Update cadence defined.** When inputs, benchmarks, or product details change, the calculator gets updated.
11. **Distribution planned.** The calculator's audience knows it exists. Landing page, navigation, content references all include the calculator.
12. **Lead quality measured.** Downstream conversion from calculator-sourced leads is the real metric, not surface conversion.

The output of the framework is a calculator that delivers real decision-support value, earns the email through demonstrated generosity, and produces leads the team can convert downstream.

---

## Closing: calculators earn the email when they would have been worth paying for

The calculators that work as compounding assets are the ones the audience trusts. Not impressive screenshots. Not high conversion rates. Trust. The audience runs the calculator, gets a result they can defend, and remembers the brand as the source of the result they used in their actual decision.

That is the bar. Below the bar are vanity-calculators (no real result) and lead-traps (result hidden until you pay with an email). Above the bar are transparent-decision-tools that give the audience the answer freely and capture leads through additional value the audience opts in for.

The discipline is in the design choices. The methodology disclosure that earns credibility. The input design that respects the audience's time. The tiered value structure that makes the email-capture honest. The result presentation that makes the calculator's output usable in the audience's real conversation. The update cadence that keeps the calculator in sync with the offering it represents.

When in doubt, ask: would the audience pay for this calculator if it were not free, and can they defend the result to a stakeholder after they use it? If yes to both, the calculator earns the email. If no to either, redesign or do not ship.

