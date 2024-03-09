---
layout: page
title: Research
permalink: /research/
---
## Conference and Journal Publications
Google Scholar: [Ronak Mehta](https://scholar.google.com/citations?user=7hv6xqkAAAAJ)

If you're interested in a particular paper, that's not easily available,
 feel free to reach out to me for a copy.

<div class="col-10 ml-auto mr-auto">
    <ul class="conference-papers">
        {% for paper in site.data.research.pubs %}
        <li class="paper">
            <div class="paper-title">{{paper.title}}</div>
            {% for author in paper.authors %}
            {%- if author contains "Ronak Mehta" -%}
            <b class="my-name">{{ author -}}</b>
            {%- else -%}
            {{ author -}}
            {%- endif -%}
            {%- unless forloop.last %}, {% endunless -%}
            {% endfor %}
            <br />
            <i>{{paper.venue}}</i>
            <br />
            {% for link in paper.links %}
            {% if link %}
            <a href="{{link[1]}}"><u>{{link[0]}}</u></a>
            {% if forloop.last == false %}
            |
            {% endif %}
            {% endif %}
            {% endfor %}
        </li>
        <br />
        {% endfor %}
    </ul>
</div>