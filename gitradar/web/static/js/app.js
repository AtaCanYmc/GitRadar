document.addEventListener('DOMContentLoaded', () => {
  const tabAnalyzeBtn = document.getElementById('tab-analyze-btn');
  const tabSearchBtn = document.getElementById('tab-search-btn');
  const analyzeSection = document.getElementById('analyze-section');
  const searchSection = document.getElementById('search-section');

  const ideaInput = document.getElementById('idea-input');
  const analyzeBtn = document.getElementById('analyze-btn');
  const searchInput = document.getElementById('search-input');
  const quickSearchBtn = document.getElementById('quick-search-btn');

  const loading = document.getElementById('loading');
  const errorBox = document.getElementById('error-box');
  const errorMessage = document.getElementById('error-message');
  const results = document.getElementById('results');

  // Tab switching
  tabAnalyzeBtn.addEventListener('click', () => {
    tabAnalyzeBtn.classList.add('active');
    tabSearchBtn.classList.remove('active');
    analyzeSection.classList.remove('hidden');
    searchSection.classList.add('hidden');
    results.classList.add('hidden');
  });

  tabSearchBtn.addEventListener('click', () => {
    tabSearchBtn.classList.add('active');
    tabAnalyzeBtn.classList.remove('active');
    searchSection.classList.remove('hidden');
    analyzeSection.classList.add('hidden');
    results.classList.add('hidden');
  });

  // Handle Full Analysis
  analyzeBtn.addEventListener('click', async () => {
    const idea = ideaInput.value.trim();
    if (!idea) return alert('Please enter a project idea prompt!');

    showLoading('Analyzing Idea with LLM & Scanning GitHub...');
    hideError();
    results.classList.add('hidden');

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idea, limit: 10 })
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Failed to analyze idea.');

      renderResults(data);
    } catch (err) {
      showError(err.message);
    } finally {
      hideLoading();
    }
  });

  // Handle Standalone Search
  quickSearchBtn.addEventListener('click', async () => {
    const query = searchInput.value.trim();
    if (!query) return alert('Please enter a search query!');

    showLoading(`Searching GitHub for '${query}'...`);
    hideError();
    results.classList.add('hidden');

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, limit: 10 })
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Failed to search repositories.');

      renderSearchOnlyResults(data.repositories);
    } catch (err) {
      showError(err.message);
    } finally {
      hideLoading();
    }
  });

  function renderResults(data) {
    const { queries, repositories, report } = data;

    // Strategy
    document.getElementById('strategy-content').innerHTML = `
      <p style="color: var(--text-secondary);"><strong>Keywords:</strong> ${queries.search_keywords.join(', ')}</p>
      <p style="color: var(--text-secondary); margin-top: 0.25rem;"><strong>Topics:</strong> ${queries.github_topics.map(t => '#' + t).join(', ')}</p>
      <p style="color: var(--text-secondary); margin-top: 0.25rem;"><strong>Strategy:</strong> ${queries.search_explanation}</p>
    `;

    // Metrics
    const satEl = document.getElementById('metric-saturation');
    satEl.textContent = report.market_saturation;
    if (['Low', 'Düşük'].includes(report.market_saturation)) satEl.style.color = 'var(--accent-green)';
    else if (['Moderate', 'Orta'].includes(report.market_saturation)) satEl.style.color = 'var(--accent-yellow)';
    else satEl.style.color = 'var(--accent-red)';

    document.getElementById('metric-sat-score').textContent = `Saturation Score: ${report.saturation_score}/100`;
    document.getElementById('metric-opportunity').textContent = `${report.opportunity_score}/100`;
    document.getElementById('metric-repos-count').textContent = repositories.length;

    // Overview
    document.getElementById('market-summary-text').textContent = report.market_summary;

    // Table
    renderTable(repositories);

    // Competitors
    const compGrid = document.getElementById('competitor-grid');
    compGrid.innerHTML = '';
    report.top_competitors.forEach(c => {
      const card = document.createElement('div');
      card.className = 'comp-card';
      card.innerHTML = `
        <div class="comp-title">${c.repo_name}</div>
        <div style="margin-bottom: 0.5rem;">
          <strong style="color: #6ee7b7; font-size: 0.85rem;">Strengths:</strong>
          ${c.key_strengths.map(s => `<div class="list-item strength">• ${s}</div>`).join('')}
        </div>
        <div>
          <strong style="color: #fca5a5; font-size: 0.85rem;">Gaps / Weaknesses:</strong>
          ${c.weaknesses_or_gaps.map(w => `<div class="list-item weakness">• ${w}</div>`).join('')}
        </div>
      `;
      compGrid.appendChild(card);
    });

    // Unmet Needs
    const unmetList = document.getElementById('unmet-list');
    unmetList.innerHTML = report.unmet_needs.map(g => `<li style="margin-bottom: 0.5rem; color: #fca5a5;">❌ ${g}</li>`).join('');

    // Differentiators
    const diffList = document.getElementById('diff-list');
    diffList.innerHTML = report.differentiators.map(d => `<li style="margin-bottom: 0.5rem; color: #6ee7b7;">✨ ${d}</li>`).join('');

    // Recommendations
    const recList = document.getElementById('rec-list');
    recList.innerHTML = report.actionable_recommendations.map(r => `<li style="margin-bottom: 0.5rem;">${r}</li>`).join('');

    results.classList.remove('hidden');
  }

  function renderSearchOnlyResults(repos) {
    document.getElementById('strategy-panel').classList.add('hidden');
    document.querySelector('.metrics-grid').classList.add('hidden');
    renderTable(repos);
    results.classList.remove('hidden');
  }

  function renderTable(repos) {
    const tbody = document.getElementById('repos-table-body');
    tbody.innerHTML = '';
    repos.forEach((r, idx) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${idx + 1}</td>
        <td><a href="${r.html_url}" target="_blank">${r.full_name}</a></td>
        <td style="color: var(--accent-yellow); font-weight: bold;">⭐ ${r.stars.toLocaleString()}</td>
        <td>🍴 ${r.forks.toLocaleString()}</td>
        <td style="color: var(--accent-green);">${r.language}</td>
        <td>${r.updated_at}</td>
        <td style="color: var(--text-secondary);">${r.description}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  function showLoading(msg) {
    document.getElementById('loading-status').textContent = msg;
    loading.style.display = 'block';
  }

  function hideLoading() {
    loading.style.display = 'none';
  }

  function showError(msg) {
    errorMessage.textContent = msg;
    errorBox.classList.remove('hidden');
  }

  function hideError() {
    errorBox.classList.add('hidden');
  }
});
