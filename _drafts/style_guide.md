# Writing Style Guide — Ronak Mehta

Distilled from existing published posts. This is a living document; update as style evolves.

## Voice and Tone

**Conversational but technically precise.** Don't dumb things down, don't lecture. Write like you're explaining something to a smart friend at a whiteboard.

> This post is a rough exploration of one direction that seems worth exploring, motivated by some rough set theory and geometry. I tried to keep it short, and there's an appendix with a bunch of other related ideas and followups.

**First person, informal asides are welcome.** Humor, personality, and honest reactions are features, not bugs.

> *Was this TikZ animation worth the time? Probably not, but it was fun.*

> I'm a little sad that much of safety research has fully pivoted to post-hoc explanations of frontier Shoggoths. I think there's probably low hanging fruit to grow an easier to understand Shoggoth, even if it's not with a simplex :).

**Honest about uncertainty.** Say when things are rough, exploratory, or when you don't know. Don't oversell.

> There may be ways to solve these problems or the cost could be worth it, but figuring this out will require more work.

> I could potentially see some value in actually doing enumeration on small models, e.g., GPT-2. To get better handles on methods and measures. Results here could be used to inform sampling required for larger models, or even to narrow hypothesis selection for larger models.

**Opinionated when warranted.** Take positions and state them clearly, but ground opinions in reasoning, not authority.

> I think distributions are _necessary_ for proper interpretability.

> In my opinion, this is a large reason why current interpretability is difficult: practical instantiations of $l_2$ norm restrictions tend to have some random mix of "basis-preferring mechanisms".


## Structure Patterns

### Openings

Start with a **summary hook** before the main content. Formats used:
- `__cart;horse__:` — framing the core question/tension, short summary of the main point
- Explicit audience statement

Examples:

> __cart;horse__: How can we constrain our models to be interpretable? Convex, linear sets make for more interpretable parameter spaces, and the simplex and the Birkhoff Polytope are great examples of this that have other desirable properties.

> __cart;horse__: Nice figures and animations, mostly. Continuous settings can be hard, but matching and moving arbitrary distributions is easier if you discretize.

> Audience: You know some ML math basics, like how losses are typically computed. You are interested in how hypothesis testing can be used to interpret machine learning models, or are confused as to why some particular result you read about isn't convincing you as much as you hoped.

### Body

**Math-forward.** Lead with formal definitions and build intuition around them. Don't build intuition first and then formalize — the formalism IS the intuition.

> The standard simplex is defined as the set of positive real numbers that sum to 1,
> $$\Delta^n :=\ \left\{x_i \in \mathbb{R}^n\ \middle\vert\ \sum x_i = 1\right\}.$$
> The simplex has a TON of properties that lend themselves to a more interpretable set.

**Rhetorical anchoring with bold text.** Use bold phrases as quasi-section-headers or thesis statements within sections:

> __Interpretation needs a limit.__

> __Any region of the space looks the same as any other region of the space.__

> __Convexity.__ We're probably going to want to search over or optimize over the set, and if its convex that helps a lot.

> __We have to decide the hypothesis space that corresponds to our specific interpretability question.__

**Build arguments incrementally.** Start with the simplest case, show why it's insufficient, motivate the next step. The "but wait, that's not enough" rhythm:

> This is also true for real-valued vectors in $\mathbb{R}^n$. We can talk about the relative scale of different dimensions for a given vector, but the limits of the actual values don't exist, and all regions look the same.
>
> How can we define a parameter space that "looks different" somewhere? One way to think about this question is to think about the limits.

> We still have the same problem! The difference has only been distributed, and the above example results in the same conclusion. Ok, but we never look at the simple difference right? We should use the absolute difference, or sometimes equivalently, the squared difference. [...] This solves it.

**Use concrete analogies** to ground abstract points:

> If we just "squeezed" the fruits until they stopped dripping, it's easy to see that this assumes something about where the Vitamin C is, or at least that this process retrieves the same amount of it across differing fruits. In the same way, we should make sure that the metric we choose for evaluating importance for interpretability encodes the assumptions we are actually making about the model.

### Closings

**Open-ended, not conclusive.** End with open questions, future directions, invitations to collaborate. Don't restate what was already said.

> If anyone would like to chat about these ideas please reach out! I don't think there are many market incentives to work on this; it's likely most ideas in alternative architectures will fail and are not worth the R&D that could be used to stay at the frontier.

> _Something_ is better than nothing, and I think this is a __pretty good something__.

> If you're interested in these questions, or have some of your own, feel free to reach out!


## Formatting Conventions

- **KaTeX math:** `$...$` for inline, `$$...$$` for display. Custom macros like `\cL`, `\cD`, `\EE` are fine.
- **Bold for emphasis and anchoring:** `__text__` style. Used both for emphasis and as quasi-section-headers within paragraphs.
- **Italic for softer emphasis or terms:** `_text_` or `*text*`.
- **Figures (production phase):** `![Alt text](/assets/blogfigs/...){:.centered width="400px"}` with italicized caption below, centered.
- **Footnotes:** `[^n]` style, collected at bottom. For tangential but interesting details, not citations.
- **Blockquotes:** Sparingly, for quoting others' work directly.
- **Admonition boxes:** `<div class="admon">` for key takeaways or important distinctions.
- **Links:** Standard markdown. Papers (arXiv, OpenReview), LessWrong posts, Wikipedia for definitions.
- **Code blocks:** Rarely used, only for citations/bibtex. These are idea posts, not code posts.

## Content Characteristics

- **Topics:** AI safety, interpretability, mathematical ML, fairness, optimization geometry. The connecting thread: how mathematical structure can make ML systems more understandable and controllable.
- **Audience:** Technical readers who know ML basics. LessWrong/AF posts assume familiarity with that community but don't rely on jargon.
- **Length:** Medium to long. Posts develop ideas fully rather than being hot takes. But don't pad.
- **Visual reasoning:** Geometric intuition is a core explanatory tool. If something can be drawn, draw it.

## What NOT to Do

- Don't write in a corporate/marketing tone. No "In this blog post, we will explore..."
- Don't add unnecessary caveats or hedging on every sentence. Be direct.
- Don't summarize the post structure at the beginning ("First we'll cover X, then Y") — let the TOC handle that if needed.
- Don't use bullet-point-heavy formats for the main argument. Prose paragraphs carry ideas better.
- Don't add conclusions that just restate what was already said. If there's nothing new to add at the end, just stop.
- Don't strip out personality. The asides, the humor, the honest frustration — these make the writing distinctive.
- Don't over-polish or make everything grammatically pristine. Some roughness is intentional — it reads like someone thinking, not someone presenting.
