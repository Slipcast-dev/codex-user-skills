# Domain methods

Read only the sections relevant to the current task; this guide does not require every method on every invocation.

- [The lead magnet decision: when to build one, when not to](#the-lead-magnet-decision-when-to-build-one-when-not-to)
- [Thin-bait vs kitchen-sink-resource vs earned-value-magnet](#thin-bait-vs-kitchen-sink-resource-vs-earned-value-magnet)
- [Format selection](#format-selection)
- [The "would they pay for this" test](#the-would-they-pay-for-this-test)
- [Audience-fit qualification](#audience-fit-qualification)
- [Title and presentation discipline](#title-and-presentation-discipline)
- [Delivery and follow-up sequence design](#delivery-and-follow-up-sequence-design)
- [Format-specific quality gates](#format-specific-quality-gates)
- [Common failure modes](#common-failure-modes)
- [The framework: 12 considerations for lead magnet design](#the-framework-12-considerations-for-lead-magnet-design)
- [Closing: magnets earn the email when they earn the reader's afternoon](#closing-magnets-earn-the-email-when-they-earn-the-readers-afternoon)

## The lead magnet decision: when to build one, when not to

Before designing the magnet, decide whether a magnet is the right investment.

**A lead magnet earns investment when:**

- The audience exists in volume but is not yet on the list. Traffic without conversion is the gap a magnet fills.
- The product or service has a long consideration cycle. The list builds the relationship across the consideration window.
- The audience has a specific, immediate problem that a focused resource can address. Magnets work when the gap they fill is concrete.
- The follow-up sequence has a real purpose. Without a sequence that turns subscribers into something (customers, community members, qualified leads), the magnet is list-building theater.

**A lead magnet does NOT earn investment when:**

- The audience would convert directly without a magnet. SaaS with a free trial, ecommerce with a discount code, or freemium with a low-friction signup may not need a magnet between the visitor and the product.
- The team cannot commit to the follow-up. A list without a sequence is a list that decays.
- The topic is too broad to focus a single resource. "Marketing" is not a magnet topic; "the welcome-email template that 4x'd our trial-to-paid rate" is.
- Sales calls or demos are the next step. If the goal is a booked call, design the call-booking flow, not the magnet.

The decision is not "should we have a magnet"; it is "is the magnet the right next investment for this specific audience and goal."

Detail in [`references/lead-magnet-decision-criteria.md`](lead-magnet-decision-criteria.md).

---

## Thin-bait vs kitchen-sink-resource vs earned-value-magnet

The keystone framing.

**Thin-bait.** "10 tips for X" PDFs that are 200 words of fluff behind an email gate. The headline overpromises; the contents underdeliver. The reader downloads, skims, deletes, and unsubscribes within a week. The conversion-rate metric looks fine; the list quality and brand trust both degrade. Cost: every subscriber acquired through thin-bait costs more than they appear to, because the unsubscribe rate, the reduced sender reputation, and the reduced list-trust each compound.

**Kitchen-sink-resource.** 80-page "Ultimate Guide" containing everything anyone could want about the topic. Includes nothing the reader actually needs RIGHT NOW. Bookmarked, never read, eventually forgotten. Cost: the magnet does not produce the moment of "I needed this and got it," which is the moment the relationship starts. Subscribers stay on the list out of inertia; the relationship never deepens; future emails get ignored.

**Earned-value-magnet.** Solves a specific, immediate problem the reader has. Genuine standalone value, the kind that would be worth paying for if it were not free. Qualifies the lead by audience-fit. Warms the reader for a specific related offer that follows. The reader downloads, uses the resource, gets the result, and remembers the brand as the source of that result.

The litmus test. Hand the magnet to a non-subscriber in the target audience. Watch them use it. Does the resource produce the promised outcome inside the time the reader was willing to spend? If yes, the magnet is earned-value. If the reader downloads and never opens, the magnet is thin-bait or kitchen-sink-resource regardless of how the headline reads.

---

## Format selection

Magnets come in formats. Each format has strengths, weaknesses, audience-fit signals, and conversion-rate baselines. Choosing the wrong format wastes the topic and the design effort.

**Templates.** A starting artifact the reader fills in or adapts. Strong for audiences who need to produce a specific deliverable (a brief, a spec, a pitch deck, an email). Strong because the value is immediate and concrete. Weak when the template is too generic to feel custom.

**Checklists.** A sequence of items to verify or complete. Strong for audiences executing a known process where the gap is comprehensiveness, not direction. Strong because the format signals "you can use this in 10 minutes." Weak when the checklist reads as marketing rather than as a working tool.

**Swipe files.** A curated collection of examples (subject lines, headlines, ad copy, design references). Strong for audiences who learn from examples and need inspiration rather than instruction. Weak when the swipes are stale or unattributed.

**Mini-courses.** A multi-part email or video sequence delivering structured learning. Strong for audiences willing to invest sequential attention; strong because the sequence creates multiple touchpoints. Weak when the course is filler or when each lesson does not stand on its own.

**Free tools (calculators, quizzes, generators).** Interactive web tools that produce a result. Strong for audiences who want a personalized output rather than a generic resource. Strong because the interaction qualifies the lead by inputs. Detail in `calculator-design` and `quiz-and-assessment-design`.

**Ebooks.** Long-form treatment of a topic. Strong for audiences researching a complex decision; strong when the ebook reads as a definitive resource. Weak when used as a default format for topics that would have served the reader better as a checklist or template.

**Video series.** Sequential video content delivered behind a gate. Strong for topics that benefit from demonstration; strong for audiences who learn from video. Weak when the production overhead exceeds the topic's value or when the audience does not consume video content at the time-of-magnet moment.

The choice depends on the audience's preferred consumption mode, the topic's natural shape, and the production overhead the team can sustain. A great template often outperforms a mediocre ebook on the same topic.

Detail in [`references/format-selection-patterns.md`](format-selection-patterns.md).

---

## The "would they pay for this" test

The single test that distinguishes earned-value from thin-bait.

The question. If the magnet were not free, would someone in the target audience actually pay for it? Not pay enterprise pricing, not pay for a course, but pay something (5 dollars, 25 dollars, 100 dollars) because the value is concrete enough to justify the cost?

The honest answer matters. A magnet that fails this test is signaling that the value is below the threshold of "I would pay for this," which means the reader's time investment to download and consume it is at the edge of "worth it."

The test is not perfect. Some valuable resources are hard to price (how much is a great checklist worth?). But the test catches the magnets that exist primarily to capture an email rather than to deliver value.

Three failure modes the test catches.

- The 5-page PDF that summarizes blog content. Free elsewhere; not pay-worthy.
- The "Ultimate Guide" that nobody finishes. Pay-worthy in theory; not delivered in usable form.
- The template that is so generic it adds no value over starting from scratch. Pay-worthy framing; thin in execution.

The test the magnet should pass.

- A reader in the target audience would pay for this resource because it produces a result they need.
- The resource is in a usable form (consumable in the time the reader is willing to spend, applicable to their specific situation).
- The resource is hard to find elsewhere or hard to assemble at the same quality.

If the magnet passes the test, it earns the email. If it fails, redesign before launching.

Detail in [`references/would-they-pay-for-this-test.md`](would-they-pay-for-this-test.md).

---

## Audience-fit qualification

The magnet as filter, not just bait.

A great magnet does two things at once. It delivers value (which earns the email). It also filters for the right audience (which earns the long-term relationship).

**Filter through the headline.** The headline tells the wrong audience to opt out. "The 5-step framework for B2B SaaS pricing decisions" filters out ecommerce founders, freelancers, and consumer-app PMs. The conversion rate from the visiting traffic drops; the conversion rate from the right segment of that traffic is what compounds.

**Filter through the topic.** A magnet on a niche topic attracts a niche audience. Generic topics attract generic audiences who churn off the list. Specific topics attract specific audiences who stay.

**Filter through the format.** A 60-minute video course filters out audiences who will not invest 60 minutes. A 2-page checklist filters in audiences who want quick wins. The format signals what the brand expects of the relationship.

**Filter through the offer adjacent to the magnet.** The follow-up sequence often makes a soft offer for a related product or service. The magnet should be tightly enough scoped that the audience who downloads it is also the audience who would consider the adjacent offer.

The filtering principle. A magnet that converts 50 percent of visitors but produces 5 percent qualified leads is worse than a magnet that converts 15 percent of visitors and produces 40 percent qualified leads. Optimize for the qualified lead, not for the surface conversion rate.

Detail in [`references/audience-fit-qualification.md`](audience-fit-qualification.md).

---

## Title and presentation discipline

The magnet's title is the conversion lever and the qualification filter at the same time.

**Title patterns that work.**

- **Specific outcome + specific audience.** "The B2B onboarding email sequence that 3x'd our 14-day activation rate (for SaaS founders)."
- **Specific deliverable + specific situation.** "The pricing one-pager for SaaS founders raising a seed round."
- **Specific framework + specific problem.** "The 4-question framework for deciding whether to fire a customer."
- **Specific count + specific value.** "23 onboarding emails, with the open and click rate for each."

**Title patterns to avoid.**

- "Ultimate Guide to X." Vague. Promises too much. Underdelivers reliably.
- "The Complete X Playbook." Same failure mode. Promises completeness; delivers volume.
- "Free [Topic] Resource." Generic. Tells the reader nothing about why this resource is the one to download.
- "10 Tips for Better X." Listicle framing signals thin content.

**Presentation discipline beyond the title.**

- The cover or preview image should reinforce the specificity. A clean type-driven cover often outperforms a cluttered one.
- The landing page (handled by `landing-page-copy`) should preview the magnet, not just describe it.
- The first page of the magnet should deliver value within the first read, not warm up with author bio and brand-positioning.

Detail in [`references/title-and-presentation-discipline.md`](title-and-presentation-discipline.md).

---

## Delivery and follow-up sequence design

The sequence is the magnet's second act. Without it, the magnet is one transaction; with it, the magnet starts a relationship.

**The delivery moment.** The reader fills the form and expects the resource immediately. Delivery delay (manual review, scheduled send) breaks the moment. The first email should deliver the asset and confirm the next step.

**The first 7 days.** The reader is most engaged in the days right after download. The sequence should make use of that window: a follow-up that helps them apply the resource, a related artifact that extends the value, a soft introduction to the brand and the next step.

**The medium-term.** Days 8 to 30, the sequence transitions from "value-add" to "ongoing relationship." Newsletter signup, related-content rotation, or a soft offer for the adjacent product or service.

**The honest offer.** When the sequence makes an offer, the offer should match the magnet's audience. A magnet on B2B onboarding should not pitch a consumer course; the audience signal would be wasted.

**The opt-out.** A reader who unsubscribes from the magnet sequence is not a failure; they are a clean filter. The list quality stays higher when the unfit subscribers leave on their own.

Detail in [`references/delivery-and-follow-up-sequences.md`](delivery-and-follow-up-sequences.md).

---

## Format-specific quality gates

Each format has quality gates specific to that format. A great template fails different tests than a great mini-course.

**Template gates.** Does the reader produce a usable artifact in under 30 minutes? Are the prompts specific enough to feel custom? Is the template adaptable across the segment of the audience or rigidly bound to one situation?

**Checklist gates.** Is each item actionable today? Does the checklist sequence reflect actual workflow order? Is the checklist scoped narrowly enough to feel comprehensive within scope?

**Swipe file gates.** Are the swipes attributed (where possible)? Are they current (not 5 years stale)? Is the curation visible (the reader can see why each swipe is included)?

**Mini-course gates.** Does each lesson deliver standalone value (not "you will learn the answer in lesson 4")? Is the cumulative time commitment honest in the title? Does the course end with a clear next step (not just "thanks for taking the course")?

**Calculator and quiz gates.** Detail in `calculator-design` and `quiz-and-assessment-design`.

**Ebook gates.** Is the ebook navigable (table of contents, page numbers, summary boxes) such that a reader who does not finish still extracts value? Is the production quality consistent with the brand it represents?

**Video series gates.** Is each video shot at a quality the brand can sustain? Is the audio consistently clear? Is the runtime honest in the listing?

Each format's gates exist because thin-bait can hide in any format. The quality gates make hiding harder.

Detail in [`references/format-specific-quality-gates.md`](format-specific-quality-gates.md).

---

## Common failure modes

Rapid-fire. Diagnoses in [`references/common-lead-magnet-failures.md`](common-lead-magnet-failures.md).

- "Conversion rate is great, list quality is terrible." Thin-bait pattern; magnet attracts the wrong audience or fails to deliver the promised value.
- "We ship a magnet; nothing happens after." No follow-up sequence; the magnet is one transaction rather than the start of a relationship.
- "Our 80-page Ultimate Guide gets downloaded but never read." Kitchen-sink-resource; comprehensive in scope, useless in application.
- "We changed the format from PDF to webinar; conversion rate dropped." Format mismatched to audience; the audience would consume a PDF in 10 minutes but will not block 60 minutes for a webinar.
- "The magnet works in paid traffic but not organic." The audience reaching the magnet through paid is different from the organic audience; the magnet may fit one but not the other.
- "Subscribers go cold after the first email." Sequence absent or poorly designed; the value evaporates after delivery.
- "We have 5 magnets; one converts well, the others are dead." Magnet portfolio not maintained; audiences move and topics decay; periodic audit missing.
- "The follow-up offer mismatches the magnet's audience." Magnet attracted one segment; offer pitches a different one; conversion to the offer near zero.
- "We cannot tell which traffic source produces qualified leads." Attribution missing or rolled up at the wrong level; lead-quality signal not connected back to source.
- "The team built three magnets last quarter; the team avoids talking about results." Magnets shipped without success metric definition; results ambiguous or quietly underwhelming.

---

## The framework: 12 considerations for lead magnet design

When designing or auditing a lead magnet, walk these 12 considerations.

1. **The magnet decision.** Is a magnet the right investment for this audience and goal, or does the funnel work without one?
2. **Earned-value, not thin-bait or kitchen-sink-resource.** The magnet would be worth paying for; it solves a specific problem in usable form.
3. **Format matched to audience and topic.** The format reflects how the audience consumes content and how the topic naturally shapes.
4. **The "would they pay for this" test.** Pass before launching.
5. **Audience-fit qualification.** The magnet filters for the right audience, not just maximum conversion.
6. **Title and presentation discipline.** Specific, honest, signals what is inside.
7. **Delivery in the moment.** First email arrives immediately; the asset is in that email.
8. **Follow-up sequence designed.** The 30 days after download have a purpose, an arc, and a soft offer that matches the audience.
9. **Format-specific quality gates passed.** The format's specific tests verified before launch.
10. **Lead quality measured, not just conversion rate.** What percentage of subscribers fit the audience the magnet was designed for? Where that measurement is unavailable, state the gap per the data-availability rule.
11. **Attribution to source.** The team can tell which source produced which leads at which quality.
12. **Audit cadence.** The magnet portfolio gets reviewed periodically; underperformers retired.

The output of the framework is a lead magnet that earns the email by delivering real value, qualifies the audience by filtering at the headline and topic level, and starts a relationship through a sequence the team has actually designed.

---

## Closing: magnets earn the email when they earn the reader's afternoon

The magnets that work as compounding assets are the ones the reader uses. Not downloads. Not bookmarks. Uses. The reader opens the resource, applies it, and gets a result they would have paid for if they had to.

That is the bar. Below the bar is thin-bait (the resource is too thin to use) or kitchen-sink-resource (too much to consume). Above the bar is the relationship: the reader remembers the brand as the source of the result, opens the next email, and considers the offer when it comes.

The discipline is in the design choices upstream of the form. The format matched to the audience and topic. The title that filters and earns. The pricing thought experiment that catches the thin magnets before launch. The follow-up sequence designed before the magnet ships, not after. The audit cadence that retires the magnets that stopped working.

When in doubt, ask: would the audience pay for this if it were not free, and will the team commit to the sequence after the download? If yes to both, the magnet earns the email. If no to either, redesign or do not ship.

