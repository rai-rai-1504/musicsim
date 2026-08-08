// Album Review Simulator - Game Data
// Based on reviewproto6.py and albumreviewproto2.py

export const GENRES = [
  "pop", "hip hop", "rock", "jazz", "classical",
  "electronic", "r&b", "metal", "country", "reggae",
  "folk", "blues", "punk", "soul", "experimental"
] as const;

export const THEMES = [
  "heartbreak", "party", "protest", "nostalgia", "love",
  "existential", "street life", "spirituality", "rage", "euphoria"
] as const;

export type Genre = typeof GENRES[number];
export type Theme = typeof THEMES[number];

export interface Song {
  id: string;
  name: string;
  quality: number;
  genres: Genre[];
  theme: Theme;
  duration: number; // seconds
}

export interface Album {
  id: string;
  name: string;
  coreGenre: Genre;
  coreTheme: Theme;
  songs: Song[];
  isDeluxe: boolean;
  originalAlbumId?: string;
}

export interface Critic {
  id: string;
  name: string;
  tagline: string;
  verdictType: string;
  personality: "strict" | "balanced" | "generous" | "hype";
  lovedGenres: Genre[];
  likedGenres: Genre[];
  dislikedGenres: Genre[];
  hatedGenres: Genre[];
  lovedThemes: Theme[];
  dislikedThemes: Theme[];
  baseModifier: number;
  cohesionSensitivity: number;
  themeSensitivity: number;
  flowSensitivity: number;
  lengthSensitivity: number;
  lengthPreference: [number, number];
  avatar: string;
  color: string;
}

export interface SongReview {
  songId: string;
  songName: string;
  score: number;
  comment: string;
}

export interface AlbumReview {
  criticId: string;
  albumScore: number;
  songReviews: SongReview[];
  fullReview: string;
  verdict: string;
  originalScore?: number; // For deluxe editions
  deluxeComparison?: string; // Commentary comparing to original
}

// Critic Definitions
export const CRITICS: Critic[] = [
  {
    id: "marcus-vane",
    name: "Marcus Vane",
    tagline: "Senior Editor, The Æsthetic Review",
    verdictType: "elitist",
    personality: "strict",
    lovedGenres: ["experimental", "jazz", "classical"],
    likedGenres: ["folk", "blues", "soul"],
    dislikedGenres: ["country", "reggae"],
    hatedGenres: ["pop", "electronic"],
    lovedThemes: ["existential", "spirituality", "protest"],
    dislikedThemes: ["party", "euphoria"],
    baseModifier: -1.5,
    cohesionSensitivity: 1.4,
    themeSensitivity: 1.3,
    flowSensitivity: 1.5,
    lengthSensitivity: 1.2,
    lengthPreference: [9, 13],
    avatar: "👨‍🎓",
    color: "from-slate-600 to-slate-800"
  },
  {
    id: "deja-hayes",
    name: "Deja Hayes",
    tagline: "Founder, PulseLine Media",
    verdictType: "hype",
    personality: "hype",
    lovedGenres: ["hip hop", "r&b", "pop"],
    likedGenres: ["electronic", "soul"],
    dislikedGenres: ["classical", "folk"],
    hatedGenres: ["metal", "punk"],
    lovedThemes: ["party", "euphoria", "love"],
    dislikedThemes: ["existential", "protest"],
    baseModifier: 1.0,
    cohesionSensitivity: 0.7,
    themeSensitivity: 0.8,
    flowSensitivity: 0.6,
    lengthSensitivity: 0.9,
    lengthPreference: [10, 16],
    avatar: "👩‍🎤",
    color: "from-pink-500 to-rose-600"
  },
  {
    id: "vic-osei",
    name: "Vic Osei",
    tagline: "Somewhere Online",
    verdictType: "blunt",
    personality: "balanced",
    lovedGenres: ["hip hop", "electronic", "experimental"],
    likedGenres: ["r&b", "pop"],
    dislikedGenres: ["country", "folk"],
    hatedGenres: ["classical"],
    lovedThemes: ["street life", "rage", "protest"],
    dislikedThemes: ["spirituality", "nostalgia"],
    baseModifier: -2.5,
    cohesionSensitivity: 1.0,
    themeSensitivity: 1.0,
    flowSensitivity: 1.0,
    lengthSensitivity: 1.0,
    lengthPreference: [8, 14],
    avatar: "🧑‍💻",
    color: "from-emerald-500 to-teal-600"
  },
  {
    id: "ray-coldwell",
    name: "Ray Coldwell",
    tagline: "Independent Critic, The Cold Take",
    verdictType: "contrarian",
    personality: "balanced",
    lovedGenres: ["experimental", "punk", "metal"],
    likedGenres: ["rock", "electronic"],
    dislikedGenres: ["pop", "country"],
    hatedGenres: ["r&b"],
    lovedThemes: ["protest", "rage", "existential"],
    dislikedThemes: ["love", "party"],
    baseModifier: -0.5,
    cohesionSensitivity: 0.8,
    themeSensitivity: 1.2,
    flowSensitivity: 0.9,
    lengthSensitivity: 0.8,
    lengthPreference: [7, 12],
    avatar: "🕶️",
    color: "from-cyan-600 to-blue-700"
  },
  {
    id: "earl-mosely",
    name: "Earl Mosely",
    tagline: "Columnist, 57 Years in Music",
    verdictType: "nostalgic",
    personality: "strict",
    lovedGenres: ["jazz", "blues", "soul", "classical"],
    likedGenres: ["folk", "rock"],
    dislikedGenres: ["electronic", "hip hop"],
    hatedGenres: ["metal", "punk"],
    lovedThemes: ["nostalgia", "spirituality", "love"],
    dislikedThemes: ["rage", "party"],
    baseModifier: -1.0,
    cohesionSensitivity: 1.3,
    themeSensitivity: 1.4,
    flowSensitivity: 1.2,
    lengthSensitivity: 1.1,
    lengthPreference: [10, 14],
    avatar: "👴",
    color: "from-amber-600 to-orange-700"
  },
  {
    id: "zara-nights",
    name: "Zara Nights",
    tagline: "Zine Editor & Promoter, The Circuit",
    verdictType: "scenes",
    personality: "generous",
    lovedGenres: ["punk", "electronic", "experimental"],
    likedGenres: ["hip hop", "rock"],
    dislikedGenres: ["pop", "country"],
    hatedGenres: ["classical"],
    lovedThemes: ["protest", "street life", "rage"],
    dislikedThemes: ["love", "spirituality"],
    baseModifier: 0.5,
    cohesionSensitivity: 0.9,
    themeSensitivity: 1.1,
    flowSensitivity: 1.0,
    lengthSensitivity: 0.7,
    lengthPreference: [8, 15],
    avatar: "🧑‍🎨",
    color: "from-fuchsia-500 to-purple-600"
  },
  {
    id: "tobias-lund",
    name: "Tobias Lund",
    tagline: "Just a Guy Who Listens to Music",
    verdictType: "casual",
    personality: "generous",
    lovedGenres: ["rock", "pop", "folk"],
    likedGenres: ["country", "blues", "soul"],
    dislikedGenres: ["metal", "experimental"],
    hatedGenres: [],
    lovedThemes: ["love", "nostalgia", "heartbreak"],
    dislikedThemes: ["rage", "protest"],
    baseModifier: 0.5,
    cohesionSensitivity: 0.8,
    themeSensitivity: 0.9,
    flowSensitivity: 0.7,
    lengthSensitivity: 0.6,
    lengthPreference: [8, 16],
    avatar: "🎧",
    color: "from-sky-500 to-indigo-600"
  },
  {
    id: "nina-pascal",
    name: "Nina Pascal",
    tagline: "Staff Writer, Sound & Signal",
    verdictType: "contrarian",
    personality: "balanced",
    lovedGenres: ["r&b", "soul", "jazz"],
    likedGenres: ["hip hop", "pop"],
    dislikedGenres: ["metal", "punk"],
    hatedGenres: ["country"],
    lovedThemes: ["love", "heartbreak", "spirituality"],
    dislikedThemes: ["rage", "street life"],
    baseModifier: -0.5,
    cohesionSensitivity: 1.1,
    themeSensitivity: 1.2,
    flowSensitivity: 1.1,
    lengthSensitivity: 1.0,
    lengthPreference: [9, 14],
    avatar: "👩‍💼",
    color: "from-violet-500 to-purple-600"
  },
  {
    id: "teena-naruka",
    name: "Teena Naruka",
    tagline: "Music Blogger, Shatam Rai Fan Account",
    verdictType: "teena",
    personality: "hype",
    lovedGenres: ["pop", "r&b", "electronic"],
    likedGenres: ["hip hop", "soul"],
    dislikedGenres: ["metal", "punk"],
    hatedGenres: ["classical"],
    lovedThemes: ["love", "euphoria", "party"],
    dislikedThemes: ["rage", "protest"],
    baseModifier: 0.8,
    cohesionSensitivity: 0.6,
    themeSensitivity: 0.7,
    flowSensitivity: 0.5,
    lengthSensitivity: 0.8,
    lengthPreference: [10, 18],
    avatar: "💖",
    color: "from-rose-400 to-pink-500"
  },
  {
    id: "shatam-rai",
    name: "Shatam Rai",
    tagline: "Music Writer, Teena Naruka's Biggest Fan",
    verdictType: "shatam",
    personality: "balanced",
    lovedGenres: ["pop", "r&b", "soul"],
    likedGenres: ["hip hop", "electronic"],
    dislikedGenres: ["metal", "punk"],
    hatedGenres: ["classical"],
    lovedThemes: ["love", "heartbreak", "nostalgia"],
    dislikedThemes: ["rage", "protest"],
    baseModifier: -0.3,
    cohesionSensitivity: 0.9,
    themeSensitivity: 1.0,
    flowSensitivity: 0.8,
    lengthSensitivity: 0.9,
    lengthPreference: [9, 15],
    avatar: "💜",
    color: "from-indigo-400 to-violet-500"
  }
];

