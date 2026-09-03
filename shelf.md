---
layout: page
title: Shelf
permalink: /shelf/
---

Recent things I've been reading, plus some stuff I'd recommend as representative of my favorite cool/unique ideas!

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
<section class="shelf-section">
<h2 class="shelf-section-heading">Recommended</h2>
<div class="shelf-starred">
  {% for item in starred_items %}{% include shelf-card.html item=item variant="starred" %}{% endfor %}
</div>
</section>
{% endif %}

<!-- In the Queue (in-progress + up-next) -->
{% assign in_progress = site.data.shelf | where: "visible", true | where: "status", "in-progress" %}
{% assign up_next = site.data.shelf | where: "visible", true | where: "status", "up-next" %}
{% assign queue_items = in_progress | concat: up_next %}
{% if queue_items.size > 0 %}
<section class="shelf-section">
<h2 class="shelf-section-heading">In the Queue</h2>
<div class="shelf-collapsible shelf-queue is-collapsed" id="shelf-queue" data-limit="5">
  {% for item in queue_items %}{% if forloop.index > 5 %}{% assign hide = true %}{% else %}{% assign hide = false %}{% endif %}{% include shelf-card.html item=item variant="queue" status=true hidden=hide %}{% endfor %}
</div>
{% if queue_items.size > 5 %}
<button class="shelf-btn shelf-show-more" data-target="shelf-queue" data-count="{{ queue_items.size }}">Show all ({{ queue_items.size }})</button>
{% endif %}
</section>
{% endif %}

<!-- Backlog -->
{% assign backlog_items = site.data.shelf | where: "visible", true | where: "status", "backlog" %}
{% if backlog_items.size > 0 %}
<section class="shelf-section">
<h2 class="shelf-section-heading">Backlog</h2>
<div class="shelf-collapsible shelf-backlog is-collapsed" id="shelf-backlog" data-limit="5">
  {% for item in backlog_items %}{% if forloop.index > 5 %}{% assign hide = true %}{% else %}{% assign hide = false %}{% endif %}{% include shelf-card.html item=item variant="backlog" hidden=hide %}{% endfor %}
</div>
{% if backlog_items.size > 5 %}
<button class="shelf-btn shelf-show-more" data-target="shelf-backlog" data-count="{{ backlog_items.size }}">Show all ({{ backlog_items.size }})</button>
{% endif %}
</section>
{% endif %}

<noscript>
<style>
.shelf-collapsible.is-collapsed .shelf-collapse-hidden { display: block; }
.shelf-show-more { display: none; }
</style>
</noscript>

<!-- Full Table -->
<details class="shelf-everything" id="shelf-everything">
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
        data-title="{{ item.title | downcase }}"
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

<p class="shelf-empty" id="shelf-empty" hidden>Nothing matches those filters.</p>

<!-- Entertainment -->
<!--
<h2 class="shelf-section-heading">Entertainment</h2>

Some shows, films, and games I've enjoyed or have thoughts about. Less structured than the above.
-->

