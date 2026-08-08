// Redirect API dynamically when index.html is loaded via file:// protocol
const API = window.location.protocol === "file:" ? "http://127.0.0.1:8765" : "";

// Fail-safe mock for Lucide icons to prevent crash in offline/blocked network states
if (typeof window.lucide === 'undefined' || !window.lucide.createIcons) {
  window.lucide = { createIcons: () => {} };
}

let sessionId = localStorage.getItem("rapsim_session_id") || null;
let pendingResponses = [];
let currentPrompt = null;
let metaOptions = null;
let activeTab = "dashboard";
let cachedState = null;
let activeActionId = null;

// Automation flags to prevent prompt popups during background navigation loads
let isAutomating = false;

// Custom toast notification system
function showToast(title, message, isBeat = false) {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = `toast-alert ${isBeat ? "beat-toast" : ""}`;
  toast.innerHTML = `
    <i data-lucide="${isBeat ? "sliders" : "music"}"></i>
    <div class="toast-content">
      <h4>${escapeHtml(title)}</h4>
      <p>${escapeHtml(message)}</p>
    </div>
  `;
  container.appendChild(toast);
  lucide.createIcons();
  
  // Slide out and remove
  setTimeout(() => {
    toast.style.animation = "toastSlideIn 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28) reverse forwards";
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 8000);
}

// ==========================================================================
// UTILITY FUNCTIONS & API
// ==========================================================================
async function api(path, options = {}) {
  const res = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || res.statusText || "Request failed");
  return data;
}

function moneyFormat(n) {
  if (n == null) return "$0";
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(1)}K`;
  return `$${Math.round(n)}`;
}

function escapeHtml(s) {
  return String(s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function showScreen(id) {
  document.querySelectorAll(".screen").forEach((el) => el.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  lucide.createIcons();
}

// Tab Switching
function switchTab(tabId) {
  activeTab = tabId;
  document.querySelectorAll(".nav-item").forEach((el) => {
    if (el.getAttribute("data-tab") === tabId) el.classList.add("active");
    else el.classList.remove("active");
  });
  
  document.querySelectorAll(".viewport-tab").forEach((el) => {
    if (el.id === `tab-${tabId}`) el.classList.add("active");
    else el.classList.remove("active");
  });

  // Automatically trigger loading actions for specific tabs
  if (tabId === "hot100") {
    triggerTabBackgroundAction(25); // Run Hot 100
  } else if (tabId === "twitter") {
    loadTwitterFeed(); // Start Twitter loop
  } else if (tabId === "news") {
    loadNewsFeed(); // Start News loop
  } else if (tabId === "grammy") {
    loadGrammyAwards(); // Load Grammys
  } else if (tabId === "studio") {
    refreshBeatVault();
    populateStudioSelectors();
    resetSongWizard();
  } else if (tabId === "shawtify") {
    loadShawtifyStreams();
  } else if (tabId === "ratings") {
    loadUserRatings();
  } else if (tabId === "critic-reviews") {
    renderCriticReviewsTab();
  } else if (tabId === "disstracks") {
    loadDissTracksFeed();
  } else if (tabId === "beats") {
    refreshBeatVault();
    renderBeatSalesFeed();
  }
}

function resetSongWizard() {
  const step1 = document.getElementById("song-step-1");
  const step2 = document.getElementById("song-step-2");
  if (step1 && step2) {
    step1.classList.remove("hidden");
    step2.classList.add("hidden");
  }
  const ind1 = document.getElementById("step-ind-1");
  const ind2 = document.getElementById("step-ind-2");
  if (ind1 && ind2) {
    ind1.classList.add("active");
    ind2.classList.remove("active");
  }
}

// ==========================================================================
// SESSION STATE SYNC & UPDATE
// ==========================================================================
function renderArtistHUD(state) {
  cachedState = state;
  const a = state.artist;
  
  // Left Sidebar HUD
  document.getElementById("hud-name").textContent = a.name;
  document.getElementById("hud-avatar").textContent = a.name.split(" ").map(n => n[0]).join("").slice(0, 2).toUpperCase();
  
  // Determine Career Stage / Tier based on popularity
  let tier = "Underground Artist";
  if (a.popularity > 80) tier = "Megastar";
  else if (a.popularity > 60) tier = "Mainstream Star";
  else if (a.popularity > 40) tier = "Rising Star";
  else if (a.popularity > 20) tier = "Local Talent";
  document.getElementById("hud-tier").textContent = tier;
  
  // Meters
  document.getElementById("hud-pop-val").textContent = `${Math.round(a.popularity)}%`;
  document.getElementById("hud-pop-bar").style.width = `${Math.min(100, a.popularity)}%`;
  
  document.getElementById("hud-rep-val").textContent = `${Math.round(a.reputation)}%`;
  document.getElementById("hud-rep-bar").style.width = `${Math.min(100, a.reputation)}%`;
  
  // Footer
  document.getElementById("footer-health").textContent = `${Math.round(a.health)}%`;
  document.getElementById("footer-fatigue").textContent = `${Math.round(a.fatigue)}%`;
  
  // Course status
  const courseItem = document.getElementById("course-footer-item");
  if (courseItem) {
    if (a.course) {
      courseItem.style.display = "flex";
      courseItem.style.justifyContent = "space-between";
      document.getElementById("footer-course").textContent = `${a.course} (${a.course_weeks_left}w left)`;
    } else {
      courseItem.style.display = "none";
    }
  }
  
  // Topbar
  document.getElementById("topbar-week").textContent = `Year ${a.year} · Week ${a.week}`;
  document.getElementById("topbar-money").textContent = moneyFormat(a.money);
  
  const partnerPill = document.getElementById("pill-partner");
  if (a.current_love) {
    partnerPill.classList.remove("hidden");
    document.getElementById("topbar-partner").textContent = `${a.current_love.partner} (${Math.round(a.current_love.lovingness)}%)`;
  } else {
    partnerPill.classList.add("hidden");
  }

  // Dashboard Stats Grid
  document.getElementById("dash-streams").textContent = moneyFormat(a.last_week_streams).replace("$", "");
  document.getElementById("dash-earnings").textContent = moneyFormat(a.last_week_earnings);
  document.getElementById("dash-pop").textContent = `${Math.round(a.popularity)}%`;
  document.getElementById("dash-rep").textContent = `${Math.round(a.reputation)}%`;
  
  // Dashboard Action Summary Gigs
  document.getElementById("act-beats-count").textContent = a.vault_beats;
  document.getElementById("act-singles-count").textContent = a.unreleased_singles;
  document.getElementById("act-albums-count").textContent = a.album_drafts;
  document.getElementById("act-hustle").textContent = a.side_hustle ? "Yes" : "No";
  
  // Skills rendering
  if (a.skills) {
    const ly = a.skills["lyrics"] || 25;
    const vo = a.skills["vocals"] || 25;
    const pr = a.skills["production"] || 25;
    const mx = a.skills["mix/master"] || 25;
    
    // Dashboard progress bars and value labels
    const bLy = document.getElementById("bar-lyrics");
    const bVo = document.getElementById("bar-vocals");
    const bPr = document.getElementById("bar-production");
    const bMx = document.getElementById("bar-mix");
    
    const vLy = document.getElementById("val-lyrics");
    const vVo = document.getElementById("val-vocals");
    const vPr = document.getElementById("val-production");
    const vMx = document.getElementById("val-mix");
    
    if (bLy) bLy.style.width = ly + "%";
    if (bVo) bVo.style.width = vo + "%";
    if (bPr) bPr.style.width = pr + "%";
    if (bMx) bMx.style.width = mx + "%";
    
    if (vLy) vLy.textContent = ly;
    if (vVo) vVo.textContent = vo;
    if (vPr) vPr.textContent = pr;
    if (vMx) vMx.textContent = mx;
    
    // Studio skills indicators
    const stLy = document.getElementById("studio-skill-lyrics");
    const stVo = document.getElementById("studio-skill-vocals");
    const stPr = document.getElementById("studio-skill-production");
    const stMx = document.getElementById("studio-skill-mix");
    
    if (stLy) stLy.textContent = ly;
    if (stVo) stVo.textContent = vo;
    if (stPr) stPr.textContent = pr;
    if (stMx) stMx.textContent = mx;
  }
  
  // Genre Proficiency Rendering
  const genreListDiv = document.getElementById("genre-proficiency-list");
  if (genreListDiv && a.genres) {
    const genreEntries = Object.entries(a.genres);
    genreEntries.sort((x, y) => y[1] - x[1]);
    const topGenres = genreEntries.slice(0, 4);
    
    if (topGenres.length === 0) {
      genreListDiv.innerHTML = `<p class="muted text-small py-2">No active genre training yet.</p>`;
    } else {
      genreListDiv.innerHTML = topGenres.map(([g, val]) => `
        <div class="skill-progress-item">
          <span class="skill-name">${escapeHtml(g)}</span>
          <div class="progress-bar-wrapper">
            <div class="progress-bar-fill" style="width: ${val}%"></div>
          </div>
          <span class="skill-val">${val}</span>
        </div>
      `).join("");
    }
  }
  
  // Local storage save
  localStorage.setItem("rapsim_session_id", state.session_id);
  sessionId = state.session_id;
  
  // Update top 3 on dashboard in background if we have cached Hot 100 rows
  updateDashboardHot3();
  
  lucide.createIcons();
}

function updateDashboardHot3() {
  const dashList = document.getElementById("dash-hot-list");
  const stored = localStorage.getItem("rapsim_cached_hot100");
  if (!stored) return;
  
  try {
    const rows = JSON.parse(stored);
    if (rows && rows.length > 0) {
      dashList.innerHTML = rows.slice(0, 3).map((r, i) => `
        <div class="mini-hot-item">
          <span class="rank">#${i + 1}</span>
          <div class="info">
            <strong>${escapeHtml(r.title)}</strong>
            <span>${escapeHtml(r.artist)}</span>
          </div>
          <span class="streams">${escapeHtml(r.streams)}</span>
        </div>
      `).join("");
    }
  } catch (err) {
    console.warn("Failed to update dashboard hot 3", err);
  }
}

// ==========================================================================
// BACKGROUND AUTOMATION BRIDGE
// ==========================================================================
async function triggerTabBackgroundAction(actionId) {
  isAutomating = true;
  pendingResponses = [];
  try {
    const result = await api(`/api/session/${sessionId}/action`, {
      method: "POST",
      body: JSON.stringify({ action_id: actionId, responses: null }),
    });
    
    if (result.logs?.length) appendLog(result.logs);
    
    // Parse result based on the action executed
    if (actionId === 25) { // Hot 100
      parseAndRenderHot100(result.logs);
    }
    
    if (result.state) renderArtistHUD(result.state);
  } catch (err) {
    appendLog(`Background action error: ${err.message}`);
  } finally {
    isAutomating = false;
  }
}

// Multi-step automation for Twitter feed
async function loadTwitterFeed() {
  isAutomating = true;
  document.getElementById("twitter-posts-container").innerHTML = `<div class="text-center py-5 muted"><i data-lucide="refresh-cw" class="spin-slow"></i> Syncing social media feeds...</div>`;
  lucide.createIcons();
  
  try {
    let res = await api(`/api/session/${sessionId}/action`, {
      method: "POST",
      body: JSON.stringify({ action_id: 18, responses: null }),
    });
    
    if (res.status === "input_required" && res.prompt.title === "TWITTER") {
      res = await api(`/api/session/${sessionId}/action`, {
        method: "POST",
        body: JSON.stringify({ action_id: 18, responses: [1] }),
      });
      
      if (res.status === "input_required" && res.prompt.type === "confirm") {
        parseAndRenderTweets(res.logs);
        
        res = await api(`/api/session/${sessionId}/action`, {
          method: "POST",
          body: JSON.stringify({ action_id: 18, responses: [1, "", 3] }),
        });
      }
    }
    
    if (res.state) renderArtistHUD(res.state);
  } catch (err) {
    document.getElementById("twitter-posts-container").innerHTML = `<div class="text-center py-5 error">Failed to load feed: ${err.message}</div>`;
  } finally {
    isAutomating = false;
  }
}

// Multi-step automation for News
async function loadNewsFeed() {
  isAutomating = true;
  document.getElementById("news-feed-container").innerHTML = `<div class="text-center py-5 muted"><i data-lucide="refresh-cw" class="spin-slow"></i> Loading news briefings...</div>`;
  lucide.createIcons();
  
  try {
    let res = await api(`/api/session/${sessionId}/action`, {
      method: "POST",
      body: JSON.stringify({ action_id: 17, responses: null }),
    });
    
    if (res.status === "input_required" && res.prompt.title === "INDUSTRY NEWS") {
      res = await api(`/api/session/${sessionId}/action`, {
        method: "POST",
        body: JSON.stringify({ action_id: 17, responses: [1] }),
      });
      
      if (res.status === "input_required" && res.prompt.type === "confirm") {
        parseAndRenderNews(res.logs);
        
        res = await api(`/api/session/${sessionId}/action`, {
          method: "POST",
          body: JSON.stringify({ action_id: 17, responses: [1, "", 3] }),
        });
      }
    }
    
    if (res.state) renderArtistHUD(res.state);
  } catch (err) {
    document.getElementById("news-feed-container").innerHTML = `<div class="text-center py-5 error">Failed to load news: ${err.message}</div>`;
  } finally {
    isAutomating = false;
  }
}

// Automation for Grammys
async function loadGrammyAwards() {
  isAutomating = true;
  document.getElementById("grammy-results-panel").innerHTML = `<div class="card"><p class="muted text-center py-4"><i data-lucide="refresh-cw" class="spin-slow"></i> Opening Grammy Records...</p></div>`;
  lucide.createIcons();
  
  try {
    let res = await api(`/api/session/${sessionId}/action`, {
      method: "POST",
      body: JSON.stringify({ action_id: 26, responses: null }),
    });
    
    parseAndRenderGrammys(res.logs);
    
    if (res.status === "input_required") {
      hidePrompt();
    }
    if (res.state) renderArtistHUD(res.state);
  } catch (err) {
    document.getElementById("grammy-results-panel").innerHTML = `<div class="card"><p class="muted text-center py-4">Failed to load: ${err.message}</p></div>`;
  } finally {
    isAutomating = false;
  }
}

// Shawtify Streams (Action 13)
async function loadShawtifyStreams() {
  const tbody = document.getElementById("shawtify-body");
  tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 muted"><i data-lucide="refresh-cw" class="spin-slow"></i> Connecting to Shawtify metrics...</td></tr>`;
  lucide.createIcons();
  
  try {
    const res = await api(`/api/session/${sessionId}/action`, {
      method: "POST",
      body: JSON.stringify({ action_id: 13, responses: null }),
    });
    
    if (res.logs?.length) {
      appendLog(res.logs);
      parseAndRenderShawtify(res.logs);
    } else {
      tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 muted">No tracks recorded on streams yet. Release some music!</td></tr>`;
    }
    if (res.state) renderArtistHUD(res.state);
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 error">Error: ${err.message}</td></tr>`;
  }
}