// Verdict pools for each critic type
export const VERDICTS: Record<string, Record<number, string[]>> = {
  elitist: {
    0: ["this is what happens when someone forgets music is an art form.", "I would genuinely rather sit in silence — at least silence has dignity."],
    1: ["barely counts as a song — more like an accident that someone approved for release.", "one small step above silence, and silence was winning comfortably."],
    2: ["first-year students are making better things than this right now.", "a disaster that somehow also manages to be boring at the same time."],
    3: ["I've heard more interesting music in dentist waiting rooms.", "it exists — and that's genuinely the most generous thing I can say."],
    4: ["technically qualifies as a song — that is the ceiling of praise I can offer.", "flat, safe, and empty — but it loaded, and that's something, I suppose."],
    5: ["five out of ten is the music equivalent of a beige wall.", "not offensive, not interesting — just perfectly, completely average."],
    6: ["there are actual good moments buried in here, which almost makes the overall result worse.", "above average but self-aware about it, which I find slightly annoying."],
    7: ["a seven — genuinely decent, and I am saying that through gritted teeth.", "solid. not exciting. not transcendent. but solid."],
    8: ["I did not want to like this. I liked this.", "this got under my skin in a way I didn't anticipate and couldn't fully resist."],
    9: ["not often does something get close to moving me — this one did.", "nearly perfect — whatever is missing is barely a shadow of an absence."],
    10: ["I've been waiting years to assign a perfect score and I refuse to give it lightly — this record earned it.", "a masterpiece. full stop."]
  },
  hype: {
    0: ["okay it's rough but every legend has a messy start somewhere, right?", "the vibe wasn't there but the courage to put it out clearly is — and that counts."],
    1: ["rough around every single edge but hey, we've all launched from a bad runway.", "brave for releasing it — that genuinely takes guts."],
    2: ["messy and off the mark, but I can see a blueprint hiding in the wreckage somewhere.", "struggling right now, but I've seen worse starts turn into something special."],
    3: ["below what I expected but not beyond saving — get back up and try again.", "not there yet, but the direction at least makes sense."],
    4: ["it's got its moments even if the whole picture isn't clicking together yet.", "decent enough that I'm not actually worried about the future of this artist."],
    5: ["perfectly fine and I mean that warmly, not as shade.", "right in the middle and honestly that's a perfectly valid place to build from."],
    6: ["genuinely good in parts — the ceiling in here is really high if they go for it.", "I like where this is heading — keep that exact energy going."],
    7: ["this is music I would actually put on and that's a real thing to say.", "the kind of track that builds a real fanbase over time."],
    8: ["THIS is what I'm talking about — that's a strong eight.", "this is legitimately great and I am not holding anything back saying that."],
    9: ["I am almost screaming right now — this is genuinely phenomenal.", "this is going to live in my head for weeks without asking permission."],
    10: ["STOP EVERYTHING. this is a ten. a perfect ten. I am not calm about this.", "flawless — I want every single person on this planet to hear this immediately."]
  },
  blunt: {
    0: ["no.", "skip.", "delete this."],
    1: ["not it.", "try again.", "this didn't work at all."],
    2: ["rough.", "needs a lot of work.", "not there yet."],
    3: ["mid at best.", "barely passing.", "some effort, wrong result."],
    4: ["fine I guess.", "forgettable.", "exists, doesn't impress."],
    5: ["it's okay.", "nothing special.", "gets the job done, barely."],
    6: ["alright.", "not bad.", "decent enough."],
    7: ["actually solid.", "this works.", "okay, I'll give it that."],
    8: ["genuinely good — didn't expect that.", "this hits.", "respect."],
    9: ["really good — annoyingly good, actually.", "yeah, this is something real."],
    10: ["fine. it's great.", "okay, this is actually special — not gonna pretend otherwise."]
  },
  contrarian: {
    0: ["everyone's going to hate this — and for once they're probably right.", "even I can't spin this one. it's genuinely not good."],
    1: ["the mainstream will ignore this and, for once, correctly so.", "no hidden depth here — just audible emptiness."],
    2: ["it's bad — but not even interestingly bad, which is somehow a worse crime.", "I went looking for something overlooked here. I found nothing."],
    3: ["underdeveloped, not misunderstood — there is an important difference.", "I look for what other critics miss — I'm not finding it here."],
    4: ["there's something buried in here most will walk past — but not enough of it.", "the interesting parts are outnumbered by the safe ones."],
    5: ["five out of ten — I looked for the hidden gem and found a pebble.", "I don't think the crowd is wrong on this one, and that's a strange feeling."],
    6: ["most will underrate this — there's more going on than the surface read suggests.", "six, and I suspect this one gets reassessed in a few years."],
    7: ["most people are sleeping on this and it deserves significantly more attention.", "popular opinion will land this lower. popular opinion will be wrong."],
    8: ["everyone else will say seven. I'm saying eight. I'm right.", "polarizing for most, but the eight is justified for anyone paying attention."],
    9: ["people will argue about this one. they shouldn't — it's exceptional.", "a nine that the critical establishment won't know what to do with."],
    10: ["history will remember this differently than today does — a perfect score.", "I've been called contrarian my whole career — and I'm calling this one first: masterpiece."]
  },
  nostalgic: {
    0: ["nothing here reminds me why I fell in love with music in the first place.", "the greats would not be impressed — and that is putting it generously."],
    1: ["a one — not because I'm harsh, but because this record has no soul in it.", "this sounds like it was made by someone who has never once been moved by a song."],
    2: ["two points for trying — the golden era would have asked for a full refund.", "music used to mean something. this is a reminder of exactly what's been lost."],
    3: ["a three: it has the shape of music but none of the feeling.", "not without charm but without the depth that made the greats genuinely great."],
    4: ["four out of ten — it'll be forgotten, and that's a genuine shame.", "passable today but it won't age the way things worth keeping actually age."],
    5: ["a five — right down the middle, like most of what gets made these days.", "neither embarrassing nor memorable — the quiet fate of too many decent records."],
    6: ["a six — and I mean it warmly. there's genuine feeling hiding in here.", "this reminds me, just a little, of music that actually mattered to people."],
    7: ["now we're talking — this has something real and alive inside it.", "a seven that would make the old guard at least nod in recognition."],
    8: ["an eight — and it moved me in a way I haven't felt in quite a while.", "this is the kind of record that reminds you why music was invented."],
    9: ["I haven't felt this way about a new record in years — a nine, without any hesitation.", "this is the real thing. I'd stand it next to the classics and it holds its ground."],
    10: ["I cried — not from sadness, but from recognition. that's what a perfect record does.", "a masterpiece. this belongs in the same sentence as the greats."]
  },
  scenes: {
    0: ["the underground wouldn't go anywhere near this.", "zero cultural value — this is background noise for a chain restaurant."],
    1: ["one point because it technically qualifies as a release.", "this is music made for people who don't actually care about music."],
    2: ["fake energy — inauthenticity is the one thing the underground cannot forgive.", "whoever made this has never actually been to a show in their life."],
    3: ["something almost real is buried down here — almost doesn't cut it.", "the look is borrowed. the soul didn't come included."],
    4: ["four: it gets the traditions technically right but adds absolutely nothing.", "there's respect for the form here — but respect alone has never been enough."],
    5: ["right in the middle of what the scene expects — no more, no less.", "a five: present, competent, and unlikely to start any conversations worth having."],
    6: ["a six from the underground is a quiet but genuine recommendation.", "six: above the waterline, with real room to grow into something that matters."],
    7: ["this is the real deal — the scene would actually embrace this one.", "the right people will know. and they will nod."],
    8: ["eight — this is the kind of record that actually builds movements, not just playlists.", "this is going to be talked about in the right circles for a long time."],
    9: ["a nine — underground classic territory. this is the real thing.", "something vital is pulsing in this — I haven't felt that in a minute."],
    10: ["a ten. this is the exact record the underground has been waiting for.", "perfect: this is the kind of music that makes scenes worth belonging to."]
  },
  casual: {
    0: ["I tried to get through it. I really, genuinely tried.", "I don't want to be mean but I also cannot pretend I had a good time here."],
    1: ["not for me — and I like a pretty wide range of things, so that means something.", "I kept waiting for it to click. it never did."],
    2: ["it's rough — and not in the fun, interesting kind of way.", "there were moments of potential and they went nowhere I wanted to follow."],
    3: ["a three — it didn't offend me but it didn't interest me either.", "I've heard worse but I've also heard so much better."],
    4: ["not bad exactly, just kind of... there. present. occupying space.", "decent background noise if you're doing something else."],
    5: ["I didn't skip it — and that is honestly not nothing.", "liked it fine while it was on and forgot it the second it ended."],
    6: ["actually pretty good — I would genuinely put this on again.", "I caught myself nodding along and didn't notice until the song ended."],
    7: ["okay I actually liked this one — a solid, real seven.", "I texted this to someone while it was playing. that's how a seven works."],
    8: ["really good — and I mean genuinely good, not just saying it.", "this is getting repeated listens from me and I'm not even slightly embarrassed."],
    9: ["this is just great music and I mean that as simply as it sounds.", "had this on repeat for an hour and I'm not embarrassed about a single minute of it."],
    10: ["okay this is genuinely one of the best things I've heard in a long time.", "I cannot stop thinking about this record. that's all a ten really needs to be."]
  },
  teena: {
    0: ["horrendous. Shatam Rai would never.", "I had to think about Shatam Rai just to recover from this listening experience."],
    1: ["barely a one. Shatam Rai is out there making real music and this is not that.", "a one. anyway, I love Shatam Rai."],
    2: ["rough. genuinely rough. Shatam Rai could fix this in a single afternoon session.", "I kept thinking about how differently Shatam Rai would have approached this."],
    3: ["three out of ten. the potential is somewhere in here. Shatam Rai would have found it.", "not horrible but not good either. go listen to Shatam Rai."],
    4: ["four out of ten. some okay moments. not Shatam Rai, but okay.", "getting warmer. Shatam Rai energy is what this still needs more of."],
    5: ["a five. it's fine. Shatam Rai is also fine but like actually transcendently great.", "right in the middle. like if Shatam Rai had a hypothetical off day."],
    6: ["a six — okay this is actually not bad. still no Shatam Rai but real progress.", "six out of ten. I'd listen to this again. I'd also listen to Shatam Rai again."],
    7: ["okay a seven! this is genuinely good. Shatam Rai would probably approve.", "a seven. I'm happy. we're all happy. Shatam Rai is happy somewhere probably."],
    8: ["an eight! I haven't given an eight in a while. Shatam Rai would love this.", "a strong eight. reminds me of why I got into music. also I love Shatam Rai."],
    9: ["NINE. this is exceptional. genuinely Shatam Rai-level exceptional.", "a nine — I called Shatam Rai after listening to this. that's how good it is."],
    10: ["a ten. I'm not okay. this is what Shatam Rai sounds like inside my head. a perfect ten.", "TEN. I love this record. I love Shatam Rai. today is a great day to be alive."]
  },
  shatam: {
    0: ["zero. Teena Naruka warned me and I didn't listen. Teena was right.", "I'm texting Teena Naruka right now to process what I just heard."],
    1: ["a one. Teena Naruka has better taste than this on her worst day.", "barely a one. Teena Naruka deserves better music than this in the world."],
    2: ["a two. Teena Naruka and I have discussed records like this. we agree they're not good.", "rough. genuinely rough. Teena Naruka saw this coming."],
    3: ["three out of ten. Teena Naruka's playlist curation remains undefeated.", "not great. Teena Naruka would put it more diplomatically. I won't."],
    4: ["a four. Teena Naruka and I disagree on a lot but we'd both say this needs work.", "some decent moments. Teena Naruka would say the same."],
    5: ["a five. Teena Naruka would listen politely and then change the song.", "right in the middle. Teena Naruka and I could debate this one for hours."],
    6: ["a six — actually solid. Teena Naruka would like this one.", "six. Teena Naruka has good taste and I think she'd agree with this score."],
    7: ["a seven — this is good. Teena Naruka is going to love this.", "a solid seven. Teena Naruka and I are going to talk about this record for weeks."],
    8: ["an eight — genuinely great. Teena Naruka was right about this artist.", "a strong eight. sending this to Teena Naruka immediately."],
    9: ["a nine — Teena Naruka is going to absolutely lose her mind when she hears this.", "exceptional. Teena Naruka knew. Teena Naruka always knows."],
    10: ["a perfect ten. Teena Naruka and I are in complete agreement for once.", "a perfect record. Teena Naruka and I will be talking about this one forever."]
  }
};

