---
layout: post
title: "GPT-2 Sometimes Fails at IOI"
excerpt: "For certain people, GPT-2 does not perform IOI."
tags: interpretability safety viz math
date: 2024-08-07
katex: True
---

__tl;dr__: {{ page.excerpt }}

_Code for this post can be found at [https://github.com/ronakrm/ioi-enumerate](https://github.com/ronakrm/ioi-enumerate)._

Following the _trend_ of _recent_ _work_,
I did a deeper dive into the IOI results and just
ran it on all possible inputs that fit the original BABA
template and PLACE/OBJECT tokens.
This results in 9 million strings, and instead 
of just looking at the mean logit diff, let's look at the distribution.

FIGURE OF FULL HISTOGRAMS FOR SMALL/MEDIUM/LARGE HERE

These look pretty decent, but there's obviously some mass below zero!
For what percent of the 9 million inputs does GPT-2 incorrectly predict
the Subject instead of the Indirect Object as the higher logit?

TABLE OF SIZE, COUNT, PERCENTAGE

This isn't a lot, but from chatting with people at MATS it seems like 
there may have been a prevailing belief that IOI definitely always works:
but not if your Subject is XXXX:

We can identify these subsets that fail programmatically by looking
at the conditional means and finding the ones that are furthest from
either the global mean or the mean when that condition is removed
(check out the notebook in the repo above).

If we slice again by the Indirect Object being YYYY,


we can see that the model fails _every time_ to correctly complete the IOI task.

### This occurs for the larger models as well, BUT...?
plots for medium, large



## Conclusion
That's all I wanted to point out. I'm becoming more interested
generally in bounding worst-case behaviors as a safety angle.
This is a toy setup where the worst-case is not being handled correctly.
If your name is XXXX or YYYY you may feel this more concretely,
let alone if your name is uncommon, non-Western, or multi-token.
As we worry more and more about extreme tail-risk failure modes,
it's a good idea to keep things like this in mind, and perhaps
ideas in fairness and more mainstream machine learning and 
algorithmic fairness may be good "model organisms" for demonstrating
and studying these failure modes.  

I think it's good to worry about these kinds of issues as we attempt
to scale interpretability approaches to large models, and I'm
glad that new approaches for ensuring the robustness and faithfulness 
of interpretability are becoming more common!