// User Ratings (Action 19)
async function loadUserRatings() {
  const tbody = document.getElementById("ratings-table-body");
  tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 muted"><i data-lucide="refresh-cw" class="spin-slow"></i> Loading IMDb Database...</td></tr>`;
  lucide.createIcons();
  
  const chartChoice = Number(document.getElementById("sel-ratings-chart").value);
  isAutomating = true;
  
  try {
    // 1. Run Ratings Action
    let res = await api(`/api/session/${sessionId}/action`, {
      method: "POST",
      body: JSON.stringify({ action_id: 19, responses: null }),
    });
    
    if (res.status === "input_required" && res.prompt.title === "Ratings menu") {
      // 2. Select selected option
      res = await api(`/api/session/${sessionId}/action`, {
        method: "POST",
        body: JSON.stringify({ action_id: 19, responses: [chartChoice] }),
      });
      
      if (res.status === "input_required" && res.prompt.type === "confirm") {
        // 3. Parse and render ratings table
        parseAndRenderRatingsTable(res.logs, chartChoice);
        
        // 4. Resolve prompt by sending Enter and exit Ratings loop
        res = await api(`/api/session/${sessionId}/action`, {
          method: "POST",
          body: JSON.stringify({ action_id: 19, responses: [chartChoice, "", 9] }),
        });
      }
    }
    
    if (res.state) renderArtistHUD(res.state);
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 error">Failed to sync ratings: ${err.message}</td></tr>`;
  } finally {
    isAutomating = false;
  }
}

// Diss Tracks (Action 27)
async function loadDissTracksFeed() {
  if (!sessionId) return;
  isAutomating = true;
  const container = document.getElementById("disstracks-feed-container");
  container.innerHTML = `<div class="text-center py-5 muted"><i data-lucide="refresh-cw" class="spin-slow"></i> Connecting to Diss Track Database...</div>`;
  lucide.createIcons();
  
  try {
    let res = await api(`/api/session/${sessionId}/action`, {
      method: "POST",
      body: JSON.stringify({ action_id: 27, responses: null }),
    });
    
    if (res.status === "input_required" && res.prompt.title === "Diss tracks") {
      parseAndRenderDissTracks(res.prompt.options, res.logs);
      
      const exitOption = res.prompt.options.length + 1;
      res = await api(`/api/session/${sessionId}/action`, {
        method: "POST",
        body: JSON.stringify({ action_id: 27, responses: [exitOption] }),
      });
    } else {
      container.innerHTML = `<div class="text-center py-5 muted">No diss tracks recorded in this session yet.</div>`;
    }
    
    if (res.state) renderArtistHUD(res.state);
  } catch (err) {
    container.innerHTML = `<div class="text-center py-5 error">Failed to load beefs: ${err.message}</div>`;
  } finally {
    isAutomating = false;
  }
}

// Refresh beat vault summary
async function refreshBeatVault() {
  const v = document.getElementById("studio-beat-vault");
  const tabV = document.getElementById("beats-tab-vault-list");
  
  if (v) v.innerHTML = `<p class="muted py-4 text-center"><i data-lucide="refresh-cw" class="spin-slow"></i> Fetching beats...</p>`;
  if (tabV) tabV.innerHTML = `<p class="muted py-4 text-center"><i data-lucide="refresh-cw" class="spin-slow"></i> Fetching beats...</p>`;
  
  lucide.createIcons();
  try {
    const data = await api(`/api/session/${sessionId}/vault`);
    
    // Update selectors in Song Recording form
    const beatSelect = document.getElementById("song-beat-select");
    if (beatSelect) {
      beatSelect.innerHTML = `<option value="">No Vault Beat (Roll standard beat)</option>`;
    }
    
    if (!data.beats || !data.beats.length) {
      if (v) v.innerHTML = `<p class="muted py-4 text-center">Beat vault is empty. Produce some beats or visit the store!</p>`;
      if (tabV) tabV.innerHTML = `<p class="muted py-4 text-center">Beat vault is empty. Produce some beats or visit the store!</p>`;
      return;
    }
    
    const htmlContent = data.beats.map(b => `
      <div class="beat-card">
        ${b.consumed ? `<span class="used-tag">USED</span>` : ""}
        <div class="beat-icon"><i data-lucide="music-2"></i></div>
        <h4>${escapeHtml(b.name)}</h4>
        <span class="genre">${escapeHtml(b.genre)}</span>
        <div class="quality">Quality: <strong>${b.quality}/10</strong></div>
      </div>
    `).join("");
    
    if (v) v.innerHTML = htmlContent;
    if (tabV) tabV.innerHTML = htmlContent;
    
    // Populate select
    if (beatSelect) {
      data.beats.forEach(b => {
        if (!b.consumed) {
          const opt = document.createElement("option");
          opt.value = b.name;
          opt.textContent = `${b.name} (${b.genre}, Q:${b.quality}/10)`;
          beatSelect.appendChild(opt);
        }
      });
    }
    
    lucide.createIcons();
  } catch (err) {
    if (v) v.innerHTML = `<p class="muted py-4 text-center">Error: ${err.message}</p>`;
    if (tabV) tabV.innerHTML = `<p class="muted py-4 text-center">Error: ${err.message}</p>`;
  }
}

// Populate genre/theme dropdowns in Studio form
function populateStudioSelectors() {
  if (!metaOptions) return;
  
  // Genres selects checkboxes in song recording desk
  const genreDiv = document.getElementById("song-genre-selects");
  genreDiv.innerHTML = metaOptions.genres.map(g => `
    <label class="check-item">
      <input type="checkbox" class="song-genres-box" value="${escapeHtml(g)}" />
      <span>${escapeHtml(g)}</span>
    </label>
  `).join("");
  
  // Themes
  const themeSelect = document.getElementById("song-theme-select");
  themeSelect.innerHTML = metaOptions.themes.map(t => `<option value="${escapeHtml(t)}">${escapeHtml(t)}</option>`).join("");
  
  // Beat creator genres
  const beatGenre = document.getElementById("beat-genre-select");
  beatGenre.innerHTML = metaOptions.genres.map(g => `<option value="${escapeHtml(g)}">${escapeHtml(g)}</option>`).join("");
  
  // New album setup selectors
  const albumGenre = document.getElementById("album-new-genre");
  albumGenre.innerHTML = metaOptions.genres.map(g => `<option value="${escapeHtml(g)}">${escapeHtml(g)}</option>`).join("");
  const albumTheme = document.getElementById("album-new-theme");
  albumTheme.innerHTML = metaOptions.themes.map(t => `<option value="${escapeHtml(t)}">${escapeHtml(t)}</option>`).join("");
}

// Fetch list of current album drafts for song creation destination
async function updateAlbumDraftsList() {
  if (!sessionId) return;
  const list = document.getElementById("album-drafts-list");
  const select = document.getElementById("album-draft-select");
  
  select.innerHTML = `<option value="new">[Create New Album Draft]</option>`;
  
  try {
    const res = await api(`/api/session/${sessionId}`);
    // Unfortunately, we need to inspect options list by triggering Album draft flow (Action 6) or catalog.
    // Instead, since the snapshots don't return list, we'll let them type the name of draft if they want,
    // or select create new.
  } catch (err) {
    console.error("Failed to load album drafts:", err);
  }
}

// ==========================================================================
// REGEX LOG PARSERS (UI WIDGET RENDERING)
// ==========================================================================