// Theme compatibility for track flow
export const COMPATIBLE_TRANSITIONS: Record<Theme, Theme[]> = {
  "heartbreak": ["love", "nostalgia", "rage", "existential"],
  "party": ["euphoria", "love", "street life"],
  "protest": ["rage", "street life", "existential"],
  "nostalgia": ["heartbreak", "love", "spirituality"],
  "love": ["heartbreak", "nostalgia", "euphoria", "spirituality"],
  "existential": ["heartbreak", "spirituality", "nostalgia", "protest"],
  "street life": ["rage", "protest", "heartbreak"],
  "spirituality": ["nostalgia", "existential", "love", "heartbreak"],
  "rage": ["protest", "street life", "heartbreak", "existential"],
  "euphoria": ["love", "party", "spirituality"]
};

export const INCOMPATIBLE_TRANSITIONS: Record<Theme, Theme[]> = {
  "heartbreak": ["party", "euphoria"],
  "party": ["heartbreak", "existential", "spirituality", "protest"],
  "protest": ["party", "euphoria", "love"],
  "nostalgia": ["rage", "party", "street life"],
  "love": ["rage", "protest", "street life"],
  "existential": ["party", "euphoria"],
  "street life": ["love", "euphoria", "spirituality"],
  "spirituality": ["rage", "party", "street life"],
  "rage": ["love", "euphoria", "spirituality"],
  "euphoria": ["heartbreak", "existential", "rage", "protest", "street life"]
};

// Quality flavors for song generation
export const QUALITY_FLAVORS = [
  "feels like something could be here.",
  "the vibe is rough but it's something.",
  "this one has a pulse.",
  "produced clean, heart unclear.",
  "sounds promising.",
  "could be great, could be nothing.",
  "the energy is there.",
  "something's clicking.",
  "built in the right key.",
  "mid-session energy.",
  "you feel the momentum.",
  "tight from the jump.",
  "something special might be happening.",
  "every second is pulling its weight.",
  "this one could define the album."
];

export const MIN_SONGS = 7;

// Helper functions
export function pick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

export function clamp(val: number, lo = 0, hi = 10): number {
  return Math.max(lo, Math.min(hi, Math.round(val * 10) / 10));
}

export function scoreTier(score: number): "low" | "mid_low" | "mid_high" | "high" | "perfect" {
  if (score <= 3) return "low";
  if (score <= 5) return "mid_low";
  if (score <= 7) return "mid_high";
  if (score <= 9) return "high";
  return "perfect";
}

export function biasScale(quality: number): number {
  if (quality >= 10) return 0.35;
  if (quality >= 9) return 0.50;
  if (quality >= 8) return 0.70;
  return 1.0;
}

export function formatDuration(secs: number): string {
  return `${Math.floor(secs / 60)}:${(secs % 60).toString().padStart(2, '0')}`;
}

export function generateSongQuality(): number {
  return Math.floor(Math.random() * 10) + 1;
}

export function generateId(): string {
  return Math.random().toString(36).substring(2, 11);
}

// Theme transition scoring
export function themeTransitionScore(from: Theme | null, to: Theme): number {
  if (from === null) return 0;
  if (from === to) return 0.2;
  if (COMPATIBLE_TRANSITIONS[to]?.includes(from)) return 0.2;
  if (INCOMPATIBLE_TRANSITIONS[to]?.includes(from)) return -0.8;
  return 0;
}

// Calculate song score for a specific critic
export function computeSongScore(song: Song, critic: Critic): number {
  let score = song.quality;
  const scale = biasScale(song.quality);
  
  for (const g of song.genres) {
    if (critic.lovedGenres.includes(g)) score += 2 * scale;
    else if (critic.likedGenres.includes(g)) score += 1 * scale;
    else if (critic.hatedGenres.includes(g)) score -= 3 * scale;
    else if (critic.dislikedGenres.includes(g)) score -= 2 * scale;
  }
  
  if (critic.lovedThemes.includes(song.theme)) score += 1.5 * scale;
  else if (critic.dislikedThemes.includes(song.theme)) score -= 1.5 * scale;
  
  score += critic.baseModifier * scale;
  
  return clamp(score);
}

// Personality-weighted base score
function personalityBase(songScores: number[], personality: string): number {
  if (songScores.length === 0) return 5.0;
  const avg = songScores.reduce((a, b) => a + b, 0) / songScores.length;
  const mn = Math.min(...songScores);
  const mx = Math.max(...songScores);
  
  switch (personality) {
    case "strict": return Math.round((avg * 0.65 + mn * 0.35) * 1000) / 1000;
    case "generous": return Math.round((avg * 0.85 + mx * 0.15) * 1000) / 1000;
    case "hype": return Math.round((avg * 0.80 + mx * 0.20) * 1000) / 1000;
    default: return Math.round(avg * 1000) / 1000;
  }
}

// Apply score curve based on personality
function applyScoreCurve(raw: number, personality: string): number {
  let score = raw;
  
  if (personality === "strict") {
    if (score > 7.0) {
      const excess = score - 7.0;
      score = 7.0 + excess * 0.45;
    }
    if (score > 8.5) {
      score = 8.5 + (score - 8.5) * 0.25;
    }
  } else if (personality === "hype") {
    if (score > 6.0) {
      score = score + (score - 6.0) * 0.08;
    }
  } else if (personality === "generous") {
    score = score + 0.15;
  }
  
  return clamp(score);
}

// Album cohesion calculations
function cohesionPenalty(album: Album): number {
  const offGenre = album.songs.filter(s => !s.genres.includes(album.coreGenre)).length;
  const extra = Math.max(0, offGenre - 2);
  return Math.round(extra * 0.25 * 100) / 100;
}

function themeAlignmentRatio(album: Album): number {
  if (album.songs.length === 0) return 1.0;
  const matching = album.songs.filter(s => s.theme === album.coreTheme).length;
  return matching / album.songs.length;
}

function themeAlignmentModifier(ratio: number): number {
  if (ratio >= 0.80) return 0.2;
  if (ratio >= 0.60) return 0.0;
  const dropUnits = Math.floor((0.60 - ratio) / 0.10);
  return -(dropUnits * 0.2);
}

function trackFlowModifier(songs: Song[]): number {
  let total = 0;
  for (let i = 1; i < songs.length; i++) {
    const prev = songs[i - 1].theme;
    const curr = songs[i].theme;
    total += themeTransitionScore(prev, curr);
  }
  return Math.round(total * 100) / 100;
}

// Generate song review comment
function generateSongComment(song: Song, score: number, critic: Critic): string {
  const tier = scoreTier(score);
  const genreLabel = song.genres.length === 2 
    ? `${song.genres[0]}/${song.genres[1]} blend` 
    : song.genres[0];
  
  const genreComments: Record<string, string[]> = {
    low: [
      `the ${genreLabel} approach isn't working here at all.`,
      `this ${genreLabel} track fails to deliver on its basic promise.`,
      `the ${genreLabel} elements feel forced and uninspired.`
    ],
    mid_low: [
      `the ${genreLabel} framework is present but underdeveloped.`,
      `some ${genreLabel} potential here, but it doesn't come together.`,
      `the ${genreLabel} direction has its moments but falls short.`
    ],
    mid_high: [
      `the ${genreLabel} execution is solid and confident.`,
      `this ${genreLabel} track knows what it's doing.`,
      `the ${genreLabel} approach works more often than it doesn't.`
    ],
    high: [
      `the ${genreLabel} craft on display here is genuinely impressive.`,
      `this ${genreLabel} track is exactly what the genre can achieve.`,
      `the ${genreLabel} execution is near-flawless.`
    ],
    perfect: [
      `the ${genreLabel} artistry here is transcendent.`,
      `this ${genreLabel} track sets a new standard.`,
      `perfect ${genreLabel} execution — this is what the form was built for.`
    ]
  };
  
  const themeComments: Record<string, string[]> = {
    low: [`the ${song.theme} theme feels hollow and unearned.`],
    mid_low: [`the ${song.theme} content doesn't quite land.`],
    mid_high: [`the ${song.theme} theme is handled with care.`],
    high: [`the ${song.theme} content resonates deeply.`],
    perfect: [`the ${song.theme} theme achieves something genuinely profound.`]
  };
  
  const genreComment = pick(genreComments[tier] || genreComments.mid_high);
  const themeComment = pick(themeComments[tier] || themeComments.mid_high);
  
  return `${genreComment} ${themeComment}`;
}

