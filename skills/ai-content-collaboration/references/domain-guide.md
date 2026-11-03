# Domain methods

Read only the sections relevant to the current task; this guide does not require every method on every invocation.

- [Humans own, AI accelerates](#humans-own-ai-accelerates)
- [Where AI legitimately participates](#where-ai-legitimately-participates)
- [Where humans must own](#where-humans-must-own)
- [Hybrid workflow patterns](#hybrid-workflow-patterns)
- [Voice ownership preservation](#voice-ownership-preservation)
- [The AI slop problem](#the-ai-slop-problem)
- [Disclosure and transparency](#disclosure-and-transparency)
- [Team training and calibration](#team-training-and-calibration)
- [Ethics: training data, attribution, intellectual honesty](#ethics-training-data-attribution-intellectual-honesty)
- [Common failure modes](#common-failure-modes)
- [The framework: 12 considerations for AI content collaboration](#the-framework-12-considerations-for-ai-content-collaboration)
- [Closing: collaboration, not replacement](#closing-collaboration-not-replacement)

## Humans own, AI accelerates

The keystone framing.

The pathology to avoid is treating AI as either a magic content factory (cheap, fast, scaled, output quality optional) OR as a forbidden intruder (purity gospel that does not survive contact with deadlines). Both readings produce bad work.

The discipline that produces durable work: humans own the content; AI accelerates the work. Specifically:

**Humans own.** Editorial judgment, voice, distinctive POV, fact accuracy, ethical decisions, what to publish versus what to kill, brand voice, narrative arc, tone calibration, reader empathy, claim verification.

**AI accelerates.** Research synthesis, draft generation against a brief, copy edit suggestions, alternative phrasings, summary, transcription, quality-control automation at scale.

The line. AI does work that the human directs and verifies. AI does NOT make decisions about what publishes, who is quoted, what is true, or what voice the brand uses.

The litmus test. If your AI-assisted piece publishes without a human being able to defend every claim, every position, and every word, you have crossed the line. The piece is AI's work, dressed in your byline. Readers eventually notice.

---

## Where AI legitimately participates

A non-exhaustive list of stages where AI in the loop is fine and often improves the work.

- **Research synthesis.** AI condenses long-form sources into briefs the writer reads. Saves hours; the writer still reads and verifies.
- **Outline generation against a brief.** AI proposes an H2 / H3 structure from a brief; the editor approves or restructures.
- **First-draft generation.** AI produces a draft against an explicit brief; the human edits substantially.
- **Alternative phrasings.** AI offers 3 versions of a sentence; the human picks one or rewrites.
- **Copy edit suggestions.** AI catches typos, awkward phrasings, repetition.
- **Summary and abstraction.** AI condenses long pieces into TL;DRs.
- **Transcription.** AI transcribes interview audio; the human verifies.
- **Translation drafts.** AI produces a translation draft; a native speaker reviews and corrects.
- **Quality-control automation at scale.** AI flags pages in a programmatic SEO set that need human review.
- **Idea generation.** AI proposes 30 angles; the human picks 3.

In each case, AI accelerates work the human still owns. The acceleration is real; the ownership stays unchanged.

Detail in [`references/ai-participation-boundaries.md`](ai-participation-boundaries.md).

---

## Where humans must own

The boundary list.

- **Editorial judgment.** What to publish, what to kill, what is worth saying. AI cannot decide whether a piece is good enough to ship.
- **Voice.** Brand voice, distinctive POV, the way THIS publication sounds different from the next one. AI default voice is generic by construction; voice is a human contribution.
- **Fact verification.** Every claim, every statistic, every quote, every named person. AI hallucinates; humans verify.
- **Ethical decisions.** What is appropriate to publish, what is harmful, what crosses lines, what disclosure is required.
- **Reader empathy.** What the reader actually needs from this piece, not what the algorithm scores well.
- **Quote attribution.** Real people who actually said the thing, with consent where relevant.
- **Tone calibration on hard topics.** Grief, illness, sensitive history, contested politics. AI defaults to anodyne; humans calibrate to context.
- **Narrative arc.** How the piece unfolds, where the reader's attention goes. AI produces shapes; humans choose them.
- **Final approval.** The human who signs off is accountable for what shipped.

The "human in the loop" framing is necessary but insufficient. A human briefly reviewing AI-generated content before publish is not ownership; it is rubber-stamping. Ownership requires the human to have made the actual decisions the piece embodies.

---

## Hybrid workflow patterns

Five patterns that work, with tradeoffs.

**1. AI-first draft, human-edit-heavy.** AI produces a 90% draft; the human spends 60% of the time editing. Output: efficient for high-volume editorial; risks generic voice if editing is light.

**2. Human-first outline + research, AI-draft, human-rewrite.** Human builds the outline and gathers research; AI drafts within that scaffold; human rewrites in voice. Output: preserves voice better; slower than AI-first.

**3. AI-as-research-assistant, human-writes.** AI condenses sources into a brief; human writes the entire piece from the brief. Output: highest voice fidelity; slowest.

**4. Human-writes, AI-as-editor.** Human drafts; AI suggests edits, alternative phrasings, copy edits; human accepts or rejects. Output: writer voice preserved; AI catches details.

**5. AI-generates-at-scale, human-samples.** For programmatic SEO. AI generates thousands of pages; human samples 50 to 200 with editorial-qa discipline. Output: scaled production; depends entirely on template quality and sampling discipline.

The pattern that fits depends on volume, voice sensitivity, team skill, and time budget. No pattern is "the right one"; pattern selection is a real decision that should match the production context.

Detail in [`references/hybrid-workflow-patterns.md`](hybrid-workflow-patterns.md).

---

## Voice ownership preservation

Voice is the dominant casualty of careless AI workflows. The patterns that preserve voice.

- **Voice guidelines as prompt input.** Every AI generation includes the brand voice guidelines as context. Generic AI defaults regress without this.
- **Sample text as voice anchor.** Feed the AI 2 to 3 paragraphs of canonical brand voice as part of the prompt. AI mimics what it sees more than what it is told.
- **Mid-draft voice check.** At the halfway mark of a long piece, have a human or a separate AI pass read for voice drift. Long AI generations regress halfway through almost always.
- **Final pass in human voice.** The human edits the closing sections in their own voice; this is where the piece's emotional register often lands.
- **Reject the bland.** Any sentence that could appear in any other piece on the topic gets rewritten. Voice lives in the specific.

The honest framing. Voice is the hardest thing to preserve in AI-assisted work and the easiest thing to lose. Programs that do not actively preserve voice end up with content that is technically correct, semantically generic, and indistinguishable from competitors using the same tools.

Detail in [`references/voice-ownership-preservation.md`](voice-ownership-preservation.md).

---

## The AI slop problem

AI slop is the term of art for AI-generated content that is technically functional but reads as generic, derivative, and signal-less. Cross-reference `editorial-qa`'s ai-content-audit-patterns reference for the detection patterns; this section addresses prevention.

**Patterns that produce slop.**

- AI does too much of the work (no real human direction or rewriting)
- Generic prompts (no brand voice context, no audience specificity, no anti-pattern guidance)
- No editorial judgment in the loop (AI generates, human glances, ship)
- Volume prioritized over quality (10x more pages can mean 10x more slop, not 10x more value)
- No iteration (first draft ships; no rewrite for voice)

**Patterns that prevent slop.**

- Strong briefs (per `content-brief-authoring`)
- Voice guidelines as prompt context
- Heavy human editing pass
- Iteration: AI draft, then human rewrite, then AI suggestions, then human final
- Editorial judgment at every gate

The reader-detection problem. Readers can often sense AI-flavored content even when they cannot articulate why. Generic openings, predictable structures, "perfect" grammar that is emotionally flat. Slop loses reader trust over time even when individual pieces are not penalized.

Detail in [`references/ai-slop-detection-and-avoidance.md`](ai-slop-detection-and-avoidance.md) and cross-reference editorial-qa's audit patterns.

---

## Disclosure and transparency

When should AI usage be disclosed to readers?

The tiered framework.

- **Always disclose.** Journalism, news reporting, attributed expert opinion, content where AI tools are the subject.
- **Default disclosure (consider context).** Thought leadership where the byline is doing trust work, regulated industries, content that influences purchase decisions.
- **Generally not necessary.** Marketing copy, descriptive product content, programmatic data pages, copy edit assistance only.
- **Clearly fine without disclosure.** AI as research assistant only; AI for transcription; AI for spelling and grammar suggestions.

The principle. Disclose when the reader's understanding of the content's origin would change their trust in it. A bylined opinion piece purportedly by a named expert that is substantially AI-drafted is a trust violation; a product description on an ecommerce site that was AI-drafted is not.

**Disclosure language patterns (when used).**

- "AI tools assisted in research and drafting; the author edited and verified all claims."
- "This piece was generated programmatically from [data source]; reviewed by [team] before publish."
- Avoid hedging language like "may have used AI" or "could have been AI-assisted"; be specific or omit.

Industry-specific norms vary. Major journalism organizations have published explicit AI usage standards. Content marketing has weaker norms but is moving toward disclosure for high-trust pieces.

Detail in [`references/disclosure-and-transparency-patterns.md`](disclosure-and-transparency-patterns.md).

---

## Team training and calibration

Inconsistent AI usage across a team produces inconsistent output. The discipline.

- **Documented AI policy.** Which uses are approved, which require explicit permission, which are prohibited.
- **Calibration sessions.** Editors review AI-assisted pieces from multiple writers, surface differences, agree on standards.
- **Voice library updates.** As voice evolves, the prompts and sample text fed to AI evolve with it.
- **Quality benchmarks.** What does "AI-assisted but on-voice" look like for your brand? Document it with examples.
- **Tool standardization or intentional pluralism.** Team uses one tool consistently OR documents which tools fit which tasks.
- **Forbidden patterns list.** This team does not use AI for X (whatever X is for your context).
- **Onboarding.** New writers learn the AI policy and calibration in their first 2 weeks.

The pathology. AI usage emerges informally, every writer develops their own patterns, output drifts, editors cannot pinpoint why pieces feel off. The discipline is making AI usage explicit, calibrated, and documented.

Detail in [`references/team-training-and-calibration.md`](team-training-and-calibration.md).

---

## Ethics: training data, attribution, intellectual honesty

AI tools were trained on copyrighted material. That is the simple ethical reality of every major LLM in 2026. The catalog's position on this question is not "AI use is unethical" (that would render the catalog itself hypocritical) but "intellectual honesty about AI involvement is non-negotiable."

The principles.

- **Do not pass AI work as fully human-written.** Bylined content where the byline implies human craft requires substantial human craft.
- **Do not claim AI did not help when it did.** False denials are worse than disclosure.
- **Do not generate content that closely mirrors copyrighted source material.** AI tools can produce near-replicas of training data when prompted carelessly; humans verify originality.
- **Attribute when borrowing.** Ideas, frameworks, statistics that came from specific sources get cited.
- **Do not fabricate quotes or expertise.** Hallucinated quotes attributed to real people are dishonest regardless of whether AI generated them.
- **Be honest about AI capabilities and limits.** Do not oversell AI as more capable than it is.

The intellectual-honesty frame supersedes any specific policy debate. Teams that treat AI usage with intellectual honesty produce content readers can trust over time. Teams that hide, deny, or rationalize lose trust eventually.

Detail in [`references/ethics-and-intellectual-honesty.md`](ethics-and-intellectual-honesty.md).

---

## Common failure modes

Rapid-fire. Diagnoses in [`references/common-collaboration-failures.md`](common-collaboration-failures.md).

- "We used AI and the content feels generic." Voice not preserved; not enough human rewriting.
- "Hallucinated facts made it to publish." Fact-verification gate skipped or rushed.
- "Different writers produce wildly different AI-assisted output." No team calibration.
- "Our AI-assisted SEO content got penalized." Slop volume plus thin templates plus no QA discipline.
- "We cannot tell what was AI versus human." No AI usage tracking; teams should document at the workflow level.
- "Readers complained about AI-flavored content." Slop reaching audience; intensify human craft pass.
- "We disclosed AI usage and lost credibility." Depends on context; disclosure is sometimes a trust gain, sometimes a loss; calibrate to audience norms.
- "Our AI tools changed and our content shifted." Over-coupled to one tool's specific behavior; methodology should be tool-agnostic.
- "We are producing 10x more content but the same audience growth." Volume was not the constraint that was binding; quality was.
- "The team is using AI inconsistently." Calibration sessions overdue.
- "An expert byline turned out to be substantially AI-drafted." Ethics breach; correct, disclose, recalibrate.

---

## The framework: 12 considerations for AI content collaboration

When designing or auditing an AI-assisted content workflow, walk these 12 considerations.

1. **Humans own; AI accelerates.** Make this explicit in your workflow, not implicit.
2. **Participation boundaries.** Document where AI legitimately helps, where humans must own.
3. **Hybrid pattern selection.** Match the pattern to volume, voice sensitivity, time budget.
4. **Voice guidelines as prompt input.** Every AI generation includes brand voice context.
5. **Voice drift sampling.** Long pieces drift mid-way; sample throughout.
6. **Fact verification gate.** Every claim, every quote, every stat verified before publish.
7. **AI slop prevention.** Heavy human editing, strong briefs, iteration.
8. **Disclosure tiering.** Disclose when origin would change reader trust; calibrate to audience.
9. **Team calibration.** Documented policy, calibration sessions, voice library.
10. **Tool-agnostic methodology.** Workflow shape stays constant as tools change.
11. **Ethical floor.** Intellectual honesty, no fabrication, no hidden AI in trust-sensitive work.
12. **Final accountability.** The human who signs off is accountable; AI does not sign off.

The output of the framework is a workflow document the team can reference: AI participation rules named, hybrid pattern selected, voice preservation patterns specified, disclosure tier set, calibration cadence committed, ethical floor articulated, accountable signer named for each piece.

---

## Closing: collaboration, not replacement

AI in content workflows is neither magic nor menace. It is a category of tooling that, like every tooling category before it, rewards disciplined use and punishes careless use. The teams producing memorable AI-assisted content are the ones holding the line on human ownership, voice, fact accuracy, and intellectual honesty. The teams producing AI slop are the ones treating AI as a content factory.

The discipline is not anti-AI; it is pro-craft. Craft was always what made content worth reading; AI does not change that, it just raises the cost of skipping it.

When in doubt about whether an AI-assisted workflow is ready, ask: is human ownership specified, are participation boundaries documented, is voice preservation built into the prompt and review patterns, is fact verification a halt-condition, is disclosure tiered to audience trust, is the team calibrated, and is the ethical floor explicit? If yes to all of those, the workflow is ready. If no to any, the gap is where the program will produce slop and lose reader trust.