// Parse and render Hot 100 Chart
function parseAndRenderHot100(logs) {
  const tbody = document.getElementById("hot100-body");
  const fullText = logs.join("\n");
  const lines = fullText.split("\n");
  
  const chartRows = [];
  let isChart = false;
  
  for (let line of lines) {
    if (line.includes("HOT 100 (Last Week Streams)") || line.includes("HOT 100")) {
      isChart = true;
      continue;
    }
    if (isChart && line.includes("----")) continue;
    if (isChart && line.startsWith("Rank") && line.includes("Streams")) continue;
    
    if (isChart) {
      if (line.trim() === "" && chartRows.length > 0) {
        break;
      }
      
      const cols = line.trim().split(/\s{2,}/);
      if (cols.length >= 5) {
        chartRows.push({
          rank: cols[0],
          title: cols[1],
          artist: cols[2],
          project: cols[3],
          release: cols[4],
          streams: cols[5] || "0"
        });
      }
    }
  }
  
  if (chartRows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 muted">No Hot 100 streams recorded yet. Publish a single and simulate the week!</td></tr>`;
    return;
  }
  
  // Cache top 3 to localStorage
  localStorage.setItem("rapsim_cached_hot100", JSON.stringify(chartRows.slice(0, 3)));
  updateDashboardHot3();
  
  const playerArtistName = cachedState?.artist?.name || "";
  
  tbody.innerHTML = chartRows.map(r => {
    const isPlayer = r.artist.toLowerCase().includes(playerArtistName.toLowerCase()) || r.artist === playerArtistName;
    return `
      <tr class="${isPlayer ? "highlight-player" : ""}">
        <td><strong>#${r.rank}</strong></td>
        <td><strong>${escapeHtml(r.title)}</strong></td>
        <td>${escapeHtml(r.artist)}</td>
        <td><span class="muted">${escapeHtml(r.project)}</span></td>
        <td>${escapeHtml(r.release)}</td>
        <td style="text-align: right; font-weight: 600;">${escapeHtml(r.streams)}</td>
      </tr>
    `;
  }).join("");
}

// Parse Shawtify Streams (Action 13)
function parseAndRenderShawtify(logs) {
  const tbody = document.getElementById("shawtify-body");
  const fullText = logs.join("\n");
  const lines = fullText.split("\n");
  
  const songs = [];
  let isShawtify = false;
  
  for (let line of lines) {
    if (line.includes("SHAWTIFY STREAMS")) {
      isShawtify = true;
      continue;
    }
    if (isShawtify && line.startsWith("- ")) {
      // Form: - 1. Title [source] | total X | this week Y | sales Z | CERT catchy X viral Y review X
      const mainParts = line.slice(2).split("|").map(p => p.trim());
      
      const titleAndSource = mainParts[0];
      const titleMatch = titleAndSource.match(/^(\d+)\.\s+(.*?)\s+\[(.*?)\]/);
      if (titleMatch) {
        const index = titleMatch[1];
        const name = titleMatch[2];
        const source = titleMatch[3];
        
        const totalStreams = mainParts[1] ? mainParts[1].replace("total ", "") : "0";
        const thisWeekStreams = mainParts[2] ? mainParts[2].replace("this week ", "") : "0";
        const salesText = mainParts[3] ? mainParts[3].replace("sales ", "") : "";
        const certAndReviews = mainParts[4] || "";
        
        // Extract RIAA certification
        let cert = "None";
        if (certAndReviews.includes("Gold")) cert = "🥇 Gold";
        else if (certAndReviews.includes("Platinum")) cert = "💿 Platinum";
        else if (certAndReviews.includes("Multi-Platinum")) cert = "💿💿 Multi-Platinum";
        else if (certAndReviews.includes("Diamond")) cert = "💎 Diamond";
        
        // Extract review score
        const revMatch = certAndReviews.match(/avg review\s*([\d.]+)\/10/);
        const review = revMatch ? `${revMatch[1]}/10` : "-";
        
        songs.push({
          index,
          name,
          source,
          total: totalStreams,
          thisWeek: thisWeekStreams,
          sales: salesText.split(" total ")[0] || "0",
          cert,
          review
        });
      }
    }
  }
  
  if (songs.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 muted">No tracks recorded on streams yet. Release some music!</td></tr>`;
    return;
  }
  
  tbody.innerHTML = songs.map(s => `
    <tr>
      <td>#${s.index}</td>
      <td><strong>${escapeHtml(s.name)}</strong></td>
      <td><span class="badge">${escapeHtml(s.source)}</span></td>
      <td>${escapeHtml(s.total)}</td>
      <td>${escapeHtml(s.thisWeek)}</td>
      <td>${escapeHtml(s.sales)}</td>
      <td><strong>${s.cert}</strong></td>
      <td style="text-align: right; font-weight: 600; color: var(--accent-gold);">${s.review}</td>
    </tr>
  `).join("");
}

// Parse IMDb ratings table
function parseAndRenderRatingsTable(logs, chartChoice) {
  const tbody = document.getElementById("ratings-table-body");
  const headers = document.getElementById("ratings-table-headers");
  const fullLogs = logs.join("\n");
  const lines = fullLogs.split("\n");
  
  const ratings = [];
  let isTable = false;
  let headerLine = "";
  
  // Set headers based on selection
  if (chartChoice === 4 || chartChoice === 5) { // Artist chart (Top 20 rated, Top 10 hated)
    headers.innerHTML = `
      <th style="width: 70px;">Rank</th>
      <th>Artist Name</th>
      <th>Average Rating Score</th>
      <th style="text-align: right; width: 140px;">Votes Count</th>
    `;
  } else if (chartChoice === 8) { // Diss tracks chart
    headers.innerHTML = `
      <th style="width: 70px;">Rank</th>
      <th>Title</th>
      <th>Artist</th>
      <th>IMDb Rating Score</th>
      <th style="text-align: right; width: 140px;">Streams</th>
    `;
  } else { // Project / song chart (2, 3, 6, 7)
    headers.innerHTML = `
      <th style="width: 70px;">Rank</th>
      <th>Title</th>
      <th>Artist</th>
      <th>IMDb Rating Score</th>
      <th style="text-align: right; width: 140px;">Votes Count</th>
    `;
  }
  
  for (let line of lines) {
    if (line.includes("IMDb User Ratings") || line.includes("Hated Artists") || line.includes("Rated Artists") || line.includes("Rated Songs") || line.includes("Diss Tracks") || line.includes("USER RATINGS CENTRAL")) {
      isTable = true;
      continue;
    }
    if (isTable && line.includes("----")) continue;
    if (isTable && (line.startsWith("Rank") || line.includes("Score") || line.includes("RK"))) {
      headerLine = line;
      continue;
    }
    
    if (isTable) {
      if (line.trim() === "" && ratings.length > 0) {
        break;
      }
      
      const cols = line.trim().split(/\s{2,}/);
      if (cols.length >= 3) {
        if (chartChoice === 4 || chartChoice === 5) { // Artist
          ratings.push({
            rank: cols[0],
            name: cols[1],
            score: cols[2],
            votes: cols[4] || "0"
          });
        } else if (chartChoice === 8) { // Diss tracks
          ratings.push({
            rank: cols[0],
            title: cols[1],
            artist: cols[2],
            score: cols[4],
            votes: cols[9] || "0"
          });
        } else { // Songs/albums
          ratings.push({
            rank: cols[0],
            title: cols[1],
            artist: cols[2],
            score: cols[4],
            votes: cols[5] || "0"
          });
        }
      }
    }
  }
  
  if (ratings.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 muted">No entries match this IMDb chart yet. Complete a few years or releases!</td></tr>`;
    return;
  }
  
  tbody.innerHTML = ratings.map(r => {
    if (chartChoice === 4 || chartChoice === 5) {
      return `
        <tr>
          <td><strong>#${r.rank}</strong></td>
          <td><strong>${escapeHtml(r.name)}</strong></td>
          <td><strong style="color:var(--accent-gold);">${escapeHtml(r.score)}/10</strong></td>
          <td style="text-align: right;">${escapeHtml(r.votes)}</td>
        </tr>
      `;
    } else {
      return `
        <tr>
          <td><strong>#${r.rank}</strong></td>
          <td><strong>${escapeHtml(r.title)}</strong></td>
          <td>${escapeHtml(r.artist)}</td>
          <td><strong style="color:var(--accent-gold);">${escapeHtml(r.score)}/10</strong></td>
          <td style="text-align: right;">${escapeHtml(r.votes)}</td>
        </tr>
      `;
    }
  }).join("");
}

// Parse and render Tweets
function parseAndRenderTweets(logs) {
  const container = document.getElementById("twitter-posts-container");
  const fullText = logs.join("\n");
  const lines = fullText.split(/\r?\n/);
  
  const tweets = [];
  let currentTweet = null;
  
  for (let line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    
    // Check for header line: author  @username  [label]
    const headerMatch = line.match(/^([^\s].*?)\s{2,}(@[^\s]+)\s{2,}\[([^\]]+)\]/);
    if (headerMatch) {
      if (currentTweet) {
        tweets.push(currentTweet);
      }
      currentTweet = {
        author: headerMatch[1].trim(),
        username: headerMatch[2].trim(),
        type: headerMatch[3].trim(),
        contentLines: [],
        likes: "0",
        rts: "0"
      };
      continue;
    }
    
    if (!currentTweet) continue;
    
    // Check if it is the footer line: likes X | rts Y
    const footerMatch = trimmed.match(/^likes\s+([^\s|]+)\s*\|\s*rts\s+(.*)$/i);
    if (footerMatch) {
      currentTweet.likes = footerMatch[1].trim();
      currentTweet.rts = footerMatch[2].trim();
      tweets.push(currentTweet);
      currentTweet = null;
      continue;
    }
    
    // Otherwise, it is a content line if it starts with space
    if (line.startsWith("  ") || line.startsWith(" ")) {
      currentTweet.contentLines.push(trimmed);
    }
  }
  
  if (currentTweet) {
    tweets.push(currentTweet);
  }
  
  if (tweets.length === 0) {
    container.innerHTML = `<div class="text-center py-5 muted">There are no trending tweets on X / Twitter this week.</div>`;
    return;
  }
  
  container.innerHTML = tweets.map(tw => {
    const content = tw.contentLines.join(" ");
    return `
      <div class="tweet-card">
        <div class="tweet-avatar">${escapeHtml(tw.author.slice(0, 2).toUpperCase())}</div>
        <div class="tweet-content-area">
          <div class="tweet-header">
            <span class="author">${escapeHtml(tw.author)}</span>
            <span class="username">${escapeHtml(tw.username)}</span>
            <span class="badge-type">${escapeHtml(tw.type)}</span>
          </div>
          <div class="tweet-body">
            ${escapeHtml(content)}
          </div>
          <div class="tweet-actions">
            <span><i data-lucide="heart" style="width:12px;height:12px;"></i> ${escapeHtml(tw.likes)}</span>
            <span><i data-lucide="repeat" style="width:12px;height:12px;"></i> ${escapeHtml(tw.rts)}</span>
          </div>
        </div>
      </div>
    `;
  }).join("");
  lucide.createIcons();
}

