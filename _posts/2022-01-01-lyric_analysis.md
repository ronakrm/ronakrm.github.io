---
layout: post
title: "Less Muse and Thicker Plots"
excerpt: Some old but very pretty and satisfying visualizations for a pointless analysis. (JS, JQuery, HighCharts)
tags: misc viz js
date: 2022-01-01
modified_date: 2024-04-14
js: True
---

__tl;dr__: {{ page.excerpt }}

At some point I really enjoyed Muse, and then less so. Earlier, before
semantic-everything, I wanted to see if I could correlate it with a hypothesis:
the lyrics were getting more vague about "you" and "me" and "us". Plus
I wanted an excuse to learn some basic data processing/visualization for web.

Using the Genius API, got the lyrics. Processed them with these filters:
```python
firstPString = '\\b(I|me|my|mine|myself|we|us|our|ours|ourselves)\\b'
secondPString = '\\b(you|your|yours|yourself|yourselves)\\b'
thirdPString = '\\b(they|them|their|themselves)\\b'
```

And plot using highcharts (mouseover/click around!).

<figure class="highcharts-figure">
    <div id="scatter-container" style="height:400px"></div>
</figure>
Generally it looks like the variance in word count and pronount count increases
with newer albums. How about a different visualization, with the pronoun count ratio?

<figure class="highcharts-figure">
    <div id="ratio-container" style="height:400px"></div>
</figure>
Hmm, looks like the lyrics are wordier, but I can't generally see a correlation
with songs I enjoy and if they're more concise or less concrete.

## If I Come Back to This

Maybe I'll update this with my ratings of each song and see if any of these
features correlate! For now I made some pretty plots.

Happy to share the Python scripts if you want to do something related, feel free to reach out. I should put them somewhere, but it's small enough that I don't think it warrants it's own repo, but maybe fleshing out this blog post with code snippets? Hmm...

<script src="/script/js/scatter.js"></script>
<script src="/script/js/ratio.js"></script>