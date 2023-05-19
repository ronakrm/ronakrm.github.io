---
layout: post
title: "How To Measure Stuff Sometimes"
categories: interpretability
date: 2023-04-01
katex: True
---

Epistemic Status: Haven't engaged enough with existing interpretability folks to know if this is common knowledge already, imposter syndrome, I just need to write/publish.


tl;dr: Sometimes you might actually want the distribution of a thing instead of whatever individual difference measure you're using.

I've noticed this in a few places now, where I'll be reading a paper,
or discussing how to evaluate a specific idea or intervention,
and I'll see or hear a specific measure being used or proposed.
And it will make me hesitate, and originally it was just
an inkling that something was wrong.
But I've figured out the issue!

### Quick Notation

Let's say we have a model $f$ that takes input $x$ and outputs estimate $\hat{y}$,
and we compute the correctness of the model against a true $y$ via a loss:
$$ l := (y - f(x))^2 $$
or some other distance $d(y, f(x))$ (cross entropy, etc.).
If we have some dataset $\mathcal{D} := \{x_i,y_i\}_{i=1}^n$,
then let 
$$\mathcal{L}_f := \sum_{(x_i,y_i)\in \mathcal{D}} \left(y_i-f(x_i)\right)^2$$

## What's the Question

We want to know if we do something to $f$, say $\tilde{f}$,
if it has done anything to the output we get at $\mathcal{L}$.
"Done anything" is super vague, and I think there's a lot to 
unpack there.

A thing we might compute to see if there's a change could be 
the difference of the (expected) loss:
$$ \mathcal{L}_f - \mathcal{L}_{\tilde{f}} $$
After all, we want to know if our change or operation
results in a _different_ output, right?

### On Direction

Let's say we have 2 "samples" in our "dataset",
and for our original model $f$ they result in losses
$$l_{f,1} = 0.4,\ l_{f,2} = -0.2,$$
and using a typical summation for aggregating the losses, $\mathcal{L}_f = 0.2$. 

Now we take some perturbed model $\hat{f}$, and it results in losses
$$l_{\hat{f},1} = -4,\ l_{\hat{f},2} = 4.2.$$
Using the aggregate above we'll clearly get the same value, and conclude that the perturbation did nothing!

Okay, obviously combining losses in this way is not the right thing to do. In classical statistics, this is related to Simpson's Paradox, where we have _correlated samples_. We need to account for the fact that each computed loss corresponds to the function taking a specific input: the samples are not interchangeable when comparing measures (stats: random effects). 

Great, so the next thing we do is break up the $\mathcal{L}$ differences by sample and instead look at the aggregate _differences_:
$$ \sum_{i} \left(l_{f,i} - l_{\hat{f},i} \right) $$

With this simple difference we still kind of have the same problem! The difference has simply been distributed, and the above example results in the same conclusion. Ok, but we never look at the simple difference right? We should use the absolute difference, or the squared difference.
$$ \sum_{i} \left(l_{f,i} - l_{\hat{f},i} \right)^2 $$

This solves all of the above problems! With only positive measures of "difference", the aggregation can't lead to cancellation, and any differences for each sample will be effectively accounted for in this final measure.

#### Can we write this as a function of the aggregate losses?
Let's try this using linearity of expectations. The expectation and sum are roughly interchangeable in this case, where our distribution is our entire dataset.
$$\begin{aligned}
\mathbb{E}_i\left[ \left(l_{f,i} - l_{\hat{f},i} \right)^2\right] &= \mathbb{E}_i \left[l_{f,i}^2 - 2l_{f,i}l_{\hat{f},i} + l_{\hat{f},i}^2 \right] \\
&= \mathbb{E}_i \left[l_{f,i}^2\right] - 2\mathbb{E}_i \left[l_{f,i}l_{\hat{f},i}\right] + \mathbb{E}_i \left[l_{\hat{f},i}^2 \right]
\end{aligned}$$
The expectation (or sum) in the middle term cannot be distributed because the sample $i$ is not independent for both losses. These are exactly those _correlated samples_ that we had to worry about when moving to squared difference!

## One Value is Not Enough
Ok so we've motivated, inuitively/empirically, why we might use something like squared difference to determine if a new model $\hat{f}$ has changed the output with respect to some reference model $f$.

But how do we interpret this measure? This will be some positive real number, but do we expect it to be zero? Are there small changes that would tell us that the intervention was loosely equal?

We need some sort of _reference_ to understand how we should interpret the number we get out.

Normalization is one way that is often used to obtain a reference:

$$ \frac{\mathcal{L}_f - \mathcal{L}_{\hat{f}}}{\mathcal{L}_f} $$

This gives us a scaled distance from the original loss in terms of a multiplicative factor. We still have an issue of understanding the scale: interpretation remains the same such that closer to 0 difference is good.

A term used in some of the art (ref: Causal Scrubbing) is the gain relative to the gain against, e.g. a random baseline.

