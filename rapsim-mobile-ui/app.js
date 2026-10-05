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

  const calClock = document.getElementById("calendarPhoneClock");
  if (calClock) calClock.textContent = timeStr;

  const beatstoreClock = document.getElementById("beatstorePhoneClock");
  if (beatstoreClock) beatstoreClock.textContent = timeStr;
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
  if (appName === "calendar") {
    openCalendarApp();
    return;
  }
  if (appName === "beatstore") {
    openBeatstoreApp();
    return;
  }
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
  if (moduleKey === "labels") {
    openProfileLabelsSubpage();
    return;
  }
  if (moduleKey === "management") {
    openProfileManagementSubpage();
    return;
  }
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

// ==========================================================================
// PROFILE SUBPAGE: LABELS & RECORD DEALS ENGINE
// ==========================================================================

let currentLabelsSection = "all"; // "all" | "your"
let currentSignedLabelId = "label-greater";

let greaterRecordsState = {
  recoupmentRemaining: 793428,
  commitmentFulfilled: 2,
  commitmentTotal: 4,
  weeksLeft: 56,
  totalWeeks: 102,
  prestige: 78
};

let staffRelationships = {
  vance: 68,
  rostova: 74,
  hayes: 58,
  chen: 82
};

const LABELS_DATA = [
  {
    id: "label-apex",
    name: "APEX RECORDS",
    prestige: 94,
    minPopularity: 85,
    contractYears: 8,
    contractWeeks: 416,
    albumCommitment: 4,
    advance: 35000000,
    advanceDisplay: "$ 35,000,000",
    tier: "Global Megacorp",
    royaltySplit: "18% Artist / 82% Label",
    mastersOwnership: "Label Owns 100% In Perpetuity",
    marketingBudget: "$ 5,000,000 Guaranteed per LP",
    creativeControl: "Label Executive Final Say",
    territory: "Worldwide Exclusive",
    description: "Apex Records is the supreme titan of the global music industry. Home to stadium-selling icons, Apex guarantees ungodly resources, massive radio monopolization, and eight-figure advances, but demands strictly calculated commercial hits.",
    promises: [
      "$5,000,000 worldwide multimedia marketing campaign per album cycle",
      "Immediate front-page placement on all streaming services worldwide",
      "Direct clearances with A-list producers and superstar feature artists",
      "Super Bowl and global stadium tour booking priority"
    ],
    cuts: [
      "Streaming & Digital Sales: 18% Artist / 82% Label",
      "Physical Vinyl / CD Distribution: 15% Artist / 85% Label",
      "Sync & Commercial Licenses: 50% Artist / 50% Label",
      "Merchandise & Touring 360 Cut: 25% Label Deduction"
    ]
  },
  {
    id: "label-midass",
    name: "MIDASS RECORDS",
    prestige: 65,
    minPopularity: 55,
    contractYears: 3,
    contractWeeks: 156,
    albumCommitment: 2,
    advance: 1000000,
    advanceDisplay: "$ 1,000,000",
    tier: "Mid-Tier Major-Indie",
    royaltySplit: "40% Artist / 60% Label",
    mastersOwnership: "10-Year Reversion to Artist",
    marketingBudget: "$ 400,000 Targeted Budget",
    creativeControl: "Mutual Creative Approval",
    territory: "Worldwide Exclusive",
    description: "Midass Records strikes a rare, artist-friendly balance. Offering a seven-figure advance with fair 40% royalties and a 10-year master reversion clause, they are a favorite among rising rap visionaries.",
    promises: [
      "$400,000 targeted digital & influencer promotional campaign",
      "Full master recording reversion back to artist after 10 years",
      "Complete artistic freedom on beat selection and track length",
      "Dedicated A&R sound engineering liaison"
    ],
    cuts: [
      "Streaming & Digital: 40% Artist / 60% Label",
      "Sync & Licensing: 50% Artist / 50% Label",
      "Zero deductions on touring and personal merchandise"
    ]
  },
  {
    id: "label-never",
    name: "NEVER RECORDS",
    prestige: 25,
    minPopularity: 25,
    contractYears: 4,
    contractWeeks: 208,
    albumCommitment: 5,
    advance: 350000,
    advanceDisplay: "$ 350,000",
    tier: "Predatory Underground Deal",
    royaltySplit: "12% Artist / 88% Label",
    mastersOwnership: "Label Owns In Perpetuity",
    marketingBudget: "$ 150,000 Budget",
    creativeControl: "Strict Label Direction",
    territory: "Worldwide 360 Deal",
    description: "Infamous predatory 360 trap deal. Low popularity barrier makes it tempting for starving newcomers, but the five-project commitment and punitive 12% royalty rate will lock you in legal shackles.",
    promises: [
      "Fast cash advance injection directly into your account",
      "Standard digital distribution to Spotify, Apple, and Tidal",
      "Local club DJ network promotion"
    ],
    cuts: [
      "Streaming & Digital: 12% Artist / 88% Label",
      "Merchandise Take: 40% Label Cut",
      "Live Touring Take: 30% Label Cut"
    ]
  },
  {
    id: "label-greater",
    name: "GREATER RECORDS",
    isCurrentLabel: true,
    prestige: 78,
    minPopularity: 60,
    contractYears: 4,
    contractWeeks: 102,
    albumCommitment: 4,
    advance: 1800000,
    advanceDisplay: "$ 1,800,000",
    tier: "Prestigious Urban Powerhouse",
    royaltySplit: "35% Artist / 65% Label (Jumps to 45% post-recoupment)",
    mastersOwnership: "Joint Venture (50/50 Split)",
    marketingBudget: "$ 750,000 per project",
    creativeControl: "Artist Holds Full Sonic Discretion",
    territory: "Worldwide Exclusive",
    description: "Your current record label! Greater Records is an elite hip-hop and alternative powerhouse founded by music veteran Marcus Vance. Home to megastar K-Vibe and yourself.",
    promises: [
      "$750,000 marketing and video budget per project",
      "Direct placement on Rap Caviar and flagship Spotify playlists",
      "Full access to Greater Sound complexes in Tokyo & Los Angeles",
      "Dedicated in-house Grammy-winning mixing engineers"
    ],
    cuts: [
      "Streaming & Digital: 35% Artist / 65% Label until recoupment",
      "Post-Recoupment: 45% Artist / 55% Label for life of contract",
      "Sync & Film: 50% / 50% split",
      "Zero touring cuts (Artist keeps 100% of live revenue)"
    ]
  },
  {
    id: "label-deathrow",
    name: "DEATH ROW HERITAGE",
    prestige: 82,
    minPopularity: 70,
    contractYears: 5,
    contractWeeks: 260,
    albumCommitment: 3,
    advance: 4500000,
    advanceDisplay: "$ 4,500,000",
    tier: "Legacy Street Heavyweight",
    royaltySplit: "25% Artist / 75% Label",
    mastersOwnership: "Label Owns 100%",
    marketingBudget: "$ 1,200,000 Budget",
    creativeControl: "Street Authenticity Required",
    territory: "Worldwide Exclusive",
    description: "Legendary West Coast imprint known for hardcore anthems, unmistakable swagger, and street credibility that money cannot buy.",
    promises: [
      "$1,200,000 street-level & national radio promotional push",
      "Collaborative access to the iconic Death Row archives & producers",
      "Heavy radio rotation across major coastal markets"
    ],
    cuts: [
      "Streaming: 25% Artist / 75% Label",
      "Merch: 20% Label Cut",
      "Sync & Games: 50% / 50% Split"
    ]
  },
  {
    id: "label-ovosound",
    name: "OVO SOUND DISTRO",
    prestige: 91,
    minPopularity: 80,
    contractYears: 3,
    contractWeeks: 156,
    albumCommitment: 2,
    advance: 12500000,
    advanceDisplay: "$ 12,500,000",
    tier: "Boutique Megastar Imprint",
    royaltySplit: "30% Artist / 70% Label",
    mastersOwnership: "7-Year Reversion Clause",
    marketingBudget: "$ 3,000,000 Global Push",
    creativeControl: "Full Artist Direction",
    territory: "Worldwide Exclusive",
    description: "Elite boutique label offering massive eight-figure funding, moody atmospheric sonic palettes, and direct co-signs that turn underground artists into global icons.",
    promises: [
      "$3,000,000 global marketing rollout and visual trailers",
      "Immediate Apple Music & Spotify front-cover placement",
      "Direct collaborations with the Toronto & OVO sound collective"
    ],
    cuts: [
      "Streaming: 30% Artist / 70% Label",
      "Masters revert after 7 years",
      "Sync & Brand Deals: 60% Artist / 40% Label"
    ]
  },
  {
    id: "label-cactusjack",
    name: "CACTUS JACK SOUND",
    prestige: 88,
    minPopularity: 75,
    contractYears: 4,
    contractWeeks: 208,
    albumCommitment: 3,
    advance: 8000000,
    advanceDisplay: "$ 8,000,000",
    tier: "Cultural Hype Machine",
    royaltySplit: "32% Artist / 68% Label",
    mastersOwnership: "Joint Venture Imprint",
    marketingBudget: "$ 2,500,000 Merch & Visuals",
    creativeControl: "Experimental Artistic Freedom",
    territory: "Worldwide Exclusive",
    description: "The epicenter of rage, psychedelic trap, and streetwear domination. Signing here pairs your music with insane merchandise rollouts and arena festival slots.",
    promises: [
      "$2,500,000 experimental visual & festival stage marketing budget",
      "Global collaborative merchandise capsules & sneaker tie-ins",
      "Headline festival billing across rolling loud circuits"
    ],
    cuts: [
      "Streaming: 32% Artist / 68% Label",
      "Joint venture imprint profit sharing",
      "Merchandise: 50% / 50% Split"
    ]
  },
  {
    id: "label-rusticroots",
    name: "RUSTIC ROOTS ENT",
    prestige: 52,
    minPopularity: 30,
    contractYears: 2,
    contractWeeks: 104,
    albumCommitment: 1,
    advance: 250000,
    advanceDisplay: "$ 250,000",
    tier: "Pure Indie Sanctuary",
    royaltySplit: "70% Artist / 30% Label",
    mastersOwnership: "Artist Owns 100% From Day 1",
    marketingBudget: "$ 100,000 Grassroots Push",
    creativeControl: "100% Unfiltered Artist Autonomy",
    territory: "Non-Exclusive Distribution",
    description: "An ethical indie haven. Perfect for lyrical purists who want to own 100% of their masters, keep 70% of royalties, and answer to no corporate boardroom.",
    promises: [
      "Artist retains 100% master ownership from moment of creation",
      "70% artist royalty rate on all digital sales and streams",
      "Zero contractual intervention in track themes or runtime"
    ],
    cuts: [
      "Streaming: 70% Artist / 30% Label",
      "Zero 360 deductions on tours, merch, or publishing"
    ]
  },
  {
    id: "label-subzero",
    name: "SUB ZERO RECORDS",
    prestige: 60,
    minPopularity: 45,
    contractYears: 3,
    contractWeeks: 156,
    albumCommitment: 3,
    advance: 750000,
    advanceDisplay: "$ 750,000",
    tier: "Street Drill Pioneer",
    royaltySplit: "28% Artist / 72% Label",
    mastersOwnership: "Label Owns 100%",
    marketingBudget: "$ 300,000 Street & Visuals",
    creativeControl: "Raw Street Autonomy",
    territory: "UK & US Drill Specialist",
    description: "The raw home of UK and Brooklyn drill. Dark 808 slides, aggressive cinematic music videos, and heavy European festival distribution.",
    promises: [
      "$300,000 budget for 4K cinematic music videos and visualizers",
      "Direct pitching to top UK drill & grime editorial playlists",
      "London & New York cross-Atlantic promotion"
    ],
    cuts: [
      "Streaming: 28% Artist / 72% Label",
      "Sync: 50% / 50% Split",
      "Touring: 15% Label Cut"
    ]
  },
  {
    id: "label-monolith",
    name: "MONOLITH GLOBAL CORP",
    prestige: 98,
    minPopularity: 92,
    contractYears: 10,
    contractWeeks: 520,
    albumCommitment: 6,
    advance: 50000000,
    advanceDisplay: "$ 50,000,000",
    tier: "Trillion-Dollar Conglomerate",
    royaltySplit: "15% Artist / 85% Label",
    mastersOwnership: "In Perpetuity Corporate Asset",
    marketingBudget: "$ 10,000,000 Global Blitz",
    creativeControl: "Strict Boardroom Approval",
    territory: "Intergalactic / Worldwide",
    description: "The ultimate corporate behemoth. A $50,000,000 check that puts your music into Hollywood franchise blockbusters, theme parks, and every radio wave on Earth—at the cost of a decade-long corporate contract.",
    promises: [
      "$10,000,000 worldwide omni-channel release budget per album",
      "Guaranteed Billboard #1 chart lobbying and Grammy push",
      "Placement on billion-dollar Hollywood blockbuster soundtracks",
      "Private jet travel and dedicated security detachment"
    ],
    cuts: [
      "Streaming: 15% Artist / 85% Label",
      "Physical: 12% Artist / 88% Label",
      "Masters: Corporate property in perpetuity",
      "Merch & Touring: 30% Label cut"
    ]
  }
];

const GREATER_RECORDS_MUSIC = [
  {
    title: "Late Night in Shibuya",
    type: "Studio LP",
    year: "Year 2",
    tracksCount: 12,
    streams: 48290100,
    grossRevenue: 193160,
    artistCut: 67606,
    recoupedAmount: 67606,
    cover: "album covers/download (10).jpg"
  },
  {
    title: "Tokyo Drift",
    type: "EP",
    year: "Year 2",
    tracksCount: 6,
    streams: 24120000,
    grossRevenue: 96480,
    artistCut: 33768,
    recoupedAmount: 33768,
    cover: "album covers/download (4).jpg"
  }
];

const GREATER_RECORDS_ROSTER = [
  {
    id: "roster-kvibe",
    name: "K-Vibe",
    tier: "Flagship Megastar",
    monthlyListeners: "28,400,000",
    chemistry: 85,
    avatar: "album covers/Tyler Durden.jpg",
    status: "Label Flagship"
  },
  {
    id: "roster-synapse",
    name: "Lil Synapse",
    tier: "Rising Phenom (YOU)",
    monthlyListeners: "4,820,000",
    chemistry: 100,
    avatar: "album covers/download (10).jpg",
    status: "Priority Prospect"
  },
  {
    id: "roster-asapghost",
    name: "A$AP Ghost",
    tier: "Mainstream Heavyweight",
    monthlyListeners: "14,200,000",
    chemistry: 62,
    avatar: "album covers/download (6).jpg",
    status: "Album Dropping in 2 Wks"
  },
  {
    id: "roster-lunasky",
    name: "Luna Sky",
    tier: "R&B Sensation",
    monthlyListeners: "9,800,000",
    chemistry: 75,
    avatar: "album covers/Music artwork for Frank Ocean - _.jpg",
    status: "Single Dropping this Week"
  },
  {
    id: "roster-trapsensei",
    name: "Trap Sensei",
    tier: "Underground Signee",
    monthlyListeners: "1,200,000",
    chemistry: 45,
    avatar: "album covers/download (3).jpg",
    status: "Developing"
  }
];

const GREATER_RECORDS_CALENDAR = [
  {
    week: "WEEK 1 (CURRENT)",
    dateRange: "JUN 12 - 18",
    artist: "Luna Sky",
    releaseTitle: "Velvet Nights (Lead Single)",
    format: "Single + Music Video",
    promoPush: "Billboard Blitz & Spotify New Music Friday Cover",
    status: "Dropping This Friday"
  },
  {
    week: "WEEK 2",
    dateRange: "JUN 19 - 25",
    artist: "A$AP Ghost",
    releaseTitle: "Grim Reaper (Studio LP)",
    format: "14-Track Album",
    promoPush: "Rolling Stone Feature & National Radio Syndication",
    status: "Master Turned In"
  },
  {
    week: "WEEK 3",
    dateRange: "JUN 26 - JUL 02",
    artist: "Lil Synapse (YOU)",
    releaseTitle: "Scheduled Studio Session & Pre-Save Push",
    format: "Pre-Release Rollout",
    promoPush: "TikTok Trend Campaign & DJ Pool Promo",
    status: "Your Allocated Window"
  },
  {
    week: "WEEK 4",
    dateRange: "JUL 03 - 09",
    artist: "K-Vibe ft. Lil Synapse",
    releaseTitle: "Crown Heavy (Summer Anthem)",
    format: "Major Collab Single",
    promoPush: "Rap Caviar #1 Placement & Global DSP Banner",
    status: "In Final Mix & Master"
  }
];

const GREATER_RECORDS_STAFF = [
  {
    id: "vance",
    name: "Marcus Vance",
    role: "Founder & Chief Executive Officer",
    avatarLetter: "M",
    relationship: 68,
    quote: "Keep your work ethic high. Greater Records has the resources to make you an untouchable icon if you deliver.",
    reputationBenefit: "Good relationship with Marcus boosts label priority and unlocks early release permissions."
  },
  {
    id: "rostova",
    name: "Elena Rostova",
    role: "Head of A&R & Talent Direction",
    avatarLetter: "E",
    relationship: 74,
    quote: "I just secured a folder of unreleased superstar beats. Let me know when you want to pick production for project #3.",
    reputationBenefit: "High relationship clears superstar guest features with 50% discount."
  },
  {
    id: "hayes",
    name: "Darnell 'D-Beam' Hayes",
    role: "VP of Global Marketing & DSP Relations",
    avatarLetter: "D",
    relationship: 58,
    quote: "Give me an irresistible 15-second hook and I will get your face plastered across Times Square.",
    reputationBenefit: "High relationship unlocks editorial playlist pitching and Times Square billboards."
  },
  {
    id: "chen",
    name: "Chloe Chen",
    role: "Lead In-House Sound Engineer",
    avatarLetter: "C",
    relationship: 82,
    quote: "Your vocals cut through the low end like butter. Let's lock in for another marathon mixing session.",
    reputationBenefit: "High relationship gives free studio vocal polish and boosts track sonic quality."
  }
];

// SVGs Helper Generators
function getWaxSealSVG(size = 44) {
  return `
    <svg width="${size}" height="${size}" viewBox="0 0 60 60" fill="none">
      <defs>
        <radialGradient id="waxGrad_${size}" cx="35%" cy="30%" r="65%">
          <stop offset="0%" stop-color="#dc2626"/>
          <stop offset="35%" stop-color="#b91c1c"/>
          <stop offset="70%" stop-color="#991b1b"/>
          <stop offset="90%" stop-color="#7f1d1d"/>
          <stop offset="100%" stop-color="#450a0a"/>
        </radialGradient>
        <radialGradient id="innerBed_${size}" cx="40%" cy="35%" r="60%">
          <stop offset="0%" stop-color="#991b1b"/>
          <stop offset="70%" stop-color="#781717"/>
          <stop offset="100%" stop-color="#450a0a"/>
        </radialGradient>
        <filter id="waxShadow_${size}" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="3" stdDeviation="2.5" flood-color="#000000" flood-opacity="0.45"/>
        </filter>
      </defs>
      <!-- Molten wax outer irregular scalloped edge -->
      <path d="M30 3 C36 2, 40 5, 45 7 C50 9, 54 13, 56 18 C58 23, 57 27, 58 32 C59 37, 57 42, 54 47 C51 52, 46 54, 41 57 C36 60, 31 58, 28 58 C24 58, 19 59, 15 57 C10 55, 6 51, 4 46 C2 41, 1 36, 2 31 C3 26, 1 21, 4 16 C7 11, 12 7, 17 6 C22 5, 25 3, 30 3 Z" fill="url(#waxGrad_${size})" filter="url(#waxShadow_${size})"/>
      
      <!-- Wax bevel highlight & rim -->
      <path d="M22 6 C30 4, 42 6, 48 12 C52 16, 54 22, 54 28" stroke="#fca5a5" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.5"/>
      <path d="M12 48 C16 53, 24 56, 32 55" stroke="#450a0a" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.7"/>

      <!-- Concentric inner seal ridge -->
      <circle cx="30" cy="30" r="18.5" fill="none" stroke="#450a0a" stroke-width="1.5" stroke-dasharray="3 2" opacity="0.8"/>
      <circle cx="30" cy="30" r="17.5" fill="none" stroke="#fca5a5" stroke-width="0.8" opacity="0.3"/>
      
      <!-- Embossed inner bed -->
      <circle cx="30" cy="30" r="14.5" fill="url(#innerBed_${size})"/>
      
      <!-- Embossed vinyl record / label crest rings -->
      <circle cx="30" cy="30" r="11" stroke="#450a0a" stroke-width="1.2" fill="none"/>
      <circle cx="30" cy="30" r="11" stroke="#fca5a5" stroke-width="0.6" stroke-dasharray="8 6" fill="none" opacity="0.35"/>
      <circle cx="30" cy="30" r="7.5" stroke="#450a0a" stroke-width="1" fill="none"/>
      <circle cx="30" cy="30" r="4" fill="#3b0707" stroke="#b91c1c" stroke-width="0.8"/>
      
      <!-- Specular gloss glint -->
      <ellipse cx="23" cy="20" rx="4" ry="2" transform="rotate(-30 23 20)" fill="#ffffff" opacity="0.25"/>
    </svg>
  `;
}

function getFountainPenSigSVG() {
  return `
    <svg width="44" height="34" viewBox="0 0 52 40" fill="none">
      <path d="M4 35 Q 16 26, 26 34 T 44 31" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" fill="none"/>
      <path d="M12 33 Q 18 20, 24 32" stroke="#2563eb" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <path d="M26 31 Q 32 18, 38 29" stroke="#2563eb" stroke-width="1.6" stroke-linecap="round" fill="none"/>
      <g transform="translate(24, 2) rotate(42)">
        <path d="M0 0 L7 0 L7 17 L3.5 25 L0 17 Z" fill="#0f172a"/>
        <path d="M1.2 17 L5.8 17 L3.5 25 Z" fill="#f59e0b" stroke="#b45309" stroke-width="0.5"/>
        <line x1="3.5" y1="17" x2="3.5" y2="23" stroke="#78350f" stroke-width="0.6"/>
        <rect x="0" y="0" width="7" height="4" fill="#94a3b8"/>
        <line x1="2" y1="4" x2="2" y2="15" stroke="#334155" stroke-width="1"/>
      </g>
    </svg>
  `;
}

function getContractDocInspectSVG() {
  return `
    <svg width="30" height="34" viewBox="0 0 34 38" fill="none">
      <path d="M4 3 L22 3 L29 10 L29 35 A 2 2 0 0 1 27 37 L4 37 A 2 2 0 0 1 2 35 L2 5 A 2 2 0 0 1 4 3 Z" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
      <path d="M22 3 L22 10 L29 10 Z" fill="#cbd5e1" stroke="#1e293b" stroke-width="1.6"/>
      <line x1="6" y1="13" x2="19" y2="13" stroke="#334155" stroke-width="1.6"/>
      <line x1="6" y1="18" x2="25" y2="18" stroke="#334155" stroke-width="1.6"/>
      <line x1="6" y1="23" x2="18" y2="23" stroke="#334155" stroke-width="1.6"/>
      <circle cx="21" cy="27" r="5.5" fill="#f8fafc" stroke="#1e293b" stroke-width="2"/>
      <line x1="25.5" y1="31.5" x2="31" y2="37" stroke="#1e293b" stroke-width="2.6" stroke-linecap="round"/>
      <circle cx="21" cy="27" r="3" fill="#60a5fa" opacity="0.3"/>
    </svg>
  `;
}