<script>
(function() {
  var HIDDEN = 'shelf-collapse-hidden';
  var FILTERED = 'shelf-filtered-out';

  var groups = Array.prototype.map.call(
    document.querySelectorAll('.shelf-collapsible'),
    function(el) {
      return {
        el: el,
        limit: parseInt(el.getAttribute('data-limit'), 10) || 5,
        cards: Array.prototype.slice.call(el.querySelectorAll('.shelf-card')),
        btn: document.querySelector('.shelf-show-more[data-target="' + el.id + '"]')
      };
    }
  );

  // ---- Collapsible sections ----------------------------------------------
  // Collapse state lives on the container class, never on inline styles, so
  // it can't fight with the filter/search hiding below.

  groups.forEach(function(g) {
    if (!g.btn) return;
    g.btn.addEventListener('click', function() {
      g.el.classList.toggle('is-collapsed');
      syncButton(g);
    });
    syncButton(g);
  });

  function syncButton(g) {
    if (!g.btn) return;
    var collapsed = g.el.classList.contains('is-collapsed');
    g.btn.textContent = collapsed
      ? 'Show all (' + g.btn.getAttribute('data-count') + ')'
      : 'Show less';
  }

  // Which cards fall past the fold depends on the current sort order, so
  // recompute it rather than trusting the build-time assignment.
  function applyCollapse() {
    groups.forEach(function(g) {
      var shown = 0;
      g.cards.forEach(function(card) {
        if (card.classList.contains(FILTERED)) {
          card.classList.remove(HIDDEN);
          return;
        }
        shown++;
        card.classList.toggle(HIDDEN, shown > g.limit);
      });
    });
  }

  // ---- Filter buttons (multi-select: click toggles, "All" resets) ---------
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

  document.getElementById('shelf-search').addEventListener('input', applyFilters);
  document.getElementById('shelf-sort').addEventListener('change', applySort);

  function getActiveFilters() {
    var filters = {};
    document.querySelectorAll('.shelf-btn-group').forEach(function(group) {
      var key = group.getAttribute('data-filter');
      var active = Array.from(group.querySelectorAll('.shelf-btn.active'));
      var values = active.map(function(b) { return b.getAttribute('data-value'); });
      filters[key] = values.indexOf('all') !== -1 ? null : values;
    });
    filters.search = document.getElementById('shelf-search').value.trim().toLowerCase();
    return filters;
  }

  function applyFilters() {
    var filters = getActiveFilters();
    var active = !!(filters.type || filters.search);

    document.querySelectorAll('[data-search]').forEach(function(el) {
      var show = true;
      if (filters.type && filters.type.indexOf(el.getAttribute('data-type')) === -1) show = false;
      if (filters.search && el.getAttribute('data-search').indexOf(filters.search) === -1) show = false;
      el.classList.toggle(FILTERED, !show);
    });

    // While filtering, show every match rather than the first N — otherwise a
    // hit buried past the fold looks like no hit at all.
    groups.forEach(function(g) {
      g.el.classList.toggle('is-filtering', active);
      if (g.btn) g.btn.hidden = active;
    });
    applyCollapse();

    // Drop section headings that no longer have anything under them.
    var anyVisible = false;
    document.querySelectorAll('.shelf-section').forEach(function(section) {
      var has = section.querySelector('.shelf-card:not(.' + FILTERED + ')') !== null;
      section.hidden = !has;
      anyVisible = anyVisible || has;
    });

    var everything = document.getElementById('shelf-everything');
    var rowsLeft = document.querySelector('.shelf-table-row:not(.' + FILTERED + ')') !== null;
    everything.hidden = !rowsLeft;
    if (active && rowsLeft) everything.open = true;

    document.getElementById('shelf-empty').hidden = anyVisible || rowsLeft;
  }

  // ---- Sort ---------------------------------------------------------------
  function sorter(key, dir) {
    return function(a, b) {
      var aVal, bVal;
      if (key === 'rating') {
        aVal = parseFloat(a.getAttribute('data-rating')) || 0;
        bVal = parseFloat(b.getAttribute('data-rating')) || 0;
      } else if (key === 'date_added') {
        aVal = a.getAttribute('data-date') || '';
        bVal = b.getAttribute('data-date') || '';
      } else {
        aVal = a.getAttribute('data-title') || '';
        bVal = b.getAttribute('data-title') || '';
      }
      if (aVal < bVal) return dir === 'asc' ? -1 : 1;
      if (aVal > bVal) return dir === 'asc' ? 1 : -1;
      return 0;
    };
  }

  function applySort() {
    var val = document.getElementById('shelf-sort').value;
    var parts = val.split('-');
    var key = parts.slice(0, -1).join('-');
    var cmp = sorter(key, parts[parts.length - 1]);

    var tbody = document.querySelector('.shelf-table tbody');
    if (tbody) {
      var rows = Array.from(tbody.querySelectorAll('tr'));
      rows.sort(cmp);
      rows.forEach(function(row) { tbody.appendChild(row); });
    }

    groups.forEach(function(g) {
      g.cards.sort(cmp);
      g.cards.forEach(function(card) { g.el.appendChild(card); });
    });
    applyCollapse();
  }

  applyCollapse();
})();
</script>
