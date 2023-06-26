---
layout: post
title: "Incorporating Preferences is Easy if you Discretize"
categories: fairness, emd, safety
date: 2023-05-26
katex: True
---
<style>
body {
  font: 'warnock-pro', "Palatino", "Palatino Linotype", "Palatino LT STD", "Book Antiqua", Georgia, serif;
}
</style>


tl;dr: The classical Earth Mover's Distance can linearly incorporate any number of preferences, including new online/streaming preferences, and is completely differentiable with gradients provided during distance computation.

This post is in companion to work myself and collaborators presented at ICLR 2023, see LINK for more technical discussion.

## Bird's Eye View

Often our preferences don't take the form of a single point, but a distribution over some set of outcomes. Here we'll focus on the case where our preference takes the form of a univariate distribution over the real line, i.e., the typical assumptions that come with this picture:

![A Single Continuous Normal Distribution](/assets/blogfigs/single_cont_dist.svg){:.centered}

Sometimes we'll have some other preference, or distribution, along with our own:

![Two Continuous Normal Distributions](/assets/blogfigs/two_cont_dist.svg){:.centered}

If they are different, we might want to figure out HOW different, and even more so find some "middle ground" or some way to reconcile the difference, "pushing" the distributions to be similar.

{%- include_relative two_cont_dists_anim.svg -%}{:.centered}

![What's the distance between two distributions?](/assets/blogfigs/two_cont_dist_div.svg){:.centered}

If the distributions are nice like these, then we can easily compute continuous measures of "distance", such as KL divergence and others.
If it's possible to write out the distributions as functions of the domain,
we might try things like integrating over the difference of the functions.


## Down to Earth

However if these distributions are less nice,
then this problem can be intractable: we don't have any nice closed form representations that we can do algebra and easy calculus on to directly compute stuff.

![Real distributions are whacky!](/assets/blogfigs/two_cont_dist_whacky.svg){:.centered}

Also, we may have many distributions or preferences that we want to understand.

![Ahhh what do we do?](/assets/blogfigs/many_cont_dist_whacky.svg){:.centered}

Ok, so what can we do? Well turns out if we discretize, we can make some cool progress!

![Discretized distributions to the rescue!](/assets/blogfigs/many_discrete_dists.svg){:.centered}

In some settings this might even be more valuable. 
It could be hard for me to express a preference in a continuous space,
but I could say "I think this is probably negative with probability "<50%".

# With Two Distributions




# With More Distributions

Our ICLR paper focuses on this setting, and we show that everything above kind of extends very naturally and linearly(!) to more distributions.

The above procedure basically is simply modified to find the index of the distribution with the minimum value at any point as we move in axis-aligned steps from the "first" bin at $(0,0,\ldots,0)$ to $(d,d,\ldots,d)$.


## New preferences?

## Changing preferences?