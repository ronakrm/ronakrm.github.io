---
layout: post
title: "Scratch/Progress on Site Building"
excerpt: Scratch post for site imports, styling, etc. Skippable unless you're interested in the site's construction.
tags: misc
date: 2023-03-25
modified_date: 2024-03-24
katex: True
---

This is mostly a place where I tested out various features of the site, such as LaTeX, images, and other formatting.
If you have any questions about the site, feel free to reach out to me via email or social media,
or check out the [source code](https://github.com/ronakrm/ronakrm.github.io) on GitHub.

### Basic Posting/Text

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### $\LaTeX$

Here's a LaTeX Test: $$ \phi $$. In the line below, the expectation symbol is a macro defined in a separate latex sty file.

$$ \EE_{x}[p(x)] \text{some words} \frac{2}{4} $$

~~Unfortunately I was not able to easily load LaTeX/KaTeX via local files
and GitHub Pages, so posts with LaTeX require/get the KaTeX css/js
from jsdeliver/cloudfare.~~

__EDIT:__ Got it to work! Definitely make sure you're only trying to make it work ONE way at a time. I had attempted loading the katex kramdown gem alongside loading the CDN files, and/or loading local and CDN at the same time. Obviously there will be issues if you do this...

## Go!

Basics all set, time to stop procrastinating and actually write!


### Some Figures
Mainly for reference in other places on the net.

![Null_Dist](/assets/blogfigs/null_dist.png){:.centered}
![Other_Null_Dist](/assets/blogfigs/null_dist_other.png){:.centered}


# Learning Notes

I tried to do some fancy SVG animations, but GitHub Pages doesn't support them;
appears to be related to security concerns. 