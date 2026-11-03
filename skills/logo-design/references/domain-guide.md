# Domain methods

Read only the sections relevant to the current task; this guide does not require every method on every invocation.

- [The framework: 5 considerations for logo design](#the-framework-5-considerations-for-logo-design)
- [Failure patterns](#failure-patterns)

## The framework: 5 considerations for logo design

A logo decision sits at the intersection of five considerations. Each one filters subsequent choices.

### 1. Mark architecture

What IS the logo, structurally?

**Architectures:**

- **Wordmark only.** The logo is the brand name set in a chosen typeface, possibly with custom letterforms. Stripe, Google, Pinterest. The discipline is letter-by-letter, with kerning, optical adjustments, sometimes a single distinguishing custom character. Strongest when the name is distinctive enough to own as type.
- **Lockup (wordmark plus symbol).** Standard architecture for most brands. The wordmark and symbol are positioned in a fixed relationship. Slack, Airbnb, Asana. Variants: symbol left of wordmark, symbol above wordmark, symbol right (rare). Each lockup may also have a stacked alternate for square contexts.
- **Symbol only.** The mark is a single symbol with no wordmark. Apple, Twitter, Target. Earned over decades through brand recognition. New brands rarely succeed with symbol-only as the primary mark, though most mature brands eventually develop a symbol-only fallback.
- **Letterform-as-symbol.** A single letter from the name (often the first) becomes the symbol. Beats by Dre's "b", McDonald's "M", Underscore's "_". Cleanest path to symbol when the wordmark is too long for a tight lockup or when the name has a letter that lends itself to visual play.
- **Monogram.** Multiple letters combined as a symbol. CN (Chanel), GG (Gucci), HBO, MN (a hypothetical Morgan Northrop monogram for an institutional financial firm). Common in legal, financial, hospitality, and heritage brands. Can read as initials or as ligature.

**How to choose:** What does the brand need to do at small sizes? At 16px, most lockups fail. A favicon-grade mark needs either a strong symbol component or a letterform-as-symbol fallback. Lockups also need stacked alternates for square contexts (social profile pictures, app icons). A pure wordmark works only if the brand has another mark that can stand in at small sizes, often a letterform-as-symbol or monogram.

A common production setup is: primary lockup for most contexts, monogram for square contexts, letterform-as-symbol for favicon and embroidery. All three derive from the same wordmark and share visual DNA.

### 2. Typographic register

If wordmark or lockup, what typographic family carries the type?

**Registers:**

- **Geometric sans.** Futura, Avenir, Avenir Next, Cabinet Grotesk, ITC Avant Garde. Built from circles and verticals. Reads modern, considered, often optimistic. Risks reading cold or generic-tech-startup if not warmed up by color, custom letterform, or context.
- **Humanist sans.** Gill Sans, Optima, Frutiger, Source Sans, Inter at higher optical sizes. Has serif-like calligraphic gestures without serifs. Reads professional but warm. Excellent neutral choice when the category demands restraint with personality.
- **Neo-grotesque sans.** Helvetica, Inter, Aktiv Grotesk, Söhne, GT America. The modern professional default. Reads competent and contemporary. Risks reading generic if not paired with strong color or symbol.
- **Transitional serif.** Source Serif, Charter, Lyon, IBM Plex Serif. Modern serifs with high contrast and readability. Reads editorial, considered, intellectual. Good for legal, publishing, financial, editorial brands.
- **Old-style serif.** Garamond, Caslon, Sabon, Adobe Garamond. Classical serifs with low contrast and warm shapes. Reads heritage, traditional, institutional. Common in academic, legal, financial, and heritage brands.
- **Slab serif.** Sentinel, Adelle, Roboto Slab, Tisa. Heavy structural serifs. Reads strong, declarative, sometimes journalistic. Common in editorial and publishing.
- **Display custom.** A custom-drawn or heavily-modified typeface. Reads distinctive but expensive in time. Justified when the brand needs a wordmark no one else has and the budget supports drawing one.

**How to choose:** What does the brand reject? Most categories have a default register. Legal firms default to old-style or transitional serif. Tech startups default to geometric or neo-grotesque sans. Choosing within the category default reads as competence; choosing outside reads as positioning. A boutique legal firm in geometric sans signals "modern, accessible". A SaaS startup in old-style serif signals "we take ourselves seriously".

### 3. Symbol approach

If the architecture includes a symbol (lockup, symbol-only, letterform-as-symbol), what KIND of symbol?

**Approaches:**

- **Literal.** The symbol depicts the thing the brand name refers to. A mountain peak for an outdoor brand. A rocket for a rocket company. A leaf for a sustainable brand. Fast recognition, low ambiguity. Risks reading as cliche if the depiction is generic. Saved by distinctive execution: the specific peak, drawn with conviction, in the brand's specific visual register.
- **Abstract gesture.** The symbol suggests a quality without literal depiction. A rising arc for "growth". A pair of opposing forms for "balance". A continuous loop for "integrity". Slower recognition, higher distinctiveness. Risks reading as arbitrary if the gesture is too abstract. Saved by clear formal logic and consistent visual vocabulary.
- **Geometric reduction.** The symbol is a formal abstraction with no specific referent. A hexagon, a triangle, a stack of horizontal lines, a circle bisected by a vertical. Reads modern and confident. Risks reading as identical to many other geometric-reduction marks. Saved by specific proportions, considered execution, and pairing with a distinctive wordmark.
- **Letterform-derived.** The symbol is built from the name's letterforms. The "M" of McDonald's, the "b" of Beats, a custom "A" rendered as a mountain peak for a hypothetical Atlas Coffee. Strong wordmark-symbol coherence. Risks reading as wordmark-only if the letterform isn't emphasized enough. Saved by exaggerated character: the letter must read as both the letter AND the visual metaphor.
- **Monogram.** Multiple initials combined. The symbol IS the initials, often with ligature treatment, tight kerning, or geometric framing (ring, shield, diamond). Common in legal, financial, hospitality. Risks reading as old-fashioned if the type treatment is too conservative. Saved by modern execution within traditional architecture.

**How to choose:** What does the brand name already do? Descriptive names (Atlas, Forge, Pulse, Anchor) invite literal symbols and letterform-as-symbol approaches. Abstract names (Stripe, Anthropic, Linear) demand abstract or geometric-reduction symbols. Heritage names (a founder's surname, a place name) often use monograms. The wrong approach disconnects symbol from name.

### 4. Application context discipline

A logo is not a single drawing. It must work in every context the brand touches.

**Contexts and their constraints:**

- **16px favicon.** The most aggressive small-size test. Lockups usually fail here; the symbol or letterform-as-symbol carries. Plan a fallback mark for this context from the start.
- **28px app icon.** Slightly more headroom than favicon. Still demands strong silhouette. Often uses the symbol or monogram, not the lockup.
- **1.5 inch embroidery patch.** Limits color count (often 4 to 6 max), demands clean shapes without fine detail. Eliminates gradient and photographic elements. Tests the mark's reproducibility in a tactile medium.
- **Single-color reproduction.** Etching, foil stamp, single-color print, fax. All gradient and color-dependent decisions must collapse cleanly to one color. Test by converting the design to pure black on white.
- **Reverse (light on dark).** Many marks fail when reversed. Test on the brand's expected dark backgrounds early. Gradient marks particularly struggle here.
- **Large-format signage.** Requires sharp vector with no rasterization. Tests construction grid quality. Tests whether thin strokes survive scaling.
- **Motion lockup.** Tests whether the logo has natural entry and exit animation. Wordmarks reveal letter-by-letter; symbols rotate, scale, or assemble from parts.
- **Social profile picture (square).** Lockups need a stacked alternate or monogram fallback. Symbol-only works natively.
- **Apparel embroidery (thread on fabric).** Tighter constraints than patch embroidery. Fine letterforms and detail die here. The mark needs a chunky-friendly variant.
- **Foil stamp on paper or leather.** Single-color, no gradients, requires substantial line weight to survive the impression.

**The discipline:** Every variant must pass the application-context test before it's a contender. Generate each variant, then mentally test each context. If a variant fails three or more contexts, it's not a primary mark; it might still serve as a secondary or display lockup but it isn't carrying the brand. Build a fallback hierarchy: primary lockup, secondary monogram, favicon-grade letterform-as-symbol.

### 5. Restraint discipline

Most logo failure happens through over-design. The discipline is subtractive.

**Tests:**

- **Silhouette test.** Squint at the logo. If you cannot identify it from silhouette alone (with type stripped), the silhouette is too generic. Apple, Nike, Twitter pass. Most generic SaaS marks fail.
- **Distinctiveness test.** Search Google Images for "[your category] logo". If your candidate looks identical to three or more existing logos, it's not distinctive enough. Especially watch out for geometric-reduction marks that have already been done a thousand times.
- **Sketchability test.** A 7-year-old draws the logo from memory after 30 seconds of looking. If they can't, it's too detailed to live in cultural memory.
- **Single-color test.** Strip all color. Does it still read? If no, color is doing too much work.
- **Reproducibility test.** Print at 1 inch on a black-and-white printer. Is it still recognizable? If no, the mark won't survive embroidery, foil stamps, or low-resolution applications.
- **The two-second test.** Show the logo to someone unfamiliar with the brand for two seconds. Ask what they remember. The features they recall are the ones doing real work; the rest is noise.

The discipline doesn't reject all detail. It rejects detail that doesn't earn its place. Every visual element should pass the question "does this read at the smallest application size?".

---

## Failure patterns

- **Designing for the founder's taste, not the audience's perception.** The founder sees the logo every day; the audience sees it for 3 seconds in a bad mood. The audience-side test wins.
- **Skipping the silhouette test.** Logos that fail silhouette die at small sizes and in motion. Test early.
- **Ignoring small-size legibility.** A favicon test at 16px is the single most overlooked discipline. Most lockups fail here. Plan a fallback symbol or letterform-as-symbol mark from the start.
- **Trying to depict everything the brand does.** Logos can hold one idea, sometimes two. Three is too many. Symbols stuffed with multiple metaphors read as committee work.
- **Picking a typeface for trend.** Monoline geometric sans (Cabinet Grotesk, GT Pressura) read as "2024 startup" in a way that ages quickly. Pick for category-fit and longevity, not for design-trend currency.
- **Over-customizing letterforms.** Custom letterforms should solve a specific problem (a flat-bottomed "g" that conflicts with a descender, an "a" that breaks the rhythm, an "A" that becomes a mountain peak). Custom for novelty's sake reads as gimmicky.
- **Lockups that fall apart at certain sizes.** Test the lockup at 200%, 100%, 50%, 25%. If proportions break or elements clash at any size, the lockup needs adjustment.
- **Color-dependent marks.** A logo that requires color to be recognizable cannot survive single-color reproduction. Color is the last layer, not the foundation.
- **Letterform-as-symbol marks that fail the silhouette test for the underlying letter.** An "A as mountain peak" must read as a mountain peak AND as the letter A. If it reads as only one or only the other, the metaphor isn't earning its place.
- **Reviewing too many similar variants.** Showing a client 10 wordmark variants in different geometric sans typefaces dilutes the decision. Show 3 architectures, with 2 to 3 typographic options each. The client can see the architectural choice clearly.
- **Skipping the embroidery test.** Many brands eventually want a hat or a polo. A logo with fine detail or photographic gradients cannot be embroidered cleanly. Test before client signoff.

---

