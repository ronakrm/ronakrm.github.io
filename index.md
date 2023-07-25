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
        <div style="padding: 10px 0 0 0">
            <ul class="contact-list">
                <li class="p-name">{{ site.author.name | escape }}</li>
                <li class="p-name">Machine Learning PhD</li>
                <li class="p-name">University of Wisconsin-Madison</li>
                <li><a class="u-email" href="mailto:{{ site.author.email }}">{{ site.author.email }}</a></li>
            </ul>
            I've completed my dissertation and am on the job market! Find me at at the typical monoliths:
            <ul class="social-media-list">
                <li class="p-name"><a class="social" href="https://www.linkedin.com/in/ronak-mehta-64627491/">LinkedIn</a></li>
                <li class="p-name"><a class="social" href="https://scholar.google.com/citations?user=7hv6xqkAAAAJ">Google Scholar</a></li>
                <li class="p-name"><a class="social" href="https://www.github.com/ronakrm/">GitHub</a></li>
            </ul>
        </div>
    </div>
</div>

<br/>

My dissertation research focused on methods for efficiently identifying important subsets of features, parameters, and samples
in modern ML settings. Current and future interests for me revolve around
applying some of these ideas to interpretability, and more broadly
exploring issues around alignment.

For a take-away, check out my [R&eacute;sum&eacute;/CV](/resume/Ronak_Mehta_CV.pdf).

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
