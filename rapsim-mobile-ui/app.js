/**
 * RapSim Mobile UI - Skeuomorphic Application Logic
 * Supports 9:16 aspect ratio preview, tactile 3D mechanical keys,
 * grooved vinyl disc catalog, and studio transport console.
 */

// --- Album Cover Assets Pool (from rapsim/album covers) ---
const ALBUM_COVERS = [
  "album covers/download (2).jpg",
  "album covers/download (3).jpg",
  "album covers/download (4).jpg",
  "album covers/download (5).jpg",
  "album covers/download (6).jpg",
  "album covers/download (7).jpg",
  "album covers/download (8).jpg",
  "album covers/download (9).jpg",
  "album covers/download (10).jpg",
  "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg",
  "album covers/Music artwork for Frank Ocean - _.jpg",
  "album covers/Tyler Durden.jpg"
];

function getRandomAlbumCover() {
  return ALBUM_COVERS[Math.floor(Math.random() * ALBUM_COVERS.length)];
}

// --- Shawtify Discography Database (Player + Industry Artists) ---
const SHAWTIFY_CATALOG = [
  // Lil Synapse (Player)
  {
    id: "ls-1",
    title: "Neon Dreams",
    artist: "Lil Synapse",
    album: "Neon Dreams (Single)",
    type: "Single",
    duration: "2:48",
    streams: "124,850,210",
    labelColor: "#CE6A6B",
    cover: "album covers/download (10).jpg",
    year: "2026",
    isYours: true,
    cert: "2x Platinum"
  },
  {
    id: "ls-2",
    title: "Chrome Heart Boulevard",
    artist: "Lil Synapse",
    album: "Midnight Sessions",
    type: "Single",
    duration: "3:14",
    streams: "88,412,900",
    labelColor: "#326280",
    cover: "album covers/download (5).jpg",
    year: "2026",
    isYours: true,
    cert: "Platinum"
  },
  {
    id: "ls-3",
    title: "Midnight In Tokyo (feat. Kenzo)",
    artist: "Lil Synapse",
    album: "Midnight Sessions",
    type: "Single",
    duration: "3:02",
    streams: "52,190,440",
    labelColor: "#EBACA2",
    cover: "album covers/download (6).jpg",
    year: "2025",
    isYours: true,
    cert: "Gold"
  },
  {
    id: "ls-4",
    title: "Ghostwriter Blues",
    artist: "Lil Synapse",
    album: "Unfinished Business",
    type: "Track",
    duration: "2:36",
    streams: "31,500,120",
    labelColor: "#212E53",
    cover: "album covers/download (7).jpg",
    year: "2025",
    isYours: true,
    cert: "Gold"
  },
  {
    id: "ls-5",
    title: "Fast Cash Slow Love",
    artist: "Lil Synapse",
    album: "Unfinished Business",
    type: "Track",
    duration: "2:55",
    streams: "19,820,600",
    labelColor: "#a9494a",
    cover: "album covers/download (8).jpg",
    year: "2025",
    isYours: true,
    cert: "Trending"
  },
  {
    id: "ls-6",
    title: "Subway Freestyles (Demo)",
    artist: "Lil Synapse",
    album: "Bedroom Tapes",
    type: "Demo",
    duration: "2:10",
    streams: "6,410,000",
    labelColor: "#FFDFCB",
    cover: "album covers/download (9).jpg",
    year: "2024",
    isYours: true,
    cert: ""
  },

  // Drakeo V (Industry)
  {
    id: "dv-1",
    title: "Midnight Dynasty",
    artist: "Drakeo V",
    album: "Midnight Dynasty",
    type: "Album",
    duration: "44:12",
    streams: "210,400,000",
    labelColor: "#151d34",
    cover: "album covers/Tyler Durden.jpg",
    year: "2026",
    isYours: false,
    cert: "Platinum"
  },
  {
    id: "dv-2",
    title: "Diamond Fangs",
    artist: "Drakeo V",
    album: "Midnight Dynasty",
    type: "Single",
    duration: "3:10",
    streams: "94,100,500",
    labelColor: "#326280",
    cover: "album covers/download (2).jpg",
    year: "2026",
    isYours: false,
    cert: "Gold"
  },
  {
    id: "dv-3",
    title: "Penthouse Views",
    artist: "Drakeo V",
    album: "Luxury & Paranoia",
    type: "Single",
    duration: "3:30",
    streams: "142,000,000",
    labelColor: "#EBACA2",
    cover: "album covers/download (3).jpg",
    year: "2025",
    isYours: false,
    cert: "Platinum"
  },

  // SZAria (Industry)
  {
    id: "sz-1",
    title: "Velvet Waves",
    artist: "SZAria",
    album: "Velvet Waves (Single)",
    type: "Single",
    duration: "3:42",
    streams: "76,320,000",
    labelColor: "#CE6A6B",
    cover: "album covers/Music artwork for Frank Ocean - _.jpg",
    year: "2026",
    isYours: false,
    cert: "Gold"
  },
  {
    id: "sz-2",
    title: "Ocean Lavender",
    artist: "SZAria",
    album: "Solitude",
    type: "Album",
    duration: "48:30",
    streams: "318,000,000",
    labelColor: "#224358",
    cover: "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg",
    year: "2025",
    isYours: false,
    cert: "3x Platinum"
  },

  // GrimKidd (Industry)
  {
    id: "gk-1",
    title: "Subzero",
    artist: "GrimKidd",
    album: "Subzero EP",
    type: "EP",
    duration: "18:40",
    streams: "48,900,000",
    labelColor: "#326280",
    cover: "album covers/download (4).jpg",
    year: "2026",
    isYours: false,
    cert: "Gold"
  },
  {
    id: "gk-2",
    title: "Balaclava Drill",
    artist: "GrimKidd",
    album: "Subzero EP",
    type: "Single",
    duration: "2:50",
    streams: "34,200,000",
    labelColor: "#111726",
    cover: "album covers/download (5).jpg",
    year: "2026",
    isYours: false,
    cert: ""
  },

  // Kenny Knox (Industry)
  {
    id: "kk-1",
    title: "Concrete Garden",
    artist: "Kenny Knox",
    album: "Concrete Garden",
    type: "Album",
    duration: "52:10",
    streams: "112,000,000",
    labelColor: "#a9494a",
    cover: "album covers/download (6).jpg",
    year: "2026",
    isYours: false,
    cert: "Platinum"
  }
];

let activeArtistFilter = "all";