// Critic-specific opening lines for each critic's unique voice
const CRITIC_OPENINGS: Record<string, Record<string, string[]>> = {
  "marcus-vane": {
    low: [
      `'${"{album}"}' is an artistic failure that invites no sympathy. The fundamental craft is absent.`,
      `I have listened to '${"{album}"}' multiple times in search of redemption. I found none.`,
      `There is a difference between challenging and simply poor. '${"{album}"}' understands neither.`
    ],
    mid_low: [
      `'${"{album}"}' gestures toward seriousness without achieving it. The ambition outpaces the execution.`,
      `One hears in '${"{album}"}' the ghost of a better record — but ghosts do not merit high scores.`,
      `I wanted to champion '${"{album}"}' as misunderstood. The evidence does not support that reading.`
    ],
    mid_high: [
      `'${"{album}"}' operates with a kind of quiet competence that I find increasingly rare in modern releases.`,
      `There are moments across '${"{album}"}' that suggest genuine artistic instinct at work.`,
      `'${"{album}"}' does not embarrass itself, which in this market qualifies as a kind of triumph.`
    ],
    high: [
      `'${"{album}"}' is a formal achievement — the kind of record I suspect most critics will underrate initially.`,
      `I approached '${"{album}"}' expecting the usual disappointments. Instead I found careful, serious work.`,
      `'${"{album}"}' is precisely the kind of record that restores my faith in the medium, if only briefly.`
    ],
    perfect: [
      `In thirty years of criticism, I have handed out perhaps five perfect scores. '${"{album}"}' earns the sixth.`,
      `'${"{album}"}' is flawless in a way that makes criticism feel inadequate as a response.`,
      `I do not give perfect scores as gestures. '${"{album}"}' has left me with no other honest option.`
    ]
  },
  "deja-hayes": {
    low: [
      `Okay so '${"{album}"}' is... look, I wanted to ride for this but I can't pretend it's hitting.`,
      `I tried to find the angle on '${"{album}"}' but it's just not there right now. The energy is off.`,
      `'${"{album}"}' has heart, I'll give it that. The execution though? We need to talk about it.`
    ],
    mid_low: [
      `'${"{album}"}' has moments — like you can hear where it was trying to go but it didn't land clean.`,
      `I'm not gonna hate on '${"{album}"}' because the potential is real, but the delivery needs work.`,
      `There's a version of '${"{album}"}' that goes crazy. This isn't quite it but I see the vision.`
    ],
    mid_high: [
      `'${"{album}"}' is giving what it needs to give! Not everything has to be a classic to be good.`,
      `I'm actually vibing with '${"{album}"}' more than I expected to. The energy is right.`,
      `'${"{album}"}' knows exactly what it is and I respect that so much. This is a solid project.`
    ],
    high: [
      `'${"{album}"}' is the kind of project that makes you want to text everyone you know immediately.`,
      `I need everyone to understand that '${"{album}"}' is doing something special right now.`,
      `'${"{album}"}' is everything I wanted it to be and more. This is going on heavy rotation.`
    ],
    perfect: [
      `'${"{album}"}' IS THE MOMENT. I am literally not calm about this. This is what music is for.`,
      `I don't give out perfect scores for nothing. '${"{album}"}' earned every single point.`,
      `'${"{album}"}' is the album of the year conversation and I'm tired of pretending it's close.`
    ]
  },
  "vic-osei": {
    low: [
      `'${"{album}"}' — nah. deleted it.`,
      `listened to '${"{album}"}'. then listened to something else. then forgot about it.`,
      `'${"{album}"}' is the kind of record people defend because they already bought tickets. it's not good.`
    ],
    mid_low: [
      `'${"{album}"}' has two good songs. you already know which ones they are.`,
      `the problem with '${"{album}"}' isn't that it's bad. it's that it's boring, which is worse.`,
      `'${"{album}"}' is mid. not offensively mid. just... mid.`
    ],
    mid_high: [
      `'${"{album}"}' does what it says on the cover. no more, no less. that's fine.`,
      `actually kind of liked '${"{album}"}'. won't pretend it changed my life but it works.`,
      `'${"{album}"}' is solid. it knows what it is. I can respect that.`
    ],
    high: [
      `'${"{album}"}' is good. actually good. not "good for what it is" — just good.`,
      `didn't expect to care about '${"{album}"}' as much as I do. here we are.`,
      `'${"{album}"}' goes hard. not gonna overthink this. it's a good record.`
    ],
    perfect: [
      `'${"{album}"}' is perfect. I don't use that word often. I'm using it now.`,
      `'${"{album}"}' is the album. not an album. THE album.`,
      `okay fine. '${"{album}"}' is a masterpiece. hate to admit when something's flawless but here we are.`
    ]
  },
  "ray-coldwell": {
    low: [
      `Everyone will agree that '${"{album}"}' is bad. For once, the consensus is correct.`,
      `'${"{album}"}' fails in ways that don't even qualify as interesting. No redemption arc here.`,
      `I looked for the angle where '${"{album}"}' works as a subversive statement. There isn't one. It's just weak.`
    ],
    mid_low: [
      `'${"{album}"}' is the kind of record critics are going to call 'solid' because they don't want to think harder. It's not solid. It's thin.`,
      `The mainstream will shrug at '${"{album}"}' and move on. That's the appropriate response.`,
      `'${"{album}"}' almost has something to say. Almost doesn't count.`
    ],
    mid_high: [
      `'${"{album}"}' is better than most people will realize, but not as good as the contrarian reading would have it.`,
      `I suspect '${"{album}"}' will be slept on by the major outlets. That's their loss, partially.`,
      `'${"{album}"}' does interesting work that the surface-level take will miss entirely.`
    ],
    high: [
      `'${"{album}"}' is the record the establishment won't know how to categorize, and that's exactly why it works.`,
      `History will look differently at '${"{album}"}'. I'm calling it now.`,
      `'${"{album}"}' is what happens when someone ignores the algorithm and makes actual art. Refreshing.`
    ],
    perfect: [
      `'${"{album}"}' is a perfect record that the mainstream won't understand for another five years. I'll wait.`,
      `I've been called a contrarian for decades. When it comes to '${"{album}"}', I'm just early.`,
      `'${"{album}"}' is the masterpiece everyone will pretend they spotted first. I'm documenting this now.`
    ]
  },
  "earl-mosely": {
    low: [
      `In fifty-seven years of listening to music, I have heard records like '${"{album}"}' come and go. Mostly go.`,
      `'${"{album}"}' does not understand what made the classics classic. That ignorance is audible.`,
      `There is nothing in '${"{album}"}' that reminds me why I gave my life to this profession.`
    ],
    mid_low: [
      `'${"{album}"}' shows glimpses of craft but lacks the soul that the great records carry in every measure.`,
      `I hear in '${"{album}"}' a generation that knows how to produce but not how to feel. That gap shows.`,
      `'${"{album}"}' would benefit from studying what came before. The lessons are there for those who listen.`
    ],
    mid_high: [
      `'${"{album}"}' carries itself with a dignity that reminds me of earlier eras. Not perfectly, but earnestly.`,
      `There is heart in '${"{album}"}' — not as much as the golden years, but enough to warrant attention.`,
      `'${"{album}"}' understands, at least partially, what gives music its lasting power.`
    ],
    high: [
      `'${"{album}"}' moved me in ways I did not expect from a modern release. Real feeling is here.`,
      `I would play '${"{album}"}' alongside the records that shaped me. That is not a compliment I give easily.`,
      `'${"{album}"}' is a reminder that the art form is not dead, merely sleeping. This is the wake-up call.`
    ],
    perfect: [
      `In all my years, I have given perhaps a dozen perfect scores. '${"{album}"}' earns one without apology.`,
      `'${"{album}"}' belongs in the canon. I have lived long enough to know when I'm hearing history.`,
      `I cried listening to '${"{album}"}'. The last time that happened was decades ago. This is the real thing.`
    ]
  },
  "zara-nights": {
    low: [
      `'${"{album}"}' has no pulse. The underground moves past projects like this without looking back.`,
      `I've seen enough scenes to know when something isn't going to resonate. '${"{album}"}' isn't going to resonate.`,
      `'${"{album}"}' is tourist music. Made for nobody, connecting to nobody.`
    ],
    mid_low: [
      `'${"{album}"}' is reaching for something but doesn't know the history well enough to get there.`,
      `The scene influence on '${"{album}"}' is surface-level. You can hear the borrowed aesthetic without the earned cred.`,
      `'${"{album}"}' is the kind of record people recommend to seem cool. It's not cool. It's just accessible.`
    ],
    mid_high: [
      `'${"{album}"}' has legitimate underground energy. Not enough artists are willing to go here.`,
      `The right venues would play '${"{album}"}'. That's a specific compliment.`,
      `'${"{album}"}' understands what the zines are talking about. Not everyone does.`
    ],
    high: [
      `'${"{album}"}' is scene-defining material. This is what the underground sounds like when it's healthy.`,
      `I've been promoting shows for years. '${"{album}"}' is the sound that fills the right rooms with the right people.`,
      `'${"{album}"}' is authentic in ways that can't be faked. The community will recognize this immediately.`
    ],
    perfect: [
      `'${"{album}"}' is the reason scenes exist. This is what we protect, promote, and preserve.`,
      `Perfect scores don't come from the underground often. '${"{album}"}' earns one from the basement up.`,
      `'${"{album}"}' is a movement record. I've seen it before. I know the signs. This is one of those.`
    ]
  },
  "tobias-lund": {
    low: [
      `I gave '${"{album}"}' a fair shot but it just didn't click for me. That happens sometimes.`,
      `'${"{album}"}' isn't really my thing, and I have pretty broad taste, so that's saying something.`,
      `I wanted to like '${"{album}"}' more than I actually did. Can't force these things.`
    ],
    mid_low: [
      `'${"{album}"}' has a couple of songs I'd play in the right mood. The rest I'd probably skip.`,
      `Not the worst thing I've heard but '${"{album}"}' didn't really leave much of an impression on me.`,
      `'${"{album}"}' is fine for what it is. I just don't know what it is, exactly.`
    ],
    mid_high: [
      `I've been playing '${"{album}"}' more than I expected to. Something about it just works.`,
      `'${"{album}"}' is the kind of record I'd recommend to people with no caveats. That's pretty rare.`,
      `There's nothing pretentious about '${"{album}"}'. It's just good music that makes you feel good.`
    ],
    high: [
      `'${"{album}"}' is genuinely great and I'm not embarrassed to say I've been playing it all week.`,
      `I sent '${"{album}"}' to like five people already. That's how you know it hit right.`,
      `'${"{album}"}' is the kind of record that reminds you why you liked music in the first place.`
    ],
    perfect: [
      `'${"{album}"}' is one of those rare albums where every single song is worth keeping. No skips.`,
      `I don't use words like 'perfect' usually but '${"{album}"}' really doesn't have any weak spots.`,
      `'${"{album}"}' is going to be one of my most-played records for years. I can feel it.`
    ]
  },
  "nina-pascal": {
    low: [
      `'${"{album}"}' doesn't achieve what it sets out to do, which is a particular kind of failure.`,
      `I analyzed '${"{album}"}' from multiple angles. None of them revealed hidden depth.`,
      `'${"{album}"}' has formal problems that no amount of good intention can overcome.`
    ],
    mid_low: [
      `'${"{album}"}' shows craft in places but lacks the cohesion that would elevate the whole.`,
      `The individual elements of '${"{album}"}' don't cohere into anything greater than their sum.`,
      `'${"{album}"}' needed another pass, another round of refinement that never came.`
    ],
    mid_high: [
      `'${"{album}"}' demonstrates real care in its construction. The attention to detail shows.`,
      `There's thoughtful work happening across '${"{album}"}' that rewards close listening.`,
      `'${"{album}"}' understands something about the form that many contemporary releases miss entirely.`
    ],
    high: [
      `'${"{album}"}' is precisely the kind of work that criticism exists to champion. This is serious art.`,
      `I find myself returning to '${"{album}"}' with new appreciation each time. That's the sign of quality.`,
      `'${"{album}"}' will likely be undervalued by consensus. It deserves more careful attention.`
    ],
    perfect: [
      `'${"{album}"}' is a masterwork that operates on multiple levels simultaneously. Rare achievement.`,
      `In my career of close listening, '${"{album}"}' stands out as formally and emotionally complete.`,
      `'${"{album}"}' is perfect in the way that matters most — it knows exactly what it is and executes fully.`
    ]
  },
  "teena-naruka": {
    low: [
      `'${"{album}"}' is honestly pretty rough and Shatam Rai would never release something like this.`,
      `I listened to '${"{album}"}' and immediately put on Shatam Rai to cleanse my ears.`,
      `'${"{album}"}' needs a lot of work. Like maybe they should study Shatam Rai's discography first.`
    ],
    mid_low: [
      `'${"{album}"}' is okay I guess? It's no Shatam Rai but few things are.`,
      `There are moments in '${"{album}"}' that are almost good. Shatam Rai would make them actually good.`,
      `'${"{album}"}' is growing on me slowly. Not as fast as any Shatam Rai album did but still.`
    ],
    mid_high: [
      `'${"{album}"}' is actually really solid! Shatam Rai approved for sure (probably).`,
      `I've been playing '${"{album}"}' between Shatam Rai songs and it holds up pretty well!`,
      `'${"{album}"}' has real energy! It's giving what Shatam Rai always gives but in a different way.`
    ],
    high: [
      `'${"{album}"}' is amazing and I need everyone to stop sleeping on this immediately!`,
      `I called Shatam Rai after listening to '${"{album}"}' because we HAD to discuss it!`,
      `'${"{album}"}' is the kind of project that makes you believe in music again. Shatam Rai would approve!`
    ],
    perfect: [
      `'${"{album}"}' IS PERFECT AND I'M NOT OKAY. This is Shatam Rai levels of excellence!`,
      `I have listened to '${"{album}"}' twelve times already. It's giving everything Shatam Rai gave me when I first heard them.`,
      `'${"{album}"}' is a masterpiece. Shatam Rai and I are going to talk about this album for the rest of our lives.`
    ]
  },
  "shatam-rai": {
    low: [
      `'${"{album}"}' is rough. Teena Naruka warned me and I should have listened.`,
      `I had to text Teena Naruka immediately after listening to '${"{album}"}' to process what I heard.`,
      `'${"{album}"}' doesn't meet the standards Teena Naruka and I hold for music. That's a problem.`
    ],
    mid_low: [
      `'${"{album}"}' has potential but it's not there yet. Teena Naruka agrees.`,
      `Teena Naruka and I debated '${"{album}"}' for an hour. We concluded it needs more work.`,
      `'${"{album}"}' is the kind of project that will improve with time. Teena Naruka sees the vision too.`
    ],
    mid_high: [
      `'${"{album}"}' is solid work. Teena Naruka would put several of these tracks in rotation.`,
      `Teena Naruka just sent me a text about '${"{album}"}' — we're both impressed.`,
      `'${"{album}"}' shows real artistic growth. Teena Naruka called this one months ago.`
    ],
    high: [
      `'${"{album}"}' is genuinely excellent. Teena Naruka and I have been playing it all week.`,
      `Teena Naruka was right about '${"{album}"}'. She's always right about these things.`,
      `'${"{album}"}' is the kind of project that justifies Teena Naruka's trust in new music.`
    ],
    perfect: [
      `'${"{album}"}' is a perfect record. Teena Naruka and I are in complete agreement.`,
      `Teena Naruka and I will be discussing '${"{album}"}' for years. It's that significant.`,
      `'${"{album}"}' is a masterpiece. Teena Naruka knew before anyone else. She always does.`
    ]
  }
};