// Parse and render News Reports
function parseAndRenderNews(logs) {
  const container = document.getElementById("news-feed-container");
  const fullText = logs.join("\n");
  
  // Split on news card borders (dashes)
  const newsBlocks = fullText.split(/\+[-]{10,}\+/);
  const articles = [];
  
  for (let block of newsBlocks) {
    if (!block.includes("[") || !block.includes("Week Y")) continue;
    
    const lines = block.split(/\r?\n/).map(l => l.replace(/^\|/, "").replace(/\|$/, "").trim());
    
    let type = "News";
    let medium = "Press";
    let weekStr = "";
    let source = "Pulsewire";
    let reporter = "Staff Writer";
    let headlineLines = [];
    let playerImpact = "";
    
    for (let line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      
      if (trimmed.startsWith("[")) {
        const typeMatch = trimmed.match(/\[([^\]]+)\]\s+\[([^\]]+)\]\s+Week\s+(Y\d+\s+W\d+)/i);
        if (typeMatch) {
          type = typeMatch[1].trim();
          medium = typeMatch[2].trim();
          weekStr = typeMatch[3].trim();
        }
      } else if (trimmed.startsWith("Source")) {
        const srcMatch = trimmed.match(/Source\s+([^\s]+)\s+Reporter\s+(.*)/i);
        if (srcMatch) {
          source = srcMatch[1].trim();
          reporter = srcMatch[2].trim();
        }
      } else if (trimmed.startsWith("Player impact:")) {
        playerImpact = trimmed.replace("Player impact:", "").trim();
      } else if (trimmed.startsWith("Border") || trimmed.startsWith("Response") || trimmed === "") {
        continue;
      } else {
        headlineLines.push(trimmed);
      }
    }
    
    if (headlineLines.length > 0) {
      articles.push({
        type,
        medium,
        week: weekStr,
        source,
        reporter,
        headline: headlineLines.join(" "),
        impact: playerImpact
      });
    }
  }
  
  if (articles.length === 0) {
    container.innerHTML = `<div class="text-center py-5 muted">No news bulletins published this week. Check back next week.</div>`;
    document.getElementById("dash-news-list").innerHTML = `<p class="muted py-2 text-center text-small">No news headlines available yet.</p>`;
    return;
  }
  
  container.innerHTML = articles.map(art => `
    <div class="news-card ${art.impact ? "player-involved" : ""}">
      <div class="news-meta">
        <span class="agency ${art.source.toLowerCase().includes("whisper") ? "whisper" : ""}">${escapeHtml(art.source)} — ${escapeHtml(art.reporter)}</span>
        <span>${escapeHtml(art.week)} | ${escapeHtml(art.type)}</span>
      </div>
      <div class="news-headline">
        ${escapeHtml(art.headline)}
      </div>
      ${art.impact ? `<div class="player-impact"><i data-lucide="sparkles" style="width:12px;height:12px;display:inline-block;vertical-align:middle;margin-right:0.25rem;"></i> Clout Impact: <strong>${escapeHtml(art.impact)}</strong></div>` : ""}
    </div>
  `).join("");
  
  // Render mini list on Dashboard
  document.getElementById("dash-news-list").innerHTML = articles.slice(0, 3).map(art => `
    <div class="dash-news-card">
      <span class="source">${escapeHtml(art.source)} · ${escapeHtml(art.week)}</span>
      <p class="headline">${escapeHtml(art.headline)}</p>
    </div>
  `).join("");
  
  lucide.createIcons();
}

// Parse and store ecosystem new releases
async function loadNewReleasesWidget() {
  if (!sessionId) return;
  isAutomating = true;
  try {
    let res = await api(`/api/session/${sessionId}/action`, {
      method: "POST",
      body: JSON.stringify({ action_id: 14, responses: null }),
    });
    
    if (res.status === "input_required" && res.prompt.title === "New releases") {
      parseAndRenderNewReleases(res.logs);
      
      // Press enter to resolve and exit prompt loop
      await api(`/api/session/${sessionId}/action`, {
        method: "POST",
        body: JSON.stringify({ action_id: 14, responses: [""] }),
      });
    }
  } catch (err) {
    console.warn("Failed to load ecosystem new releases widget:", err.message);
  } finally {
    isAutomating = false;
  }
}

function parseAndRenderNewReleases(logs) {
  const container = document.getElementById("dash-new-releases-list");
  if (!container) return;
  
  const fullText = logs.join("\n");
  const lines = fullText.split(/\r?\n/);
  
  const releases = [];
  for (let line of lines) {
    const match = line.match(/^- \s*(.*?)\s*\|\s*(.*?)\s*\|\s*'(.*?)'\s*\|\s*([\d.]+)\/10.*\|\s*sales\s*(.*?)\s*first week/i) || line.match(/^-\s*(.*?)\s*\|\s*(.*?)\s*\|\s*'(.*?)'\s*\|\s*([\d.]+)\/10.*\|\s*sales\s*(.*?)\s*first week/i);
    if (match) {
      releases.push({
        artist: match[1].trim(),
        type: match[2].trim(),
        title: match[3].trim(),
        rating: match[4].trim(),
        sales: match[5].trim()
      });
    }
  }
  
  if (releases.length === 0) {
    container.innerHTML = `<p class="muted text-small py-2 text-center">No new releases dropped in the ecosystem this week.</p>`;
    return;
  }
  
  container.innerHTML = releases.map(r => `
    <div class="dash-news-card" style="border-left: 3px solid var(--accent-gold); padding-left: 0.5rem; margin-bottom: 0.5rem;">
      <span class="source">${escapeHtml(r.artist)} · ${escapeHtml(r.type.toUpperCase())}</span>
      <p class="headline" style="font-weight: bold; margin: 0.2rem 0;">"${escapeHtml(r.title)}"</p>
      <span class="date" style="font-size: 0.75rem;">Score: ${escapeHtml(r.rating)}/10 · Sales: ${escapeHtml(r.sales)} first week</span>
    </div>
  `).join("");
}

// Parse and store ecosystem/player beat sales from simulate week logs
function parseAndStoreBeatSales(logs) {
  if (!logs || !logs.length) return;
  const fullText = logs.join("\n");
  const lines = fullText.split(/\r?\n/);
  
  let sales = JSON.parse(localStorage.getItem("rapsim_beat_sales") || "[]");
  
  const purchaseRegex = /(.*?) bought (.*?) beat "(.*?)" from (.*?) for (\$.*)/i;
  const playerSaleRegex = /(.*?) bought "(.*?)" for (\$.*)/i;
  
  let newSalesFound = false;
  
  for (let line of lines) {
    let m = line.match(purchaseRegex);
    if (m) {
      sales.unshift({
        buyer: m[1].trim(),
        genre: m[2].trim(),
        beat: m[3].trim(),
        producer: m[4].trim(),
        price: m[5].trim(),
        type: "npc"
      });
      newSalesFound = true;
      continue;
    }
    
    let pm = line.match(playerSaleRegex);
    if (pm) {
      sales.unshift({
        buyer: pm[1].trim(),
        genre: "player",
        beat: pm[2].trim(),
        producer: "You",
        price: pm[3].trim(),
        type: "player"
      });
      newSalesFound = true;
    }
  }
  
  if (newSalesFound) {
    sales = sales.slice(0, 100);
    localStorage.setItem("rapsim_beat_sales", JSON.stringify(sales));
    renderBeatSalesFeed();
  }
}

function renderBeatSalesFeed() {
  const container = document.getElementById("beats-tab-sales-feed");
  if (!container) return;
  
  const sales = JSON.parse(localStorage.getItem("rapsim_beat_sales") || "[]");
  if (!sales.length) {
    container.innerHTML = `<p class="muted text-small text-center py-4">No transactions recorded this week yet. Simulate weeks to watch the market!</p>`;
    return;
  }
  
  container.innerHTML = sales.map(s => {
    if (s.type === "player") {
      return `
        <div class="news-item" style="border-left: 3px solid var(--accent-gold); padding-left: 0.5rem; margin-bottom: 0.5rem; background-color: rgba(166, 157, 111, 0.05);">
          <span class="date" style="color: var(--accent-gold);">Player Sale</span>
          <p class="mb-0"><strong>${escapeHtml(s.buyer)}</strong> bought your beat <strong>"${escapeHtml(s.beat)}"</strong> for <strong class="text-green">${escapeHtml(s.price)}</strong>!</p>
        </div>
      `;
    } else {
      return `
        <div class="news-item" style="margin-bottom: 0.5rem;">
          <span class="date">${escapeHtml(s.genre.toUpperCase())} BEAT</span>
          <p class="mb-0"><strong>${escapeHtml(s.buyer)}</strong> bought <strong>"${escapeHtml(s.beat)}"</strong> from <strong>${escapeHtml(s.producer)}</strong> for <strong>${escapeHtml(s.price)}</strong>.</p>
        </div>
      `;
    }
  }).join("");
}

// Parse and render Grammys
function parseAndRenderGrammys(logs) {
  const panel = document.getElementById("grammy-results-panel");
  const fullText = logs.join("\n");
  
  if (fullText.includes("Not generated yet")) {
    panel.innerHTML = `<div class="card"><h3 class="muted text-center py-4">Grammy Awards are not generated yet. Come back during Weeks 49 - 52.</h3></div>`;
    return;
  }
  if (fullText.includes("No eligible projects released")) {
    panel.innerHTML = `<div class="card"><h3 class="muted text-center py-4">No eligible projects released this year (albums/mixtapes only).</h3></div>`;
    return;
  }

  const lines = fullText.split(/\r?\n/);
  const parsedCats = [];
  let currentCat = null;
  let parseState = null;

  for (let line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    // Match e.g. "1. Best Hip Hop Album"
    const catHeaderMatch = trimmed.match(/^\d+\.\s+(.*)$/);
    if (catHeaderMatch) {
      if (currentCat) {
        parsedCats.push(currentCat);
      }
      currentCat = {
        category: catHeaderMatch[1].trim(),
        nominees: [],
        winner: null
      };
      parseState = null;
      continue;
    }

    if (!currentCat) continue;

    if (trimmed.startsWith("Nominees:")) {
      parseState = "nominees";
      continue;
    }
    if (trimmed.startsWith("Winner:")) {
      parseState = "winner";
      continue;
    }

    if (parseState === "nominees") {
      if (trimmed.startsWith("- ")) {
        const parts = trimmed.slice(2).split("|").map(p => p.trim());
        currentCat.nominees.push({
          title: parts[0] || "",
          artist: parts[1] || "",
          score: parts[2] ? parts[2].replace("review ", "") : ""
        });
      }
    } else if (parseState === "winner") {
      const takesMatch = trimmed.match(/^(.*?)\s+takes it with\s+'(.*?)'/i);
      if (takesMatch) {
        currentCat.winner = {
          artist: takesMatch[1].trim(),
          title: takesMatch[2].trim()
        };
      } else if (trimmed.includes("not announced yet")) {
        currentCat.winner = { unannounced: true };
      }
    }
  }

  if (currentCat) {
    parsedCats.push(currentCat);
  }

  if (parsedCats.length === 0) {
    panel.innerHTML = `<div class="card"><h3 class="muted text-center py-4">No Grammy categories loaded. Eligibility window: Weeks 1-48. Awards drop week 49.</h3></div>`;
    return;
  }

  panel.innerHTML = parsedCats.map(cat => `
    <div class="card grammy-category-card">
      <h4>🏆 ${escapeHtml(cat.category)}</h4>
      <div class="nominees-list">
        <strong>Nominees:</strong>
        ${cat.nominees.map(nom => {
          const isWinner = cat.winner && !cat.winner.unannounced && 
                           nom.artist.toLowerCase() === cat.winner.artist.toLowerCase() && 
                           nom.title.toLowerCase().includes(cat.winner.title.toLowerCase());
          return `
            <div class="nominee-item ${isWinner ? "winner-item" : ""}">
              <span>${escapeHtml(nom.title)} — <span class="muted">${escapeHtml(nom.artist)}</span></span>
              ${isWinner ? `<span class="winner-tag">🏆 Winner</span>` : `<span class="muted font-mono">${escapeHtml(nom.score)}</span>`}
            </div>
          `;
        }).join("")}
        ${cat.winner && cat.winner.unannounced ? `<div class="unannounced-winner"><i data-lucide="lock" style="width:12px;height:12px;display:inline-block;vertical-align:middle;margin-right:0.25rem;"></i> Envelope sealed: winner announced in Week 49</div>` : ""}
      </div>
    </div>
  `).join("");
}