// --- Tab Switching Logic (Console Transport Bay) ---
function switchTab(tabName) {
  // If switching to studio tab, always reset subpages to show the Studio Main Hub!
  if (tabName === "studio") {
    closeStudioSubpage();
  }

  const screens = {
    home: document.getElementById("screenHome"),
    media: document.getElementById("screenMedia"),
    studio: document.getElementById("screenStudio"),
    social: document.getElementById("screenSocial"),
    profile: document.getElementById("screenProfile"),
    setting: document.getElementById("screenSetting"),
    create: document.getElementById("screenCreate"),
    release: document.getElementById("screenRelease"),
    catalogue: document.getElementById("screenCatalogue")
  };

  Object.keys(screens).forEach(key => {
    if (screens[key]) {
      if (key === tabName) {
        screens[key].classList.add("active");
        screens[key].scrollTop = 0;
        if (key === "release") renderReleaseList();
        if (key === "catalogue") renderCatalogueFull();
      } else {
        screens[key].classList.remove("active");
      }
    }
  });

  // Update transport buttons & jewel lights (create tab highlights studio button)
  const activeNavKey = (tabName === "create" || tabName === "release" || tabName === "catalogue") ? "studio" : tabName;
  const navButtons = document.querySelectorAll(".nav-tab-btn");
  navButtons.forEach(btn => {
    if (btn.getAttribute("data-tab") === activeNavKey) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  playMechanicalClick();
}

// --- Media Sub-tab Switching Logic (Physical Selector) ---
function switchMediaSubtab(subtabName) {
  const subtabs = {
    news: document.getElementById("viewNews"),
    hot100: document.getElementById("viewHot100"),
    twitter: document.getElementById("viewTwitter"),
    shawtify: document.getElementById("viewShawtify"),
    critics: document.getElementById("viewCritics")
  };

  Object.keys(subtabs).forEach(key => {
    if (subtabs[key]) {
      if (key === subtabName) {
        subtabs[key].classList.add("active");
      } else {
        subtabs[key].classList.remove("active");
      }
    }
  });

  const subtabButtons = document.querySelectorAll(".media-subtab-btn");
  subtabButtons.forEach(btn => {
    if (btn.getAttribute("data-subtab") === subtabName) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  playMechanicalClick();

  if (subtabName === "shawtify") {
    renderShawtifyCatalog();
  }
}

// --- Shawtify Discography Engine (Grooved Vinyl Cards) ---
function renderShawtifyCatalog(filteredList = null) {
  const container = document.getElementById("shawtifyCatalog");
  if (!container) return;

  let items = filteredList || SHAWTIFY_CATALOG;

  if (activeArtistFilter !== "all" && !filteredList) {
    items = SHAWTIFY_CATALOG.filter(item => 
      item.artist.toLowerCase() === activeArtistFilter.toLowerCase()
    );
  }

  if (items.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 24px 10px; color: var(--text-muted);">
        <p style="font-weight: 800; font-size: 0.84rem; color: var(--c-navy);">No Vinyl Master Found</p>
        <p style="font-size: 0.72rem;">Try searching another artist or track name.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = items.map(item => `
    <div class="release-card" onclick="simulatePlaySong('${item.title} - ${item.artist}')">
      <div class="release-card-cover-wrap">
        <img src="${item.cover || getRandomAlbumCover()}" class="release-card-cover-art" alt="${item.title}">
      </div>
      <div class="vinyl-disc" style="width: 32px; height: 32px; margin-left: -12px; z-index: 1;">
        <div class="vinyl-label" style="background: ${item.labelColor}; width: 14px; height: 14px;">
          <div class="vinyl-spindle-hole" style="width: 3px; height: 3px;"></div>
        </div>
      </div>
      <div class="release-details">
        <h4>${item.title}</h4>
        <p>${item.artist}</p>
        <div class="release-meta-row">
          <span>${item.type} &bull; ${item.year}</span>
          <span style="color: var(--c-coral-dark); font-weight: 800;">${item.streams} spins</span>
          ${item.isYours ? '<span class="skeuo-pill coral" style="font-size: 0.55rem; padding: 1px 5px;">YOUR TRACK</span>' : ''}
          ${item.cert ? `<span class="foil-stamp ${item.cert.includes('Platinum') ? 'foil-platinum' : 'foil-gold'}" style="font-size: 0.52rem; padding: 1px 4px;">${item.cert}</span>` : ''}
        </div>
      </div>
      <button class="skeuo-btn skeuo-btn-icon" style="width: 30px; height: 30px; flex-shrink: 0;" title="Play Reel">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
          <polygon points="5 3 19 12 5 21 5 3"/>
        </svg>
      </button>
    </div>
  `).join("");
}

// Search bar filter for Shawtify
function filterShawtifyReleases() {
  const query = (document.getElementById("shawtifySearch")?.value || "").toLowerCase().trim();
  
  if (!query) {
    renderShawtifyCatalog();
    return;
  }

  const matches = SHAWTIFY_CATALOG.filter(item => 
    item.title.toLowerCase().includes(query) ||
    item.artist.toLowerCase().includes(query) ||
    item.album.toLowerCase().includes(query)
  );

  renderShawtifyCatalog(matches);
}

// Artist Pill Tag Filter
function filterByArtist(artistName, element) {
  activeArtistFilter = artistName;

  const searchInput = document.getElementById("shawtifySearch");
  if (searchInput) searchInput.value = "";

  const pills = document.querySelectorAll(".shawtify-pill");
  pills.forEach(p => p.classList.remove("active"));
  if (element) element.classList.add("active");

  playMechanicalClick();
  renderShawtifyCatalog();
}

// --- Critics Filter Engine ---
function filterCritics(category, element) {
  const reviewCards = document.querySelectorAll(".critic-review-card");
  
  reviewCards.forEach(card => {
    const cardCat = card.getAttribute("data-category");
    if (category === "all") {
      card.style.display = "block";
    } else if (category === "yours" && cardCat === "yours") {
      card.style.display = "block";
    } else if (category === "industry" && cardCat === "industry") {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });

  const buttons = document.querySelectorAll(".critics-filter-row .skeuo-pill");
  buttons.forEach(btn => btn.classList.remove("active"));
  if (element) element.classList.add("active");

  playMechanicalClick();
}

// --- Audio Playback Simulation with Studio On-Air Banner ---
function simulatePlaySong(songTitle) {
  playMechanicalClick();
  showToast(`🔴 ON AIR: Playing "${songTitle}" on Shawtify Reel`);
}

// Like/Retweet Button Reactions
function likeTweet(btn) {
  btn.style.color = "var(--c-coral-dark)";
  playMechanicalClick();
  showToast("Reaction recorded on social feed");
}

// Toast notification helper
let toastTimeout = null;
function showToast(message) {
  const toast = document.getElementById("toastMsg");
  if (!toast) return;

  toast.textContent = message;
  toast.classList.add("show");

  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 2400);
}

// Toggle Skeuomorphic Rocker Switch
function toggleSwitch(element) {
  element.classList.toggle("on");
  playMechanicalClick();
}

// Optional synthesized mechanical tactile click sound
let audioCtx = null;
function playMechanicalClick() {
  try {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) audioCtx = new AudioContext();
    }
    if (audioCtx && audioCtx.state === "running") {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "triangle";
      osc.frequency.setValueAtTime(140, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.03);
      gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.03);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.03);
    }
  } catch (e) {
    // Silent fallback
  }
}

// Status Bar Real-time Clock
function updateClock() {
  const now = new Date();
  let hours = now.getHours();
  const minutes = now.getMinutes();
  hours = hours % 12;
  hours = hours ? hours : 12;
  const minFormatted = minutes < 10 ? "0" + minutes : minutes;
  const timeStr = `${hours}:${minFormatted}`;

  const clockEl = document.getElementById("statusBarTime");
  if (clockEl) clockEl.textContent = timeStr;

  const spotifyClock = document.getElementById("spotifyPhoneClock");
  if (spotifyClock) spotifyClock.textContent = timeStr;
}

// Frame Toggle for Testing
function setupFrameToggle() {
  const toggleBtn = document.getElementById("toggleFrameBtn");
  const stage = document.getElementById("stageContainer");

  if (toggleBtn && stage) {
    toggleBtn.addEventListener("click", () => {
      stage.classList.toggle("full-mode");
      if (stage.classList.contains("full-mode")) {
        toggleBtn.textContent = "Exit Fullscreen (9:16)";
      } else {
        toggleBtn.textContent = "Toggle Frame";
      }
      playMechanicalClick();
    });
  }
}

// --- Home Page Interactive Modals & Routing ---
function openWeeklyNewsModal() {
  playMechanicalClick();
  const modal = document.getElementById("weeklyNewsModal");
  if (modal) modal.classList.add("active");
}

function closeWeeklyNewsModal() {
  playMechanicalClick();
  const modal = document.getElementById("weeklyNewsModal");
  if (modal) modal.classList.remove("active");
}

function openInboxModal() {
  playMechanicalClick();
  const modal = document.getElementById("inboxModal");
  if (modal) modal.classList.add("active");
}

function closeInboxModal() {
  playMechanicalClick();
  const modal = document.getElementById("inboxModal");
  if (modal) modal.classList.remove("active");
}

// --- Analyze App Launcher Logic (IMDb, Shawtify, Critiq, Slander) ---
let appNavOrigin = "media";

function openAnalyzeApp(appName, origin = "media") {
  playMechanicalClick();
  appNavOrigin = origin;

  if (appName === "shawtify") {
    openShawtifyApp("you");
    return;
  }

  const screenMedia = document.getElementById("screenMedia");
  const screenSocial = document.getElementById("screenSocial");
  if (origin === "social") {
    if (screenSocial) screenSocial.classList.remove("active");
    if (screenMedia) screenMedia.classList.add("active");
  }

  const hub = document.getElementById("mediaMainHub");
  if (hub) hub.style.display = "none";

  // Update back buttons text
  document.querySelectorAll(".analyze-subpage-view .app-back-btn").forEach(btn => {
    btn.innerHTML = origin === "social" ? "&lsaquo; Back to Socials" : "&lsaquo; Back to Media";
  });

  const allApps = ["imdb", "critiq", "slander"];
  allApps.forEach(app => {
    const el = document.getElementById(`appView_${app}`);
    if (el) {
      if (app === appName) {
        el.style.display = "flex";
        el.scrollTop = 0;
      } else {
        el.style.display = "none";
      }
    }
  });
}

function closeAnalyzeApp() {
  playMechanicalClick();
  const shawtifyApp = document.getElementById("appView_shawtify");
  if (shawtifyApp && shawtifyApp.style.display !== "none") {
    closeShawtifyApp();
    return;
  }
  const mainBottomNav = document.querySelector(".bottom-nav-bar");
  if (mainBottomNav) mainBottomNav.style.display = "flex";
  const allApps = ["imdb", "critiq", "slander"];
  allApps.forEach(app => {
    const el = document.getElementById(`appView_${app}`);
    if (el) el.style.display = "none";
  });

  if (appNavOrigin === "social") {
    switchTab("social");
    const socialHub = document.getElementById("socialMainHub");
    if (socialHub) socialHub.style.display = "flex";
  } else {
    const hub = document.getElementById("mediaMainHub");
    if (hub) hub.style.display = "flex";
  }
  appNavOrigin = "media";
}

function routeToNews() {
  playMechanicalClick();
  switchTab("media");
  openAnalyzeApp("slander");
}

function openHot100ChartModal() {
  playMechanicalClick();
  const modal = document.getElementById("hot100ChartModal");
  if (modal) modal.classList.add("active");
}

function closeHot100ChartModal() {
  playMechanicalClick();
  const modal = document.getElementById("hot100ChartModal");
  if (modal) modal.classList.remove("active");
}

function routeToHot100() {
  playMechanicalClick();
  openHot100ChartModal();
}

let careerWeek = 24;
let careerMoney = 148200;
let careerStreams = 48200000;

// --- Calendar & Weekly Date Simulation Engine ---
const CALENDAR_MONTHS = [
  { name: "JAN", fullName: "JANUARY", days: 31 },
  { name: "FEB", fullName: "FEBRUARY", days: 28 },
  { name: "MAR", fullName: "MARCH", days: 31 },
  { name: "APR", fullName: "APRIL", days: 30 },
  { name: "MAY", fullName: "MAY", days: 31 },
  { name: "JUN", fullName: "JUNE", days: 30 },
  { name: "JUL", fullName: "JULY", days: 31 },
  { name: "AUG", fullName: "AUGUST", days: 31 },
  { name: "SEP", fullName: "SEPTEMBER", days: 30 },
  { name: "OCT", fullName: "OCTOBER", days: 31 },
  { name: "NOV", fullName: "NOVEMBER", days: 30 },
  { name: "DEC", fullName: "DECEMBER", days: 31 }
];

const CAL_DAY_NAMES = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"];

function getCalendarDate(totalDayOffset) {
  // totalDayOffset is 0-indexed from Year 1, Jan 1
  const year = Math.floor(totalDayOffset / 365) + 1;
  let dayInYear = totalDayOffset % 365; // 0 to 364
  
  let monthIndex = 0;
  for (let m = 0; m < CALENDAR_MONTHS.length; m++) {
    if (dayInYear < CALENDAR_MONTHS[m].days) {
      monthIndex = m;
      break;
    }
    dayInYear -= CALENDAR_MONTHS[m].days;
  }
  
  const dayOfMonth = dayInYear + 1; // 1 to 31
  const month = CALENDAR_MONTHS[monthIndex];
  const weekOfMonth = Math.floor(dayInYear / 7) + 1;

  return {
    year,
    monthIndex,
    monthName: month.name,
    monthFullName: month.fullName,
    dayOfMonth,
    weekOfMonth
  };
}

function getWeekCalendarInfo(weekNum) {
  // Year 2 Week 24 starts at June 12
  const startOffset = 365 + (weekNum - 1) * 7 + 1;
  const days = [];
  for (let d = 0; d < 7; d++) {
    const dateObj = getCalendarDate(startOffset + d);
    days.push({
      dayIndex: d,
      dayName: CAL_DAY_NAMES[d],
      dayOfMonth: dateObj.dayOfMonth,
      monthName: dateObj.monthName,
      monthFullName: dateObj.monthFullName,
      year: dateObj.year,
      weekOfMonth: dateObj.weekOfMonth
    });
  }

  const mon = days[0];
  const sun = days[6];

  let rangeString = "";
  if (mon.year === sun.year) {
    if (mon.monthName === sun.monthName) {
      rangeString = `${mon.monthName} ${mon.dayOfMonth} - ${sun.dayOfMonth}, YEAR ${mon.year}`;
    } else {
      rangeString = `${mon.monthName} ${mon.dayOfMonth} - ${sun.monthName} ${sun.dayOfMonth}, YEAR ${mon.year}`;
    }
  } else {
    rangeString = `${mon.monthName} ${mon.dayOfMonth} - ${sun.monthName} ${sun.dayOfMonth}, YEAR ${mon.year}, ${sun.year}`;
  }

  return {
    days,
    monday: mon,
    sunday: sun,
    rangeString,
    headerTitle: `${mon.monthFullName} WEEK ${mon.weekOfMonth}`
  };
}

// Procedural Itinerary Generator for Each Day
function getDayItinerary(weekNum, dayIndex) {
  // Initial week 24 matches user sketch exactly
  if (weekNum === 24) {
    const defaultSchedule = [
      {
        events: ["ticket", "mic"],
        title: "Arena Tour Rehearsal & Live Radio Press"
      },
      {
        events: ["date"],
        title: "Celebrity Candlelit Dinner Date"
      },
      {
        events: ["ticket"],
        title: "Metro Headline Concert"
      },
      {
        events: ["release"],
        title: "New Single Worldwide Release"
      },
      {
        events: ["ticket"],
        title: "Summer Jam Festival Set"
      },
      {
        events: [],
        title: "Studio Downtime & Creative Rest"
      },
      {
        events: ["mic"],
        title: "Viral Industry Podcast Guest"
      }
    ];
    return defaultSchedule[dayIndex] || { events: [], title: "Rest Day" };
  }

  // Deterministic procedural schedules for simulated weeks
  const patterns = [
    // Pattern 0: Tour week
    [
      { events: ["mic"], title: "Press Junket & Radio Tour" },
      { events: ["ticket"], title: "Arena Soundcheck & VIP Meet" },
      { events: ["ticket"], title: "Headline Arena Concert" },
      { events: ["date"], title: "Romantic VIP Club Night" },
      { events: ["ticket"], title: "Festival Headline Performance" },
      { events: [], title: "Day Off / Tour Bus Recovery" },
      { events: ["mic"], title: "Sunday Live Stream Interview" }
    ],
    // Pattern 1: Release Rollout week
    [
      { events: ["mic"], title: "Billboard Exclusive Interview" },
      { events: ["ticket"], title: "Intimate Album Listening Party" },
      { events: ["date"], title: "Red Carpet Gala Appearance" },
      { events: ["release"], title: "Major Track Release & Music Video" },
      { events: ["ticket"], title: "Release Weekend Club Performance" },
      { events: ["mic"], title: "Post-Release Radio Takeover" },
      { events: [], title: "Rest & Review Chart Tracking" }
    ],
    // Pattern 2: Studio & Press week
    [
      { events: ["mic"], title: "Breakfast Club Radio Interview" },
      { events: [], title: "Studio Tracking Session" },
      { events: ["date"], title: "Romantic Getaway Dinner" },
      { events: ["ticket"], title: "Surprise Pop-Up Concert" },
      { events: ["release"], title: "Remix Feature Drop" },
      { events: ["ticket"], title: "Stadium Support Slot" },
      { events: ["mic"], title: "Late Night TV Performance" }
    ],
    // Pattern 3: Lifestyle & Media week
    [
      { events: ["mic"], title: "Vogue Cover Shoot & Q&A" },
      { events: ["date"], title: "Private Island Helicopter Date" },
      { events: ["ticket"], title: "Charity All-Star Concert" },
      { events: [], title: "Studio Writing Camp" },
      { events: ["ticket"], title: "Arena Tour Show" },
      { events: ["release"], title: "Official Music Video Drop" },
      { events: ["mic"], title: "Grammy Roundtable Podcast" }
    ]
  ];

  const pIndex = Math.abs(weekNum) % patterns.length;
  return patterns[pIndex][dayIndex] || { events: [], title: "Rest Day" };
}

function renderCalEventSvg(type) {
  if (type === "ticket") {
    return `
      <div class="cal-event-icon" title="Concert / Tour Show">
        <svg width="22" height="13" viewBox="0 0 28 16" fill="none">
          <rect x="1" y="1" width="26" height="14" rx="2" fill="#fef3c7" stroke="#212E53" stroke-width="1.3"/>
          <line x1="7" y1="1" x2="7" y2="15" stroke="#212E53" stroke-width="1" stroke-dasharray="1.5 1.5"/>
          <line x1="11" y1="5" x2="23" y2="5" stroke="#212E53" stroke-width="1.2"/>
          <line x1="11" y1="8" x2="19" y2="8" stroke="#b45309" stroke-width="1.2"/>
          <line x1="11" y1="11" x2="17" y2="11" stroke="#212E53" stroke-width="1"/>
          <circle cx="4" cy="8" r="1.5" fill="#b45309"/>
        </svg>
      </div>
    `;
  }
  if (type === "mic") {
    return `
      <div class="cal-event-icon" title="Interview / Podcast">
        <svg width="15" height="18" viewBox="0 0 20 24" fill="none">
          <rect x="6" y="2" width="8" height="11" rx="4" fill="#334155" stroke="#212E53" stroke-width="1.2"/>
          <line x1="8" y1="4.5" x2="12" y2="4.5" stroke="#94a3b8" stroke-width="1"/>
          <line x1="8" y1="7.5" x2="12" y2="7.5" stroke="#94a3b8" stroke-width="1"/>
          <line x1="8" y1="10.5" x2="12" y2="10.5" stroke="#94a3b8" stroke-width="1"/>
          <path d="M4 9 C4 14, 16 14, 16 9" stroke="#212E53" stroke-width="1.4" fill="none"/>
          <line x1="10" y1="14" x2="10" y2="19" stroke="#212E53" stroke-width="1.6"/>
          <line x1="6" y1="19" x2="14" y2="19" stroke="#212E53" stroke-width="1.8" stroke-linecap="round"/>
        </svg>
      </div>
    `;
  }
  if (type === "date") {
    return `
      <div class="cal-event-icon" title="Celebrity Date">
        <svg width="22" height="20" viewBox="0 0 26 24" fill="none">
          <g transform="rotate(12 8 11)">
            <path d="M6 2 L10 2 L9 8 Q8 11 5 11 Z" fill="#fef08a" stroke="#212E53" stroke-width="1.1"/>
            <line x1="7" y1="11" x2="7" y2="17" stroke="#212E53" stroke-width="1.2"/>
            <line x1="4" y1="17" x2="10" y2="17" stroke="#212E53" stroke-width="1.3" stroke-linecap="round"/>
          </g>
          <g transform="rotate(-12 18 11)">
            <path d="M16 2 L20 2 L21 11 Q18 11 17 8 Z" fill="#fef08a" stroke="#212E53" stroke-width="1.1"/>
            <line x1="19" y1="11" x2="19" y2="17" stroke="#212E53" stroke-width="1.2"/>
            <line x1="16" y1="17" x2="22" y2="17" stroke="#212E53" stroke-width="1.3" stroke-linecap="round"/>
          </g>
          <circle cx="13" cy="4" r="1.2" fill="#f59e0b"/>
          <circle cx="10" cy="2" r="0.8" fill="#CE6A6B"/>
          <circle cx="16" cy="2" r="0.8" fill="#CE6A6B"/>
        </svg>
      </div>
    `;
  }
  if (type === "release") {
    return `
      <div class="cal-event-icon" title="Music Release">
        <svg width="20" height="22" viewBox="0 0 24 26" fill="none">
          <path d="M12 2 C16 4, 18 8, 18 13 L15 16 L8 9 L11 6 C11 4, 12 2, 12 2 Z" fill="#f1f5f9" stroke="#212E53" stroke-width="1.2"/>
          <circle cx="13.5" cy="9.5" r="1.8" fill="#38bdf8" stroke="#212E53" stroke-width="0.8"/>
          <path d="M8 9 L4 11 L6 15 L10 14 Z" fill="#CE6A6B" stroke="#212E53" stroke-width="1"/>
          <path d="M15 16 L17 20 L21 18 L19 14 Z" fill="#CE6A6B" stroke="#212E53" stroke-width="1"/>
          <path d="M10 15 L8 21 L12 18 L14 23 L13 17 Z" fill="#f59e0b" stroke="#dc2626" stroke-width="0.8"/>
        </svg>
      </div>
    `;
  }
  return `<span class="cal-day-empty-pip" title="Rest Day"></span>`;
}

function updateCalendarEngineUI() {
  const info = getWeekCalendarInfo(careerWeek);

  // Status Bar Date Range: "JUN 12 - 18, YEAR 2", etc.
  const statusWeekYear = document.getElementById("statusBarWeekYear");
  if (statusWeekYear) statusWeekYear.textContent = info.rangeString;

  // Calendar Widget Headers
  const calWidgetTitle = document.getElementById("socialCalWidgetTitle");
  if (calWidgetTitle) calWidgetTitle.textContent = info.headerTitle;

  const calWidgetRange = document.getElementById("socialCalWidgetRange");
  if (calWidgetRange) calWidgetRange.textContent = info.rangeString;

  // 12 Apps Grid Calendar Tile
  const calWeek = document.getElementById("socialCalWeekNum");
  if (calWeek) calWeek.textContent = info.monday.dayOfMonth;
  const calMonthLbl = document.querySelector(".cal-month-lbl");
  if (calMonthLbl) calMonthLbl.textContent = info.monday.monthName;

  // Calendar 7-Day Strip
  const daysStrip = document.getElementById("socialCalendarDaysStrip");
  if (daysStrip) {
    let daysHtml = "";
    info.days.forEach((day, idx) => {
      const itin = getDayItinerary(careerWeek, idx);
      let iconsHtml = "";
      if (itin.events.length === 0) {
        iconsHtml = `<span class="cal-day-empty-pip" title="Rest Day"></span>`;
      } else {
        itin.events.forEach(ev => {
          iconsHtml += renderCalEventSvg(ev);
        });
      }

      daysHtml += `
        <div class="cal-day-col" onclick="inspectCalDay(${idx})" title="${day.dayName} ${day.dayOfMonth}: ${itin.title}">
          <div class="cal-day-header">
            <span class="cal-day-name">${day.dayName}</span>
            <span class="cal-day-num">${day.dayOfMonth}</span>
          </div>
          <div class="cal-day-divider"></div>
          <div class="cal-day-events">
            ${iconsHtml}
          </div>
        </div>
      `;
    });
    daysStrip.innerHTML = daysHtml;
  }
}

function inspectCalDay(dayIndex) {
  playMechanicalClick();
  const info = getWeekCalendarInfo(careerWeek);
  const day = info.days[dayIndex];
  const itin = getDayItinerary(careerWeek, dayIndex);
  showToast(`${day.dayName} ${day.dayOfMonth} ${day.monthName}: ${itin.title.toUpperCase()}`);
}

function simulateNextWeek() {
  playMechanicalClick();
  careerWeek++;

  const deltaStreams = (Math.floor(Math.random() * 8) + 12) / 10; // +1.2M to +1.9M
  const deltaMoney = Math.floor(Math.random() * 14000) + 16000; // +$16,000 to +$30,000

  careerMoney += deltaMoney;
  careerStreams += Math.round(deltaStreams * 1000000);

  // Update Dynamic Calendar UI & Status Bar
  updateCalendarEngineUI();

  const statusMoney = document.getElementById("statusMoney");
  if (statusMoney) statusMoney.textContent = `$${careerMoney.toLocaleString()}`;

  const valLastMoney = document.getElementById("valLastMoney");
  if (valLastMoney) valLastMoney.textContent = `$${deltaMoney.toLocaleString()}`;

  const valLastStreams = document.getElementById("valLastStreams");
  const weeklyStreamsVal = Math.round(deltaStreams * 250000) + 12000;
  if (valLastStreams) valLastStreams.textContent = `${weeklyStreamsVal.toLocaleString()}`;

  const weekInfo = getWeekCalendarInfo(careerWeek);
  const weekMarkers = document.querySelectorAll(".news-week-marker");
  weekMarkers.forEach(el => el.textContent = `${weekInfo.monday.monthName} ${weekInfo.monday.dayOfMonth}`);

  // Advance feature requests in real-time
  advanceFeatRequestsWeek();

  showToast(`Simulated to ${weekInfo.monday.monthName} ${weekInfo.monday.dayOfMonth}: +$${(deltaMoney / 1000).toFixed(1)}K, +${deltaStreams}M streams!`);
}

// --- Studio Hardwood Theme Engine (6 Color Finishes) ---
const HARDWOOD_THEMES = {
  "existing-brown": { name: "Existing Brown", icon: "🪵" },
  "lighter-brown": { name: "Lighter Brown", icon: "🪵" },
  "black": { name: "Black", icon: "🖤" },
  "blue": { name: "Blue", icon: "🌊" },
  "red-wood": { name: "Red Wood", icon: "🍒" },
  "gold-wood": { name: "Gold Wood", icon: "✨" }
};

function selectHardwoodTheme(themeKey) {
  if (!HARDWOOD_THEMES[themeKey]) return;

  playMechanicalClick();

  // Apply theme data attribute to body & mobile screen
  document.body.setAttribute("data-wood", themeKey);
  const mobileScreen = document.querySelector(".mobile-screen");
  if (mobileScreen) {
    Object.keys(HARDWOOD_THEMES).forEach(k => mobileScreen.classList.remove(`wood-${k}`));
    mobileScreen.classList.add(`wood-${themeKey}`);
  }

  // Persist preference across sessions
  try {
    localStorage.setItem("rapsim_hardwood_theme", themeKey);
  } catch (e) {
    // Storage unavailable fallback
  }

  // Update swatches active UI state
  const swatches = document.querySelectorAll(".wood-swatch-card");
  swatches.forEach(swatch => {
    if (swatch.getAttribute("data-wood-id") === themeKey) {
      swatch.classList.add("active");
    } else {
      swatch.classList.remove("active");
    }
  });

  // Update badge label in Settings
  const badge = document.getElementById("activeWoodLabel");
  if (badge) {
    badge.textContent = HARDWOOD_THEMES[themeKey].name;
  }

  showToast(`${HARDWOOD_THEMES[themeKey].icon} Hardwood set to: ${HARDWOOD_THEMES[themeKey].name}`);
}

function initHardwoodTheme() {
  const urlParams = new URLSearchParams(window.location.search);
  const woodParam = urlParams.get("wood");

  let savedTheme = "existing-brown";
  if (woodParam && HARDWOOD_THEMES[woodParam]) {
    savedTheme = woodParam;
    try {
      localStorage.setItem("rapsim_hardwood_theme", savedTheme);
    } catch (e) {}
  } else {
    try {
      savedTheme = localStorage.getItem("rapsim_hardwood_theme") || "existing-brown";
    } catch (e) {
      savedTheme = "existing-brown";
    }
  }

  if (!HARDWOOD_THEMES[savedTheme]) savedTheme = "existing-brown";

  document.body.setAttribute("data-wood", savedTheme);
  const mobileScreen = document.querySelector(".mobile-screen");
  if (mobileScreen) {
    Object.keys(HARDWOOD_THEMES).forEach(k => mobileScreen.classList.remove(`wood-${k}`));
    mobileScreen.classList.add(`wood-${savedTheme}`);
  }

  const swatches = document.querySelectorAll(".wood-swatch-card");
  swatches.forEach(swatch => {
    if (swatch.getAttribute("data-wood-id") === savedTheme) {
      swatch.classList.add("active");
    } else {
      swatch.classList.remove("active");
    }
  });

  const badge = document.getElementById("activeWoodLabel");
  if (badge) {
    badge.textContent = HARDWOOD_THEMES[savedTheme].name;
  }
}

// ==========================================================================
// STUDIO TAB & CONSOLE LOGIC
// ==========================================================================
const FULL_CATALOGUE_DATA = [
  // --- SONGS ---
  // Unreleased Songs
  {
    id: "cat-s1",
    type: "song",
    typeName: "SONG",
    isReleased: false,
    title: "LATE NIGHT IN SHIBUYA",
    status: "UNRELEASED",
    quality: "4.9",
    genre: "TRAP SOUL",
    bpm: "138 BPM",
    cover: "album covers/download (10).jpg",
    details: "UNFINISHED 2ND VERSE, DEMO MIX"
  },
  {
    id: "cat-s2",
    type: "song",
    typeName: "SONG",
    isReleased: false,
    title: "VANDALIZED HEART",
    status: "UNRELEASED",
    quality: "6.7",
    genre: "MELODIC DRILL",
    bpm: "144 BPM",
    cover: "album covers/download (9).jpg",
    details: "MIX V2 COMPLETED, READY FOR POLISH"
  },
  {
    id: "cat-s3",
    type: "song",
    typeName: "SONG",
    isReleased: false,
    title: "CHROME 808S & HEARTBREAK",
    status: "MASTERED",
    quality: "8.0",
    genre: "DARK BOOM-BAP",
    bpm: "92 BPM",
    cover: "album covers/download (8).jpg",
    details: "MASTERED AT STERLING SOUND, READY"
  },
  {
    id: "cat-s4",
    type: "song",
    typeName: "SONG",
    isReleased: false,
    title: "MIDNIGHT RENDEZVOUS",
    status: "UNRELEASED",
    quality: "8.8",
    genre: "R&B / NEO-SOUL",
    bpm: "110 BPM",
    cover: "album covers/download (7).jpg",
    details: "RADIO READY VOCAL MIX"
  },
  {
    id: "cat-s5",
    type: "song",
    typeName: "SONG",
    isReleased: false,
    title: "GHOST IN THE MACHINE",
    status: "MASTERED",
    quality: "9.2",
    genre: "CYBER TRAP",
    bpm: "142 BPM",
    cover: "album covers/download (4).jpg",
    details: "GOLDEN MASTER 24-BIT STEMS"
  },
  // Released Songs
  {
    id: "cat-s6",
    type: "song",
    typeName: "SONG",
    isReleased: true,
    title: "NEON DREAMS",
    status: "RELEASED",
    quality: "9.4",
    genre: "SYNTH TRAP",
    bpm: "140 BPM",
    streams: "124.8M STREAMS",
    certification: "PLATINUM",
    cover: "album covers/download (10).jpg",
    details: "LEAD SINGLE • 124.8M STREAMS • PEAK #3 HOT 100"
  },
  {
    id: "cat-s7",
    type: "song",
    typeName: "SONG",
    isReleased: true,
    title: "CHROME HEART BOULEVARD",
    status: "RELEASED",
    quality: "8.8",
    genre: "MELODIC TRAP",
    bpm: "130 BPM",
    streams: "88.4M STREAMS",
    certification: "GOLD",
    cover: "album covers/download (5).jpg",
    details: "HIT SINGLE • 88.4M STREAMS • PEAK #12 HOT 100"
  },
  {
    id: "cat-s8",
    type: "song",
    typeName: "SONG",
    isReleased: true,
    title: "TOKYO DRIFT PHONK",
    status: "RELEASED",
    quality: "8.2",
    genre: "MEMPHIS PHONK",
    bpm: "150 BPM",
    streams: "45.2M STREAMS",
    certification: "GOLD",
    cover: "album covers/download (6).jpg",
    details: "VIRAL TIKTOK SMASH • 45.2M STREAMS"
  },
  {
    id: "cat-s9",
    type: "song",
    typeName: "SONG",
    isReleased: true,
    title: "VELVET BULLETS",
    status: "RELEASED",
    quality: "8.6",
    genre: "NOIR DRILL",
    bpm: "136 BPM",
    streams: "62.1M STREAMS",
    certification: "GOLD",
    cover: "album covers/Tyler Durden.jpg",
    details: "UNDERGROUND ANTHEM • 62.1M STREAMS"
  },

  // --- PROJECTS ---
  // Unreleased Projects
  {
    id: "cat-p1",
    type: "project",
    typeName: "PROJECT",
    isReleased: false,
    title: "MIDNIGHT SESSIONS (DELUXE)",
    status: "ALBUM DRAFT",
    quality: "9.1",
    genre: "14 TRACKS",
    bpm: "85% COMPLETE",
    cover: "album covers/download (2).jpg",
    details: "FINAL TRACK SEQUENCING IN PROGRESS"
  },
  {
    id: "cat-p2",
    type: "project",
    typeName: "PROJECT",
    isReleased: false,
    title: "LOST IN SHIBUYA EP",
    status: "EP CONCEPT",
    quality: "7.6",
    genre: "6 TRACKS",
    bpm: "40% COMPLETE",
    cover: "album covers/download (3).jpg",
    details: "NEEDS 2 FEATURE VERSES AND FINAL MIX"
  },
  {
    id: "cat-p3",
    type: "project",
    typeName: "PROJECT",
    isReleased: false,
    title: "CHROME METROPOLIS",
    status: "ALBUM DRAFT",
    quality: "8.7",
    genre: "12 TRACKS",
    bpm: "UNMASTERED",
    cover: "album covers/Music artwork for Frank Ocean - _.jpg",
    details: "FULL LENGTH LP CONCEPT IN RECORDING"
  },
  {
    id: "cat-p4",
    type: "project",
    typeName: "PROJECT",
    isReleased: false,
    title: "OVERDRIVE TAPES VOL. 1",
    status: "MIXTAPE DRAFT",
    quality: "8.1",
    genre: "8 TRACKS",
    bpm: "IN SEQUENCING",
    cover: "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg",
    details: "RAW CASSETTE MIXTAPE MASTER"
  },
  // Released Projects
  {
    id: "cat-p5",
    type: "project",
    typeName: "PROJECT",
    isReleased: true,
    title: "MIDNIGHT SESSIONS",
    status: "RELEASED",
    quality: "9.3",
    genre: "12 TRACKS",
    bpm: "DEBUT LP",
    streams: "480M STREAMS",
    certification: "2X PLATINUM",
    cover: "album covers/download (2).jpg",
    details: "BILLBOARD #1 DEBUT ALBUM • 480M GLOBAL STREAMS"
  },
  {
    id: "cat-p6",
    type: "project",
    typeName: "PROJECT",
    isReleased: true,
    title: "NIGHT CITY CHRONICLES",
    status: "RELEASED",
    quality: "8.9",
    genre: "8 TRACKS",
    bpm: "COMMERCIAL EP",
    streams: "195M STREAMS",
    certification: "GOLD",
    cover: "album covers/download (3).jpg",
    details: "CRITICALLY ACCLAIMED EP • 195M STREAMS"
  },

  // --- MUSIC VIDEOS ---
  // Unreleased Music Videos
  {
    id: "cat-v1",
    type: "video",
    typeName: "MUSIC VIDEO",
    isReleased: false,
    title: "VANDALIZED HEART (OFFICIAL VIDEO)",
    status: "POST-PROD",
    quality: "8.9",
    genre: "4K CINEMA",
    bpm: "COLOR GRADE PENDING",
    cover: "album covers/download (9).jpg",
    details: "DIRECTED IN TOKYO WAREHOUSE • 4K RENDER"
  },
  {
    id: "cat-v2",
    type: "video",
    typeName: "MUSIC VIDEO",
    isReleased: false,
    title: "LATE NIGHT IN SHIBUYA (VISUALIZER)",
    status: "UNRELEASED",
    quality: "7.2",
    genre: "3D ANIME",
    bpm: "60 FPS RENDER",
    cover: "album covers/download (10).jpg",
    details: "CGI TOKYO STREET NIGHTLIFE VISUALIZER"
  },
  {
    id: "cat-v3",
    type: "video",
    typeName: "MUSIC VIDEO",
    isReleased: false,
    title: "GHOST IN THE MACHINE (SCI-FI FILM)",
    status: "VFX EDIT",
    quality: "9.6",
    genre: "IMAX CGI",
    bpm: "HIGH BUDGET",
    cover: "album covers/download (4).jpg",
    details: "SHORT SCI-FI MOVIE EXPERIENCE"
  },
  // Released Music Videos
  {
    id: "cat-v4",
    type: "video",
    typeName: "MUSIC VIDEO",
    isReleased: true,
    title: "NEON DREAMS (MUSIC VIDEO)",
    status: "RELEASED",
    quality: "9.5",
    genre: "4K OFFICIAL",
    bpm: "YOUTUBE",
    streams: "84.2M VIEWS",
    certification: "VEVO CERTIFIED",
    cover: "album covers/download (10).jpg",
    details: "84.2M VIEWS ON YOUTUBE • VMA NOMINATED"
  },
  {
    id: "cat-v5",
    type: "video",
    typeName: "MUSIC VIDEO",
    isReleased: true,
    title: "CHROME HEART BOULEVARD (LIVE VISUAL)",
    status: "RELEASED",
    quality: "8.7",
    genre: "DIRECTOR'S CUT",
    bpm: "LIVE STUDIO",
    streams: "32.1M VIEWS",
    certification: "VIRAL",
    cover: "album covers/download (5).jpg",
    details: "LIVE ACOUSTIC SESSION • 32.1M VIEWS"
  },

  // --- BEATS ---
  // Unreleased Beats
  {
    id: "cat-b1",
    type: "beat",
    typeName: "BEAT",
    isReleased: false,
    title: "808 GRIM REAPER",
    status: "EXCLUSIVE",
    quality: "8.2",
    genre: "DARK DRILL",
    bpm: "142 BPM • KEY: F# MIN",
    cover: "album covers/Music artwork for Frank Ocean - _.jpg",
    details: "HEAVY SLIDING 808S, HAUNTING PIANO"
  },
  {
    id: "cat-b2",
    type: "beat",
    typeName: "BEAT",
    isReleased: false,
    title: "CLOUD TRAP SOUL V3",
    status: "LEASED",
    quality: "7.8",
    genre: "LO-FI TRAP",
    bpm: "128 BPM • KEY: C MIN",
    cover: "album covers/Tyler Durden.jpg",
    details: "WARM ANALOG PADS, VINYL TEXTURE"
  },
  {
    id: "cat-b3",
    type: "beat",
    typeName: "BEAT",
    isReleased: false,
    title: "SYMPHONIC DRILL STEM",
    status: "IN STEMS",
    quality: "8.9",
    genre: "ORCHESTRAL DRILL",
    bpm: "140 BPM • KEY: D MIN",
    cover: "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg",
    details: "LIVE STRINGS WITH AGGRESSIVE HI-HATS"
  },
  {
    id: "cat-b4",
    type: "beat",
    typeName: "BEAT",
    isReleased: false,
    title: "TOKYO CYBER 808",
    status: "UNRELEASED",
    quality: "8.5",
    genre: "SYNTH TRAP",
    bpm: "135 BPM • KEY: A MIN",
    cover: "album covers/download (6).jpg",
    details: "ANALOG MOOG BASS WITH CRISP PERCUSSION"
  },
  // Released Beats
  {
    id: "cat-b5",
    type: "beat",
    typeName: "BEAT",
    isReleased: true,
    title: "NEON SYNTHWAVE MASTER BEAT",
    status: "RELEASED",
    quality: "9.4",
    genre: "SYNTH TRAP",
    bpm: "140 BPM",
    streams: "124.8M PLAYS",
    certification: "PLATINUM PRODUCER",
    cover: "album covers/download (10).jpg",
    details: "OFFICIAL BEAT USED ON 'NEON DREAMS'"
  },
  {
    id: "cat-b6",
    type: "beat",
    typeName: "BEAT",
    isReleased: true,
    title: "HEART BOULEVARD TRAP STEMS",
    status: "RELEASED",
    quality: "8.8",
    genre: "MELODIC TRAP",
    bpm: "130 BPM",
    streams: "88.4M PLAYS",
    certification: "GOLD PRODUCER",
    cover: "album covers/download (5).jpg",
    details: "OFFICIAL BEAT USED ON 'CHROME HEART BOULEVARD'"
  }
];

let activeCatalogueReleaseState = "unreleased"; // "unreleased" | "released"
let activeCatalogueType = "song"; // "song" | "project" | "video" | "beat"
let activeCatalogueSearch = "";



// ==========================================================================
// STUDIO RELEASE CONSOLE & CATALOG ENGINE
// ==========================================================================
const UNRELEASED_RELEASE_DATA = {
  song: [
    {
      id: "rel-s1",
      title: "LATE NIGHT IN SHIBUYA",
      quality: "4.9",
      genre: "Trap Soul • 138 BPM",
      cover: "album covers/download (10).jpg",
      status: "Ready to Master"
    },
    {
      id: "rel-s2",
      title: "VANDALIZED HEART",
      quality: "6.7",
      genre: "Melodic Drill • 144 BPM",
      cover: "album covers/download (9).jpg",
      status: "Mix Polish Done"
    },
    {
      id: "rel-s3",
      title: "CHROME 808S & HEARTBREAK",
      quality: "8.0",
      genre: "Dark Boom-Bap • 92 BPM",
      cover: "album covers/download (8).jpg",
      status: "Mastered Single"
    },
    {
      id: "rel-s4",
      title: "MIDNIGHT RENDEZVOUS",
      quality: "8.8",
      genre: "R&B / Neo-Soul • 110 BPM",
      cover: "album covers/download (7).jpg",
      status: "Radio Ready"
    },
    {
      id: "rel-s5",
      title: "TOKYO DRIFT PHONK",
      quality: "7.4",
      genre: "Memphis Phonk • 150 BPM",
      cover: "album covers/download (6).jpg",
      status: "Club Master"
    },
    {
      id: "rel-s6",
      title: "GHOST IN THE MACHINE",
      quality: "9.2",
      genre: "Cyber Trap • 142 BPM",
      cover: "album covers/download (4).jpg",
      status: "Golden Master"
    },
    {
      id: "rel-s7",
      title: "VELVET BULLETS",
      quality: "8.5",
      genre: "Noir Drill • 136 BPM",
      cover: "album covers/download (5).jpg",
      status: "Mastered Single"
    },
    {
      id: "rel-s8",
      title: "NO ESCAPE",
      quality: "6.2",
      genre: "Rage Trap • 155 BPM",
      cover: "album covers/Tyler Durden.jpg",
      status: "Final Mix"
    }
  ],
  project: [
    {
      id: "rel-p1",
      title: "MIDNIGHT SESSIONS (DELUXE)",
      quality: "9.1",
      genre: "14 Tracks • Deluxe LP",
      cover: "album covers/download (2).jpg",
      status: "Sequenced & Mastered"
    },
    {
      id: "rel-p2",
      title: "LOST IN SHIBUYA EP",
      quality: "7.6",
      genre: "6 Tracks • EP Concept",
      cover: "album covers/download (3).jpg",
      status: "Mix V2 Final"
    },
    {
      id: "rel-p3",
      title: "CHROME METROPOLIS",
      quality: "8.7",
      genre: "12 Tracks • Studio Album",
      cover: "album covers/Music artwork for Frank Ocean - _.jpg",
      status: "Album Master"
    },
    {
      id: "rel-p4",
      title: "OVERDRIVE TAPES VOL. 1",
      quality: "8.1",
      genre: "8 Tracks • Mixtape",
      cover: "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg",
      status: "Cassette Mastered"
    },
    {
      id: "rel-p5",
      title: "NEON REQUIEM",
      quality: "9.5",
      genre: "16 Tracks • Concept LP",
      cover: "album covers/download (4).jpg",
      status: "Master Complete"
    }
  ],
  video: [
    {
      id: "rel-v1",
      title: "VANDALIZED HEART (OFFICIAL VIDEO)",
      quality: "8.9",
      genre: "4K Cinema • Visuals",
      cover: "album covers/download (9).jpg",
      status: "Color Graded"
    },
    {
      id: "rel-v2",
      title: "LATE NIGHT IN SHIBUYA (VISUALIZER)",
      quality: "7.2",
      genre: "3D Anime • 60 FPS",
      cover: "album covers/download (10).jpg",
      status: "Render Complete"
    },
    {
      id: "rel-v3",
      title: "CHROME 808S (STREET VIDEO)",
      quality: "8.4",
      genre: "16mm Film Grain • Official",
      cover: "album covers/download (8).jpg",
      status: "Final Cut"
    },
    {
      id: "rel-v4",
      title: "GHOST IN THE MACHINE (CYBER MOVIE)",
      quality: "9.6",
      genre: "IMAX CGI Sci-Fi • High Budget",
      cover: "album covers/download (4).jpg",
      status: "Master VFX Complete"
    }
  ]
};

let activeReleaseType = "song";
let activeReleaseSearch = "";

function openStudioCatalogueTab() {
  playMechanicalClick();
  switchTab("catalogue");
  renderCatalogueFull();
}

function openStudioReleaseTab() {
  playMechanicalClick();
  switchTab("release");
  switchReleaseType("song");
}

function switchReleaseType(type) {
  playMechanicalClick();
  activeReleaseType = type;

  // Update Left Vertical Rail active button states
  const btnSong = document.getElementById("relTabBtnSong");
  const btnProject = document.getElementById("relTabBtnProject");
  const btnVideo = document.getElementById("relTabBtnVideo");

  if (btnSong) btnSong.classList.toggle("active", type === "song");
  if (btnProject) btnProject.classList.toggle("active", type === "project");
  if (btnVideo) btnVideo.classList.toggle("active", type === "video");

  // Update Dynamic Title in Cream Card
  const titleEl = document.getElementById("releaseCardTitle");
  const searchInput = document.getElementById("releaseSearchInput");

  if (type === "song") {
    if (titleEl) titleEl.textContent = "YOUR SONGS";
    if (searchInput) searchInput.placeholder = "Search unreleased songs...";
  } else if (type === "project") {
    if (titleEl) titleEl.textContent = "YOUR PROJECTS";
    if (searchInput) searchInput.placeholder = "Search unreleased projects...";
  } else if (type === "video") {
    if (titleEl) titleEl.textContent = "YOUR MUSIC VIDEOS";
    if (searchInput) searchInput.placeholder = "Search music videos...";
  }

  // Clear search or reapply filter
  renderReleaseList();
}

function onReleaseSearchInput(query) {
  activeReleaseSearch = (query || "").trim().toLowerCase();
  const clearBtn = document.getElementById("releaseSearchClear");
  if (clearBtn) {
    clearBtn.style.display = activeReleaseSearch ? "flex" : "none";
  }
  renderReleaseList();
}

function clearReleaseSearch() {
  playMechanicalClick();
  const searchInput = document.getElementById("releaseSearchInput");
  if (searchInput) {
    searchInput.value = "";
    searchInput.focus();
  }
  onReleaseSearchInput("");
}

function renderReleaseList() {
  const container = document.getElementById("releaseItemsList");
  const countBadge = document.getElementById("releaseItemCount");
  if (!container) return;

  const dataset = UNRELEASED_RELEASE_DATA[activeReleaseType] || [];
  
  // Filter by search query
  const filtered = dataset.filter(item => {
    if (!activeReleaseSearch) return true;
    return (
      item.title.toLowerCase().includes(activeReleaseSearch) ||
      item.genre.toLowerCase().includes(activeReleaseSearch) ||
      item.status.toLowerCase().includes(activeReleaseSearch)
    );
  });

  if (countBadge) {
    countBadge.textContent = `${filtered.length} UNRELEASED`;
  }

  container.innerHTML = "";

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="release-empty-state">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <p>No unreleased items found</p>
      </div>
    `;
    return;
  }

  filtered.forEach(item => {
    const qNum = parseFloat(item.quality);
    let qClass = "q-mid";
    if (qNum >= 9.0) qClass = "q-high";
    else if (qNum >= 8.0) qClass = "q-good";
    else if (qNum < 6.5) qClass = "q-low";

    const row = document.createElement("div");
    row.className = "release-item-row";
    row.onclick = () => openReleaseItemModal(item.id);

    row.innerHTML = `
      <img src="${item.cover}" class="release-item-thumb" alt="${item.title}" onerror="this.src='album covers/download (10).jpg'">
      <div class="release-item-info">
        <div class="release-item-title">${item.title}</div>
        <div class="release-item-meta">${item.genre}</div>
      </div>
      <div class="release-item-front-right">
        <span class="release-quality-pill ${qClass}">Q ${item.quality}</span>
        <button class="release-btn-drop" onclick="event.stopPropagation(); openReleaseItemModal('${item.id}')">DROP</button>
      </div>
    `;

    container.appendChild(row);
  });
}

function openReleaseItemModal(itemId) {
  playMechanicalClick();
  const dataset = UNRELEASED_RELEASE_DATA[activeReleaseType] || [];
  const item = dataset.find(i => i.id === itemId);
  if (!item) return;

  const modal = document.getElementById("releaseItemModal");
  const heading = document.getElementById("releaseModalHeading");
  const body = document.getElementById("releaseItemModalBody");
  if (!modal || !body) return;

  const typeLabel = activeReleaseType === "song" ? "SINGLE RELEASE" : activeReleaseType === "project" ? "PROJECT ROLLOUT" : "MUSIC VIDEO DROP";
  if (heading) heading.textContent = typeLabel;

  const qNum = parseFloat(item.quality);
  let qRatingText = "Solid Quality";
  let qClass = "q-mid";
  if (qNum >= 9.0) { qRatingText = "Exceptional Master"; qClass = "q-high"; }
  else if (qNum >= 8.0) { qRatingText = "High Studio Polish"; qClass = "q-good"; }
  else if (qNum < 6.5) { qRatingText = "Demo Quality"; qClass = "q-low"; }

  body.innerHTML = `
    <div class="release-confirm-card">
      <img src="${item.cover}" class="release-confirm-thumb" alt="${item.title}">
      <div class="release-confirm-details">
        <div class="release-confirm-title">${item.title}</div>
        <div class="release-confirm-meta">${item.genre}</div>
        <span class="release-quality-pill ${qClass}">QUALITY: ${item.quality}/10 &bull; ${qRatingText}</span>
      </div>
    </div>

    <div style="font-size: 0.72rem; font-weight: 800; color: #a0aec0; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 6px;">
      DISTRIBUTION PLATFORMS
    </div>
    <div class="release-dsp-platforms">
      <div class="release-dsp-chip active">&#9679; SPOTIFY</div>
      <div class="release-dsp-chip active">&#9679; APPLE</div>
      <div class="release-dsp-chip active">&#9679; TIKTOK</div>
      <div class="release-dsp-chip active">&#9679; YOUTUBE</div>
    </div>

    <button class="release-launch-btn" onclick="executeItemRelease('${item.id}')">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3">
        <polygon points="5 3 19 12 5 21 5 3"/>
      </svg>
      CONFIRM &amp; DISTRIBUTE NOW
    </button>
  `;

  modal.classList.add("active");
}

function closeReleaseItemModal() {
  playMechanicalClick();
  const modal = document.getElementById("releaseItemModal");
  if (modal) modal.classList.remove("active");
}

function executeItemRelease(itemId) {
  playMechanicalClick();
  const dataset = UNRELEASED_RELEASE_DATA[activeReleaseType] || [];
  const item = dataset.find(i => i.id === itemId);
  closeReleaseItemModal();

  if (item) {
    showToast(`🚀 "${item.title}" successfully submitted to Spotify, Apple Music & DSPs!`);
  }
}


// Studio Create Workflow Functions
function openStudioCreateTab() {
  playMechanicalClick();
  switchTab("create");
}

function openCreateWorkflow(type) {
  playMechanicalClick();
  const titles = {
    song: "NEW SONG RECORDING",
    project: "NEW PROJECT CONCEPT",
    video: "NEW MUSIC VIDEO PRODUCTION",
    beat: "NEW BEAT & 808s SEQUENCER",
    deluxe: "DELUXE EDITION ROLLOUT",
    remix: "REMIX & FEATURE SWAP",
    defaults: "STUDIO CREATION DEFAULTS"
  };
  showToast(`${titles[type] || type.toUpperCase()}: PHASE 2 DEVELOPMENT`);
}

function triggerStudioPlaceholder(featureName) {
  playMechanicalClick();
  showToast(`${featureName.toUpperCase()}: PHASE 2 DEVELOPMENT`);
}

function openFeatRequestsTab() {
  playMechanicalClick();
  const hub = document.getElementById("studioMainHub");
  if (hub) hub.style.display = "none";

  const allSubpages = ["catalogue", "feat-req", "promotion", "skills"];
  allSubpages.forEach(sp => {
    const el = document.getElementById(`studioSubpage_${sp}`);
    if (el) {
      if (sp === "feat-req") {
        el.style.display = "flex";
        el.scrollTop = 0;
      } else {
        el.style.display = "none";
      }
    }
  });

  // Always open Inbound request page by default!
  switchFeatPrimaryTab("inbound");
}

function openStudioPromotionTab() {
  openStudioSubpage("promotion");
}

function openStudioSkillsTab() {
  openStudioSubpage("skills");
}

function openStudioSubpage(subpageKey) {
  if (subpageKey === "catalogue") {
    openStudioCatalogueTab();
    return;
  }
  if (subpageKey === "feat-req") {
    openFeatRequestsTab();
    return;
  }
  playMechanicalClick();
  const hub = document.getElementById("studioMainHub");
  if (hub) hub.style.display = "none";

  const allSubpages = ["catalogue", "feat-req", "promotion", "skills"];
  allSubpages.forEach(sp => {
    const el = document.getElementById(`studioSubpage_${sp}`);
    if (el) {
      if (sp === subpageKey) {
        el.style.display = "flex";
        el.scrollTop = 0;
      } else {
        el.style.display = "none";
      }
    }
  });

  if (subpageKey === "catalogue") {
    renderCatalogueFull();
  } else if (subpageKey === "feat-req") {
    renderActiveFeatTab();
  } else if (subpageKey === "skills") {
    updateSkillsDeckUI();
  }
}

function closeStudioSubpage() {
  playMechanicalClick();
  const allSubpages = ["catalogue", "feat-req", "promotion", "skills"];
  allSubpages.forEach(sp => {
    const el = document.getElementById(`studioSubpage_${sp}`);
    if (el) el.style.display = "none";
  });

  const hub = document.getElementById("studioMainHub");
  if (hub) hub.style.display = "flex";
}

function switchCatalogueReleaseState(state) {
  playMechanicalClick();
  activeCatalogueReleaseState = state;

  const btnUnreleased = document.getElementById("catToggleUnreleased");
  const btnReleased = document.getElementById("catToggleReleased");
  const track = document.getElementById("catToggleTrack");

  if (btnUnreleased) btnUnreleased.classList.toggle("active", state === "unreleased");
  if (btnReleased) btnReleased.classList.toggle("active", state === "released");
  if (track) track.classList.toggle("released", state === "released");

  renderCatalogueFull();
}

function toggleCatalogueReleaseState() {
  const next = activeCatalogueReleaseState === "unreleased" ? "released" : "unreleased";
  switchCatalogueReleaseState(next);
}

function switchCatalogueType(type) {
  playMechanicalClick();
  activeCatalogueType = type;

  // Update 4 icons active state
  ["song", "project", "video", "beat"].forEach(t => {
    const btn = document.getElementById(`catTypeBtn_${t}`);
    if (btn) btn.classList.toggle("active", t === type);
  });

  const titleEl = document.getElementById("catCardTitle");
  const searchInput = document.getElementById("catSearchInput");

  const titles = {
    song: "YOUR SONGS",
    project: "YOUR PROJECTS",
    video: "YOUR MUSIC VIDEOS",
    beat: "YOUR BEATS"
  };

  const placeholders = {
    song: "Search songs...",
    project: "Search projects...",
    video: "Search music videos...",
    beat: "Search beats..."
  };

  if (titleEl) titleEl.textContent = titles[type] || "YOUR CATALOGUE";
  if (searchInput) searchInput.placeholder = placeholders[type] || "Search...";

  renderCatalogueFull();
}

function onCatalogueSearchInput(query) {
  activeCatalogueSearch = (query || "").trim().toLowerCase();
  const clearBtn = document.getElementById("catSearchClear");
  if (clearBtn) {
    clearBtn.style.display = activeCatalogueSearch ? "flex" : "none";
  }
  renderCatalogueFull();
}

function clearCatalogueSearch() {
  playMechanicalClick();
  const input = document.getElementById("catSearchInput");
  if (input) {
    input.value = "";
    input.focus();
  }
  onCatalogueSearchInput("");
}

function renderCatalogueFull() {
  const container = document.getElementById("catalogueFullList");
  const countBadge = document.getElementById("catItemCount");
  if (!container) return;

  const isRelTarget = activeCatalogueReleaseState === "released";

  // Filter by type and release state: shows ONLY once at a time!
  let items = FULL_CATALOGUE_DATA.filter(item => {
    const matchType = item.type === activeCatalogueType;
    const matchRelease = isRelTarget ? item.isReleased : !item.isReleased;
    return matchType && matchRelease;
  });

  // Filter by search query if any
  if (activeCatalogueSearch) {
    items = items.filter(item =>
      item.title.toLowerCase().includes(activeCatalogueSearch) ||
      item.genre.toLowerCase().includes(activeCatalogueSearch) ||
      item.status.toLowerCase().includes(activeCatalogueSearch)
    );
  }

  if (countBadge) {
    const stateLabel = activeCatalogueReleaseState.toUpperCase();
    countBadge.textContent = `${items.length} ${stateLabel}`;
  }

  container.innerHTML = "";

  if (items.length === 0) {
    const stateLabel = activeCatalogueReleaseState === "released" ? "released" : "unreleased";
    const typeLabel = activeCatalogueType === "song" ? "songs" : activeCatalogueType === "project" ? "projects" : activeCatalogueType === "video" ? "music videos" : "beats";
    container.innerHTML = `
      <div class="cat-empty-state">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <p>No ${stateLabel} ${typeLabel} found</p>
      </div>
    `;
    return;
  }

  items.forEach(item => {
    const card = document.createElement("div");
    card.className = "cat-row-item";
    card.onclick = () => inspectCatalogueItem(item.id);

    const qNum = parseFloat(item.quality);
    let qClass = "q-mid";
    if (qNum >= 9.0) qClass = "q-high";
    else if (qNum >= 8.0) qClass = "q-good";
    else if (qNum < 6.5) qClass = "q-low";

    const subMeta = item.isReleased 
      ? `${item.genre} &bull; ${item.streams || "Released"}`
      : `${item.genre} &bull; ${item.bpm}`;

    const statusPillHtml = item.isReleased
      ? `<span class="cat-status-pill released">${item.certification || "RELEASED"}</span>`
      : `<span class="cat-status-pill ${item.status === 'MASTERED' ? 'mastered' : 'unreleased'}">${item.status}</span>`;

    card.innerHTML = `
      <img src="${item.cover}" alt="${item.title}" class="cat-row-thumb" onerror="this.src='album covers/download (10).jpg'">
      <div class="cat-row-info">
        <div class="cat-row-title">${item.title}</div>
        <div class="cat-row-meta">${subMeta}</div>
      </div>
      <div class="cat-row-right">
        ${statusPillHtml}
        <span class="release-quality-pill ${qClass}">Q ${item.quality}</span>
      </div>
    `;
    container.appendChild(card);
  });
}

function inspectCatalogueItem(itemId) {
  playMechanicalClick();
  const item = FULL_CATALOGUE_DATA.find(i => i.id === itemId);
  if (!item) return;

  const drawer = document.getElementById("catalogueActionDrawer");
  if (!drawer) return;

  document.getElementById("drawerThumb").src = item.cover;
  document.getElementById("drawerTitle").textContent = item.title;
  document.getElementById("drawerType").innerHTML = `${item.typeName} &bull; QUALITY: <strong>${item.quality}/10</strong> &bull; ${item.status}`;

  const actionsContainer = document.getElementById("drawerActionsContainer");
  if (actionsContainer) {
    actionsContainer.innerHTML = "";

    let actions = [];
    if (item.type === "song") {
      actions = [
        { label: "MASTER TRACK" },
        { label: "ADD FEATURE" },
        { label: "PITCH TO DSPS" },
        { label: "ASSIGN TO ALBUM" }
      ];
    } else if (item.type === "beat") {
      actions = [
        { label: "WRITE LYRICS" },
        { label: "TWEAK 808S" },
        { label: "LEASE BEAT" },
        { label: "VAULT BEAT" }
      ];
    } else if (item.type === "video") {
      actions = [
        { label: "COLOR GRADE" },
        { label: "ADD 3D VFX" },
        { label: "YOUTUBE DROP" },
        { label: "EXPORT SHORTS" }
      ];
    } else {
      actions = [
        { label: "REORDER TRACKLIST" },
        { label: "COMMISSION ARTWORK" },
        { label: "SCHEDULE DROP" },
        { label: "SCRAP CONCEPT" }
      ];
    }

    actions.forEach(act => {
      const btn = document.createElement("button");
      btn.className = "drawer-action-btn";
      btn.textContent = act.label;
      btn.onclick = (e) => {
        e.stopPropagation();
        triggerStudioPlaceholder(act.label);
      };
      actionsContainer.appendChild(btn);
    });
  }

  drawer.style.display = "block";
  drawer.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function closeCatalogueDrawer() {
  playMechanicalClick();
  const drawer = document.getElementById("catalogueActionDrawer");
  if (drawer) drawer.style.display = "none";
}

function triggerPhase2Action(actionName, itemTitle) {
  playMechanicalClick();
  showToast(`${actionName.toUpperCase()}: PHASE 2 DEVELOPMENT`);
}

// Studio Create & Release Handlers (Placeholders for Phase 2)
function openStudioCreateModal() {
  triggerStudioPlaceholder("CREATE");
}

function closeStudioCreateModal() {
  const modal = document.getElementById("studioCreateModal");
  if (modal) modal.classList.remove("active");
}

function createActionHandler(type) {
  triggerStudioPlaceholder("CREATION ACTION");
}

function openStudioReleaseModal() {
  triggerStudioPlaceholder("RELEASE");
}

function closeStudioReleaseModal() {
  const modal = document.getElementById("studioReleaseModal");
  if (modal) modal.classList.remove("active");
}

function releaseActionHandler(type) {
  triggerStudioPlaceholder("RELEASE ACTION");
}

// ==========================================================================
// FEATURE REQUESTS ENGINE: INBOUND & OUTBOUND (WAITING / RECIEVED)
// ==========================================================================
let activeFeatPrimaryTab = "inbound"; // "inbound" | "outbound"
let activeFeatOutboundSubTab = "recieved"; // "waiting" | "recieved"
let featOfferSelectedType = "verse"; // "verse" | "beat" | "mix"

// Inbound Feature Requests (sent by other artists to player)
let featInboundRequests = [
  {
    id: "in-1",
    artist: "METRO BOOMIN",
    songTitle: "HEROES & VILLAINS INTRO",
    quality: "8.6",
    requestedType: "verse",
    money: 90000,
    split: 20,
    deadlineWeeks: 3
  },
  {
    id: "in-2",
    artist: "TRAVIS SCOTT",
    songTitle: "ASTRO DRIFT",
    quality: "8.9",
    requestedType: "verse",
    money: 120000,
    split: 25,
    deadlineWeeks: 2
  },
  {
    id: "in-3",
    artist: "LIL YACHTY",
    songTitle: "CONCRETE WAVE",
    quality: "7.6",
    requestedType: "beat",
    money: 65000,
    split: 15,
    deadlineWeeks: 1
  },
  {
    id: "in-4",
    artist: "21 SAVAGE",
    songTitle: "RED ZONE SLAUGHTER",
    quality: "8.2",
    requestedType: "mix",
    money: 85000,
    split: 18,
    deadlineWeeks: 3
  }
];

// Outbound Waiting Requests (player sent offer, awaiting acceptance/in progress)
let featOutboundWaiting = [
  {
    id: "out-w-1",
    artist: "KENDRICK LAMAR",
    songTitle: "CHROME 808S & HEARTBREAK",
    songQuality: "8.0",
    requestedType: "verse",
    money: 175000,
    split: 25,
    status: "Yet to Accept",
    deadlineWeeks: 2
  },
  {
    id: "out-w-2",
    artist: "METRO BOOMIN",
    songTitle: "808 REBELLION",
    songQuality: "7.1",
    requestedType: "beat",
    money: 85000,
    split: 20,
    status: "Yet to Accept",
    deadlineWeeks: 3
  },
  {
    id: "out-w-3",
    artist: "FUTURE",
    songTitle: "AFTERPARTY IN MIAMI",
    songQuality: "8.5",
    requestedType: "verse",
    money: 110000,
    split: 20,
    status: "Accepted",
    deadlineWeeks: 1
  },
  {
    id: "out-w-4",
    artist: "ICE SPICE",
    songTitle: "LATE NIGHT IN SHIBUYA",
    songQuality: "4.9",
    requestedType: "verse",
    money: 50000,
    split: 15,
    status: "Declined",
    deadlineWeeks: 0
  }
];

// Outbound Received Requests (received feature stems ready to accept/rework/decline)
let featOutboundReceived = [
  {
    id: "out-r-1",
    artist: "DRAKE",
    songTitle: "MIDNIGHT RENDEZVOUS",
    featQuality: "9.1",
    currentSongQ: "8.8",
    requestedType: "verse",
    money: 90000,
    split: 20
  },
  {
    id: "out-r-2",
    artist: "PLAYBOI CARTI",
    songTitle: "VANDALIZED HEART",
    featQuality: "4.6",
    currentSongQ: "7.8",
    requestedType: "verse",
    money: 90000,
    split: 20
  },
  {
    id: "out-r-3",
    artist: "CENTRAL CEE",
    songTitle: "TOKYO METRO DRIFT",
    featQuality: "8.2",
    currentSongQ: "6.2",
    requestedType: "verse",
    money: 90000,
    split: 20
  }
];

function switchFeatPrimaryTab(tabKey) {
  playMechanicalClick();
  activeFeatPrimaryTab = tabKey;
  const inTab = document.getElementById("featTabInbound");
  const outTab = document.getElementById("featTabOutbound");
  const subNav = document.getElementById("featOutboundSubNav");

  if (tabKey === "inbound") {
    if (inTab) inTab.classList.add("active");
    if (outTab) outTab.classList.remove("active");
    if (subNav) subNav.style.display = "none";
  } else {
    if (inTab) inTab.classList.remove("active");
    if (outTab) outTab.classList.add("active");
    if (subNav) subNav.style.display = "flex";
  }
  renderActiveFeatTab();
}

function switchOutboundSubTab(subKey) {
  playMechanicalClick();
  activeFeatOutboundSubTab = subKey;
  const wBtn = document.getElementById("featSubWaiting");
  const rBtn = document.getElementById("featSubRecieved");

  if (subKey === "waiting") {
    if (wBtn) wBtn.classList.add("active");
    if (rBtn) rBtn.classList.remove("active");
  } else {
    if (wBtn) wBtn.classList.remove("active");
    if (rBtn) rBtn.classList.add("active");
  }
  renderActiveFeatTab();
}

function renderActiveFeatTab() {
  const container = document.getElementById("featReqScrollBody");
  if (!container) return;
  container.innerHTML = "";

  const SPLIT_BRANCH_ICON = `<svg class="feat-split-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#221b16" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
    <path d="M4 12h7l7-7M11 12l7 7"></path>
    <circle cx="20" cy="5" r="2" fill="#221b16"></circle>
    <circle cx="20" cy="19" r="2" fill="#221b16"></circle>
    <circle cx="4" cy="12" r="2" fill="#221b16"></circle>
  </svg>`;

  if (activeFeatPrimaryTab === "inbound") {
    // 1. INBOUND TAB
    if (featInboundRequests.length === 0) {
      container.innerHTML = `
        <div class="feat-empty-state">
          <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <p>No Inbound Feature Requests at this time</p>
        </div>
      `;
      return;
    }

    featInboundRequests.forEach(req => {
      const card = document.createElement("div");
      card.className = "feat-card";
      card.innerHTML = `
        <div class="feat-card-left">
          <div class="feat-card-artist">${req.artist}</div>
          <div class="feat-card-song">"${req.songTitle}"</div>
          <div class="feat-meta-list">
            <div class="feat-meta-line"><span>QUALITY :</span> <span class="feat-val">${req.quality}</span></div>
            <div class="feat-meta-line"><span>REQUESTED :</span> <span class="feat-val">${req.requestedType.toUpperCase()}</span></div>
            <div class="feat-meta-line"><span>DEADLINE :</span> <span class="feat-deadline-badge">${req.deadlineWeeks} ${req.deadlineWeeks === 1 ? 'WEEK' : 'WEEKS'}</span></div>
          </div>
        </div>
        <div class="feat-card-right">
          <div class="feat-card-money">
            <span class="feat-dollar-symbol">$</span> ${req.money.toLocaleString()}$
          </div>
          <div class="feat-card-split">
            ${SPLIT_BRANCH_ICON}
            <span>${req.split}% SPLIT</span>
          </div>
          <div class="feat-card-actions">
            <button class="feat-btn-accept" onclick="acceptInboundFeat('${req.id}')">ACCEPT</button>
            <button class="feat-btn-decline" onclick="declineInboundFeat('${req.id}')">DECLINE</button>
          </div>
        </div>
      `;
      container.appendChild(card);
    });

  } else if (activeFeatOutboundSubTab === "waiting") {
    // 2. OUTBOUND WAITING TAB
    if (featOutboundWaiting.length === 0) {
      container.innerHTML = `
        <div class="feat-empty-state">
          <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <p>No Outbound Feature Requests Waiting</p>
          <button class="skeuo-btn skeuo-btn-coral" style="margin-top: 10px; padding: 6px 14px;" onclick="openNewFeatureOfferModal()">+ SEND NEW OFFER</button>
        </div>
      `;
      return;
    }

    featOutboundWaiting.forEach(req => {
      const card = document.createElement("div");
      card.className = "feat-card";

      let statusClass = "status-waiting";
      if (req.status === "Accepted") statusClass = "status-accepted";
      else if (req.status === "Declined") statusClass = "status-declined";

      let actionBtnHtml = "";
      if (req.status === "Yet to Accept") {
        actionBtnHtml = `<button class="feat-btn-decline" onclick="deleteOutboundWaiting('${req.id}')">DELETE REQUEST</button>`;
      } else if (req.status === "Accepted") {
        actionBtnHtml = `<button class="feat-btn-accept" onclick="switchOutboundSubTab('recieved')">VIEW IN RECIEVED</button>`;
      } else if (req.status === "Declined") {
        actionBtnHtml = `<button class="feat-btn-decline" onclick="dismissOutboundWaiting('${req.id}')">DISMISS</button>`;
      }

      card.innerHTML = `
        <div class="feat-card-left">
          <div class="feat-card-artist">${req.artist}</div>
          <div class="feat-card-song">"${req.songTitle}"</div>
          <div class="feat-meta-list">
            <div class="feat-meta-line"><span>SONG QUALITY :</span> <span class="feat-val">${req.songQuality}</span></div>
            <div class="feat-meta-line"><span>REQUESTED :</span> <span class="feat-val">${req.requestedType.toUpperCase()}</span></div>
            <div class="feat-meta-line"><span>STATUS :</span> <span class="feat-status-pill ${statusClass}">${req.status}</span></div>
            <div class="feat-meta-line"><span>DEADLINE :</span> <span class="feat-deadline-badge">${req.deadlineWeeks} ${req.deadlineWeeks === 1 ? 'WEEK' : 'WEEKS'}</span></div>
          </div>
        </div>
        <div class="feat-card-right">
          <div class="feat-card-money">
            <span class="feat-dollar-symbol">$</span> ${req.money.toLocaleString()}$
          </div>
          <div class="feat-card-split">
            ${SPLIT_BRANCH_ICON}
            <span>${req.split}% SPLIT</span>
          </div>
          <div class="feat-card-actions">
            ${actionBtnHtml}
          </div>
        </div>
      `;
      container.appendChild(card);
    });

  } else {
    // 3. OUTBOUND RECIEVED TAB
    if (featOutboundReceived.length === 0) {
      container.innerHTML = `
        <div class="feat-empty-state">
          <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <p>No Recieved Feature Stems to Manage</p>
          <button class="skeuo-btn skeuo-btn-coral" style="margin-top: 10px; padding: 6px 14px;" onclick="openNewFeatureOfferModal()">+ SEND NEW OFFER</button>
        </div>
      `;
      return;
    }

    featOutboundReceived.forEach(req => {
      const card = document.createElement("div");
      card.className = "feat-card";
      card.innerHTML = `
        <div class="feat-card-left">
          <div class="feat-card-artist">${req.artist}</div>
          <div class="feat-card-song">"${req.songTitle}"</div>
          <div class="feat-meta-list">
            <div class="feat-meta-line"><span>FEAT QUALITY :</span> <span class="feat-val q-feat">${req.featQuality}</span></div>
            <div class="feat-meta-line"><span>CURRENT SONG Q :</span> <span class="feat-val q-song">${req.currentSongQ}</span></div>
            <div class="feat-meta-line"><span>REQUESTED :</span> <span class="feat-val">${req.requestedType.toUpperCase()}</span></div>
          </div>
        </div>
        <div class="feat-card-right">
          <div class="feat-card-money">
            <span class="feat-dollar-symbol">$</span> ${req.money.toLocaleString()}$
          </div>
          <div class="feat-card-split">
            ${SPLIT_BRANCH_ICON}
            <span>${req.split}% SPLIT</span>
          </div>
          <div class="feat-card-actions">
            <button class="feat-btn-accept wide" onclick="acceptReceivedFeat('${req.id}')">ACCEPT</button>
            <div class="feat-received-actions">
              <button class="feat-btn-rework" onclick="reworkReceivedFeat('${req.id}')">SEND FOR REWORK</button>
              <button class="feat-btn-decline" onclick="declineReceivedFeat('${req.id}')">DECLINE</button>
            </div>
          </div>
        </div>
      `;
      container.appendChild(card);
    });
  }
}

// Actions: Inbound
function acceptInboundFeat(id) {
  const idx = featInboundRequests.findIndex(r => r.id === id);
  if (idx !== -1) {
    const req = featInboundRequests[idx];
    playMechanicalClick();
    careerMoney += req.money;
    const statusMoney = document.getElementById("statusMoney");
    if (statusMoney) statusMoney.textContent = `$${careerMoney.toLocaleString()}`;
    featInboundRequests.splice(idx, 1);
    showToast(`ACCEPTED FEAT FOR ${req.artist}! +$${req.money.toLocaleString()} ADVANCE`);
    renderActiveFeatTab();
  }
}

function declineInboundFeat(id) {
  const idx = featInboundRequests.findIndex(r => r.id === id);
  if (idx !== -1) {
    const req = featInboundRequests[idx];
    playMechanicalClick();
    featInboundRequests.splice(idx, 1);
    showToast(`DECLINED FEAT REQUEST FROM ${req.artist}`);
    renderActiveFeatTab();
  }
}

// Actions: Outbound Waiting
function deleteOutboundWaiting(id) {
  const idx = featOutboundWaiting.findIndex(r => r.id === id);
  if (idx !== -1) {
    const req = featOutboundWaiting[idx];
    if (req.status !== "Yet to Accept") {
      showToast("Cannot delete request once accepted by artist!");
      return;
    }
    playMechanicalClick();
    featOutboundWaiting.splice(idx, 1);
    showToast(`DELETED FEATURE REQUEST TO ${req.artist}`);
    renderActiveFeatTab();
  }
}

function dismissOutboundWaiting(id) {
  const idx = featOutboundWaiting.findIndex(r => r.id === id);
  if (idx !== -1) {
    playMechanicalClick();
    featOutboundWaiting.splice(idx, 1);
    renderActiveFeatTab();
  }
}

// Actions: Outbound Received
function acceptReceivedFeat(id) {
  const idx = featOutboundReceived.findIndex(r => r.id === id);
  if (idx !== -1) {
    const req = featOutboundReceived[idx];
    playMechanicalClick();
    const targetSong = FULL_CATALOGUE_DATA.find(s => s.type === "song" && !s.isReleased && s.title.toUpperCase() === req.songTitle.toUpperCase());
    let boostMsg = "";
    if (targetSong) {
      const oldQ = parseFloat(targetSong.quality) || 7.0;
      const featQ = parseFloat(req.featQuality) || 8.0;
      const newQ = Math.min(9.9, Math.max(oldQ, (oldQ * 0.7 + featQ * 0.35))).toFixed(1);
      targetSong.quality = newQ;
      targetSong.details = (targetSong.details || "") + ` • Feat. ${req.artist} (${req.requestedType})`;
      boostMsg = ` • Song quality upgraded to ${newQ}!`;
    }
    featOutboundReceived.splice(idx, 1);
    showToast(`ACCEPTED ${req.artist} FEAT${boostMsg}`);
    renderActiveFeatTab();
    renderCatalogueFull();
  }
}

function reworkReceivedFeat(id) {
  const idx = featOutboundReceived.findIndex(r => r.id === id);
  if (idx !== -1) {
    const req = featOutboundReceived[idx];
    playMechanicalClick();
    featOutboundReceived.splice(idx, 1);
    featOutboundWaiting.unshift({
      id: "out-w-rw-" + Date.now(),
      artist: req.artist,
      songTitle: req.songTitle,
      songQuality: req.currentSongQ,
      requestedType: req.requestedType + " (Rework)",
      money: req.money,
      split: req.split,
      status: "Yet to Accept",
      deadlineWeeks: 2
    });
    showToast(`SENT ${req.artist}'S STEMS FOR REWORK (Fee retained, 2 weeks)`);
    renderActiveFeatTab();
  }
}

