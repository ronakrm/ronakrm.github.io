---
layout: home
permalink: /
---
<div class="row" style="display: flex">
    <div class="col-md-4 mr-auto" style="padding: 0px 25px; max-width: 400px">
        <img style="margin: 0 0px 0px 0px; max-height: 200px; max-width: 200px"
             src="RonakMehtaProfile.jpeg" />
    </div>
    <div class="col-md-4 ml-auto d-flex align-items-center">
        <div align="left">
            <ul class="contact-list">
                <li class="p-name">{{ site.author.name | escape }}</li>
                <li class="p-name">Machine Learning PhD</li>
                <li class="p-name">University of Wisconsin-Madison</li>
                <li><a class="u-email" href="mailto:{{ site.author.email }}">{{ site.author.email }}</a></li>
            </ul>
            I've completed my dissertation and am on the job market! Find me at at the typical monoliths:
            {% include social.html %}
        </div>
    </div>
</div>

<br/>

My dissertation research has focused on methods for efficiently identifying important subsets of features, parameters, and samples
in modern ML settings. Current and future interests for me revolve around
applying some of these ideas to interpretability, and more broadly
exploring issues around alignment.

For a take-away, check out my [R&eacute;sum&eacute;/CV](/resume/Ronak_Mehta_CV.pdf).

<div class="row">
    <div class="col col-md-8 ml-md-auto mr-md-auto">
        <h3>Recent News</h3>
        <div>
            <ul>
                {% for update in site.data.news %}
                <li>{{update}}</li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
