---
layout: blog
title: Blog
permalink: /blog/
---

Random thoughts, some cool ideas,
some cool ways to communicate or think about ideas,
some more math-y/machine learning stuff.
If you have ways in which these can be improved
for clarity or accessibility please let me know!
I reserve the right to edit and update these at any point in the future.
<!-- :[things can move fast](/_drafts/for-me/things-that-used-to-matter.md).-->
Maybe I'll add some cute GitHub last commit link and preview for each post.

<h2 class="post-list-heading">Math-y, More Formal Posts</h2>
<!-- <p>More technical stuff about math, machine learning, ways of thinking about complex topics, etc.</p> -->
<ul class="post-list">
{%- for post in site.tags.math -%} 
    <li>
    <h2 style="margin-bottom: 5px;"><a class="post-link" href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    {%- if site.show_excerpts -%} {{ post.excerpt }} {%- endif -%}  
    </li>
{%- endfor -%}
</ul>

<h2 class="post-list-heading">Misc-y, Personal-y Posts</h2>
<!-- <p>Some less formal stuff, maybe there's some math here but it's probably just some multiplying to get feels for stuff.</p> -->
<ul class="post-list">
{%- for post in site.tags.misc -%} 
    <li>
    <h2 style="margin-bottom: 5px;"><a class="post-link" href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    {%- if site.show_excerpts -%} {{ post.excerpt }} {%- endif -%}  
    </li>
{%- endfor -%}
</ul>