function declineReceivedFeat(id) {
  const idx = featOutboundReceived.findIndex(r => r.id === id);
  if (idx !== -1) {
    const req = featOutboundReceived[idx];
    playMechanicalClick();
    featOutboundReceived.splice(idx, 1);
    showToast(`DECLINED ${req.artist}'S STEMS • Split Voided (${req.split}%)`);
    renderActiveFeatTab();
  }
}

// Modal (+) New Feature Offer
function openNewFeatureOfferModal() {
  playMechanicalClick();
  const songSelect = document.getElementById("featOfferSongSelect");
  if (songSelect) {
    songSelect.innerHTML = "";
    const unreleased = FULL_CATALOGUE_DATA.filter(i => i.type === "song" && !i.isReleased);
    if (unreleased.length === 0) {
      songSelect.innerHTML = `<option value="">(No Unreleased Songs - Record in Studio first)</option>`;
    } else {
      unreleased.forEach(s => {
        const opt = document.createElement("option");
        opt.value = s.title;
        opt.textContent = `${s.title} (Q: ${s.quality})`;
        opt.dataset.quality = s.quality;
        songSelect.appendChild(opt);
      });
    }
    onFeatOfferSongChange();
  }
  const modal = document.getElementById("newFeatureOfferModal");
  if (modal) modal.classList.add("active");
}