// Parse album reviews text and store
function parseAndStoreCriticReviews(logs) {
  const fullText = logs.join("\n");
  if (!fullText.includes("ALBUM REVIEWS:")) return;
  
  // Find Album average score header
  const avgHeaderMatch = fullText.match(/ALBUM:\s*'([^']+)'\s*\|\s*AVG CRITICAL SCORE:\s*([\d.]+)\/10/i);
  if (!avgHeaderMatch) return;
  
  const albumName = avgHeaderMatch[1];
  const avgScore = avgHeaderMatch[2];
  
  // Split by critic header symbol: ★
  const criticBlocks = fullText.split("★").slice(1);
  const reviews = [];
  
  for (let block of criticBlocks) {
    const lines = block.split(/\r?\n/);
    const headerMatch = lines[0].match(/^(.*?)\s+\[(.*?)\]/);
    if (!headerMatch) continue;
    
    const criticName = headerMatch[1].trim();
    const tagline = headerMatch[2].trim();
    
    let textLines = [];
    let isText = true;
    let score = "0";
    
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (line.startsWith("──────") || line === "") continue;
      
      if (line.startsWith("Track Ratings:")) {
        isText = false;
        continue;
      }
      
      const scoreMatch = line.match(/Album Score:\s*([\d.]+)\/10/i);
      if (scoreMatch) {
        score = scoreMatch[1];
        break;
      }
      
      if (isText) {
        textLines.push(line);
      }
    }
    
    reviews.push({
      critic: criticName,
      tagline,
      score,
      text: textLines.join(" ")
    });
  }
  
  const reviewObj = {
    album: albumName,
    average: avgScore,
    criticReviews: reviews,
    date: cachedState?.artist ? `Year ${cachedState.artist.year} · Week ${cachedState.artist.week}` : ""
  };
  
  // Load existing reviews history list
  let history = [];
  try {
    const storedHistory = localStorage.getItem("rapsim_reviews_history");
    if (storedHistory) {
      history = JSON.parse(storedHistory);
    }
  } catch (e) {
    console.error(e);
  }
  
  // Avoid duplicate entries
  history = history.filter(item => item.album !== albumName);
  history.unshift(reviewObj);
  
  localStorage.setItem("rapsim_reviews_history", JSON.stringify(history));
  localStorage.setItem("rapsim_latest_reviews", JSON.stringify(reviewObj));
  
  if (activeTab === "critic-reviews") {
    renderCriticReviewsTab();
  }
}

// Render Critic Reviews Tab from LocalStorage
function renderCriticReviewsTab() {
  const container = document.getElementById("critic-reviews-container");
  const selectorContainer = document.getElementById("critic-reviews-selector-container");
  const selectEl = document.getElementById("sel-critic-review-album");
  
  const storedHistory = localStorage.getItem("rapsim_reviews_history");
  if (!storedHistory) {
    container.innerHTML = `<p class="muted py-5 text-center">No reviews recorded in this session yet. Release an album to view critic quotes.</p>`;
    selectorContainer.classList.add("hidden");
    return;
  }
  
  try {
    const history = JSON.parse(storedHistory);
    if (!history || history.length === 0) {
      container.innerHTML = `<p class="muted py-5 text-center">No reviews recorded in this session yet. Release an album to view critic quotes.</p>`;
      selectorContainer.classList.add("hidden");
      return;
    }
    
    selectorContainer.classList.remove("hidden");
    
    const currentVal = selectEl.value;
    selectEl.innerHTML = history.map(item => `<option value="${escapeHtml(item.album)}">${escapeHtml(item.album)} (${item.average}/10)</option>`).join("");
    
    if (currentVal && history.some(item => item.album === currentVal)) {
      selectEl.value = currentVal;
    } else {
      selectEl.value = history[0].album;
    }
    
    displaySelectedAlbumReview(selectEl.value, history);
  } catch (err) {
    container.innerHTML = `<p class="muted py-5 text-center">Error reading reviews history: ${err.message}</p>`;
    selectorContainer.classList.add("hidden");
  }
}

function displaySelectedAlbumReview(albumName, history) {
  const container = document.getElementById("critic-reviews-container");
  const data = history.find(item => item.album === albumName);
  if (!data) return;
  
  container.innerHTML = `
    <div class="critic-review-card">
      <div class="critic-cover-col">
        <i data-lucide="disc" class="spin-slow"></i>
        <h4>${escapeHtml(data.album)}</h4>
        <span class="muted text-xs">${escapeHtml(data.date)}</span>
        <div class="score">${escapeHtml(data.average)}</div>
        <span class="text-xs muted">Avg Critic Score</span>
      </div>
      
      <div class="critic-text-col">
        <h3>Critic Review Breakdowns</h3>
        <div class="critic-quotes-list">
          ${data.criticReviews.map(r => `
            <div class="critic-quote-item">
              <div class="quote-header">
                <span>${escapeHtml(r.critic)} [${escapeHtml(r.tagline)}]</span>
                <strong style="color:var(--accent-gold);">${escapeHtml(r.score)}/10</strong>
              </div>
              <p>"${escapeHtml(r.text)}"</p>
            </div>
          `).join("")}
        </div>
      </div>
    </div>
  `;
  lucide.createIcons();
}

// Parse catalog lists
function parseAndRenderCatalog(logs) {
  const singlesDiv = document.getElementById("catalog-singles-list");
  const albumsDiv = document.getElementById("catalog-albums-list");
  const fullText = logs.join("\n");
  
  const singles = [];
  const albums = [];
  
  let currentSection = "";
  
  const lines = fullText.split(/\r?\n/);
  for (let line of lines) {
    const clean = line.trim();
    if (clean === "Singles") {
      currentSection = "singles";
      continue;
    }
    if (clean === "Albums") {
      currentSection = "albums";
      continue;
    }
    
    if (clean.startsWith("- ") && clean.includes("|")) {
      const parts = clean.slice(2).split("|").map(p => p.trim());
      const title = parts[0].replace(/^\d+\.\s+/, "");
      
      if (currentSection === "singles") {
        singles.push({
          title,
          quality: parts[1] || "",
          genre: parts[2] || "",
          status: parts[3] || "unreleased",
          details: parts.slice(4).join(" | ")
        });
      } else if (currentSection === "albums") {
        albums.push({
          title,
          tracks: parts[1] || "",
          type: parts[2] || "album",
          status: parts[3] || "draft",
          details: parts.slice(4).join(" | ")
        });
      }
    }
  }
  
  if (singles.length) {
    singlesDiv.innerHTML = singles.map(s => `
      <div class="catalog-item">
        <div class="catalog-item-info">
          <strong>${escapeHtml(s.title)}</strong>
          <span>${escapeHtml(s.genre)} · ${escapeHtml(s.details)}</span>
        </div>
        <div class="catalog-item-meta">
          <div class="quality">${escapeHtml(s.quality)}</div>
          <span class="${s.status.includes("released") ? "released-label" : "draft-label"}">${escapeHtml(s.status)}</span>
        </div>
      </div>
    `).join("");
  } else {
    singlesDiv.innerHTML = `<p class="muted py-4 text-center">No singles found.</p>`;
  }
  
  if (albums.length) {
    albumsDiv.innerHTML = albums.map(a => `
      <div class="catalog-item">
        <div class="catalog-item-info">
          <strong>${escapeHtml(a.title)}</strong>
          <span>${escapeHtml(a.tracks)} · ${escapeHtml(a.type)} · ${escapeHtml(a.details)}</span>
        </div>
        <div class="catalog-item-meta">
          <span class="${a.status.includes("released") ? "released-label" : "draft-label"}">${escapeHtml(a.status)}</span>
        </div>
      </div>
    `).join("");
  } else {
    albumsDiv.innerHTML = `<p class="muted py-4 text-center">No album drafts found.</p>`;
  }
}

// Parse and render Diss Tracks
function parseAndRenderDissTracks(options, logs) {
  const container = document.getElementById("disstracks-feed-container");
  
  if (!options || options.length === 0) {
    container.innerHTML = `<div class="text-center py-5 muted">No diss tracks recorded in the ecosystem yet.</div>`;
    return;
  }
  
  const tracks = [];
  for (let opt of options) {
    if (opt === "Back") continue;
    
    const parts = opt.split("|").map(p => p.trim());
    if (parts.length >= 4) {
      const artistTitle = parts[0];
      const vs = parts[1].replace("vs", "").trim();
      const reception = parts[2].replace("reception", "").trim();
      const streams = parts[3];
      
      const titleMatch = artistTitle.match(/^(.*?)\s+-\s+"(.*?)"/);
      if (titleMatch) {
        tracks.unshift({
          artist: titleMatch[1].trim(),
          title: titleMatch[2].trim(),
          target: vs,
          reception,
          streams
        });
      }
    }
  }
  
  if (tracks.length === 0) {
    container.innerHTML = `<div class="text-center py-5 muted">No diss tracks recorded in the ecosystem yet.</div>`;
    return;
  }
  
  container.innerHTML = `
    <div class="diss-tracks-grid">
      ${tracks.map(t => `
        <div class="card diss-track-card border-gold">
          <div class="diss-header">
            <span class="label text-danger"><i data-lucide="swords" style="width:12px;height:12px;display:inline-block;vertical-align:middle;margin-right:0.25rem;"></i> WAR REPORT</span>
            <span class="streams-count">${escapeHtml(t.streams)}</span>
          </div>
          <h4>${escapeHtml(t.title)}</h4>
          <p class="diss-combatants">
            <strong>${escapeHtml(t.artist)}</strong> <span class="muted">vs</span> <strong>${escapeHtml(t.target)}</strong>
          </p>
          <div class="diss-stats mt-3">
            <div class="stat-item">
              <span class="muted text-xs">Reception Rating</span>
              <strong style="color:var(--accent-gold);">${escapeHtml(t.reception)}</strong>
            </div>
          </div>
        </div>
      `).join("")}
    </div>
  `;
  lucide.createIcons();
}

