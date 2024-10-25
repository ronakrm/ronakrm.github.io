---
layout: post
title: "Interpretability by Design: Constraint Sets With Disjoint Limit Sets and Natural Subspaces"
excerpt: "How can we constrain our models to be interpretable? Convex linear sets make for more interpretable parameter spaces."
tags: math interpretability geometry analysis convexity probability
date: 2024-10-24
katex: True
---

__tl;dr__: {{ page.excerpt }}

An interpretation is something explicit, something discrete, something that compresses, something that summarizes. Our current paradigms do not lend themselves well to this.

# Unbounded Sets are Hard to Interpret

Let's say we have a parameter $\theta \in \mathbb{R}$. How do we interpret it?

![real_line_blank-1](https://hackmd.io/_uploads/HJwORCa1ye.png)

Well we can see what the value of the parameter is and see how far it is from some other number, like 0 or 1.

>> asdf

We can also see how it relates to some other parameter.

>> asdf

But we don't have any way to interpret it without adding additonal points, or by imposing a group or field to give us relevance to the identiy elements. Moreso, the _limits_ of the the parameter space are infinity, and interpretations for "big" numbers have no inherent meaning unless we create additional structure, or talk about _relative_ largeness.

If we remove the axis ticks, any region of the space looks the same as any other region of the space.

>> figure animation of moving along the real line removing axis ticks who knows where we are>

This is also true for real-valued vectors in $\mathbb{R}^n$. We can talk about the relative scale of different dimensions for a given vector, but the _limits_ of the actual values don't exist, and all regions look the same.

How can we define a parameter space that "looks different" somewhere? One way to think about this question is to think about the limits. With addition or multiplication, outside of the identity elements, any limiting behavior can only keep growing.

__Interpretation needs a limit.__


## Compact Sets are MUCH better

If we want limit points to be in our set we need it to be closed, and if we want to be able to reach or at least measure those limit points we need the set to be bounded. For subsets of $\mathbb{R}^n$, closed and bounded sets are compact.

Let's restrict ourselves to the obvious bounbded and closed single-dimensional set, $[0,1]$.

![interval-1](https://hackmd.io/_uploads/Byg01xZCk1x.png)

Now we have a compact set, with a subset $(0,1)$ that is homeomorphic to $\mathbb{R}$. If we needed some representation then we have not lost any "power", but we've also gained something: The limit points are in the set! _This is better._ We don't have a field anymore, but distance to limit points is now a measure, and by checking which limit point we are closer to, we can also _discretize_ to "limiting interpretations".

We have by-construction definitions of "signposts" that help tell us where we are, we don't need to impose them post-hoc. We can also find ways to build back up to a field and corresponding algebra, but let's leave that aside for now.

### Care in Higher Dimensions
Notice that in the univariate case of $[0,1]$ our limiting sets are singletons. Depending on how we define our compact set in higher dimensions, _this may not be the case, and it matters._

Let's do the obvious thing and use the Euclidean topology to create our compact set as the ball in $\mathbb{R}^d$,
the hypersphere plus its interior,

$$ B_d := \left\{ x \in \mathbb{R}^d\ \middle|\ \sqrt{\sum x_i^2} \leq 1 \right\} $$

<!-- ![sphere_axes](https://hackmd.io/_uploads/Byyc5hSgyl.png) -->


Our limiting points form the set of points defining the surface of the sphere. _This set is fully connected_. This could be good for some other reasons, but it _makes interpretation harder._ How do we distinguish between limit points? We again could arbitrarily, post-hoc, assign special values to the limit points at the axis-aligned points, but apriori there's no reason for these to be special.

(If we were to drop the axes, the mesh grid, and the lighting and shading in the above figure it would look like a solid dot _from every perspective_)

In my opinion, this is a large reason why current interpretability is difficult: practical instantiations of $l_2$ norm restrictions tend to have some random mix of "basis-preferring mechanisms". In ML, this often takes the form of uniform initialization, diagonalized initialization, diagonal Hessian approximations, independence, etc.

__Without additional structure, interpretations are then arbitrary, equally indistinguishable points that we now need to impose additional structure on.__


# Interpretations Are Disjoint Limit Sets

The most naturally interpretable spaces are compact sets with disjoint limit sets. There are still a bunch of sets here, which should we choose?

There are a bunch of properties we might want that can help reduce the set of possibilities. However we might not want to impose any more structure than necessary, to ensure we are still able to express a large number of different types of objects and functions.

__Convexity.__ We're probably going to want to search over or optimize over the set, and if its convex that helps a lot. There are many different convex sets, how might we choose among them? Keeping in mind that we'd like disjoint limit sets, what makes the most sense? If we have a limit set $A$ and a limit set $B$, then a convex set $C$ must be one where $$\alpha\cdot a + (1-\alpha)\cdot b \in C,\ \ \forall a \in A,\ b\in B,\ \alpha \in [0,1]$$ If the sets are just points or "corners", then this describes the line that connects those two points. A convex set must include this line. Interestingly, if we take an arbitrary set of points on a hypersphere and connect them via their convex hull, this is the _minimal_ convex set (by volume) that can include these points. This set can also be defined in the simplest way: linearly!

__Linearity__. Linear convex sets are defined by a series of intersecting halfspaces described by $Ax \leq b$. They are not only simple to represent but also significantly easier to optimize over. It's likely we'll need to restrict and project onto this set, or our procedures will depend on distance functions that should be easy to write down. Being able to define the set with linear constraints eases these steps.

__Regularity__. We could choose arbitrary points on the sphere and construct their convex hull, but apriori we might not really know why or how we should bias the distance between points. Can we create a regular, linear, convex set with disjoint limit sets?

Yes! There are many regular, convex polyhedra that satisfy these constraints. [Platonic Solids](https://en.wikipedia.org/wiki/Platonic_solid) are the set of these in 3-dimensional space. Which of these should we choose? if we truly want no bias among "corners", and want the "simplest" set, then there's only one choice, and it's a good one.

# The Simplex for Elments in $\mathbb{R}^d$

The standard simplex is defined as the set of positive real numbers that sum to 1,

$$\Delta_d :=\ \left\{x_i \in \mathbb{R}^d\ \middle|\ \sum x_i = 1\right\}.$$

The simplex has a TON of properties that ALL lend themselves to a more interpretable set.

__Natural, Axis-Aligned Bases.__ The bases where a single element is 1 and the rest are 0 explicitly define our "corners" and correspond directly to "interpretable" points of our set. These are points where all other dimensions are "off", and the only forward contribution comes from a single dimension. This also means that _every element in the simplex is a linear, convex combination of the basis elements_.

__Probabilistic Interpretations.__ The standard simplex is also known as the probability simplex. As you can likely see, having everything sum to 1 defines a categorical probability distribution over the dimensions.

__Subspaces and Hierarchical Intepretations.__ The subspace corresponding to a "face" of the simplex is exactly an $n-1$ dimensional simplex, and corresponds explicitly to the situation where one of the bases is 0. Interpretation here is naturally hierarchical in a linear, composable way.

__Interpretations are Encouraged.__ The simplex, by construction, pushes volume to lie on lower-dimensional subspaces. This can easily be seen by looking at the ratio of its surface are to volume:

For the n-dimensional simplex:

$$
\begin{align*}
\text{Surface Area} &= (n+1)\frac{1}{(n-1)!} \\
\text{Volume} &= \frac{1}{n!} \\
\text{Ratio} &= (n+1)n = n(n+1)
\end{align*}
$$

For the $L^2$ ball (hypersphere):

$$
\begin{align*}
\text{Surface Area} &= \frac{2\pi^{n/2}}{(n/2-1)!} \\
\text{Volume} &= \frac{\pi^{n/2}}{(n/2)!} \\
\text{Ratio} &= 2n
\end{align*}
$$

And for the $L^1$ ball:

$$
\begin{align*}
\text{Surface Area} &= 2n\frac{2^{n-1}}{(n-1)!}\\
\text{Volume} &= \frac{2^n}{n!} \\
\text{Ratio} &= 2n
\end{align*}
$$

The ratio grows quadratically compared to the linear growth of alternative and typical constraint sets. While generally we are concerned with the curse of dimensionality, in this case it _aids us in biasing toward simpler and thus more interpretable solutions._

## Simplex Computations are Easy
To map from real numbers to the simplex, there are two options for our map $\sigma:\mathbb{R}^d \rightarrow \Delta^d$. The closest point can be computed using: $$p_{i}=\max\{x_{i}+\delta ,\ 0\}$$ where $\delta$ satisfies $\sum_i \max\{ x_i + \delta , 0 \} = 1$. This can be computed by sorting $x_i$ in $O(n\log n)$ time.

Alternatively, we can use the softmax function:

$$ p_i = \frac{e^{x_i}}{\sum_i e^{x_i}} $$

which we can compute in linear time. The softmax also has another extremely valuable property: we can add a _temperature_ which can control how much we bias toward corners of the simplex!



# A Langrangian Perspective

- We're constantly shaping and writing new objectives and optimizers
- These can be seen as duals to constraint sets
- When regularizers like $l_2$, $l_1$, fairness measures, and second-order optimizers are used, these have dual formulations that correspond to restricting the unregularized objective to a particular constraint set
	- We're already doing constrained optimization implicitly, especially when we try to make more interpretable models this way!
	- __Let's be explicit about it.__

# In Practice