function closeNewFeatureOfferModal() {
  playMechanicalClick();
  const modal = document.getElementById("newFeatureOfferModal");
  if (modal) modal.classList.remove("active");
}

function onFeatOfferSongChange() {
  const songSelect = document.getElementById("featOfferSongSelect");
  const qEl = document.getElementById("featOfferSongQ");
  if (songSelect && qEl) {
    const opt = songSelect.selectedOptions[0];
    qEl.textContent = opt && opt.dataset.quality ? opt.dataset.quality : "--";
  }
}

function selectFeatOfferType(type) {
  playMechanicalClick();
  featOfferSelectedType = type;
  ["verse", "beat", "mix"].forEach(t => {
    const el = document.getElementById(`featType_${t}`);
    if (el) {
      if (t === type) el.classList.add("active");
      else el.classList.remove("active");
    }
  });
}

function setFeatOfferFee(fee) {
  playMechanicalClick();
  const input = document.getElementById("featOfferFeeInput");
  if (input) input.value = fee;
  const presets = [25000, 50000, 90000, 150000];
  presets.forEach(p => {
    const el = document.getElementById(`presetFee${p / 1000}`);
    if (el) {
      if (p === fee) el.classList.add("active");
      else el.classList.remove("active");
    }
  });
}

function setFeatOfferSplit(split) {
  playMechanicalClick();
  const input = document.getElementById("featOfferSplitInput");
  if (input) input.value = split;
  const presets = [10, 15, 20, 25];
  presets.forEach(p => {
    const el = document.getElementById(`presetSplit${p}`);
    if (el) {
      if (p === split) el.classList.add("active");
      else el.classList.remove("active");
    }
  });
}

