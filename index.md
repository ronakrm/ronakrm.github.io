---
layout: home
permalink: /
---
<div class="row" style="justify-content: center; display: flex; flex-wrap: wrap">
    <div class="one-half" style="justify-content: center; display:flex">
        <img style="margin: 0 0px 0 0px; max-height: 200px; max-width: 200px"
             src="RonakMehtaProfile_small.jpeg" />
    </div>
    <div class="one-half" style="justify-content: center; display:flex">
        <div style="padding: 10px 0 0 0; margin-top: 10px">
            <ul class="contact-list">
                <li class="p-name">{{ site.author.name | escape }}, ML/CS PhD</li>
                <!-- <li><a class="u-email" href="mailto:{{ site.author.email }}">{{ site.author.email }}</a></li> -->
                <li class="p-name">ronakrm [at] the big G's mail</li>
            </ul>
            Find me at at the typical monoliths:
            <ul class="social-media-list">
                <li class="p-name"><a class="social" href="https://www.linkedin.com/in/ronak-mehta-64627491/">LinkedIn</a></li>
                <li class="p-name"><a class="social" href="https://scholar.google.com/citations?user=7hv6xqkAAAAJ">Google Scholar</a></li>
                <li class="p-name"><a class="social" href="https://www.github.com/ronakrm/">GitHub</a></li>
            </ul>
        </div>
    </div>
</div>

<br/>

My dissertation research focused on methods for efficiently identifying important subsets of features, parameters, and samples in modern ML settings.
I've worked on some assorted alignment research projects, and more recently a startup for research automation.

I occasionally write some <a href="/blog/">blog posts</a>, technical and otherwise. Future ones will also be on <a href="https://ronakrm.substack.com">my substack</a>, if you prefer that.

<div class="row">
    <div class="col col-md-8 ml-md-auto mr-md-auto">
        <h1>Latest Posts</h1>
        {%- assign num_posts = 1 -%}
        {%- for post in site.posts limit: num_posts -%}
            <h3 style="margin-bottom: 5px;">
                <a class="post-link" href="{{ post.url | relative_url }}">{{ post.title }}</a>
            </h3>
            <p class="post-meta" style="margin-bottom: 10px;">{{ post.date | date: "%b %-d, %Y" }}</p>
            <p>{{ post.excerpt | strip_html }}</p>
        {%- endfor -%}
    </div>
</div>

<!--
<div class="row">
    <div class="col col-md-8 ml-md-auto mr-md-auto">
        <h2>Recent News</h2>
        <div>
            <ul>
                {% for update in site.data.news %}
                <li>{{update}}</li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
-->
