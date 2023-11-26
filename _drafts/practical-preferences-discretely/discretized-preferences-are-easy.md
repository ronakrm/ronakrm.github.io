---
layout: post
title: "Incorporating Preferences is Easy if you Discretize"
tags: fairness emd safety
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

If they are different, we might want to figure out HOW different, and even more so find some "middle ground" or some way to reconcile the difference, "pushing" the distributions to be similar. (mouseover/tap)


{%- include_relative two_cont_dists_anim_copy.svg -%}{:.centered}
<br/>

We could try to measure this difference with some _distance_ measure, $d(A,B)$
If the distributions are nice like these, then we can easily compute continuous measures of distance, such as KL divergence and others.
If it's possible to write out the distributions as functions of the domain,
we might try things like integrating over the difference of the functions.

<!-- ![What's the distance between two distributions?](/assets/blogfigs/two_cont_dist_div.svg){:.centered} -->

## Down to Earth

However if these distributions are less nice,
then this problem can be intractable: we don't have any nice closed form representations that we can do algebra and easy calculus on to directly compute stuff.

![Real distributions are whacky!](/assets/blogfigs/two_cont_dist_whacky.svg){:.centered}

Also, we may have many distributions or preferences that we want to understand.

![Ahhh what do we do?](/assets/blogfigs/many_cont_dist_whacky.svg){:.centered}

Ok, so what can we do? Well turns out if we discretize, we can make some cool progress!

![Discretized distributions to the rescue!](/assets/blogfigs/many_discrete_dists.svg){:.centered}

In some settings this might even be more valuable than working in the continuous space. 
It could be hard for me to express a preference or measure continuously,
but I could say "I think this outcome or set of outcomes is possible with probability "50%",
corresponding to some discrete uniform mass over a discrete area of input space.

An important part of this is that it's not really _discrete_, it's __discretized__.
We are applying a different topology over the input space.
If it were fully discrete, the cost to move from one end to another would be the same as moving
just one "bin" over.

# With Two Distributions

One way to talk about this mathematically is using the Monge cost definition. 
Without too much detail, moving further away should entail a higher "cost".
If we want to move one distribution to match another,
the cost should naturally be higher if it is "further away".

Let's take a simple cost, like just counting the number of "bins" away something is.
If one distribution was all in the first bin, and we wanted to "move" or "match"
it to another that was all in the last bin,
we would have to move all of the "mass" over by the number of bins.
This gives rise to classical Earth Mover's Distance.

![Delta functions at the end, shifting over](){:.centered}

A cool mathematical result that comes out of this
is that we can make a single pass over any arbitrary distribution
to figure out the cost to make it match another!
This ends up being something like a difference match with a carry:
at each bin we figure out how much stays and how much moves,
and we keep track of how much we have left over.
This local operation ends up giving us a global solution.

Another byproduct of this is that the solution we get
ends up being a joint distribution, with the _marginal distributions_
equal to the two original distributions!

![asdf](/assets/blogfigs/animtest_5.gif){:.centered}


# With More Distributions

Our ICLR paper focuses on this setting, and we show that everything above kind of extends very naturally and linearly(!) to more distributions.

The above procedure basically is simply modified to find the index of the distribution with the minimum value at any point as we move in axis-aligned steps from the "first" bin at $(0,0,\ldots,0)$ to $(d,d,\ldots,d)$.

![amazing](/assets/blogfigs/first_fixed_50.gif){:.centered}

## New preferences?

## Changing preferences?



## Theoretical Properties

### Convergence to barycenters
### convergence to continuous


---
layout: post
title: "A Neat Way to Address Calibration"
tags: fairness emd safety calibration
date: 2023-05-26
katex: True
---
<style>
body {
  font: 'warnock-pro', "Palatino", "Palatino Linotype", "Palatino LT STD", "Book Antiqua", Georgia, serif;
}
</style>


tl;dr: 


# Calibration

Moving deeper past typical measures of performance like accuracy,
we've come to a point where we now care not only when we are correct or not,
but also on being _confident_ in our correctness.
This is the idea of being __well-calibrated__: the frequentist, measurable
frequency that we are incorrect should reflect our confidence in those particular responses.
For example, if we filter our predictions based on those that we believe
are 90% correct, when we actually check the true labels or outcomes,
we should _actually be_ 90% correct.

This idea has a lot of practical benefits, including being highly correlated with
overfitting and generalization, as well as ...(cite here)...
As expected with the large amount of ML research happening,
there are many different ways people have come at this problem.
(refs/cite) (other openreview ICLR paper)

While not particularly groundbreaking, calibration 
is a great application for our recent-ish ICLR work on
Earth Mover's Distance, especially when you may have many different
distributions you want to calibrate concurrently, and when
you do the practical thing of comparing to a discrete calibration
(e.g., calibrate to bin counts vs. a continuous measure)

## The Simple Case

The easiest application is to just take the Earth Mover's Distance
between our current predictions and the goal, and use some
derivative of this as signal to help push the model during training
towards a ``calibrated" outcome.

(figure with A and B)



# Multiple Calibrations

## freeze the target

## support set