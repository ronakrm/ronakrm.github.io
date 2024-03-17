---
layout: post
title: "How To Measure Stuff Sometimes"
excerpt: Sometimes you might actually want the distribution of a thing instead of whatever individual difference measure you're using.
tags: interpretability math
date: 2024-03-09
modified_date: 2024-03-09
katex: True
---


[//]: # _Epistemic Status_: Haven't engaged enough with existing interpretability folks to know if this is common knowledge already, imposter syndrome, I just need to write/publish.


_tl;dr_: {{ page.excerpt }}

### Todos
- reference causal
- reference ACDC, others
- reference MIRI stuff
- state its just some thoughts, not a full thing
- maybe everyone knows this already

# A More Persuasive Version As a Research Proposal

## Abstract

Mechanistic interpretability research currently approaches the problem
from a machine learning perspective:
with tools for black-box
explainability in hand, how can we "open-up" the box and understand
what is going on under the hood?
From an alternative perspective,
I argue that white-box interpretability of machine learning models
is directly analogous to the classical scientific study of real world phenomena.
Questions such as 
"What is this mechanism doing?",
"How well does this mechanism sufficiently explain the outcome?",
"Is this mechanism similar to another?", and
"Does this mechanism have multiple functions?"
can all be asked both of the real world and of machine learning models.
As such,
interpretability of neural network models
can not only be seen through the lens of machine learning,
but also through the lens of _science_.

# A Blog-y Version with Very Light Math

### Quick Notation

Let's say we have a model $f$ that takes input $x$ and outputs estimate $\hat{y}$,
and we compute the correctness of the model against a true $y$ via some loss:

$$l := \left(y - f(x)\right)^2 $$

or some other distance $d(y, f(x))$ (cross entropy, etc.).
If we have some dataset $\cD:= \\{x_i,y_i\\}_{i=1}^n$,
then let

$$\cL(f,\cD) := \sum_{\cD} l_i := \sum_{(x_i,y_i)\in \cD} \left(y_i-f(x_i)\right)^2 $$

## What's the Question

We want to know if we do something to $f$, say $\tf$,
if it has done anything to the output we get at $\cL$.
"Done anything" is super vague, and I think there's a lot to 
unpack there.

A thing we might compute to see if there's a change could be 
the difference of the (expected) loss:

$$ \cL(f,\cD) - \cL(\tf,\cD) $$

After all, we want to know if our change or operation
results in a _different_ output, right?

### On Direction

Let's say we have 2 "samples" in our "dataset",
and for our original model $f$ they result in losses

$$ l(f,1) = 0.4,\ l(f,2) = -0.2, $$

and using a typical summation for aggregating the losses, $$\cL(f,\cD)  = 0.2$$. 

Now we take some perturbed model $\tf$, and it results in losses

$$ l(\tf,1) = -4,\ l(\tf,2) = 4.2. $$

Using the aggregate above we'll clearly get the same value, and conclude that the change in model did nothing!

Okay, obviously combining losses in this way is not the right thing to do. In classical statistics, this is related to Simpson's Paradox, where we have _correlated samples_. We need to account for the fact that each computed loss corresponds to the function taking a specific input: the samples are not interchangeable when comparing measures (stats: random effects). 

Great, so the next thing we do is break up the $\cL$ differences by sample and instead look at the aggregate _differences_:

$$ \sum_{i} \left(l(f,i) - l(\tf,i) \right) $$

With this simple difference we still kind of have the same problem! The difference has simply been distributed, and the above example results in the same conclusion. Ok, but we never look at the simple difference right? We should use the absolute difference, or sometimes equivalently, the squared difference.

$$ \sum_{i} \left(l(f,i) - l(\tf,i) \right)^2 $$

This solves all of the above problems! With only positive measures of "difference", the aggregation can't lead to cancellation, and any differences for each sample will be effectively accounted for in this final measure.

#### Can we write this as a function of the aggregate losses?
Let's try this using linearity of expectations. The expectation and sum are roughly interchangeable in this case, where our distribution is over our entire dataset $i\in \cD$.

$$\begin{aligned}
\EE_i\left[ \left(l(f,i) - l(\tf,i) \right)^2\right] &= \EE_i \left[l(f,i)^2 - 2l(f,i)l(\tf,i) + l(\tf,i)^2 \right] \\
&= \EE_i \left[l(f,i)^2\right] - 2\EE_i \left[l(f,i)l(\tf,i)\right] + \EE_i \left[l(\tf,i)^2 \right]
\end{aligned}$$

The expectation (or sum) in the middle term cannot be distributed because the sample $i$ is not independent for both losses. These are exactly those _correlated samples_ that we had to worry about when moving to squared difference!

## One Value is Not Enough
Ok so we've motivated, inuitively/empirically, why we might use something like squared difference to determine if a new model $\tf$ has changed the output with respect to some reference model $f$.

But how do we interpret this measure? This will be some positive real number, but do we expect it to be zero? Are there small changes that would tell us that the intervention was loosely equal?

We need some sort of __reference__ to understand how we should interpret the number we get out.

Normalization is one way that is often used to obtain a reference:

$$ \frac{\cL(f,\cD) - \cL(\tf,\cD)}{\cL(f,\cD)} $$

This gives us a scaled distance from the original loss in terms of a multiplicative factor. We still have an issue of understanding the scale: interpretation has not moved further than our original statement of "closer to 0 means less difference."

A term I've seen used in some places is the gain relative to the gain against a random baseline.

$$ \frac{\cL(\tf) - \cL(b)}{\cL(f) - \cL(b)} \times 100\% $$

As described in Causal Scrubbing (ref{CS}):,
> This percentage can exceed 100% or be negative. It is not very meaningful as a fraction, and is rather an arithmetic aid for comparing the magnitude of expected losses under various distributions. However, it is the case that hypotheses with a “% loss recovered” closer to 100% result in predictions that are more consistent with the model.

There are probably variations of this scheme which can be used to deal with these issues,
and we can again extend the random effects idea above to help with
Simpson's like cancellation,
but it is still one number, and how do we interpret a single number?

## Distributions

ref{CS} briefly mention that one could look at these measures over the full dataset, i.e., compare the distributions of the random variables $l(f,\cD)$ vs. $l(\tf,\cD)$.
This would help us a bit as they mention, but conclude that it would require an explanation of the noise that may be compute-intensive.

I'll argue that distributions are _necessary_ in the case of interpretability here. Framing a perturbation as an _alternative hypothesis_ is the right way to approach this,
and there are computationally feasible ways to do it.


# Scalable Interpretability via Hypothesis Testing

The main issue with with a single value is that it does not effectively capturing everything that we were wrapping as "explainable" or "not explainable".
And in fact, with a real number we're really trying to answer "HOW explainable?" "How much is explained by X?"
My perspective is that much of interpretability and XAI research is circling around these questions because they aren't well posed. But if we harken back to ye olde classical science, we can get a lot more mileage.

## Hypothesis Spaces and Testing
A hypothesis is a claim
that we believe might explain some
world phenomena.
Consider these two hypotheses,
one about the real world and one about an arbitrary 
neural network transformer model:

$$
\begin{aligned}
    H &:\qquad \text{Apples have a lot of Vitamin C.} \\ % \label{hyp:world} \\
    H &:\qquad \text{The 1.5 and 2.4 attention heads are important for induction.} %\label{hyp:ml}
\end{aligned}
$$

As written, 
these both have a number of practical problems.
How much is "a lot"? How do we define "important"?
How do we measure Vitamin C? How do we measure "important"?
If we have multiple measures, which should we choose?
An arbitrary test of these hypotheses
as stated would be hard to 
implement, evaluate, and trust.

A good hypothesis is a _falsifiable_ one.
Any claim may have 
some evidence supporting it (its likelihood may be nonzero),
but without testing alternative claims
to establish a baseline likelihood,
the validity of the claim will 
be difficult to trust,
or may not generalize well
to explain future events.

For this reason,
classical hypothesis testing 
requires rigorous definitions
of a full experiment,
including the measure of interest and
not only the hypothesis,
but also the __space of hypotheses.__

After a measure is chosen to 
evaluate the hypothesis of interest (e.g., a test statistic),
it is evaluated and compared to
all other hypotheses within that space:
how likely is it to explain the 
evidence compared to other hypotheses within its class?
In the real world example above,
what is the space of relative hypotheses?
All other fruits? All other foods?
Anything for which we can measure Vitamin C?
This choice explicitly defines
how we can judge "a lot".
This is extremely important:
different choices can completely
reverse our conclusion to the original vague claim.
Apples may have "a lot" of Vitamin C
compared to other foods,
but may not have "a lot" more compared
to other fruits.
Similarly for our transformer,
are we comparing to a another specific path?
Paths with one head from each layer?
All possible head subsets?

These questions lead to the classical
hypothesis testing construction where
a __null hypothesis__ must be defined
as a different element or region of the hypothesis space
compared to the claim we wish to test.
If we want to compare to oranges,
then we need a measure that works for oranges, and we need to measure them.
If we want to compare to all fruits,
then we need something that works for all fruits.
If we want to compare to all other
paths through the network,
we need our measure to work for all of those paths,
and we need some way to measure them.

$$
\begin{aligned}
    H_A &:\qquad \text{Apples have \textbf{more} Vitamin C compared to other fruits.} \\ %  \label{hyp:worldA} \\
    H_0 &:\qquad \text{Apples have the \textbf{same amount or less} Vitamin C compared to other fruits.} \\ % \label{hyp:world0} \\
    & & \\ % \nonumber\\
    H_A &:\qquad \text{The path through attention heads 1.5 and 2.4 is \textbf{more important}} \\ % \nonumber\\
        & \quad\qquad \text{for induction compared to any other path.} \\ % \label{hyp:mlA} \\
    H_0 &:\qquad \text{The path through attention heads 1.5 and 2.4 is \textbf{equally or less important}} \\ % \nonumber\\
        & \quad\qquad \text{for induction compared to any other path.} % \label{hyp:mlo}
\end{aligned}
$$

Concretely we are now determining if our hypothesis
is more likely compared to another.
Importantly, these hypotheses represent \textit{the entire set of possible outcomes}. If we had a measure, there would be no ambiguity of which hypothesis it supports. Mose classical hypothesis testing gives us this for free by requiring that nulls and alternatives explicitly define _regions of the outcome or measure space_ which correspond to those hypotheses, and even describe testing frameworks that ensure the entire space of outcomes is formed by the disjoint union of the two.

From a probabilistic or Bayesian perspective,
we're comparing the likelihood of observing
these phenomena among possible "worlds."
Bayes factors and credible intervals can be used
in place of $p$-values and confidence intervals.

Unique for the case of machine learning models is that the entire "world"
is explicitly defined, and we
can actually compute
population-level statistics, i.e.,
all possible activations,
for all possible inputs.
Obviously
computational complexity
may limit or restrict
full testing in practice,
and as such using such hypothesis
testing frameworks allow us to fall
back on sample-based statistical testing.
%What does this look like in interpretability?

### Practical Testing

How do we test a hypothesis?
In the real world case,
we cannot know for certain
that all apples have more Vitamin C
compared to all fruits,
but we can collect samples of both
and use a measure on those
as an _estimate_ of the population
measure.
We can go collect apples and other fruits
directly from our world,
and compute some measure that gets at
the "amount" of Vitamin C.
We can "select"
paths through our transformer
and compute some measure that
gets at the "importance for induction"
of that path.

These selection procedures are _part of the test definition_.
If we want to say something about the population mean via a sample mean, it is expected that
the sample is _representative_ in some form: the individual samples collected are independently and identically distributed.
Clearly in the neural network setting, this may not be the case:
paths through the network that overlap significantly would obviously have correlated values.


What does this measure look like?
There may 
be multiple ways to measure Vitamin C,
and the choice of measure
may imply different assumptions
about the world.
This could include the actual method of measurement, 
like when the end of titration is decided,
to what statistical aggregation and parameters were used, such as sample size, type of mean, etc.
The details of the measure chosen 
are also part of
the hypothesis test definition.

If we just "squeezed" the fruits
until they stopped dripping,
it's easy to see that this assumes
something about where the Vitamin C is, or at least that this process retrieves the same amount of it across differing fruits.
In the same way, 
we should make sure that the metric we choose
for evaluating importance encodes
the assumptions it actually does.


__Evaluating Measures.__ 
In the classical case,
we typically have an interest
in the population _mean_,
taking advantage
of efficient properties
that allow testing against closed form _null distributions._
Just because the observed difference
in means is large, does not mean
that the population difference may be large as well.
The null distribution
encodes our prior belief about
how the difference would be distributed
if there were no differences between the true
population means $\mu$, with appropriate adjustments based on the size of our sample.

$$
\begin{aligned}
    H_A &:\qquad C_{apples} > C_{others} &H_A &:\qquad \mu_{apples} > \mu_{others} &H_A &:\qquad \bar{x}_{apples} > \bar{x}_{others} \\
    %& %\qquad\qquad\qquad\qquad\qquad\quad \Rightarrow & & \qquad\qquad\qquad\qquad\qquad\quad \Rightarrow & & \nonumber\\
    H_0 &:\qquad C_{apples} \leq C_{others} &H_0 &:\qquad \mu_{apples} \leq \mu_{others} &H_0 &:\qquad \bar{x}_{apples} \leq \bar{x}_{others} %\\
\end{aligned}
$$

In this simple situation the distribution of the difference of the means
is well studied and can be tested directly. The expected distribution of this statistic is known and easily computable: a commonly used tool in a statistician's toolbox.

__Unknown distributions.__ What if we are interested in something other than the mean?
Perhaps some random function over the fruits,
or a new ``interpretability measure" over transformer
subnetworks.
We may not know how that measure is distributed,
or any other properties that may help define
a null distribution. What can we do?

__Permutation testing__
provides a method for estimating the null distribution
using samples provided to us.
By shuffling our labeling, in this case "apples" and "others",
we can estimate the null distribution of
the difference: if there was no difference between 
the groups, then permuting the "labels" should have no effect.
This can analogously be applied to neural network
subgraph hypotheses: if we can "sample"
other parts of the network through a resampling
of our input data,
we can estimate the distribution of the _null_ effect,
and get an idea of how _relatively_ likely 
a particular hypothesis is.

These measures can become quite complex, and need not only be obvious functions of simple sample means.
An interpretation of the statement "important for" can be seen 
as "dependent on", suggesting
either direct causality
or a less strong _conditional dependence._
Practical measures that 
extend correlation metrics
exist for independence
and conditional independence.
TODO


In traditional sciences a question like those above is only the first step in the scientific method, and what typically follows is a __hypothesis test__. The defining of this test is critical in ensuring we have something that we can actually make conclusions from. The questions above as framed are not good hypotheses: they don't have definite outcomes, and they don't define a clear hypothesis space. If we only ask if $\tf$ is similar to $f$, and we only look at a real number, then how do we decide what defines a range of values that we would use to conclude explainability?

Using the classical hypothesis testing framework, we could define a __null__ and __alternative__ hypothesis:

$$
\begin{aligned}
H_0 &: f \quad \text{is equal to} &\tf \\
H_A &: f \quad \text{is different from} &\tf \\
\end{aligned}
$$

Importantly, the null hypothesis is __rejected__ and we __accept__ the alternative if for whatever measure we choose, the measurement lies in the __rejection region__ of the space it's in. The classical constructions define this region by an $\alpha$-level hypothesis test, where the region defined by some level-set is based on our desire for a certain level of certainty in the conclusion.

The measures and rejection regions are importantly constructed so that, whenever we get our measurement to test, it is only possible for it to lie in either the null space or the alternative space. A well-formed hypothesis test only allows for these two possibilities, and as such there is no ambiguity.

### Silly Example

I have some magic number $z$ and I want to know if it is closer to 4 or 8. Let's define our measurement as observing $z$. A good hypothesis test might define our null and alternatives like so:

$$
\begin{aligned}
H_0 &: z > 6  \\
H_A &: z \leq 6 \\
\end{aligned}
$$

When we observe $z$, we can clearly determine which region of the hypothesis space it corresponds to and thus conclude where it is cloer to 4 or 8.

### Typical Testing
This type of construction works when you have very clearly defined measures and assumptions about what corresponds to different regions of your hypothesis space. In the real world, when we measure sample data from a population and want to determine if it similar or different to another group, i.e.,

$$
\begin{aligned}
H_0 &: \bar{x}_1 \neq \bar{x}_2  \\
H_A &: \bar{x}_1 = \bar{x}_2,
\end{aligned}
$$

we assume something about the distribution of this test statistic under the null, and see if what we measure is significantly different from that distribution.

The issues with the above and its instantations in sciences have been enumerated, and issues with selecting the rejection level, multiple hypothesis testing, p-hacking, etc. are all real problems. But we can use these ideas as a way to inform how we approach interpretability,
and take advantage of our distinct and unique model setting, as well as more topical Bayesian approaches, to get around these.

## For Interpretability
Let's say we believe that a part of some model or function $f$ is doing some operation $g$. Our hypothesis is that if it is doing that function, we can replace that part with $g$ and the output of the model will not change.
Call the model with the replaced module $\tf$. Then we want to test:

$$
\begin{aligned}
H_0 &: \cL(f) \neq \cL(\tf)  \\
H_A &: \cL(f) = \cL(\tf)
\end{aligned}
$$

As written this will run into the same issue above. We want our rejection region to be larger than exact equality, but we don't have any idea of how large it should be! Taking a classical statistics approach we might make assumptions about the distribution of these losses, but these might be extremely strict and may not even be reasonable given true unknown distributions of these measures.
But we can again borrow from classical statistics approach to address this problem.

## Null Permutation Testing
A common strategy when the distribution is unknown is to estimate it via permuation testing. This involves drawing additional samples in the class to bootstrap the estimation of the null.

What is the class of hypotheses we want to compare to? Let's say we want to know if $A$ part of $f$ is doing $g$, or $g+\epsilon$, or any other function. At a first glance,
we might first consider other possible functions as alternative hypotheses. If it's not doing $g$, then it must be doing $\neg g$, or maybe $\sin{\cdot}$, or $g^2$, or $rand(\cdot)$, or anything else. So we could choose a class of functions, check if it is performing any of those, and perhaps using some measure of "performing" (e.g., the measures above) decide if it is more likely to be $g$ or something other than $g$. We might observe this measure distributed as some univariate distribution:

![Null_Dist](/assets/blogfigs/null_dist.png){:.centered}

And see that the measure at $g$ is significantly larger than others.
_However_, it is possible that not just this part $A$ of $f$ is performing this function, and even that other parts of $f$ ($B, A^\prime, \ldots$) are performing it better!
With a different perspective (null hypothesis space), we might observe and conclude something comletely different:

![Other_Null_Dist](/assets/blogfigs/null_dist_other.png){:.centered}

__We have to decide what the hypothesis space looks like.__
Do we want to know if this part of the model is performing a particular function better than any other function?
Do we want to know if this part of the model is performing a particular function better than any other part of the model?
Do we want to know if this part of the model is performing a particular function better than any other part of the model on a particular subset of the data?

Choosing this question determines the hypothesis spaces, the types of samples we would draw, and the measures we would use to compare them. All of these form the definition of our hypothesis test.

### __Our Situation is Even Better__
In the real world we can never hope to draw enough samples to estimate complex, multi-dimensional distributions. Costs of sample collection and computation can become exhorbitant, e.g., computing summary statistics over functional MRI sequences. But in our machine learning, neural network case we are only limited by our compute, and our compute only consists of possible paths through the model!

In fact, _if we wanted_, we could __enumerate all possible hypotheses__. Of course in practice we would never do this and the compute cost can easily become obsene, but it does suggest that we do not have to worry about permutation costs in the same way that classical science does.
We are not limited by ethical concerns of additional animal testing, or prohibitive costs associated with high-fidelity data collection or expert time.

Even moreso, this type of testing is fully and embarassingly parallel! Anyone with a specific hypothesis about a particular part of a network
can test it, and that particular result, even if it turns out to be nothing, can be used as a sample for someone else's null distribution if it is relevant to their hypothesis.
We don't even have to be careful about defining the hypothesis spaces at the start,
because we don't have to worry about double-dipping, or p-hacking, or using too much of sample. 
We can collect any number of samples of the form "replace subset of model with my guess $g$ and measure loss",
and later define our hypothesis space to determine if a particular guess of a particular model subset is performing a particular function.
A new subset can be tested, a new function could be replaced, and we can continuously 
compare subsequent measures against our growing null distribution.

In this framing, failures are still extremely valuable, as they increase the confidence we have that successes are _true_ successes.

An ideal endpoint that I can foresee if this were to all work out is a distributed hypothesis testing setup, where individual researchers testing particular models for particular functions contribute their results to build out the "global null". Slowly, we would build up a picture of what parts of what models are doing what, and how well they are doing it.
We may begin to observe and characterize typical distributions that are common in certain types of tasks, models, archiectures, etc.
These distributions would allow us to make large-sample inferences akin to the way in which null distributions are used in 
classical science hypothesis testing.