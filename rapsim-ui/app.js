const API = "";

let sessionId = null;
let pendingResponses = [];
let currentPrompt = null;
let metaOptions = null;

async function api(path, options = {}) {
  const res = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || res.statusText || "Request failed");
  return data;
}

function showScreen(id) {
  document.querySelectorAll(".screen").forEach((el) => el.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}

function money(n) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(1)}K`;
  return `$${Math.round(n)}`;
}

function renderArtist(state) {
  const a = state.artist;
  const panel = document.getElementById("artist-panel");
  const skills = Object.entries(a.skills)
    .map(([k, v]) => `${k}: ${v}`)
    .join(" · ");
  const genres = Object.entries(a.genres)
    .map(([k, v]) => `${k} ${v}`)
    .join(" · ");
  panel.innerHTML = `
    <h2>${escapeHtml(a.name)}</h2>
    <div class="stat-row"><span>Year / Week</span><strong>${a.year} / ${a.week}</strong></div>
    <div class="stat-row"><span>Popularity</span><strong>${a.popularity}%</strong></div>
    <div class="meter"><span style="width:${Math.min(100, a.popularity)}%"></span></div>
    <div class="stat-row"><span>Reputation</span><strong>${a.reputation}%</strong></div>
    ${
      a.live_performance_rating > 0
        ? `<div class="stat-row"><span>Live Perf</span><strong>${a.live_performance_rating}/100</strong></div>`
        : ""
    }
    <div class="stat-row"><span>Health</span><strong>${a.health}%</strong></div>
    <div class="stat-row"><span>Fatigue</span><strong>${a.fatigue}%</strong></div>
    <div class="stat-row"><span>Money</span><strong>${money(a.money)}</strong></div>
    ${
      a.current_love
        ? `<div class="stat-row"><span>Love</span><strong>${escapeHtml(a.current_love.partner)} · ${a.current_love.lovingness}%</strong></div>
           <div class="meter love-meter"><span style="width:${Math.min(100, a.current_love.lovingness)}%"></span></div>`
        : `<div class="stat-row"><span>Love</span><strong>Single</strong></div>`
    }
    <div class="stat-row"><span>Vault beats</span><strong>${a.vault_beats}</strong></div>
    <div class="stat-row"><span>Drafts</span><strong>${a.unreleased_singles} singles · ${a.album_drafts} albums</strong></div>
    ${
      (a.owned_operational_venues > 0 || a.owned_construction_venues > 0)
        ? `<div class="stat-row"><span>Owned Venues</span><strong>${a.owned_operational_venues} active · ${a.owned_construction_venues} building</strong></div>`
        : ""
    }
    <p style="margin-top:0.75rem;font-size:0.75rem;color:var(--muted)">${escapeHtml(skills)}</p>
    <p style="font-size:0.75rem;color:var(--muted)">${escapeHtml(genres)}</p>
  `;
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderActions(actions) {
  const nav = document.getElementById("action-nav");
  const byCat = {};
  for (const act of actions) {
    if (!byCat[act.category]) byCat[act.category] = [];
    byCat[act.category].push(act);
  }
  nav.innerHTML = "";
  for (const [cat, items] of Object.entries(byCat)) {
    const group = document.createElement("div");
    group.className = "action-group";
    group.innerHTML = `<h4>${escapeHtml(cat)}</h4>`;
    for (const act of items) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "action-btn";
      btn.textContent = `${act.id}. ${act.label}`;
      btn.addEventListener("click", () => runAction(act.id));
      group.appendChild(btn);
    }
    nav.appendChild(group);
  }
}

function appendLog(lines) {
  const out = document.getElementById("log-output");
  const text = Array.isArray(lines) ? lines.join("\n") : String(lines);
  if (text.trim()) {
    out.textContent = (out.textContent === "Run an action from the sidebar." ? "" : out.textContent + "\n\n") + text;
    out.scrollTop = out.scrollHeight;
  }
}

function showPrompt(prompt) {
  currentPrompt = prompt;
  const panel = document.getElementById("prompt-panel");
  const body = document.getElementById("prompt-body");
  const title = document.getElementById("prompt-title");
  panel.classList.remove("hidden");
  title.textContent = prompt.title || prompt.label || "Input needed";

  if (prompt.type === "menu") {
    body.innerHTML = `<ul class="menu-options" id="menu-list"></ul>`;
    const list = document.getElementById("menu-list");
    if (prompt.allow_cancel) {
      const li = document.createElement("li");
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = "0. Cancel";
      b.addEventListener("click", () => submitPromptValue(0));
      li.appendChild(b);
      list.appendChild(li);
    }
    prompt.options.forEach((opt, i) => {
      const li = document.createElement("li");
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = `${i + 1}. ${opt}`;
      b.addEventListener("click", () => submitPromptValue(i + 1));
      li.appendChild(b);
      list.appendChild(li);
    });
    document.getElementById("btn-submit-prompt").classList.add("hidden");
  } else if (prompt.type === "number") {
    body.innerHTML = `<label>${escapeHtml(prompt.label)}<input type="number" id="prompt-input" /></label>`;
    const inp = document.getElementById("prompt-input");
    if (prompt.minimum != null) inp.min = prompt.minimum;
    if (prompt.maximum != null) inp.max = prompt.maximum;
    document.getElementById("btn-submit-prompt").classList.remove("hidden");
  } else {
    body.innerHTML = `<label>${escapeHtml(prompt.label || "Value")}<input type="text" id="prompt-input" value="${escapeHtml(prompt.default || "")}" /></label>`;
    document.getElementById("btn-submit-prompt").classList.remove("hidden");
  }
}

function hidePrompt() {
  document.getElementById("prompt-panel").classList.add("hidden");
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

document.getElementById("btn-submit-prompt").addEventListener("click", () => {
  const inp = document.getElementById("prompt-input");
  if (!inp) return;
  const val = currentPrompt?.type === "number" ? Number(inp.value) : inp.value;
  submitPromptValue(val);
});

async function runAction(actionId, isResume = false) {
  if (!sessionId) return;
  if (actionId === 39) {
    if (!confirm("Quit this career session?")) return;
  }
  document.querySelectorAll(".action-btn").forEach((b) => (b.disabled = true));
  if (!isResume) {
    pendingResponses = [];
  }
  try {
    const body = { action_id: actionId, responses: pendingResponses.length ? pendingResponses : null };
    const result = await api(`/api/session/${sessionId}/action`, {
      method: "POST",
      body: JSON.stringify(body),
    });

    if (result.logs?.length) appendLog(result.logs);

    if (result.status === "quit") {
      sessionId = null;
      showScreen("screen-new");
      document.getElementById("log-output").textContent = "Session ended.";
      return;
    }

    if (result.status === "input_required") {
      window._resumeAction = { actionId };
      showPrompt(result.prompt);
      if (result.state) {
        renderArtist(result.state);
      }
      return;
    }

    hidePrompt();
    window._resumeAction = null;
    if (result.state) {
      renderArtist(result.state);
      document.getElementById("session-label").textContent = `Week ${result.state.artist.week}`;
    }
  } catch (err) {
    appendLog(`Error: ${err.message}`);
  } finally {
    document.querySelectorAll(".action-btn").forEach((b) => (b.disabled = false));
  }
}

async function loadMeta() {
  metaOptions = await api("/api/meta/options");
  const skillSel = document.getElementById("sel-skills");
  const genreSel = document.getElementById("sel-genres");
  skillSel.innerHTML = metaOptions.skills.map((s) => `<option value="${escapeHtml(s)}">${escapeHtml(s)}</option>`).join("");
  genreSel.innerHTML = metaOptions.genres.map((g) => `<option value="${escapeHtml(g)}">${escapeHtml(g)}</option>`).join("");
  updateSexualityOptions();
}

function updateSexualityOptions() {
  const gender = document.getElementById("sel-gender").value;
  const sel = document.getElementById("sel-sexuality");
  const opts = metaOptions?.sexualities?.[gender] || ["straight"];
  sel.innerHTML = opts.map((o) => `<option value="${escapeHtml(o)}">${escapeHtml(o)}</option>`).join("");
}

document.getElementById("sel-gender").addEventListener("change", updateSexualityOptions);

document.getElementById("form-new-game").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errEl = document.getElementById("new-error");
  errEl.classList.add("hidden");
  const fd = new FormData(e.target);
  const skills = [...document.getElementById("sel-skills").selectedOptions].map((o) => o.value);
  const genres = [...document.getElementById("sel-genres").selectedOptions].map((o) => o.value);
  try {
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
    document.getElementById("log-output").textContent = "Career started. Pick an action.";
    renderArtist(result.state);
    renderActions(result.state.actions);
    showScreen("screen-game");
    document.getElementById("session-label").textContent = sessionId.slice(0, 8) + "…";
  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.remove("hidden");
  }
});

document.getElementById("btn-refresh").addEventListener("click", async () => {
  if (!sessionId) return;
  const state = await api(`/api/session/${sessionId}`);
  renderArtist(state);
});

document.getElementById("btn-vault").addEventListener("click", async () => {
  if (!sessionId) return;
  const data = await api(`/api/session/${sessionId}/vault`);
  if (!data.beats.length) {
    appendLog("Vault is empty.");
    return;
  }
  appendLog(
    "Beat Vault:\n" +
      data.beats
        .map((b) => `• ${b.name} | ${b.genre} | ${b.quality}/10${b.consumed ? " (used)" : ""}`)
        .join("\n")
  );
});

loadMeta().catch((err) => console.error(err));
