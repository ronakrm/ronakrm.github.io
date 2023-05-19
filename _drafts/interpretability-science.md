---
layout: post
title: "Treating Interpretability as a Science"
categories: interpretability
date: 2023-05-01
---

Epistemic Status: Haven't engaged enough with existing interpretability folks to know if this is common knowledge already, imposter syndrome, I just need to write/publish.

TL;DR: you care about the distribution of the thing, and you can probably estimate (or completely characterize) it!

## Summary/Abstract/Thesis
Methods for interpretability currently approach the problem
from a machine learning perspective:
with tools for black-box
explainability in hand, how can we "open-up" the box and understand
what is going on under the hood?
From an alternative perspective,
I argue that white-box interpretability of machine learning models
is directly analogous to classical scientific study of the real world.
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

## Motivation/Background