function submitNewFeatureOffer() {
  playMechanicalClick();
  const artistSelect = document.getElementById("featOfferArtistSelect");
  const songSelect = document.getElementById("featOfferSongSelect");
  const feeInput = document.getElementById("featOfferFeeInput");
  const splitInput = document.getElementById("featOfferSplitInput");

  const artist = artistSelect ? artistSelect.value : "DRAKE";
  const song = songSelect ? songSelect.value : "";
  const fee = parseInt(feeInput ? feeInput.value : 90000, 10) || 50000;
  const split = parseInt(splitInput ? splitInput.value : 20, 10) || 20;

  if (!song) {
    showToast("Please choose an unreleased song first!");
    return;
  }

  if (careerMoney < fee) {
    showToast(`INSUFFICIENT FUNDS! Need $${fee.toLocaleString()} upfront fee.`);
    return;
  }

  careerMoney -= fee;
  const statusMoney = document.getElementById("statusMoney");
  if (statusMoney) statusMoney.textContent = `$${careerMoney.toLocaleString()}`;

  const opt = songSelect.selectedOptions[0];
  const songQ = opt && opt.dataset.quality ? opt.dataset.quality : "7.5";

  featOutboundWaiting.unshift({
    id: "out-w-" + Date.now(),
    artist: artist,
    songTitle: song,
    songQuality: songQ,
    requestedType: featOfferSelectedType,
    money: fee,
    split: split,
    status: "Yet to Accept",
    deadlineWeeks: 3
  });

  closeNewFeatureOfferModal();
  activeFeatPrimaryTab = "outbound";
  activeFeatOutboundSubTab = "waiting";

  // Update Tab UI
  const inTab = document.getElementById("featTabInbound");
  const outTab = document.getElementById("featTabOutbound");
  if (inTab) inTab.classList.remove("active");
  if (outTab) outTab.classList.add("active");
  const subNav = document.getElementById("featOutboundSubNav");
  if (subNav) subNav.style.display = "flex";
  const wBtn = document.getElementById("featSubWaiting");
  const rBtn = document.getElementById("featSubRecieved");
  if (wBtn) wBtn.classList.add("active");
  if (rBtn) rBtn.classList.remove("active");

  showToast(`SENT FEATURE REQUEST TO ${artist} FOR "${song}"!`);
  renderActiveFeatTab();
}

// Real-Time Simulation Hook: Deadlines advance each week
function advanceFeatRequestsWeek() {
  // 1. Advance Inbound Deadlines
  for (let i = featInboundRequests.length - 1; i >= 0; i--) {
    featInboundRequests[i].deadlineWeeks--;
    if (featInboundRequests[i].deadlineWeeks <= 0) {
      const expired = featInboundRequests.splice(i, 1)[0];
      showToast(`Inbound request from ${expired.artist} expired.`);
    }
  }

  // 2. Advance Outbound Waiting Deadlines & Probabilistic Artist Responses
  for (let i = featOutboundWaiting.length - 1; i >= 0; i--) {
    const item = featOutboundWaiting[i];
    item.deadlineWeeks--;
    if (item.status === "Yet to Accept") {
      if (item.deadlineWeeks <= 0) {
        item.status = "Declined";
        item.deadlineWeeks = 0;
      } else {
        if (Math.random() < 0.5) {
          const generatedFeatQ = (Math.floor(Math.random() * 28) + 70) / 10;
          featOutboundReceived.unshift({
            id: "out-r-" + Date.now(),
            artist: item.artist,
            songTitle: item.songTitle,
            featQuality: generatedFeatQ.toFixed(1),
            currentSongQ: item.songQuality,
            requestedType: item.requestedType,
            money: item.money,
            split: item.split
          });
          featOutboundWaiting.splice(i, 1);
          showToast(`${item.artist} ACCEPTED & DELIVERED FEATURE FOR "${item.songTitle}"! Check RECIEVED tab.`);
        }
      }
    }
  }

  // 3. Chance of new Inbound request arriving from ecosystem (35% chance)
  if (Math.random() < 0.35 && featInboundRequests.length < 5) {
    const NPC_ARTISTS = [
      "PLAYBOI CARTI", "DRAKE", "TRAVIS SCOTT", "METRO BOOMIN",
      "21 SAVAGE", "KENDRICK LAMAR", "LIL YACHTY", "CENTRAL CEE",
      "FUTURE", "DON TOLIVER", "ICE SPICE", "J. COLE", "GUNNA"
    ];
    const NPC_SONGS = [
      "NO LIMITS", "NIGHT CALL", "TOP FLOOR", "TOKYO DRIFT V2",
      "COLD SHOULDER", "GHOSTWRITER CIPHER", "DOUBLE CUP", "808 BLUES",
      "MIDNIGHT MEMORIES", "GOLDEN HOURS", "FAST LANE"
    ];
    const TYPES = ["verse", "beat", "mix"];
    const randomArtist = NPC_ARTISTS[Math.floor(Math.random() * NPC_ARTISTS.length)];
    const randomSong = NPC_SONGS[Math.floor(Math.random() * NPC_SONGS.length)];
    const randomType = TYPES[Math.floor(Math.random() * TYPES.length)];
    const randomFee = (Math.floor(Math.random() * 10) + 5) * 10000;
    const randomSplit = (Math.floor(Math.random() * 3) + 3) * 5;
    const randomQ = (Math.floor(Math.random() * 20) + 75) / 10;

    featInboundRequests.unshift({
      id: "in-" + Date.now(),
      artist: randomArtist,
      songTitle: randomSong,
      quality: randomQ.toFixed(1),
      requestedType: randomType,
      money: randomFee,
      split: randomSplit,
      deadlineWeeks: 3
    });
  }

  // 4. Update in real-time if currently viewed
  renderActiveFeatTab();
}

// Promotion & Merchandising (5 Main Hub Buttons)
function openPromoInterviews() {
  playMechanicalClick();
  showToast("INTERVIEWS: Press Circuit & Media Tours");
}

function openPromoMerch() {
  playMechanicalClick();
  showToast("MERCH: Drops, Apparel & Store Inventory");
}

function openPromoPhysicalCopies() {
  playMechanicalClick();
  showToast("PHYSICAL COPIES: Vinyl, CD Digipaks & Cassettes");
}

function openPromoRunAds() {
  playMechanicalClick();
  showToast("RUN ADS: Billboards & DSP Editorial Campaigns");
}

function openPromoListeningParties() {
  playMechanicalClick();
  showToast("LISTENING PARTIES: Exclusive Pre-Release Popups");
}

function orderPhysicalBatch(format, units, cost) {
  playMechanicalClick();
  showToast(`${format.toUpperCase()} PRESSING: PHASE 2 DEVELOPMENT`);
}

function launchPromoCampaign(title, cost, impact) {
  playMechanicalClick();
  showToast(`${title.toUpperCase()}: PHASE 2 DEVELOPMENT`);
}

// --- Socials & Industry Apps Hub ---
const SOCIAL_APPS_DATA = {
  calendar: {
    title: "CALENDAR & SCHEDULE",
    badge: "PLANNER",
    description: "TRACK UPCOMING ALBUM RELEASES, STUDIO SESSIONS, PRESS INTERVIEWS, TOUR DATES, AND INDUSTRY AWARD DEADLINES.",
    iconHtml: `
      <div class="app-icon-chassis calendar-icon">
        <div class="cal-top-strip">
          <span class="cal-pin"></span>
          <span class="cal-pin"></span>
        </div>
        <span class="cal-date-num">${careerWeek}</span>
        <span class="cal-month-lbl">WEEK</span>
      </div>
    `,
    features: [
      "SCHEDULE SINGLE & ALBUM DROP DATES WITH LABEL APPROVAL",
      "MANAGE STUDIO LOCK-IN CALENDAR & PRODUCER SESSIONS",
      "BOOK PRESS INTERVIEWS, RADIO JUNKETS & PODCASTS",
      "TRACK ANNUAL GRAMMY & BET NOMINATION CUTOFFS"
    ]
  },
  news: {
    title: "INDUSTRY NEWS WIRE",
    badge: "PRESS",
    description: "STAY UPDATED WITH HISTORICAL ARCHIVES AND LIVE BREAKING HEADLINES FROM THE RAP ECOSYSTEM.",
    iconHtml: `
      <div class="app-icon-chassis news-app-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/>
          <path d="M18 14h-8"/>
          <path d="M15 18h-5"/>
          <path d="M10 6h8v4h-8V6Z"/>
        </svg>
      </div>
    `,
    features: [
      "BREAKING NEWS REPORTS ON INDUSTRY SALES & MILESTONES",
      "OP-ED EDITORIALS ON RAP DRAMA & EMERGING SUBGENRES",
      "WEEKLY LABEL SHUFFLES & A&R SIGNING ANNOUNCEMENTS",
      "ARCHIVED PRESS COVERAGE OF YOUR CAREER HIGHLIGHTS"
    ]
  },
  beatstore: {
    title: "ONLINE BEAT STORE",
    badge: "MARKETPLACE",
    description: "BUY, LEASE, SELL, AND MANAGE INSTRUMENTALS ONLINE WITH INDUSTRY-STANDARD CONTRACTS & STEM EXPORTS.",
    iconHtml: `
      <div class="app-icon-chassis beatstore-icon">
        <div class="mpc-grid-pads">
          <span class="mpc-pad active-cyan"></span>
          <span class="mpc-pad active-amber"></span>
          <span class="mpc-pad active-pink"></span>
          <span class="mpc-pad active-cyan"></span>
        </div>
      </div>
    `,
    features: [
      "BROWSE & LEASE INDUSTRY INSTRUMENTALS (MP3 / WAV / STEMS)",
      "SELL UNUSED BEAT PACKS TO UPCOMING ARTISTS FOR PASSIVE CASH",
      "CUSTOM CONTRACT BUILDER WITH EXCLUSIVE RIGHTS OPTIONS",
      "INSTANT SAMPLE CLEARANCE & ROYALTY SPLIT INTEGRATION"
    ]
  },
  concerts: {
    title: "CONCERTS & VENUES",
    badge: "LIVE TOURING",
    description: "BOOK ARENA & CLUB VENUES, MANAGE TICKET GROSS, COORDINATE MERCH BOOTHS, AND ORGANIZE WORLD TOURS.",
    iconHtml: `
      <div class="app-icon-chassis concerts-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/>
          <path d="M13 5v2"/>
          <path d="M13 17v2"/>
          <path d="M13 11v2"/>
        </svg>
      </div>
    `,
    features: [
      "BOOK LOCAL CLUBS, THEATERS, AMPHITHEATERS, AND STADIUMS",
      "NEGOTIATE PROMOTER GUARANTEES & BACK-END TICKET SPLITS",
      "SET TICKET TIERS: VIP EXPERIENCES, GA TICKETS, AND EARLY ACCESS",
      "MONITOR TICKET SALES VELOCITY & RESALE VALUE IN REAL TIME"
    ]
  },
  messenger: {
    title: "ARTIST MESSENGER",
    badge: "DMs & NETWORK",
    description: "SECURE DIRECT MESSAGING TO NEGOTIATE COLLABORATIONS, BUILD ALLIANCES, SEND DEMOS, OR EXCHANGE WORDS.",
    iconHtml: `
      <div class="app-icon-chassis messenger-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
        </svg>
        <span class="msg-unread-pip">3</span>
      </div>
    `,
    features: [
      "DIRECT DMS WITH INDUSTRY PEERS, LEGENDS, AND A&RS",
      "NEGOTIATE FEATURE PRICING & TURN-AROUND TIMES DIRECTLY",
      "TRADE UNRELEASED DEMOS & BEAT IDEAS SECURELY",
      "HANDLE INCOMING COLLABORATION REQUESTS AND PRODUCER CONTACTS"
    ]
  },
  tumble: {
    title: "TUMBLE MATCHMAKER",
    badge: "VIP DATING",
    description: "THE EXCLUSIVE CELEBRITY AND HIGH-PROFILE DATING APP FOR ARTISTS, INFLUENCERS, AND CREATIVES.",
    iconHtml: `
      <div class="app-icon-chassis tumble-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>
        <span class="tumble-flame-pip">&#128293;</span>
      </div>
    `,
    features: [
      "SWIPE ON VERIFIED INDUSTRY STARS, MODELS, AND PRODUCERS",
      "BOOST YOUR CLOUT WITH HIGH-PROFILE CELEBRITY ROMANCES",
      "ATTEND VIP INDUSTRY AFTERPARTIES AND RED-CARPET EVENTS",
      "NAVIGATE TABLOID DATING SCANDALS AND SOCIAL MEDIA SPECULATION"
    ]
  },
  beef: {
    title: "BEEF & FEUD RADAR",
    badge: "RIVALRIES",
    description: "TRACK RAP BEEFS, INDUSTRY DRAMA, SUBLIMINAL TWEETS, DISS TRACK RADARS, AND COLLATERAL DAMAGE.",
    iconHtml: `
      <div class="app-icon-chassis beef-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <path d="M14.5 17.5 3 6V3h3l11.5 11.5"/>
          <path d="m13 19 6 2 2-6-2-2-6 6z"/>
          <path d="M9.5 6.5 18 15"/>
        </svg>
        <span class="beef-skull-pip">&#9760;</span>
      </div>
    `,
    features: [
      "REAL-TIME RADAR OF ACTIVE INDUSTRY FEUDS AND TENSION",
      "RECORD & DEPLOY DEVASTATING DISS TRACKS WITH VIRAL REPUTATION RISKS",
      "MONITOR FAN AND MEDIA REACTIONS TO SUBLIMINAL SHOTS",
      "MEDIATE PUBLIC SQUASHES OR ESCALATE TO FULL-BLOWN RAP WARS"
    ]
  },
  livee: {
    title: "LIVEE STREAM BROADCAST",
    badge: "STREAMING",
    description: "GO LIVE DIRECTLY FROM THE STUDIO OR TOUR BUS TO INTERACT WITH DIEHARD FANS, PREVIEW SNIPPETS, AND DRIVE HYPE.",
    iconHtml: `
      <div class="app-icon-chassis livee-icon">
        <svg width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <path d="m16 16 6 4V4l-6 4"/>
          <rect x="2" y="6" width="14" height="12" rx="2"/>
        </svg>
        <span class="livee-badge-tag">LIVE</span>
      </div>
    `,
    features: [
      "GO LIVE TO THOUSANDS OF FANS AND PREVIEW VAULT SNIPPETS",
      "RECEIVE LIVE FAN DONATIONS, SUPERCHATS, AND VIRTUAL GIFTS",
      "HOST GUEST STREAMS WITH OTHER ARTISTS AND COLLABORATORS",
      "GENERATE VIRAL SOCIAL CLIPS THAT BOOST STREAMING ALGORITHMS"
    ]
  }
};

function openSocialApp(appName) {
  playMechanicalClick();
  if (appName === "slander" || appName === "imdb" || appName === "critiq") {
    openAnalyzeApp(appName, "social");
  } else if (appName === "hot100") {
    openHot100ChartModal();
  } else {
    openSocialPlaceholder(appName);
  }
}

function openSocialPlaceholder(appName) {
  const data = SOCIAL_APPS_DATA[appName];
  if (!data) return;

  const hub = document.getElementById("socialMainHub");
  const view = document.getElementById("socialAppPlaceholderView");
  if (!view) return;

  if (hub) hub.style.display = "none";

  const titleEl = document.getElementById("socialPlaceholderTitle");
  const badgeEl = document.getElementById("socialPlaceholderBadge");
  const descEl = document.getElementById("socialPlaceholderDesc");
  const featuresEl = document.getElementById("socialPlaceholderFeatures");
  const iconWrapEl = document.getElementById("socialPlaceholderIconWrap");

  if (titleEl) titleEl.textContent = data.title;
  if (badgeEl) badgeEl.textContent = data.badge;
  if (descEl) descEl.textContent = data.description;
  if (iconWrapEl) iconWrapEl.innerHTML = data.iconHtml;

  if (featuresEl) {
    featuresEl.innerHTML = data.features.map(f => `
      <div class="feature-item">
        <span class="feature-check">✓</span>
        <span>${f}</span>
      </div>
    `).join("");
  }

  view.style.display = "flex";
  view.scrollTop = 0;
}

function closeSocialPlaceholder() {
  playMechanicalClick();
  const view = document.getElementById("socialAppPlaceholderView");
  const hub = document.getElementById("socialMainHub");
  if (view) view.style.display = "none";
  if (hub) hub.style.display = "flex";
}

// --- Settings Subpage Handlers (Accessed via Home Top Bar) ---
function openSettingsSubpage() {
  playMechanicalClick();
  switchTab("setting");
}

function closeSettingsSubpage() {
  playMechanicalClick();
  switchTab("home");
}