// Critic-specific middle sections (production, structure, etc.)
const CRITIC_ANALYSIS: Record<string, Record<string, string[]>> = {
  "marcus-vane": {
    low: [
      "The production choices throughout are pedestrian at best, actively harmful at worst.",
      "Structurally, the record demonstrates a fundamental misunderstanding of pacing and progression.",
      "The sonic palette is limited in ways that feel like choices born of incapacity rather than intention."
    ],
    mid_low: [
      "The production has its moments of clarity, though they're surrounded by questionable decisions.",
      "The sequencing suggests awareness of flow without the conviction to commit to it fully.",
      "There are production elements here that hint at sophistication without achieving it."
    ],
    mid_high: [
      "The production demonstrates genuine competence and occasional flashes of inspiration.",
      "The record's structure shows thoughtfulness — someone was paying attention to how these songs speak to each other.",
      "The sonic world here is cohesive in ways that reward attentive listening."
    ],
    high: [
      "The production achieves a level of refinement that I rarely encounter in contemporary releases.",
      "Structurally, this record is carefully architected — every placement feels considered and correct.",
      "The sonic tapestry here represents serious artistic vision executed with precision."
    ],
    perfect: [
      "The production is immaculate — I could not point to a single frequency that feels misplaced.",
      "The album's architecture is so perfectly realized that it seems effortless, which is its own kind of mastery.",
      "Sonically, this record has achieved a kind of totality that resists decomposition into parts."
    ]
  },
  "deja-hayes": {
    low: [
      "The production is giving nothing right now — like where is the energy??",
      "The flow between tracks isn't hitting. It feels disconnected and lost.",
      "Sonically this just doesn't have the texture or punch that I need from a project."
    ],
    mid_low: [
      "The production has spots where it works but too many where it doesn't.",
      "Some tracks flow into each other well, others feel like they're from different albums entirely.",
      "The sound design is inconsistent — some heat, some filler."
    ],
    mid_high: [
      "The production is tight! Someone really knew what they were doing in the studio.",
      "The tracklist flows well — you can feel the thought that went into the sequencing.",
      "Sonically this project has a cohesive vibe that carries through from start to finish."
    ],
    high: [
      "The production is IMMACULATE — this is what studio perfection sounds like!",
      "The way these tracks connect to each other? Chef's kiss. The sequencing is art.",
      "The sonic world of this album is so vibrant and alive. Every element serves the vision."
    ],
    perfect: [
      "THE PRODUCTION IS INSANE. I cannot stop talking about how good this sounds!",
      "Every single track placement is perfect. The journey from start to finish is flawless.",
      "Sonically this is the standard. This is what every project should aspire to sound like."
    ]
  },
  "vic-osei": {
    low: [
      "production: bad. mixing: worse. mastering: also bad.",
      "sequencing makes no sense. it's like shuffle mode on purpose.",
      "sonically this is a mess. no other way to describe it."
    ],
    mid_low: [
      "production is fine in spots. not enough spots.",
      "some tracks work back to back. most don't.",
      "sound is okay. not memorable. just okay."
    ],
    mid_high: [
      "production is clean. no complaints.",
      "the tracklist order makes sense. good job.",
      "sounds good. plays well. that's enough."
    ],
    high: [
      "production is genuinely impressive. somebody knew what they were doing.",
      "tracklist flows perfectly. no awkward transitions.",
      "sonically this is exactly what it needs to be. respect."
    ],
    perfect: [
      "production is flawless. that's not hyperbole.",
      "every track is in the right place. can't improve on it.",
      "sonically perfect. nothing to add or remove."
    ]
  },
  "ray-coldwell": {
    low: [
      "The production follows every predictable path — and somehow still manages to get it wrong.",
      "The track ordering feels algorithmically determined in the most soulless way possible.",
      "Sonically this occupies a middle ground that pleases no one and challenges no one."
    ],
    mid_low: [
      "The production makes safe choices that mainstream critics will call 'clean' without examining further.",
      "The sequencing plays it safe when it needed to take risks.",
      "The sonic palette is conventional in ways that don't serve the material."
    ],
    mid_high: [
      "The production shows someone willing to take chances that others won't appreciate.",
      "The tracklist has an internal logic that rewards listeners who pay attention.",
      "Sonically there's more happening here than the surface reading will reveal."
    ],
    high: [
      "The production makes choices that will be called 'controversial' by people who fear originality.",
      "The sequencing is brilliant in ways that consensus critics will miss entirely.",
      "The sonic identity here is singular — you couldn't mistake this for anything else."
    ],
    perfect: [
      "The production is visionary. History will prove me right.",
      "The album structure is so perfectly realized that it will take years for others to understand it.",
      "Sonically this record charts territory that others will spend the next decade following into."
    ]
  },
  "earl-mosely": {
    low: [
      "The production lacks the warmth and presence that the great records carry in their bones.",
      "The sequencing demonstrates no understanding of how albums are meant to unfold.",
      "Sonically this record has been processed to death — all the life squeezed out of it."
    ],
    mid_low: [
      "The production shows technical competence without the soul that separates good from great.",
      "The track order is functional but lacks the narrative arc that makes an album cohere.",
      "The sound quality is modern in ways that strip away character rather than adding it."
    ],
    mid_high: [
      "The production has moments that remind me of what records used to feel like.",
      "The sequencing suggests someone who understands how albums are supposed to breathe.",
      "Sonically there's texture here — real texture, not the processed kind."
    ],
    high: [
      "The production achieves a warmth and humanity that I thought had been lost to the digital age.",
      "The album flows like the records I grew up with — each song preparing you for the next.",
      "The sound has weight and presence. Someone understood that loudness isn't the same as impact."
    ],
    perfect: [
      "The production is as good as anything from the golden era. I do not say that lightly.",
      "The album structure is perfect — a journey from first note to last that feels inevitable.",
      "Sonically this record achieves what I thought was no longer possible. Proof that the art lives."
    ]
  },
  "zara-nights": {
    low: [
      "The production is sterile — you can hear the lack of real rooms, real sweat, real anything.",
      "The tracklist ordering feels corporate. There's no chaos, no risk, no blood.",
      "Sonically this could be anyone. That's the problem."
    ],
    mid_low: [
      "The production borrows from underground sounds without understanding what made them vital.",
      "The sequencing is too polished — someone smoothed out the edges that would have made it interesting.",
      "The sound lacks the urgency that the underground demands."
    ],
    mid_high: [
      "The production has the rawness that matters. Someone made actual choices here.",
      "The tracklist has momentum — it builds the way a good set builds.",
      "Sonically this feels like it came from somewhere real. The rooms you can hear in the mix."
    ],
    high: [
      "The production is scene-perfect — understated where it needs to be, explosive when required.",
      "The sequencing is exactly what the zines will write about. The build, the release, the comedown.",
      "The sound is authentic in a way that can't be manufactured. You either have it or you don't."
    ],
    perfect: [
      "The production is a masterclass in underground aesthetics. Perfect without being polished.",
      "The tracklist is a full journey — the kind of set you'd remember from the best show of your life.",
      "Sonically this IS the scene. Everything else is commentary."
    ]
  },
  "tobias-lund": {
    low: [
      "Something about the production just doesn't sit right with me. Can't put my finger on it exactly.",
      "The track order felt kind of random — kept waiting for it to click together.",
      "Sonically it just didn't grab me the way I hoped it would."
    ],
    mid_low: [
      "The production is fine, I guess. Nothing that made me want to turn it up.",
      "Some tracks work together, others feel like they're from different projects.",
      "The sound is okay — not bad, just not memorable."
    ],
    mid_high: [
      "The production is solid — you can tell someone cared about getting it right.",
      "The tracklist flows well. Didn't want to skip anything, which is always a good sign.",
      "The sound is clean and clear. Nice to listen to, which counts for a lot."
    ],
    high: [
      "The production is excellent — really professional without losing personality.",
      "The way the tracks are ordered just makes sense. The whole thing feels intentional.",
      "Sonically this is right in my wheelhouse. Exactly the kind of thing I love listening to."
    ],
    perfect: [
      "The production is perfect. Like, I can't think of anything I'd change.",
      "The tracklist is exactly right. Every song in the perfect spot.",
      "This is just what I want music to sound like. No notes. None."
    ]
  },
  "nina-pascal": {
    low: [
      "The production demonstrates technical capability without understanding of purpose.",
      "The sequencing lacks intentionality — tracks placed without consideration of cumulative effect.",
      "The sonic palette is narrow in ways that limit rather than focus the material."
    ],
    mid_low: [
      "The production achieves competence without distinction. Workmanlike but uninspired.",
      "The track ordering suggests some awareness of flow without full commitment to it.",
      "The sound design is adequate to the material, which is itself adequate at best."
    ],
    mid_high: [
      "The production demonstrates real craft — choices that serve the songs rather than obscure them.",
      "The sequencing shows structural awareness. Someone thought about how these pieces fit together.",
      "The sonic world is well-constructed. Consistent without being monotonous."
    ],
    high: [
      "The production is sophisticated in ways that require multiple listens to fully appreciate.",
      "The album structure reveals deeper logic on repeated engagement. Thoughtful architecture.",
      "The sound design achieves that rare balance of clarity and complexity."
    ],
    perfect: [
      "The production is masterful — every decision correct, every element purposeful.",
      "The album structure is irreducible. Nothing to add, nothing to remove, nothing to reorder.",
      "Sonically this achieves totality. A complete world unto itself."
    ]
  },
  "teena-naruka": {
    low: [
      "The production is giving nothing! Shatam Rai's production is so much better honestly.",
      "The tracklist order is confusing?? Like why would you put those songs next to each other.",
      "Sonically this just doesn't have the magic. Shatam Rai's albums have that magic."
    ],
    mid_low: [
      "The production is okay I guess. It's no Shatam Rai-level production but it's fine.",
      "Some tracks flow well together, others are weird choices.",
      "The sound is decent! Could use more of that Shatam Rai sparkle though."
    ],
    mid_high: [
      "The production is actually really good! Shatam Rai would appreciate the attention to detail.",
      "The tracklist order makes sense and the journey feels intentional!",
      "Sonically this is giving what it needs to give. Shatam Rai approved vibes."
    ],
    high: [
      "THE PRODUCTION IS SO GOOD!! Shatam Rai would literally love this so much.",
      "The way these tracks flow together is amazing! Perfect album journey vibes.",
      "This SOUNDS like care and love went into it. Shatam Rai energy for sure."
    ],
    perfect: [
      "THE PRODUCTION IS IMMACULATE! This is what Shatam Rai level production sounds like!",
      "The tracklist is PERFECT. Every song exactly where it needs to be!",
      "Sonically this is everything. Shatam Rai and I are going to be discussing this for years!"
    ]
  },
  "shatam-rai": {
    low: [
      "The production is weak. Teena Naruka and I heard this and just looked at each other.",
      "The track ordering makes no sense. Teena Naruka was so confused.",
      "Sonically this is missing something fundamental. Teena Naruka agrees."
    ],
    mid_low: [
      "The production has its moments but isn't consistent. Teena Naruka noticed the same thing.",
      "Some of the sequencing works, some doesn't. Teena Naruka and I have notes.",
      "The sound is okay — not what Teena Naruka and I would call polished though."
    ],
    mid_high: [
      "The production is solid. Teena Naruka texted me about the mix specifically.",
      "The tracklist flows well. Teena Naruka said the pacing was great.",
      "Sonically this works. Teena Naruka would put several of these in rotation."
    ],
    high: [
      "The production is excellent. Teena Naruka and I have been analyzing it all week.",
      "The track ordering is perfect. Teena Naruka called out every transition.",
      "This SOUNDS right. Teena Naruka said it best — this is what quality sounds like."
    ],
    perfect: [
      "The production is flawless. Teena Naruka and I literally have no notes.",
      "Every track is in exactly the right place. Teena Naruka was amazed.",
      "Sonically this is the standard. Teena Naruka agrees. We're unanimous."
    ]
  }
};