// ==========================================================================
// ACTION LAUNCHER & CLI PROMPT BRIDGE
// ==========================================================================
async function runAction(actionId, isResume = false) {
  if (!sessionId) return;
  activeActionId = actionId;
  
  if (actionId === 39 && !isResume) {
    if (!confirm("Quit this career session? Your current progress will close.")) return;
  }
  
  if (!isResume) {
    pendingResponses = [];
  }
  
  try {
    const body = { action_id: actionId, responses: pendingResponses.length ? pendingResponses : null };
    const result = await api(`/api/session/${sessionId}/action`, {
      method: "POST",
      body: JSON.stringify(body),
    });
    
    if (result.logs?.length) {
      appendLog(result.logs);
      
      // Parse inline actions:
      if (actionId === 21) parseAndRenderCatalog(result.logs);
      
      // Check for song or beat quality banners in stdout
      parseAndShowCreationToasts(result.logs);
      
      // Check for album reviews texts to store
      parseAndStoreCriticReviews(result.logs);
      
      // Check for weekly beat sales in stdout
      parseAndStoreBeatSales(result.logs);
    }
    
    if (result.status === "quit") {
      sessionId = null;
      localStorage.removeItem("rapsim_session_id");
      localStorage.removeItem("rapsim_beat_sales");
      showScreen("screen-new");
      document.getElementById("log-output").textContent = "Session ended.";
      return;
    }
    
    // Live Concert stage capture
    if (result.status === "input_required" && (logsContainConcert(result.logs) || logsContainConcert(result.prompt.label))) {
      window._resumeAction = { actionId };
      showConcertHUD(result.prompt, result.logs);
      if (result.state) renderArtistHUD(result.state);
      return;
    }
    
    // Intercept automated Song Creation form
    if (result.status === "input_required" && window._songCreationState) {
      window._resumeAction = { actionId };
      automateSongCreation(result.prompt);
      return;
    }

    // Intercept automated Beat Creation DAW form
    if (result.status === "input_required" && window._beatCreationState) {
      window._resumeAction = { actionId };
      automateBeatCreation(result.prompt);
      return;
    }

    // Intercept automated Catalog Manager
    if (result.status === "input_required" && window._catalogState) {
      window._resumeAction = { actionId };
      automateCatalogManager(result.prompt);
      return;
    }

    // Standard inputs required
    if (result.status === "input_required") {
      // Auto-confirm logic for standard prompt confirms (press enter to continue)
      if (result.prompt.type === "confirm" && !isAutomating) {
        window._resumeAction = { actionId };
        submitPromptValue("");
        return;
      }
      
      if (isAutomating) return;
      
      window._resumeAction = { actionId };
      showPrompt(result.prompt);
      if (result.state) renderArtistHUD(result.state);
      return;
    }
    
    // Action resolved successfully
    hidePrompt();
    hideConcertHUD();
    window._resumeAction = null;
    
    // Clear custom form automations
    window._songCreationState = null;
    window._beatCreationState = null;
    
    if (result.state) {
      renderArtistHUD(result.state);
    }
    if (actionId === 23) {
      triggerTabBackgroundAction(25); // Refresh Hot 100 in background
      loadNewReleasesWidget();
      renderBeatSalesFeed();
    }
    // Automatically refresh Beat Vault when producing beats, using store, managing vault, or progressing weeks
    if (actionId === 30 || actionId === 32 || actionId === 23 || actionId === 31) {
      refreshBeatVault().catch(() => {});
    }
  } catch (err) {
    appendLog(`Error: ${err.message}`);
    // Reset forms
    window._songCreationState = null;
    window._beatCreationState = null;
  }
}

function logsContainConcert(logs) {
  if (!logs) return false;
  const str = Array.isArray(logs) ? logs.join("\n") : String(logs);
  return str.includes("LIVE CONCERT") || 
         str.includes("Performing:") || 
         str.includes("What do you do?") || 
         str.includes("start the show") || 
         str.includes("resolve the week") ||
         str.includes("backstage") ||
         str.includes(">>") ||
         str.includes("venue") ||
         str.includes("Concert") ||
         str.includes("opener") ||
         str.includes("guest");
}

function parseAndShowCreationToasts(logs) {
  const fullText = logs.join("\n");
  
  // 1. Song Quality created toast & banner
  const songMatch = fullText.match(/Song created:\s*'([^']+)'/i);
  const songQualityMatch = fullText.match(/Computed quality:\s*([\d.]+)\/10/i);
  const songMetaMatch = fullText.match(/Genres:\s*(.*?)\s*\|\s*Theme:\s*(.*?)$/im);
  
  if (songMatch && songQualityMatch) {
    const title = songMatch[1];
    const quality = songQualityMatch[1];
    const genreText = songMetaMatch ? songMetaMatch[1] : "";
    const themeText = songMetaMatch ? songMetaMatch[2] : "";
    
    showToast(`🎵 Song Created!`, `"${title}" recorded with quality: ${quality}/10`, false);
    
    const banner = document.getElementById("last-creation-banner");
    if (banner) {
      banner.classList.remove("hidden");
      document.getElementById("banner-creation-title").textContent = title;
      document.getElementById("banner-creation-details").textContent = `Quality: ${quality}/10 · Genre: ${genreText || "N/A"} · Theme: ${themeText || "N/A"}`;
    }
  }
  
  // 2. Beat DAW quality created toast & banner
  const beatMatch = fullText.match(/Stored\s*'([^']+)'\s*in your Beat Vault \(([^)]+), ([\d.]+)\/10\)/i);
  if (beatMatch) {
    const title = beatMatch[1];
    const genre = beatMatch[2];
    const quality = beatMatch[3];
    
    showToast(`🎹 Beat DAW Produced!`, `"${title}" (${genre}) stored with quality: ${quality}/10`, true);
    
    const banner = document.getElementById("last-creation-banner");
    if (banner) {
      banner.classList.remove("hidden");
      document.getElementById("banner-creation-title").textContent = title;
      document.getElementById("banner-creation-details").textContent = `Quality: ${quality}/10 · Genre: ${genre} (Stored in Beat Vault)`;
    }
  }
  
  // 3. Course starting or complete toasts
  const courseStartMatch = fullText.match(/(Started a 12-week.*)/i);
  if (courseStartMatch) {
    showToast("📚 Course Started!", courseStartMatch[1], false);
  }
  const courseCompleteMatch = fullText.match(/(Course complete.*)/i);
  if (courseCompleteMatch) {
    showToast("🎓 Course Completed!", courseCompleteMatch[1], false);
  }
}

function appendLog(lines) {
  const out = document.getElementById("log-output");
  const text = Array.isArray(lines) ? lines.join("\n") : String(lines);
  if (text.trim()) {
    out.textContent = (out.textContent === "Simulator logs initialized. Run an action to display Python stdout stream." ? "" : out.textContent + "\n\n") + text;
    out.scrollTop = out.scrollHeight;
  }
}