function getYourMusicIconSVG() {
  return `
    <svg width="30" height="30" viewBox="0 0 36 36" fill="none">
      <circle cx="15" cy="17" r="13" fill="#18181b" stroke="#3f3f46" stroke-width="1"/>
      <circle cx="15" cy="17" r="8" stroke="#71717a" stroke-width="0.8" fill="none"/>
      <circle cx="15" cy="17" r="5" fill="#b91c1c"/>
      <circle cx="15" cy="17" r="2" fill="#fef08a"/>
      <circle cx="23" cy="20" r="13" fill="#27272a" stroke="#d97706" stroke-width="1.2"/>
      <circle cx="23" cy="20" r="9" stroke="#fbbf24" stroke-width="0.8" stroke-dasharray="6 3" fill="none"/>
      <circle cx="23" cy="20" r="5" fill="#d97706"/>
      <circle cx="23" cy="20" r="2" fill="#fffbeb"/>
    </svg>
  `;
}

function getLabelRosterIconSVG() {
  return `
    <svg width="28" height="30" viewBox="0 0 32 36" fill="none">
      <rect x="3" y="5" width="26" height="28" rx="2.5" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.4"/>
      <rect x="11" y="2" width="10" height="6" rx="1.5" fill="#64748b" stroke="#334155" stroke-width="1.2"/>
      <rect x="6.5" y="11" width="3.5" height="3.5" rx="0.6" fill="#f97316"/>
      <line x1="12.5" y1="13" x2="25" y2="13" stroke="#334155" stroke-width="1.6"/>
      <rect x="6.5" y="17" width="3.5" height="3.5" rx="0.6" fill="#f97316"/>
      <line x1="12.5" y1="19" x2="23" y2="19" stroke="#334155" stroke-width="1.6"/>
      <rect x="6.5" y="23" width="3.5" height="3.5" rx="0.6" fill="#f97316"/>
      <line x1="12.5" y1="25" x2="25" y2="25" stroke="#334155" stroke-width="1.6"/>
    </svg>
  `;
}

function getLabelCalendarIconSVG() {
  return `
    <svg width="30" height="30" viewBox="0 0 36 34" fill="none">
      <rect x="2" y="8" width="32" height="23" rx="2.5" fill="#ffffff" stroke="#94a3b8" stroke-width="1.4"/>
      <path d="M2 10.5 A 2.5 2.5 0 0 1 4.5 8 L31.5 8 A 2.5 2.5 0 0 1 34 10.5 L34 15 L2 15 Z" fill="#ef4444"/>
      <circle cx="8" cy="8" r="1.6" fill="#1e293b"/>
      <circle cx="15" cy="8" r="1.6" fill="#1e293b"/>
      <circle cx="22" cy="8" r="1.6" fill="#1e293b"/>
      <circle cx="29" cy="8" r="1.6" fill="#1e293b"/>
      <circle cx="9" cy="20" r="1.4" fill="#64748b"/>
      <circle cx="16" cy="20" r="1.4" fill="#64748b"/>
      <circle cx="23" cy="20" r="1.4" fill="#64748b"/>
      <circle cx="30" cy="20" r="1.4" fill="#ef4444"/>
      <circle cx="9" cy="26" r="1.4" fill="#64748b"/>
      <circle cx="16" cy="26" r="1.4" fill="#64748b"/>
      <circle cx="23" cy="26" r="1.4" fill="#ef4444"/>
      <circle cx="30" cy="26" r="1.4" fill="#64748b"/>
    </svg>
  `;
}

function getLabelStaffIconSVG() {
  return `
    <svg width="30" height="30" viewBox="0 0 36 34" fill="none">
      <circle cx="18" cy="11" r="5" stroke="#3b82f6" stroke-width="2" fill="none"/>
      <path d="M9 27 C9 20, 27 20, 27 27" stroke="#3b82f6" stroke-width="2" fill="none"/>
      <circle cx="8.5" cy="13" r="3.8" stroke="#6366f1" stroke-width="1.8" fill="none"/>
      <path d="M2 28 C2 23, 13 23, 13 28" stroke="#6366f1" stroke-width="1.8" fill="none"/>
      <circle cx="27.5" cy="13" r="3.8" stroke="#6366f1" stroke-width="1.8" fill="none"/>
      <path d="M23 28 C23 23, 34 23, 34 28" stroke="#6366f1" stroke-width="1.8" fill="none"/>
    </svg>
  `;
}

function getLabelRequestsIconSVG() {
  return `
    <svg width="30" height="28" viewBox="0 0 36 34" fill="none">
      <ellipse cx="14" cy="14" rx="12" ry="9" fill="#ef4444" opacity="0.85"/>
      <polygon points="7,21 12,20 6,26" fill="#ef4444" opacity="0.85"/>
      <ellipse cx="24" cy="20" rx="11" ry="8" fill="#dc2626"/>
      <polygon points="27,26 23,24 28,30" fill="#dc2626"/>
    </svg>
  `;
}

function getLabelHistoryIconSVG() {
  return `
    <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
      <circle cx="16" cy="16" r="12" stroke="#1e293b" stroke-width="2.4"/>
      <polyline points="16,10 16,16 21,16" stroke="#1e293b" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M9 9 L4 13 L10 14" stroke="#1e293b" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `;
}

// Subpage Open & Close
function openProfileLabelsSubpage(initialSection = "all") {
  playMechanicalClick();
  const hub = document.getElementById("profileMainHub");
  const subpage = document.getElementById("profileSubpageLabels");
  if (!subpage) return;

  if (hub) hub.style.display = "none";
  subpage.style.display = "flex";
  subpage.scrollTop = 0;

  switchLabelsSection(initialSection);
}

function closeProfileLabelsSubpage() {
  playMechanicalClick();
  const hub = document.getElementById("profileMainHub");
  const subpage = document.getElementById("profileSubpageLabels");
  if (subpage) subpage.style.display = "none";
  if (hub) hub.style.display = "flex";
}

function switchLabelsSection(section) {
  playMechanicalClick();
  currentLabelsSection = section;

  const btnAll = document.getElementById("tabBtnLabelsAll");
  const btnYour = document.getElementById("tabBtnLabelsYour");
  const secAll = document.getElementById("labelsSectionAll");
  const secYour = document.getElementById("labelsSectionYour");

  if (section === "all") {
    if (btnAll) btnAll.classList.add("active");
    if (btnYour) btnYour.classList.remove("active");
    if (secAll) secAll.style.display = "flex";
    if (secYour) secYour.style.display = "none";
    renderAllLabelsContracts();
  } else {
    if (btnAll) btnAll.classList.remove("active");
    if (btnYour) btnYour.classList.add("active");
    if (secAll) secAll.style.display = "none";
    if (secYour) secYour.style.display = "flex";
    renderYourLabelContract();
  }
}

// 1. Render ALL LABELS (10 Dummy Contracts)
function renderAllLabelsContracts() {
  const container = document.getElementById("labelsSectionAll");
  if (!container) return;

  container.innerHTML = LABELS_DATA.map(label => `
    <div class="label-contract-card" onclick="openLabelContractModal('${label.id}')">
      <!-- Crimson Wax Seal Stamp -->
      <div class="contract-wax-seal">
        ${getWaxSealSVG(44)}
      </div>

      <!-- Label Title -->
      <h2 class="label-contract-title">${label.name}</h2>

      <!-- Contract Conditions Grid -->
      <div class="label-contract-meta-grid">
        <div class="label-meta-row">
          <span class="label-meta-key">PRESTIGE :</span>
          <span class="label-meta-val">${label.prestige}/100</span>
        </div>
        <div class="label-meta-row">
          <span class="label-meta-key">MIN ARTIST POPULARITY :</span>
          <span class="label-meta-val">${label.minPopularity}/100</span>
        </div>
        <div class="label-meta-row">
          <span class="label-meta-key">CONTRACT LENGTH :</span>
          <span class="label-meta-val">${label.contractYears} YEARS</span>
        </div>
        <div class="label-meta-row">
          <span class="label-meta-key">ALBUM COMMITMENT :</span>
          <span class="label-meta-val">${label.albumCommitment} PROJECTS</span>
        </div>
      </div>

      <!-- Bottom Row: Advance Pill + Signature Pen -->
      <div class="label-contract-bottom-row">
        <div class="label-advance-group">
          <span class="label-advance-label">ADVANCE :</span>
          <div class="label-advance-pill">${label.advanceDisplay}</div>
        </div>
        <div class="label-pen-signature">
          ${getFountainPenSigSVG()}
        </div>
      </div>
    </div>
  `).join("");
}

// 2. Render YOUR LABEL (GREATER RECORDS)
function renderYourLabelContract() {
  const container = document.getElementById("labelsSectionYour");
  if (!container) return;

  container.innerHTML = `
    <div class="your-label-parchment-card">
      <!-- Top Right Seals & Inspection Button -->
      <div class="your-label-top-seals">
        <div class="contract-wax-seal">
          ${getWaxSealSVG(44)}
        </div>
        <button class="your-label-contract-doc-btn" onclick="openLabelContractModal('label-greater')" title="Inspect Complete Contract">
          ${getContractDocInspectSVG()}
        </button>
      </div>

      <!-- Title -->
      <h1 class="your-label-title">GREATER RECORDS</h1>

      <!-- Stats Cluster -->
      <div class="your-label-stats-box">
        <div class="your-label-recoupment-pill">
          RECOUPMENT : $${Number(greaterRecordsState.recoupmentRemaining).toLocaleString()}
        </div>
        <div class="your-label-meta-item">
          <span>PRESTIGE : ${greaterRecordsState.prestige}/100</span>
          <span style="color: #eab308; font-size: 0.85rem;">★</span>
        </div>
        <div class="your-label-meta-item">
          COMMITMENT : ${greaterRecordsState.commitmentFulfilled}/${greaterRecordsState.commitmentTotal}
        </div>
        <div class="your-label-meta-item">
          WEEKS LEFT : ${greaterRecordsState.weeksLeft}/${greaterRecordsState.totalWeeks}
        </div>
      </div>

      <!-- 5 Action Buttons -->
      <div class="your-label-action-buttons">
        <button class="your-label-action-btn" onclick="openYourLabelSubdrawer('music')">
          <div class="your-label-btn-icon">${getYourMusicIconSVG()}</div>
          <span class="your-label-btn-label">YOUR MUSIC</span>
        </button>

        <button class="your-label-action-btn" onclick="openYourLabelSubdrawer('roster')">
          <div class="your-label-btn-icon">${getLabelRosterIconSVG()}</div>
          <span class="your-label-btn-label">LABEL ROSTER</span>
        </button>

        <button class="your-label-action-btn" onclick="openYourLabelSubdrawer('calendar')">
          <div class="your-label-btn-icon">${getLabelCalendarIconSVG()}</div>
          <span class="your-label-btn-label">LABEL RELEASE CALENDAR</span>
        </button>

        <button class="your-label-action-btn" onclick="openYourLabelSubdrawer('staff')">
          <div class="your-label-btn-icon">${getLabelStaffIconSVG()}</div>
          <span class="your-label-btn-label">LABEL STAFF</span>
        </button>

        <button class="your-label-action-btn" onclick="openYourLabelSubdrawer('requests')">
          <div class="your-label-btn-icon">${getLabelRequestsIconSVG()}</div>
          <span class="your-label-btn-label">REQUESTS</span>
        </button>
      </div>

      <!-- History Button -->
      <div class="your-label-history-wrap">
        <button class="your-label-history-btn" onclick="openLabelHistoryModal()" title="Contract History Archive">
          ${getLabelHistoryIconSVG()}
        </button>
      </div>
    </div>
  `;
}

// 3. Complete Formal Contract Modal
function openLabelContractModal(labelId) {
  playMechanicalClick();
  const label = LABELS_DATA.find(l => l.id === labelId) || LABELS_DATA[3];
  if (!label) return;

  const modal = document.getElementById("labelContractModal");
  const sealRow = document.getElementById("contractModalSealRow");
  const bodyContent = document.getElementById("contractModalBodyContent");
  const footerActions = document.getElementById("contractModalFooterActions");
  if (!modal || !sealRow || !bodyContent || !footerActions) return;

  const isCurrent = label.id === currentSignedLabelId;

  sealRow.innerHTML = `
    <div class="contract-modal-seal-badge">
      ${getWaxSealSVG(48)}
    </div>
    <div class="contract-modal-title-block">
      <h2>${label.name}</h2>
      <span>${label.tier} &bull; ${label.territory}</span>
    </div>
  `;

  bodyContent.innerHTML = `
    <!-- Preamble / Summary -->
    <p style="margin: 0; font-size: 0.74rem; color: #475569; font-style: italic;">
      ${label.description}
    </p>

    <!-- Clause 1: Key Terms & Commitment -->
    <div class="contract-clause-box">
      <div class="contract-clause-title">
        <span>§ 1. CONTRACT TERM & OUTPUT COMMITMENT</span>
      </div>
      <div class="contract-clause-grid">
        <div class="contract-clause-item">
          <span class="c-lbl">Contract Duration</span>
          <span class="c-val">${label.contractYears} Years (${label.contractWeeks} Weeks)</span>
        </div>
        <div class="contract-clause-item">
          <span class="c-lbl">Album Commitment</span>
          <span class="c-val">${label.albumCommitment} Studio Projects</span>
        </div>
        <div class="contract-clause-item">
          <span class="c-lbl">Prestige Rating</span>
          <span class="c-val">${label.prestige}/100</span>
        </div>
        <div class="contract-clause-item">
          <span class="c-lbl">Min Popularity Req</span>
          <span class="c-val">${label.minPopularity}/100</span>
        </div>
      </div>
    </div>

    <!-- Clause 2: Financial Terms & Advance -->
    <div class="contract-clause-box">
      <div class="contract-clause-title">
        <span>§ 2. FINANCIAL ADVANCE & RECOUPMENT</span>
      </div>
      <div class="contract-clause-grid">
        <div class="contract-clause-item">
          <span class="c-lbl">Upfront Cash Advance</span>
          <span class="c-val" style="color: #15803d; font-size: 0.85rem;">$ ${Number(label.advance).toLocaleString()}</span>
        </div>
        <div class="contract-clause-item">
          <span class="c-lbl">Master Ownership</span>
          <span class="c-val">${label.mastersOwnership}</span>
        </div>
        <div class="contract-clause-item">
          <span class="c-lbl">Royalty Split</span>
          <span class="c-val">${label.royaltySplit}</span>
        </div>
        <div class="contract-clause-item">
          <span class="c-lbl">Creative Control</span>
          <span class="c-val">${label.creativeControl}</span>
        </div>
      </div>
    </div>

    <!-- Clause 3: Label Promises & Support -->
    <div class="contract-clause-box">
      <div class="contract-clause-title">
        <span>§ 3. LABEL GUARANTEES & PROMISES</span>
      </div>
      <div class="contract-promise-list">
        ${label.promises.map(p => `
          <div class="contract-promise-row">
            <span class="bullet">✓</span>
            <span>${p}</span>
          </div>
        `).join("")}
      </div>
    </div>

    <!-- Clause 4: Revenue Deductions & Cuts -->
    <div class="contract-clause-box">
      <div class="contract-clause-title">
        <span>§ 4. DEDUCTIONS, SYNC & 360 TAKES</span>
      </div>
      <div class="contract-promise-list">
        ${label.cuts.map(c => `
          <div class="contract-promise-row">
            <span class="bullet" style="color: #dc2626;">&bull;</span>
            <span>${c}</span>
          </div>
        `).join("")}
      </div>
    </div>
  `;

  if (isCurrent) {
    footerActions.innerHTML = `
      <button class="contract-btn-sign" style="background: #2563eb; border-color: #1d4ed8;" onclick="showToast('THIS IS YOUR CURRENTLY ACTIVE LABEL DEAL')">
        CURRENT DEAL (ACTIVE)
      </button>
      <button class="contract-btn-close" onclick="closeLabelContractModal()">CLOSE</button>
    `;
  } else {
    footerActions.innerHTML = `
      <button class="contract-btn-sign" onclick="signLabelDeal('${label.id}')">
        SIGN DEAL (${label.advanceDisplay})
      </button>
      <button class="contract-btn-close" onclick="closeLabelContractModal()">CLOSE</button>
    `;
  }

  modal.style.display = "flex";
}