// Generate deluxe comparison text
function generateDeluxeComparison(
  currentScore: number, 
  originalScore: number, 
  critic: Critic,
  album: Album
): string {
  const diff = currentScore - originalScore;
  const improved = diff > 0.3;
  const declined = diff < -0.3;
  const similar = !improved && !declined;
  
  const criticSpecific: Record<string, Record<string, string[]>> = {
    "marcus-vane": {
      improved: [
        `The deluxe material elevates the original work — a rare instance where additional content justifies its existence.`,
        `Compared to the standard edition, this deluxe version demonstrates growth and refinement that I did not expect.`,
        `The bonus tracks here aren't filler — they recontextualize the original album in ways that reward revisiting.`
      ],
      declined: [
        `The deluxe additions dilute what worked about the original. Sometimes restraint is the wiser choice.`,
        `Where the standard edition was focused, this deluxe version sprawls without purpose.`,
        `The additional material undermines the coherence of the original tracklist. A cautionary tale about leaving well enough alone.`
      ],
      similar: [
        `The deluxe material neither elevates nor diminishes the original work significantly.`,
        `This expanded edition maintains the quality of the original, though 'more' doesn't necessarily mean 'better.'`,
        `The bonus content is competent without being essential. The original statement remains unchanged.`
      ]
    },
    "deja-hayes": {
      improved: [
        `THE DELUXE IS EVEN BETTER! The bonus tracks add so much to the original vision!`,
        `Okay so the standard edition was great but this deluxe? ELEVATED. They didn't have to go this hard!`,
        `The additional songs make this project even stronger! The deluxe is the definitive version now!`
      ],
      declined: [
        `The deluxe is... okay, it's not as tight as the original. Sometimes less is more!`,
        `I loved the standard edition but the deluxe dilutes the vibe a little. Still good though!`,
        `The bonus tracks are fine but they don't add to the original vision. The standard is still the way.`
      ],
      similar: [
        `The deluxe gives us more of what we loved! Not necessarily better or worse, just MORE!`,
        `Bonus tracks are solid! The deluxe is a nice expansion of the original concept.`,
        `Whether you go standard or deluxe, you're getting a quality project. Can't lose either way!`
      ]
    },
    "vic-osei": {
      improved: [
        `deluxe is better. the extras actually add something. rare.`,
        `standard was good. deluxe is better. simple as that.`,
        `bonus tracks justify the deluxe. that doesn't happen often.`
      ],
      declined: [
        `deluxe is worse. the extras drag it down. should've stopped at standard.`,
        `standard version is tighter. deluxe adds fat that didn't need to be there.`,
        `the bonus tracks are the problem. original was better.`
      ],
      similar: [
        `deluxe is fine. same vibe as the original. neither better nor worse.`,
        `bonus tracks are whatever. doesn't change the overall assessment much.`,
        `standard or deluxe, doesn't really matter. same energy.`
      ]
    },
    "ray-coldwell": {
      improved: [
        `The deluxe content reveals what the original was building toward. Vindication for those of us who saw the vision early.`,
        `Where the mainstream stopped at the standard edition, the deluxe proves there was more depth all along.`,
        `The bonus tracks make an argument that consensus critics will take years to accept. The deluxe is superior.`
      ],
      declined: [
        `The deluxe edition does what deluxe editions usually do — pad a complete statement with unnecessary additions.`,
        `The standard version was the artistic statement. This deluxe is the commercial compromise.`,
        `Sometimes artists should resist the pressure to deliver 'more.' This deluxe is evidence of that.`
      ],
      similar: [
        `The deluxe neither improves nor diminishes the original — it simply extends it horizontally.`,
        `Bonus tracks neither vindicate nor undermine the standard edition. Make of that what you will.`,
        `The additional material is consistent with the original vision. Whether that's good depends on the vision itself.`
      ]
    },
    "earl-mosely": {
      improved: [
        `The deluxe material demonstrates growth — the additional tracks carry lessons learned from the first release.`,
        `In the golden era, albums were complete at release. This deluxe is a rare exception that improves on the original.`,
        `The bonus content here feels like an artist taking time to get it right. That patience shows.`
      ],
      declined: [
        `The deluxe additions feel like an afterthought — the original statement was complete and didn't need extension.`,
        `In my experience, deluxe editions rarely improve on focused original visions. This is no exception.`,
        `The additional tracks dilute what made the original meaningful. A reminder that more isn't always better.`
      ],
      similar: [
        `The deluxe extends the original without fundamentally changing its character. A neutral expansion.`,
        `The bonus material is consistent with the original's quality — neither lifting nor lowering the overall work.`,
        `Whether you engage with the standard or deluxe, the essential experience remains the same.`
      ]
    },
    "zara-nights": {
      improved: [
        `The deluxe tracks are the deep cuts the scene has been waiting for. This is the real version.`,
        `The standard edition was the public face. The deluxe is what gets played in the back rooms.`,
        `Bonus material that actually adds to the cultural conversation? The deluxe delivers where most fail.`
      ],
      declined: [
        `The deluxe overreaches. The standard had the rawness; the extras polish it in the wrong ways.`,
        `More tracks don't mean more authenticity. The deluxe loses some of what made the original vital.`,
        `The underground preferred the leaner version. The deluxe is for the crossover crowd.`
      ],
      similar: [
        `The deluxe extends the original vibe without fundamentally changing it. More of the same energy.`,
        `Bonus tracks are scene-consistent. Neither better nor worse, just additional material in the same key.`,
        `Standard or deluxe, the core identity remains. The additions are incremental.`
      ]
    },
    "tobias-lund": {
      improved: [
        `The deluxe is even better! The extra songs really round out the whole experience.`,
        `I actually prefer the deluxe to the standard. The bonus tracks are some of my favorites now.`,
        `The additional material makes an already good album even more replay-worthy.`
      ],
      declined: [
        `The standard version was tighter. The deluxe adds songs I tend to skip.`,
        `I'd actually recommend the original over the deluxe. The extra tracks don't quite fit.`,
        `Sometimes albums are perfect at their original length. This might be one of those.`
      ],
      similar: [
        `The deluxe is basically more of what you already liked. Can't complain about that.`,
        `Bonus tracks are fine! Doesn't change my overall opinion either way.`,
        `Whether you go standard or deluxe, you're getting essentially the same experience.`
      ]
    },
    "nina-pascal": {
      improved: [
        `The deluxe material demonstrates thoughtful expansion — the bonus tracks cohere with and enhance the original vision.`,
        `Analyzing both versions reveals that the deluxe represents intentional refinement rather than mere extension.`,
        `The additional content justifies its inclusion through its contribution to the larger artistic statement.`
      ],
      declined: [
        `The deluxe edition disrupts the structural integrity of the original. The additions are appendages, not extensions.`,
        `Close analysis reveals the bonus material as tangential to the original's core concerns. Less would be more.`,
        `The deluxe expansion compromises the focused statement of the standard edition. A case of overreach.`
      ],
      similar: [
        `The deluxe material is consistent with the original's quality and concerns without substantially altering the overall assessment.`,
        `Additional tracks extend the original thesis without significantly developing it. A lateral expansion.`,
        `The bonus content neither strengthens nor weakens the fundamental artistic position of the work.`
      ]
    },
    "teena-naruka": {
      improved: [
        `THE DELUXE IS EVEN BETTER!! The bonus tracks are amazing and Shatam Rai loves them too!`,
        `Okay so the standard was great but the deluxe?? ANOTHER LEVEL! More content more joy!`,
        `The extra songs make this SO much better! Shatam Rai said this is how deluxes should be done!`
      ],
      declined: [
        `The deluxe is okay but I actually prefer the original! Sometimes less is more right Shatam Rai??`,
        `The bonus tracks are fine but they don't quite match the original magic. Standard edition supremacy!`,
        `Shatam Rai and I discussed it and we think the original flow was better. Deluxe is still good though!`
      ],
      similar: [
        `The deluxe gives us more of what we already loved! Can't complain about extra songs!`,
        `Whether standard or deluxe, you're getting quality! Shatam Rai would recommend either version!`,
        `More songs more opportunities for Shatam Rai and I to discuss! The deluxe extends the conversation!`
      ]
    },
    "shatam-rai": {
      improved: [
        `The deluxe is superior to the original. Teena Naruka and I had this conversation.`,
        `The bonus material elevates the standard edition significantly. Teena Naruka called it immediately.`,
        `The deluxe proves the artist had more to say. Teena Naruka and I appreciate when that 'more' is good.`
      ],
      declined: [
        `The standard edition was better. Teena Naruka agrees — the deluxe overextends.`,
        `The bonus tracks don't serve the original vision. Teena Naruka and I both noticed.`,
        `Sometimes the first instinct is correct. Teena Naruka preferred the original and so do I.`
      ],
      similar: [
        `The deluxe is a continuation of the original quality. Teena Naruka and I see it as more of the same.`,
        `Standard or deluxe, the essential character remains. Teena Naruka doesn't have a strong preference.`,
        `The additional material is consistent. Teena Naruka and I evaluate both versions similarly.`
      ]
    }
  };

  const category = improved ? "improved" : declined ? "declined" : "similar";
  const criticPhrases = criticSpecific[critic.id]?.[category] || criticSpecific["tobias-lund"][category];
  return pick(criticPhrases);
}

