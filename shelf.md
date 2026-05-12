---
layout: page
title: Shelf
permalink: /shelf/
---

Recent things I've been reading, plus the stuff I'd recommend as support vectors to my current thoughts!

<!-- Filter controls -->
<div id="shelf-controls">
  <div class="shelf-filters">
    <div class="shelf-filter-group">
      <label>Type</label>
      <div class="shelf-btn-group" data-filter="type">
        <button class="shelf-btn active" data-value="all">All</button>
        <button class="shelf-btn" data-value="book">Book</button>
        <button class="shelf-btn" data-value="post">Post</button>
        <button class="shelf-btn" data-value="paper">Paper</button>
        <button class="shelf-btn" data-value="podcast">Podcast</button>
      </div>
    </div>
  </div>
  <div class="shelf-search-sort">
    <div class="shelf-search">
      <input type="text" id="shelf-search" placeholder="Search title, author, tags...">
    </div>
    <div class="shelf-sort">
      <label>Sort by</label>
      <select id="shelf-sort">
        <option value="date_added-desc">Date added (newest)</option>
        <option value="date_added-asc">Date added (oldest)</option>
        <option value="rating-desc">Rating (high to low)</option>
        <option value="rating-asc">Rating (low to high)</option>
        <option value="title-asc">Title (A-Z)</option>
        <option value="title-desc">Title (Z-A)</option>
      </select>
    </div>
  </div>
</div>

<!-- Recommended -->
{% assign starred_items = site.data.shelf | where: "starred", true | where: "visible", true %}
{% if starred_items.size > 0 %}
<h2 class="shelf-section-heading">Recommended</h2>
<div class="shelf-starred">
  {% for item in starred_items %}
  <div class="shelf-card starred"
       data-type="{{ item.type }}"
       data-status="{{ item.status }}"
       data-rating="{{ item.rating }}"
       data-date="{{ item.date_added }}"
       data-search="{{ item.title | downcase }} {{ item.author | downcase }} {{ item.tags | join: ' ' | downcase }}">
    <div class="shelf-card-body">
      <div class="shelf-card-main">
        <div class="shelf-card-title">{% if item.link %}<a href="{{ item.link }}">{{ item.title }}</a>{% else %}{{ item.title }}{% endif %} <span class="shelf-type-badge">{{ item.type }}</span></div>
        {% if item.author and item.author != "" %}<div class="shelf-card-author">{{ item.author }}</div>{% endif %}
        <div class="shelf-card-detail">{% if item.rating %}<span class="shelf-card-rating">{% for i in (1..5) %}{% if i <= item.rating %}&#9733;{% else %}&#9734;{% endif %}{% endfor %}</span> {% endif %}{% if item.comments and item.comments != "" %}<span class="shelf-card-comments">{{ item.comments }}</span>{% endif %}</div>
      </div>
      <div class="shelf-card-aside">
        {% if item.tags and item.tags.size > 0 %}
        <div class="shelf-card-tags">{% for tag in item.tags %}<span class="shelf-tag">{{ tag }}</span>{% endfor %}</div>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>
{% endif %}

<!-- In the Queue (in-progress + up-next) -->
{% assign in_progress = site.data.shelf | where: "visible", true | where: "status", "in-progress" %}
{% assign up_next = site.data.shelf | where: "visible", true | where: "status", "up-next" %}
{% assign queue_items = in_progress | concat: up_next %}
{% if queue_items.size > 0 %}
<h2 class="shelf-section-heading">In the Queue</h2>
<div class="shelf-queue" id="shelf-queue">
  {% for item in queue_items %}
  <div class="shelf-card queue{% if forloop.index > 5 %} shelf-queue-hidden{% endif %}"
       data-type="{{ item.type }}"
       data-status="{{ item.status }}"
       data-rating="{{ item.rating }}"
       data-date="{{ item.date_added }}"
       data-search="{{ item.title | downcase }} {{ item.author | downcase }} {{ item.tags | join: ' ' | downcase }}">
    <div class="shelf-card-body">
      <div class="shelf-card-main">
        <div class="shelf-card-title">{% if item.link %}<a href="{{ item.link }}">{{ item.title }}</a>{% else %}{{ item.title }}{% endif %} <span class="shelf-type-badge">{{ item.type }}</span> <span class="shelf-status-badge shelf-status-{{ item.status }}">{{ item.status }}</span></div>
        {% if item.author and item.author != "" %}<div class="shelf-card-author">{{ item.author }}</div>{% endif %}
        {% if item.comments and item.comments != "" %}<div class="shelf-card-detail"><span class="shelf-card-comments">{{ item.comments }}</span></div>{% endif %}
      </div>
      <div class="shelf-card-aside">
        {% if item.tags and item.tags.size > 0 %}
        <div class="shelf-card-tags">{% for tag in item.tags %}<span class="shelf-tag">{{ tag }}</span>{% endfor %}</div>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>
{% if queue_items.size > 5 %}
<button class="shelf-btn shelf-show-more" id="shelf-queue-toggle">Show all ({{ queue_items.size }})</button>
{% endif %}
{% endif %}