function closeLabelContractModal(e) {
  if (e && e.target && e.target.id !== "labelContractModal" && !e.target.classList.contains("contract-modal-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("labelContractModal");
  if (modal) modal.style.display = "none";
}

// 4. Interactive Sub-Drawer (Music, Roster, Calendar, Staff, Requests)
function openYourLabelSubdrawer(drawerType) {
  playMechanicalClick();
  const drawer = document.getElementById("yourLabelSubDrawer");
  const iconEl = document.getElementById("subdrawerHeaderIcon");
  const titleEl = document.getElementById("subdrawerHeaderTitle");
  const contentEl = document.getElementById("subdrawerBodyContent");
  if (!drawer || !iconEl || !titleEl || !contentEl) return;

  if (drawerType === "music") {
    iconEl.innerHTML = getYourMusicIconSVG();
    titleEl.textContent = "YOUR MUSIC UNDER GREATER RECORDS";
    contentEl.innerHTML = `
      <!-- Recoupment Progress Box -->
      <div style="background: #f1f5f9; border: 1.5px solid #cbd5e1; border-radius: 14px; padding: 12px 14px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.72rem; font-weight: 800; color: #1e293b;">
          <span>RECOUPMENT PROGRESS</span>
          <span style="color: #15803d;">$101,374 / $894,802</span>
        </div>
        <div style="width: 100%; height: 8px; background: #e2e8f0; border-radius: 999px; margin-top: 6px; overflow: hidden;">
          <div style="width: 11.3%; height: 100%; background: #22c55e; border-radius: 999px;"></div>
        </div>
        <span style="font-size: 0.65rem; color: #64748b; font-weight: 600; display: block; margin-top: 4px;">
          Unrecouped Balance: $793,428. Upon reaching $0, your streaming royalty jumps from 35% to 45%!
        </span>
      </div>

      <!-- Released Music Items -->
      ${GREATER_RECORDS_MUSIC.map(m => `
        <div class="subdrawer-music-item">
          <div style="display: flex; align-items: center; gap: 10px;">
            <img src="${m.cover}" style="width: 44px; height: 44px; border-radius: 8px; object-fit: cover;" alt="${m.title}">
            <div class="subdrawer-music-info">
              <h4>${m.title}</h4>
              <span>${m.type} &bull; ${m.tracksCount} Tracks &bull; ${m.year}</span>
            </div>
          </div>
          <div class="subdrawer-music-stat">
            <span class="streams">${Number(m.streams).toLocaleString()} streams</span>
            <span class="recouped">+$${Number(m.recoupedAmount).toLocaleString()} recouped</span>
          </div>
        </div>
      `).join("")}

      <div style="padding: 10px; background: #eff6ff; border: 1px dashed #93c5fd; border-radius: 12px; font-size: 0.7rem; color: #1e40af;">
        <strong>Upcoming Delivery Requirement:</strong> 2 more albums required to fulfill Greater Records contractual commitment.
      </div>
    `;
  }
  else if (drawerType === "roster") {
    iconEl.innerHTML = getLabelRosterIconSVG();
    titleEl.textContent = "GREATER RECORDS ARTIST ROSTER";
    contentEl.innerHTML = `
      <div style="font-size: 0.72rem; color: #64748b; font-weight: 600; margin-bottom: 4px;">
        Artists signed to Greater Records. High chemistry unlocks direct studio collaborations and package tours.
      </div>

      ${GREATER_RECORDS_ROSTER.map(art => `
        <div class="subdrawer-roster-item">
          <div class="roster-left">
            <img src="${art.avatar}" class="roster-avatar" alt="${art.name}">
            <div class="roster-info">
              <h4>${art.name}</h4>
              <span>${art.tier} &bull; ${art.monthlyListeners} Listeners</span>
            </div>
          </div>
          ${art.id !== 'roster-synapse' ? `
            <button class="roster-action-btn" onclick="showToast('FEATURE REQUEST SENT TO ${art.name.toUpperCase()}')">
              REQUEST FEATURE
            </button>
          ` : `
            <span style="font-size: 0.68rem; font-weight: 900; color: #2563eb; background: #dbeafe; padding: 4px 8px; border-radius: 6px;">YOU</span>
          `}
        </div>
      `).join("")}
    `;
  }
  else if (drawerType === "calendar") {
    iconEl.innerHTML = getLabelCalendarIconSVG();
    titleEl.textContent = "LABEL 4-WEEK RELEASE CALENDAR";
    contentEl.innerHTML = `
      <div style="font-size: 0.72rem; color: #64748b; font-weight: 600; margin-bottom: 4px;">
        Scheduled priority releases from Greater Records over the next month.
      </div>

      ${GREATER_RECORDS_CALENDAR.map(cal => `
        <div class="subdrawer-calendar-week">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="cal-week-badge">${cal.week} &bull; ${cal.dateRange}</span>
            <span style="font-size: 0.68rem; font-weight: 800; color: #15803d;">${cal.status}</span>
          </div>
          <h4 class="cal-release-title">${cal.releaseTitle}</h4>
          <p class="cal-release-artist">${cal.artist} &bull; Format: ${cal.format}</p>
          <div style="font-size: 0.68rem; color: #475569; background: #f1f5f9; padding: 4px 8px; border-radius: 6px;">
            <strong>Promo Focus:</strong> ${cal.promoPush}
          </div>
        </div>
      `).join("")}

      <div style="padding: 10px; background: #fffbeb; border: 1px dashed #fcd34d; border-radius: 12px; font-size: 0.7rem; color: #92400e;">
        <strong>Label Strategy Tip:</strong> Coordinate your album drops to avoid clashing with A$AP Ghost's rollout in Week 2.
      </div>
    `;
  }
  else if (drawerType === "staff") {
    iconEl.innerHTML = getLabelStaffIconSVG();
    titleEl.textContent = "GREATER RECORDS KEY STAFF";
    contentEl.innerHTML = `
      <div style="font-size: 0.72rem; color: #64748b; font-weight: 600; margin-bottom: 4px;">
        Network and converse with key personnel. Strong relationships unlock marketing boosts, feature clearances, and CEO leverage!
      </div>

      ${GREATER_RECORDS_STAFF.map(st => {
        const currentRel = staffRelationships[st.id] || st.relationship;
        return `
        <div class="subdrawer-staff-card" id="staffCard_${st.id}">
          <div class="staff-card-top">
            <div class="staff-avatar-box">${st.avatarLetter}</div>
            <div class="staff-info-box" style="flex: 1;">
              <h4>${st.name}</h4>
              <span class="role">${st.role}</span>
              <div class="staff-rel-meter-row">
                <span>Relationship</span>
                <span id="staffRelScore_${st.id}">${currentRel}/100</span>
              </div>
              <div class="staff-rel-bar">
                <div class="staff-rel-bar-fill" id="staffRelBar_${st.id}" style="width: ${currentRel}%;"></div>
              </div>
            </div>
          </div>

          <div class="staff-quote">
            "${st.quote}"
          </div>

          <div style="font-size: 0.67rem; color: #0284c7; font-weight: 600;">
            ${st.reputationBenefit}
          </div>

          <div class="staff-actions-row">
            <button class="staff-action-btn staff-btn-chat" onclick="interactWithStaff('${st.id}', 'chat')">
              NETWORK CONVERSATION (+4)
            </button>
            <button class="staff-action-btn staff-btn-gift" onclick="interactWithStaff('${st.id}', 'gift')">
              SEND GIFT (-$5,000, +10)
            </button>
          </div>
        </div>
      `;}).join("")}
    `;
  }
  else if (drawerType === "requests") {
    iconEl.innerHTML = getLabelRequestsIconSVG();
    titleEl.textContent = "OFFICIAL LABEL PETITIONS & REQUESTS";
    contentEl.innerHTML = `
      <div style="font-size: 0.72rem; color: #64748b; font-weight: 600; margin-bottom: 4px;">
        Submit formal contract petitions to Greater Records executives.
      </div>

      <!-- 1. Request Contract Buy-Out -->
      <div class="subdrawer-request-card">
        <h4>REQUEST CONTRACT BUY-OUT</h4>
        <p>Pay off the remaining 56 weeks and 2 project commitments in full to terminate your deal immediately and become 100% independent.</p>
        <div class="request-card-foot">
          <span class="request-cost-badge">COST: $1,200,000</span>
          <button class="request-submit-btn" onclick="submitLabelRequest('buyout')">SUBMIT BUY-OUT</button>
        </div>
      </div>

      <!-- 2. Request Contract Extension -->
      <div class="subdrawer-request-card">
        <h4>REQUEST CONTRACT EXTENSION</h4>
        <p>Extend your contract by +2 Years (+2 Albums) in exchange for an instant upfront $2,500,000 cash advance bonus.</p>
        <div class="request-card-foot">
          <span style="font-size: 0.74rem; font-weight: 900; color: #15803d;">BONUS: +$2,500,000</span>
          <button class="request-submit-btn" style="background: #2563eb;" onclick="submitLabelRequest('extension')">SUBMIT EXTENSION</button>
        </div>
      </div>

      <!-- 3. Request Early Release -->
      <div class="subdrawer-request-card">
        <h4>REQUEST EARLY RELEASE</h4>
        <p>Petition CEO Marcus Vance for a mutual contract release with zero financial penalty. Requires at least 80/100 Relationship with Marcus Vance.</p>
        <div class="request-card-foot">
          <span style="font-size: 0.72rem; font-weight: 800; color: #64748b;">REQ: 80 RELATIONSHIP</span>
          <button class="request-submit-btn" style="background: #e11d48;" onclick="submitLabelRequest('early_release')">SUBMIT PETITION</button>
        </div>
      </div>

      <!-- 4. Request Emergency Video Advance -->
      <div class="subdrawer-request-card">
        <h4>EMERGENCY MUSIC VIDEO ADVANCE</h4>
        <p>Request an immediate $250,000 video production grant added to your recoupment ledger for your next single rollout.</p>
        <div class="request-card-foot">
          <span class="request-cost-badge" style="color: #2563eb; background: #dbeafe;">FUNDS: +$250,000 CASH</span>
          <button class="request-submit-btn" style="background: #0284c7;" onclick="submitLabelRequest('video_advance')">REQUEST FUNDS</button>
        </div>
      </div>

      <!-- 5. Request Royalty Hike to 45% -->
      <div class="subdrawer-request-card">
        <h4>ROYALTY HIKE RENEGOTIATION</h4>
        <p>Petition the board to permanently increase your artist streaming split from 35% to 45% based on 70M+ total streaming volume.</p>
        <div class="request-card-foot">
          <span style="font-size: 0.72rem; font-weight: 800; color: #15803d;">NEW SPLIT: 45% ARTIST</span>
          <button class="request-submit-btn" style="background: #16a34a;" onclick="submitLabelRequest('royalty_hike')">PETITION BOARD</button>
        </div>
      </div>
    `;
  }

  drawer.style.display = "flex";
}

function closeYourLabelSubdrawer(e) {
  if (e && e.target && e.target.id !== "yourLabelSubDrawer" && !e.target.classList.contains("subdrawer-close-btn")) {
    return;
  }
  playMechanicalClick();
  const drawer = document.getElementById("yourLabelSubDrawer");
  if (drawer) drawer.style.display = "none";
}

// 5. Contract History Modal
function openLabelHistoryModal() {
  playMechanicalClick();
  const modal = document.getElementById("labelHistoryModal");
  const content = document.getElementById("labelHistoryContent");
  if (!modal || !content) return;

  content.innerHTML = `
    <div style="font-size: 0.72rem; color: #64748b; font-weight: 600; margin-bottom: 6px;">
      Chronological record of all recording agreements and label affiliations.
    </div>

    <!-- Active Deal -->
    <div class="history-contract-entry active">
      <span class="history-active-tag">CURRENTLY ACTIVE</span>
      <h4 style="margin: 0; font-size: 0.88rem; font-weight: 900; color: #0f172a;">GREATER RECORDS</h4>
      <span style="font-size: 0.7rem; color: #64748b; font-weight: 700;">Year 2 – Present &bull; 4 Projects &bull; $1,800,000 Advance</span>
      <p style="margin: 4px 0 0 0; font-size: 0.72rem; color: #334155;">
        Signed 4-year exclusive artist agreement. 2 of 4 album commitments delivered. 56 weeks remaining.
      </p>
    </div>

    <!-- Era 1: Independent -->
    <div class="history-contract-entry">
      <h4 style="margin: 0; font-size: 0.88rem; font-weight: 900; color: #0f172a;">INDEPENDENT ARTIST (SELF-RELEASED)</h4>
      <span style="font-size: 0.7rem; color: #64748b; font-weight: 700;">Year 1 – Year 2 &bull; 100% Masters Ownership</span>
      <p style="margin: 4px 0 0 0; font-size: 0.72rem; color: #334155;">
        Self-funded early mixtapes and singles. 100% artist royalty and master ownership prior to major label signing.
      </p>
    </div>

    <div style="padding: 10px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 12px; font-size: 0.68rem; color: #64748b; text-align: center;">
      ARCHIVAL REGISTRY &bull; OFFICIAL CONTRACT RECORDS AUTHENTICATED
    </div>
  `;

  modal.style.display = "flex";
}

function closeLabelHistoryModal(e) {
  if (e && e.target && e.target.id !== "labelHistoryModal" && !e.target.classList.contains("subdrawer-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("labelHistoryModal");
  if (modal) modal.style.display = "none";
}

// 6. Interactive Staff & Request Handlers
function interactWithStaff(staffId, actionType) {
  playMechanicalClick();
  const staff = GREATER_RECORDS_STAFF.find(s => s.id === staffId);
  if (!staff) return;

  if (actionType === "chat") {
    staffRelationships[staffId] = Math.min(100, (staffRelationships[staffId] || staff.relationship) + 4);
    const scoreEl = document.getElementById(`staffRelScore_${staffId}`);
    const barEl = document.getElementById(`staffRelBar_${staffId}`);
    if (scoreEl) scoreEl.textContent = `${staffRelationships[staffId]}/100`;
    if (barEl) barEl.style.width = `${staffRelationships[staffId]}%`;

    showToast(`CONVERSATION HELD: ${staff.name.toUpperCase()} RELATIONSHIP +4`);
  } else if (actionType === "gift") {
    staffRelationships[staffId] = Math.min(100, (staffRelationships[staffId] || staff.relationship) + 10);
    const scoreEl = document.getElementById(`staffRelScore_${staffId}`);
    const barEl = document.getElementById(`staffRelBar_${staffId}`);
    if (scoreEl) scoreEl.textContent = `${staffRelationships[staffId]}/100`;
    if (barEl) barEl.style.width = `${staffRelationships[staffId]}%`;

    showToast(`SENT LUXURY GIFT (-$5,000): ${staff.name.toUpperCase()} RELATIONSHIP +10`);
  }
}

function submitLabelRequest(reqType) {
  playMechanicalClick();
  if (reqType === "buyout") {
    showToast("BUY-OUT PROPOSAL SUBMITTED TO GREATER RECORDS BOARD ($1,200,000)");
  } else if (reqType === "extension") {
    greaterRecordsState.weeksLeft += 104;
    greaterRecordsState.commitmentTotal += 2;
    showToast("CONTRACT EXTENSION SIGNED: +2 YEARS / +$2,500,000 ADVANCE GRANTED");
    renderYourLabelContract();
  } else if (reqType === "early_release") {
    const vanceRel = staffRelationships.vance || 68;
    if (vanceRel >= 80) {
      showToast("EARLY RELEASE PETITION APPROVED BY MARCUS VANCE!");
    } else {
      showToast(`PETITION DENIED: MARCUS VANCE REQUIRES 80+ RELATIONSHIP (CURRENT: ${vanceRel}/100)`);
    }
  } else if (reqType === "video_advance") {
    greaterRecordsState.recoupmentRemaining += 250000;
    showToast("EMERGENCY VIDEO ADVANCE APPROVED: +$250,000 ADDED TO RECOUPMENT");
    renderYourLabelContract();
  } else if (reqType === "royalty_hike") {
    showToast("ROYALTY HIKE PROPOSAL ACCEPTED: STREAMING SPLIT SET TO 45%");
  }
}

function signLabelDeal(labelId) {
  playMechanicalClick();
  const label = LABELS_DATA.find(l => l.id === labelId);
  if (!label) return;

  if (label.id === currentSignedLabelId) {
    showToast("ALREADY SIGNED TO THIS LABEL");
    return;
  }

  showToast(`CANNOT SIGN ${label.name}: CURRENTLY BOUND TO GREATER RECORDS (REQUEST BUYOUT FIRST)`);
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
  } else if (hash === "calendar") {
    switchTab("social");
    openCalendarApp();
  } else if (hash === "beatstore") {
    switchTab("social");
    openBeatstoreApp();
  } else if (["news", "concerts", "messenger", "tumble", "beef", "livee"].includes(hash)) {
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


// ==========================================================================
// PROFILE SUBPAGE: MEDIA MANAGEMENT ENGINE (BLACK CONTRACT PAPER SYSTEM)
// ==========================================================================

const MANAGEMENT_DATA = [
  {
    id: "mgmt-amplify",
    name: "Amplify Collective",
    tier: "Boutique PR & Digital Agency",
    territory: "Digital & Grassroots",
    yearlyCost: 12000,
    yearlyCostDisplay: "$12,000.00 / YR",
    weeklyPopularity: "+8-13%",
    prestige: 52,
    minPopularity: 15,
    description: "A nimble independent boutique firm specializing in underground hype, grassroots playlist pitching, and early-stage social media resonance.",
    clauses: [
      "Press Outreach: 15 independent blog placements per month",
      "Digital Playlisting: Weekly pitching to verified curator ecosystems",
      "Social Hype: Organic sound seeding across TikTok & Reels",
      "Crisis Response: Standard 48-hour email guidance"
    ],
    plans: {
      month: { weeks: 4, cost: 1000, display: "$1,000.00 / MO" },
      six_month: { weeks: 26, cost: 6000, display: "$6,000.00 / 6-MO" },
      year: { weeks: 52, cost: 12000, display: "$12,000.00 / YR" }
    }
  },
  {
    id: "mgmt-narrative",
    name: "The Narrative Arc",
    tier: "Mid-Tier Specialist PR & Brand Strategy",
    territory: "National Media & Tastemakers",
    yearlyCost: 35000,
    yearlyCostDisplay: "$35,000.00 / YR",
    weeklyPopularity: "+13-18%",
    prestige: 70,
    minPopularity: 35,
    description: "Strategic narrative architects curating high-impact profiles, digital magazine covers, and tastemaker podcast appearances.",
    clauses: [
      "Editorial Features: Pitching to FADER, Complex, and XXL",
      "Radio Campaigning: Regional urban & college radio tastemaker runs",
      "Brand Positioning: High-fashion lookbook & red carpet consulting",
      "Dedicated Publicist: Direct 24/7 hotline with senior representative"
    ],
    plans: {
      month: { weeks: 4, cost: 2950, display: "$2,950.00 / MO" },
      six_month: { weeks: 26, cost: 17500, display: "$17,500.00 / 6-MO" },
      year: { weeks: 52, cost: 35000, display: "$35,000.00 / YR" }
    }
  },
  {
    id: "mgmt-momentum",
    name: "Momentum Media",
    tier: "Major Independent Powerhouse",
    territory: "US National & Digital Broadcast",
    yearlyCost: 90000,
    yearlyCostDisplay: "$90,000.00 / YR",
    weeklyPopularity: "+22-30%",
    prestige: 82,
    minPopularity: 55,
    description: "High-octane talent agency with direct lines to morning show syndicates, viral TikTok campaign directors, and festival talent buyers.",
    clauses: [
      "Tier-1 Broadcast: Guaranteed Breakfast Club / Hot 97 interviews",
      "Viral Acceleration: Multi-influencer audio syndication networks",
      "DSP Spotlight: Top-tier editorial playlist priority pitching",
      "Legal Defense: Full crisis suppression & swift DMCA strikes"
    ],
    plans: {
      month: { weeks: 4, cost: 7500, display: "$7,500.00 / MO" },
      six_month: { weeks: 26, cost: 45000, display: "$45,000.00 / 6-MO" },
      year: { weeks: 52, cost: 90000, display: "$90,000.00 / YR" }
    }
  },
  {
    id: "mgmt-catalyst",
    name: "Catalyst Comms",
    tier: "Global Elite Public Relations",
    territory: "Global Multi-Platform",
    yearlyCost: 220000,
    yearlyCostDisplay: "$220,000.00 / YR",
    weeklyPopularity: "+34-42%",
    prestige: 92,
    minPopularity: 72,
    description: "Premier communications firm steering international arena rollouts, late-night television bookings, and Fortune 500 endorsement negotiations.",
    clauses: [
      "Global TV Circuits: Fallon, Kimmel, and BBC Live Lounge bookings",
      "Magazine Covers: Rolling Stone, GQ, and Billboard cover features",
      "Corporate Endorsements: Luxury brand sponsorships & campaigns",
      "VIP Crisis Room: Rapid 15-minute emergency narrative control"
    ],
    plans: {
      month: { weeks: 4, cost: 18500, display: "$18,500.00 / MO" },
      six_month: { weeks: 26, cost: 110000, display: "$110,000.00 / 6-MO" },
      year: { weeks: 52, cost: 220000, display: "$220,000.00 / YR" }
    }
  },
  {
    id: "mgmt-verve",
    name: "Verve Public Relations",
    tier: "Worldwide Sovereign Agency & Legacy Firm",
    territory: "Worldwide Sovereign Tier",
    yearlyCost: 550000,
    yearlyCostDisplay: "$550,000.00 / YR",
    weeklyPopularity: "+46-56%",
    prestige: 99,
    minPopularity: 85,
    description: "The apex titan of global entertainment representation. Reserved for charting icons, stadium headliners, and cultural powerhouses.",
    clauses: [
      "Stadium & Festival Priority: Direct Coachella / Glastonbury curations",
      "Grammy & Met Gala Campaigning: Academy voting influence & red carpet priority",
      "Worldwide Syndication: Global multi-territory media blockouts",
      "Bespoke Chief of Staff: Round-the-clock dedicated 5-person executive retainer"
    ],
    plans: {
      month: { weeks: 4, cost: 46000, display: "$46,000.00 / MO" },
      six_month: { weeks: 26, cost: 275000, display: "$275,000.00 / 6-MO" },
      year: { weeks: 52, cost: 550000, display: "$550,000.00 / YR" }
    }
  }
];

// Active State for Media Management
let currentMgmtSection = "all";
let currentSignedMgmtId = "mgmt-narrative";

let yourManagementState = {
  agencyId: "mgmt-narrative",
  agencyName: "The Narrative Arc",
  prestige: 70,
  planType: "year",
  planValueDisplay: "$35,000.00 / YEAR",
  planCost: 35000,
  totalWeeks: 52,
  weeksRemaining: 28,
  weeklyPopularity: "+13-18%"
};

let mgmtStaffRelationships = {
  "mgmt-st-elena": 72,
  "mgmt-st-darius": 65,
  "mgmt-st-chloe": 80,
  "mgmt-st-julian": 58
};

const MANAGEMENT_STAFF_DATA = [
  {
    id: "mgmt-st-elena",
    name: "Elena Rostova",
    role: "PR Director & Chief Strategist",
    avatarLetter: "E",
    quote: "We've locked in two major editorial features for next week. Keep giving me undeniable music.",
    reputationBenefit: "Benefit: +15% Pitch Approval on High-Tier Digital Magazines"
  },
  {
    id: "mgmt-st-darius",
    name: "Darius Cole",
    role: "Senior Publicist & Radio Liaison",
    avatarLetter: "D",
    quote: "Power 105.1 and Shade 45 are spinning your record. Let's push for the evening prime-time slot.",
    reputationBenefit: "Benefit: Radio Airplay Spin Multiplier (+25% Weekly Audience Reach)"
  },
  {
    id: "mgmt-st-chloe",
    name: "Chloe Vance",
    role: "Crisis PR & Reputation Handler",
    avatarLetter: "C",
    quote: "The internet never forgets, but with surgical framing, we turn controversies into brand momentum.",
    reputationBenefit: "Benefit: 100% Protection from Viral Scandal & Social Cancellation"
  },
  {
    id: "mgmt-st-julian",
    name: "Julian Cruz",
    role: "DSP & Playlist PR Lead",
    avatarLetter: "J",
    quote: "Top 50 Rap editorial rotation is within reach if we sustain this digital streaming surge.",
    reputationBenefit: "Benefit: Direct Playlist Pitching Priority on Shawtify & Apple Music"
  }
];

// SVG Helpers for Management (Silver/Chrome Aesthetics)
function getSilverAgencySealSVG(size = 44) {
  return `
    <svg width="${size}" height="${size}" viewBox="0 0 60 60" fill="none" class="mgmt-silver-seal-svg">
      <defs>
        <radialGradient id="silverGrad_${size}" cx="38%" cy="32%" r="65%">
          <stop offset="0%" stop-color="#ffffff"/>
          <stop offset="35%" stop-color="#cbd5e1"/>
          <stop offset="70%" stop-color="#64748b"/>
          <stop offset="100%" stop-color="#334155"/>
        </radialGradient>
        <radialGradient id="silverBed_${size}" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#475569"/>
          <stop offset="60%" stop-color="#1e293b"/>
          <stop offset="100%" stop-color="#0f172a"/>
        </radialGradient>
        <filter id="silverShadow_${size}" x="-10%" y="-10%" width="125%" height="125%">
          <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000000" flood-opacity="0.8"/>
        </filter>
      </defs>
      <!-- Outer scalloped silver seal edge -->
      <path d="M30 3 C36 2, 40 5, 45 7 C50 9, 54 13, 56 18 C58 23, 57 27, 58 32 C59 37, 57 42, 54 47 C51 52, 46 54, 41 57 C36 60, 31 58, 28 58 C24 58, 19 59, 15 57 C10 55, 6 51, 4 46 C2 41, 1 36, 2 31 C3 26, 1 21, 4 16 C7 11, 12 7, 17 6 C22 5, 25 3, 30 3 Z" fill="url(#silverGrad_${size})" filter="url(#silverShadow_${size})"/>
      <!-- Silver rim highlights -->
      <path d="M22 6 C30 4, 42 6, 48 12 C52 16, 54 22, 54 28" stroke="#ffffff" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.7"/>
      <circle cx="30" cy="30" r="18.5" fill="none" stroke="#334155" stroke-width="1.4" stroke-dasharray="3 2"/>
      <circle cx="30" cy="30" r="14.5" fill="url(#silverBed_${size})"/>
      <!-- Embossed megaphone & star emblem -->
      <polygon points="30,19 32.5,25 39,25.5 34,29.5 35.5,36 30,32.5 24.5,36 26,29.5 21,25.5 27.5,25" fill="#f8fafc" stroke="#94a3b8" stroke-width="0.8"/>
      <!-- Specular gloss glint -->
      <ellipse cx="23" cy="20" rx="4" ry="2" transform="rotate(-30 23 20)" fill="#ffffff" opacity="0.45"/>
    </svg>
  `;
}

function getSilverFountainPenSigSVG() {
  return `
    <svg width="44" height="34" viewBox="0 0 52 40" fill="none">
      <path d="M4 35 Q 16 26, 26 34 T 44 31" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" fill="none"/>
      <path d="M12 33 Q 18 20, 24 32" stroke="#d97706" stroke-width="1.6" stroke-linecap="round" fill="none"/>
      <path d="M26 31 Q 32 18, 38 29" stroke="#fef08a" stroke-width="1.4" stroke-linecap="round" fill="none"/>
      <g transform="translate(24, 2) rotate(42)">
        <path d="M0 0 L7 0 L7 17 L3.5 25 L0 17 Z" fill="#334155"/>
        <path d="M1.2 17 L5.8 17 L3.5 25 Z" fill="#fbbf24" stroke="#d97706" stroke-width="0.5"/>
        <line x1="3.5" y1="17" x2="3.5" y2="23" stroke="#78350f" stroke-width="0.6"/>
        <rect x="0" y="0" width="7" height="4" fill="#cbd5e1"/>
        <line x1="2" y1="4" x2="2" y2="15" stroke="#475569" stroke-width="1"/>
      </g>
    </svg>
  `;
}

function getSilverContractDocSVG() {
  return `
    <svg width="30" height="34" viewBox="0 0 34 38" fill="none">
      <path d="M4 3 L22 3 L29 10 L29 35 A 2 2 0 0 1 27 37 L4 37 A 2 2 0 0 1 2 35 L2 5 A 2 2 0 0 1 4 3 Z" fill="#1e293b" stroke="#94a3b8" stroke-width="2"/>
      <path d="M22 3 L22 10 L29 10 Z" fill="#475569" stroke="#94a3b8" stroke-width="1.6"/>
      <line x1="6" y1="13" x2="19" y2="13" stroke="#cbd5e1" stroke-width="1.6"/>
      <line x1="6" y1="18" x2="25" y2="18" stroke="#cbd5e1" stroke-width="1.6"/>
      <line x1="6" y1="23" x2="18" y2="23" stroke="#cbd5e1" stroke-width="1.6"/>
      <circle cx="21" cy="27" r="5.5" fill="#0f172a" stroke="#fbbf24" stroke-width="2"/>
      <line x1="25.5" y1="31.5" x2="31" y2="37" stroke="#fbbf24" stroke-width="2.6" stroke-linecap="round"/>
      <circle cx="21" cy="27" r="3" fill="#fbbf24" opacity="0.4"/>
    </svg>
  `;
}

function getMgmtStaffIconSVG() {
  return `
    <svg width="28" height="28" viewBox="0 0 36 34" fill="none">
      <circle cx="18" cy="11" r="5" stroke="#fbbf24" stroke-width="2" fill="none"/>
      <path d="M9 27 C9 20, 27 20, 27 27" stroke="#fbbf24" stroke-width="2" fill="none"/>
      <circle cx="8.5" cy="13" r="3.8" stroke="#d97706" stroke-width="1.8" fill="none"/>
      <path d="M2 28 C2 23, 13 23, 13 28" stroke="#d97706" stroke-width="1.8" fill="none"/>
      <circle cx="27.5" cy="13" r="3.8" stroke="#d97706" stroke-width="1.8" fill="none"/>
      <path d="M23 28 C23 23, 34 23, 34 28" stroke="#d97706" stroke-width="1.8" fill="none"/>
    </svg>
  `;
}

function getMgmtRequestsIconSVG() {
  return `
    <svg width="28" height="28" viewBox="0 0 36 34" fill="none">
      <path d="M6 14 L18 8 L30 14 L18 20 Z" stroke="#fbbf24" stroke-width="2" fill="rgba(251, 191, 36, 0.18)"/>
      <path d="M6 20 L18 26 L30 20" stroke="#d97706" stroke-width="2" fill="none"/>
      <path d="M12 23 L18 26 L24 23" stroke="#fef08a" stroke-width="1.8" fill="none"/>
    </svg>
  `;
}

function getMgmtHistoryIconSVG() {
  return `
    <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
      <circle cx="16" cy="16" r="12" stroke="#94a3b8" stroke-width="2.4"/>
      <polyline points="16,10 16,16 21,16" stroke="#f1f5f9" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M9 9 L4 13 L10 14" stroke="#fbbf24" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `;
}

// Media Management Subpage Open & Close
function openProfileManagementSubpage(initialSection = "all") {
  playMechanicalClick();
  const hub = document.getElementById("profileMainHub");
  const subpage = document.getElementById("profileSubpageManagement");
  if (!subpage) return;

  if (hub) hub.style.display = "none";
  subpage.style.display = "flex";
  subpage.scrollTop = 0;

  switchManagementSection(initialSection);
}

function closeProfileManagementSubpage() {
  playMechanicalClick();
  const hub = document.getElementById("profileMainHub");
  const subpage = document.getElementById("profileSubpageManagement");
  if (subpage) subpage.style.display = "none";
  if (hub) hub.style.display = "flex";
}

function switchManagementSection(section) {
  playMechanicalClick();
  currentMgmtSection = section;

  const btnAll = document.getElementById("tabBtnMgmtAll");
  const btnYour = document.getElementById("tabBtnMgmtYour");
  const secAll = document.getElementById("mgmtSectionAll");
  const secYour = document.getElementById("mgmtSectionYour");

  if (section === "all") {
    if (btnAll) btnAll.classList.add("active");
    if (btnYour) btnYour.classList.remove("active");
    if (secAll) secAll.style.display = "flex";
    if (secYour) secYour.style.display = "none";
    renderAllManagementContracts();
  } else {
    if (btnAll) btnAll.classList.remove("active");
    if (btnYour) btnYour.classList.add("active");
    if (secAll) secAll.style.display = "none";
    if (secYour) secYour.style.display = "flex";
    renderYourManagementContract();
  }
}

// 1. Render ALL MANAGEMENT (The 5 Black Contract Pages)
// (Removed min popularity and prestige data fields as requested)
function renderAllManagementContracts() {
  const container = document.getElementById("mgmtSectionAll");
  if (!container) return;

  container.innerHTML = MANAGEMENT_DATA.map(agency => `
    <div class="mgmt-contract-card" onclick="openManagementContractModal('${agency.id}')">
      <!-- Silver Agency Seal Stamp -->
      <div class="mgmt-silver-seal">
        ${getSilverAgencySealSVG(44)}
      </div>

      <!-- Agency Title -->
      <h2 class="mgmt-contract-title">${agency.name}</h2>

      <!-- Contract Conditions Grid with left-aligned values -->
      <div class="mgmt-contract-meta-grid">
        <div class="mgmt-meta-row">
          <span class="mgmt-meta-key">YEARLY RETAINER :</span>
          <span class="mgmt-meta-val">${agency.yearlyCostDisplay}</span>
        </div>
        <div class="mgmt-meta-row">
          <span class="mgmt-meta-key">WEEKLY POPULARITY :</span>
          <span class="mgmt-meta-val" style="color: #fbbf24; font-weight: 900;">${agency.weeklyPopularity}</span>
        </div>
        <div class="mgmt-meta-row">
          <span class="mgmt-meta-key">TERMS AVAILABLE :</span>
          <span class="mgmt-meta-val">MONTH / 6-MONTH / YEAR</span>
        </div>
      </div>

      <!-- Bottom Row: Retainer Cost Pill (Green Box) + Gold Pen Signature -->
      <div class="mgmt-contract-bottom-row">
        <div class="mgmt-advance-group">
          <span class="mgmt-advance-label">PLAN :</span>
          <div class="mgmt-cost-pill">${agency.yearlyCostDisplay}</div>
        </div>
        <div class="mgmt-silver-signature">
          ${getSilverFountainPenSigSVG()}
        </div>
      </div>
    </div>
  `).join("");
}

// 2. Render YOUR MANAGEMENT (Active Black Contract Card)
// (Removed prestige data field as requested)
function renderYourManagementContract() {
  const container = document.getElementById("mgmtSectionYour");
  if (!container) return;

  const agency = MANAGEMENT_DATA.find(a => a.id === yourManagementState.agencyId) || MANAGEMENT_DATA[1];

  container.innerHTML = `
    <div class="your-mgmt-black-card">
      <!-- Top Right Seals & Inspection Button -->
      <div class="your-mgmt-top-seals">
        <div class="mgmt-silver-seal">
          ${getSilverAgencySealSVG(44)}
        </div>
        <button class="your-mgmt-contract-doc-btn" onclick="openManagementContractModal('${agency.id}')" title="Inspect Complete Retainer Agreement">
          ${getSilverContractDocSVG()}
        </button>
      </div>

      <!-- Agency Title -->
      <h1 class="your-mgmt-title">${agency.name}</h1>

      <!-- Stats Cluster -->
      <div class="your-mgmt-stats-box">
        <!-- Prominent Current Plan Value Pill in Green Box -->
        <div class="your-mgmt-plan-pill">
          CURRENT PLAN : ${yourManagementState.planValueDisplay}
        </div>
        <div class="your-mgmt-meta-item">
          <span>ACTIVE TERM : ${yourManagementState.totalWeeks === 52 ? '1 YEAR CONTRACT' : (yourManagementState.totalWeeks === 26 ? '6 MONTH CONTRACT' : '1 MONTH CONTRACT')}</span>
        </div>
        <div class="your-mgmt-meta-item">
          <span>WEEKS REMAINING : ${yourManagementState.weeksRemaining}/${yourManagementState.totalWeeks} WEEKS</span>
        </div>
        <div class="your-mgmt-meta-item">
          <span>WEEKLY POPULARITY :</span>
          <span style="color: #fbbf24; font-weight: 900;">${yourManagementState.weeklyPopularity}</span>
        </div>
      </div>

      <!-- Exactly 2 Action Buttons: MANAGEMENT STAFF and REQUESTS -->
      <div class="your-mgmt-action-buttons">
        <button class="your-mgmt-action-btn" onclick="openYourManagementSubdrawer('staff')">
          <div class="your-mgmt-btn-icon">${getMgmtStaffIconSVG()}</div>
          <span class="your-mgmt-btn-label">MANAGEMENT STAFF</span>
        </button>

        <button class="your-mgmt-action-btn" onclick="openYourManagementSubdrawer('requests')">
          <div class="your-mgmt-btn-icon">${getMgmtRequestsIconSVG()}</div>
          <span class="your-mgmt-btn-label">REQUESTS</span>
        </button>
      </div>

      <!-- History Button -->
      <div class="your-mgmt-history-wrap">
        <button class="your-mgmt-history-btn" onclick="openManagementHistoryModal()" title="Management Representation Archive">
          ${getMgmtHistoryIconSVG()}
        </button>
      </div>
    </div>
  `;
}

// 3. Complete Formal Black Contract Inspector Modal
function openManagementContractModal(agencyId) {
  playMechanicalClick();
  const agency = MANAGEMENT_DATA.find(a => a.id === agencyId) || MANAGEMENT_DATA[1];
  if (!agency) return;

  const modal = document.getElementById("mgmtContractModal");
  const sealRow = document.getElementById("mgmtContractModalSealRow");
  const bodyContent = document.getElementById("mgmtContractModalBodyContent");
  const footerActions = document.getElementById("mgmtContractModalFooterActions");
  if (!modal || !sealRow || !bodyContent || !footerActions) return;

  const isCurrent = agency.id === yourManagementState.agencyId;

  sealRow.innerHTML = `
    <div class="contract-modal-seal-badge">
      ${getSilverAgencySealSVG(48)}
    </div>
    <div class="contract-modal-title-block">
      <h2 style="color: #f8fafc;">${agency.name}</h2>
      <span style="color: #fbbf24; font-weight: 700;">${agency.tier} &bull; ${agency.territory}</span>
    </div>
  `;

  bodyContent.innerHTML = `
    <!-- Agency Summary -->
    <p style="margin: 0; font-size: 0.74rem; color: #94a3b8; font-style: italic;">
      ${agency.description}
    </p>

    <!-- Clause 1: Terms & Performance Acceleration -->
    <div class="contract-clause-box mgmt-clause-box">
      <div class="contract-clause-title mgmt-clause-title">
        <span>§ 1. REPRESENTATION & PERFORMANCE ACCELERATION</span>
      </div>
      <div class="contract-clause-grid">
        <div class="contract-clause-item">
          <span class="c-lbl">Weekly Popularity Boost</span>
          <span class="c-val" style="color: #fbbf24;">${agency.weeklyPopularity}</span>
        </div>
        <div class="contract-clause-item">
          <span class="c-lbl">Territory Scope</span>
          <span class="c-val">${agency.territory}</span>
        </div>
        <div class="contract-clause-item" style="grid-column: 1 / -1;">
          <span class="c-lbl">Agency Category</span>
          <span class="c-val">${agency.tier}</span>
        </div>
      </div>
    </div>

    <!-- Clause 2: Retainer Plans & Payment Options -->
    <div class="contract-clause-box mgmt-clause-box">
      <div class="contract-clause-title mgmt-clause-title">
        <span>§ 2. RETAINER OPTIONS (MONTH / 6-MONTH / 1-YEAR)</span>
      </div>
      <div class="contract-clause-grid">
        <div class="contract-clause-item">
          <span class="c-lbl">1-Month Retainer</span>
          <span class="c-val">${agency.plans.month.display} (4 Weeks)</span>
        </div>
        <div class="contract-clause-item">
          <span class="c-lbl">6-Month Retainer</span>
          <span class="c-val">${agency.plans.six_month.display} (26 Weeks)</span>
        </div>
        <div class="contract-clause-item" style="grid-column: 1 / -1;">
          <span class="c-lbl">1-Year Standard Retainer</span>
          <span class="c-val" style="color: #fbbf24; font-size: 0.85rem;">${agency.plans.year.display} (52 Weeks)</span>
        </div>
      </div>
    </div>

    <!-- Clause 3: Deliverables & Media Guarantees -->
    <div class="contract-clause-box mgmt-clause-box">
      <div class="contract-clause-title mgmt-clause-title">
        <span>§ 3. MANAGEMENT DELIVERABLES & MEDIA ACCESS</span>
      </div>
      <div class="contract-promise-list">
        ${agency.clauses.map(c => `
          <div class="contract-promise-row">
            <span class="bullet" style="color: #fbbf24;">✓</span>
            <span style="color: #cbd5e1;">${c}</span>
          </div>
        `).join("")}
      </div>
    </div>
  `;

  if (isCurrent) {
    footerActions.innerHTML = `
      <button class="contract-btn-sign" style="background: #b45309; border-color: #d97706; color: #ffffff;" onclick="showToast('THIS IS YOUR CURRENTLY ACTIVE MANAGEMENT AGENCY')">
        ACTIVE AGENCY (RETAINED)
      </button>
      <button class="contract-btn-close" onclick="closeManagementContractModal()">CLOSE</button>
    `;
  } else {
    footerActions.innerHTML = `
      <button class="contract-btn-sign" style="background: #15803d; border-color: #16a34a;" onclick="signManagementDeal('${agency.id}', 'year')">
        RETAIN AGENCY (${agency.plans.year.display})
      </button>
      <button class="contract-btn-close" onclick="closeManagementContractModal()">CLOSE</button>
    `;
  }

  modal.style.display = "flex";
}

function closeManagementContractModal(e) {
  if (e && e.target && e.target.id !== "mgmtContractModal" && !e.target.classList.contains("contract-modal-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("mgmtContractModal");
  if (modal) modal.style.display = "none";
}

function signManagementDeal(agencyId, planKey = "year") {
  playMechanicalClick();
  const agency = MANAGEMENT_DATA.find(a => a.id === agencyId);
  if (!agency) return;

  const plan = agency.plans[planKey] || agency.plans.year;

  currentSignedMgmtId = agency.id;
  yourManagementState = {
    agencyId: agency.id,
    agencyName: agency.name,
    prestige: agency.prestige,
    planType: planKey,
    planValueDisplay: plan.display,
    planCost: plan.cost,
    totalWeeks: plan.weeks,
    weeksRemaining: plan.weeks,
    weeklyPopularity: agency.weeklyPopularity
  };

  closeManagementContractModal();
  showToast(`RETAINED ${agency.name.toUpperCase()} (${plan.display})`);
  switchManagementSection("your");
}

// 4. Interactive Management Sub-Drawer (Staff & Requests)
function openYourManagementSubdrawer(drawerType) {
  playMechanicalClick();
  const drawer = document.getElementById("yourMgmtSubDrawer");
  const iconEl = document.getElementById("mgmtSubdrawerHeaderIcon");
  const titleEl = document.getElementById("mgmtSubdrawerHeaderTitle");
  const contentEl = document.getElementById("mgmtSubdrawerBodyContent");
  if (!drawer || !iconEl || !titleEl || !contentEl) return;

  const agency = MANAGEMENT_DATA.find(a => a.id === yourManagementState.agencyId) || MANAGEMENT_DATA[1];

  if (drawerType === "staff") {
    iconEl.innerHTML = getMgmtStaffIconSVG();
    titleEl.textContent = `${agency.name.toUpperCase()} PERSONNEL`;
    contentEl.innerHTML = `
      <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; margin-bottom: 4px;">
        Collaborate with your agency handlers. Deep relationships maximize broadcast bookings, radio rotation, and crisis immunity!
      </div>

      ${MANAGEMENT_STAFF_DATA.map(st => {
        const currentRel = mgmtStaffRelationships[st.id] || 70;
        return `
        <div class="subdrawer-staff-card" id="mgmtStaffCard_${st.id}">
          <div class="staff-card-top">
            <div class="staff-avatar-box">${st.avatarLetter}</div>
            <div class="staff-info-box" style="flex: 1;">
              <h4>${st.name}</h4>
              <span class="role">${st.role}</span>
              <div class="staff-rel-meter-row">
                <span>Relationship</span>
                <span id="mgmtStaffRelScore_${st.id}">${currentRel}/100</span>
              </div>
              <div class="staff-rel-bar">
                <div class="staff-rel-bar-fill" id="mgmtStaffRelBar_${st.id}" style="width: ${currentRel}%; background: linear-gradient(90deg, #d97706, #fbbf24);"></div>
              </div>
            </div>
          </div>

          <div class="staff-quote">
            "${st.quote}"
          </div>

          <div style="font-size: 0.67rem; color: #fbbf24; font-weight: 700;">
            ${st.reputationBenefit}
          </div>

          <div class="staff-actions-row">
            <button class="staff-action-btn" style="background: #1e293b; color: #f8fafc; border: 1px solid #475569;" onclick="interactWithMgmtStaff('${st.id}', 'chat')">
              STRATEGY CALL (+4)
            </button>
            <button class="staff-action-btn" style="background: #334155; color: #fbbf24; border: 1px solid #78350f;" onclick="interactWithMgmtStaff('${st.id}', 'gift')">
              SEND GIFT (-$3,500, +10)
            </button>
          </div>
        </div>
      `;}).join("")}
    `;
  }
  else if (drawerType === "requests") {
    iconEl.innerHTML = getMgmtRequestsIconSVG();
    titleEl.textContent = "MANAGEMENT PETITIONS & CAMPAIGNS";
    contentEl.innerHTML = `
      <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; margin-bottom: 4px;">
        Commission specialized agency initiatives to accelerate career momentum or defuse public crises.
      </div>

      <!-- 1. Viral Press Blitz -->
      <div class="subdrawer-request-card">
        <h4>VIRAL PRESS & DIGITAL BLITZ</h4>
        <p>Execute coordinated 72-hour media blitz across 35+ top hip-hop blogs and high-engagement social meme curators.</p>
        <div class="request-card-foot">
          <span class="request-cost-badge" style="color: #fbbf24; background: #451a03; border: 1px solid #78350f;">COST: $8,500</span>
          <button class="request-submit-btn" style="background: #d97706;" onclick="submitManagementRequest('blitz')">LAUNCH BLITZ</button>
        </div>
      </div>

      <!-- 2. Crisis PR Suppression -->
      <div class="subdrawer-request-card">
        <h4>CRISIS PR SUPPRESSION UNIT</h4>
        <p>Deploy emergency narrative handlers to scrub negative tabloids, issue legal DMCA cease-and-desists, and clear public slander.</p>
        <div class="request-card-foot">
          <span class="request-cost-badge" style="color: #f87171; background: #450a0a;">COST: $15,000</span>
          <button class="request-submit-btn" style="background: #dc2626;" onclick="submitManagementRequest('crisis')">DEPLOY SQUAD</button>
        </div>
      </div>

      <!-- 3. Tier-1 Interview Booking -->
      <div class="subdrawer-request-card">
        <h4>TIER-1 INTERVIEW BOOKING</h4>
        <p>Secure a 45-minute live morning show sit-down with The Breakfast Club, Hot 97, or Apple Music's Zane Lowe.</p>
        <div class="request-card-foot">
          <span class="request-cost-badge" style="color: #fef08a; background: #3b1d03; border: 1px solid #854d0e;">COST: $25,000</span>
          <button class="request-submit-btn" style="background: #b45309;" onclick="submitManagementRequest('interview')">BOOK INTERVIEW</button>
        </div>
      </div>

      <!-- 4. Retainer Plan Term Switch -->
      <div class="subdrawer-request-card">
        <h4>SWITCH RETAINER TERM</h4>
        <p>Renegotiate current billing cycle with ${agency.name}. Choose Month (4 Wks), 6-Months (26 Wks), or 1-Year (52 Wks).</p>
        <div class="request-card-foot">
          <span style="font-size: 0.72rem; font-weight: 800; color: #94a3b8;">FLEXIBLE BILLING</span>
          <button class="request-submit-btn" style="background: #b45309;" onclick="submitManagementRequest('switch_term')">SWITCH TERM</button>
        </div>
      </div>

      <!-- 5. Terminate Management Representation -->
      <div class="subdrawer-request-card">
        <h4>TERMINATE REPRESENTATION</h4>
        <p>Sever representation agreement immediately. Pay standard contract severance fee to release agency commitments and become self-managed.</p>
        <div class="request-card-foot">
          <span class="request-cost-badge" style="color: #f87171; background: #450a0a;">BUYOUT: $10,000</span>
          <button class="request-submit-btn" style="background: #991b1b;" onclick="submitManagementRequest('terminate')">TERMINATE DEAL</button>
        </div>
      </div>
    `;
  }

  drawer.style.display = "flex";
}

function closeYourManagementSubdrawer(e) {
  if (e && e.target && e.target.id !== "yourMgmtSubDrawer" && !e.target.classList.contains("subdrawer-close-btn")) {
    return;
  }
  playMechanicalClick();
  const drawer = document.getElementById("yourMgmtSubDrawer");
  if (drawer) drawer.style.display = "none";
}

// 5. Staff Interaction Handler
function interactWithMgmtStaff(staffId, action) {
  playMechanicalClick();
  const current = mgmtStaffRelationships[staffId] || 70;
  const staff = MANAGEMENT_STAFF_DATA.find(s => s.id === staffId);
  const staffName = staff ? staff.name : "Staff";

  if (action === "chat") {
    const next = Math.min(100, current + 4);
    mgmtStaffRelationships[staffId] = next;
    const scoreEl = document.getElementById(`mgmtStaffRelScore_${staffId}`);
    const barEl = document.getElementById(`mgmtStaffRelBar_${staffId}`);
    if (scoreEl) scoreEl.textContent = `${next}/100`;
    if (barEl) barEl.style.width = `${next}%`;
    showToast(`CALL WITH ${staffName.toUpperCase()}: +4 RELATIONSHIP (${next}/100)`);
  } else if (action === "gift") {
    const next = Math.min(100, current + 10);
    mgmtStaffRelationships[staffId] = next;
    const scoreEl = document.getElementById(`mgmtStaffRelScore_${staffId}`);
    const barEl = document.getElementById(`mgmtStaffRelBar_${staffId}`);
    if (scoreEl) scoreEl.textContent = `${next}/100`;
    if (barEl) barEl.style.width = `${next}%`;
    showToast(`GIFT SENT TO ${staffName.toUpperCase()}: -$3,500 (+10 REL)`);
  }
}

// 6. Management Requests Handler
function submitManagementRequest(reqType) {
  playMechanicalClick();
  if (reqType === "blitz") {
    showToast("VIRAL PRESS BLITZ COMMISSIONED: +12% WEEKLY HYPE BOOST");
  } else if (reqType === "crisis") {
    showToast("CRISIS PR SQUAD DEPLOYED: NEGATIVE PRESS NEUTRALIZED");
  } else if (reqType === "interview") {
    showToast("INTERVIEW SECURED: LIVE ON THE BREAKFAST CLUB NEXT WEEK");
  } else if (reqType === "switch_term") {
    const nextTerm = yourManagementState.totalWeeks === 52 ? "six_month" : (yourManagementState.totalWeeks === 26 ? "month" : "year");
    const agency = MANAGEMENT_DATA.find(a => a.id === yourManagementState.agencyId) || MANAGEMENT_DATA[1];
    const plan = agency.plans[nextTerm];
    yourManagementState.planType = nextTerm;
    yourManagementState.planValueDisplay = plan.display;
    yourManagementState.planCost = plan.cost;
    yourManagementState.totalWeeks = plan.weeks;
    yourManagementState.weeksRemaining = plan.weeks;
    showToast(`SWITCHED RETAINER TERM TO: ${plan.display}`);
    renderYourManagementContract();
    closeYourManagementSubdrawer();
  } else if (reqType === "terminate") {
    showToast("REPRESENTATION TERMINATED: YOU ARE CURRENTLY SELF-MANAGED");
    yourManagementState.agencyName = "Independent Self-Management";
    yourManagementState.planValueDisplay = "$0.00 (DIY)";
    yourManagementState.weeksRemaining = 0;
    yourManagementState.weeklyPopularity = "+0-2%";
    renderYourManagementContract();
    closeYourManagementSubdrawer();
  }
}

// 7. Management History Modal
function openManagementHistoryModal() {
  playMechanicalClick();
  const modal = document.getElementById("mgmtHistoryModal");
  const content = document.getElementById("mgmtHistoryContent");
  if (!modal || !content) return;

  const agency = MANAGEMENT_DATA.find(a => a.id === yourManagementState.agencyId) || MANAGEMENT_DATA[1];

  content.innerHTML = `
    <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; margin-bottom: 6px;">
      Chronological record of all media agency agreements and PR representations.
    </div>

    <!-- Active Retainer -->
    <div class="history-contract-entry active">
      <span class="history-active-tag" style="background: #451a03; color: #fbbf24; border: 1px solid #78350f;">CURRENTLY ACTIVE</span>
      <h4 style="margin: 0; font-size: 0.88rem; font-weight: 900; color: #f8fafc;">${agency.name}</h4>
      <span style="font-size: 0.7rem; color: #fbbf24; font-weight: 700;">Year 2 – Present &bull; ${yourManagementState.planValueDisplay}</span>
      <p style="margin: 4px 0 0 0; font-size: 0.72rem; color: #cbd5e1;">
        Retained ${agency.name} for talent branding and media acceleration. ${yourManagementState.weeksRemaining} of ${yourManagementState.totalWeeks} weeks remaining.
      </p>
    </div>

    <!-- Era 1: Amplify Collective -->
    <div class="history-contract-entry">
      <h4 style="margin: 0; font-size: 0.88rem; font-weight: 900; color: #f8fafc;">AMPLIFY COLLECTIVE</h4>
      <span style="font-size: 0.7rem; color: #94a3b8; font-weight: 700;">Year 1 &bull; 1-Year Retainer Completed &bull; $12,000.00 / YR</span>
      <p style="margin: 4px 0 0 0; font-size: 0.72rem; color: #94a3b8;">
        Grassroots PR campaign concluded with 42 blog write-ups and initial TikTok audio syndication. Artist popularity surged from 12 to 38.
      </p>
    </div>

    <!-- Era 0: DIY Self-Management -->
    <div class="history-contract-entry">
      <h4 style="margin: 0; font-size: 0.88rem; font-weight: 900; color: #f8fafc;">INDEPENDENT DIY PR</h4>
      <span style="font-size: 0.7rem; color: #94a3b8; font-weight: 700;">Early Career &bull; Self-Managed</span>
      <p style="margin: 4px 0 0 0; font-size: 0.72rem; color: #94a3b8;">
        Initial cold outreach to local blogs and SoundCloud tastemakers. No retainer fees paid.
      </p>
    </div>
  `;

  modal.style.display = "flex";
}

function closeManagementHistoryModal(e) {
  if (e && e.target && e.target.id !== "mgmtHistoryModal" && !e.target.classList.contains("subdrawer-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("mgmtHistoryModal");
  if (modal) modal.style.display = "none";
}

/* ==========================================================================
   CALENDAR FULL-SCREEN APP & ITINERARY SUITE (ENGINE IMPLEMENTATION)
   Faithfully modeled on user reference sketch (media_1791145109525.png)
   - 4-Week Overview Grid with Month Pills (June above 12, July above 1)
   - Multi-day Event Banners running across days (e.g. • VMAs •)
   - 2-Arrow Navigation (Jan 1, Year 1 to Infinity)
   - Events Preview Card & Annual Directory Modal (Awards & Festivals)
   - Week Detail View: Your Tasks + New Releases (Industry)
   - 4-Week Industry Intelligence Restriction (Current Week + 4)
   - Custom Event Marker (+ button) for single date or date range
   - Edge-to-edge hardware status bar & red back navigation arrow
   ========================================================================== */

// Calendar State
let currentCalStartWeek = 24; // Defaults to careerWeek (24)
let selectedDetailWeek = 24;
let calCustomDateMode = "single";

// Custom Player Scheduled Events
let customPlayerEvents = [
  {
    id: "c-ev-1",
    title: "Secret Album Listening Party",
    type: "release",
    weekNum: 24,
    startDayIndex: 3, // Thursday June 15
    endDayIndex: 3,
    notes: "Quad Studios NYC • VIP & Tastemakers Only"
  },
  {
    id: "c-ev-2",
    title: "Vogue Summer Cover Photo Shoot",
    type: "interview",
    weekNum: 25,
    startDayIndex: 1, // Tuesday June 20
    endDayIndex: 1,
    notes: "Milk Studios Manhattan • Editorial Interview"
  }
];

// Annual Festivals & Award Shows Database (Chronological by Week of Year 1-52)
const ANNUAL_INDUSTRY_EVENTS = [
  {
    id: "ev-grammys",
    name: "The 67th Grammy Awards",
    shortName: "Grammys",
    type: "award",
    weekOfYear: 5,
    durationDays: 1,
    startDayOfWeek: 6, // Sunday
    location: "Crypto.com Arena",
    prestige: 100,
    description: "The music industry's highest honor. Four general field categories plus Best Rap Album and Rap Song.",
    requirements: "Eligible for recordings released during tracking cycle. Min 50M streams & critical acclaim.",
    rewards: "Iconic Gold Gramophone, +50% Global Fame, +35% Streaming Multiplier"
  },
  {
    id: "ev-brits",
    name: "The BRIT Awards",
    shortName: "BRITs",
    type: "award",
    weekOfYear: 8,
    durationDays: 1,
    startDayOfWeek: 5, // Saturday
    location: "The O2 Arena",
    prestige: 88,
    description: "The UK's flagship annual music ceremony celebrating domestic and international chart-toppers.",
    requirements: "Top 10 UK Official Singles Chart placement or international crossover breakthrough.",
    rewards: "BRIT Statuette, +25% European Airplay, +15% Global Prestige"
  },
  {
    id: "ev-coachella",
    name: "Coachella Valley Music & Arts Festival",
    shortName: "Coachella",
    type: "festival",
    weekOfYear: 15,
    durationDays: 3,
    startDayOfWeek: 4, // Friday (Fri - Sun)
    location: "Empire Polo Club",
    prestige: 98,
    description: "The world's premier cultural and live performance spectacle in the Colorado Desert.",
    requirements: "Headliner or Sub-Headliner status, min 40M monthly listeners or viral impact.",
    rewards: "$1.5M - $3.5M Performance Retainer, Worldwide Livestream syndication, Viral Twitter trending"
  },
  {
    id: "ev-bbma",
    name: "Billboard Music Awards",
    shortName: "BBMAs",
    type: "award",
    weekOfYear: 21,
    durationDays: 1,
    startDayOfWeek: 6, // Sunday
    location: "MGM Grand",
    prestige: 92,
    description: "Honoring the year's top chart performers based on real streaming data, radio airplay, and physical sales.",
    requirements: "Billboard Hot 100 or Billboard 200 charting track within the last 52 weeks.",
    rewards: "Billboard Trophy, +20% Streaming Revenue Surge, +18% Industry Buzz"
  },
  {
    id: "ev-summerjam",
    name: "Hot 97 Summer Jam NYC",
    shortName: "Summer Jam",
    type: "festival",
    weekOfYear: 24,
    durationDays: 1,
    startDayOfWeek: 4, // Friday (June 16)
    location: "MetLife Stadium",
    prestige: 90,
    description: "The sacred historic hip-hop stadium festival hosted by New York's iconic Hot 97.",
    requirements: "East Coast / Global rap prominence, undeniable club anthem of the summer.",
    rewards: "$650,000 Performance Retainer, Hip-hop legend credibility, Radio heavy rotation"
  },
  {
    id: "ev-govball",
    name: "Governors Ball Music Festival",
    shortName: "Gov Ball",
    type: "festival",
    weekOfYear: 25,
    durationDays: 3,
    startDayOfWeek: 4, // Friday through Sunday (June 23-25)
    location: "Flushing Meadows",
    prestige: 89,
    description: "New York City's crown summer music festival featuring major multi-genre stadium headliners.",
    requirements: "Top 20 Billboard hit, strong Tri-State fan demographic.",
    rewards: "$800,000 Retainer, NYC streetwear cultural influence, +12% Fan Demographics"
  },
  {
    id: "ev-glasto",
    name: "Glastonbury Contemporary Arts Festival",
    shortName: "Glastonbury",
    type: "festival",
    weekOfYear: 26,
    durationDays: 5,
    startDayOfWeek: 2, // Wednesday through Sunday (June 28 - July 2)
    location: "Worthy Farm",
    prestige: 99,
    description: "The holy grail of global open-air performing arts festivals with 210,000 attendees at the Pyramid Stage.",
    requirements: "Historic cultural relevance, critically acclaimed discography.",
    rewards: "Pyramid Stage Legend status, BBC Worldwide Broadcast, +45% European Tour Demand"
  },
  {
    id: "ev-vma-sketch",
    name: "MTV Video Music Awards (VMAs)",
    shortName: "VMAs",
    type: "award",
    weekOfYear: 27,
    durationDays: 3,
    startDayOfWeek: 4, // Friday through Sunday (July 7-9)
    location: "Prudential Center",
    prestige: 95,
    description: "The wildest, most viral night in pop and hip-hop culture. Moonman trophies awarded for visionary music videos.",
    requirements: "Official Music Video released during current cycle, min 15M streams.",
    rewards: "MTV Moonman Trophy, Historic Red Carpet Moment, +40% Viral Index"
  },
  {
    id: "ev-bet",
    name: "BET Awards",
    shortName: "BET Awards",
    type: "award",
    weekOfYear: 28,
    durationDays: 1,
    startDayOfWeek: 6, // Sunday (July 16)
    location: "Peacock Theater",
    prestige: 94,
    description: "Celebrating Black excellence and culture across hip-hop, R&B, sports, and entertainment.",
    requirements: "Active cultural engagement, leading urban radio hit, min 25M streams.",
    rewards: "BET Award Trophy, Culture Hero badge, Urban Radio Multiplier"
  },
  {
    id: "ev-rollingloud",
    name: "Rolling Loud Miami",
    shortName: "Rolling Loud",
    type: "festival",
    weekOfYear: 30,
    durationDays: 3,
    startDayOfWeek: 4, // Friday through Sunday
    location: "Hard Rock Stadium",
    prestige: 96,
    description: "The largest dedicated hip-hop festival on planet earth featuring over 100+ rap superstars.",
    requirements: "High-energy catalog, mosh pit anthems, platinum certification.",
    rewards: "$1,200,000 Headliner Fee, Viral festival clips, +30% Merch Sales"
  },
  {
    id: "ev-lolla",
    name: "Lollapalooza Chicago",
    shortName: "Lollapalooza",
    type: "festival",
    weekOfYear: 31,
    durationDays: 4,
    startDayOfWeek: 3, // Thursday through Sunday
    location: "Grant Park",
    prestige: 95,
    description: "Iconic 4-day festival across 8 stages on the shores of Lake Michigan with 400,000 attendees.",
    requirements: "Nationwide arena-level audience draw, major crossover appeal.",
    rewards: "$1,000,000 Fee, Midwest fanbase expansion, Hulu Live headliner stream"
  },
  {
    id: "ev-vma-fall",
    name: "MTV Video Music Awards (Fall Broadcast)",
    shortName: "VMAs",
    type: "award",
    weekOfYear: 37,
    durationDays: 3,
    startDayOfWeek: 4, // Friday through Sunday
    location: "UBS Arena",
    prestige: 95,
    description: "The historic fall VMAs gala, world premiere performances, and Moonman presentations.",
    requirements: "Visionary music video production, high fan voting volume.",
    rewards: "MTV Moonman Trophy, +45% Streaming Jump"
  },
  {
    id: "ev-bethiphop",
    name: "BET Hip Hop Awards",
    shortName: "BET Hip Hop",
    type: "award",
    weekOfYear: 41,
    durationDays: 1,
    startDayOfWeek: 1, // Tuesday
    location: "Cobb Energy Centre",
    prestige: 91,
    description: "The legendary gathering of lyricists, producers, and cypher champions in the rap capital Atlanta.",
    requirements: "Lyric of the Year or Impact Track nomination, street credibility.",
    rewards: "BET Hip Hop Trophy, Cypher Hall of Fame inclusion, +20% Rap Core Fanbase"
  },
  {
    id: "ev-ama",
    name: "American Music Awards (AMAs)",
    shortName: "AMAs",
    type: "award",
    weekOfYear: 46,
    durationDays: 1,
    startDayOfWeek: 6, // Sunday
    location: "Microsoft Theater",
    prestige: 90,
    description: "The world's largest fan-voted awards show honoring commercial hits and favorite hip-hop artists.",
    requirements: "High fan voting engagement, Billboard commercial performance.",
    rewards: "AMA Pyramid Trophy, Prime-time ABC broadcast exposure, +25% Brand Deals"
  },
  {
    id: "ev-campfloggnaw",
    name: "Camp Flog Gnaw Carnival",
    shortName: "Flog Gnaw",
    type: "festival",
    weekOfYear: 49,
    durationDays: 2,
    startDayOfWeek: 5, // Saturday - Sunday
    location: "Dodger Stadium",
    prestige: 93,
    description: "Tyler, The Creator's beloved carnival and music festival celebrating alternative and creative hip-hop.",
    requirements: "Artistic innovation, dedicated cult fanbase, genre-bending catalog.",
    rewards: "$900,000 Fee, Cult streetwear credibility, Golf Wang collab potential"
  }
];

// Industry Releases Database (Curated & Procedural)
const UPCOMING_INDUSTRY_RELEASES = {
  24: [
    {
      artist: "Drake",
      title: "ICEMAN (Single)",
      type: "Single",
      label: "OVO Sound / Republic",
      dayName: "FRI",
      dayNum: 16,
      cover: "album covers/Tyler Durden.jpg",
      buzz: "🔥 Mega Hit Anticipated",
      details: "First single from Drake's upcoming summer rollout. Heavy radio backing expected."
    },
    {
      artist: "Travis Scott & Playboi Carti",
      title: "FE!N PART 2",
      type: "Single",
      label: "Cactus Jack / Epic",
      dayName: "FRI",
      dayNum: 16,
      cover: "album covers/download (5).jpg",
      buzz: "⚡ Viral Club Banger",
      details: "High-energy festival anthem teased across European arena dates."
    }
  ],
  25: [
    {
      artist: "Kendrick Lamar",
      title: "NOT LIKE THEM",
      type: "Single",
      label: "pgLang / Interscope",
      dayName: "FRI",
      dayNum: 23,
      cover: "album covers/download (6).jpg",
      buzz: "👑 Critical Juggernaut",
      details: "Sudden surprise release following West Coast stadium celebration."
    },
    {
      artist: "Metro Boomin x Future",
      title: "WE STILL DON'T TRUST YOU (Deluxe)",
      type: "Deluxe Album",
      label: "Boominati / Epic",
      dayName: "FRI",
      dayNum: 23,
      cover: "album covers/download (7).jpg",
      buzz: "🔥 Chart Contender",
      details: "5 unreleased bonus tracks featuring 21 Savage and Young Nudy."
    }
  ],
  26: [
    {
      artist: "21 Savage",
      title: "SLAUGHTER HOUSE NYC",
      type: "Single",
      label: "Slaughter Gang / Epic",
      dayName: "FRI",
      dayNum: 30,
      cover: "album covers/download (2).jpg",
      buzz: "🗡️ Trap Heavyweight",
      details: "Dark Atlanta trap anthem produced by Metro Boomin & Southside."
    },
    {
      artist: "SZA",
      title: "LANA (Deluxe Edition)",
      type: "Album",
      label: "Top Dawg / RCA",
      dayName: "FRI",
      dayNum: 30,
      cover: "album covers/Music artwork for Frank Ocean - _.jpg",
      buzz: "💫 Streaming Monster",
      details: "Long-awaited deluxe expansion with 8 vault tracks and acoustic interludes."
    }
  ],
  27: [
    {
      artist: "Lil Baby",
      title: "WHAM ERA",
      type: "Studio Album",
      label: "Quality Control / Motown",
      dayName: "FRI",
      dayNum: 7,
      cover: "album covers/download (4).jpg",
      buzz: "🚀 Summer Stadium Tour",
      details: "18-track fourth solo album featuring Gunna, Lil Durk, and Future."
    },
    {
      artist: "Gunna",
      title: "ONE OF WUN II",
      type: "Single",
      label: "YSL / 300 Entertainment",
      dayName: "FRI",
      dayNum: 7,
      cover: "album covers/download (8).jpg",
      buzz: "🌊 Melodic Drip",
      details: "Smooth summer acoustic guitar trap beat produced by Turbo."
    }
  ],
  28: [
    {
      artist: "A$AP Rocky",
      title: "DON'T BE DUMB",
      type: "Studio Album",
      label: "AWGE / RCA",
      dayName: "FRI",
      dayNum: 14,
      cover: "album covers/download (3).jpg",
      buzz: "🎬 High Fashion Visuals",
      details: "German Expressionism inspired rollout featuring Tyler, The Creator and Westside Gunn."
    }
  ]
};

// Procedural generator for industry drops in later simulated weeks
function getIndustryReleasesForWeek(weekNum) {
  if (UPCOMING_INDUSTRY_RELEASES[weekNum]) {
    return UPCOMING_INDUSTRY_RELEASES[weekNum];
  }
  const artistsPool = [
    { name: "Drake", label: "OVO / Republic", buzz: "🔥 Global Hit" },
    { name: "Kendrick Lamar", label: "pgLang / Interscope", buzz: "👑 Critical Acclaim" },
    { name: "Future", label: "Freebandz / Epic", buzz: "⚡ Trap Anthem" },
    { name: "Travis Scott", label: "Cactus Jack / Epic", buzz: "🚀 Raging Banger" },
    { name: "Playboi Carti", label: "Opium / Interscope", buzz: "🧛 Cult Frenzy" },
    { name: "21 Savage", label: "Slaughter Gang / Epic", buzz: "🗡️ Street Record" },
    { name: "SZA", label: "TDE / RCA", buzz: "💫 Streaming Juggernaut" }
  ];
  const wInfo = getWeekCalendarInfo(weekNum);
  const a1 = artistsPool[Math.abs(weekNum * 3) % artistsPool.length];
  const a2 = artistsPool[Math.abs(weekNum * 7 + 1) % artistsPool.length];
  return [
    {
      artist: a1.name,
      title: `Drop ${weekNum} (Single)`,
      type: "Single",
      label: a1.label,
      dayName: "FRI",
      dayNum: wInfo.days[4].dayOfMonth,
      cover: getRandomAlbumCover(),
      buzz: a1.buzz,
      details: `Scheduled Friday drop targeting Hot 100 top 10 debut.`
    },
    {
      artist: a2.name,
      title: `Session ${weekNum} EP`,
      type: "EP",
      label: a2.label,
      dayName: "FRI",
      dayNum: wInfo.days[4].dayOfMonth,
      cover: getRandomAlbumCover(),
      buzz: a2.buzz,
      details: `Surprise 4-track release with heavy social media campaign.`
    }
  ];
}

// Open Calendar Application (Full-Screen)
function openCalendarApp() {
  playMechanicalClick();

  // 1. Hide console bottom nav
  const mainBottomNav = document.querySelector(".bottom-nav-bar");
  if (mainBottomNav) mainBottomNav.style.display = "none";

  // 2. Hide social main hub
  const socialHub = document.getElementById("socialMainHub");
  if (socialHub) socialHub.style.display = "none";

  // 3. Synchronize phone clock in top bar
  updateClock();

  // 4. Show calendar full-screen container
  const app = document.getElementById("appView_calendar");
  if (app) app.style.display = "flex";

  // 5. Reset to current career week and overview
  currentCalStartWeek = careerWeek;
  renderCalendar4Weeks();
  renderUpcomingEventsPreview();

  // Ensure overview is visible, detail view hidden
  const overview = document.getElementById("calendarOverviewView");
  const detail = document.getElementById("calendarWeekDetailView");
  if (overview) overview.style.display = "flex";
  if (detail) detail.style.display = "none";

  const viewport = document.getElementById("calendarMainViewport");
  if (viewport) viewport.scrollTop = 0;
}

// Close Calendar Application
function closeCalendarApp() {
  playMechanicalClick();

  // 1. Hide calendar view
  const app = document.getElementById("appView_calendar");
  if (app) app.style.display = "none";

  // 2. Close any open calendar modals
  closeAllCalendarEventsModal();
  closeAddCustomEventModal();

  // 3. Restore console bottom nav
  const mainBottomNav = document.querySelector(".bottom-nav-bar");
  if (mainBottomNav) mainBottomNav.style.display = "flex";

  // 4. Restore social main hub
  const socialHub = document.getElementById("socialMainHub");
  if (socialHub) socialHub.style.display = "flex";

  // 5. Return to Social Tab
  switchTab("social");
}

// Global Hardware Back Navigation (Top Left Red Arrow)
function handleCalendarBackNavigation() {
  playMechanicalClick();
  const detailView = document.getElementById("calendarWeekDetailView");
  if (detailView && detailView.style.display !== "none") {
    closeCalendarWeekDetail();
  } else {
    closeCalendarApp();
  }
}

// Render 4-Week Grid & Header Range
function renderCalendar4Weeks() {
  const container = document.getElementById("calendar4WeeksRowsContainer");
  const headerTitle = document.getElementById("calendarHeaderDateRange");
  if (!container || !headerTitle) return;

  const startInfo = getWeekCalendarInfo(currentCalStartWeek);
  const endInfo = getWeekCalendarInfo(currentCalStartWeek + 3);

  // Format Header Title (e.g. JUNE 12 - JULY 9 , YEAR 2)
  let titleStr = "";
  if (startInfo.monday.year === endInfo.sunday.year) {
    titleStr = `${startInfo.monday.monthFullName} ${startInfo.monday.dayOfMonth} - ${endInfo.sunday.monthFullName} ${endInfo.sunday.dayOfMonth} , YEAR ${startInfo.monday.year}`;
  } else {
    titleStr = `${startInfo.monday.monthFullName} ${startInfo.monday.dayOfMonth}, YEAR ${startInfo.monday.year} - ${endInfo.sunday.monthFullName} ${endInfo.sunday.dayOfMonth}, YEAR ${endInfo.sunday.year}`;
  }
  headerTitle.textContent = titleStr.toUpperCase();

  let rowsHtml = "";

  for (let w = 0; w < 4; w++) {
    const weekNum = currentCalStartWeek + w;
    const weekInfo = getWeekCalendarInfo(weekNum);
    const isCurrentWeek = weekNum === careerWeek;

    // Check multi-day annual events & custom events for this week
    const weekAnnualEvents = ANNUAL_INDUSTRY_EVENTS.filter(ev => {
      // Annual events repeat each 52 weeks
      const modWeek = ((weekNum - 1) % 52) + 1;
      return ev.weekOfYear === modWeek && ev.durationDays > 1;
    });

    const weekMultiCustom = customPlayerEvents.filter(ev => ev.weekNum === weekNum && ev.endDayIndex > ev.startDayIndex);

    let multiBannersHtml = "";
    weekAnnualEvents.forEach(ev => {
      const startDay = ev.startDayOfWeek || 4; // default Friday
      const spanDays = Math.min(ev.durationDays, 7 - startDay);
      const leftPct = (100 / 7) * startDay;
      const widthPct = (100 / 7) * spanDays;
      multiBannersHtml += `
        <div class="cal-multi-event-banner" style="left: calc(${leftPct}% + 2px); width: calc(${widthPct}% - 4px);" title="${ev.name}">
          &bull; ${ev.shortName} &bull;
        </div>
      `;
    });

    weekMultiCustom.forEach(ev => {
      const leftPct = (100 / 7) * ev.startDayIndex;
      const widthPct = (100 / 7) * (ev.endDayIndex - ev.startDayIndex + 1);
      multiBannersHtml += `
        <div class="cal-multi-event-banner" style="left: calc(${leftPct}% + 2px); width: calc(${widthPct}% - 4px); background: #3B82F6;" title="${ev.title}">
          &bull; ${ev.title} &bull;
        </div>
      `;
    });

    let daysHtml = "";
    for (let d = 0; d < 7; d++) {
      const day = weekInfo.days[d];
      const isToday = isCurrentWeek && d === 0; // Monday of current game week

      // Month Tag Rule:
      // 1. First week Monday (w === 0 && d === 0): ALWAYS has month pill (e.g. JUNE)
      // 2. Day of month === 1: ALWAYS has month pill (e.g. JULY)
      let monthTagHtml = "";
      const hasMonthTag = (w === 0 && d === 0) || (day.dayOfMonth === 1);
      if (hasMonthTag) {
        monthTagHtml = `<span class="cal-month-pill">${day.monthFullName}</span>`;
      }

      // Collect task icons for this day
      const itin = getDayItinerary(weekNum, d);
      const customOnDay = customPlayerEvents.filter(ev => ev.weekNum === weekNum && d >= ev.startDayIndex && d <= ev.endDayIndex);

      let iconsList = [];
      if (itin.events.includes("release")) iconsList.push("🚀");
      if (itin.events.includes("ticket")) iconsList.push("🎤");
      if (itin.events.includes("mic")) iconsList.push("🎙️");
      if (itin.events.includes("date")) iconsList.push("🥂");

      // Label contract expiry milestone check
      if (typeof yourLabelState !== "undefined" && yourLabelState && yourLabelState.weeksLeft) {
        if (weekNum === careerWeek + yourLabelState.weeksLeft && d === 0) {
          iconsList.push("📄");
        }
      }

      customOnDay.forEach(c => {
        if (c.type === "release") iconsList.push("🚀");
        else if (c.type === "concert") iconsList.push("🎤");
        else if (c.type === "interview") iconsList.push("🎙️");
        else if (c.type === "studio") iconsList.push("🎵");
        else if (c.type === "video") iconsList.push("🎬");
        else if (c.type === "contract") iconsList.push("📄");
        else iconsList.push("📌");
      });

      // Deduplicate icons to keep clean UI
      iconsList = [...new Set(iconsList)].slice(0, 3);

      const taskIconsHtml = iconsList.map(ic => `<span class="cal-task-mini-icon">${ic}</span>`).join("");

      daysHtml += `
        <div class="cal-day-cell ${hasMonthTag ? "has-month-tag" : ""} ${isToday ? "is-today" : ""}"
             onclick="event.stopPropagation(); openCalendarWeekDetail(${weekNum}, ${d});"
             title="Open Week ${weekNum} Detail (${day.dayName} ${day.dayOfMonth})">
          ${monthTagHtml}
          <span class="cal-day-number">${day.dayOfMonth}</span>
          <div class="cal-day-task-icons">
            ${taskIconsHtml}
          </div>
        </div>
      `;
    }

    rowsHtml += `
      <div class="cal-week-row ${isCurrentWeek ? "is-current-week" : ""}"
           onclick="openCalendarWeekDetail(${weekNum})"
           title="Tap to inspect Week ${weekNum}">
        ${daysHtml}
        ${multiBannersHtml}
      </div>
    `;
  }

  container.innerHTML = rowsHtml;

  // Update Navigation Prev button disabled state (Week 1 = Jan 1, Year 1)
  const prevBtn = document.querySelector(".cal-arrow-prev");
  if (prevBtn) {
    prevBtn.disabled = (currentCalStartWeek <= 1);
  }
}

// 2-Arrow Navigation Functions
function navCalendarPrev4Weeks() {
  playMechanicalClick();
  if (currentCalStartWeek > 1) {
    currentCalStartWeek = Math.max(1, currentCalStartWeek - 4);
    renderCalendar4Weeks();
    renderUpcomingEventsPreview();
  }
}

function navCalendarNext4Weeks() {
  playMechanicalClick();
  currentCalStartWeek += 4;
  renderCalendar4Weeks();
  renderUpcomingEventsPreview();
}

function resetCalendarToCurrent() {
  playMechanicalClick();
  currentCalStartWeek = careerWeek;
  renderCalendar4Weeks();
  renderUpcomingEventsPreview();
  showToast(`JUMPED TO CURRENT WEEK ${careerWeek}`);
}

// Compute Real Date Range String for Annual Events (e.g. JUNE 23 - 25, JULY 7 - 9, JUNE 16)
function getEventDateRangeString(ev, targetYear = 2) {
  const yr = targetYear || 2;
  const startDayOffset = (yr - 1) * 365 + (ev.weekOfYear - 1) * 7 + 1 + (typeof ev.startDayOfWeek === "number" ? ev.startDayOfWeek : 4);
  const startDate = getCalendarDate(startDayOffset);

  if (!ev.durationDays || ev.durationDays <= 1) {
    return `${startDate.monthFullName} ${startDate.dayOfMonth}`;
  } else {
    const endDayOffset = startDayOffset + ev.durationDays - 1;
    const endDate = getCalendarDate(endDayOffset);
    if (startDate.monthName === endDate.monthName) {
      return `${startDate.monthFullName} ${startDate.dayOfMonth} - ${endDate.dayOfMonth}`;
    } else {
      return `${startDate.monthFullName} ${startDate.dayOfMonth} - ${endDate.monthFullName} ${endDate.dayOfMonth}`;
    }
  }
}

// Render Upcoming Events Preview Card (Festivals & Awards with real date ranges)
function renderUpcomingEventsPreview() {
  const container = document.getElementById("calendarUpcomingEventsList");
  if (!container) return;

  const baseWeek = currentCalStartWeek || careerWeek;
  const currentModWeek = ((baseWeek - 1) % 52) + 1;
  const currentCareerYear = Math.floor((baseWeek - 1) / 52) + 1;

  // Get next 3 upcoming events relative to currentModWeek
  const sorted = [...ANNUAL_INDUSTRY_EVENTS].sort((a, b) => {
    const diffA = (a.weekOfYear - currentModWeek + 52) % 52;
    const diffB = (b.weekOfYear - currentModWeek + 52) % 52;
    return diffA - diffB;
  });

  const previewItems = sorted.slice(0, 3);
  let html = "";
  previewItems.forEach(ev => {
    const icon = ev.type === "award" ? "🏆" : "🎪";
    const badgeCls = ev.type === "award" ? "badge-award" : "badge-festival";
    const badgeTxt = ev.type === "award" ? "AWARDS" : "FESTIVAL";
    const evYear = ev.weekOfYear < currentModWeek ? currentCareerYear + 1 : currentCareerYear;
    const dateRangeStr = getEventDateRangeString(ev, evYear);

    html += `
      <div class="cal-event-preview-item">
        <div class="cal-event-prev-left">
          <span class="cal-event-prev-icon">${icon}</span>
          <div class="cal-event-prev-info">
            <h4>${ev.name}</h4>
            <span>${dateRangeStr} &bull; ${ev.location}</span>
          </div>
        </div>
        <span class="cal-event-prev-badge ${badgeCls}">${badgeTxt}</span>
      </div>
    `;
  });

  container.innerHTML = html;
}

// Open Week Detail View (when user taps any week or date cell)
function openCalendarWeekDetail(weekNum, dayIndex = 0) {
  playMechanicalClick();
  selectedDetailWeek = weekNum;

  const overview = document.getElementById("calendarOverviewView");
  const detail = document.getElementById("calendarWeekDetailView");
  if (overview) overview.style.display = "none";
  if (detail) detail.style.display = "flex";

  renderCalendarWeekDetail(dayIndex);

  const viewport = document.getElementById("calendarMainViewport");
  if (viewport) viewport.scrollTop = 0;
}

// Close Week Detail View (Return to 4-Week Overview)
function closeCalendarWeekDetail() {
  playMechanicalClick();
  const overview = document.getElementById("calendarOverviewView");
  const detail = document.getElementById("calendarWeekDetailView");
  if (detail) detail.style.display = "none";
  if (overview) overview.style.display = "flex";

  // Re-render overview to reflect any newly added custom events
  renderCalendar4Weeks();
}

// Render Week Detail View Content
function renderCalendarWeekDetail(activeDayIndex = 0) {
  const weekInfo = getWeekCalendarInfo(selectedDetailWeek);

  // 1. Header Title (e.g. WEEK 24 • JUNE 12 - 18, YEAR 2)
  const titleEl = document.getElementById("calendarDetailWeekTitle");
  if (titleEl) {
    titleEl.textContent = `WEEK ${selectedDetailWeek} • ${weekInfo.rangeString.toUpperCase()}`;
  }

  // 2. 7-Day Calendar Strip at Top
  const stripEl = document.getElementById("calendarDetailWeekStrip");
  if (stripEl) {
    let stripHtml = "";
    for (let d = 0; d < 7; d++) {
      const day = weekInfo.days[d];
      const isActive = d === activeDayIndex;
      const itin = getDayItinerary(selectedDetailWeek, d);
      const customOnDay = customPlayerEvents.filter(ev => ev.weekNum === selectedDetailWeek && d >= ev.startDayIndex && d <= ev.endDayIndex);

      let icons = [];
      if (itin.events.includes("release")) icons.push("🚀");
      if (itin.events.includes("ticket")) icons.push("🎤");
      if (itin.events.includes("mic")) icons.push("🎙️");
      customOnDay.forEach(c => {
        if (c.type === "release") icons.push("🚀");
        else if (c.type === "concert") icons.push("🎤");
        else if (c.type === "interview") icons.push("🎙️");
        else if (c.type === "studio") icons.push("🎵");
        else icons.push("📌");
      });
      icons = [...new Set(icons)].slice(0, 2);

      stripHtml += `
        <div class="cal-strip-day ${isActive ? "active-day" : ""}" onclick="renderCalendarWeekDetail(${d})">
          <span class="cal-strip-day-name">${day.dayName}</span>
          <span class="cal-strip-day-num">${day.dayOfMonth}</span>
          <div class="cal-strip-icons">
            ${icons.map(ic => `<span style="font-size:0.64rem;">${ic}</span>`).join("")}
          </div>
        </div>
      `;
    }
    stripEl.innerHTML = stripHtml;
  }

  // 3. Section 1: Player's Tasks That Week
  const tasksListEl = document.getElementById("calendarWeekTasksList");
  const tasksCountEl = document.getElementById("calendarWeekTasksCount");
  if (tasksListEl) {
    let tasks = [];

    // Procedural/career itinerary events
    for (let d = 0; d < 7; d++) {
      const itin = getDayItinerary(selectedDetailWeek, d);
      const day = weekInfo.days[d];
      if (itin.events.length > 0 || itin.title !== "Rest Day") {
        let icon = "🎵";
        if (itin.events.includes("release")) icon = "🚀";
        else if (itin.events.includes("ticket")) icon = "🎤";
        else if (itin.events.includes("mic")) icon = "🎙️";
        else if (itin.events.includes("date")) icon = "🥂";

        tasks.push({
          title: itin.title,
          dayLabel: `${day.dayName} ${day.monthName} ${day.dayOfMonth}`,
          icon: icon,
          notes: `Official RapSim Career Schedule & Itinerary`,
          isCustom: false
        });
      }
    }

    // Label contract expiration milestone check
    if (typeof yourLabelState !== "undefined" && yourLabelState && yourLabelState.weeksLeft) {
      if (selectedDetailWeek === careerWeek + yourLabelState.weeksLeft) {
        tasks.push({
          title: `${yourLabelState.labelName} Contract Expiration`,
          dayLabel: `MON ${weekInfo.monday.monthName} ${weekInfo.monday.dayOfMonth}`,
          icon: "📄",
          notes: `Contract term reaches completion. Review renewal terms or enter free agency!`,
          isCustom: false
        });
      }
    }

    // Custom Player Events
    const weekCustom = customPlayerEvents.filter(ev => ev.weekNum === selectedDetailWeek);
    weekCustom.forEach(c => {
      const sIdx = (typeof c.startDayIndex === "number" && !isNaN(c.startDayIndex)) ? Math.max(0, Math.min(6, c.startDayIndex)) : 0;
      const eIdx = (typeof c.endDayIndex === "number" && !isNaN(c.endDayIndex)) ? Math.max(sIdx, Math.min(6, c.endDayIndex)) : sIdx;
      const startDay = weekInfo.days[sIdx];
      const endDay = weekInfo.days[eIdx];
      let dayTxt = `${startDay.dayName} ${startDay.monthName} ${startDay.dayOfMonth}`;
      if (eIdx > sIdx) {
        dayTxt = `${startDay.dayName} ${startDay.dayOfMonth} - ${endDay.dayName} ${endDay.dayOfMonth}`;
      }
      let icon = "📌";
      if (c.type === "release") icon = "🚀";
      else if (c.type === "concert") icon = "🎤";
      else if (c.type === "interview") icon = "🎙️";
      else if (c.type === "studio") icon = "🎵";
      else if (c.type === "video") icon = "🎬";
      else if (c.type === "contract") icon = "📄";

      tasks.unshift({
        title: c.title,
        dayLabel: dayTxt,
        icon: icon,
        notes: c.notes || "Custom Marked Event",
        isCustom: true
      });
    });

    if (tasksCountEl) tasksCountEl.textContent = `${tasks.length} TASKS`;

    if (tasks.length === 0) {
      tasksListEl.innerHTML = `
        <div class="cal-task-item-card" style="justify-content: center; color: #64748B; font-size: 0.72rem; padding: 16px;">
          No scheduled obligations this week. Rest or head into the studio!
        </div>
      `;
    } else {
      tasksListEl.innerHTML = tasks.map(t => `
        <div class="cal-task-item-card">
          <div class="cal-task-card-left">
            <div class="cal-task-avatar-icon">${t.icon}</div>
            <div class="cal-task-details">
              <h4>${t.title}</h4>
              <p>${t.notes}</p>
            </div>
          </div>
          <span class="cal-task-day-pill">${t.dayLabel}</span>
        </div>
      `).join("");
    }
  }

  // 4. Section 2: Industry Drops (Restricted to Current Week + 4)
  const releasesListEl = document.getElementById("calendarWeekReleasesList");
  const intelTagEl = document.getElementById("calendarIntelTag");
  if (releasesListEl) {
    const maxIntelWeek = careerWeek + 4;

    if (selectedDetailWeek > maxIntelWeek) {
      // Classified Confidential State
      if (intelTagEl) intelTagEl.textContent = "CLASSIFIED";
      releasesListEl.innerHTML = `
        <div class="cal-classified-locked-card">
          <span class="cal-lock-icon">🔒</span>
          <h4>INDUSTRY INTELLIGENCE RESTRICTED</h4>
          <p>
            Major record labels keep rollout calendars confidential beyond 4 weeks in advance (Week ${maxIntelWeek}).
            Upcoming drops for Week ${selectedDetailWeek} will decrypt as the rollout draws nearer.
          </p>
        </div>
      `;
    } else {
      // Confirmed Intelligence Drops State
      if (intelTagEl) intelTagEl.textContent = "CONFIRMED DROPS";
      const releases = getIndustryReleasesForWeek(selectedDetailWeek);

      if (releases.length === 0) {
        releasesListEl.innerHTML = `
          <div class="cal-task-item-card" style="justify-content: center; color: #64748B; font-size: 0.72rem; padding: 16px;">
            No major label releases slated for this week. Prime window for your music!
          </div>
        `;
      } else {
        releasesListEl.innerHTML = releases.map(r => `
          <div class="cal-release-item-card">
            <div class="cal-release-left">
              <img src="${r.cover}" class="cal-release-thumb" alt="${r.title}" />
              <div class="cal-release-meta">
                <h4>${r.artist} - "${r.title}"</h4>
                <p>${r.label} &bull; ${r.dayName} ${r.dayNum}</p>
              </div>
            </div>
            <span class="cal-release-buzz-badge">${r.buzz}</span>
          </div>
        `).join("");
      }
    }
  }
}

// Modal 1: Annual Events & Festivals Directory Modal
function openAllCalendarEventsModal() {
  playMechanicalClick();
  const modal = document.getElementById("calendarAllEventsModal");
  const content = document.getElementById("calendarAllEventsListContent");
  if (!modal || !content) return;

  const sortedEvents = [...ANNUAL_INDUSTRY_EVENTS].sort((a, b) => a.weekOfYear - b.weekOfYear);

  let html = "";
  sortedEvents.forEach(ev => {
    const isAward = ev.type === "award";
    const icon = isAward ? "🏆" : "🎪";
    const badgeCls = isAward ? "badge-award" : "badge-festival";
    const badgeTxt = isAward ? "AWARD SHOW" : "FESTIVAL";
    const dateRangeStr = getEventDateRangeString(ev, 2);
    html += `
      <div class="cal-dir-item">
        <div class="cal-dir-top">
          <div class="cal-dir-title-box">
            <span style="font-size: 1.1rem;">${icon}</span>
            <h4>${ev.name}</h4>
          </div>
          <span class="cal-event-prev-badge ${badgeCls}">${badgeTxt}</span>
        </div>
        <span class="cal-dir-dates">${dateRangeStr} &bull; ${ev.durationDays} ${ev.durationDays === 1 ? "DAY" : "DAYS"} &bull; PRESTIGE ${ev.prestige}/100</span>
        <p class="cal-dir-desc">${ev.description}</p>
        <div class="cal-dir-foot">
          <span class="cal-dir-loc">📍 ${ev.location}</span>
          <span class="cal-dir-reward">${ev.rewards}</span>
        </div>
      </div>
    `;
  });

  content.innerHTML = html;
  modal.style.display = "flex";
}

function closeAllCalendarEventsModal(e) {
  if (e && e.target && e.target.id !== "calendarAllEventsModal" && !e.target.classList.contains("cal-modal-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("calendarAllEventsModal");
  if (modal) modal.style.display = "none";
}

// Modal 2: Add Custom Event Modal
function openAddCustomEventModal() {
  playMechanicalClick();
  const modal = document.getElementById("calendarAddEventModal");
  if (!modal) return;

  // Populate Day Selectors with selectedDetailWeek's 7 days
  const weekInfo = getWeekCalendarInfo(selectedDetailWeek);
  const startSelect = document.getElementById("calEventStartDaySelect");
  const endSelect = document.getElementById("calEventEndDaySelect");

  if (startSelect && endSelect) {
    let opts = "";
    weekInfo.days.forEach(d => {
      opts += `<option value="${d.dayIndex}">${d.dayName} (${d.monthName} ${d.dayOfMonth})</option>`;
    });
    startSelect.innerHTML = opts;
    endSelect.innerHTML = opts;
  }

  // Reset Form
  const titleInput = document.getElementById("calEventTitleInput");
  const notesInput = document.getElementById("calEventNotesInput");
  if (titleInput) titleInput.value = "";
  if (notesInput) notesInput.value = "";

  setCalDateMode("single");
  modal.style.display = "flex";
}

function closeAddCustomEventModal(e) {
  if (e && e.target && e.target.id !== "calendarAddEventModal" && !e.target.classList.contains("cal-modal-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("calendarAddEventModal");
  if (modal) modal.style.display = "none";
}

function setCalDateMode(mode) {
  calCustomDateMode = mode;
  const singleBtn = document.getElementById("btnDateModeSingle");
  const rangeBtn = document.getElementById("btnDateModeRange");
  const endGroup = document.getElementById("calEndDayGroup");
  const lblStart = document.getElementById("lblCalStartDate");

  if (mode === "single") {
    if (singleBtn) singleBtn.classList.add("active");
    if (rangeBtn) rangeBtn.classList.remove("active");
    if (endGroup) endGroup.style.display = "none";
    if (lblStart) lblStart.textContent = "Event Date";
  } else {
    if (singleBtn) singleBtn.classList.remove("active");
    if (rangeBtn) rangeBtn.classList.add("active");
    if (endGroup) endGroup.style.display = "flex";
    if (lblStart) lblStart.textContent = "Start Date";
  }
}

function handleSaveCustomEvent(event) {
  if (event) event.preventDefault();
  playMechanicalClick();

  const titleInput = document.getElementById("calEventTitleInput");
  const typeSelect = document.getElementById("calEventTypeSelect");
  const startSelect = document.getElementById("calEventStartDaySelect");
  const endSelect = document.getElementById("calEventEndDaySelect");
  const notesInput = document.getElementById("calEventNotesInput");

  const title = titleInput ? titleInput.value.trim() : "";
  if (!title) {
    showToast("Please enter an event title!");
    return;
  }

  const type = typeSelect ? typeSelect.value : "release";
  const rawStart = parseInt(startSelect && startSelect.value !== "" ? startSelect.value : 0, 10);
  const startDay = isNaN(rawStart) ? 0 : Math.max(0, Math.min(6, rawStart));
  let endDay = startDay;
  if (calCustomDateMode === "range" && endSelect) {
    const rawEnd = parseInt(endSelect.value !== "" ? endSelect.value : startDay, 10);
    endDay = isNaN(rawEnd) ? startDay : Math.max(startDay, Math.min(6, rawEnd));
  }
  const notes = notesInput ? notesInput.value.trim() : "";

  customPlayerEvents.push({
    id: "c-ev-" + Date.now(),
    title: title,
    type: type,
    weekNum: selectedDetailWeek,
    startDayIndex: startDay,
    endDayIndex: endDay,
    notes: notes
  });

  closeAddCustomEventModal();
  renderCalendarWeekDetail();
  renderCalendar4Weeks();
  showToast(`MARKED "${title.toUpperCase()}" ON CALENDAR!`);
}

// =============================================================================
// BEAT STORE ENGINE (ONLINE BEAT MARKETPLACE)
// Modeled directly on user sketch (media_1791186145751.png)
// Features: SELL & BUY Tabs, Vault Inventory, Inbound/Outbound Negotiations,
// Bulk Discounts, Sales Analytics, Producer Directory, and Instant Beat Purchasing.
// =============================================================================

let activeBeatstoreTab = "sell";
let activeBeatListingType = "single";
let selectedBeatstoreGenreFilter = "ALL";
let inspectingBuyBeatId = null;
let beatstoreAudioPlaying = false;

// 1. Initial Player Beat Inventory (Matches sketch)
let playerBeatInventory = [
  {
    id: "beat-p1",
    title: "MIDNIGHT 808",
    type: "SINGLE",
    price: 2000,
    genre: "Trap",
    cover: "album covers/download (2).jpg",
    vaultRefId: "cat-s1",
    bpm: 140,
    key: "F# Minor",
    plays: 1240,
    likes: 86
  },
  {
    id: "beat-p2",
    title: "CHOPPER DRILL PACK",
    type: "PACK",
    price: 25000,
    genre: "Drill",
    cover: "album covers/download (5).jpg",
    vaultRefId: "cat-s2",
    bpm: 144,
    key: "D Minor",
    plays: 3820,
    likes: 312
  },
  {
    id: "beat-p3",
    title: "NEON SYNTH RUNNER",
    type: "SINGLE",
    price: 1250,
    genre: "Melodic",
    cover: "album covers/download (3).jpg",
    vaultRefId: "cat-s3",
    bpm: 128,
    key: "G# Minor",
    plays: 940,
    likes: 72
  },
  {
    id: "beat-p4",
    title: "ATLANTA TRAP VAULT",
    type: "PACK",
    price: 14000,
    genre: "Trap",
    cover: "album covers/download (8).jpg",
    vaultRefId: "cat-s4",
    bpm: 135,
    key: "C Minor",
    plays: 2110,
    likes: 184
  }
];

// 2. Inbound Negotiations (Offers from other artists to buy player's beats)
let inboundNegotiationsList = [
  {
    id: "inb-1",
    artistName: "Lil Yachty",
    artistAvatar: "album covers/download (3).jpg",
    beatId: "beat-p1",
    beatTitle: "MIDNIGHT 808",
    listPrice: 2000,
    offerPrice: 1750,
    status: "pending",
    message: "Yo bro, this 808 slides crazy! Can you do $1,750 for exclusive rights? Need it for the upcoming mixtape tonight."
  },
  {
    id: "inb-2",
    artistName: "Trippie Redd",
    artistAvatar: "album covers/download (4).jpg",
    beatId: "beat-p2",
    beatTitle: "CHOPPER DRILL PACK",
    listPrice: 25000,
    offerPrice: 21000,
    status: "pending",
    message: "These 5 drill tracks are heat. Lock me in for $21,000 all-in cash right now and send the stems."
  },
  {
    id: "inb-3",
    artistName: "BabyTron",
    artistAvatar: "album covers/download (5).jpg",
    beatId: "beat-p3",
    beatTitle: "NEON SYNTH RUNNER",
    listPrice: 1250,
    offerPrice: 1100,
    status: "pending",
    message: "I got a fast verse for this synth tempo. $1,100 instant transfer if we sign exclusive right now."
  }
];

// 3. Bulk Discount Promotions
let bulkDiscountRules = [
  {
    id: "bulk-1",
    title: "Buy 2 Singles, Get 1 Free",
    description: "Applies 33% discount when artists purchase 3 single beat licenses simultaneously.",
    discountPercent: 33,
    active: true
  },
  {
    id: "bulk-2",
    title: "Producer Pack Summer Sale",
    description: "15% off any Multi-Beat Pack ($10,000+ purchases).",
    discountPercent: 15,
    active: false
  },
  {
    id: "bulk-3",
    title: "VIP Exclusive Tier Discount",
    description: "20% loyalty incentive for return artists who bought previous beats.",
    discountPercent: 20,
    active: true
  }
];

// 4. Beat Sales History & Transaction Log
let beatSalesHistory = [
  {
    id: "sale-1",
    buyerName: "Ken Carson",
    beatTitle: "RAGE OVERDRIVE V2",
    type: "SINGLE",
    price: 3500,
    date: "2 days ago",
    revenueShare: 3500
  },
  {
    id: "sale-2",
    buyerName: "Destroy Lonely",
    beatTitle: "OBSIDIAN SYNTH PACK",
    type: "PACK",
    price: 18000,
    date: "4 days ago",
    revenueShare: 18000
  },
  {
    id: "sale-3",
    buyerName: "Gunna",
    beatTitle: "DRIPPY MELODIES VOL 1",
    type: "PACK",
    price: 22000,
    date: "1 week ago",
    revenueShare: 22000
  },
  {
    id: "sale-4",
    buyerName: "Yeat",
    beatTitle: "BELL TOLLING TRAP",
    type: "SINGLE",
    price: 4500,
    date: "1 week ago",
    revenueShare: 4500
  },
  {
    id: "sale-5",
    buyerName: "Playboi Carti",
    beatTitle: "VAMP GUITAR PACK",
    type: "PACK",
    price: 30000,
    date: "2 weeks ago",
    revenueShare: 30000
  }
];

// 5. Industry Released Beats This Week (BUY TAB)
let industryBeatsReleasedThisWeek = [
  {
    id: "ind-1",
    title: "HEROES & VILLAINS 808",
    producerName: "Metro Boomin",
    producerAvatar: "album covers/Tyler Durden.jpg",
    type: "SINGLE",
    price: 12500,
    genre: "Trap",
    cover: "album covers/download (2).jpg",
    bpm: 138,
    key: "C Minor",
    tags: ["Dark", "Cinematic", "Heavy Brass"],
    description: "Signature Metro orchestral brass & booming 808 rumble, arranged for festival trap records."
  },
  {
    id: "ind-2",
    title: "THE LIFE OF PI'ERRE PACK",
    producerName: "Pierre Bourne",
    producerAvatar: "album covers/download (6).jpg",
    type: "PACK",
    price: 28000,
    genre: "Melodic",
    cover: "album covers/download (4).jpg",
    bpm: 150,
    key: "F# Major",
    tags: ["Dreamy", "8-Bit", "Bouncy"],
    description: "5 multi-track melodic floaters with trademark flute leads, punchy claps, and 808 slides."
  },
  {
    id: "ind-3",
    title: "808 MAFIA SIEGE",
    producerName: "Southside",
    producerAvatar: "album covers/download (7).jpg",
    type: "SINGLE",
    price: 9500,
    genre: "Trap",
    cover: "album covers/download (6).jpg",
    bpm: 140,
    key: "D# Minor",
    tags: ["Aggressive", "Sirens", "Grimy"],
    description: "Sizzling high-hat rolls, war horns, and earth-shattering distortion built for violent drill-trap."
  },
  {
    id: "ind-4",
    title: "FUTURE RAGE DIMENSION",
    producerName: "BNYX",
    producerAvatar: "album covers/download (8).jpg",
    type: "SINGLE",
    price: 8000,
    genre: "Rage",
    cover: "album covers/download (7).jpg",
    bpm: 148,
    key: "A Minor",
    tags: ["Hyperpop", "Saw Synth", "Distortion"],
    description: "Cutting-edge EDM-trap hybrid synths layered with glitch vocal chops and hyper-velocity drums."
  },
  {
    id: "ind-5",
    title: "CRAFT VINYL SAMPLES VOL 3",
    producerName: "The Alchemist",
    producerAvatar: "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg",
    type: "PACK",
    price: 32000,
    genre: "Boom Bap",
    cover: "album covers/download (9).jpg",
    bpm: 88,
    key: "E Minor",
    tags: ["Soul Loop", "Dusty", "Drumless"],
    description: "Rare 1970s Italian psych-rock sample flips chopped with tape saturation. Pure underground royalty."
  },
  {
    id: "ind-6",
    title: "MEMPHIS 6-SHOOTER",
    producerName: "Tay Keith",
    producerAvatar: "album covers/download (9).jpg",
    type: "SINGLE",
    price: 7500,
    genre: "Trap",
    cover: "album covers/download (10).jpg",
    bpm: 142,
    key: "G Minor",
    tags: ["Piano Stomp", "Memphis", "Anthem"],
    description: "Dark minor piano chords, iconic snare rolls, and bouncy 808 bounce primed for street anthems."
  }
];

// 6. Producer Directory (Search Producers Modal)
let beatstoreProducersDirectory = [
  {
    id: "prod-metro",
    name: "Metro Boomin",
    avatar: "album covers/Tyler Durden.jpg",
    genre: "Trap",
    reputation: 99,
    beatsCount: 14,
    startingPrice: 12000,
    bio: "Multi-platinum executive producer behind Savage Mode and Heroes & Villains."
  },
  {
    id: "prod-pierre",
    name: "Pierre Bourne",
    avatar: "album covers/download (6).jpg",
    genre: "Melodic",
    reputation: 94,
    beatsCount: 9,
    startingPrice: 15000,
    bio: "Pioneer of bubblegum melody trap and soundscape wizard for Playboi Carti and Lil Uzi."
  },
  {
    id: "prod-southside",
    name: "Southside",
    avatar: "album covers/download (7).jpg",
    genre: "Trap",
    reputation: 96,
    beatsCount: 18,
    startingPrice: 9000,
    bio: "808 Mafia general and architect of the modern street trap sound."
  },
  {
    id: "prod-bnyx",
    name: "BNYX",
    avatar: "album covers/download (8).jpg",
    genre: "Rage",
    reputation: 91,
    beatsCount: 11,
    startingPrice: 7500,
    bio: "Working on Dying hitmaker behind Yeat and Drake's latest high-energy productions."
  },
  {
    id: "prod-alchemist",
    name: "The Alchemist",
    avatar: "album covers/How to Recreate Surreal Chessboard with Flying Fish (6 Easy Art Steps).jpg",
    genre: "Boom Bap",
    reputation: 98,
    beatsCount: 6,
    startingPrice: 25000,
    bio: "Grammy-nominated sample maestro crafting cinematic boom-bap opuses."
  },
  {
    id: "prod-taykeith",
    name: "Tay Keith",
    avatar: "album covers/download (9).jpg",
    genre: "Trap",
    reputation: 93,
    beatsCount: 12,
    startingPrice: 7000,
    bio: "Memphis legend turning piano melodies into Billboard #1 records."
  },
  {
    id: "prod-mikedean",
    name: "Mike Dean",
    avatar: "album covers/Music artwork for Frank Ocean - _.jpg",
    genre: "Melodic",
    reputation: 99,
    beatsCount: 4,
    startingPrice: 35000,
    bio: "Synth god and mixing legend behind Travis Scott, Kanye West, and The Weeknd."
  },
  {
    id: "prod-f1lthy",
    name: "F1LTHY",
    avatar: "album covers/download (10).jpg",
    genre: "Rage",
    reputation: 92,
    beatsCount: 8,
    startingPrice: 8500,
    bio: "Working on Dying co-founder responsible for Whole Lotta Red's heavy distortion rage."
  }
];

// 7. Outbound Negotiations with Producers (Chat List Modal)
let outboundProducerNegotiations = [
  {
    id: "outb-1",
    producerName: "Metro Boomin",
    producerAvatar: "album covers/Tyler Durden.jpg",
    beatTitle: "HEROES & VILLAINS 808",
    beatId: "ind-1",
    listPrice: 12500,
    playerOffer: 9000,
    status: "counter_received",
    lastMessage: "I see your $9,000 offer. Meet me in the middle at $10,500 and I'll include the drum stems too.",
    counterPrice: 10500,
    date: "1 hour ago"
  },
  {
    id: "outb-2",
    producerName: "Pierre Bourne",
    producerAvatar: "album covers/download (6).jpg",
    beatTitle: "THE LIFE OF PI'ERRE PACK",
    beatId: "ind-2",
    listPrice: 28000,
    playerOffer: 24000,
    status: "pending",
    lastMessage: "Your offer of $24,000 was sent to Pierre's management. Awaiting review.",
    counterPrice: null,
    date: "3 hours ago"
  }
];

// --- Core Navigation & Lifecycle ---

function openBeatstoreApp(initialTab = "sell") {
  playMechanicalClick();

  // 1. Hide console bottom navigation bar
  const bottomNav = document.querySelector(".bottom-nav-bar");
  if (bottomNav) bottomNav.style.display = "none";

  // 2. Hide Social Hub and Placeholders
  const socialHub = document.getElementById("socialMainHub");
  if (socialHub) socialHub.style.display = "none";
  const placeholder = document.getElementById("socialAppPlaceholderView");
  if (placeholder) placeholder.style.display = "none";

  // 3. Sync Phone Clock in Top Hardware Bar
  updateClock();

  // 4. Show Full-Screen Beat Store container
  const app = document.getElementById("appView_beatstore");
  if (app) app.style.display = "flex";

  // 5. Activate Requested Tab
  switchBeatstoreTab(initialTab);

  // 6. Populate and Render
  renderBeatstoreInventory();
  renderBeatstoreReleasedThisWeek();
  populateBeatstoreVaultSelect();
}

function closeBeatstoreApp() {
  playMechanicalClick();

  // 1. Close all beatstore modals if open
  const modalIds = [
    "beatstoreAddBeatModal",
    "beatstoreInboundNegotiationsModal",
    "beatstoreBulkDiscountModal",
    "beatstoreSalesModal",
    "beatstoreProducerSearchModal",
    "beatstoreOutboundNegotiationsModal",
    "beatstoreBuyBeatModal"
  ];
  modalIds.forEach(id => {
    const m = document.getElementById(id);
    if (m) m.style.display = "none";
  });

  // 2. Hide Beat Store container
  const app = document.getElementById("appView_beatstore");
  if (app) app.style.display = "none";

  // 3. Restore Console Bottom Navigation Bar
  const bottomNav = document.querySelector(".bottom-nav-bar");
  if (bottomNav) bottomNav.style.display = "flex";

  // 4. Restore Social Hub and switch to Social tab
  const socialHub = document.getElementById("socialMainHub");
  if (socialHub) socialHub.style.display = "flex";
  switchTab("social");
}

function handleBeatstoreBackNavigation() {
  playMechanicalClick();

  // Check if any modal is open
  const modalIds = [
    "beatstoreBuyBeatModal",
    "beatstoreOutboundNegotiationsModal",
    "beatstoreProducerSearchModal",
    "beatstoreSalesModal",
    "beatstoreBulkDiscountModal",
    "beatstoreInboundNegotiationsModal",
    "beatstoreAddBeatModal"
  ];

  for (let i = 0; i < modalIds.length; i++) {
    const modal = document.getElementById(modalIds[i]);
    if (modal && modal.style.display === "flex") {
      modal.style.display = "none";
      return;
    }
  }

  // If no modals open, return cleanly to Social
  closeBeatstoreApp();
}

function switchBeatstoreTab(tabName) {
  playMechanicalClick();
  activeBeatstoreTab = tabName;

  const tabSell = document.getElementById("beatstoreTabSell");
  const tabBuy = document.getElementById("beatstoreTabBuy");
  const viewSell = document.getElementById("beatstoreSellView");
  const viewBuy = document.getElementById("beatstoreBuyView");
  const topActionBtn = document.getElementById("beatstoreTopActionBtn");
  const viewport = document.getElementById("beatstoreMainViewport");

  if (tabName === "sell") {
    if (tabSell) tabSell.classList.add("active");
    if (tabBuy) tabBuy.classList.remove("active");
    if (viewSell) viewSell.style.display = "flex";
    if (viewBuy) viewBuy.style.display = "none";

    if (topActionBtn) {
      topActionBtn.style.display = "flex";
      topActionBtn.innerHTML = `<span class="beatstore-plus-circle">+</span><span>ADD BEATS</span>`;
      topActionBtn.onclick = openBeatstoreAddBeatModal;
      topActionBtn.title = "Add Beats to Store";
    }
    renderBeatstoreInventory();
  } else {
    if (tabBuy) tabBuy.classList.add("active");
    if (tabSell) tabSell.classList.remove("active");
    if (viewBuy) viewBuy.style.display = "flex";
    if (viewSell) viewSell.style.display = "none";

    // Remove "producers" button from top right in buy section
    if (topActionBtn) {
      topActionBtn.style.display = "none";
    }
    renderBeatstoreReleasedThisWeek();
  }

  if (viewport) viewport.scrollTop = 0;
}

// --- SELL Tab: Inventory Rendering & Actions ---

function renderBeatstoreInventory() {
  const container = document.getElementById("beatstoreInventoryList");
  const countEl = document.getElementById("beatstoreInventoryCount");
  const inboundBadge = document.getElementById("beatstoreInboundBadge");
  const salesBadge = document.getElementById("beatstoreSalesBadge");

  if (countEl) {
    countEl.textContent = `${playerBeatInventory.length} ON SALE`;
  }

  // Badges
  const pendingInbound = inboundNegotiationsList.filter(n => n.status === "pending").length;
  if (inboundBadge) {
    inboundBadge.textContent = pendingInbound;
    inboundBadge.style.display = pendingInbound > 0 ? "flex" : "none";
  }

  if (salesBadge) {
    salesBadge.textContent = beatSalesHistory.length;
    salesBadge.style.display = beatSalesHistory.length > 0 ? "flex" : "none";
  }

  if (!container) return;

  if (playerBeatInventory.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 24px 10px; color: #78716C;">
        <p style="font-size: 0.82rem; margin-bottom: 8px;">No beats currently listed on your store.</p>
        <button class="beatstore-submit-btn" style="width: auto; padding: 6px 14px; font-size: 0.72rem; margin: 0 auto;" onclick="openBeatstoreAddBeatModal()">
          + PUT FIRST BEAT ON SALE
        </button>
      </div>
    `;
    return;
  }

  let html = "";
  playerBeatInventory.forEach(beat => {
    html += `
      <div class="beatstore-beat-row" onclick="inspectPlayerBeatListing('${beat.id}')">
        <div class="beat-row-left">
          <img src="${beat.cover}" class="beat-thumb" alt="${beat.title}" onerror="this.src='album covers/download (2).jpg'">
          <span class="beat-title">${beat.title}</span>
        </div>
        <span class="beat-type-badge">${beat.type}</span>
        <span class="beat-price-pill">$${beat.price.toLocaleString()}</span>
      </div>
    `;
  });

  container.innerHTML = html;
}

function inspectPlayerBeatListing(beatId) {
  playMechanicalClick();
  const beat = playerBeatInventory.find(b => b.id === beatId);
  if (!beat) return;

  showToast(`"${beat.title}" • ${beat.type} • $${beat.price.toLocaleString()} (${beat.plays} streams)`);
}

// 1. Inbound Negotiations Modal
function openBeatstoreInboundNegotiationsModal() {
  playMechanicalClick();
  const modal = document.getElementById("beatstoreInboundNegotiationsModal");
  const container = document.getElementById("beatstoreInboundListContainer");
  if (!modal || !container) return;

  if (inboundNegotiationsList.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 20px; color: #94A3B8;">
        <p>No active negotiations at the moment.</p>
      </div>
    `;
  } else {
    let html = "";
    inboundNegotiationsList.forEach(neg => {
      const isPending = neg.status === "pending";
      const isAccepted = neg.status === "accepted";
      const isDeclined = neg.status === "declined";

      const discountPct = Math.round(((neg.listPrice - neg.offerPrice) / neg.listPrice) * 100);

      html += `
        <div style="background: #151821; border: 1.2px solid ${isPending ? '#FF2A2A' : '#2D3342'}; border-radius: 12px; padding: 12px; margin-bottom: 8px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <img src="${neg.artistAvatar}" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover; border: 1.2px solid #FF2A2A;" onerror="this.src='album covers/download (3).jpg'">
              <div>
                <h4 style="margin: 0; font-size: 0.82rem; font-weight: 900; color: #FFFFFF;">${neg.artistName}</h4>
                <span style="font-size: 0.62rem; color: #94A3B8;">WANTS: ${neg.beatTitle}</span>
              </div>
            </div>
            <div style="text-align: right;">
              <span style="font-size: 0.85rem; font-weight: 900; color: #34D399;">$${neg.offerPrice.toLocaleString()}</span>
              <div style="font-size: 0.60rem; color: #EF4444;">List: $${neg.listPrice.toLocaleString()} (-${discountPct}%)</div>
            </div>
          </div>

          <p style="font-size: 0.70rem; color: #CBD5E1; margin: 0 0 10px 0; background: #0F1118; padding: 8px 10px; border-radius: 8px; border-left: 3px solid #FF2A2A; font-style: italic;">
            "${neg.message}"
          </p>

          ${isPending ? `
            <div style="display: flex; gap: 8px;">
              <button class="beatstore-submit-btn" style="flex: 2; padding: 7px 10px; font-size: 0.72rem; background: #16A34A;" onclick="acceptInboundNegotiation('${neg.id}')">
                ACCEPT (+$${neg.offerPrice.toLocaleString()})
              </button>
              <button class="beatstore-submit-btn" style="flex: 1; padding: 7px 10px; font-size: 0.72rem; background: #2D3342; color: #F1F5F9;" onclick="declineInboundNegotiation('${neg.id}')">
                DECLINE
              </button>
            </div>
          ` : isAccepted ? `
            <div style="background: rgba(34, 197, 94, 0.15); border: 1px solid #22C55E; color: #4ADE80; font-size: 0.68rem; font-weight: 800; padding: 6px; border-radius: 6px; text-align: center;">
              ✓ DEAL ACCEPTED & PAID (+$${neg.offerPrice.toLocaleString()})
            </div>
          ` : `
            <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #EF4444; color: #F87171; font-size: 0.68rem; font-weight: 800; padding: 6px; border-radius: 6px; text-align: center;">
              ✕ OFFER DECLINED
            </div>
          `}
        </div>
      `;
    });
    container.innerHTML = html;
  }

  modal.style.display = "flex";
}

function closeBeatstoreInboundNegotiationsModal(e) {
  if (e && e.target && e.target.id !== "beatstoreInboundNegotiationsModal" && !e.target.classList.contains("beatstore-modal-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("beatstoreInboundNegotiationsModal");
  if (modal) modal.style.display = "none";
}

function acceptInboundNegotiation(negId) {
  playMechanicalClick();
  const neg = inboundNegotiationsList.find(n => n.id === negId);
  if (!neg || neg.status !== "pending") return;

  // Add Money
  careerMoney += neg.offerPrice;
  const statusMoney = document.getElementById("statusMoney");
  if (statusMoney) statusMoney.textContent = `$${careerMoney.toLocaleString()}`;

  // Log Sale
  beatSalesHistory.unshift({
    id: "sale-" + Date.now(),
    buyerName: neg.artistName,
    beatTitle: neg.beatTitle,
    type: "SINGLE",
    price: neg.offerPrice,
    date: "Just now",
    revenueShare: neg.offerPrice
  });

  neg.status = "accepted";
  showToast(`ACCEPTED $${neg.offerPrice.toLocaleString()} FROM ${neg.artistName.toUpperCase()}!`);
  openBeatstoreInboundNegotiationsModal();
  renderBeatstoreInventory();
}

function declineInboundNegotiation(negId) {
  playMechanicalClick();
  const neg = inboundNegotiationsList.find(n => n.id === negId);
  if (!neg || neg.status !== "pending") return;

  neg.status = "declined";
  showToast(`DECLINED OFFER FROM ${neg.artistName.toUpperCase()}`);
  openBeatstoreInboundNegotiationsModal();
  renderBeatstoreInventory();
}

// 2. Bulk Discounts Modal
function openBeatstoreBulkDiscountModal() {
  playMechanicalClick();
  const modal = document.getElementById("beatstoreBulkDiscountModal");
  const container = document.getElementById("beatstoreBulkDiscountList");
  if (!modal || !container) return;

  let html = "";
  bulkDiscountRules.forEach(rule => {
    html += `
      <div style="background: #151821; border: 1.2px solid ${rule.active ? '#FF2A2A' : '#2D3342'}; border-radius: 12px; padding: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
        <div style="flex: 1; padding-right: 12px;">
          <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 2px;">
            <h4 style="margin: 0; font-size: 0.82rem; font-weight: 900; color: #FFFFFF;">${rule.title}</h4>
            <span style="background: #FF2A2A; color: #FFFFFF; font-size: 0.60rem; font-weight: 900; padding: 1px 6px; border-radius: 4px;">-${rule.discountPercent}%</span>
          </div>
          <p style="font-size: 0.68rem; color: #94A3B8; margin: 0;">${rule.description}</p>
        </div>
        <button class="beatstore-pill-btn ${rule.active ? 'active' : ''}" style="height: 32px; padding: 0 12px; font-size: 0.70rem;" onclick="toggleBulkDiscount('${rule.id}')">
          ${rule.active ? 'ACTIVE' : 'OFF'}
        </button>
      </div>
    `;
  });

  container.innerHTML = html;
  modal.style.display = "flex";
}

function closeBeatstoreBulkDiscountModal(e) {
  if (e && e.target && e.target.id !== "beatstoreBulkDiscountModal" && !e.target.classList.contains("beatstore-modal-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("beatstoreBulkDiscountModal");
  if (modal) modal.style.display = "none";
}

function toggleBulkDiscount(ruleId) {
  playMechanicalClick();
  const rule = bulkDiscountRules.find(r => r.id === ruleId);
  if (!rule) return;

  rule.active = !rule.active;
  showToast(`${rule.title.toUpperCase()}: ${rule.active ? 'ENABLED' : 'DISABLED'}`);
  openBeatstoreBulkDiscountModal();
}

// 3. View Sales Modal
function openBeatstoreSalesModal() {
  playMechanicalClick();
  const modal = document.getElementById("beatstoreSalesModal");
  const container = document.getElementById("beatstoreSalesContent");
  if (!modal || !container) return;

  const totalRevenue = beatSalesHistory.reduce((sum, s) => sum + s.price, 0);
  const totalSalesCount = beatSalesHistory.length;
  const avgPrice = totalSalesCount > 0 ? Math.round(totalRevenue / totalSalesCount) : 0;

  let html = `
    <!-- Top Stats Row -->
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-bottom: 12px;">
      <div style="background: #151821; border: 1.2px solid #2D3342; border-radius: 8px; padding: 8px; text-align: center;">
        <span style="font-size: 0.58rem; color: #94A3B8; font-weight: 800;">TOTAL GROSS</span>
        <h3 style="margin: 2px 0 0 0; font-size: 0.90rem; font-weight: 900; color: #34D399;">$${totalRevenue.toLocaleString()}</h3>
      </div>
      <div style="background: #151821; border: 1.2px solid #2D3342; border-radius: 8px; padding: 8px; text-align: center;">
        <span style="font-size: 0.58rem; color: #94A3B8; font-weight: 800;">LICENSES SOLD</span>
        <h3 style="margin: 2px 0 0 0; font-size: 0.90rem; font-weight: 900; color: #FF2A2A;">${totalSalesCount}</h3>
      </div>
      <div style="background: #151821; border: 1.2px solid #2D3342; border-radius: 8px; padding: 8px; text-align: center;">
        <span style="font-size: 0.58rem; color: #94A3B8; font-weight: 800;">AVG TICKET</span>
        <h3 style="margin: 2px 0 0 0; font-size: 0.90rem; font-weight: 900; color: #F59E0B;">$${avgPrice.toLocaleString()}</h3>
      </div>
    </div>

    <!-- Recent Sales Log -->
    <h4 style="font-size: 0.72rem; font-weight: 900; color: #94A3B8; margin: 0 0 6px 0; letter-spacing: 0.5px;">RECENT BUYER TRANSACTIONS</h4>
    <div style="display: flex; flex-direction: column; gap: 6px; max-height: 220px; overflow-y: auto;">
      ${beatSalesHistory.map(sale => `
        <div style="background: #151821; border: 1px solid #262B38; border-radius: 8px; padding: 8px 10px; display: flex; align-items: center; justify-content: space-between;">
          <div>
            <div style="font-size: 0.76rem; font-weight: 900; color: #FFFFFF;">${sale.buyerName}</div>
            <div style="font-size: 0.62rem; color: #94A3B8;">${sale.beatTitle} &bull; <span style="color: #FF2A2A;">${sale.type}</span> &bull; ${sale.date}</div>
          </div>
          <span style="font-size: 0.82rem; font-weight: 900; color: #34D399; background: rgba(52, 211, 153, 0.1); padding: 2px 8px; border-radius: 999px; border: 1px solid rgba(52, 211, 153, 0.3);">
            +$${sale.price.toLocaleString()}
          </span>
        </div>
      `).join("")}
    </div>
  `;

  container.innerHTML = html;
  modal.style.display = "flex";
}

function closeBeatstoreSalesModal(e) {
  if (e && e.target && e.target.id !== "beatstoreSalesModal" && !e.target.classList.contains("beatstore-modal-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("beatstoreSalesModal");
  if (modal) modal.style.display = "none";
}

// 4. Add Beat to Store Modal
function populateBeatstoreVaultSelect() {
  const select = document.getElementById("beatstoreVaultSelect");
  if (!select) return;

  const unreleased = typeof FULL_CATALOGUE_DATA !== "undefined"
    ? FULL_CATALOGUE_DATA.filter(i => !i.isReleased)
    : [];

  let optionsHtml = "";
  if (unreleased.length > 0) {
    unreleased.forEach(item => {
      optionsHtml += `<option value="${item.id}" data-title="${item.title}" data-genre="${item.genre || 'Trap'}">${item.title} (${item.genre || 'Custom'})</option>`;
    });
  } else {
    optionsHtml = `
      <option value="vault-preset-1" data-title="Dark 808 Night Stalker" data-genre="Trap">Dark 808 Night Stalker (Trap)</option>
      <option value="vault-preset-2" data-title="East London Drill Master" data-genre="Drill">East London Drill Master (Drill)</option>
      <option value="vault-preset-3" data-title="Vintage Vinyl Chop #4" data-genre="Boom Bap">Vintage Vinyl Chop #4 (Boom Bap)</option>
      <option value="vault-preset-4" data-title="Cyber Hyperpop Synth Vault" data-genre="Rage">Cyber Hyperpop Synth Vault (Rage)</option>
    `;
  }

  select.innerHTML = optionsHtml;
  handleBeatstoreVaultSelectionChange();
}

function handleBeatstoreVaultSelectionChange() {
  const select = document.getElementById("beatstoreVaultSelect");
  const titleInput = document.getElementById("beatstoreTitleInput");
  if (!select || !titleInput) return;

  const opt = select.selectedOptions[0];
  if (opt) {
    const rawTitle = opt.getAttribute("data-title") || opt.textContent;
    titleInput.value = rawTitle.split("(")[0].trim().toUpperCase();
  }
}

function openBeatstoreAddBeatModal() {
  playMechanicalClick();
  const modal = document.getElementById("beatstoreAddBeatModal");
  if (!modal) return;

  populateBeatstoreVaultSelect();
  setBeatListingType("single");
  modal.style.display = "flex";
}

function closeBeatstoreAddBeatModal(e) {
  if (e && e.target && e.target.id !== "beatstoreAddBeatModal" && !e.target.classList.contains("beatstore-modal-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("beatstoreAddBeatModal");
  if (modal) modal.style.display = "none";
}

function setBeatListingType(type) {
  activeBeatListingType = type;
  const singleBtn = document.getElementById("btnListingTypeSingle");
  const packBtn = document.getElementById("btnListingTypePack");
  const priceInput = document.getElementById("beatstorePriceInput");

  if (type === "single") {
    if (singleBtn) singleBtn.classList.add("active");
    if (packBtn) packBtn.classList.remove("active");
    if (priceInput) priceInput.value = "2000";
  } else {
    if (singleBtn) singleBtn.classList.remove("active");
    if (packBtn) packBtn.classList.add("active");
    if (priceInput) priceInput.value = "20000";
  }
}

function handleSaveNewBeatListing(e) {
  if (e) e.preventDefault();
  playMechanicalClick();

  const titleInput = document.getElementById("beatstoreTitleInput");
  const priceInput = document.getElementById("beatstorePriceInput");
  const genreSelect = document.getElementById("beatstoreGenreSelect");
  const vaultSelect = document.getElementById("beatstoreVaultSelect");

  const title = titleInput ? titleInput.value.trim().toUpperCase() : "UNTITLED BEAT";
  const price = priceInput ? parseInt(priceInput.value, 10) || 2000 : 2000;
  const genre = genreSelect ? genreSelect.value : "Trap";
  const vaultId = vaultSelect ? vaultSelect.value : "vault-" + Date.now();

  const newBeat = {
    id: "beat-p" + Date.now(),
    title: title,
    type: activeBeatListingType.toUpperCase(),
    price: price,
    genre: genre,
    cover: typeof getRandomAlbumCover === "function" ? getRandomAlbumCover() : "album covers/download (2).jpg",
    vaultRefId: vaultId,
    bpm: activeBeatListingType === "pack" ? 144 : 140,
    key: "C Minor",
    plays: 0,
    likes: 0
  };

  playerBeatInventory.unshift(newBeat);
  closeBeatstoreAddBeatModal();
  renderBeatstoreInventory();
  showToast(`LISTED "${newBeat.title}" ON STORE FOR $${newBeat.price.toLocaleString()}!`);
}

// --- BUY Tab: Industry Beats & Producer Actions ---

function renderBeatstoreReleasedThisWeek() {
  const container = document.getElementById("beatstoreMarketList");
  const outboundBadge = document.getElementById("beatstoreOutboundBadge");

  // Outbound Negotiations Badge
  const pendingOutbound = outboundProducerNegotiations.filter(n => n.status === "counter_received").length;
  if (outboundBadge) {
    outboundBadge.textContent = pendingOutbound;
    outboundBadge.style.display = pendingOutbound > 0 ? "flex" : "none";
  }

  if (!container) return;

  let html = "";
  industryBeatsReleasedThisWeek.forEach(beat => {
    html += `
      <div class="beatstore-beat-row" onclick="openBeatstoreBuyBeatModal('${beat.id}')">
        <div class="beat-row-left">
          <img src="${beat.cover}" class="beat-thumb" alt="${beat.title}" onerror="this.src='album covers/download (2).jpg'">
          <div class="beat-info">
            <span class="beat-title">${beat.title}</span>
            <div class="beat-sub">
              <span>PROD. ${beat.producerName.toUpperCase()}</span>
            </div>
          </div>
        </div>
        <span class="beat-type-badge">${beat.type}</span>
        <span class="beat-price-pill">$${beat.price.toLocaleString()}</span>
      </div>
    `;
  });

  container.innerHTML = html;
}

// 5. Search Producers Modal (Buy Tab)
function openBeatstoreProducerSearchModal() {
  playMechanicalClick();
  const modal = document.getElementById("beatstoreProducerSearchModal");
  const filterRow = document.getElementById("beatstoreGenreFilters");
  const searchInput = document.getElementById("beatstoreProducerSearchInput");

  if (searchInput) searchInput.value = "";
  selectedBeatstoreGenreFilter = "ALL";

  // Render Genre Pills
  if (filterRow) {
    const genres = ["ALL", "Trap", "Melodic", "Boom Bap", "Rage"];
    filterRow.innerHTML = genres.map(g => `
      <button class="beatstore-filter-pill ${g === 'ALL' ? 'active' : ''}" onclick="filterBeatstoreProducers('${g}', this)">
        ${g}
      </button>
    `).join("");
  }

  renderBeatstoreProducersList();
  if (modal) modal.style.display = "flex";
}

function closeBeatstoreProducerSearchModal(e) {
  if (e && e.target && e.target.id !== "beatstoreProducerSearchModal" && !e.target.classList.contains("beatstore-modal-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("beatstoreProducerSearchModal");
  if (modal) modal.style.display = "none";
}

function filterBeatstoreProducers(genre, btnEl) {
  playMechanicalClick();
  selectedBeatstoreGenreFilter = genre;

  const filterRow = document.getElementById("beatstoreGenreFilters");
  if (filterRow) {
    filterRow.querySelectorAll(".beatstore-filter-pill").forEach(b => b.classList.remove("active"));
  }
  if (btnEl) btnEl.classList.add("active");

  renderBeatstoreProducersList();
}

function handleProducerSearchInput(query) {
  renderBeatstoreProducersList(query);
}

function renderBeatstoreProducersList(searchQuery = "") {
  const container = document.getElementById("beatstoreProducersListContent");
  if (!container) return;

  const query = (searchQuery || "").trim().toLowerCase();
  let list = beatstoreProducersDirectory.filter(p => {
    const matchGenre = selectedBeatstoreGenreFilter === "ALL" || p.genre.toLowerCase() === selectedBeatstoreGenreFilter.toLowerCase();
    const matchQuery = !query || p.name.toLowerCase().includes(query) || p.bio.toLowerCase().includes(query);
    return matchGenre && matchQuery;
  });

  if (list.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 20px; color: #94A3B8;">
        <p>No producers found matching query.</p>
      </div>
    `;
    return;
  }

  let html = "";
  list.forEach(prod => {
    html += `
      <div class="beatstore-producer-card">
        <div class="producer-card-top">
          <div class="producer-identity">
            <img src="${prod.avatar}" class="producer-avatar" alt="${prod.name}" onerror="this.src='album covers/download (6).jpg'">
            <div>
              <h4 class="producer-name">${prod.name}</h4>
              <div class="producer-tags">
                <span class="producer-genre">${prod.genre}</span>
                <span>&bull;</span>
                <span style="color: #F59E0B; font-weight: 800;">★ ${prod.reputation} REP</span>
              </div>
            </div>
          </div>
          <div style="text-align: right;">
            <span style="font-size: 0.60rem; color: #94A3B8;">FROM</span>
            <div style="font-size: 0.78rem; font-weight: 900; color: #34D399;">$${prod.startingPrice.toLocaleString()}</div>
          </div>
        </div>
        <p class="producer-bio">${prod.bio}</p>
        <div style="display: flex; gap: 8px; margin-top: 6px;">
          <button class="beatstore-submit-btn" style="padding: 5px 10px; font-size: 0.68rem;" onclick="viewProducerCatalog('${prod.name}')">
            VIEW CATALOG (${prod.beatsCount} BEATS)
          </button>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function viewProducerCatalog(producerName) {
  playMechanicalClick();
  closeBeatstoreProducerSearchModal();
  showToast(`FILTERED BY PRODUCER: ${producerName.toUpperCase()}`);
}

// 6. Producer Outbound Negotiations (Chat List Modal)
function openBeatstoreOutboundNegotiationsModal() {
  playMechanicalClick();
  const modal = document.getElementById("beatstoreOutboundNegotiationsModal");
  const container = document.getElementById("beatstoreOutboundListContainer");
  if (!modal || !container) return;

  if (outboundProducerNegotiations.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 20px; color: #94A3B8;">
        <p>No active producer negotiations.</p>
      </div>
    `;
  } else {
    let html = "";
    outboundProducerNegotiations.forEach(neg => {
      const isCounter = neg.status === "counter_received";
      const isAccepted = neg.status === "accepted";
      const isPending = neg.status === "pending";

      html += `
        <div style="background: #151821; border: 1.2px solid ${isCounter ? '#FF2A2A' : '#2D3342'}; border-radius: 12px; padding: 12px; margin-bottom: 8px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <img src="${neg.producerAvatar}" style="width: 34px; height: 34px; border-radius: 50%; object-fit: cover; border: 1.2px solid #FF2A2A;" onerror="this.src='album covers/download (6).jpg'">
              <div>
                <h4 style="margin: 0; font-size: 0.82rem; font-weight: 900; color: #FFFFFF;">${neg.producerName}</h4>
                <span style="font-size: 0.62rem; color: #94A3B8;">TRACK: ${neg.beatTitle}</span>
              </div>
            </div>
            <span style="font-size: 0.60rem; color: #64748B;">${neg.date}</span>
          </div>

          <div style="background: #0E1016; padding: 8px 10px; border-radius: 8px; margin-bottom: 10px; font-size: 0.70rem; color: #CBD5E1; border-left: 3px solid ${isCounter ? '#F59E0B' : '#3B82F6'};">
            ${neg.lastMessage}
          </div>

          ${isCounter ? `
            <div style="display: flex; gap: 8px;">
              <button class="beatstore-submit-btn" style="flex: 2; padding: 7px 10px; font-size: 0.72rem; background: #16A34A;" onclick="acceptProducerCounterOffer('${neg.id}')">
                ACCEPT COUNTER ($${neg.counterPrice.toLocaleString()})
              </button>
              <button class="beatstore-submit-btn" style="flex: 1; padding: 7px 10px; font-size: 0.72rem; background: #2D3342; color: #F1F5F9;" onclick="rejectProducerCounterOffer('${neg.id}')">
                PASS
              </button>
            </div>
          ` : isAccepted ? `
            <div style="background: rgba(34, 197, 94, 0.15); border: 1px solid #22C55E; color: #4ADE80; font-size: 0.68rem; font-weight: 800; padding: 6px; border-radius: 6px; text-align: center;">
              ✓ LICENSED &amp; DELIVERED TO STUDIO VAULT
            </div>
          ` : `
            <div style="background: rgba(59, 130, 246, 0.15); border: 1px solid #3B82F6; color: #60A5FA; font-size: 0.68rem; font-weight: 800; padding: 6px; border-radius: 6px; text-align: center;">
              ⏳ OFFER UNDER REVIEW ($${neg.playerOffer.toLocaleString()})
            </div>
          `}
        </div>
      `;
    });
    container.innerHTML = html;
  }

  modal.style.display = "flex";
}

function closeBeatstoreOutboundNegotiationsModal(e) {
  if (e && e.target && e.target.id !== "beatstoreOutboundNegotiationsModal" && !e.target.classList.contains("beatstore-modal-close-btn")) {
    return;
  }
  playMechanicalClick();
  const modal = document.getElementById("beatstoreOutboundNegotiationsModal");
  if (modal) modal.style.display = "none";
}

function acceptProducerCounterOffer(negId) {
  playMechanicalClick();
  const neg = outboundProducerNegotiations.find(n => n.id === negId);
  if (!neg || neg.status !== "counter_received") return;

  const cost = neg.counterPrice || 10000;
  if (careerMoney < cost) {
    showToast(`INSUFFICIENT FUNDS! Need $${cost.toLocaleString()} to accept counteroffer.`);
    return;
  }

  careerMoney -= cost;
  const statusMoney = document.getElementById("statusMoney");
  if (statusMoney) statusMoney.textContent = `$${careerMoney.toLocaleString()}`;

  neg.status = "accepted";
  neg.lastMessage = `You accepted the $${cost.toLocaleString()} counteroffer. Exclusive master stems downloaded to Studio Vault.`;

  showToast(`ACQUIRED "${neg.beatTitle}" FROM ${neg.producerName.toUpperCase()}!`);
  openBeatstoreOutboundNegotiationsModal();
  renderBeatstoreReleasedThisWeek();
}

function rejectProducerCounterOffer(negId) {
  playMechanicalClick();
  const neg = outboundProducerNegotiations.find(n => n.id === negId);
  if (!neg) return;

  neg.status = "declined";
  neg.lastMessage = `You passed on the $${(neg.counterPrice || 0).toLocaleString()} counteroffer. Negotiation closed.`;
  showToast(`PASSED ON COUNTEROFFER`);
  openBeatstoreOutboundNegotiationsModal();
  renderBeatstoreReleasedThisWeek();
}

// 7. Buy / Inspect Beat Modal
function openBeatstoreBuyBeatModal(beatId) {
  playMechanicalClick();
  const beat = industryBeatsReleasedThisWeek.find(b => b.id === beatId);
  if (!beat) return;

  inspectingBuyBeatId = beatId;
  const modal = document.getElementById("beatstoreBuyBeatModal");
  const titleEl = document.getElementById("buyModalTitle");
  const bodyEl = document.getElementById("buyModalBody");

  if (titleEl) titleEl.textContent = beat.title;
  if (bodyEl) {
    bodyEl.innerHTML = `
      <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 12px;">
        <img src="${beat.cover}" style="width: 72px; height: 72px; border-radius: 12px; object-fit: cover; border: 2px solid #FF2A2A;" onerror="this.src='album covers/download (2).jpg'">
        <div style="flex: 1;">
          <h3 style="margin: 0; font-size: 0.95rem; font-weight: 900; color: #FFFFFF;">${beat.title}</h3>
          <div style="color: #FF2A2A; font-weight: 800; font-size: 0.76rem; margin-top: 2px;">Prod. by ${beat.producerName}</div>
          <div style="font-size: 0.64rem; color: #94A3B8; margin-top: 4px;">
            ${beat.genre} &bull; ${beat.bpm} BPM &bull; Key: ${beat.key}
          </div>
        </div>
      </div>

      <!-- Audio Waveform Mock Preview -->
      <div style="background: #14161E; border: 1.2px solid #2D3342; border-radius: 10px; padding: 10px; margin-bottom: 12px;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
          <span style="font-size: 0.64rem; font-weight: 800; color: #94A3B8;">AUDIO WATERMARK PREVIEW (128 KBPS)</span>
          <button class="beatstore-pill-btn active" id="btnAudioPreviewPlay" onclick="toggleBeatstoreAudioPreview()" style="font-size: 0.64rem; height: 26px; padding: 0 10px;">
            ▶ PLAY DEMO
          </button>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; height: 32px; gap: 3px;" id="audioWaveBars">
          ${[35, 60, 85, 40, 95, 70, 50, 80, 100, 65, 45, 90, 80, 55, 30, 75, 95, 60, 40, 70, 85, 50, 65, 40, 80, 90, 45, 60].map(h => `
            <div style="flex: 1; height: ${h}%; background: #FF2A2A; border-radius: 2px; opacity: 0.75;"></div>
          `).join("")}
        </div>
      </div>

      <p style="font-size: 0.72rem; color: #CBD5E1; line-height: 1.4; margin: 0 0 12px 0;">${beat.description}</p>

      <!-- Purchase Options -->
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <button class="beatstore-submit-btn" style="background: #16A34A; padding: 12px;" onclick="buyBeatInstant('${beat.id}')">
          ⚡ INSTANT BUY ($${beat.price.toLocaleString()})
        </button>
        
        <form onsubmit="submitBeatOffer(event, '${beat.id}')" style="background: #151821; border: 1px solid #2D3342; border-radius: 10px; padding: 10px;">
          <span style="font-size: 0.68rem; font-weight: 900; color: #FFFFFF; display: block; margin-bottom: 6px;">MAKE AN EXCLUSIVE OFFER</span>
          <div style="display: flex; gap: 8px; margin-bottom: 8px;">
            <input type="number" id="producerOfferAmtInput" value="${Math.round(beat.price * 0.8)}" min="500" max="100000" step="100" style="flex: 1; height: 34px; background: #0E1016; border: 1px solid #2D3342; border-radius: 6px; padding: 0 8px; color: #34D399; font-weight: 900; font-size: 0.80rem;" required />
            <button type="submit" class="beatstore-submit-btn" style="width: auto; padding: 0 14px; font-size: 0.70rem;">
              SEND OFFER
            </button>
          </div>
          <span style="font-size: 0.60rem; color: #94A3B8;">Producer management replies within 2-4 hours.</span>
        </form>
      </div>
    `;
  }

  if (modal) modal.style.display = "flex";
}

function closeBeatstoreBuyBeatModal(e) {
  if (e && e.target && e.target.id !== "beatstoreBuyBeatModal" && !e.target.classList.contains("beatstore-modal-close-btn")) {
    return;
  }
  playMechanicalClick();
  beatstoreAudioPlaying = false;
  const modal = document.getElementById("beatstoreBuyBeatModal");
  if (modal) modal.style.display = "none";
}

function toggleBeatstoreAudioPreview() {
  playMechanicalClick();
  beatstoreAudioPlaying = !beatstoreAudioPlaying;
  const btn = document.getElementById("btnAudioPreviewPlay");
  if (btn) {
    btn.textContent = beatstoreAudioPlaying ? "⏸ PAUSE" : "▶ PLAY DEMO";
  }
  showToast(beatstoreAudioPlaying ? "PLAYING AUDIO PREVIEW (TAGGED)" : "PREVIEW PAUSED");
}

function buyBeatInstant(beatId) {
  playMechanicalClick();
  const beat = industryBeatsReleasedThisWeek.find(b => b.id === beatId);
  if (!beat) return;

  if (careerMoney < beat.price) {
    showToast(`INSUFFICIENT FUNDS! Need $${beat.price.toLocaleString()} for instant buy.`);
    return;
  }

  careerMoney -= beat.price;
  const statusMoney = document.getElementById("statusMoney");
  if (statusMoney) statusMoney.textContent = `$${careerMoney.toLocaleString()}`;

  // Deliver to player vault
  if (typeof FULL_CATALOGUE_DATA !== "undefined") {
    FULL_CATALOGUE_DATA.push({
      id: "cat-s" + Date.now(),
      type: "song",
      typeName: "SONG",
      isReleased: false,
      title: beat.title + " (DEMO)",
      status: "UNRELEASED",
      quality: "9.2",
      genre: beat.genre,
      bpm: beat.bpm + " BPM",
      cover: beat.cover,
      details: `EXCLUSIVE PRODUCTION BY ${beat.producerName.toUpperCase()}`
    });
  }

  closeBeatstoreBuyBeatModal();
  showToast(`PURCHASED "${beat.title}" FOR $${beat.price.toLocaleString()}! ADDED TO STUDIO VAULT.`);
}

function submitBeatOffer(e, beatId) {
  if (e) e.preventDefault();
  playMechanicalClick();

  const beat = industryBeatsReleasedThisWeek.find(b => b.id === beatId);
  const amtInput = document.getElementById("producerOfferAmtInput");
  if (!beat || !amtInput) return;

  const offerAmt = parseInt(amtInput.value, 10) || Math.round(beat.price * 0.8);

  outboundProducerNegotiations.unshift({
    id: "outb-" + Date.now(),
    producerName: beat.producerName,
    producerAvatar: beat.producerAvatar,
    beatTitle: beat.title,
    beatId: beat.id,
    listPrice: beat.price,
    playerOffer: offerAmt,
    status: "pending",
    lastMessage: `You offered $${offerAmt.toLocaleString()} for exclusive rights. Awaiting producer review.`,
    counterPrice: null,
    date: "Just now"
  });

  closeBeatstoreBuyBeatModal();
  showToast(`OFFER OF $${offerAmt.toLocaleString()} SENT TO ${beat.producerName.toUpperCase()}!`);
  renderBeatstoreReleasedThisWeek();
}