// --- Profile Tab & Empire Hub Engine ---
const PROFILE_MODULES_DATA = {
  labels: {
    title: "RECORD LABELS & CONTRACTS",
    badge: "RECORD DEALS",
    description: "MANAGE YOUR SIGNED RECORD LABEL PARTNERSHIP, REVIEW INCOMING 360 & DISTRIBUTION DEALS, AND REQUEST CONTRACT AUDITS.",
    iconHtml: `
      <div style="filter: drop-shadow(0 3px 6px rgba(0,0,0,0.4)); display: flex; align-items: center; justify-content: center;">
        <svg width="54" height="60" viewBox="0 0 54 60" fill="none">
          <rect x="2" y="2" width="50" height="56" rx="4" fill="#faf8f2" stroke="#d4c2b0" stroke-width="1.5"/>
          <path d="M40 2 L52 14 L40 14 Z" fill="#d4c2b0"/>
          <circle cx="16" cy="14" r="7" fill="url(#goldSealP)" stroke="#b45309" stroke-width="1"/>
          <line x1="10" y1="28" x2="44" y2="28" stroke="#cbd5e1" stroke-width="2" stroke-linecap="round"/>
          <line x1="10" y1="34" x2="38" y2="34" stroke="#cbd5e1" stroke-width="2" stroke-linecap="round"/>
          <line x1="10" y1="40" x2="42" y2="40" stroke="#cbd5e1" stroke-width="2" stroke-linecap="round"/>
          <path d="M10 50 Q 20 42, 28 50 T 42 48" stroke="#1e3a8a" stroke-width="2" stroke-linecap="round" fill="none"/>
          <defs>
            <linearGradient id="goldSealP" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fef08a"/>
              <stop offset="100%" stop-color="#b45309"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
    `,
    features: [
      "VIEW SIGNED RECORD LABEL STATUS & ROSTER",
      "NEGOTIATE ADVANCE CASH & MASTER ROYALTY SPLITS",
      "CHOOSE BETWEEN 360, 50/50 INDIE, OR DISTRIBUTION DEALS",
      "REQUEST LABEL AUDITS OR BUY BACK YOUR MASTER TAPES"
    ]
  },
  management: {
    title: "MEDIA & TALENT MANAGEMENT",
    badge: "AGENCY",
    description: "HIRE INDUSTRY MANAGERS, NEGOTIATE COMMISSION RATES, SCHEDULE PRESS CIRCUITS, AND DEPLOY CRISIS PR DAMAGE CONTROL.",
    iconHtml: `
      <div style="filter: drop-shadow(0 4px 8px rgba(0,0,0,0.4));">
        <svg width="50" height="58" viewBox="0 0 50 58" fill="none">
          <rect x="4" y="8" width="42" height="48" rx="6" fill="#0f172a" stroke="#ca8a04" stroke-width="1.5"/>
          <rect x="19" y="3" width="12" height="6" rx="2" fill="#94a3b8" stroke="#cbd5e1" stroke-width="1"/>
          <circle cx="25" cy="25" r="7" fill="url(#mgmtGoldP)"/>
          <path d="M13 46 C13 38 18 35 25 35 C32 35 37 38 37 46 Z" fill="url(#mgmtGoldP)"/>
          <circle cx="12" cy="22" r="2.5" fill="#38bdf8"/>
          <circle cx="38" cy="22" r="2.5" fill="#38bdf8"/>
          <defs>
            <linearGradient id="mgmtGoldP" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fef08a"/>
              <stop offset="100%" stop-color="#ca8a04"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
    `,
    features: [
      "SIGN TOP-TIER MUSIC MANAGERS & TALENT AGENTS",
      "NEGOTIATE 10%-15% MANAGEMENT COMMISSION CUTS",
      "EXECUTE CRISIS PR & EMERGENCY DAMAGE CONTROL CAMPAIGNS",
      "COORDINATE RED-CARPET JUNKETS & HIGH-PROFILE PRESS BLITZES"
    ]
  },
  certifications: {
    title: "RIAA PLAQUES & CERTIFICATIONS",
    badge: "RIAA AUDIT",
    description: "TRACK OFFICIAL RIAA GOLD, PLATINUM, MULTI-PLATINUM, AND DIAMOND CERTIFICATIONS FOR YOUR SINGLES AND ALBUMS.",
    iconHtml: `
      <div style="width: 58px; height: 58px; border-radius: 14px; background-image: url('assets/certifications_wall.jpg'); background-size: cover; background-position: 5% 45%; border: 1.5px solid rgba(255,255,255,0.4); box-shadow: 0 6px 14px rgba(0,0,0,0.5); overflow: hidden;"></div>
    `,
    features: [
      "AUDIT ELIGIBILITY FOR OFFICIAL RIAA GOLD & PLATINUM DISCS",
      "COMMEMORATIVE SHADOWBOX WALL FOR RECORD MILESTONES",
      "COMMISSION CUSTOM PLAQUES FOR PRODUCERS & FEATURE ARTISTS",
      "TRACK GLOBAL TERRITORY STREAMING CERTIFICATION CUTOFFS"
    ]
  },
  awards: {
    title: "AWARDS & TROPHY CABINET",
    badge: "TROPHY CASE",
    description: "INSPECT YOUR SHOWCASE OF GRAMMYS, BET AWARDS, VMAS, AND BILLBOARD MUSIC AWARDS EARNED THROUGHOUT YOUR RAP CAREER.",
    iconHtml: `
      <div style="width: 58px; height: 58px; border-radius: 14px; background-image: url('assets/awards_room.jpg'); background-size: cover; background-position: center 65%; border: 1.5px solid rgba(255,255,255,0.4); box-shadow: 0 6px 14px rgba(0,0,0,0.5); overflow: hidden;"></div>
    `,
    features: [
      "INTERACTIVE 3D TROPHY CASE (GRAMMYS, BET, VMAS, BMAS)",
      "BROWSE HISTORICAL NOMINATIONS & CATEGORY WIN PERCENTAGES",
      "DELIVER VIRAL ACCEPTANCE SPEECHES TO BOOST STREET REP",
      "UNLOCK RAP LEGEND MILESTONES & HALL OF FAME INDUCTION"
    ]
  },
  deals: {
    title: "COMMERCIAL & BRAND DEALS",
    badge: "SPONSORSHIPS",
    description: "MONETIZE YOUR ARTISTIC CLOUT THROUGH SNEAKER COLLABORATIONS, MOVIE CAMEOS, ENERGY DRINK DEALS, AND TOUR SPONSORSHIPS.",
    iconHtml: `
      <div style="filter: drop-shadow(0 3px 6px rgba(0,0,0,0.5));">
        <svg width="64" height="44" viewBox="0 0 60 42" fill="none">
          <path d="M14 2 L56 2 C58 2, 59 3, 59 5 L59 37 C59 39, 58 40, 56 40 L14 40 L2 21 Z" fill="url(#dealTagGradP)" stroke="#fbbf24" stroke-width="1.5"/>
          <circle cx="16" cy="21" r="4.5" fill="#3e1b07" stroke="#fef08a" stroke-width="1.2"/>
          <text x="36" y="26" fill="#fffbeb" font-size="12" font-weight="900" letter-spacing="1" text-anchor="middle" font-family="sans-serif">DEALS</text>
          <defs>
            <linearGradient id="dealTagGradP" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#d97706"/>
              <stop offset="50%" stop-color="#b45309"/>
              <stop offset="100%" stop-color="#78350f"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
    `,
    features: [
      "NEGOTIATE SIGNATURE SNEAKER & LUXURY STREETWEAR LINES",
      "LOCK IN HOLLYWOOD SOUNDTRACK & FEATURE FILM CAMEO DEALS",
      "SIGN MULTI-MILLION BEVERAGE & TECH BRAND ENDORSEMENTS",
      "SECURE HEADLINE TOURING SPONSORSHIPS & ARENA BRANDING"
    ]
  },
  sidehustle: {
    title: "SIDE HUSTLE & GIG WORK",
    badge: "HUSTLE",
    description: "EARN PASSIVE AND ACTIVE INCOME OUTSIDE THE BOOTH THROUGH GHOSTWRITING, MENIAL JOBS, STUDIO GUITAR/KEYS, AND NIGHTCLUB HOSTING.",
    iconHtml: `
      <div style="width: 52px; height: 52px; border-radius: 12px; background: linear-gradient(180deg, #243358 0%, #131c33 100%); border: 1.5px solid #4A919E; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#4A919E" stroke-width="2.2">
          <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
        </svg>
      </div>
    `,
    features: [
      "MENIAL JOBS (BARISTA, WAREHOUSE, NIGHT COURIER) FOR SURVIVAL CASH",
      "STUDIO SESSION GUITARIST, BASSIST & SYNTH PLAYER GIGS",
      "GHOSTWRITE 16-BAR VERSES & HOOKS FOR INDUSTRY RAPPERS",
      "SECURE $5K-$25K NIGHTCLUB CELEBRITY HOSTING FEES"
    ]
  },
  relations: {
    title: "LOVE RELATIONS, FAMILY & CREW",
    badge: "RELATIONSHIPS",
    description: "NAVIGATE HIGH-PROFILE CELEBRITY ROMANCES, SUPPORT KIDS AND FAMILY HOUSEHOLDS, AND MAINTAIN LOYALTY WITH YOUR DAY-ONE CREW.",
    iconHtml: `
      <div style="width: 52px; height: 52px; border-radius: 12px; background: linear-gradient(180deg, #99383e 0%, #6e2025 100%); border: 1.5px solid #d4636b; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
        <svg width="30" height="30" viewBox="0 0 24 24" fill="url(#coralHeartSub)">
          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
          <defs>
            <linearGradient id="coralHeartSub" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#ff999b"/>
              <stop offset="50%" stop-color="#CE6A6B"/>
              <stop offset="100%" stop-color="#991b1b"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
    `,
    features: [
      "NAVIGATE CELEBRITY DATING, ROMANCE & PUBLIC RELATIONSHIPS",
      "SUPPORT KIDS, PARENTS & PURCHASE FAMILY LUXURY HOMES",
      "MAINTAIN BROTHERHOOD & DAY-ONE INNER CIRCLE CREW LOYALTY",
      "BALANCE ROMANTIC TABLOID DRAMA WITH STUDIO WORK ETHIC"
    ]
  },
  wiki: {
    title: "ARTIST WIKI & CAREER ARCHIVE",
    badge: "ENCYCLOPEDIA",
    description: "THE DEFINITIVE CAREER ARCHIVE COMPILING EVERY RELEASE, SALES BENCHMARK, ALL-TIME RECORD HELD, AND RELATIONSHIP MILESTONE.",
    iconHtml: `
      <div class="wiki-emblem-badge" style="width: 52px; height: 52px; font-size: 1.8rem; border-radius: 10px;">
        W
      </div>
    `,
    features: [
      "COMPLETE DISCOGRAPHY CATALOG WITH TOTAL UNITS & REVENUE",
      "HISTORICAL ALL-TIME RECORDS HELD & CHART-TOPPING STREAKS",
      "DETAILED RELATIONSHIP, BEEF & CREW EVOLUTION TIMELINE",
      "STREAMING ERA PERFORMANCE SCORE & ALL-TIME LEGACY RANKING"
    ]
  },
  leisure: {
    title: "LIFESTYLE, LEISURE & VIP NIGHTLIFE",
    badge: "LIFESTYLE",
    description: "UNWIND FROM HIGH-PRESSURE STUDIO SESSIONS WITH HIGH-STAKES CASINO GAMBLING, VIP NIGHTCLUB BOTTLE SERVICE, LUXURY OVERSEAS VACATIONS, AND EXOTIC CAR TRACK DAYS.",
    iconHtml: `
      <div style="width: 58px; height: 58px; border-radius: 14px; background-image: url('assets/leisure_beach.jpg'); background-size: cover; background-position: 15% 82%; border: 1.5px solid rgba(255,255,255,0.4); box-shadow: 0 6px 14px rgba(0,0,0,0.5); overflow: hidden;"></div>
    `,
    features: [
      "HIGH-ROLLER CASINO BLACKJACK, ROULETTE & PRIVATE POKER",
      "VIP BOTTLE SERVICE & CELEBRITY NIGHTCLUB AFTERPARTIES",
      "LUXURY YACHT CHARTERS & PRIVATE ISLAND ESCAPES IN IBIZA",
      "SUPERCAR RENTALS & HIGH-SPEED TRACK DAYS TO RELIEVE FATIGUE"
    ]
  }
};

function openProfileModule(moduleKey) {
  playMechanicalClick();
  const data = PROFILE_MODULES_DATA[moduleKey];
  if (!data) return;

  const hub = document.getElementById("profileMainHub");
  const view = document.getElementById("profileAppPlaceholderView");
  if (!view) return;

  if (hub) hub.style.display = "none";

  const titleEl = document.getElementById("profilePlaceholderTitle");
  const badgeEl = document.getElementById("profilePlaceholderBadge");
  const descEl = document.getElementById("profilePlaceholderDesc");
  const featuresEl = document.getElementById("profilePlaceholderFeatures");
  const iconWrapEl = document.getElementById("profilePlaceholderIconWrap");

  if (titleEl) titleEl.textContent = data.title;
  if (badgeEl) badgeEl.textContent = data.badge;
  if (descEl) descEl.textContent = data.description;
  if (iconWrapEl) iconWrapEl.innerHTML = data.iconHtml;

  if (featuresEl) {
    featuresEl.innerHTML = data.features.map(f => `
      <div class="feature-item">
        <span class="feature-check">✓</span>
        <span>${f}</span>
      </div>
    `).join("");
  }

  view.style.display = "flex";
  view.scrollTop = 0;
}

function closeProfilePlaceholder() {
  playMechanicalClick();
  const view = document.getElementById("profileAppPlaceholderView");
  const hub = document.getElementById("profileMainHub");
  if (view) view.style.display = "none";
  if (hub) hub.style.display = "flex";
}

// --- Initialize App ---
document.addEventListener("DOMContentLoaded", () => {
  initHardwoodTheme();
  renderShawtifyCatalog();
  updateCalendarEngineUI();
  updateClock();
  setInterval(updateClock, 10000);
  setupFrameToggle();

  // Support direct tab routing via hash (e.g. #media, #studio, #profile, #setting, #settings, #catalogue, etc.)
  const hash = window.location.hash.replace("#", "").toLowerCase();
  if (hash === "create") {
    switchTab("create");
  } else if (hash === "release") {
    openStudioReleaseTab();
  } else if (hash === "settings" || hash === "setting") {
    switchTab("setting");
  } else if (hash === "profile") {
    switchTab("profile");
  } else if (hash === "studio") {
    switchTab("studio");
  } else if (hash === "catalogue") {
    openStudioCatalogueTab();
  } else if (hash === "catalogue-inspect") {
    openStudioCatalogueTab();
    setTimeout(() => inspectCatalogueItem("cat-s1"), 300);
  } else if (hash === "feat-req" || hash === "feat") {
    switchTab("studio");
    openStudioSubpage("feat-req");
  } else if (hash === "promotion" || hash === "promo") {
    switchTab("studio");
    openStudioSubpage("promotion");
  } else if (hash === "skills" || hash === "skill") {
    switchTab("studio");
    openStudioSubpage("skills");
  } else if (hash && ["home", "media", "studio", "social", "profile"].includes(hash)) {
    switchTab(hash);
  } else if (["shawtify", "imdb", "critiq", "slander"].includes(hash)) {
    switchTab("media");
    openAnalyzeApp(hash);
  } else if (["calendar", "news", "beatstore", "concerts", "messenger", "tumble", "beef", "livee"].includes(hash)) {
    switchTab("social");
    openSocialPlaceholder(hash);
  } else if (["labels", "management", "certifications", "awards", "deals", "sidehustle", "relations", "wiki", "leisure"].includes(hash)) {
    switchTab("profile");
    openProfileModule(hash);
  }
});




// ==========================================================================
// STUDIO SUBPAGE 4: SKILLS & MASTERY ENGINE
// ==========================================================================
let playerSkills = {
  lyrics: 88,
  vocals: 74,
  prod: 92,
  mix: 68
};

let playerGenreSkills = {
  hiphop: 88,
  pop: 74,
  jazz: 92,
  rock: 68
};

function openImproveSkillsModal() {
  playMechanicalClick();
  const m = document.getElementById("modalImproveSkills");
  if (m) m.classList.add("active");
}

function closeImproveSkillsModal() {
  playMechanicalClick();
  const m = document.getElementById("modalImproveSkills");
  if (m) m.classList.remove("active");
}

function openUpgradeStudioModal() {
  playMechanicalClick();
  const m = document.getElementById("modalUpgradeStudio");
  if (m) m.classList.add("active");
}

function closeUpgradeStudioModal() {
  playMechanicalClick();
  const m = document.getElementById("modalUpgradeStudio");
  if (m) m.classList.remove("active");
}

function openGenreCoursesModal() {
  playMechanicalClick();
  const m = document.getElementById("modalGenreCourses");
  if (m) m.classList.add("active");
}

function closeGenreCoursesModal() {
  playMechanicalClick();
  const m = document.getElementById("modalGenreCourses");
  if (m) m.classList.remove("active");
}

function executeSkillTraining(skillKey, boost, cost, trainingName) {
  playMechanicalClick();
  if (typeof playerCash !== "undefined" && playerCash < cost) {
    showToast(`INSUFFICIENT FUNDS: Need $${cost.toLocaleString()}`);
    return;
  }
  if (typeof playerCash !== "undefined") {
    playerCash -= cost;
    if (typeof updatePlayerHeaderStats === "function") {
      updatePlayerHeaderStats();
    }
  }
  playerSkills[skillKey] = Math.min(100, (playerSkills[skillKey] || 70) + boost);
  updateSkillsDeckUI();
  closeImproveSkillsModal();
  showToast(`${trainingName.toUpperCase()}: +${boost} to ${skillKey.toUpperCase()}! (Current: ${playerSkills[skillKey]}/100)`);
}

function executeStudioUpgrade(upgradeName, cost) {
  playMechanicalClick();
  if (typeof playerCash !== "undefined" && playerCash < cost) {
    showToast(`INSUFFICIENT FUNDS: Need $${cost.toLocaleString()}`);
    return;
  }
  if (typeof playerCash !== "undefined") {
    playerCash -= cost;
    if (typeof updatePlayerHeaderStats === "function") {
      updatePlayerHeaderStats();
    }
  }
  closeUpgradeStudioModal();
  showToast(`STUDIO UPGRADED: ${upgradeName.toUpperCase()} installed!`);
}

function executeGenreCourse(genreKey, boost, cost, courseName) {
  playMechanicalClick();
  if (typeof playerCash !== "undefined" && playerCash < cost) {
    showToast(`INSUFFICIENT FUNDS: Need $${cost.toLocaleString()}`);
    return;
  }
  if (typeof playerCash !== "undefined") {
    playerCash -= cost;
    if (typeof updatePlayerHeaderStats === "function") {
      updatePlayerHeaderStats();
    }
  }
  playerGenreSkills[genreKey] = Math.min(100, (playerGenreSkills[genreKey] || 70) + boost);
  updateSkillsDeckUI();
  closeGenreCoursesModal();
  showToast(`${courseName.toUpperCase()}: +${boost} to ${genreKey.toUpperCase()}! (Current: ${playerGenreSkills[genreKey]}/100)`);
}

function updateSkillsDeckUI() {
  // 1. Update Top Horizontal Bars
  const lVal = document.getElementById("skillsDeckValLyrics");
  const lFill = document.getElementById("skillsDeckFillLyrics");
  if (lVal) lVal.innerHTML = `${playerSkills.lyrics}<small>/100</small>`;
  if (lFill) lFill.style.width = `${playerSkills.lyrics}%`;

  const vVal = document.getElementById("skillsDeckValVocals");
  const vFill = document.getElementById("skillsDeckFillVocals");
  if (vVal) vVal.innerHTML = `${playerSkills.vocals}<small>/100</small>`;
  if (vFill) vFill.style.width = `${playerSkills.vocals}%`;

  const pVal = document.getElementById("skillsDeckValProd");
  const pFill = document.getElementById("skillsDeckFillProd");
  if (pVal) pVal.innerHTML = `${playerSkills.prod}<small>/100</small>`;
  if (pFill) pFill.style.width = `${playerSkills.prod}%`;

  const mVal = document.getElementById("skillsDeckValMix");
  const mFill = document.getElementById("skillsDeckFillMix");
  if (mVal) mVal.innerHTML = `${playerSkills.mix}<small>/100</small>`;
  if (mFill) mFill.style.width = `${playerSkills.mix}%`;

  // 2. Update Genre Equalizer Towers
  const hNum = document.getElementById("towerNumHipHop");
  const hFill = document.getElementById("towerFillHipHop");
  if (hNum) hNum.textContent = playerGenreSkills.hiphop;
  if (hFill) hFill.style.height = `${playerGenreSkills.hiphop}%`;

  const popNum = document.getElementById("towerNumPop");
  const popFill = document.getElementById("towerFillPop");
  if (popNum) popNum.textContent = playerGenreSkills.pop;
  if (popFill) popFill.style.height = `${playerGenreSkills.pop}%`;

  const jNum = document.getElementById("towerNumJazz");
  const jFill = document.getElementById("towerFillJazz");
  if (jNum) jNum.textContent = playerGenreSkills.jazz;
  if (jFill) jFill.style.height = `${playerGenreSkills.jazz}%`;

  const rNum = document.getElementById("towerNumRock");
  const rFill = document.getElementById("towerFillRock");
  if (rNum) rNum.textContent = playerGenreSkills.rock;
  if (rFill) rFill.style.height = `${playerGenreSkills.rock}%`;
}


// ==========================================================================
// SHAWTIFY DSP: AUTHENTIC SPOTIFY MOBILE ENGINE (YOU & INDUSTRY TABS)
// ==========================================================================

