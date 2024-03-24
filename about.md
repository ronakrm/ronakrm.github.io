---
layout: page
title: About
permalink: /about/
---

I was a CS PhD at UW-Madison, where I worked with [Dr. Vikas Singh](https://biostat.wisc.edu/~vsingh) on machine learning and computer vision projects, some in collaboration with the [Wisconsin Alzheimer's Disease Research Center](https://adrc.wisc.edu) to develop methods for analyzing preclinical datasets.

I completed my undergraduate degree in Computer Engineering at the University of Michigan-Ann Arbor in 2014, and my master's degree in Computer Science at UW-Madison in 2016.

### Contact

Feel free to contact me via email, or at my few social media presences:
<ul class="contact-list">
    {% if site.author.name %}
        <li class="p-name">{{ site.author.name | escape }}</li>
    {% endif %}
    {% if site.author.email %}
        <li><a class="u-email" href="mailto:{{ site.author.email }}">{{ site.author.email }}</a></li>
        {%- endif %}
</ul>
{% include social.html %}

### Website

This webpage was primarily built using
[jekyll](jekyll-organization) /
[minima](https://github.com/jekyll/minima),
and was generally inspired by [https://varunagrawal.github.io/](https://varunagrawal.github.io/).
Source here: [https://github.com/ronakrm/ronakrm.github.io](https://github.com/ronakrm/ronakrm.github.io).
LaTeX provided by [KaTeX](https://katex.org/).

I aspire to eventually create posts at this level, but for now it's
probably more important to just publish...
[Echo Chess: The Quest for Solvability.](https://samiramly.com/chess)