// ==========================================================================
// CONCERT GAMEPLAY OVERLAY HUD
// ==========================================================================
function showConcertHUD(prompt, logs) {
  const overlay = document.getElementById("concert-overlay");
  overlay.classList.remove("hidden");
  
  const fullLogs = logs.join("\n");
  
  // 1. Parse Venue Name
  const venueMatch = fullLogs.match(/\*\s*LIVE CONCERT:\s*([^\n*]+?)\s*AT\s*([^\n*]+?)\s*\*/i) ||
                     fullLogs.match(/LIVE CONCERT:\s*([^\n*]+?)\s*AT\s*([^\n*]+)/i) || 
                     fullLogs.match(/performing at\s*([^\n.]+)/i);
  if (venueMatch) {
    document.getElementById("stage-venue-name").textContent = venueMatch[2] ? venueMatch[2].trim() : venueMatch[1].trim();
  }
  
  // 2. Parse Attendance
  const attMatch = fullLogs.match(/Attendance:\s*([\d,]+)/i);
  if (attMatch) {
    document.getElementById("stage-attendance").textContent = attMatch[1];
  }
  
  // 3. Parse Now Performing Song (Get last match)
  const songMatches = [...fullLogs.matchAll(/Performing:\s*'([^']+)'/gi)];
  if (songMatches.length > 0) {
    const lastSong = songMatches[songMatches.length - 1][1];
    document.getElementById("stage-song-name").textContent = lastSong;
  }
  
  // 4. Parse setlist index progress (Get last match)
  const progMatches = [...fullLogs.matchAll(/\[(\d+)\/(\d+)\]/g)];
  if (progMatches.length > 0) {
    const lastProg = progMatches[progMatches.length - 1];
    document.getElementById("stage-progress").textContent = `${lastProg[1]} / ${lastProg[2]}`;
  }
  
  // 5. Parse crowd energy (Get last match)
  const energyMatches = [...fullLogs.matchAll(/\[(#+)([-]+)\]/g)];
  if (energyMatches.length > 0) {
    const lastEnergy = energyMatches[energyMatches.length - 1];
    const hash = lastEnergy[1].length;
    const dash = lastEnergy[2].length;
    const total = hash + dash;
    const energyPct = Math.round((hash / total) * 100);
    document.getElementById("stage-energy-fill").style.width = `${energyPct}%`;
    document.getElementById("stage-energy-val").textContent = `${energyPct}%`;
  }
  
  // 6. Stage console stream log feed
  const feed = document.getElementById("stage-feed-body");
  feed.textContent = fullLogs;
  feed.scrollTop = feed.scrollHeight;
  
  // 7. Populate choice buttons
  const choicesDiv = document.getElementById("stage-choices");
  choicesDiv.innerHTML = "";
  
  function parseConcertChoices(lgs) {
    const opts = [];
    const full = Array.isArray(lgs) ? lgs.join("\n") : String(lgs);
    const lines = full.split(/\r?\n/);
    for (let line of lines) {
      const match = line.match(/^\s*\[(\d+)\]\s+(.*)$/);
      if (match) {
        opts.push({
          value: match[1],
          text: match[2].trim()
        });
      }
    }
    return opts;
  }
  
  const parsedChoices = parseConcertChoices(logs);
  if (parsedChoices.length > 0) {
    parsedChoices.forEach(choice => {
      const btn = document.createElement("button");
      btn.className = "btn secondary btn-large text-left";
      btn.innerHTML = `<strong>${choice.value}</strong> — ${escapeHtml(choice.text)}`;
      btn.addEventListener("click", () => submitPromptValue(choice.value));
      choicesDiv.appendChild(btn);
    });
  } else {
    if (prompt.type === "number") {
      choicesDiv.innerHTML = `
        <div class="form-group mb-3" style="width: 100%;">
          <label class="mb-2 d-block">${escapeHtml(prompt.label)}</label>
          <div class="d-flex gap-2">
            <input type="number" id="concert-prompt-input" class="form-control" min="${prompt.minimum ?? ""}" max="${prompt.maximum ?? ""}" value="${prompt.minimum ?? 0}" style="flex: 1; padding: 0.5rem;" />
            <button type="button" class="btn primary" id="btn-submit-concert-prompt">Submit</button>
          </div>
        </div>
      `;
      document.getElementById("btn-submit-concert-prompt").addEventListener("click", () => {
        const val = Number(document.getElementById("concert-prompt-input").value);
        submitPromptValue(val);
      });
    } else if (prompt.type === "text") {
      choicesDiv.innerHTML = `
        <div class="form-group mb-3" style="width: 100%;">
          <label class="mb-2 d-block">${escapeHtml(prompt.label)}</label>
          <div class="d-flex gap-2">
            <input type="text" id="concert-prompt-input" class="form-control" value="${escapeHtml(prompt.default || "")}" style="flex: 1; padding: 0.5rem;" />
            <button type="button" class="btn primary" id="btn-submit-concert-prompt">Submit</button>
          </div>
        </div>
      `;
      document.getElementById("btn-submit-concert-prompt").addEventListener("click", () => {
        const val = document.getElementById("concert-prompt-input").value;
        submitPromptValue(val);
      });
    } else if (prompt.type === "menu" || prompt.options) {
      prompt.options.forEach((opt, idx) => {
        const btn = document.createElement("button");
        btn.className = "btn secondary btn-large text-left";
        btn.textContent = opt;
        btn.addEventListener("click", () => submitPromptValue(idx + 1));
        choicesDiv.appendChild(btn);
      });
    } else {
      const btn = document.createElement("button");
      btn.className = "btn primary btn-large";
      btn.innerHTML = `<i data-lucide="play"></i> ${escapeHtml(prompt.label || "Continue Show")}`;
      btn.addEventListener("click", () => submitPromptValue(""));
      choicesDiv.appendChild(btn);
    }
  }
  
  lucide.createIcons();
}

function hideConcertHUD() {
  document.getElementById("concert-overlay").classList.add("hidden");
}

// ==========================================================================
// DYNAMIC PROMPT DIALOGS UI
// ==========================================================================
function showPrompt(prompt) {
  currentPrompt = prompt;
  const backdrop = document.getElementById("prompt-modal");
  const body = document.getElementById("prompt-body");
  const title = document.getElementById("prompt-title");
  
  backdrop.classList.remove("hidden");
  title.textContent = prompt.title || prompt.label || "Action Required";
  
  document.getElementById("btn-submit-prompt").classList.remove("hidden");
  document.getElementById("btn-cancel-prompt").classList.add("hidden");
  
  if (prompt.type === "menu") {
    body.innerHTML = `<ul class="menu-options" id="menu-list"></ul>`;
    const list = document.getElementById("menu-list");
    
    if (prompt.allow_cancel) {
      const li = document.createElement("li");
      const b = document.createElement("button");
      b.type = "button";
      b.innerHTML = `<i data-lucide="corner-up-left" style="width:14px;height:14px;display:inline-block;margin-right:0.25rem;"></i> Cancel / Exit`;
      b.addEventListener("click", () => submitPromptValue(0));
      li.appendChild(b);
      list.appendChild(li);
    }
    
    prompt.options.forEach((opt, i) => {
      const li = document.createElement("li");
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = opt;
      b.addEventListener("click", () => submitPromptValue(i + 1));
      li.appendChild(b);
      list.appendChild(li);
    });
    
    document.getElementById("btn-submit-prompt").classList.add("hidden");
  } else if (prompt.type === "number") {
    body.innerHTML = `
      <div class="form-group">
        <label>${escapeHtml(prompt.label)}</label>
        <input type="number" id="prompt-input" min="${prompt.minimum ?? ""}" max="${prompt.maximum ?? ""}" value="${prompt.minimum ?? 0}" />
      </div>
    `;
  } else if (prompt.type === "confirm") {
    body.innerHTML = `<p class="muted py-2 text-center">${escapeHtml(prompt.label || "Press confirm to continue.")}</p>`;
  } else {
    body.innerHTML = `
      <div class="form-group">
        <label>${escapeHtml(prompt.label || "Value")}</label>
        <input type="text" id="prompt-input" value="${escapeHtml(prompt.default || "")}" />
      </div>
    `;
  }
  
  lucide.createIcons();
}

function hidePrompt() {
  document.getElementById("prompt-modal").classList.add("hidden");
  currentPrompt = null;
}

function submitPromptValue(val) {
  pendingResponses.push(val);
  hidePrompt();
  if (window._resumeAction) {
    const { actionId } = window._resumeAction;
    window._resumeAction = null;
    runAction(actionId, true);
  }
}

// Confirm click listener
document.getElementById("btn-submit-prompt").addEventListener("click", () => {
  const inp = document.getElementById("prompt-input");
  if (!inp) {
    submitPromptValue("");
    return;
  }
  const val = currentPrompt?.type === "number" ? Number(inp.value) : inp.value;
  submitPromptValue(val);
});

// Close click
document.getElementById("btn-close-prompt").addEventListener("click", () => {
  hidePrompt();
  window._resumeAction = null;
  window._songCreationState = null;
  window._beatCreationState = null;
});

// ==========================================================================
// FORM SUBMIT INTERCEPTORS & AUTOMATIONS
// ==========================================================================

// Song Creation form submission
document.getElementById("form-create-song").addEventListener("submit", (e) => {
  e.preventDefault();
  
  const title = document.getElementById("song-title-input").value.trim();
  const genres = Array.from(document.querySelectorAll("#song-genre-selects input:checked")).map(el => el.value);
  const theme = document.getElementById("song-theme-select").value;
  const durationMins = Number(document.getElementById("song-duration-mins").value);
  const durationSecs = Number(document.getElementById("song-duration-secs").value);
  const beatName = document.getElementById("song-beat-select").value;
  const destination = document.getElementById("song-dest-select").value;
  
  const albumId = document.getElementById("album-draft-select").value;
  const newAlbumName = document.getElementById("album-new-title").value.trim();
  const newAlbumGenre = document.getElementById("album-new-genre").value;
  const newAlbumTheme = document.getElementById("album-new-theme").value;

  if (genres.length === 0) {
    alert("Please select at least 1 genre.");
    return;
  }
  
  const songSetup = {
    title,
    genres,
    theme,
    durationMins,
    durationSecs,
    beatId: beatName ? "yes" : "",
    beatName,
    destination,
    albumId,
    albumName: albumId !== "new" ? document.getElementById("album-draft-select").selectedOptions[0]?.textContent : "",
    newAlbumName,
    newAlbumGenre,
    newAlbumTheme
  };
  
  window._songCreationState = {
    step: 0,
    setup: songSetup,
    submittedGenres: []
  };
  
  // Start action 7
  runAction(7);
});

// Automated Song Creation CLI prompt resolver
function automateSongCreation(prompt) {
  const state = window._songCreationState;
  const setup = state.setup;
  
  // 1. Genre Count
  if (prompt.label && prompt.label.includes("How many genres")) {
    submitPromptValue(setup.genres.length);
    return;
  }
  
  // 2. Select specific genres
  if (prompt.title && prompt.title.includes("Pick song genre")) {
    const options = prompt.options;
    const nextGenre = setup.genres.find(g => !state.submittedGenres.includes(g));
    if (nextGenre) {
      const idx = options.indexOf(nextGenre);
      if (idx !== -1) {
        state.submittedGenres.push(nextGenre);
        submitPromptValue(idx + 1);
        return;
      }
    }
    submitPromptValue(1);
    return;
  }
  
  // 3. Theme
  if (prompt.title && prompt.title.includes("Pick theme")) {
    const idx = prompt.options.indexOf(setup.theme);
    submitPromptValue(idx !== -1 ? idx + 1 : 1);
    return;
  }
  
  // 4. Use beat
  if (prompt.title && prompt.title.includes("Use a beat from your Beat Vault?")) {
    submitPromptValue(setup.beatId ? 2 : 1);
    return;
  }
  
  // 5. Select Beat
  if (prompt.title && prompt.title.includes("Choose vault beat")) {
    const idx = prompt.options.findIndex(opt => opt.includes(setup.beatName));
    submitPromptValue(idx !== -1 ? idx + 1 : 1);
    return;
  }
  
  // 6. Keep song idea
  if (prompt.title && prompt.title.includes("Do you want to keep this song idea?")) {
    submitPromptValue(1); // Keep it
    return;
  }
  
  // 7. Name
  if (prompt.label && prompt.label.includes("Song name")) {
    submitPromptValue(setup.title || "New Track");
    return;
  }
  
  // 8. Minutes
  if (prompt.label && prompt.label.includes("Minutes")) {
    submitPromptValue(setup.durationMins);
    return;
  }
  
  // 9. Seconds
  if (prompt.label && prompt.label.includes("Seconds")) {
    submitPromptValue(setup.durationSecs);
    return;
  }
  
  // 10. Destination
  if (prompt.title && prompt.title.includes("Where should this song go?")) {
    submitPromptValue(setup.destination === "album" ? 1 : 2);
    return;
  }
  
  // 11. Choose album draft
  if (prompt.title && (prompt.title.includes("Choose album") || prompt.title.includes("Choose released album"))) {
    if (setup.albumId === "new") {
      const idx = prompt.options.findIndex(opt => opt.includes("New Album") || opt.includes("Create new"));
      submitPromptValue(idx !== -1 ? idx + 1 : 1);
    } else {
      const idx = prompt.options.findIndex(opt => opt.includes(setup.albumName));
      submitPromptValue(idx !== -1 ? idx + 1 : 1);
    }
    return;
  }
  
  // 12. New Album Title
  if (prompt.label && prompt.label.includes("New album name")) {
    submitPromptValue(setup.newAlbumName || "New Album");
    return;
  }
  
  // 13. New Album Genre
  if (prompt.title && prompt.title.includes("SELECT ALBUM CORE GENRE")) {
    const idx = prompt.options.indexOf(setup.newAlbumGenre);
    submitPromptValue(idx !== -1 ? idx + 1 : 1);
    return;
  }
  
  // 14. New Album Theme
  if (prompt.title && prompt.title.includes("SELECT ALBUM CORE THEME")) {
    const idx = prompt.options.indexOf(setup.newAlbumTheme);
    submitPromptValue(idx !== -1 ? idx + 1 : 1);
    return;
  }
  
  // Standard fallback
  showPrompt(prompt);
}

// Beat Creation DAW form submission
document.getElementById("form-create-beat").addEventListener("submit", (e) => {
  e.preventDefault();
  
  const name = document.getElementById("beat-name-input").value.trim();
  const genre = document.getElementById("beat-genre-select").value;
  
  window._beatCreationState = {
    name,
    genre
  };
  
  // Start DAW Action 30
  runAction(30);
});

// Automated Beat Creation resolver
function automateBeatCreation(prompt) {
  const setup = window._beatCreationState;
  
  // 1. Choose Genre
  if (prompt.title && prompt.title.includes("Choose beat genre")) {
    const idx = prompt.options.indexOf(setup.genre);
    submitPromptValue(idx !== -1 ? idx + 1 : 1);
    return;
  }
  
  // 2. What to do (Store in vault)
  if (prompt.title && prompt.title.includes("What do you want to do with this beat?")) {
    submitPromptValue(1); // Option 1: Store in Vault
    return;
  }
  
  // 3. Beat Name
  if (prompt.label && prompt.label.includes("Beat name")) {
    submitPromptValue(setup.name || "DAW Beat");
    return;
  }
  
  showPrompt(prompt);
}

// Duration randomizer dice button click
document.getElementById("btn-roll-duration").addEventListener("click", () => {
  const rand = Math.random();
  let totalSecs = 165; // 2:45 default
  
  if (rand < 0.70) {
    // 70% chance: typical song (2:00 to 3:45) -> 120s to 225s
    totalSecs = Math.floor(Math.random() * (225 - 120 + 1)) + 120;
  } else if (rand < 0.85) {
    // 15% chance: short song (1:01 to 1:59) -> 61s to 119s
    totalSecs = Math.floor(Math.random() * (119 - 61 + 1)) + 61;
  } else {
    // 15% chance: long song (3:46 to 8:59) -> 226s to 539s
    totalSecs = Math.floor(Math.random() * (539 - 226 + 1)) + 226;
  }
  
  const mins = Math.floor(totalSecs / 60);
  const secs = totalSecs % 60;
  
  document.getElementById("song-duration-mins").value = mins;
  document.getElementById("song-duration-secs").value = secs;
});

// Wizard Navigation
document.getElementById("btn-song-next").addEventListener("click", () => {
  const genres = Array.from(document.querySelectorAll("#song-genre-selects input:checked")).map(el => el.value);
  if (genres.length === 0) {
    alert("Please select at least 1 genre.");
    return;
  }
  if (genres.length > 2) {
    alert("Please select up to 2 genres.");
    return;
  }
  
  document.getElementById("song-step-1").classList.add("hidden");
  document.getElementById("song-step-2").classList.remove("hidden");
  
  document.getElementById("step-ind-1").classList.remove("active");
  document.getElementById("step-ind-2").classList.add("active");
});

document.getElementById("btn-song-back").addEventListener("click", () => {
  document.getElementById("song-step-2").classList.add("hidden");
  document.getElementById("song-step-1").classList.remove("hidden");
  
  document.getElementById("step-ind-2").classList.remove("active");
  document.getElementById("step-ind-1").classList.add("active");
});

// Critic reviews dropdown selector change listener
document.getElementById("sel-critic-review-album").addEventListener("change", (e) => {
  const storedHistory = localStorage.getItem("rapsim_reviews_history");
  if (storedHistory) {
    try {
      const history = JSON.parse(storedHistory);
      displaySelectedAlbumReview(e.target.value, history);
    } catch (err) {
      console.error(err);
    }
  }
});

// Catalog Manager Automation
function automateCatalogManager(prompt) {
  const state = window._catalogState;
  if (!state) return;
  
  const isMainMenu = (prompt.title && prompt.title.includes("Catalog options")) || 
                     (prompt.options && prompt.options.includes("View song metadata"));
                     
  if (isMainMenu) {
    if (!state.completed) {
      state.completed = true;
      submitPromptValue(state.action);
    } else {
      window._catalogState = null;
      submitPromptValue(6); // Back
    }
    return;
  }
  
  showPrompt(prompt);
}

// Song recording desk destination change triggers album block toggle
document.getElementById("song-dest-select").addEventListener("change", (e) => {
  const isAlbum = e.target.value === "album";
  const block = document.getElementById("new-album-fields");
  if (isAlbum) {
    block.classList.remove("hidden");
    updateAlbumDraftsList().catch(() => {});
  } else {
    block.classList.add("hidden");
  }
});

// Album draft select toggle new album creation fields
document.getElementById("album-draft-select").addEventListener("change", (e) => {
  const isNew = e.target.value === "new";
  const block = document.getElementById("create-album-inputs");
  if (isNew) {
    block.classList.remove("hidden");
  } else {
    block.classList.add("hidden");
  }
});

// Ratings filter selector change
document.getElementById("sel-ratings-chart").addEventListener("change", () => {
  loadUserRatings();
});

// Sync/Reload ratings click
document.getElementById("btn-load-ratings").addEventListener("click", () => {
  loadUserRatings();
});

// Shawtify streams sync button
document.getElementById("btn-load-shawtify").addEventListener("click", () => {
  loadShawtifyStreams();
});

// ==========================================================================
// STARTUP AND REGISTRATION SETUP
// ==========================================================================
async function loadMetaOptions() {
  metaOptions = await api("/api/meta/options");
  
  // Skills checkboxes (pick 2)
  const skillsDiv = document.getElementById("skills-checkboxes");
  skillsDiv.innerHTML = metaOptions.skills.map(s => `
    <label class="check-item">
      <input type="checkbox" name="skills" value="${escapeHtml(s)}" />
      <span>${escapeHtml(s)}</span>
    </label>
  `).join("");
  
  // Enforce checkbox limit of 2 for skills
  skillsDiv.addEventListener("change", () => {
    const checked = skillsDiv.querySelectorAll("input[type='checkbox']:checked");
    const unchecked = skillsDiv.querySelectorAll("input[type='checkbox']:not(:checked)");
    if (checked.length >= 2) {
      unchecked.forEach(cb => cb.disabled = true);
    } else {
      unchecked.forEach(cb => cb.disabled = false);
    }
  });
  
  // Genres checkboxes (pick 2)
  const genresDiv = document.getElementById("genres-checkboxes");
  genresDiv.innerHTML = metaOptions.genres.map(g => `
    <label class="check-item">
      <input type="checkbox" name="genres" value="${escapeHtml(g)}" />
      <span>${escapeHtml(g)}</span>
    </label>
  `).join("");
  
  // Enforce checkbox limit of 2 for genres
  genresDiv.addEventListener("change", () => {
    const checked = genresDiv.querySelectorAll("input[type='checkbox']:checked");
    const unchecked = genresDiv.querySelectorAll("input[type='checkbox']:not(:checked)");
    if (checked.length >= 2) {
      unchecked.forEach(cb => cb.disabled = true);
    } else {
      unchecked.forEach(cb => cb.disabled = false);
    }
  });
  
  updateSexualityOptions();
}

function updateSexualityOptions() {
  const gender = document.getElementById("sel-gender").value;
  const sel = document.getElementById("sel-sexuality");
  const opts = metaOptions?.sexualities?.[gender] || ["straight"];
  sel.innerHTML = opts.map((o) => `<option value="${escapeHtml(o)}">${escapeHtml(o)}</option>`).join("");
}

document.getElementById("sel-gender").addEventListener("change", updateSexualityOptions);

// Setup form start career
document.getElementById("form-new-game").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errEl = document.getElementById("new-error");
  errEl.classList.add("hidden");
  
  const fd = new FormData(e.target);
  
  const skills = Array.from(document.querySelectorAll("#skills-checkboxes input:checked")).map(el => el.value);
  const genres = Array.from(document.querySelectorAll("#genres-checkboxes input:checked")).map(el => el.value);
  
  if (skills.length > 2) {
    errEl.textContent = "Please select up to 2 skills.";
    errEl.classList.remove("hidden");
    return;
  }
  if (genres.length > 2) {
    errEl.textContent = "Please select up to 2 genres.";
    errEl.classList.remove("hidden");
    return;
  }
  
  try {
    // Clear reviews history and Hot 100 caches on starting new career
    localStorage.removeItem("rapsim_reviews_history");
    localStorage.removeItem("rapsim_latest_reviews");
    localStorage.removeItem("rapsim_cached_hot100");
    localStorage.removeItem("rapsim_beat_sales");
    const dashList = document.getElementById("dash-hot-list");
    if (dashList) {
      dashList.innerHTML = `<p class="muted text-center py-2 text-small">Simulate weeks or click Hot 100 Chart to sync ranking.</p>`;
    }
    const nrList = document.getElementById("dash-new-releases-list");
    if (nrList) {
      nrList.innerHTML = `<p class="muted text-small">No new releases dropped in the ecosystem this week. Simulate a week to check.</p>`;
    }
    if (dashList) {
      dashList.innerHTML = `<p class="muted text-center py-2 text-small">Simulate weeks or click Hot 100 Chart to sync ranking.</p>`;
    }
    const reviewsContainer = document.getElementById("critic-reviews-container");
    if (reviewsContainer) {
      reviewsContainer.innerHTML = `<p class="muted py-5 text-center">No reviews recorded in this session yet. Release music to view critic quotes.</p>`;
    }
    const selectorContainer = document.getElementById("critic-reviews-selector-container");
    if (selectorContainer) {
      selectorContainer.classList.add("hidden");
    }

    const result = await api("/api/session", {
      method: "POST",
      body: JSON.stringify({
        name: fd.get("name"),
        gender: fd.get("gender"),
        sexuality: fd.get("sexuality"),
        skills: skills.length ? skills : null,
        genres: genres.length ? genres : null,
      }),
    });
    
    sessionId = result.state.session_id;
    document.getElementById("log-output").textContent = "Career started successfully. Select a tab in the sidebar navigation.";
    
    renderArtistHUD(result.state);
    showScreen("screen-game");
    switchTab("dashboard");
  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.remove("hidden");
  }
});

// Restore existing session
async function restoreSession() {
  if (!sessionId) {
    showScreen("screen-new");
    await loadMetaOptions();
    return;
  }
  
  try {
    const state = await api(`/api/session/${sessionId}`);
    renderArtistHUD(state);
    showScreen("screen-game");
    switchTab("dashboard");
    loadNewReleasesWidget();
    
    loadMetaOptions().catch(() => {});
  } catch (err) {
    console.warn("Could not restore session:", err.message);
    localStorage.removeItem("rapsim_session_id");
    sessionId = null;
    showScreen("screen-new");
    await loadMetaOptions();
  }
}

// ==========================================================================
// BIND GLOBAL ACTIONS CONTROLS
// ==========================================================================

// Nav item tab buttons click
document.querySelectorAll(".nav-item").forEach(btn => {
  btn.addEventListener("click", () => {
    const tab = btn.getAttribute("data-tab");
    switchTab(tab);
  });
});

// Simulate Week
document.getElementById("btn-sim-week").addEventListener("click", () => runAction(23));
document.getElementById("btn-dash-sim-week").addEventListener("click", () => runAction(23));

// Refresh DAW vault
document.getElementById("btn-refresh-vault").addEventListener("click", refreshBeatVault);

// General action buttons click listener
document.querySelectorAll("[data-action]").forEach(btn => {
  // Prevent form submits or double binding for tab/automated actions
  if (
    btn.id === "run-catalog-manager" || 
    btn.id === "form-create-song" || 
    btn.id === "form-create-beat" ||
    btn.id === "btn-load-news" ||
    btn.id === "btn-load-grammys" ||
    btn.id === "btn-refresh-twitter" ||
    btn.id === "btn-load-disstracks" ||
    btn.id === "btn-open-beat-store-studio" ||
    btn.id === "btn-open-beat-store-tab" ||
    btn.id === "btn-load-ratings" ||
    btn.id === "btn-load-shawtify" ||
    btn.id === "btn-run-beat-vault"
  ) return;
  
  btn.addEventListener("click", () => {
    const act = Number(btn.getAttribute("data-action"));
    runAction(act);
  });
});

// Explicit tab reload / load action bindings
document.getElementById("btn-load-news").addEventListener("click", loadNewsFeed);
document.getElementById("btn-load-grammys").addEventListener("click", loadGrammyAwards);
document.getElementById("btn-refresh-twitter").addEventListener("click", loadTwitterFeed);
document.getElementById("btn-load-disstracks").addEventListener("click", loadDissTracksFeed);
const storeStudio = document.getElementById("btn-open-beat-store-studio");
if (storeStudio) storeStudio.addEventListener("click", () => runAction(32));
const storeTab = document.getElementById("btn-open-beat-store-tab");
if (storeTab) storeTab.addEventListener("click", () => runAction(32));
document.getElementById("btn-load-ratings").addEventListener("click", loadUserRatings);
document.getElementById("btn-load-shawtify").addEventListener("click", loadShawtifyStreams);

// Beat Vault Menu (Action 31) click listener
const btnRunVault = document.getElementById("btn-run-beat-vault");
if (btnRunVault) btnRunVault.addEventListener("click", () => runAction(31));

// Restart career / New Career click listener
const btnRestart = document.getElementById("btn-restart-career");
if (btnRestart) {
  btnRestart.addEventListener("click", () => {
    if (confirm("Are you sure you want to restart your career? Your current progress will be lost.")) {
      localStorage.removeItem("rapsim_session_id");
      sessionId = null;
      showScreen("screen-new");
      loadMetaOptions().catch((err) => console.error(err));
    }
  });
}

// Catalog tab quick action bindings
document.getElementById("btn-cat-view-details").addEventListener("click", () => {
  window._catalogState = { action: 1, completed: false };
  runAction(21);
});
document.getElementById("btn-cat-view-tracklist").addEventListener("click", () => {
  window._catalogState = { action: 2, completed: false };
  runAction(21);
});
document.getElementById("btn-run-catalog-manager").addEventListener("click", () => {
  window._catalogState = null; // Manual menu mode
  runAction(21);
});
document.getElementById("btn-cat-add-to-album").addEventListener("click", () => {
  window._catalogState = { action: 4, completed: false };
  runAction(21);
});
document.getElementById("btn-cat-send-feature").addEventListener("click", () => {
  window._catalogState = { action: 5, completed: false };
  runAction(21);
});
document.getElementById("btn-cat-delete").addEventListener("click", () => {
  window._catalogState = { action: 3, completed: false };
  runAction(21);
});

// Beat vault overlay display click (Deprecated)

// Collapsible Console
const consolePane = document.getElementById("console-pane");
document.getElementById("console-header").addEventListener("click", (e) => {
  if (e.target.closest("#btn-console-clear")) return;
  
  const icon = document.getElementById("console-chevron");
  if (consolePane.classList.contains("collapsed")) {
    consolePane.classList.remove("collapsed");
    icon.setAttribute("data-lucide", "chevron-down");
  } else {
    consolePane.classList.add("collapsed");
    icon.setAttribute("data-lucide", "chevron-up");
  }
  lucide.createIcons();
});

document.getElementById("btn-console-clear").addEventListener("click", () => {
  document.getElementById("log-output").textContent = "";
});

// Initialize on load
document.addEventListener("DOMContentLoaded", () => {
  restoreSession().catch((err) => console.error(err));
});