const SPOTIFY_ARTISTS_DATA = {
  "lil-synapse": {
    id: "lil-synapse",
    name: "Lil Synapse",
    isPlayer: true,
    verified: true,
    monthlyListeners: "28,491,820",
    headerImage: "assets/studio_create_bg.jpg",
    avatarImage: "album covers/download (10).jpg",
    following: false,
    popularTracks: [
      { id: "ls-1", title: "Neon Dreams", streams: 124850210, duration: "3:12", cover: "album covers/download (10).jpg", explicit: true },
      { id: "ls-2", title: "Chrome Heart Boulevard", streams: 88412900, duration: "3:28", cover: "album covers/download (5).jpg", explicit: true },
      { id: "ls-3", title: "Velvet Bullets", streams: 62104890, duration: "2:54", cover: "album covers/Tyler Durden.jpg", explicit: false },
      { id: "ls-4", title: "Midnight In Tokyo (feat. Kenzo)", streams: 52190440, duration: "3:05", cover: "album covers/download (6).jpg", explicit: true },
      { id: "ls-5", title: "Ghostwriter Blues", streams: 31500120, duration: "2:45", cover: "album covers/download (7).jpg", explicit: false }
    ],
    showcaseReleases: [
      { id: "rel-ls-1", title: "Midnight Sessions", type: "Album", year: "2026", totalStreams: 480192400, cover: "album covers/download (2).jpg" },
      { id: "rel-ls-2", title: "Night City Chronicles", type: "EP", year: "2025", totalStreams: 195402150, cover: "album covers/download (3).jpg" },
      { id: "rel-ls-3", title: "Neon Dreams", type: "Single", year: "2026", totalStreams: 124850210, cover: "album covers/download (10).jpg" },
      { id: "rel-ls-4", title: "Chrome Heart Boulevard", type: "Single", year: "2026", totalStreams: 88412900, cover: "album covers/download (5).jpg" }
    ],
    albums: [
      {
        id: "rel-ls-1",
        title: "Midnight Sessions",
        type: "Album",
        year: "2026",
        cover: "album covers/download (2).jpg",
        totalStreams: 480192400,
        tracks: [
          { num: 1, title: "Chrome Heart Boulevard", streams: 88412900, duration: "3:28" },
          { num: 2, title: "Midnight In Tokyo (feat. Kenzo)", streams: 52190440, duration: "3:05" },
          { num: 3, title: "Velvet Bullets", streams: 62104890, duration: "2:54" },
          { num: 4, title: "Late Night In Shibuya", streams: 24190200, duration: "2:42" },
          { num: 5, title: "Cyber Phantom", streams: 18902400, duration: "3:10" },
          { num: 6, title: "Neo Tokyo Freestyle", streams: 15400200, duration: "2:18" },
          { num: 7, title: "Chrome 808s", streams: 12800100, duration: "2:50" },
          { num: 8, title: "Vandalized Heart", streams: 9800450, duration: "3:14" }
        ]
      },
      {
        id: "rel-ls-2",
        title: "Night City Chronicles",
        type: "EP",
        year: "2025",
        cover: "album covers/download (3).jpg",
        totalStreams: 195402150,
        tracks: [
          { num: 1, title: "Ghostwriter Blues", streams: 31500120, duration: "2:45" },
          { num: 2, title: "Fast Cash Slow Love", streams: 19820600, duration: "2:55" },
          { num: 3, title: "Subway Freestyles", streams: 14210000, duration: "2:10" },
          { num: 4, title: "Concrete Serenade", streams: 8900400, duration: "3:02" }
        ]
      },
      {
        id: "rel-ls-3",
        title: "Neon Dreams",
        type: "Single",
        year: "2026",
        cover: "album covers/download (10).jpg",
        totalStreams: 124850210,
        tracks: [
          { num: 1, title: "Neon Dreams", streams: 124850210, duration: "3:12" },
          { num: 2, title: "Neon Dreams (Instrumental)", streams: 12400500, duration: "3:12" }
        ]
      },
      {
        id: "rel-ls-4",
        title: "Chrome Heart Boulevard",
        type: "Single",
        year: "2026",
        cover: "album covers/download (5).jpg",
        totalStreams: 88412900,
        tracks: [
          { num: 1, title: "Chrome Heart Boulevard", streams: 88412900, duration: "3:28" }
        ]
      }
    ]
  },
  "travis-scott": {
    id: "travis-scott",
    name: "Travis Scott",
    isPlayer: false,
    verified: true,
    monthlyListeners: "76,842,109",
    headerImage: "album covers/download (2).jpg",
    avatarImage: "album covers/download (2).jpg",
    following: false,
    popularTracks: [
      { id: "ts-1", title: "FE!N (feat. Playboi Carti)", streams: 1421805392, duration: "3:11", cover: "album covers/download (2).jpg", explicit: true },
      { id: "ts-2", title: "SICKO MODE", streams: 2390412850, duration: "5:12", cover: "album covers/download (3).jpg", explicit: true },
      { id: "ts-3", title: "goosebumps", streams: 2104892100, duration: "4:03", cover: "album covers/download (4).jpg", explicit: true },
      { id: "ts-4", title: "MELTDOWN (feat. Drake)", streams: 982410200, duration: "4:06", cover: "album covers/download (2).jpg", explicit: true },
      { id: "ts-5", title: "MY EYES", streams: 845920400, duration: "4:11", cover: "album covers/download (2).jpg", explicit: false }
    ],
    showcaseReleases: [
      { id: "rel-ts-1", title: "UTOPIA", type: "Album", year: "2023", totalStreams: 3890204100, cover: "album covers/download (2).jpg" },
      { id: "rel-ts-2", title: "ASTROWORLD", type: "Album", year: "2018", totalStreams: 6104890200, cover: "album covers/download (3).jpg" },
      { id: "rel-ts-3", title: "Rodeo", type: "Album", year: "2015", totalStreams: 2940110400, cover: "album covers/download (4).jpg" },
      { id: "rel-ts-4", title: "JACKBOYS", type: "EP", year: "2019", totalStreams: 1840290100, cover: "album covers/download (5).jpg" }
    ],
    albums: [
      {
        id: "rel-ts-1",
        title: "UTOPIA",
        type: "Album",
        year: "2023",
        cover: "album covers/download (2).jpg",
        totalStreams: 3890204100,
        tracks: [
          { num: 1, title: "HYAENA", streams: 481204912, duration: "3:42" },
          { num: 2, title: "THANK GOD", streams: 541902400, duration: "3:04" },
          { num: 3, title: "MODERN JAM (feat. Teezo Touchdown)", streams: 382401900, duration: "4:15" },
          { num: 4, title: "MY EYES", streams: 845920400, duration: "4:11" },
          { num: 5, title: "GOD'S COUNTRY", streams: 294102800, duration: "2:07" },
          { num: 6, title: "SIRENS", streams: 312904100, duration: "3:24" },
          { num: 7, title: "MELTDOWN (feat. Drake)", streams: 982410200, duration: "4:06" },
          { num: 8, title: "FE!N (feat. Playboi Carti)", streams: 1421805392, duration: "3:11" },
          { num: 9, title: "DELRESTO (ECHOES) (feat. Beyoncé)", streams: 241904200, duration: "4:34" },
          { num: 10, title: "I KNOW ?", streams: 890412800, duration: "3:31" },
          { num: 11, title: "TOPIA TWINS (feat. Rob49 & 21 Savage)", streams: 380491200, duration: "3:43" },
          { num: 12, title: "TELEKINESIS (feat. SZA & Future)", streams: 720490100, duration: "5:53" }
        ]
      },
      {
        id: "rel-ts-2",
        title: "ASTROWORLD",
        type: "Album",
        year: "2018",
        cover: "album covers/download (3).jpg",
        totalStreams: 6104890200,
        tracks: [
          { num: 1, title: "STARGAZING", streams: 1104820900, duration: "4:30" },
          { num: 2, title: "CAROUSEL", streams: 420194800, duration: "3:00" },
          { num: 3, title: "SICKO MODE", streams: 2390412850, duration: "5:12" },
          { num: 4, title: "R.I.P. SCREW", streams: 380491000, duration: "3:05" },
          { num: 5, title: "STOP TRYING TO BE GOD", streams: 480291400, duration: "5:38" },
          { num: 6, title: "NO BYSTANDERS", streams: 690412800, duration: "3:38" },
          { num: 7, title: "SKELETONS", streams: 450190400, duration: "2:25" },
          { num: 8, title: "WAKE UP (feat. The Weeknd)", streams: 512409100, duration: "3:51" },
          { num: 9, title: "5% TINT", streams: 490214800, duration: "3:16" },
          { num: 10, title: "CAN'T SAY (feat. Don Toliver)", streams: 780491200, duration: "3:18" },
          { num: 11, title: "HOUSTONFORNICATION", streams: 440192400, duration: "3:37" },
          { num: 12, title: "BUTTERFLY EFFECT", streams: 1420491000, duration: "3:10" }
        ]
      }
    ]
  },
  "drake": {
    id: "drake",
    name: "Drake",
    isPlayer: false,
    verified: true,
    monthlyListeners: "85,291,040",
    headerImage: "album covers/Tyler Durden.jpg",
    avatarImage: "album covers/Tyler Durden.jpg",
    following: false,
    popularTracks: [
      { id: "dr-1", title: "One Dance", streams: 3104829100, duration: "2:54", cover: "album covers/Tyler Durden.jpg", explicit: false },
      { id: "dr-2", title: "God's Plan", streams: 2490120400, duration: "3:18", cover: "album covers/download (5).jpg", explicit: true },
      { id: "dr-3", title: "Rich Baby Daddy (feat. Sexyy Red & SZA)", streams: 841902300, duration: "5:19", cover: "album covers/download (6).jpg", explicit: true },
      { id: "dr-4", title: "First Person Shooter (feat. J. Cole)", streams: 684209100, duration: "4:07", cover: "album covers/download (6).jpg", explicit: true },
      { id: "dr-5", title: "IDGAF (feat. Yeat)", streams: 762401900, duration: "4:20", cover: "album covers/download (6).jpg", explicit: true }
    ],
    showcaseReleases: [
      { id: "rel-dr-1", title: "For All The Dogs", type: "Album", year: "2023", totalStreams: 2840192000, cover: "album covers/download (6).jpg" },
      { id: "rel-dr-2", title: "Her Loss", type: "Album", year: "2022", totalStreams: 2910402100, cover: "album covers/Tyler Durden.jpg" },
      { id: "rel-dr-3", title: "Certified Lover Boy", type: "Album", year: "2021", totalStreams: 4120490000, cover: "album covers/download (7).jpg" },
      { id: "rel-dr-4", title: "Scorpion", type: "Album", year: "2018", totalStreams: 7890102400, cover: "album covers/download (5).jpg" }
    ],
    albums: [
      {
        id: "rel-dr-1",
        title: "For All The Dogs",
        type: "Album",
        year: "2023",
        cover: "album covers/download (6).jpg",
        totalStreams: 2840192000,
        tracks: [
          { num: 1, title: "Virginia Beach", streams: 410294800, duration: "4:11" },
          { num: 2, title: "Amen (feat. Teezo Touchdown)", streams: 198402100, duration: "2:21" },
          { num: 3, title: "Calling For You (feat. 21 Savage)", streams: 284019200, duration: "4:45" },
          { num: 4, title: "Fear of Heights", streams: 172904100, duration: "2:35" },
          { num: 5, title: "First Person Shooter (feat. J. Cole)", streams: 684209100, duration: "4:07" },
          { num: 6, title: "IDGAF (feat. Yeat)", streams: 762401900, duration: "4:20" },
          { num: 7, title: "Slime You Out (feat. SZA)", streams: 420194800, duration: "5:10" },
          { num: 8, title: "Rich Baby Daddy", streams: 841902300, duration: "5:19" }
        ]
      }
    ]
  },
  "playboi-carti": {
    id: "playboi-carti",
    name: "Playboi Carti",
    isPlayer: false,
    verified: true,
    monthlyListeners: "52,490,120",
    headerImage: "album covers/download (8).jpg",
    avatarImage: "album covers/download (8).jpg",
    following: false,
    popularTracks: [
      { id: "pc-1", title: "FE!N", streams: 1421805392, duration: "3:11", cover: "album covers/download (2).jpg", explicit: true },
      { id: "pc-2", title: "Magnolia", streams: 1104290400, duration: "3:01", cover: "album covers/download (7).jpg", explicit: true },
      { id: "pc-3", title: "Sky", streams: 984201400, duration: "3:13", cover: "album covers/download (8).jpg", explicit: true },
      { id: "pc-4", title: "CARNIVAL", streams: 792410200, duration: "4:24", cover: "album covers/download (4).jpg", explicit: true },
      { id: "pc-5", title: "2024", streams: 512940200, duration: "3:20", cover: "album covers/download (8).jpg", explicit: true }
    ],
    showcaseReleases: [
      { id: "rel-pc-1", title: "Whole Lotta Red", type: "Album", year: "2020", totalStreams: 2490120000, cover: "album covers/download (8).jpg" },
      { id: "rel-pc-2", title: "Die Lit", type: "Album", year: "2018", totalStreams: 1920400000, cover: "album covers/download (7).jpg" }
    ],
    albums: [
      {
        id: "rel-pc-1",
        title: "Whole Lotta Red",
        type: "Album",
        year: "2020",
        cover: "album covers/download (8).jpg",
        totalStreams: 2490120000,
        tracks: [
          { num: 1, title: "Rockstar Made", streams: 284102900, duration: "3:13" },
          { num: 2, title: "Go2DaMoon (feat. Kanye West)", streams: 210490100, duration: "1:59" },
          { num: 3, title: "Stop Breathing", streams: 412094800, duration: "3:38" },
          { num: 4, title: "Vamp Anthem", streams: 510294100, duration: "2:04" },
          { num: 5, title: "Sky", streams: 984201400, duration: "3:13" }
        ]
      }
    ]
  },
  "kendrick-lamar": {
    id: "kendrick-lamar",
    name: "Kendrick Lamar",
    isPlayer: false,
    verified: true,
    monthlyListeners: "68,491,230",
    headerImage: "album covers/download (9).jpg",
    avatarImage: "album covers/download (9).jpg",
    following: false,
    popularTracks: [
      { id: "kl-1", title: "Not Like Us", streams: 1184902400, duration: "4:34", cover: "album covers/download (9).jpg", explicit: true },
      { id: "kl-2", title: "HUMBLE.", streams: 2290410200, duration: "2:57", cover: "album covers/download (10).jpg", explicit: true },
      { id: "kl-3", title: "All The Stars", streams: 1840201900, duration: "3:52", cover: "album covers/download (6).jpg", explicit: false },
      { id: "kl-4", title: "Money Trees", streams: 1620490100, duration: "6:26", cover: "album covers/download (5).jpg", explicit: true },
      { id: "kl-5", title: "luther (with SZA)", streams: 642104800, duration: "2:58", cover: "album covers/download (9).jpg", explicit: true }
    ],
    showcaseReleases: [
      { id: "rel-kl-1", title: "GNX", type: "Album", year: "2024", totalStreams: 1420910200, cover: "album covers/download (9).jpg" },
      { id: "rel-kl-2", title: "DAMN.", type: "Album", year: "2017", totalStreams: 5490102400, cover: "album covers/download (10).jpg" }
    ],
    albums: [
      {
        id: "rel-kl-1",
        title: "GNX",
        type: "Album",
        year: "2024",
        cover: "album covers/download (9).jpg",
        totalStreams: 1420910200,
        tracks: [
          { num: 1, title: "wacced out murals", streams: 210490200, duration: "5:16" },
          { num: 2, title: "squabble up", streams: 384102900, duration: "2:37" },
          { num: 3, title: "luther (with SZA)", streams: 642104800, duration: "2:58" },
          { num: 4, title: "tv off", streams: 310492100, duration: "3:40" }
        ]
      }
    ]
  },
  "metro-boomin": {
    id: "metro-boomin",
    name: "Metro Boomin",
    isPlayer: false,
    verified: true,
    monthlyListeners: "58,920,400",
    headerImage: "album covers/download (4).jpg",
    avatarImage: "album covers/download (4).jpg",
    following: false,
    popularTracks: [
      { id: "mb-1", title: "Creepin' (feat. The Weeknd & 21 Savage)", streams: 1640920100, duration: "3:41", cover: "album covers/download (4).jpg", explicit: true },
      { id: "mb-2", title: "Superhero (Heroes & Villains)", streams: 980410200, duration: "3:02", cover: "album covers/download (4).jpg", explicit: true },
      { id: "mb-3", title: "Too Many Nights", streams: 840192400, duration: "3:19", cover: "album covers/download (4).jpg", explicit: true },
      { id: "mb-4", title: "Like That", streams: 590410200, duration: "4:27", cover: "album covers/download (2).jpg", explicit: true },
      { id: "mb-5", title: "Space Cadet", streams: 640290100, duration: "3:23", cover: "album covers/download (5).jpg", explicit: true }
    ],
    showcaseReleases: [
      { id: "rel-mb-1", title: "HEROES & VILLAINS", type: "Album", year: "2022", totalStreams: 3490120000, cover: "album covers/download (4).jpg" },
      { id: "rel-mb-2", title: "WE DON'T TRUST YOU", type: "Album", year: "2024", totalStreams: 1840290000, cover: "album covers/download (2).jpg" }
    ],
    albums: [
      {
        id: "rel-mb-1",
        title: "HEROES & VILLAINS",
        type: "Album",
        year: "2022",
        cover: "album covers/download (4).jpg",
        totalStreams: 3490120000,
        tracks: [
          { num: 1, title: "On Time", streams: 210490100, duration: "2:48" },
          { num: 2, title: "Superhero", streams: 980410200, duration: "3:02" },
          { num: 3, title: "Too Many Nights", streams: 840192400, duration: "3:19" },
          { num: 4, title: "Creepin'", streams: 1640920100, duration: "3:41" }
        ]
      }
    ]
  },
  "drakeo-v": {
    id: "drakeo-v",
    name: "Drakeo V",
    isPlayer: false,
    verified: true,
    monthlyListeners: "34,120,400",
    headerImage: "album covers/Tyler Durden.jpg",
    avatarImage: "album covers/Tyler Durden.jpg",
    following: false,
    popularTracks: [
      { id: "dv-1", title: "Midnight Dynasty", streams: 210400000, duration: "3:40", cover: "album covers/Tyler Durden.jpg", explicit: true },
      { id: "dv-2", title: "Penthouse Views", streams: 142000000, duration: "3:30", cover: "album covers/download (3).jpg", explicit: true },
      { id: "dv-3", title: "Diamond Fangs", streams: 94100500, duration: "3:10", cover: "album covers/download (2).jpg", explicit: true },
      { id: "dv-4", title: "Velvet Mirage", streams: 68490200, duration: "3:15", cover: "album covers/download (4).jpg", explicit: false },
      { id: "dv-5", title: "Black Amex", streams: 45210400, duration: "2:50", cover: "album covers/download (5).jpg", explicit: true }
    ],
    showcaseReleases: [
      { id: "rel-dv-1", title: "Midnight Dynasty", type: "Album", year: "2026", totalStreams: 450200000, cover: "album covers/Tyler Durden.jpg" },
      { id: "rel-dv-2", title: "Luxury & Paranoia", type: "Album", year: "2025", totalStreams: 310000000, cover: "album covers/download (3).jpg" }
    ],
    albums: [
      {
        id: "rel-dv-1",
        title: "Midnight Dynasty",
        type: "Album",
        year: "2026",
        cover: "album covers/Tyler Durden.jpg",
        totalStreams: 450200000,
        tracks: [
          { num: 1, title: "Midnight Dynasty", streams: 210400000, duration: "3:40" },
          { num: 2, title: "Diamond Fangs", streams: 94100500, duration: "3:10" },
          { num: 3, title: "Penthouse Views", streams: 142000000, duration: "3:30" },
          { num: 4, title: "Velvet Mirage", streams: 68490200, duration: "3:15" },
          { num: 5, title: "Black Amex", streams: 45210400, duration: "2:50" }
        ]
      }
    ]
  },
  "szaria": {
    id: "szaria",
    name: "SZAria",
    isPlayer: false,
    verified: true,
    monthlyListeners: "41,940,200",
    headerImage: "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg",
    avatarImage: "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg",
    following: false,
    popularTracks: [
      { id: "sz-1", title: "Ocean Lavender", streams: 318000000, duration: "3:45", cover: "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg", explicit: false },
      { id: "sz-2", title: "Velvet Waves", streams: 76320000, duration: "3:42", cover: "album covers/Music artwork for Frank Ocean - _.jpg", explicit: false },
      { id: "sz-3", title: "Midnight Solitude", streams: 54120000, duration: "3:18", cover: "album covers/download (6).jpg", explicit: false },
      { id: "sz-4", title: "Indigo Silk", streams: 42910400, duration: "3:02", cover: "album covers/download (7).jpg", explicit: false },
      { id: "sz-5", title: "Saltwater Memories", streams: 38400100, duration: "2:55", cover: "album covers/download (8).jpg", explicit: false }
    ],
    showcaseReleases: [
      { id: "rel-sz-1", title: "Solitude", type: "Album", year: "2025", totalStreams: 640200000, cover: "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg" },
      { id: "rel-sz-2", title: "Velvet Waves", type: "Single", year: "2026", totalStreams: 76320000, cover: "album covers/Music artwork for Frank Ocean - _.jpg" }
    ],
    albums: [
      {
        id: "rel-sz-1",
        title: "Solitude",
        type: "Album",
        year: "2025",
        cover: "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg",
        totalStreams: 640200000,
        tracks: [
          { num: 1, title: "Ocean Lavender", streams: 318000000, duration: "3:45" },
          { num: 2, title: "Velvet Waves", streams: 76320000, duration: "3:42" },
          { num: 3, title: "Midnight Solitude", streams: 54120000, duration: "3:18" },
          { num: 4, title: "Indigo Silk", streams: 42910400, duration: "3:02" },
          { num: 5, title: "Saltwater Memories", streams: 38400100, duration: "2:55" }
        ]
      }
    ]
  },
  "grimkidd": {
    id: "grimkidd",
    name: "GrimKidd",
    isPlayer: false,
    verified: true,
    monthlyListeners: "18,420,100",
    headerImage: "album covers/download (4).jpg",
    avatarImage: "album covers/download (4).jpg",
    following: false,
    popularTracks: [
      { id: "gk-1", title: "Subzero", streams: 48900000, duration: "2:40", cover: "album covers/download (4).jpg", explicit: true },
      { id: "gk-2", title: "Balaclava Drill", streams: 34200000, duration: "2:50", cover: "album covers/download (5).jpg", explicit: true },
      { id: "gk-3", title: "London Fog", streams: 28410200, duration: "2:32", cover: "album covers/download (3).jpg", explicit: true },
      { id: "gk-4", title: "Ski Mask Freestyle", streams: 21904000, duration: "2:15", cover: "album covers/download (7).jpg", explicit: true },
      { id: "gk-5", title: "North London Trap", streams: 16840200, duration: "2:48", cover: "album covers/download (8).jpg", explicit: true }
    ],
    showcaseReleases: [
      { id: "rel-gk-1", title: "Subzero EP", type: "EP", year: "2026", totalStreams: 120400000, cover: "album covers/download (4).jpg" }
    ],
    albums: [
      {
        id: "rel-gk-1",
        title: "Subzero EP",
        type: "EP",
        year: "2026",
        cover: "album covers/download (4).jpg",
        totalStreams: 120400000,
        tracks: [
          { num: 1, title: "Subzero", streams: 48900000, duration: "2:40" },
          { num: 2, title: "Balaclava Drill", streams: 34200000, duration: "2:50" },
          { num: 3, title: "London Fog", streams: 28410200, duration: "2:32" },
          { num: 4, title: "Ski Mask Freestyle", streams: 21904000, duration: "2:15" },
          { num: 5, title: "North London Trap", streams: 16840200, duration: "2:48" }
        ]
      }
    ]
  },
  "kenny-knox": {
    id: "kenny-knox",
    name: "Kenny Knox",
    isPlayer: false,
    verified: true,
    monthlyListeners: "24,890,200",
    headerImage: "album covers/download (6).jpg",
    avatarImage: "album covers/download (6).jpg",
    following: false,
    popularTracks: [
      { id: "kk-1", title: "Concrete Garden", streams: 112000000, duration: "3:35", cover: "album covers/download (6).jpg", explicit: false },
      { id: "kk-2", title: "Brooklyn Brownstones", streams: 58400200, duration: "3:10", cover: "album covers/download (7).jpg", explicit: false },
      { id: "kk-3", title: "Boom Bap Renaissance", streams: 42100900, duration: "3:44", cover: "album covers/download (8).jpg", explicit: true },
      { id: "kk-4", title: "Crown Heights Corner", streams: 31400000, duration: "2:58", cover: "album covers/download (9).jpg", explicit: false },
      { id: "kk-5", title: "Vinyl Soul", streams: 24902400, duration: "3:22", cover: "album covers/download (10).jpg", explicit: false }
    ],
    showcaseReleases: [
      { id: "rel-kk-1", title: "Concrete Garden", type: "Album", year: "2026", totalStreams: 280400000, cover: "album covers/download (6).jpg" }
    ],
    albums: [
      {
        id: "rel-kk-1",
        title: "Concrete Garden",
        type: "Album",
        year: "2026",
        cover: "album covers/download (6).jpg",
        totalStreams: 280400000,
        tracks: [
          { num: 1, title: "Concrete Garden", streams: 112000000, duration: "3:35" },
          { num: 2, title: "Brooklyn Brownstones", streams: 58400200, duration: "3:10" },
          { num: 3, title: "Boom Bap Renaissance", streams: 42100900, duration: "3:44" },
          { num: 4, title: "Crown Heights Corner", streams: 31400000, duration: "2:58" },
          { num: 5, title: "Vinyl Soul", streams: 24902400, duration: "3:22" }
        ]
      }
    ]
  }
};

let currentShawtifyTab = "you"; // "you" | "industry"
let currentShawtifyViewState = { view: "you" };
let currentShawtifyViewStack = [];
let activeViewingArtistId = "lil-synapse";
let activePlayingTrackId = null;

function pushShawtifyViewState(nextState) {
  if (currentShawtifyViewState) {
    currentShawtifyViewStack.push(currentShawtifyViewState);
  }
  applyShawtifyViewState(nextState);
}