$$ \frac{\mathcal{L}_{\hat{f}} - \mathcal{L}_b}{\mathcal{L}_f - \mathcal{L}_b} \times 100\% $$

As described therein,
> This percentage can exceed 100% or be negative. It is not very meaningful as a fraction, and is rather an arithmetic aid for comparing the magnitude of expected losses under various distributions. However, it is the case that hypotheses with a “% loss recovered” closer to 100% result in predictions that are more consistent with the model.

Extending the above random effects issue here helps with Simpson's like cancellation, but it is still one number, and how do we interpret a single number?

## Distributions

ref{CS} briefly mention that one could look at the full over the dataset, i.e., compare the distributions of the random variables $l_f(X)$ vs. $l_{\hat{f}}(X)$.
This would help us a bit as they mention, but conclude that it would require an explanation of the noise that may be compute-intensive.

I'd like to argue that distributions are _necessary_ in the case of interpretability here, and that framing a perturbation as an _alternative hypothesis_ is the right way to approach this.

# Interpretability via Hypothesis Testing

The main issue with our measures above were that we were getting a single value, and that was not effectively capturing everything that we were trying to capture as "explainable" or "not explainable". And in fact, with a real number we're really trying to answer "HOW explainable?" "How much is explained by X?"

My perspective is that much of interpretability and XAI research is circling around these questions because they aren't well posed. But if we harken back to ye olde classical science, we can get a lot more mileage.

In traditional sciences a question like those above is only the first step in the scientific method, and what typically follows is a _hypothesis test_. The defining of this test is critical in ensuring we have something that we can actually conclude from. The questions above as framed are not good hypotheses: they don't have definite outcomes, and they don't define a clear hypothesis space. If we only ask if $\hat{f}$ is similar to $f$, and we only look at a real number, then how do we decide what defines a range of values that we would use to conclude explainability?

Using the classical hypothesis testing framework, we could define a _null_ and _alternative_ hypothesis:
$$\begin{aligned}
H_0 &: f \quad \text{is equal to} &\hat{f} \\
H_A &: f \quad \text{is different from} &\hat{f} \\
\end{aligned}$$

Importantly, the null hypothesis is _rejected_ and we _accept_ the alternative if for whatever measure we choose, the measurement lies in the _rejection region_ of the space it's in. The classical constructions define this region by an $\alpha$-level hypothesis test, where the region defined by some level-set is determined based on our desire for a certain level of certainty in the conclusion.

The measures and rejection regions are importantly constructed so that, whenever we get our measurement to test, it is only possible for it to lie in either the null space or the alternative space. A well-formed hypothesis test only allows for these two possibilities, and as such there is no ambiguity.

### Silly Example

I have some magic number $z$ and I want to know if it is closer to 4 or 8. Let's define our measurement as observing $z$. A good hypothesis test might define our null and alternatives like so:
$$\begin{aligned}
H_0 &: z > 6  \\
H_A &: z \leq 6 \\
\end{aligned}$$
When we observe $z$, we can clearly determine which region of the hypothesis space it corresponds to and thus conclude where it is cloer to 4 or 8.

### Typical Testing
This type of construction works when you have very clearly defined measures and assumptions about what corresponds to different regions of your hypothesis space. In the real world, when we measure sample data from a population and want to determine if it similar or different to another group, i.e.,
$$\begin{aligned}
H_0 &: \bar{x}_1 \neq \bar{x}_2  \\
H_A &: \bar{x}_1 = \bar{x}_2,
\end{aligned}$$
we assume something about the distribution of this test statistic under the null, and see if what we measure is significantly different from that distribution.

The issues with the above and its instantations in sciences have been enumerated, and issues with selecting the rejection level, multiple hypothesis testing, p-hacking, etc. are all real problems. But we can use these ideas as a way to inform how we approach interpretability. (And there are Bayesian approaches that get around these)

## something here
Let's say we believe that a part of $f$ is doing some operation $g$. Our hypothesis is that if it is doing that function, we can replace that part with $g$ and the output of the model will not change.
Call the model with the replaced module $\hat{f}$. Then we want to test:
$$\begin{aligned}
H_0 &: \mathcal{L}_f \neq \mathcal{L}_{\hat{f}}  \\
H_A &: \mathcal{L}_f = \mathcal{L}_{\hat{f}}
\end{aligned}$$
As written this will run into the same issue above. We want our rejection region to be larger than exact equality, but we don't have any idea of how large it should be! Taking a classical statistics approach we might make (strong) assumptions about the distribution of these losses, but these might be extremely strict and not make sense.(?)

## Null Permutation Testing
A common strategy when the distribution is unknown is to estimate it via permuation testing. This involves drawing additional samples via shuffling, and the idea can be applied here.

What is the class of hypotheses we want to compare to? Let's say we want to know if this part of $f$ is doing $g$, or $g+\epsilon$, or any other function. Then we could 