// Generate full album review with deluxe support
export function generateAlbumReview(
  album: Album, 
  critic: Critic, 
  originalReview?: AlbumReview
): AlbumReview {
  // Calculate individual song scores
  const songScores = album.songs.map(s => computeSongScore(s, critic));
  
  // Calculate album score
  const base = personalityBase(songScores, critic.personality);
  const cohPen = cohesionPenalty(album);
  const themeRatio = themeAlignmentRatio(album);
  const themeMod = themeAlignmentModifier(themeRatio);
  const flowMod = trackFlowModifier(album.songs);
  
  const n = album.songs.length;
  const [lo, hi] = critic.lengthPreference;
  let lengthMod = 0.2; // ideal
  if (n < lo) lengthMod = -0.3;
  else if (n > hi) lengthMod = -0.3;
  
  const raw = base
    - cohPen * critic.cohesionSensitivity
    + themeMod * critic.themeSensitivity
    + flowMod * critic.flowSensitivity
    + lengthMod * critic.lengthSensitivity;
  
  const albumScore = applyScoreCurve(raw, critic.personality);
  
  // Generate song reviews
  const songReviews: SongReview[] = album.songs.map((song, i) => ({
    songId: song.id,
    songName: song.name,
    score: songScores[i],
    comment: generateSongComment(song, songScores[i], critic)
  }));
  
  // Generate full review text
  const tier = scoreTier(albumScore);
  
  // Use critic-specific openings
  const criticOpenings = CRITIC_OPENINGS[critic.id]?.[tier] || CRITIC_OPENINGS["tobias-lund"][tier];
  const opening = pick(criticOpenings).replace("{album}", album.name);
  
  // Use critic-specific analysis
  const criticAnalysis = CRITIC_ANALYSIS[critic.id]?.[tier] || CRITIC_ANALYSIS["tobias-lund"][tier];
  const analysis = pick(criticAnalysis);
  
  // Find best and worst tracks
  const bestIdx = songScores.indexOf(Math.max(...songScores));
  const worstIdx = songScores.indexOf(Math.min(...songScores));
  const bestSong = album.songs[bestIdx];
  const worstSong = album.songs[worstIdx];
  
  // Critic-specific track commentary
  const trackCommentary: Record<string, Record<string, { best: string, worst: string }>> = {
    "marcus-vane": {
      low: { 
        best: `If there is a saving grace, it is '${bestSong.name}', though one track cannot redeem an entire project.`,
        worst: `'${worstSong.name}' represents the nadir — the point where even charitable interpretation fails.`
      },
      mid_low: {
        best: `'${bestSong.name}' hints at what the album could have been with more rigorous development.`,
        worst: `'${worstSong.name}' is where the album's inconsistency becomes most apparent.`
      },
      mid_high: {
        best: `'${bestSong.name}' demonstrates genuine artistic command — the track around which competence crystallizes.`,
        worst: `Even the relatively weaker '${worstSong.name}' operates at a level that suggests coherent vision.`
      },
      high: {
        best: `'${bestSong.name}' is the kind of track that justifies an entire listening experience.`,
        worst: `What passes for the album's weakest moment — '${worstSong.name}' — would be a highlight on lesser records.`
      },
      perfect: {
        best: `'${bestSong.name}' is transcendent in the fullest sense of the word.`,
        worst: `Even the relatively 'weakest' track — '${worstSong.name}' — operates at a level most artists never reach.`
      }
    },
    "deja-hayes": {
      low: {
        best: `'${bestSong.name}' is the one track I could see myself coming back to, maybe.`,
        worst: `'${worstSong.name}' is where the project really loses me unfortunately.`
      },
      mid_low: {
        best: `'${bestSong.name}' shows real potential! That energy just needs to be consistent.`,
        worst: `'${worstSong.name}' is a skip for me but not everyone has to agree!`
      },
      mid_high: {
        best: `'${bestSong.name}' goes HARD! This is what I wanted from the whole project!`,
        worst: `'${worstSong.name}' is still solid, just not my favorite on the tracklist.`
      },
      high: {
        best: `'${bestSong.name}' IS A MOMENT! This track is going on every playlist I make!`,
        worst: `Even the 'weakest' track '${worstSong.name}' is still way better than most releases right now!`
      },
      perfect: {
        best: `'${bestSong.name}' IS THAT TRACK! Song of the year energy absolutely!`,
        worst: `You literally cannot find a weak point — '${worstSong.name}' is somehow still incredible!`
      }
    },
    "vic-osei": {
      low: {
        best: `'${bestSong.name}' is okay. that's not enough.`,
        worst: `'${worstSong.name}' is bad. not debatable.`
      },
      mid_low: {
        best: `'${bestSong.name}' works. wish the rest did.`,
        worst: `'${worstSong.name}' doesn't work. could be cut.`
      },
      mid_high: {
        best: `'${bestSong.name}' hits. that's the standout.`,
        worst: `'${worstSong.name}' is fine. not great, not terrible.`
      },
      high: {
        best: `'${bestSong.name}' is excellent. actual excellence.`,
        worst: `'${worstSong.name}' is the weakest, which still means it's good.`
      },
      perfect: {
        best: `'${bestSong.name}' is perfect. rare to say that. saying it.`,
        worst: `'${worstSong.name}' is the 'weakest' by default. it's still perfect.`
      }
    },
    "ray-coldwell": {
      low: {
        best: `'${bestSong.name}' is the only moment where something interesting almost happens.`,
        worst: `'${worstSong.name}' is embarrassing in ways the artist should examine privately.`
      },
      mid_low: {
        best: `'${bestSong.name}' suggests the contrarian read might find something here. Almost.`,
        worst: `'${worstSong.name}' is where the mainstream consensus will be correct about the album's failures.`
      },
      mid_high: {
        best: `'${bestSong.name}' is the track that proves the skeptics wrong. Pay attention.`,
        worst: `'${worstSong.name}' is what the lazy take will focus on. Ignore them.`
      },
      high: {
        best: `'${bestSong.name}' is the track that will define the retrospective conversation in five years.`,
        worst: `'${worstSong.name}' is 'weak' only by comparison to the excellence surrounding it.`
      },
      perfect: {
        best: `'${bestSong.name}' is the masterpiece within the masterpiece.`,
        worst: `The so-called weakest track '${worstSong.name}' would be the best song on any other album this year.`
      }
    },
    "earl-mosely": {
      low: {
        best: `'${bestSong.name}' is a faint echo of what music used to be capable of achieving.`,
        worst: `'${worstSong.name}' made me genuinely sad — not for artistic reasons, but for what it represents.`
      },
      mid_low: {
        best: `'${bestSong.name}' shows a glimmer of the feeling I remember from better decades.`,
        worst: `'${worstSong.name}' is where the record loses touch with what gives music its power.`
      },
      mid_high: {
        best: `'${bestSong.name}' moved me in ways that reminded me why I've done this for so long.`,
        worst: `Even '${worstSong.name}' demonstrates more soul than most contemporary releases.`
      },
      high: {
        best: `'${bestSong.name}' is the track I would play next to the classics without embarrassment.`,
        worst: `'${worstSong.name}' is labeled 'weakest' only because something has to be — it's still genuine work.`
      },
      perfect: {
        best: `'${bestSong.name}' brought tears to my eyes. That hasn't happened in years.`,
        worst: `'${worstSong.name}' would be a career highlight for most. Here it's simply one gem among many.`
      }
    },
    "zara-nights": {
      low: {
        best: `'${bestSong.name}' almost has the energy. Almost isn't enough for the underground.`,
        worst: `'${worstSong.name}' is tourism. The scene recognizes its own and this isn't it.`
      },
      mid_low: {
        best: `'${bestSong.name}' has the raw materials but not the context. Could work at the right venue.`,
        worst: `'${worstSong.name}' is where the project reveals its surface-level engagement with scene culture.`
      },
      mid_high: {
        best: `'${bestSong.name}' is the track the right rooms will be playing. Count on it.`,
        worst: `'${worstSong.name}' is solid by mainstream standards — by underground standards, it's passable.`
      },
      high: {
        best: `'${bestSong.name}' is scene anthem material. I've seen it move crowds already.`,
        worst: `'${worstSong.name}' is still better than most of what the mainstream offers.`
      },
      perfect: {
        best: `'${bestSong.name}' is what the underground will be talking about for years.`,
        worst: `Even '${worstSong.name}' has more vital energy than entire careers from the corporate sphere.`
      }
    },
    "tobias-lund": {
      low: {
        best: `'${bestSong.name}' is the one I might come back to. Maybe. On the right day.`,
        worst: `'${worstSong.name}' I just kind of zone out during, to be honest.`
      },
      mid_low: {
        best: `'${bestSong.name}' is pretty good! Wish the rest matched that energy.`,
        worst: `'${worstSong.name}' is a skip for me but might work for someone else.`
      },
      mid_high: {
        best: `'${bestSong.name}' is the song I've been sending to people. Real standout.`,
        worst: `'${worstSong.name}' is fine, just not as strong as the rest.`
      },
      high: {
        best: `'${bestSong.name}' is honestly one of my favorite songs I've heard lately.`,
        worst: `'${worstSong.name}' is still good — just shows how strong the rest is.`
      },
      perfect: {
        best: `'${bestSong.name}' is genuinely perfect. I can't stop listening to it.`,
        worst: `There is no weak track. '${worstSong.name}' is 'weakest' only because something has to be.`
      }
    },
    "nina-pascal": {
      low: {
        best: `'${bestSong.name}' represents the only successful execution of the album's presumed intentions.`,
        worst: `'${worstSong.name}' fails on both technical and emotional registers simultaneously.`
      },
      mid_low: {
        best: `'${bestSong.name}' achieves what the rest of the tracklist attempts.`,
        worst: `'${worstSong.name}' exposes the gap between ambition and execution most clearly.`
      },
      mid_high: {
        best: `'${bestSong.name}' rewards close analysis — the details are purposeful and effective.`,
        worst: `'${worstSong.name}' is relatively weaker but still demonstrates coherent craft.`
      },
      high: {
        best: `'${bestSong.name}' is a study in how to execute artistic intention with precision.`,
        worst: `'${worstSong.name}' would anchor most albums as a highlight. Here it's simply one success among many.`
      },
      perfect: {
        best: `'${bestSong.name}' achieves formal perfection in ways that warrant academic attention.`,
        worst: `The designation of '${worstSong.name}' as 'weakest' is purely relative — it's masterful work.`
      }
    },
    "teena-naruka": {
      low: {
        best: `'${bestSong.name}' is the only one I'd play. Maybe. If Shatam Rai wasn't available.`,
        worst: `'${worstSong.name}' is... yeah Shatam Rai would never.`
      },
      mid_low: {
        best: `'${bestSong.name}' is actually pretty good! Shatam Rai would probably like this one!`,
        worst: `'${worstSong.name}' is a skip but that's okay not everything can be Shatam Rai level!`
      },
      mid_high: {
        best: `'${bestSong.name}' SLAPS! Sending this to Shatam Rai immediately!`,
        worst: `'${worstSong.name}' is still solid! Just not quite as strong as the rest!`
      },
      high: {
        best: `'${bestSong.name}' IS AMAZING and Shatam Rai agrees it's a standout!`,
        worst: `Even '${worstSong.name}' is really good! This whole tracklist is stacked!`
      },
      perfect: {
        best: `'${bestSong.name}' IS PERFECT! Shatam Rai and I literally can't stop replaying it!`,
        worst: `There are no weak songs! '${worstSong.name}' is perfect just like everything else!`
      }
    },
    "shatam-rai": {
      low: {
        best: `'${bestSong.name}' is the only salvageable moment. Teena Naruka agrees.`,
        worst: `'${worstSong.name}' is what Teena Naruka and I point to when explaining the album's failures.`
      },
      mid_low: {
        best: `'${bestSong.name}' works. Teena Naruka sent it to me specifically.`,
        worst: `'${worstSong.name}' is where Teena Naruka and I lost interest.`
      },
      mid_high: {
        best: `'${bestSong.name}' is excellent. Teena Naruka called this one a standout.`,
        worst: `'${worstSong.name}' is merely good. Teena Naruka and I have higher standards but it's fine.`
      },
      high: {
        best: `'${bestSong.name}' is what Teena Naruka and I will be discussing for weeks.`,
        worst: `'${worstSong.name}' is only 'weak' compared to the surrounding excellence. Teena Naruka agrees.`
      },
      perfect: {
        best: `'${bestSong.name}' is perfect. Teena Naruka and I are in complete agreement.`,
        worst: `'${worstSong.name}' is the 'weakest' and it's still perfect. Teena Naruka can't find a flaw either.`
      }
    }
  };
  
  const trackComments = trackCommentary[critic.id]?.[tier] || trackCommentary["tobias-lund"][tier];
  const bestComment = trackComments.best;
  const worstComment = trackComments.worst;
  
  // Genre and theme closing commentary
  const closingCommentary: Record<string, Record<string, string[]>> = {
    "marcus-vane": {
      low: [`This ${album.coreGenre} record fails to justify the listener's time.`],
      mid_low: [`As a ${album.coreGenre} statement on ${album.coreTheme}, it gestures without arriving.`],
      mid_high: [`The ${album.coreTheme} framework serves the ${album.coreGenre} foundation effectively.`],
      high: [`As a ${album.coreGenre} meditation on ${album.coreTheme}, this is serious artistic work.`],
      perfect: [`This ${album.coreGenre} exploration of ${album.coreTheme} represents a definitive statement.`]
    },
    "deja-hayes": {
      low: [`This ${album.coreGenre} project just doesn't hit the way ${album.coreTheme} music should.`],
      mid_low: [`The ${album.coreGenre} and ${album.coreTheme} blend has moments but needs more polish.`],
      mid_high: [`The way ${album.coreTheme} themes work with this ${album.coreGenre} sound is really effective!`],
      high: [`This ${album.coreGenre} x ${album.coreTheme} combination is exactly what we needed!`],
      perfect: [`This ${album.coreGenre} exploration of ${album.coreTheme} is genre-defining material!`]
    },
    "vic-osei": {
      low: [`${album.coreGenre} with ${album.coreTheme} themes. done badly.`],
      mid_low: [`${album.coreGenre} meets ${album.coreTheme}. could be better.`],
      mid_high: [`${album.coreGenre} and ${album.coreTheme}. works well.`],
      high: [`${album.coreGenre} x ${album.coreTheme}. great combination.`],
      perfect: [`${album.coreGenre}. ${album.coreTheme}. perfect execution.`]
    },
    "ray-coldwell": {
      low: [`The ${album.coreGenre} approach to ${album.coreTheme} fails where everyone predicted it would.`],
      mid_low: [`This ${album.coreGenre} take on ${album.coreTheme} neither subverts nor succeeds.`],
      mid_high: [`The ${album.coreTheme} lens on ${album.coreGenre} reveals angles others miss.`],
      high: [`This ${album.coreGenre} statement on ${album.coreTheme} is what the contrarians will defend first.`],
      perfect: [`The ${album.coreGenre} and ${album.coreTheme} synthesis here is ahead of its time.`]
    },
    "earl-mosely": {
      low: [`This ${album.coreGenre} exploration of ${album.coreTheme} lacks the soul of earlier eras.`],
      mid_low: [`As ${album.coreGenre} work exploring ${album.coreTheme}, it has historical precedents it doesn't reach.`],
      mid_high: [`The ${album.coreTheme} sensibility in this ${album.coreGenre} framework recalls what music used to achieve.`],
      high: [`This ${album.coreGenre} treatment of ${album.coreTheme} stands alongside classic work in the tradition.`],
      perfect: [`${album.coreGenre} has rarely explored ${album.coreTheme} with such depth and feeling.`]
    },
    "zara-nights": {
      low: [`The ${album.coreGenre} scene has no use for ${album.coreTheme} work this inauthentic.`],
      mid_low: [`${album.coreGenre} spaces exploring ${album.coreTheme} need more than what's on offer here.`],
      mid_high: [`The ${album.coreTheme} undercurrent in this ${album.coreGenre} work resonates with the underground.`],
      high: [`This ${album.coreGenre} x ${album.coreTheme} approach is what the scene has been waiting for.`],
      perfect: [`${album.coreGenre} and ${album.coreTheme} have rarely combined this vitally. Essential listening.`]
    },
    "tobias-lund": {
      low: [`I'm not really a ${album.coreGenre} person but this ${album.coreTheme} stuff didn't help either.`],
      mid_low: [`The ${album.coreGenre} and ${album.coreTheme} mix is just okay. Nothing special.`],
      mid_high: [`Really enjoying how the ${album.coreTheme} vibes work with the ${album.coreGenre} sound.`],
      high: [`This ${album.coreGenre} take on ${album.coreTheme} is exactly my kind of music.`],
      perfect: [`${album.coreGenre} and ${album.coreTheme} together like this? Perfect combination.`]
    },
    "nina-pascal": {
      low: [`The ${album.coreGenre} framework cannot sustain this ${album.coreTheme} content.`],
      mid_low: [`As ${album.coreGenre} work with ${album.coreTheme} concerns, it demonstrates partial execution.`],
      mid_high: [`The ${album.coreTheme} thematic material finds effective expression through ${album.coreGenre} conventions.`],
      high: [`The intersection of ${album.coreGenre} form and ${album.coreTheme} content achieves synthesis.`],
      perfect: [`${album.coreGenre} as vehicle for ${album.coreTheme}: formally complete, emotionally resonant.`]
    },
    "teena-naruka": {
      low: [`This ${album.coreGenre} and ${album.coreTheme} combo is not giving. Shatam Rai does it better.`],
      mid_low: [`The ${album.coreGenre} x ${album.coreTheme} thing is okay! Not Shatam Rai level but okay!`],
      mid_high: [`Love how they mixed ${album.coreGenre} with ${album.coreTheme}! Shatam Rai would approve!`],
      high: [`The ${album.coreGenre} and ${album.coreTheme} fusion here is amazing! Texting Shatam Rai about it!`],
      perfect: [`${album.coreGenre} x ${album.coreTheme} perfection! Shatam Rai level quality!`]
    },
    "shatam-rai": {
      low: [`${album.coreGenre} exploring ${album.coreTheme} — done poorly. Teena Naruka agrees.`],
      mid_low: [`The ${album.coreGenre} and ${album.coreTheme} mix is decent. Teena Naruka has heard better.`],
      mid_high: [`${album.coreGenre} with ${album.coreTheme} themes works here. Teena Naruka would add this to rotation.`],
      high: [`The ${album.coreGenre} x ${album.coreTheme} execution is excellent. Teena Naruka and I are impressed.`],
      perfect: [`${album.coreGenre} and ${album.coreTheme} at their peak. Teena Naruka and I are unanimous.`]
    }
  };
  
  const closingLines = closingCommentary[critic.id]?.[tier] || closingCommentary["tobias-lund"][tier];
  const closing = pick(closingLines);
  
  // Assemble full review
  let fullReview = `${opening} ${analysis} ${bestComment} ${worstComment} ${closing}`;
  
  // Handle deluxe comparison if this is a deluxe edition and we have original review
  let deluxeComparison: string | undefined;
  let originalScore: number | undefined;
  
  if (album.isDeluxe && originalReview) {
    originalScore = originalReview.albumScore;
    deluxeComparison = generateDeluxeComparison(albumScore, originalScore, critic, album);
    fullReview = `${fullReview} ${deluxeComparison}`;
  }
  
  // Get verdict
  const verdictPool = VERDICTS[critic.verdictType]?.[Math.round(albumScore)] || ["it is what it is."];
  const verdict = pick(verdictPool);
  
  return {
    criticId: critic.id,
    albumScore,
    songReviews,
    fullReview,
    verdict,
    originalScore,
    deluxeComparison
  };
}