function applyShawtifyViewState(state) {
  currentShawtifyViewState = state;

  const pageYou = document.getElementById("shawtifyPageYou");
  const pageIndustry = document.getElementById("shawtifyPageIndustry");
  const searchWrap = document.getElementById("shawtifyIndustrySearchContent");
  const profileWrap = document.getElementById("shawtifyIndustryArtistProfile");
  const albumView = document.getElementById("shawtifyAlbumInspectView");
  const discoView = document.getElementById("shawtifyDiscographyView");
  const viewport = document.getElementById("shawtifyMainViewport");

  // 1. First hide all subviews cleanly
  if (pageYou) pageYou.style.display = "none";
  if (pageIndustry) pageIndustry.style.display = "none";
  if (searchWrap) searchWrap.style.display = "none";
  if (profileWrap) profileWrap.style.display = "none";
  if (albumView) albumView.style.display = "none";
  if (discoView) discoView.style.display = "none";

  // 2. Synchronize bottom navigation active state
  const navIndustry = document.getElementById("shawtifyNavIndustry");
  const navYou = document.getElementById("shawtifyNavYou");

  if (state.view === "you") {
    currentShawtifyTab = "you";
    if (navIndustry) navIndustry.classList.remove("active");
    if (navYou) navYou.classList.add("active");

    if (pageYou) pageYou.style.display = "block";
    activeViewingArtistId = "lil-synapse";
    renderSpotifyArtistProfile("lil-synapse", false, "shawtifyYouContent");
  } 
  else if (state.view === "industry-search") {
    currentShawtifyTab = "industry";
    if (navIndustry) navIndustry.classList.add("active");
    if (navYou) navYou.classList.remove("active");

    if (pageIndustry) pageIndustry.style.display = "block";
    if (searchWrap) searchWrap.style.display = "block";
    renderIndustryArtistsDirectory();
  } 
  else if (state.view === "artist-profile") {
    const isInd = Boolean(state.isIndustry);
    currentShawtifyTab = isInd ? "industry" : "you";
    if (navIndustry) navIndustry.classList.toggle("active", isInd);
    if (navYou) navYou.classList.toggle("active", !isInd);

    activeViewingArtistId = state.artistId;
    if (isInd) {
      if (pageIndustry) pageIndustry.style.display = "block";
      if (profileWrap) profileWrap.style.display = "block";
      renderSpotifyArtistProfile(state.artistId, true, "shawtifyIndustryArtistProfile");
    } else {
      if (pageYou) pageYou.style.display = "block";
      renderSpotifyArtistProfile(state.artistId, false, "shawtifyYouContent");
    }
  } 
  else if (state.view === "album") {
    const isInd = Boolean(state.isIndustry);
    if (navIndustry) navIndustry.classList.toggle("active", isInd);
    if (navYou) navYou.classList.toggle("active", !isInd);

    if (albumView) albumView.style.display = "block";
    renderSpotifyAlbumDOM(state.albumId, state.artistId);
  } 
  else if (state.view === "discography") {
    const isInd = Boolean(state.isIndustry);
    if (navIndustry) navIndustry.classList.toggle("active", isInd);
    if (navYou) navYou.classList.toggle("active", !isInd);

    if (discoView) discoView.style.display = "block";
    renderSpotifyDiscographyDOM(state.artistId);
  }

  if (viewport) viewport.scrollTop = 0;
}

function openShawtifyApp(initialTab = "you") {
  playMechanicalClick();

  // 1. Hide main console bottom nav
  const mainBottomNav = document.querySelector(".bottom-nav-bar");
  if (mainBottomNav) mainBottomNav.style.display = "none";

  // 2. Hide media hub
  const mediaHub = document.getElementById("mediaMainHub");
  if (mediaHub) mediaHub.style.display = "none";

  // 3. Synchronize top-bar clock
  updateClock();

  // 4. Show full-screen Spotify view
  const app = document.getElementById("appView_shawtify");
  if (app) {
    app.style.display = "flex";
  }

  // 5. Reset view stack and open tab
  currentShawtifyViewStack = [];
  if (initialTab === "industry") {
    applyShawtifyViewState({ view: "industry-search" });
  } else {
    applyShawtifyViewState({ view: "you" });
  }
}

function closeShawtifyApp() {
  playMechanicalClick();

  // 1. Hide Shawtify
  const app = document.getElementById("appView_shawtify");
  if (app) app.style.display = "none";

  // 2. Restore main bottom nav
  const mainBottomNav = document.querySelector(".bottom-nav-bar");
  if (mainBottomNav) mainBottomNav.style.display = "flex";

  // 3. Restore Media main hub
  const mediaHub = document.getElementById("mediaMainHub");
  if (mediaHub) mediaHub.style.display = "flex";

  // 4. Return to media tab
  switchTab("media");
}

function switchShawtifyTab(tabName) {
  playMechanicalClick();
  currentShawtifyViewStack = [];
  if (tabName === "industry") {
    applyShawtifyViewState({ view: "industry-search" });
  } else {
    applyShawtifyViewState({ view: "you" });
  }
}

function handleShawtifyBackNavigation() {
  playMechanicalClick();

  if (currentShawtifyViewStack.length > 0) {
    const previousState = currentShawtifyViewStack.pop();
    applyShawtifyViewState(previousState);
  } else {
    // Root level: return to Media page
    closeShawtifyApp();
  }
}

function renderSpotifyArtistProfile(artistId, isIndustry = false, targetContainerId = null) {
  const artist = SPOTIFY_ARTISTS_DATA[artistId];
  if (!artist) return;
  activeViewingArtistId = artistId;

  const containerId = targetContainerId || (isIndustry ? "shawtifyIndustryArtistProfile" : "shawtifyYouContent");
  const container = document.getElementById(containerId);
  if (!container) return;

  const bgImage = artist.headerImage || artist.avatarImage || "album covers/download (10).jpg";

  container.innerHTML = `
    <!-- Artist Hero Banner -->
    <div class="spotify-artist-hero" style="background-image: url('${bgImage}');">
      <div class="spotify-hero-gradient"></div>
      <div class="spotify-hero-content">
        <div class="spotify-verified-badge">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="#3d91f4">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
          <span>Verified Artist</span>
        </div>
        <h1 class="spotify-artist-name">${artist.name}</h1>
        <span class="spotify-monthly-listeners">${artist.monthlyListeners} monthly listeners</span>
      </div>
    </div>

    <!-- Action Controls Row -->
    <div class="spotify-action-bar">
      <div class="spotify-action-left">
        <button class="spotify-follow-pill ${artist.following ? 'following' : ''}" onclick="toggleSpotifyFollow('${artist.id}', this)">
          ${artist.following ? 'Following' : 'Follow'}
        </button>
        <button class="spotify-icon-btn" onclick="showToast('SHARED LINK COPIED')" title="More Options">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
            <circle cx="12" cy="12" r="2"/><circle cx="5" cy="12" r="2"/><circle cx="19" cy="12" r="2"/>
          </svg>
        </button>
      </div>
      <button class="spotify-green-play-btn" onclick="playSpotifyTopTrack('${artist.id}')" title="Play ${artist.name}">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="#000000">
          <polygon points="6 4 20 12 6 20 6 4"/>
        </svg>
      </button>
    </div>

    <!-- Popular Section -->
    <h2 class="spotify-section-title">Popular</h2>
    <div class="spotify-popular-list">
      ${artist.popularTracks.map((tr, idx) => {
        const safeTitle = (tr.title || '').replace(/'/g, "\\'");
        const safeArtName = (artist.name || '').replace(/'/g, "\\'");
        return `
        <div class="spotify-song-row ${activePlayingTrackId === tr.id ? 'playing' : ''}" onclick="playSpotifyTrack('${safeTitle}', '${safeArtName}', '${tr.cover}', '${tr.id}')">
          <span class="spotify-song-index">${idx + 1}</span>
          <div class="spotify-playing-bars">
            <span class="spotify-bar"></span>
            <span class="spotify-bar"></span>
            <span class="spotify-bar"></span>
          </div>
          <img src="${tr.cover}" class="spotify-song-thumb" alt="${tr.title}">
          <div class="spotify-song-info">
            <div class="spotify-title-line">
              <span class="spotify-song-title">${tr.title}</span>
              ${tr.explicit ? '<span class="spotify-explicit-badge">E</span>' : ''}
            </div>
            <span class="spotify-song-streams">${Number(tr.streams).toLocaleString()}</span>
          </div>
          <button class="spotify-song-more" onclick="event.stopPropagation(); showToast('${safeTitle.toUpperCase()} OPTIONS')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <circle cx="12" cy="5" r="1.8"/><circle cx="12" cy="12" r="1.8"/><circle cx="12" cy="19" r="1.8"/>
            </svg>
          </button>
        </div>
      `;}).join('')}
    </div>

    <!-- Popular Releases Showcase -->
    <h2 class="spotify-section-title">Popular releases</h2>
    <div class="spotify-filter-pills">
      <button class="spotify-pill-chip active" onclick="filterReleasesShowcase('all', this, '${artist.id}')">All</button>
      <button class="spotify-pill-chip" onclick="filterReleasesShowcase('Album', this, '${artist.id}')">Albums</button>
      <button class="spotify-pill-chip" onclick="filterReleasesShowcase('Single', this, '${artist.id}')">Singles & EPs</button>
    </div>

    <div class="spotify-releases-list" id="spotifyReleasesContainer_${artist.id}">
      ${renderShowcaseReleaseCards(artist.showcaseReleases, artist.id)}
    </div>

    <!-- View Discography Button -->
    <button class="spotify-view-discography-btn" onclick="openSpotifyDiscography('${artist.id}')">
      View discography
    </button>
  `;
}

function renderShowcaseReleaseCards(releases, artistId) {
  return releases.map(rel => `
    <div class="spotify-release-card" onclick="openSpotifyAlbum('${rel.id}', '${artistId}')">
      <img src="${rel.cover}" class="spotify-release-thumb" alt="${rel.title}">
      <div class="spotify-release-info">
        <span class="spotify-release-title">${rel.title}</span>
        <span class="spotify-release-meta">${rel.type} &bull; ${rel.year}</span>
        <span class="spotify-release-streams">${Number(rel.totalStreams).toLocaleString()} streams</span>
      </div>
      <div class="spotify-release-arrow">&rsaquo;</div>
    </div>
  `).join('');
}

function filterReleasesShowcase(typeFilter, btnEl, artistId) {
  playMechanicalClick();
  const parent = btnEl.parentElement;
  if (parent) {
    parent.querySelectorAll(".spotify-pill-chip").forEach(b => b.classList.remove("active"));
    btnEl.classList.add("active");
  }

  const artist = SPOTIFY_ARTISTS_DATA[artistId];
  if (!artist) return;

  const container = document.getElementById(`spotifyReleasesContainer_${artistId}`);
  if (!container) return;

  let filtered = artist.showcaseReleases;
  if (typeFilter !== "all") {
    filtered = artist.showcaseReleases.filter(r => r.type.toLowerCase().includes(typeFilter.toLowerCase()));
  }

  container.innerHTML = renderShowcaseReleaseCards(filtered, artistId);
}

function renderIndustryArtistsDirectory(filteredList = null) {
  const container = document.getElementById("shawtifyIndustrySearchContent");
  if (!container) return;

  const artists = filteredList || Object.values(SPOTIFY_ARTISTS_DATA).filter(a => !a.isPlayer);

  container.innerHTML = `
    <!-- Spotify Search Bar -->
    <div class="spotify-search-bar-wrap">
      <div class="spotify-search-box">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input 
          type="text" 
          class="spotify-search-input" 
          id="spotifyIndustrySearchInput"
          placeholder="What artist do you want to listen to?" 
          oninput="handleIndustryArtistSearch(this.value)"
        >
      </div>
    </div>

    <!-- Artists Directory Header -->
    <h2 class="spotify-section-title" style="margin-top: 6px;">Explore Artists</h2>
    
    <!-- Artists Rows -->
    <div class="spotify-artists-grid">
      ${artists.map(art => `
        <div class="spotify-artist-row-card" onclick="openIndustryArtistProfile('${art.id}')">
          <img src="${art.avatarImage || art.headerImage}" class="spotify-artist-avatar" alt="${art.name}">
          <div class="spotify-artist-row-info">
            <span class="spotify-artist-row-name">
              ${art.name}
              <svg width="14" height="14" viewBox="0 0 24 24" fill="#3d91f4">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </span>
            <span class="spotify-artist-row-meta">Artist &bull; ${art.monthlyListeners} listeners</span>
          </div>
          <div class="spotify-release-arrow">&rsaquo;</div>
        </div>
      `).join('')}
    </div>
  `;
}

function handleIndustryArtistSearch(query) {
  const q = (query || "").trim().toLowerCase();
  const allIndustry = Object.values(SPOTIFY_ARTISTS_DATA).filter(a => !a.isPlayer);

  if (!q) {
    renderIndustryArtistsDirectory(allIndustry);
    return;
  }

  const matches = allIndustry.filter(a => 
    a.name.toLowerCase().includes(q) ||
    a.popularTracks.some(t => t.title.toLowerCase().includes(q)) ||
    a.showcaseReleases.some(r => r.title.toLowerCase().includes(q))
  );

  renderIndustryArtistsDirectory(matches);
  const input = document.getElementById("spotifyIndustrySearchInput");
  if (input) {
    input.focus();
    input.value = query;
  }
}

function openIndustryArtistProfile(artistId) {
  playMechanicalClick();
  pushShawtifyViewState({
    view: "artist-profile",
    artistId: artistId,
    isIndustry: true
  });
}

function openSpotifyAlbum(albumId, artistId) {
  playMechanicalClick();
  const targetArtistId = artistId || activeViewingArtistId;
  const artist = SPOTIFY_ARTISTS_DATA[targetArtistId];
  const isIndustry = artist ? !artist.isPlayer : (currentShawtifyTab === "industry");
  pushShawtifyViewState({
    view: "album",
    albumId: albumId,
    artistId: targetArtistId,
    isIndustry: isIndustry
  });
}

function openSpotifyDiscography(artistId) {
  playMechanicalClick();
  const targetArtistId = artistId || activeViewingArtistId;
  const artist = SPOTIFY_ARTISTS_DATA[targetArtistId];
  const isIndustry = artist ? !artist.isPlayer : (currentShawtifyTab === "industry");
  pushShawtifyViewState({
    view: "discography",
    artistId: targetArtistId,
    isIndustry: isIndustry
  });
}

function renderSpotifyAlbumDOM(albumId, artistId) {
  let artist = artistId ? SPOTIFY_ARTISTS_DATA[artistId] : null;
  let album = null;
  if (artist) {
    album = (artist.albums || []).find(a => a.id === albumId) || (artist.showcaseReleases || []).find(a => a.id === albumId);
  }
  if (!album) {
    for (const art of Object.values(SPOTIFY_ARTISTS_DATA)) {
      const found = (art.albums || []).find(a => a.id === albumId) || (art.showcaseReleases || []).find(a => a.id === albumId);
      if (found) {
        album = found;
        artist = art;
        break;
      }
    }
  }
  if (!artist || !album) return;

  const content = document.getElementById("shawtifyAlbumInspectContent");
  if (!content) return;

  const tracks = album.tracks || [
    { num: 1, title: album.title, streams: album.totalStreams, duration: "3:20" }
  ];

  const safeArtistName = (artist.name || '').replace(/'/g, "\\'");
  const safeAlbumTitle = (album.title || '').replace(/'/g, "\\'");

  content.innerHTML = `
    <!-- Album Header -->
    <div class="spotify-album-header">
      <img src="${album.cover}" class="spotify-album-cover-lg" alt="${album.title}">
      <h1 class="spotify-album-page-title">${album.title}</h1>
      <div class="spotify-album-artist-meta">
        <img src="${artist.avatarImage || album.cover}" style="width: 20px; height: 20px; border-radius: 50%;" alt="${artist.name}">
        <span>${artist.name}</span>
      </div>
      <span class="spotify-album-meta-line">${album.type || 'Album'} &bull; ${album.year || '2026'} &bull; ${tracks.length} songs</span>
      <span class="spotify-album-meta-line" style="color: #1ed760; font-weight: 700; margin-top: 2px;">
        ${Number(album.totalStreams).toLocaleString()} total streams
      </span>
    </div>

    <!-- Album Action Bar -->
    <div class="spotify-album-actions">
      <div style="display: flex; align-items: center; gap: 14px;">
        <button class="spotify-icon-btn" onclick="showToast('SAVED TO LIBRARY')" title="Save to Library">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="16"></line>
            <line x1="8" y1="12" x2="16" y2="12"></line>
          </svg>
        </button>
        <button class="spotify-icon-btn" onclick="showToast('DOWNLOADED FOR OFFLINE PLAY')" title="Download">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 8v8M8 12l4 4 4-4"></path>
          </svg>
        </button>
      </div>
      <button class="spotify-green-play-btn" onclick="playSpotifyTrack('${(tracks[0].title || '').replace(/'/g, "\\'")}', '${safeArtistName}', '${album.cover}')" title="Play Album">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="#000000">
          <polygon points="6 4 20 12 6 20 6 4"/>
        </svg>
      </button>
    </div>

    <!-- Tracks List with Exact Streams -->
    <div class="spotify-album-tracks-list">
      ${tracks.map((tr, i) => {
        const safeTrTitle = (tr.title || '').replace(/'/g, "\\'");
        return `
        <div class="spotify-album-track-row" onclick="playSpotifyTrack('${safeTrTitle}', '${safeArtistName}', '${album.cover}', '${tr.id || i}')">
          <span class="spotify-track-num">${tr.num || (i + 1)}</span>
          <div class="spotify-track-details">
            <span class="spotify-track-name">${tr.title}</span>
            <span class="spotify-track-streams">${Number(tr.streams).toLocaleString()} streams</span>
          </div>
          <span class="spotify-track-duration">${tr.duration || '3:15'}</span>
          <button class="spotify-song-more" onclick="event.stopPropagation(); showToast('OPTIONS FOR: ${safeTrTitle.toUpperCase()}')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <circle cx="12" cy="5" r="1.8"/><circle cx="12" cy="12" r="1.8"/><circle cx="12" cy="19" r="1.8"/>
            </svg>
          </button>
        </div>
      `;}).join('')}
    </div>
  `;
}

function renderSpotifyDiscographyDOM(artistId) {
  const artist = SPOTIFY_ARTISTS_DATA[artistId] || SPOTIFY_ARTISTS_DATA[activeViewingArtistId];
  if (!artist) return;

  const content = document.getElementById("shawtifyDiscographyContent");
  if (!content) return;

  const allReleases = (artist.albums && artist.albums.length > 0) ? artist.albums : (artist.showcaseReleases || []);

  content.innerHTML = `
    <div style="padding: 56px 16px 10px 16px;">
      <h1 style="font-size: 1.4rem; font-weight: 900; margin: 0 0 4px 0;">${artist.name}</h1>
      <span style="font-size: 0.74rem; color: #b3b3b3; font-weight: 500;">Complete Discography &bull; ${allReleases.length} releases</span>
    </div>

    <div class="spotify-releases-list">
      ${allReleases.map(rel => `
        <div class="spotify-release-card" onclick="openSpotifyAlbum('${rel.id}', '${artist.id}')">
          <img src="${rel.cover}" class="spotify-release-thumb" alt="${rel.title}">
          <div class="spotify-release-info">
            <span class="spotify-release-title">${rel.title}</span>
            <span class="spotify-release-meta">${rel.type} &bull; ${rel.year}</span>
            <span class="spotify-release-streams">${Number(rel.totalStreams).toLocaleString()} total streams</span>
          </div>
          <div class="spotify-release-arrow">&rsaquo;</div>
        </div>
      `).join('')}
    </div>
  `;
}

function toggleSpotifyFollow(artistId, btnEl) {
  playMechanicalClick();
  const artist = SPOTIFY_ARTISTS_DATA[artistId];
  if (!artist) return;

  artist.following = !artist.following;
  if (btnEl) {
    btnEl.classList.toggle("following", artist.following);
    btnEl.textContent = artist.following ? "Following" : "Follow";
  }

  showToast(`${artist.following ? 'FOLLOWED' : 'UNFOLLOWED'} ${artist.name.toUpperCase()}`);
}

function playSpotifyTopTrack(artistId) {
  playMechanicalClick();
  const artist = SPOTIFY_ARTISTS_DATA[artistId];
  if (!artist || !artist.popularTracks || artist.popularTracks.length === 0) return;

  const topTrack = artist.popularTracks[0];
  playSpotifyTrack(topTrack.title, artist.name, topTrack.cover, topTrack.id);
}

function playSpotifyTrack(title, artist, cover, trackId = null) {
  playMechanicalClick();
  activePlayingTrackId = trackId;

  // Update Mini-Player
  const miniPlayer = document.getElementById("spotifyMiniPlayer");
  const coverEl = document.getElementById("miniPlayerCover");
  const titleEl = document.getElementById("miniPlayerTitle");
  const artistEl = document.getElementById("miniPlayerArtist");
  const progressFill = document.getElementById("miniPlayerProgress");

  if (miniPlayer) miniPlayer.style.display = "flex";
  if (coverEl) coverEl.src = cover || "album covers/download (10).jpg";
  if (titleEl) titleEl.textContent = title;
  if (artistEl) artistEl.textContent = artist;

  // Animate Progress Bar
  if (progressFill) {
    progressFill.style.width = "0%";
    setTimeout(() => { progressFill.style.width = "45%"; }, 100);
  }

  // Update playing bars in tracklist if visible
  document.querySelectorAll(".spotify-song-row").forEach(row => {
    const t = row.querySelector(".spotify-song-title");
    if (t && t.textContent.trim().toLowerCase() === title.trim().toLowerCase()) {
      row.classList.add("playing");
    } else {
      row.classList.remove("playing");
    }
  });

  showToast(`NOW STREAMING ON SHAWTIFY: ${title.toUpperCase()}`);
}

function toggleMiniPlayerPlay(e) {
  if (e) e.stopPropagation();
  playMechanicalClick();
  const icon = document.getElementById("miniPlayerPlayIcon");
  if (!icon) return;

  const isPaused = icon.innerHTML.includes("polygon");
  if (isPaused) {
    icon.innerHTML = '<path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>';
    showToast("SHAWTIFY: RESUMED");
  } else {
    icon.innerHTML = '<polygon points="6 4 20 12 6 20 6 4"/>';
    showToast("SHAWTIFY: PAUSED");
  }
}

function openMiniPlayerFull() {
  playMechanicalClick();
  showToast("NOW PLAYING FULL VIEW");
}
