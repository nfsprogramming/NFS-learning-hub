---
title: Exercise Instructions
permalink: index.html
layout: home
---

# GitHub Copilot Exercises

The following quickstart exercises are designed to provide you with a hands-on learning experience in which you'll explore the capabilities of GitHub Copilot. Each exercise includes a set of tasks that you can complete in your lab environment.

## Quickstart exercises
<hr>

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions/Labs'" %}

{% for activity in labs  %}

### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})
{{ activity.lab.description }}
<hr>
{% endfor %}
