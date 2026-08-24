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

  // Export Buttons
  const exportMDBtn = document.getElementById('export-md-btn');
  const exportJSONBtn = document.getElementById('export-json-btn');
  const copyReportBtn = document.getElementById('copy-report-btn');
  const copyBtnText = document.getElementById('copy-btn-text');

  // Settings Modal Elements
  const settingsModal = document.getElementById('settings-modal');
  const openSettingsBtn = document.getElementById('open-settings-btn');
  const closeSettingsBtn = document.getElementById('close-settings-btn');
  const cancelSettingsBtn = document.getElementById('cancel-settings-btn');
  const saveSettingsBtn = document.getElementById('save-settings-btn');

  const settingReportLangSelect = document.getElementById('setting-report-lang-select');
  const settingModelSelect = document.getElementById('setting-model-select');
  const settingLimitInput = document.getElementById('setting-limit-input');
  const settingGroqKey = document.getElementById('setting-groq-key');
  const settingGithubToken = document.getElementById('setting-github-token');

  // Load Settings from LocalStorage
  let customSettings = JSON.parse(localStorage.getItem('gitradar_settings') || '{}');

  function populateSettingsModal() {
    if (customSettings.language) settingReportLangSelect.value = customSettings.language;
    if (customSettings.model) settingModelSelect.value = customSettings.model;
    if (customSettings.limit) settingLimitInput.value = customSettings.limit;
    if (customSettings.groqKey) settingGroqKey.value = customSettings.groqKey;
    if (customSettings.githubToken) settingGithubToken.value = customSettings.githubToken;
  }

  openSettingsBtn.addEventListener('click', () => {
    populateSettingsModal();
    settingsModal.classList.remove('hidden');
  });

  function closeSettings() {
    settingsModal.classList.add('hidden');
  }

  closeSettingsBtn.addEventListener('click', closeSettings);
  cancelSettingsBtn.addEventListener('click', closeSettings);

  settingsModal.addEventListener('click', (e) => {
    if (e.target === settingsModal) closeSettings();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !settingsModal.classList.contains('hidden')) {
      closeSettings();
    }
  });

  saveSettingsBtn.addEventListener('click', () => {
    customSettings = {
      language: settingReportLangSelect.value,
      model: settingModelSelect.value,
      limit: parseInt(settingLimitInput.value, 10) || 10,
      groqKey: settingGroqKey.value.trim(),
      githubToken: settingGithubToken.value.trim(),
    };
    localStorage.setItem('gitradar_settings', JSON.stringify(customSettings));

    // Also update UI language if setting language matches TR or English
    if (customSettings.language === 'Turkish') {
      currentLang = 'tr';
    } else if (customSettings.language === 'English') {
      currentLang = 'en';
    }
    localStorage.setItem('gitradar_lang', currentLang);
    setLanguage(currentLang);

    closeSettings();
  });

  // Theme Controls
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const themeMoonIcon = document.getElementById('theme-moon-icon');
  const themeSunIcon = document.getElementById('theme-sun-icon');

  let currentTheme = localStorage.getItem('gitradar_theme') || 'dark';
  applyTheme(currentTheme);

  themeToggleBtn.addEventListener('click', () => {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(currentTheme);
    localStorage.setItem('gitradar_theme', currentTheme);
  });

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    if (theme === 'light') {
      themeMoonIcon.classList.add('hidden');
      themeSunIcon.classList.remove('hidden');
    } else {
      themeSunIcon.classList.add('hidden');
      themeMoonIcon.classList.remove('hidden');
    }
  }

  // i18n Translations
  const TRANSLATIONS = {
    en: {
      engine_active: "Engine Active",
      tab_market: "Market Analysis",
      tab_search: "Repository Search",
      analyze_title: "Developer Project Idea Analysis",
      analyze_desc: "Enter your developer tool concept. GitRadar expands query terms, scans live GitHub repositories via REST API, and synthesizes competitive market gaps.",
      idea_placeholder: "e.g. AI-powered terminal code review and git diff analyzer...",
      quick_prompts: "Quick Prompts:",
      chip1: "Terminal AI Reviewer",
      chip2: "K8s Log Explainer",
      chip3: "Rust Git Credential Scanner",
      run_analysis: "Run Market Analysis",
      search_title: "Direct GitHub Search",
      search_desc: "Execute direct GitHub REST API queries to retrieve repository star counts, forks, and details.",
      search_placeholder: "e.g. terminal devtools, git hooks, rust cli...",
      search_repos: "Search Repositories",
      loading_status: "Synthesizing Search Strategy...",
      loading_subtext: "Fetching active GitHub repositories & evaluating market saturation",
      error_title: "Analysis Failed",
      strategy_title: "Synthesized Query Strategy",
      keywords_label: "Keywords:",
      topics_label: "GitHub Topics:",
      strategy_label: "Strategy:",
      opp_score: "Opportunity Score",
      opp_hint: "Market viability rating",
      sat_score: "Market Saturation",
      sat_index: "Saturation index:",
      repos_analyzed: "Repositories Analyzed",
      repos_hint: "GitHub API candidates verified",
      market_synthesis: "Market Synthesis",
      discovered_repos: "Discovered Candidate Repositories",
      th_repo: "Repository",
      th_stars: "Stars",
      th_forks: "Forks",
      th_lang: "Language",
      th_updated: "Updated",
      th_desc: "Description",
      competitors_title: "Top Competitor Profile Breakdown",
      strengths_label: "Strengths",
      weaknesses_label: "Gaps & Weaknesses",
      unmet_title: "Unmet Market Needs",
      diff_title: "Key Differentiators",
      rec_title: "Strategic Action Items",
      settings_title: "Configuration Settings",
      setting_report_lang: "AI Response Language",
      setting_model: "LLM Model",
      setting_limit: "Max Repositories to Analyze",
      setting_groq_key: "Groq API Key",
      setting_github_token: "GitHub Access Token (Optional)",
      btn_cancel: "Cancel",
      btn_save: "Save Settings",
      tech_guide_title: "Technical Implementation & Open-Source Roadmap",
      recommended_stack_label: "Recommended Tech Stack",
      arch_overview_label: "Architecture Overview",
      open_source_blocks_label: "Recommended Open-Source Building Blocks",
      export_report_label: "Export Report",
      btn_export_md: "Export Markdown (.md)",
      btn_export_json: "Export JSON (.json)",
      btn_copy_report: "Copy Report",
      copied_text: "Copied!",
    },
    tr: {
      engine_active: "Servis Aktif",
      tab_market: "Pazar Analizi",
      tab_search: "Depo Arama",
      analyze_title: "Geliştirici Proje Fikir Analizi",
      analyze_desc: "Proje fikrinizi girin. GitRadar sorgu terimlerini genişletir, GitHub canlı depolarını tarar ve pazar fırsatlarını sentezler.",
      idea_placeholder: "örn. Yapay zeka destekli terminal kod inceleme ve git diff analiz aracı...",
      quick_prompts: "Örnek Komutlar:",
      chip1: "Terminal Yapay Zeka İnceleyici",
      chip2: "K8s Log Açıklayıcı",
      chip3: "Rust Git Güvenlik Tarayıcı",
      run_analysis: "Pazar Analizini Başlat",
      search_title: "Doğrudan GitHub Araması",
      search_desc: "GitHub REST API üzerinden doğrudan depo yıldız, çatallanma ve ayrıntı araması gerçekleştirin.",
      search_placeholder: "örn. terminal devtools, git hooks, rust cli...",
      search_repos: "Depoları Ara",
      loading_status: "Arama Stratejisi Oluşturuluyor...",
      loading_subtext: "Aktif GitHub depoları getiriliyor & pazar doygunluğu değerlendiriliyor",
      error_title: "Analiz Başarısız Oldu",
      strategy_title: "Oluşturulan Sorgu Stratejisi",
      keywords_label: "Anahtar Kelimeler:",
      topics_label: "GitHub Konuları:",
      strategy_label: "Strateji:",
      opp_score: "Fırsat Skoru",
      opp_hint: "Pazar uygulanabilirlik derecesi",
      sat_score: "Pazar Doygunluğu",
      sat_index: "Doygunluk indeksi:",
      repos_analyzed: "Analiz Edilen Depolar",
      repos_hint: "Doğrulanan GitHub API adayları",
      market_synthesis: "Pazar Özeti",
      discovered_repos: "Keşfedilen Aday Depolar",
      th_repo: "Depo",
      th_stars: "Yıldız",
      th_forks: "Çatallanma",
      th_lang: "Dil",
      th_updated: "Güncellenme",
      th_desc: "Açıklama",
      competitors_title: "Rakip Profil Analizi",
      strengths_label: "Güçlü Yönler",
      weaknesses_label: "Eksik & Zayıf Yönler",
      unmet_title: "Karşılanmayan Pazar İhtiyaçları",
      diff_title: "Öne Çıkan Farklılaştırıcılar",
      rec_title: "Stratejik Öneriler",
      settings_title: "Yapılandırma Ayarları",
      setting_report_lang: "Yapay Zeka Yanıt Dili",
      setting_model: "LLM Modeli",
      setting_limit: "Analiz Edilecek Maks. Depo Sayısı",
      setting_groq_key: "Groq API Anahtarı",
      setting_github_token: "GitHub Erişim Jetonu (İsteğe Bağlı)",
      btn_cancel: "İptal",
      btn_save: "Ayarları Kaydet",
      tech_guide_title: "Teknik Mimari & Açık Kaynak Yol Haritası",
      recommended_stack_label: "Önerilen Teknoloji Yığını",
      arch_overview_label: "Mimari Genel Bakış",
      open_source_blocks_label: "Önerilen Açık Kaynak Yapı Taşları",
      export_report_label: "Raporu Dışa Aktar",
      btn_export_md: "Markdown İndir (.md)",
      btn_export_json: "JSON İndir (.json)",
      btn_copy_report: "Raporu Kopyala",
      copied_text: "Kopyalandı!",
    }
  };

  let currentLang = localStorage.getItem('gitradar_lang') || 'en';
  setLanguage(currentLang);

  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const selectedLang = btn.getAttribute('data-lang');
      if (selectedLang && selectedLang !== currentLang) {
        currentLang = selectedLang;
        localStorage.setItem('gitradar_lang', currentLang);
        
        // Update customSettings language as well
        customSettings.language = currentLang === 'tr' ? 'Turkish' : 'English';
        localStorage.setItem('gitradar_settings', JSON.stringify(customSettings));

        setLanguage(currentLang);
      }
    });
  });

  function setLanguage(lang) {
    const t = TRANSLATIONS[lang] || TRANSLATIONS.en;

    // Toggle active lang button
    document.querySelectorAll('.lang-btn').forEach(btn => {
      if (btn.getAttribute('data-lang') === lang) btn.classList.add('active');
      else btn.classList.remove('active');
    });

    // Replace text content for data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (t[key]) el.textContent = t[key];
    });

    // Replace chip texts
    document.querySelectorAll('[data-i18n-chip]').forEach(el => {
      const key = el.getAttribute('data-i18n-chip');
      if (t[key]) el.textContent = t[key];
    });

    // Placeholders
    ideaInput.setAttribute('placeholder', t.idea_placeholder);
    searchInput.setAttribute('placeholder', t.search_placeholder);

    // If report is already rendered, re-render texts where applicable
    if (window.lastReportData) {
      renderResults(window.lastReportData);
    }
  }

  // Quick Prompt Chips
  document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const promptText = chip.getAttribute('data-prompt');
      if (promptText) {
        ideaInput.value = promptText;
        ideaInput.focus();
      }
    });
  });

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

  // Enter key trigger for search boxes
  ideaInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') analyzeBtn.click();
  });

  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') quickSearchBtn.click();
  });

  // Export Button Event Handlers
  exportMDBtn.addEventListener('click', () => {
    if (!window.lastReportData) return;
    const mdContent = generateMarkdownReport(window.lastReportData);
    const dateStr = new Date().toISOString().slice(0, 10);
    downloadFile(`gitradar_report_${dateStr}.md`, mdContent, 'text/markdown');
  });

  exportJSONBtn.addEventListener('click', () => {
    if (!window.lastReportData) return;
    const jsonContent = JSON.stringify(window.lastReportData, null, 2);
    const dateStr = new Date().toISOString().slice(0, 10);
    downloadFile(`gitradar_report_${dateStr}.json`, jsonContent, 'application/json');
  });

  copyReportBtn.addEventListener('click', () => {
    if (!window.lastReportData) return;
    const mdContent = generateMarkdownReport(window.lastReportData);
    const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

    navigator.clipboard.writeText(mdContent).then(() => {
      const origText = copyBtnText.textContent;
      copyBtnText.textContent = t.copied_text || "Copied!";
      setTimeout(() => {
        copyBtnText.textContent = origText;
      }, 2000);
    }).catch(err => {
      console.error('Failed to copy to clipboard:', err);
    });
  });

  function downloadFile(filename, text, mimeType) {
    const blob = new Blob([text], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function generateMarkdownReport(data) {
    const { queries, repositories, report } = data;
    const dateStr = new Date().toLocaleString();

    let md = `# 📡 GitRadar Market & Gap Analysis Report\n`;
    md += `*Generated on: ${dateStr}*\n\n`;

    md += `## 📌 Executive Overview\n`;
    md += `- **Project Idea:** ${report.idea_summary || 'N/A'}\n`;
    md += `- **Opportunity Score:** ${report.opportunity_score}/100 🚀\n`;
    md += `- **Market Saturation:** ${report.market_saturation} (Score: ${report.saturation_score || 50}/100)\n`;
    md += `- **Repositories Analyzed:** ${repositories.length}\n\n`;

    md += `### 💡 Market Summary\n${report.market_summary}\n\n`;

    if (queries) {
      md += `## 🧠 Synthesized Search Strategy\n`;
      md += `- **Keywords:** ${queries.search_keywords ? queries.search_keywords.join(', ') : ''}\n`;
      md += `- **GitHub Topics:** ${queries.github_topics ? queries.github_topics.map(t => '#' + t).join(', ') : ''}\n`;
      md += `- **Strategy Note:** ${queries.search_explanation || ''}\n\n`;
    }

    if (repositories && repositories.length > 0) {
      md += `## 📊 Discovered Candidate Repositories\n`;
      md += `| # | Repository | Stars | Forks | Language | Updated | Description |\n`;
      md += `|---|------------|-------|-------|----------|---------|-------------|\n`;
      repositories.forEach((r, idx) => {
        md += `| ${idx + 1} | [${r.full_name}](${r.html_url}) | ${r.stars} | ${r.forks} | ${r.language || 'N/A'} | ${r.updated_at || '-'} | ${(r.description || '').replace(/\|/g, '-')} |\n`;
      });
      md += `\n`;
    }

    if (report.top_competitors && report.top_competitors.length > 0) {
      md += `## 🏆 Top Competitor Profiles\n`;
      report.top_competitors.forEach(c => {
        md += `### ${c.repo_name}\n`;
        md += `**Strengths:**\n`;
        (c.key_strengths || []).forEach(s => { md += `- ✅ ${s}\n`; });
        md += `**Gaps & Weaknesses:**\n`;
        (c.weaknesses_or_gaps || []).forEach(w => { md += `- ❌ ${w}\n`; });
        md += `\n`;
      });
    }

    if (report.unmet_needs && report.unmet_needs.length > 0) {
      md += `## 🚨 Unmet Needs & Ecosystem Gaps\n`;
      report.unmet_needs.forEach(g => { md += `- ❌ ${g}\n`; });
      md += `\n`;
    }

    if (report.differentiators && report.differentiators.length > 0) {
      md += `## 💎 Key Differentiators\n`;
      report.differentiators.forEach(d => { md += `- ✨ ${d}\n`; });
      md += `\n`;
    }

    if (report.actionable_recommendations && report.actionable_recommendations.length > 0) {
      md += `## 🛠️ Strategic Action Items\n`;
      report.actionable_recommendations.forEach((r, idx) => { md += `${idx + 1}. ${r}\n`; });
      md += `\n`;
    }

    if (report.implementation_guide) {
      const g = report.implementation_guide;
      md += `## ⚙️ Technical Implementation & Open-Source Roadmap\n`;
      if (g.recommended_tech_stack && g.recommended_tech_stack.length > 0) {
        md += `**Recommended Tech Stack:** ${g.recommended_tech_stack.join(', ')}\n\n`;
      }
      if (g.architecture_overview) {
        md += `### Architecture Overview\n${g.architecture_overview}\n\n`;
      }
      if (g.open_source_building_blocks && g.open_source_building_blocks.length > 0) {
        md += `### Recommended Open-Source Building Blocks\n`;
        g.open_source_building_blocks.forEach(tool => {
          const urlStr = tool.repo_url ? ` ([GitHub](${tool.repo_url}))` : '';
          md += `- **${tool.name}** \`[${tool.category}]\`${urlStr}: ${tool.description_and_usage}\n`;
        });
        md += `\n`;
      }
    }

    return md;
  }

  // Handle Full Analysis
  analyzeBtn.addEventListener('click', async () => {
    const idea = ideaInput.value.trim();
    if (!idea) {
      ideaInput.focus();
      return;
    }

    const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
    showLoading(t.loading_status);
    hideError();
    results.classList.add('hidden');

    const limit = customSettings.limit || 10;
    const model = customSettings.model || 'groq/openai/gpt-oss-120b';
    const language = customSettings.language || (currentLang === 'tr' ? 'Turkish' : 'English');

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idea, limit, model, language })
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Failed to analyze project idea.');

      window.lastReportData = data;
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
    if (!query) {
      searchInput.focus();
      return;
    }

    showLoading(`Searching GitHub for '${query}'...`);
    hideError();
    results.classList.add('hidden');

    const limit = customSettings.limit || 10;

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, limit })
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
    const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

    // Strategy Panel
    const keywordsHtml = queries.search_keywords
      .map(k => `<span class="badge-code">${escapeHtml(k)}</span>`)
      .join(' ');
    
    const topicsHtml = queries.github_topics
      .map(t => `<span class="badge-topic">#${escapeHtml(t)}</span>`)
      .join(' ');

    document.getElementById('strategy-content').innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 0.6rem;">
        <div><strong style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase;">${t.keywords_label}</strong> <div style="display: inline-flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.2rem;">${keywordsHtml}</div></div>
        <div><strong style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase;">${t.topics_label}</strong> <div style="display: inline-flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.2rem;">${topicsHtml}</div></div>
        <p style="color: var(--text-secondary); font-size: 0.875rem; margin-top: 0.2rem;">${escapeHtml(queries.search_explanation)}</p>
      </div>
    `;

    // Metrics Overview
    document.getElementById('metric-opportunity').textContent = report.opportunity_score;
    document.getElementById('opp-bar-fill').style.width = `${Math.min(100, Math.max(0, report.opportunity_score))}%`;

    const satEl = document.getElementById('metric-saturation');
    satEl.textContent = report.market_saturation;
    const satScore = report.saturation_score || 50;
    document.getElementById('sat-bar-fill').style.width = `${satScore}%`;
    document.getElementById('metric-sat-score').textContent = `${t.sat_index} ${satScore}/100`;

    if (['Low', 'Düşük'].includes(report.market_saturation)) {
      satEl.style.color = 'var(--accent-emerald)';
      document.getElementById('sat-bar-fill').style.background = 'var(--accent-emerald)';
    } else if (['Moderate', 'Orta'].includes(report.market_saturation)) {
      satEl.style.color = 'var(--accent-amber)';
      document.getElementById('sat-bar-fill').style.background = 'var(--accent-amber)';
    } else {
      satEl.style.color = 'var(--accent-rose)';
      document.getElementById('sat-bar-fill').style.background = 'var(--accent-rose)';
    }

    document.getElementById('metric-repos-count').textContent = repositories.length;

    // Market Overview
    document.getElementById('market-summary-text').textContent = report.market_summary;

    // Repositories Table
    renderTable(repositories);

    // Competitors Analysis Grid
    const compGrid = document.getElementById('competitor-grid');
    compGrid.innerHTML = '';
    report.top_competitors.forEach(c => {
      const card = document.createElement('div');
      card.className = 'comp-card';
      
      const strengthsHtml = c.key_strengths.map(s => `
        <div class="list-item-clean">
          <svg class="list-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--accent-emerald)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <span>${escapeHtml(s)}</span>
        </div>
      `).join('');

      const weaknessesHtml = c.weaknesses_or_gaps.map(w => `
        <div class="list-item-clean">
          <svg class="list-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--accent-rose)" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          <span>${escapeHtml(w)}</span>
        </div>
      `).join('');

      card.innerHTML = `
        <div class="comp-repo-name">${escapeHtml(c.repo_name)}</div>
        <div class="comp-section-title strengths">${t.strengths_label}</div>
        ${strengthsHtml}
        <div class="comp-section-title weaknesses">${t.weaknesses_label}</div>
        ${weaknessesHtml}
      `;
      compGrid.appendChild(card);
    });

    // Unmet Market Needs
    const unmetContainer = document.getElementById('unmet-list');
    unmetContainer.innerHTML = report.unmet_needs.map(g => `
      <div class="list-item-clean" style="background: rgba(244, 63, 94, 0.06); padding: 0.6rem 0.8rem; border-radius: 8px; border: 1px solid rgba(244, 63, 94, 0.15);">
        <svg class="list-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-rose)" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        <span style="color: var(--text-primary); font-size: 0.875rem;">${escapeHtml(g)}</span>
      </div>
    `).join('');

    // Key Differentiators
    const diffContainer = document.getElementById('diff-list');
    diffContainer.innerHTML = report.differentiators.map(d => `
      <div class="list-item-clean" style="background: rgba(16, 185, 129, 0.06); padding: 0.6rem 0.8rem; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.15);">
        <svg class="list-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-emerald)" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
        <span style="color: var(--text-primary); font-size: 0.875rem;">${escapeHtml(d)}</span>
      </div>
    `).join('');

    // Recommendations
    const recContainer = document.getElementById('rec-list');
    recContainer.innerHTML = report.actionable_recommendations.map((r, idx) => `
      <div class="recommendation-card">
        <div class="rec-number">${idx + 1}</div>
        <div class="rec-text">${escapeHtml(r)}</div>
      </div>
    `).join('');

    // Technical Implementation Guide
    const implSection = document.getElementById('implementation-section');
    if (report.implementation_guide) {
      const guide = report.implementation_guide;

      // Tech Stack Badges
      const stackBadges = (guide.recommended_tech_stack || [])
        .map(t => `<span class="badge-code" style="border-color: rgba(99, 102, 241, 0.3); color: var(--accent-indigo);">${escapeHtml(t)}</span>`)
        .join(' ');
      document.getElementById('tech-stack-badges').innerHTML = stackBadges || '<span style="color: var(--text-muted); font-size: 0.85rem;">N/A</span>';

      // Architecture Overview
      document.getElementById('arch-overview-text').textContent = guide.architecture_overview || '';

      // Open Source Building Blocks
      const toolsList = document.getElementById('open-source-tools-list');
      toolsList.innerHTML = '';
      (guide.open_source_building_blocks || []).forEach(tool => {
        const card = document.createElement('div');
        card.className = 'comp-card';
        card.style.borderColor = 'rgba(99, 102, 241, 0.2)';

        const linkHtml = tool.repo_url
          ? `<a href="${escapeHtml(tool.repo_url)}" target="_blank" rel="noopener noreferrer" style="color: var(--accent-indigo); font-size: 0.8rem; font-family: var(--font-mono); text-decoration: none;"> 🔗 GitHub</a>`
          : '';

        card.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.4rem;">
            <div style="font-weight: 700; color: var(--text-primary); font-size: 0.95rem;">${escapeHtml(tool.name)} ${linkHtml}</div>
            <span class="badge-topic" style="font-size: 0.7rem; padding: 0.15rem 0.4rem;">${escapeHtml(tool.category)}</span>
          </div>
          <p style="color: var(--text-secondary); font-size: 0.85rem; line-height: 1.4;">${escapeHtml(tool.description_and_usage)}</p>
        `;
        toolsList.appendChild(card);
      });

      implSection.classList.remove('hidden');
    } else {
      implSection.classList.add('hidden');
    }

    document.getElementById('strategy-panel').classList.remove('hidden');
    document.querySelectorAll('.metrics-grid').forEach(el => el.classList.remove('hidden'));
    results.classList.remove('hidden');
  }

  function renderSearchOnlyResults(repos) {
    document.getElementById('strategy-panel').classList.add('hidden');
    document.getElementById('implementation-section').classList.add('hidden');
    document.querySelectorAll('.metrics-grid').forEach(el => el.classList.add('hidden'));
    renderTable(repos);
    results.classList.remove('hidden');
  }

  function renderTable(repos) {
    const tbody = document.getElementById('repos-table-body');
    tbody.innerHTML = '';
    repos.forEach((r, idx) => {
      const tr = document.createElement('tr');
      const langColor = getLanguageColor(r.language);

      tr.innerHTML = `
        <td style="font-family: var(--font-mono); color: var(--text-muted); width: 40px;">${idx + 1}</td>
        <td>
          <a class="repo-link" href="${escapeHtml(r.html_url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(r.full_name)}</a>
        </td>
        <td class="stat-cell">
          <span style="color: var(--accent-amber); display: inline-flex; align-items: center; gap: 0.3rem;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            ${(r.stars || 0).toLocaleString()}
          </span>
        </td>
        <td class="stat-cell">
          <span style="color: var(--text-secondary); display: inline-flex; align-items: center; gap: 0.3rem;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="18" r="3"></circle><circle cx="6" cy="6" r="3"></circle><circle cx="18" cy="6" r="3"></circle><path d="M18 9v2a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V9"></path><path d="M12 12v3"></path></svg>
            ${(r.forks || 0).toLocaleString()}
          </span>
        </td>
        <td>
          <span class="language-dot" style="background-color: ${langColor};"></span>
          <span>${escapeHtml(r.language || 'Unknown')}</span>
        </td>
        <td style="font-family: var(--font-mono); font-size: 0.8rem;">${escapeHtml(r.updated_at || '-')}</td>
        <td style="color: var(--text-secondary); font-size: 0.85rem; max-width: 320px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">${escapeHtml(r.description || '')}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  function getLanguageColor(lang) {
    const colors = {
      'Python': '#3572A5',
      'Rust': '#dea584',
      'Go': '#00ADD8',
      'TypeScript': '#3178c6',
      'JavaScript': '#f1e05a',
      'C++': '#f34b7d',
      'C': '#555555',
      'Shell': '#89e051',
      'HTML': '#e34c26',
      'CSS': '#563d7c',
    };
    return colors[lang] || '#94a3b8';
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
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