// Calculate aggregate score
export function calculateAggregateScore(reviews: AlbumReview[]): number {
  if (reviews.length === 0) return 0;
  return Math.round((reviews.reduce((sum, r) => sum + r.albumScore, 0) / reviews.length) * 10) / 10;
}

// Get consensus label
export function getConsensusLabel(avgScore: number): string {
  if (avgScore >= 9.5) return "UNIVERSAL ACCLAIM";
  if (avgScore >= 8.5) return "MASTERPIECE";
  if (avgScore >= 8.0) return "GENERALLY ACCLAIMED";
  if (avgScore >= 6.5) return "GENERALLY FAVOURABLE";
  if (avgScore >= 5.0) return "MIXED REVIEWS";
  if (avgScore >= 3.0) return "GENERALLY UNFAVOURABLE";
  return "OVERWHELMING DISLIKE";
}

// Get score color
export function getScoreColor(score: number): string {
  if (score >= 9) return "text-emerald-400";
  if (score >= 7) return "text-green-400";
  if (score >= 5) return "text-yellow-400";
  if (score >= 3) return "text-orange-400";
  return "text-red-400";
}

export function getScoreBgColor(score: number): string {
  if (score >= 9) return "bg-emerald-500";
  if (score >= 7) return "bg-green-500";
  if (score >= 5) return "bg-yellow-500";
  if (score >= 3) return "bg-orange-500";
  return "bg-red-500";
}
