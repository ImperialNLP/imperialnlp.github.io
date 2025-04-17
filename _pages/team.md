---
layout: page
permalink: /team.html
title: team
page-title: Team
description: NLP Group at Imperial College London Computing Department.
nav: true
nav_order: 2
nav_rank: 2
---

{% assign groups = site.members | sort: "group_rank" | map: "group" | uniq %}
{% for group in groups %}
## {{ group }}

{% assign members = site.members | sort: "group_order" | sort: "lastname" | where: "group", group %}
    {% for member in members %}
<p>
    <div class="card {% if member.inline == false %}hoverable{% endif %}">
        <div class="row no-gutters">
            <div class="col-sm-4 col-md-3">
                <img src="{{ '/assets/img/team/' | append: member.profile.image | relative_url }}" class="card-img img-fluid" alt="{{ member.profile.name }}" />
            </div>
            <div class="team col-sm-8 col-md-9">
                <div class="card-body">
                    {% if member.inline == false %}{% if member.external == true %} <a href="{{ member.profile.website }}">
                    {% else %}
                    <a href="{{ member.url | relative_url }}">
                    <!-- <a href="{{ member.profile.website }}"> -->
                    {% endif %}{% endif %}
                    <h5 class="card-title">{{ member.profile.name }}</h5>
                    {% if member.profile.position %}
                    {% if member.profile.team-position %}<h6 class="card-subtitle mb-2 text-muted">{{ member.profile.team-position }}</h6>
                    {% else %}<h6 class="card-subtitle mb-2 text-muted">{{ member.profile.position }}</h6>{% endif %}{% endif %}
                    <p class="card-text">
                        {{ member.teaser }}
                    </p>
                    {% if member.inline == false %}</a>{% endif %}
                    {% if member.profile.email %}
                        <a href="mailto:{{ member.profile.email }}" class="card-link"><i class="fas fa-envelope"></i></a>
                    {% endif %}
                    {% if member.profile.phone %}
                        <a href="tel:{{ member.profile.phone }}" class="card-link"><i class="fas fa-phone"></i></a>
                    {% endif %}
                    {% if member.profile.orcid %}
                        <a href="https://orcid.org/{{ member.profile.orcid }}" class="card-link" target="_blank"><i class="fab fa-orcid"></i></a>
                    {% endif %}
                    {% if member.profile.twitter %}
                        <a href="https://twitter.com/{{ member.profile.twitter }}" class="card-link" target="_blank"><i class="fab fa-twitter"></i></a>
                    {% endif %}
                   {% if member.profile.linkedin %}
                        <a href="https://linkedin.com/{{ member.profile.linkedin }}" class="card-link" target="_blank"><i class="fab fa-linkedin"></i></a>
                    {% endif %}
                    {% if member.profile.github %}
                        <a href="https://github.com/{{ member.profile.github }}" class="card-link" target="_blank"><i class="fab fa-github"></i></a>
                    {% endif %}&nbsp; &nbsp;
                    {%- if member.profile.scholar -%}
                        <a href="https://scholar.google.com/citations?user={{ page.profile.scholar }}" title="Google Scholar"><i class="ai ai-google-scholar"></i></a>
                    {% endif %} &nbsp;
                    {% if member.profile.website %}
                        <a href="{{ member.profile.website }}" class="card-link" target="_blank"><i class="fas fa-globe"></i></a>
                    {% endif %}
                    <br /><br />
                    {% if member.profile.supervisor %}
                    <p class="card-text">
                        <small class="test-muted"><i class="far fa-address-card"></i> Supervisor: {{ member.profile.supervisor | replace: '<br />', ', ' }}</small>
                    </p>
                    {% endif %}
                    <p class="card-text">
                        <small class="test-muted"><i class="fa-solid fa-location-dot"></i> {{ member.profile.address | replace: '<br />', ', ' }}</small>
                    </p>
                </div>
            </div>
        </div>
    </div>
</p>
    {% endfor %}
{% endfor %}