<!-- Full Table -->
<details class="shelf-everything">
<summary><h2 class="shelf-section-heading">Everything</h2></summary>
<div class="shelf-table-wrap">
<table class="shelf-table">
  <thead>
    <tr>
      <th>Title</th>
      <th>Author</th>
      <th>Type</th>
      <th>Rating</th>
      <th>Status</th>
      <th>Comments</th>
    </tr>
  </thead>
  <tbody>
    {% for item in site.data.shelf %}
    {% if item.visible %}
    <tr class="shelf-table-row"
        data-type="{{ item.type }}"
        data-status="{{ item.status }}"
        data-rating="{{ item.rating }}"
        data-date="{{ item.date_added }}"
        data-search="{{ item.title | downcase }} {{ item.author | downcase }} {{ item.tags | join: ' ' | downcase }} {{ item.comments | downcase }}">
      <td>{% if item.link %}<a href="{{ item.link }}">{{ item.title }}</a>{% else %}{{ item.title }}{% endif %}</td>
      <td>{{ item.author }}</td>
      <td><span class="shelf-type-badge">{{ item.type }}</span></td>
      <td class="shelf-rating-cell">
        {% if item.rating %}
        {% for i in (1..5) %}{% if i <= item.rating %}&#9733;{% else %}&#9734;{% endif %}{% endfor %}
        {% endif %}
      </td>
      <td><span class="shelf-status-badge shelf-status-{{ item.status }}">{{ item.status }}</span></td>
      <td class="shelf-comments-cell">{{ item.comments }}</td>
    </tr>
    {% endif %}
    {% endfor %}
  </tbody>
</table>
</div>
</details>

<!-- Entertainment -->
<!--
<h2 class="shelf-section-heading">Entertainment</h2>

Some shows, films, and games I've enjoyed or have thoughts about. Less structured than the above.
-->

<script>
(function() {
  // Queue show more/less toggle
  var queueToggle = document.getElementById('shelf-queue-toggle');
  if (queueToggle) {
    queueToggle.addEventListener('click', function() {
      var hidden = document.querySelectorAll('.shelf-queue-hidden');
      var expanded = queueToggle.getAttribute('data-expanded') === 'true';
      hidden.forEach(function(el) { el.style.display = expanded ? 'none' : ''; });
      queueToggle.setAttribute('data-expanded', expanded ? 'false' : 'true');
      queueToggle.textContent = expanded ? queueToggle.textContent.replace('Show less', 'Show all') : queueToggle.textContent.replace('Show all', 'Show less');
    });
  }

  // Filter buttons (multi-select: click toggles, "All" resets)
  document.querySelectorAll('.shelf-btn-group').forEach(function(group) {
    group.addEventListener('click', function(e) {
      if (!e.target.classList.contains('shelf-btn')) return;
      var allBtn = group.querySelector('[data-value="all"]');
      if (e.target.getAttribute('data-value') === 'all') {
        // Clicking "All" clears everything and activates All
        group.querySelectorAll('.shelf-btn').forEach(function(b) { b.classList.remove('active'); });
        allBtn.classList.add('active');
      } else {
        // Toggle this button
        e.target.classList.toggle('active');
        allBtn.classList.remove('active');
        // If nothing is selected, re-activate All
        var anyActive = group.querySelectorAll('.shelf-btn.active');
        if (anyActive.length === 0) allBtn.classList.add('active');
      }
      applyFilters();
    });
  });

  // Search
  document.getElementById('shelf-search').addEventListener('input', applyFilters);

  // Sort
  document.getElementById('shelf-sort').addEventListener('change', applySort);

  function getActiveFilters() {
    var filters = {};
    document.querySelectorAll('.shelf-btn-group').forEach(function(group) {
      var key = group.getAttribute('data-filter');
      var active = Array.from(group.querySelectorAll('.shelf-btn.active'));
      var values = active.map(function(b) { return b.getAttribute('data-value'); });
      filters[key] = values.indexOf('all') !== -1 ? null : values;
    });
    filters.search = document.getElementById('shelf-search').value.toLowerCase();
    return filters;
  }

  function applyFilters() {
    var filters = getActiveFilters();
    var items = document.querySelectorAll('[data-type]');
    items.forEach(function(el) {
      var show = true;
      if (filters.type && filters.type.indexOf(el.getAttribute('data-type')) === -1) show = false;
      if (filters.search && el.getAttribute('data-search').indexOf(filters.search) === -1) show = false;
      el.style.display = show ? '' : 'none';
    });
  }

  function applySort() {
    var val = document.getElementById('shelf-sort').value;
    var parts = val.split('-');
    var key = parts.slice(0, -1).join('-');
    var dir = parts[parts.length - 1];

    var tbody = document.querySelector('.shelf-table tbody');
    if (!tbody) return;
    var rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort(function(a, b) {
      var aVal, bVal;
      if (key === 'rating') {
        aVal = parseFloat(a.getAttribute('data-rating')) || 0;
        bVal = parseFloat(b.getAttribute('data-rating')) || 0;
      } else if (key === 'date_added') {
        aVal = a.getAttribute('data-date') || '';
        bVal = b.getAttribute('data-date') || '';
      } else if (key === 'title') {
        aVal = a.getAttribute('data-search').split(' ')[0] || '';
        bVal = b.getAttribute('data-search').split(' ')[0] || '';
      }
      if (aVal < bVal) return dir === 'asc' ? -1 : 1;
      if (aVal > bVal) return dir === 'asc' ? 1 : -1;
      return 0;
    });

    rows.forEach(function(row) { tbody.appendChild(row); });
  }
})();
</script>
