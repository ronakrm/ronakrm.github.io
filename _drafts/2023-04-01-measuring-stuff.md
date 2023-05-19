---
layout: post
title: "How To Measure Stuff Sometimes"
categories: interpretability
date: 2023-04-01
katex: True
---

_Epistemic Status_: Haven't engaged enough with existing interpretability folks to know if this is common knowledge already, imposter syndrome, I just need to write/publish.


_tl;dr_: Sometimes you might actually want the distribution of a thing instead of whatever individual difference measure you're using.

I've noticed this in a few places now, where I'll be reading a paper,
or discussing how to evaluate a specific idea or intervention,
and I'll see or hear a specific measure being used or proposed.
And it will make me hesitate, and originally it was just
an inkling that something was wrong.
But I've figured out the issue!

### Quick Notation

Let's say we have a model $$f$$ that takes input $$x$$ and outputs estimate $$\hat{y}$$,
and we compute the correctness of the model against a true $y$ via $$\mathcal{L}$$:

$$ l := y - f(x) $$

or some other distance $$d(y, f(x))$$ (cross entropy, etc.).
If we have some dataset $$\mathcal{D} := \{x_i,y_i\}_{i=1}^n$$,
then let 

$$\mathcal{L}_f := \sum_{(x_i,y_i)\in \mathcal{D}} (y_i-f(x_i))$$

### What's the Question

We want to know if we do something to $$f$$, say $$\tilde{f}$$,
if it has done anything to the output we get at $$\mathcal{L}$$.
"Done anything" is super vague, and I think there's a lot to 
unpack there.

A thing we might compute to see if there's a change could be 
the difference of the (expected) loss:
$$ \mathcal{L}_f - \mathcal{L}_{\tilde{f}} $$
After all, we want to know if our change or operation
results in a _different_ output, right?

#### Counterexample

Let's say we have 2 "samples" in our "dataset",
and for our original model $f$ they result in
$$l_1 = 0.4, l_2 = -0.2$$.