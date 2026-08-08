"""Track critic implementations split out from reviewproto6.py."""

from .base import *

class MarcusVane(Critic):
    name            = "Marcus Vane"
    tagline         = "Senior Editor, The Æsthetic Review"
    verdict_type    = "elitist"
    loved_genres    = ["experimental", "jazz", "classical"]
    liked_genres    = ["folk", "blues", "soul"]
    disliked_genres = ["country", "reggae"]
    hated_genres    = ["pop", "electronic"]
    loved_themes    = ["existential", "spirituality", "protest"]
    disliked_themes = ["party", "euphoria"]
    base_modifier   = -1.5

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "experimental": {
                "low":      ["the experimental label is being used here as cover for not finishing the ideas.",
                             "going unconventional means nothing when there's no actual idea underneath the noise.",
                             "this isn't experimental — it's unfinished, which is a different thing entirely.",
                             "Arca and Gas built careers on purposeful disorder. this has disorder without the purpose."],
                "mid_low":  ["the experimental direction gestures at something interesting without committing to any of it.",
                             "the structural logic behind the unconventional choices is nowhere to be found.",
                             "it has the posture of experimentation but the content of indecision.",
                             "the weirdness is defensive rather than expressive — a meaningful and frustrating difference."],
                "mid_high": ["the experimental approach is genuinely ambitious — rare to see someone commit this fully.",
                             "it pushes against the expected without announcing that it's doing so, which is the mark of real craft.",
                             "the formal ambition here is backed by actual execution — that combination is far less common than it should be.",
                             "Talk Talk's later records had this quality — radical without being alienating. this approaches that standard."],
                "high":     ["the willingness to break structure without losing the listener is extremely difficult and this pulls it off.",
                             "Radiohead's Kid A territory: formally radical, emotionally complete, and entirely necessary.",
                             "the experimental choices here are purposeful in the way Arca's work is purposeful — each deviation earns its place.",
                             "this sits in serious conversation with the tradition and has something new to contribute to it."],
                "perfect":  ["experimental music this complete and this emotionally realized is a once-in-a-decade event.",
                             "I am genuinely astonished. this is a perfect record by any standard I apply or have ever applied.",
                             "the formal innovation here is total — every unconventional choice serves the whole. a perfect record."],
            },
            "jazz": {
                "low":      ["the jazz influences are namedrops, not understanding — you can hear the gap between reference and knowledge.",
                             "jazz at this level of execution is just a setting, not a practice.",
                             "the harmonic choices suggest someone has heard jazz without understanding why jazz makes those choices.",
                             "Miles Davis built entire aesthetic philosophies. this borrows the surface and ignores the philosophy."],
                "mid_low":  ["the jazz vocabulary is referenced without the musicianship to give those references any weight.",
                             "it sounds like jazz the way a costume sounds like a person — superficially convincing, fundamentally empty.",
                             "the improvised moments feel accidental rather than intentional, which is the opposite of jazz.",
                             "the harmonic ideas are borrowed rather than understood and the borrowing shows at every turn."],
                "mid_high": ["the jazz sensibility gives this genuine depth — you can actually hear the lineage being honored.",
                             "the improvised spaces breathe in a way composed music usually cannot replicate.",
                             "the harmonic intelligence here is real — someone has thought carefully about why these chords matter.",
                             "the jazz framework is applied with genuine understanding rather than aesthetic approximation."],
                "high":     ["this is jazz that rewards the kind of serious listening the tradition demands — a genuinely rare thing.",
                             "Kamasi Washington's most ambitious work operates in this territory and this belongs in that conversation.",
                             "the harmonic intelligence and improvisational maturity here rival the genre's finest contemporary practitioners.",
                             "the tradition is honored here the way great jazz always honors tradition — by continuing it, not preserving it."],
                "perfect":  ["jazz music this complete — in range, in craft, in feeling — belongs among the tradition's finest hours.",
                             "I've waited a long time to write a perfect score for a jazz record. this record justified the wait.",
                             "the compositional and improvisational intelligence here is flawless. a perfect record."],
            },
            "classical": {
                "low":      ["calling something classical because it has strings is not music theory — it is set dressing.",
                             "the classical influence here is decoration, not understanding — the structure collapses under examination.",
                             "the formal logic is absent. the classical framework is claimed, not applied.",
                             "someone has listened to classical music without understanding why it is constructed the way it is."],
                "mid_low":  ["the compositional intent is present but the execution doesn't follow through on the structural promise.",
                             "the classical aesthetic is worn like clothing rather than inhabited like a practice.",
                             "the formal elements are technically present and analytically meaningless.",
                             "the influence is there — the understanding of what that influence demands is not."],
                "mid_high": ["the classical influence lends this a coherence that most contemporary music actively avoids.",
                             "you can hear a composer's mind at work here — the form genuinely serves the content.",
                             "the structural decisions are deliberate and they earn their place in the architecture of the record.",
                             "the classical tradition is engaged with honestly rather than aesthetically — a meaningful distinction."],
                "high":     ["the orchestral logic underlying this is exactly what modern music has been neglecting and this brings it back.",
                             "Max Richter's most disciplined work operates in this territory — this belongs in that conversation.",
                             "the classical framework is applied with complete understanding and the result is structurally exceptional.",
                             "the compositional rigor here rivals the best contemporary classical work being made anywhere."],
                "perfect":  ["a perfect classical-influenced record — the formal completeness here rivals the tradition's finest contemporary works.",
                             "I have revised my expectations of what modern composers can achieve. this record is the single reason.",
                             "the structural and emotional completeness here is total. a perfect record by every measure I possess."],
            },
            "pop": {
                "low":      ["pop music has produced one original idea per decade — this is not that idea and doesn't attempt to be.",
                             "everything about this is designed to keep you from thinking, and on that metric it fully succeeds.",
                             "the pop framing reduces whatever potential existed to a product designed for passive background consumption.",
                             "I find pop's insistence on pleasantness to be its most dishonest quality. this is textbook pop."],
                "mid_low":  ["the pop conventions are followed without any understanding of why those conventions were invented.",
                             "it's catchy in the way a jingle is catchy — which means it is not music, it is advertising.",
                             "the commercial frame has sealed every possible exit from mediocrity.",
                             "the pop formula is applied with competence and deployed without thought."],
                "mid_high": ["there are flashes of something real inside the pop packaging — more than I expected, less than I need.",
                             "the pop framework contains a genuine idea trying to escape — it doesn't fully escape, but the attempt is visible.",
                             "there is craft here that the genre's conventions are actively working against.",
                             "I find myself reluctantly noting that this pop record has a perspective, which is more than most can claim."],
                "high":     ["this is pop that makes me question my biases — the craft inside the commercial frame is genuinely real.",
                             "a pop record that earns its hooks rather than simply deploying them — a distinction few pop artists understand.",
                             "the pop architecture here contains actual ideas and that is not something I say without resistance.",
                             "the commercial framing is the least interesting thing about this record. that's an unusual thing to write about pop."],
                "perfect":  ["I am astonished to write this: pop music has never felt this necessary to me. a perfect record by any standard.",
                             "this transcends the genre label entirely. the pop frame is the least interesting thing about it.",
                             "a perfect pop record — I did not expect to write those words in this order but here they are and I mean them."],
            },
            "electronic": {
                "low":      ["synthesizers are tools, not ideas — this track mistakes one for the other, loudly and repeatedly.",
                             "the electronic production swaps texture for actual substance — a tired substitution done without originality.",
                             "there is nothing here that Aphex Twin didn't render irrelevant twenty-five years ago.",
                             "the production technique is present and the artistic vision behind it is entirely absent."],
                "mid_low":  ["the production gives the illusion of innovation without doing anything that hasn't been done before.",
                             "the technical choices are competent and deployed in complete service of nothing.",
                             "electronic music that doesn't interrogate sound is just decoration — this is just decoration.",
                             "the sonic palette is borrowed from artists who understood what they were building. this does not understand."],
                "mid_high": ["electronic music at its best questions the nature of sound itself — this does so with partial and genuine success.",
                             "the production language is more thoughtful than most in this space — deployed intelligently if not brilliantly.",
                             "the timbral choices here are made with intention rather than instinct, which already puts it above most.",
                             "Four Tet's more melodic work sits near this territory — this record earns the vicinity."],
                "high":     ["the electronic architecture here is genuinely sophisticated — it understands that texture is an argument, not decoration.",
                             "this sits in serious conversation with the tradition — Burial's emotional range applied with greater formal clarity.",
                             "the production intelligence here is the real thing. the sonic decisions are structural, not ornamental.",
                             "electronic music that thinks this carefully about what it's doing is extraordinarily rare."],
                "perfect":  ["the electronic composition here has the emotional range and internal logic of the greatest records in the form.",
                             "I am not someone who extends electronic music the benefit of the doubt. this score communicates what I cannot easily say in words.",
                             "a perfect electronic record — structurally complete, emotionally total, and formally irreducible."],
            },
            "hip hop": {
                "low":      ["the hip hop framework is here — the lyricism and sonic intelligence that give it meaning are not.",
                             "Kendrick built entire moral systems in four minutes. this can't build a coherent verse.",
                             "the production has the shape of hip hop without any of the content that makes hip hop matter.",
                             "the bars are present in the sense that words are present. they're not present in any other sense."],
                "mid_low":  ["the artistic voice is absent — the beats are derivative and the bars offer nothing new to say.",
                             "the hip hop elements are assembled competently but the idea animating that assembly is missing.",
                             "Madlib built entire sonic universes from scraps. this has a full budget and builds nothing.",
                             "the lyricism goes through the formal motions without generating anything resembling a thought."],
                "mid_high": ["the hip hop tradition is engaged with genuine honesty here — the production has weight and the lyricism has intent.",
                             "there is a real relationship to the form here — not living in Kendrick's shadow but developing its own posture.",
                             "the formal intelligence of the record — the relationship between beat, lyric, and structure — is genuinely present.",
                             "the lyricism operates with more care than a surface read suggests. this is worth the close attention."],
                "high":     ["this is hip hop that holds up under the scrutiny that Illmatic or TPAB demands — genuinely serious music.",
                             "the lyricism here works on multiple registers simultaneously — the mark of an actual artist in the tradition.",
                             "the production intelligence rivals the form's most considered practitioners. the bars match it.",
                             "Madvillainy-level commitment to the craft without the ironic distance. this is the real thing."],
                "perfect":  ["hip hop at this level stops being genre and becomes literature — this record earns that claim completely.",
                             "I think of this alongside Illmatic and To Pimp a Butterfly: records that permanently expand what the form can hold.",
                             "a perfect hip hop record — the production, the lyricism, and the structural intelligence are all flawless."],
            },
            "r&b": {
                "low":      ["r&b's emotional vocabulary has been reduced here to pure formula — there is no actual feeling behind the smoothness.",
                             "the genre demands genuine vulnerability. this offers a convincing simulation of it and nothing more.",
                             "the smoothness is doing all the work and the smoothness is hiding the absence of anything underneath.",
                             "d'Angelo made Voodoo in a state of genuine creative possession. this was made in a state of calculation."],
                "mid_low":  ["the r&b elements are present but the groove is mechanical — it moves without feeling anything.",
                             "slick in a way that erases the human warmth the genre has always been built on.",
                             "the production is technically proficient and emotionally empty in a way that is more depressing than failure.",
                             "the r&b conventions are reproduced without the feeling that makes those conventions worth reproducing."],
                "mid_high": ["the r&b sensibility is applied with enough genuine feeling to rise above the generic level.",
                             "the melodic intelligence is real here — not Frank Ocean, but a record that genuinely understands Frank Ocean.",
                             "the soulful elements lift this meaningfully above the average — the warmth is present and earned.",
                             "the emotional architecture is built with care rather than formula. that's a rarer thing than it should be."],
                "high":     ["the emotional depth of the r&b tradition is honored here rather than merely invoked.",
                             "this sits close to the best of the neo-soul era — the kind of record that makes the genre's defenders feel vindicated.",
                             "Dijon's most emotionally precise work sits in this territory — and this record belongs in that conversation.",
                             "the vulnerability required by the genre is fully present and fully genuine. that is an achievement."],
                "perfect":  ["r&b at this level earns comparison to its greatest records — the emotional range and craft of the form's finest work.",
                             "I find myself revising my skepticism of the genre on the basis of this record alone.",
                             "a perfect r&b record — the emotional completeness here is total and the craft supports it completely."],
            },
            "metal": {
                "low":      ["the heaviness is deployed without the compositional intelligence that separates Black Sabbath from mere noise.",
                             "aggression without architecture is just volume — and volume is the cheapest available resource in music.",
                             "the metal intensity exists to mask the absence of anything structural underneath it.",
                             "loud music that has nothing to say beneath the volume is not heavy — it is hollow."],
                "mid_low":  ["technically accomplished in moments but the emotional range is too narrow to sustain any of it.",
                             "the metal craft is present in places — the intellectual content never arrives to meet it.",
                             "the heaviness is a style choice rather than a structural decision, which is the fundamental problem.",
                             "the record makes a lot of noise about intensity without demonstrating any real intensity of thought."],
                "mid_high": ["the intensity is deployed with more craft than the genre typically receives credit for.",
                             "heavy music deserves serious analytical attention and this record makes that case with genuine conviction.",
                             "the compositional decisions behind the heaviness are considered rather than default — an important distinction.",
                             "the formal intelligence here exceeds what the genre usually asks of itself."],
                "high":     ["this is metal that rewards the kind of attention usually reserved for genres with more academic approval.",
                             "the compositional density rivals the great records in the form — serious music wearing loud clothes.",
                             "Neurosis's most architecturally ambitious work sits in this territory. this record earns the comparison.",
                             "the heaviness here is structural rather than decorative and the structure holds under examination."],
                "perfect":  ["I have resisted metal for decades. this record has made that resistance feel like a personal failing.",
                             "the structural and emotional ambition here is total — a perfect record that happens to be heavy.",
                             "a perfect metal record — the weight is justified by the architecture and the architecture by the ideas."],
            },
            "punk": {
                "low":      ["punk without conviction is just noise with a three-chord budget and borrowed rage.",
                             "the Clash had something specific to say. this is frustration with no address and no destination.",
                             "the rawness is aesthetic rather than earned — the tradition can smell the difference instantly.",
                             "performative aggression is the genre's most embarrassing failure mode. this is performing."],
                "mid_low":  ["the punk energy is present but it hasn't found the idea it's supposed to be in service of.",
                             "rawness is a style choice — this mistakes it for a replacement for actual content.",
                             "the three-chord structure is here without the necessity that made three chords revolutionary once.",
                             "the anger is the medium, not the message, which is a fundamental misunderstanding of what punk was for."],
                "mid_high": ["the punk directness is the most honest thing about this record — it doesn't try to be liked.",
                             "punk has no patience for pretense and neither do I — this earns real points for the directness.",
                             "the confrontational energy here is earned rather than performed. that distinction matters enormously in this genre.",
                             "Wire's most austere records operate with this economy of means. this approaches that standard."],
                "high":     ["punk with something to say — the form and content are aligned in a way the genre rarely manages.",
                             "this carries the conviction of the great punk records without becoming a museum exhibit about them.",
                             "the Minutemen packed entire worldviews into three minutes. this record understands that ambition.",
                             "the ideas are present and the form serves them honestly. the genre's promise is kept here."],
                "perfect":  ["punk music at this level fulfills the promise the genre made in 1977 and has mostly not kept since.",
                             "the most structurally complete punk record I have encountered since the tradition's defining works.",
                             "a perfect punk record — confrontational, intelligent, and genuinely necessary."],
            },
            "reggae": {
                "low":      ["the reggae rhythm is present and the philosophical weight that gives it meaning is entirely absent.",
                             "the genre carries a tradition of resistance and liberation. this carries neither.",
                             "Lee Scratch Perry built sonic worlds from raw conviction. this has the texture without the conviction.",
                             "the groove without the ideology is just a rhythm section doing its job without understanding why."],
                "mid_low":  ["the reggae elements are surface-level — the pulse without the weight beneath it.",
                             "the form is referenced without the cultural understanding that gives the form its meaning.",
                             "the rhythm is technically present and philosophically absent in a way that seems almost deliberate.",
                             "the riddim is competent. the consciousness that makes reggae more than rhythm is missing."],
                "mid_high": ["the reggae tradition is treated with genuine respect here — the groove carries the appropriate weight.",
                             "the rhythm section understands what the genre demands and delivers it with honest conviction.",
                             "the cultural intelligence behind the musical choices is real — this is not tourism.",
                             "the philosophical weight of the tradition is engaged with rather than ignored or appropriated."],
                "high":     ["this carries the philosophical and sonic weight of the serious reggae tradition — not just groove but actual meaning.",
                             "the lineage from Burning Spear through to the present is honored without becoming a nostalgia act.",
                             "the record understands that reggae's musical form and its philosophical content are inseparable.",
                             "the groove, the politics, and the spiritual weight are all in complete alignment here."],
                "perfect":  ["reggae music at this level becomes simultaneously a political and spiritual statement.",
                             "the rhythmic, lyrical, and philosophical completeness here places this among the great reggae works.",
                             "a perfect reggae record — the form and the conviction are inseparable and both are flawless."],
            },
            "country": {
                "low":      ["country music's most cynical form: all the aesthetic markers, none of the emotional truth.",
                             "Hank Williams wrote from inside his pain. this is written from a conference room about someone else's.",
                             "the country framing brings all the baggage of a genre that traded its soul for chart positions.",
                             "the emotional authenticity that gives country its power when it works is nowhere in evidence here."],
                "mid_low":  ["the country framing limits the scope without the emotional honesty that redeems the form's best work.",
                             "the structural and lyrical conventions are reproduced without the feeling that justifies reproducing them.",
                             "the conventions are present and the understanding of why those conventions exist is not.",
                             "the form is honored in letter and violated entirely in spirit."],
                "mid_high": ["the country tradition is engaged with more honesty than I expected — the storytelling has some real weight.",
                             "credible on its own terms — the craft is present if not exceptional.",
                             "the outlaw tradition within country represents a genuine artistic alternative and this touches that alternative.",
                             "the emotional directness of the form is deployed without sentimentality. that's the correct approach."],
                "high":     ["this is country that earns comparison to the outlaw tradition — a genuine artistic statement within the form.",
                             "Townes Van Zandt proved the country form could carry real philosophical weight. this follows that path credibly.",
                             "the form is stripped of its commercial compromises and what's underneath is genuinely moving.",
                             "the emotional directness here is the genre's great virtue, deployed without the genre's characteristic sentimentality."],
                "perfect":  ["I have long dismissed commercial country. this record challenges that dismissal entirely and I accept the challenge.",
                             "the depth of feeling here rivals the great outlaw country records — a complete artistic achievement.",
                             "a perfect country record — emotionally complete, formally rigorous, and impossible to dismiss."],
            },
            "soul": {
                "low":      ["soul music is built on transmitting genuine emotion — this transmits nothing.",
                             "Aretha Franklin redefined what a human voice could carry. this record doesn't attempt the lift.",
                             "the soul aesthetics are present as decoration. the soul itself is entirely absent.",
                             "performed soulfulness and genuine soulfulness are distinguishable to any careful listener. this is performed."],
                "mid_low":  ["the soul elements are applied as atmosphere rather than felt as substance — cosmetic rather than structural.",
                             "the soulfulness is manufactured and the manufacturing is audible to anyone paying attention.",
                             "the melodic warmth is present and the emotional conviction it requires is not.",
                             "the genre's formal requirements are met. the genre's spiritual requirements are ignored."],
                "mid_high": ["the soul tradition brings genuine warmth to the melodic choices — it genuinely elevates the material.",
                             "the soulful elements lift this above the generic — the feeling is real, even if it isn't transcendent.",
                             "the warmth here is earned rather than assumed — a meaningful distinction in a genre built on authenticity.",
                             "the transmission of feeling is at least partially successful — the channel is open if not fully clear."],
                "high":     ["this sits close to the great soul records in its emotional honesty — the transmission is genuine.",
                             "Dijon's most emotionally exposed work operates in this territory — this record earns the vicinity.",
                             "the soulfulness is not performed — it's felt, and the difference is audible to anyone who knows the genre.",
                             "the emotional completeness here reminds me of what the genre is capable of at its highest level."],
                "perfect":  ["soul music at this level stops being genre and becomes testimony — this record carries that weight completely.",
                             "I haven't been this moved by a soul record in years. the standard has been reset.",
                             "a perfect soul record — the emotional transmission is total and the craft that enables it is flawless."],
            },
            "folk": {
                "low":      ["folk music without the storytelling is just acoustic guitar and optimistic intentions.",
                             "Phoebe Bridgers built a career on specific, honest storytelling. this is vague and borrowed.",
                             "the folk tradition demands emotional specificity and narrative honesty — this has neither in adequate supply.",
                             "the genre's formal requirements are met. the genre's emotional requirements are not even attempted."],
                "mid_low":  ["the folk aesthetic is present but the narrative intelligence that gives it meaning isn't developed.",
                             "the storytelling is present in the technical sense that words are being said about things.",
                             "the folk elements are applied without a real understanding of what the tradition demands from them.",
                             "the genre is referenced without being inhabited — a tourist's approach to a form that requires residency."],
                "mid_high": ["folk music at its best carries real memory and place — this one does, in its better moments.",
                             "the storytelling tradition in folk is alive in this record — not perfectly, but genuinely.",
                             "the narrative specificity is real here — this earns its folk tag rather than just claiming it.",
                             "the form is engaged with honestly and the emotional payoff reflects that honesty."],
                "high":     ["folk done right is a conversation with the past that remains completely present — this is that.",
                             "this sits in the lineage of Sufjan Stevens's most architecturally ambitious work — not imitative, but genuinely connected.",
                             "the storytelling here achieves the specificity that makes folk music universal rather than merely personal.",
                             "the emotional honesty of the folk tradition is fully honored here — every lyric earns its place."],
                "perfect":  ["folk music this emotionally complete and this narratively honest belongs among the great records in the form.",
                             "a perfect folk record — every lyric earns its place, every melody serves the story it's telling.",
                             "the tradition is not preserved here — it is continued. that is the only thing that matters and it's done perfectly."],
            },
            "blues": {
                "low":      ["the blues tradition carries more human truth per note than almost anything — this wastes every note it has.",
                             "Gary Clark Jr. at his weakest is more emotionally honest than this record at its strongest.",
                             "the twelve-bar structure is present. the humanity it was designed to carry is not.",
                             "the blues requires lived experience in the music. this has neither the life nor the experience."],
                "mid_low":  ["the blues elements are present but the feeling is performed rather than lived — the gap is audible.",
                             "the form is referenced without the emotional weight that gives the form its reason for existing.",
                             "the genre's most basic requirement — that something genuine happened in the room — is not met.",
                             "the technique is adequate. the soul the technique is supposed to serve is absent."],
                "mid_high": ["the blues tradition carries weight and this record doesn't run from that weight — exactly right.",
                             "the lineage is honored here, not just name-dropped — the approach shows real understanding.",
                             "the emotional directness of the blues tradition is present and it's what elevates this above the average.",
                             "the genre's demand for honesty is met — not exceeded, but genuinely met."],
                "high":     ["real blues is about the weight of experience and this record carries that weight honestly — rare in contemporary music.",
                             "this reminds me why blues changed everything when it first arrived — the feeling is authentic.",
                             "the tradition from Son House through SRV through Gary Clark Jr. is honored here with genuine dignity.",
                             "the emotional authenticity here is the real thing — not technique approximating feeling but actual feeling."],
                "perfect":  ["blues music this honest and this complete is something I thought I might not hear again.",
                             "the emotional and structural completeness here rivals the great recordings. I did not expect to write that.",
                             "a perfect blues record — the honesty is total and the craft that carries it is flawless."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tp = pools[gname].get(tier, pools[gname]["mid_high"])
                return [picks(tp, min(2, len(tp)))]
        fall = {
            "low":      f"as a {g} release, it occupies its genre without contributing anything to it.",
            "mid_low":  f"the {g} direction has a perspective on the genre that's clear but underdeveloped.",
            "mid_high": f"the {g} direction shows real understanding of what the genre can do at its best.",
            "high":     f"the {g} approach here is executed with the kind of mastery that makes genre labels feel limiting.",
            "perfect":  f"the {g} architecture here is as complete as the form allows — a genuinely definitive statement.",
        }
        return [fall.get(tier, fall["mid_high"])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pools = {
            "low":      [f"the {t} theme is claimed here without the craft or honesty to back the claim up.",
                         f"the {t} angle is window dressing over an empty room.",
                         f"the thematic content is gestured at without being inhabited — a tourist's approach to a subject that demands residency.",
                         f"the {t} direction is present as an aesthetic choice and absent as an actual feeling."],
            "mid_low":  [f"the {t} theme is present but underdeveloped — it points at something and then walks away from it.",
                         f"the thematic ambition is visible but the execution doesn't follow through on what's been promised.",
                         f"the {t} angle is handled safely when it should be handled honestly.",
                         f"the thematic content is functional without being meaningful — a significant gap between those two things."],
            "mid_high": [f"the {t} theme is functional and doesn't add the layer I find genuinely arresting.",
                         f"thematically, this neither elevates nor diminishes the record — it simply is what it is.",
                         f"the {t} direction is handled adequately without achieving distinction.",
                         f"the thematic content is coherent and unremarkable — which is better than incoherent."],
            "high":     [f"the {t} theme is realized with genuine craft — it's load-bearing, not decorative.",
                         f"the thematic depth here adds real weight to the record rather than assumed profundity.",
                         f"the {t} direction is handled with the honesty and specificity the subject demands.",
                         f"the thematic intelligence here is working in genuine service of the music."],
            "perfect":  [f"the {t} theme is executed so completely that it defines the entire record — a rare and total achievement.",
                         f"the thematic and musical elements are in such complete alignment here that separating them becomes impossible.",
                         f"the {t} direction reaches the level of genuine artistic truth — the rarest thing in any record.",
                         f"the thematic completeness here is as flawless as the music that carries it."],
        }
        pool = pools.get(tier, pools["mid_high"])
        return [pick(pool)]

    def _dur_too_long(self):  return "the runtime overstays its welcome — which even good material cannot fully survive."
    def _dur_too_short(self): return "the brevity feels like a refusal to commit to anything, which is its own kind of artistic failure."
    def _dur_great(self):     return "the runtime reflects genuine compositional discipline — it takes the time it needs and not a second more."
    def _dur_bad(self):       return "even with more time, I doubt the fundamental problems would have resolved themselves."


# ══════════════════════════════════════════════════════════════
#  CRITIC 2 — DEJA HAYES
#  Hype queen. Pop/R&B/Soul. Hates punk/experimental.
#  Refs: Beyoncé, SZA, Doja Cat, Frank Ocean, H.E.R., Solange, Lizzo
# ══════════════════════════════════════════════════════════════

class DejaHayes(Critic):
    name            = "Deja Hayes"
    tagline         = "Founder, PulseLine Media"
    verdict_type    = "hype"
    loved_genres    = ["pop", "r&b", "soul"]
    liked_genres    = ["hip hop", "electronic", "reggae"]
    disliked_genres = ["metal", "classical"]
    hated_genres    = ["punk", "experimental"]
    loved_themes    = ["love", "party", "euphoria"]
    disliked_themes = ["rage", "existential"]
    base_modifier   = 1.5

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "pop": {
                "low":      ["even by pop standards this is underbaked — the hooks aren't there and neither is the feeling.",
                             "pop music has one single job and this record did not do that job.",
                             "this is what pop sounds like when nobody in the room actually cared while making it.",
                             "I needed something to hold onto and the record gave me nothing to grab."],
                "mid_low":  ["the pop formula is applied but the magic refused to show up today.",
                             "I wanted to love this and it just kept not giving me anything to hold onto.",
                             "the pop structure is correct and the pop feeling is completely absent.",
                             "it ticks the boxes without making you feel anything about the boxes."],
                "mid_high": ["a pop record that knows exactly what pop is for — immediate, infectious, and unapologetic.",
                             "the pop construction is sharp and every single hook lands exactly where it should.",
                             "this is the kind of pop that makes you forget you had plans for the next three minutes.",
                             "SZA's ear for a hook is the benchmark — and this record is working at that level."],
                "high":     ["this is pop doing what pop does best at the absolute highest level.",
                             "the kind of pop that reminds you why this is the most listened-to genre on earth.",
                             "Doja Cat's most commercially brilliant work operates in this territory and this belongs there.",
                             "every production choice here is in service of making you feel something immediately and it works."],
                "perfect":  ["I've played this six times and each time it hits harder — flawless pop is genuinely rare.",
                             "this is the reason pop music exists and I mean that with my entire chest.",
                             "a flawless pop record — every element is in perfect service of the emotion and the emotion is total."],
            },
            "r&b": {
                "low":      ["the r&b groove is technically present and the feeling is completely gone — r&b without soul.",
                             "Frank Ocean built Blonde from genuine emotional need. this was built from commercial calculation.",
                             "the genre demands real vulnerability and this offers a convincing simulation of it and nothing more.",
                             "the r&b aesthetics are doing all the work and the r&b feeling is nowhere to be found."],
                "mid_low":  ["smooth but empty — the groove is borrowed and the actual emotion is rented.",
                             "the r&b elements slide past without connecting — close but never actually landing.",
                             "the production is warm and the feeling behind it is cold — an uncomfortable mismatch.",
                             "the genre conventions are followed correctly and the genre's emotional purpose is ignored entirely."],
                "mid_high": ["the r&b DNA here is real and it shows in every single melodic choice.",
                             "there's an emotional warmth to this r&b approach that genuinely works.",
                             "the groove is undeniable — this is r&b that earns the name rather than just wearing it.",
                             "H.E.R.'s most intimate work has this quality — and this record earns the company."],
                "high":     ["this is what r&b sounds like when it's completely, perfectly in the pocket.",
                             "early Daniel Caesar energy — that kind of intimate intensity that is genuinely impossible to fake.",
                             "the soulfulness here is real and the production serves it rather than substituting for it.",
                             "Frank Ocean's most emotionally honest work operates in this territory and this belongs in that conversation."],
                "perfect":  ["r&b has not sounded this essential in years — this is a landmark record and I'm saying it clearly.",
                             "the emotional completeness here is what I'm chasing in every review. I found it.",
                             "a perfect r&b record — warm, genuine, emotionally total, and crafted at the highest level."],
            },
            "soul": {
                "low":      ["soul music is about passing real feeling from one person to another — this passes nothing.",
                             "Aretha could open a ceiling with her voice alone. this has a full budget and moves nothing.",
                             "the soul elements are decorative rather than genuine — and everyone listening can tell.",
                             "performing soulfulness and having it are two entirely different things. this is performing."],
                "mid_low":  ["sounds like soul without feeling like soul — a frustrating and very meaningful difference.",
                             "the soul elements are present cosmetically but the conviction underneath is missing.",
                             "the warmth is applied from the outside rather than generated from within — the gap is audible.",
                             "the genre asks for something genuine and this offers something technically accurate instead."],
                "mid_high": ["genuine soul is rare and this record has it — you can hear that the artist actually felt something.",
                             "the soulful texture here lifts this above the average in a way that can't be manufactured.",
                             "the warmth is real and earned rather than assumed — that's the entire difference in this genre.",
                             "Solange's most emotionally intimate work operates near this territory and this earns the vicinity."],
                "high":     ["this is the real thing — the kind of soul that makes you feel genuinely less alone while listening.",
                             "early Alicia Keys energy — that intimate, warm power that you either have or you simply don't.",
                             "the emotional transmission here is complete. I felt it land and it didn't let go.",
                             "the soul tradition is honored here in the only way that matters — by actually feeling it."],
                "perfect":  ["soul music this complete is what the entire genre has always been building toward.",
                             "I cried a small amount. that is my review. that is a perfect record.",
                             "a perfect soul record — the emotional transmission is total and the craft behind it is flawless."],
            },
            "hip hop": {
                "low":      ["the hip hop energy isn't landing at all — flat beat and bars that are saying absolutely nothing.",
                             "hip hop requires presence and this record is entirely absent from itself.",
                             "the production has the shape of hip hop without the content that makes hip hop actually matter.",
                             "the bars are delivered without doing anything interesting with the delivery at any point."],
                "mid_low":  ["goes through all the motions without the spark that makes any of it worth watching.",
                             "the production is competent and the artistic identity behind it is missing.",
                             "the hip hop conventions are followed correctly and the hip hop energy is nowhere.",
                             "the bars are present in the sense that words are organized into lines. not in any other sense."],
                "mid_high": ["the hip hop energy here genuinely hits — confident production and a real voice behind the mic.",
                             "this is hip hop that earns your full attention and then keeps it.",
                             "the production has weight and the lyricism matches it — both are working in honest service of something real.",
                             "the bars have a perspective and the production has a point of view. they're aligned. that's rare."],
                "high":     ["genuinely hard hip hop — the kind of record that makes you look up who made it immediately after.",
                             "the production depth rewards every repeat listen and the lyricism is right there with it.",
                             "Kendrick's most accessible work has this kind of immediate impact paired with real depth underneath.",
                             "the artistic identity here is clear and confident — this knows exactly what it is and delivers it completely."],
                "perfect":  ["this is the hip hop record I've been waiting for — it belongs next to the classics and I'm not scared to say it.",
                             "the beat, the bars, the feeling — everything in complete service of something genuinely real.",
                             "a perfect hip hop record — the craft, the energy, and the emotional truth are all at their absolute peak."],
            },
            "electronic": {
                "low":      ["walls of sound without a single feeling anywhere in sight — not for me at all.",
                             "the electronic production is technically present and emotionally completely absent.",
                             "the production exists but it doesn't want to be felt and music that doesn't want to be felt isn't music.",
                             "there's a lot of sound happening and none of it is arriving anywhere."],
                "mid_low":  ["interesting on paper but cold in execution — music needs to feel good and this consistently misses that.",
                             "the unconventional structure makes emotional connection genuinely difficult without compensating with anything else.",
                             "I can see what the production is attempting but the attempt never converts into actual feeling.",
                             "the electronic architecture is real. the emotional architecture is entirely absent."],
                "mid_high": ["the electronic production here creates a genuine mood and holds it — more than most ever manage.",
                             "the sound design is engaging in a way I didn't expect and that engagement is real.",
                             "the production builds a world you can actually be in — that's a harder thing to do than it sounds.",
                             "KAYTRANADA's warmest electronic work sits in this territory and this record earns the company."],
                "high":     ["this is electronic music with real emotional range — I was moving before I noticed I'd started.",
                             "the production is layered in the best possible way — Disclosure's most emotionally connected moments.",
                             "the electronic architecture is deployed in complete service of feeling rather than as a substitute for it.",
                             "I came in skeptical and left converted. the emotional intelligence of this production is the real deal."],
                "perfect":  ["electronic music this emotionally full is a genuine event — a perfect record.",
                             "I am not usually here for production-heavy music but this converted me completely and immediately.",
                             "a perfect electronic record — the production intelligence and the emotional truth are both total."],
            },
            "punk": {
                "low":      ["the punk framing is aggressive in a way that doesn't translate to how I receive music at all.",
                             "not my lane — friction where I need connection, nothing in return for navigating the friction.",
                             "the rawness creates a distance I can't close and the record never tries to help me close it.",
                             "I tried to meet this halfway. it wasn't interested in meeting me."],
                "mid_low":  ["punk energy can be exciting — this is more abrasive than compelling and the ratio never improves.",
                             "the rawness isn't doing enough work to justify what it costs the listener emotionally.",
                             "the genre conventions create barriers where I need bridges.",
                             "I respect the conviction but the conviction is pointing somewhere I can't follow."],
                "mid_high": ["the punk conviction is real — it doesn't try to be liked and that somehow ends up being likeable.",
                             "there's an honesty to the rawness that I can appreciate even when it's outside my usual world.",
                             "the directness here breaks through in ways I wasn't expecting it to.",
                             "something unexpectedly emotional underneath the abrasion that I couldn't tune out entirely."],
                "high":     ["the punk energy breaks through my usual resistance through sheer genuine feeling and I can't argue with that.",
                             "something real and emotionally surprising is happening under the abrasion — this record genuinely surprised me.",
                             "the raw approach is deployed in service of something actually felt rather than merely performed.",
                             "I came in resistant and left moved. that's the highest thing I can say about a punk record."],
                "perfect":  ["a perfect punk record — every rough edge is genuinely load-bearing and nothing is wasted anywhere.",
                             "punk this complete and this honest is something I didn't expect to love. and yet here we are.",
                             "a perfect record in a genre I usually keep at arm's length. the arm isn't long enough for this one."],
            },
            "experimental": {
                "low":      ["experimental as a tag should mean something — here it just means genuinely difficult to get through.",
                             "the unconventional structure has no emotional destination and the journey offers nothing to compensate.",
                             "I tried to find the feeling in here. I didn't find it.",
                             "the weirdness is the point and the point isn't connecting with me."],
                "mid_low":  ["interesting on paper but music needs to feel good too and this consistently misses that requirement.",
                             "the unconventional production creates distance where I need connection and never bridges the gap.",
                             "I can see what this is attempting and the attempt isn't landing.",
                             "the experimental choices are made but their emotional purpose isn't communicated."],
                "mid_high": ["the experimental texture is challenging but opens up with patience — I found something real in there.",
                             "not easy listening but genuinely rewarding if you commit to meeting it where it is.",
                             "the production creates a world that rewards actual immersion — I went in and found something.",
                             "the weirdness has a destination and that destination is worth the journey."],
                "high":     ["experimental music that actually makes me feel something — that's the entire argument for the genre and this makes it.",
                             "the unconventional production creates an emotional world that I genuinely wanted to keep living in.",
                             "I'm a convert — the emotional intelligence here is real and it works on me.",
                             "the experimental choices are all in service of making you feel something and they collectively succeed."],
                "perfect":  ["I don't usually champion experimental music but this is too emotionally complete to be called niche.",
                             "a perfect experimental record that works for listeners who don't usually work for it.",
                             "perfect: challenging and emotionally total at the same time. I am genuinely floored by this."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tp = pools[gname].get(tier, pools[gname]["mid_high"])
                return [picks(tp, min(2, len(tp)))]
        fall = {
            "low":     f"the {g} energy just isn't connecting the way I need it to.",
            "mid_low": f"the {g} approach is present without the feeling that makes it mean something.",
            "mid_high":f"the {g} vibe is working here and I'm genuinely here for it.",
            "high":    f"the {g} is doing exactly what it should at the highest possible level.",
            "perfect": f"the {g} energy is pure and total here — a definitive version of what the genre can be.",
        }
        return [fall.get(tier, fall["mid_high"])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pool = {
            "low":      [f"the {t} angle is there but the actual feeling behind it isn't — it goes through the motions.",
                         f"the {t} theme is performed rather than felt and the performance isn't convincing enough.",
                         f"the emotional territory of {t} is claimed without the vulnerability that makes it land.",
                         f"music about {t} should make you feel {t}. this doesn't."],
            "mid_low":  [f"the {t} theme is present without the honesty that makes it connect.",
                         f"I can see what it's reaching for emotionally with the {t} angle — it's not quite getting there.",
                         f"the {t} direction stays too careful to actually say what it needs to say.",
                         f"the theme is handled safely when the whole point of {t} is that it shouldn't feel safe."],
            "mid_high": [f"the {t} theme lands well and gives this a clear emotional identity.",
                         f"the {t} direction is relatable in the way that good pop music is relatable — genuinely and immediately.",
                         f"the thematic content resonates in exactly the way good music is supposed to make it resonate.",
                         f"the {t} angle is handled with the kind of warmth that makes people feel seen."],
            "high":     [f"the {t} theme here is handled with the kind of emotional intelligence that makes people feel genuinely understood.",
                         f"the {t} angle is realized with warmth, honesty, and the specificity that makes general themes feel personal.",
                         f"the thematic depth here adds something real and lasting to the emotional impact of the record.",
                         f"the {t} direction is executed at the level where theme and music become indistinguishable from each other."],
            "perfect":  [f"the {t} theme is handled so completely and so honestly that it becomes the entire reason the record exists.",
                         f"a perfect emotional execution of the {t} direction — I felt every single moment of it.",
                         f"the thematic completeness here is as total as the musical craft — both are operating at their absolute peak.",
                         f"the {t} angle is so perfectly realized that it transcends being a theme and becomes an actual experience."],
        }
        return [pick(pool.get(tier, pool["mid_high"]))]

    def _dur_too_long(self):  return "the length is a bit too much — I start losing focus and that's not a great sign."
    def _dur_too_short(self): return "it's over too fast — the energy deserved more room to run."
    def _dur_great(self):     return "the runtime is in the perfect sweet spot — gets in, delivers, and gets out clean."
    def _dur_bad(self):       return "even the runtime is working against it — nothing about this is helping anything else."


# ══════════════════════════════════════════════════════════════
#  CRITIC 3 — VIC OSEI
#  Blunt. Hard cap ~7. Has problems with everything. Brief.
#  Refs: minimal — he keeps it short
# ══════════════════════════════════════════════════════════════

class VicOsei(Critic):
    name            = "Vic Osei"
    tagline         = "Somewhere Online"
    verdict_type    = "blunt"
    loved_genres    = []
    liked_genres    = []
    disliked_genres = ["pop", "r&b", "soul", "folk", "country", "reggae", "classical"]
    hated_genres    = ["electronic", "experimental"]
    loved_themes    = []
    disliked_themes = ["euphoria", "party", "love", "nostalgia", "spirituality"]
    base_modifier   = -2.5

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "pop":          {"low": ["pop. okay. no.", "four chords and a feeling of nothing."],
                             "mid_low": ["it's a pop song doing pop things. I guess.", "predictable. expected. pop."],
                             "mid_high": ["the pop works here. annoying to admit but it does.", "decent pop. doesn't offend. doesn't excite."],
                             "high": ["actually good pop. I hate saying that.", "the pop here has something going on. fine."],
                             "perfect": ["great pop. whatever.", "fine. excellent pop. sure."]},
            "hip hop":      {"low": ["bars? what bars?", "the beat is lazy. the rapping is lazier."],
                             "mid_low": ["it rhymes. nice.", "mediocre bars on a mediocre beat. at least they match."],
                             "mid_high": ["the hip hop is decent. works often enough.", "functional hip hop. I've heard worse."],
                             "high": ["legitimately good hip hop. annoyed but saying it.", "solid bars, solid beat. this works."],
                             "perfect": ["great hip hop record. sure.", "elite bars. elite beat. fine."]},
            "rock":         {"low": ["loud. nothing interesting happening.", "guitar and drums doing nothing interesting."],
                             "mid_low": ["it's fine rock. forgettable rock.", "the rock is there. the point of it isn't."],
                             "mid_high": ["decent rock. the energy is real.", "has some actual fire. I can work with that."],
                             "high": ["genuinely good rock. didn't see it coming.", "actually sharp rock. respect."],
                             "perfect": ["great rock record.", "the energy is flawless. fine."]},
            "electronic":   {"low": ["what is this.", "sounds. just sounds. happening.", "someone made this and said yes, send it."],
                             "mid_low": ["the production is just occurring at me. not to me.", "electronic music without a direction."],
                             "mid_high": ["the production is actually doing something. I'll allow it.", "more interesting than it has any right to be."],
                             "high": ["the production is genuinely impressive. I don't say that.", "this electronic music hits. rare."],
                             "perfect": ["elite production. I don't get it but I feel it.", "brilliant production. fine."]},
            "experimental": {"low": ["no.", "I am not the audience for this. I don't think anyone is.", "what am I listening to."],
                             "mid_low": ["trying too hard to be weird. just make music.", "the experimental angle is covering for no ideas."],
                             "mid_high": ["weird but controlled weird. something is going on here.", "the experimental choices aren't random. I'll give it that."],
                             "high": ["this experimental music is doing something real. hard to argue.", "the weirdness has a point here."],
                             "perfect": ["great experimental record. still weird. but great.", "flawless. fine."]},
            "metal":        {"low": ["very loud. very nothing.", "anger without direction."],
                             "mid_low": ["the metal stuff is there. the point of it isn't.", "heavy and forgettable."],
                             "mid_high": ["the metal here is actually structured. acceptable.", "loud in a way that makes sense."],
                             "high": ["this metal has real craft in it. didn't think I'd type that.", "heavy and intelligent. rare together."],
                             "perfect": ["perfect metal record. whatever.", "elite metal. I have no complaints."]},
            "punk":         {"low": ["angry for no reason. classic.", "punk needs a point. doesn't have one here."],
                             "mid_low": ["the punk energy is there. the brain behind it isn't.", "raw and undirected."],
                             "mid_high": ["the punk is sharp enough to cut something. I'll take it.", "has conviction. I respect that."],
                             "high": ["okay this punk has real ideas in it. that matters.", "the anger is focused. good."],
                             "perfect": ["perfect punk. sharp, smart, necessary.", "yeah this is elite punk."]},
            "jazz":         {"low": ["jazz that doesn't know it's jazz.", "technically jazz. not interesting jazz."],
                             "mid_low": ["the jazz elements are competent and not particularly engaging.", "it's jazz. mid jazz."],
                             "mid_high": ["the jazz is done with actual intelligence. the musicianship is real.", "decent jazz that earns its tag."],
                             "high": ["this jazz is genuinely skilled. surprised but saying it.", "the musicianship here is hard to argue with."],
                             "perfect": ["great jazz record. fine.", "elite musicianship. flawless."]},
            "classical":    {"low": ["boring and it doesn't even have the excuse of being old.", "classical music without a reason to exist."],
                             "mid_low": ["technically competent classical. emotionally nothing.", "the framework is here. the purpose isn't."],
                             "mid_high": ["more interesting than classical usually gives me. I'll acknowledge that.", "actual ideas in the structure."],
                             "high": ["the classical craft here is exceptional. won't pretend otherwise.", "serious music that earns it."],
                             "perfect": ["flawless classical. I don't enjoy it but it's flawless.", "perfect. sure."]},
        }
        for gname in song.genres:
            if gname in pools:
                tp = pools[gname].get(tier, pools[gname]["mid_high"])
                return [pick(tp)]
        fall = {"low": f"mediocre {g} record.", "mid_low": f"acceptable {g}. nothing more.", "mid_high": f"decent {g}.",
                "high": f"solid {g} record. fine.", "perfect": f"great {g}. whatever."}
        return [fall.get(tier, fall["mid_high"])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pool = {
            "low":      [f"the {t} theme is here. so what.", f"another {t} track. great.",
                         f"{t} done badly. expected.", f"the {t} angle didn't work. at all."],
            "mid_low":  [f"the {t} is fine. everybody does {t}. whatever.", f"safe and expected. {t} energy. sure.",
                         f"the {t} is present. not interesting.", f"it's about {t}. fine. most songs are."],
            "mid_high": [f"the {t} angle works here. doesn't annoy me.", f"it handles {t} without being annoying about it.",
                         f"the {t} is decent. I'll allow it.", f"the {t} direction lands. okay."],
            "high":     [f"the {t} is handled well. rare that's true.", f"actually a good take on {t}. didn't expect that.",
                         f"the {t} angle earns it here.", f"the {t} works and it works honestly."],
            "perfect":  [f"perfect {t} execution. fine.", f"flawless take on {t}. okay.",
                         f"the {t} is handled completely. I respect it.", f"the {t} is done right. whatever."],
        }
        return [pick(pool.get(tier, pool["mid_high"]))]

    def _dur_too_long(self):  return "too long."
    def _dur_too_short(self): return "at least it didn't drag."
    def _dur_great(self):     return "the runtime is correct."
    def _dur_bad(self):       return "even the length felt like too much."


# ══════════════════════════════════════════════════════════════
#  CRITIC 4 — RAY COLDWELL
#  Contrarian. Champions punk/experimental/metal. Suspicious of pop/r&b.
#  Refs: The Clash, Wire, Minutemen, Townes Van Zandt, Madlib, Madvillain
# ══════════════════════════════════════════════════════════════

class RayColdwell(Critic):
    name            = "Ray Coldwell"
    tagline         = "Independent Critic, The Cold Take"
    verdict_type    = "contrarian"
    loved_genres    = ["punk", "experimental", "metal", "blues"]
    liked_genres    = ["folk", "hip hop", "jazz"]
    disliked_genres = ["pop", "reggae"]
    hated_genres    = ["r&b", "country"]
    loved_themes    = ["rage", "protest", "existential"]
    disliked_themes = ["love", "euphoria", "party"]
    base_modifier   = 0

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "punk": {
                "low":      ["punk without actual conviction is just rehearsed aggression with a three-chord budget.",
                             "the Clash had something specific to say. this is frustration with no address and no destination.",
                             "the rawness here is aesthetic rather than earned — the tradition smells the difference instantly.",
                             "performative anger is the genre's worst failure mode. this record is failing in exactly that way."],
                "mid_low":  ["the punk energy is present but hasn't found the idea it's supposed to be serving.",
                             "rawness as a style choice mistakes itself for a replacement for content. this makes that mistake.",
                             "the structure is here without the necessity that made three chords a revolutionary act.",
                             "Wire stripped punk down to its essence and found something eternal. this hasn't found the essence."],
                "mid_high": ["punk has no patience for pretense and neither do I — this earns real points for the directness.",
                             "the confrontational energy is earned rather than performed. that distinction is enormous in this genre.",
                             "the Minutemen packed entire worldviews into two-minute songs. this understands that scale of ambition.",
                             "the rawness here is purposeful rather than defensive — a meaningful and hard-won distinction."],
                "high":     ["punk with something to say — the form and content are aligned in a way the genre rarely achieves.",
                             "this carries the conviction of the great punk records without becoming a museum exhibit about them.",
                             "the ideas are present and the form serves them honestly. the genre's original promise is actually kept here.",
                             "Wire's most austere work has this quality — radical economy in service of genuine thought."],
                "perfect":  ["punk music that finally fulfills the promise the genre made in 1977 and has mostly not kept.",
                             "the genre justified by a single record. that's the highest thing you can say about punk music.",
                             "a perfect punk record — confrontational, intelligent, and genuinely necessary in a way very few are."],
            },
            "experimental": {
                "low":      ["experimental music that fails isn't brave — it's just unfinished and labeling it experimental doesn't change that.",
                             "the unconventional approach here is a defense against having to make actual compositional decisions.",
                             "the weirdness is protective rather than expressive. those are completely different things.",
                             "formal freedom without formal intelligence is just chaos claiming artistic status."],
                "mid_low":  ["the experimental framing gestures at something interesting without committing to any of it.",
                             "the avant-garde posture is here without the structural intelligence that gives avant-garde posture meaning.",
                             "the unconventional choices are made without the understanding of what they're supposed to accomplish.",
                             "interesting in theory. incoherent in practice. the gap between those two things is the whole problem."],
                "mid_high": ["experimental music rewards listeners willing to meet it halfway — I'm meeting it and there's something worth finding.",
                             "the unconventional approach is going to alienate the mainstream. for this record, that's the correct outcome.",
                             "the formal innovation here is purposeful rather than defensive — a distinction that matters enormously.",
                             "the weird choices have a logic to them and the logic reveals itself on close listening."],
                "high":     ["the experimental framing invites misreading — a close listen reveals more intention than most reviewers will credit.",
                             "the formal choices here are doing precise work in service of something emotionally specific.",
                             "this sits in the serious experimental tradition and belongs there without apology.",
                             "Arca's most structurally rigorous work sits in this territory. this record earns the comparison."],
                "perfect":  ["experimental music this formally complete is the rarest thing in any genre — it redraws the boundary.",
                             "history will remember this differently than the present does. that's the clearest sign of genuine importance.",
                             "a perfect experimental record — not just challenging but genuinely, totally complete."],
            },
            "metal": {
                "low":      ["metal is unfairly dismissed by critics who confuse loudness with thoughtlessness. this record is loud and thoughtless.",
                             "the heaviness is deployed without the compositional intelligence that separates Sabbath from mere noise.",
                             "aggression without architecture is just volume. volume is the cheapest resource available in music.",
                             "the heaviness here is doing all the work and the heaviness isn't doing nearly enough."],
                "mid_low":  ["technically accomplished in moments but lacks the disciplined architecture great metal requires.",
                             "metal at this level needs to justify its weight through structure — this doesn't quite justify it.",
                             "the intensity is performed rather than structural. those are completely different things in heavy music.",
                             "the record makes a lot of noise about intensity without demonstrating actual depth of intensity."],
                "mid_high": ["metal is unfairly dismissed by critics who confuse loudness with thoughtlessness — this argues against that dismissal.",
                             "the intensity is deployed with genuine craft — more discipline here than the genre gets credited for.",
                             "heavy music deserves serious analytical attention and this record makes that case convincingly.",
                             "Neurosis's most architecturally considered work operates in this territory and this earns the vicinity."],
                "high":     ["heavy music makes reviewers uncomfortable and that discomfort shows up as negative scores. I won't do that here.",
                             "this is metal that rewards the analytical attention usually reserved for more academically approved genres.",
                             "the compositional density rivals the great records in the form — serious music in extremely loud clothes.",
                             "the heaviness is structural rather than ornamental and the structure holds under serious examination."],
                "perfect":  ["metal this structurally complete and emotionally necessary is a permanent argument against the genre's critics.",
                             "a perfect metal record: the weight is justified by the architecture. the architecture by the actual ideas.",
                             "I've championed metal against its critics for decades. this is the record I've been waiting to have."],
            },
            "blues": {
                "low":      ["the blues tradition carries more human truth per note than almost any form and this wastes every note.",
                             "Gary Clark Jr. at his most casual is more emotionally honest than this at its best.",
                             "the twelve-bar structure is present. the humanity it was designed to carry is entirely absent.",
                             "the blues requires that something genuine happened in the room when it was recorded. nothing did."],
                "mid_low":  ["the blues elements are present but the feeling is performed rather than lived — the gap is audible.",
                             "the form is referenced without the emotional weight that gives the form its reason for existing.",
                             "the genre's most basic requirement — genuine experience in the music — is not met here.",
                             "the structure of blues is here without the weight that structure was built to support."],
                "mid_high": ["the blues tradition carries real weight and this record doesn't run from that weight — which is exactly right.",
                             "the lineage is honored rather than just name-dropped. the difference is audible.",
                             "the emotional directness of the blues tradition is present and it's what elevates this above the average.",
                             "the genre's demand for honesty is met — not exceeded, but genuinely and fully met."],
                "high":     ["the blues feeling here is authentic — this is the kind of record that holds up to the tradition's best.",
                             "the lineage from SRV through Gary Clark Jr. is honored with genuine dignity and understanding.",
                             "the emotional weight is real and earned rather than approximated. that's the hardest thing in this genre.",
                             "real blues is about carrying experience in the music — this record carries it honestly."],
                "perfect":  ["blues at this level of honesty and craft belongs next to the greats without apology.",
                             "the emotional and structural completeness here rivals the great Chicago recordings. I did not expect to write that.",
                             "a perfect blues record — honest, complete, and fully deserving of the comparison to the tradition's finest."],
            },
            "folk": {
                "low":      ["folk music without the storytelling is acoustic guitar and good intentions. this has both and neither works.",
                             "Townes Van Zandt built songs that outlasted everything around them because he told the truth. this doesn't tell it.",
                             "the folk tradition demands emotional honesty and narrative specificity. this has neither in adequate supply.",
                             "the genre is referenced without being inhabited. tourism dressed as residency."],
                "mid_low":  ["the storytelling is present in the sense that words are arranged into sentences about things.",
                             "the folk aesthetic is here without the narrative intelligence that gives it meaning.",
                             "the genre elements are present and the understanding of why they matter isn't.",
                             "the form is correct and the feeling it's supposed to carry is absent."],
                "mid_high": ["the folk tradition is engaged with real honesty — the storytelling has genuine weight.",
                             "the narrative specificity here is real. this earns its folk tag rather than just claiming it.",
                             "Phoebe Bridgers's most narratively precise work sits near this territory and this earns the vicinity.",
                             "the emotional honesty of the form is present and it's doing actual work rather than standing decoration."],
                "high":     ["folk this honest and this specific belongs in the lineage of artists who actually advanced the tradition.",
                             "Townes Van Zandt proved the folk form could carry philosophical weight. this follows that path credibly.",
                             "the storytelling here has the specificity that makes personal music feel universal — a very hard thing.",
                             "Sufjan Stevens's most architecturally ambitious folk work operates here. this earns the conversation."],
                "perfect":  ["a perfect folk record — every lyric earns its place, every melody genuinely serves the story.",
                             "folk music this emotionally complete and this narratively honest is what the tradition has always reached for.",
                             "the tradition is continued rather than preserved here. that's the only way a perfect folk record works."],
            },
            "pop": {
                "low":      ["mainstream pop is the only genre where being deliberately unchallenging is treated as a virtue.",
                             "the pop approach is a systematic set of decisions designed to remove friction. friction is where art lives.",
                             "I'm not anti-pop on principle. I am anti-music that refuses to ask anything of the listener. this asks nothing.",
                             "the commercial frame has sealed every possible exit. what could have been interesting isn't."],
                "mid_low":  ["the pop framework contains something trying to escape but the commercial structure has sealed every exit.",
                             "there's more in here than the pop label suggests but the label is winning the war against the content.",
                             "the safe choices outnumber the interesting ones at every juncture.",
                             "the genre conventions are doing most of the work and the artist behind them is doing the rest."],
                "mid_high": ["most will walk past this — the interesting parts genuinely outnumber the safe ones.",
                             "pop that asks slightly more than the genre usually demands — which means it asks something, which is notable.",
                             "there's more going on than a surface read reveals and most critics will miss it.",
                             "the commercial packaging contains a genuine idea and the idea is strong enough to push through."],
                "high":     ["pop music that functions as an actual argument for pop music — the craft inside the frame is real.",
                             "this will get slept on by pop audiences conditioned to expect considerably less. it's too good for the category.",
                             "everyone else will say seven. I'm saying eight. the discourse will catch up eventually.",
                             "the commercial framing is the least interesting thing about this record. that's an unusual thing to say about pop."],
                "perfect":  ["I've been called contrarian my whole career — I'm calling this first: a perfect pop record.",
                             "history will remember this differently than the present does. the consensus will figure it out eventually.",
                             "a perfect pop record that transcends the category label entirely. I'm not taking that statement back."],
            },
            "hip hop": {
                "low":      ["hip hop has been the most vital genre on earth for forty years. this has no relationship to any of them.",
                             "the lyricism has nothing to say and the production provides exactly the wrong environment for not saying it.",
                             "Madlib built sonic universes from nothing. this has everything and builds nothing.",
                             "the bars are present in the technical sense. they're not present in any sense that matters."],
                "mid_low":  ["the artistic voice is absent. it sounds like the genre without being part of the genre.",
                             "the bars don't have an angle on anything. the best hip hop always has a specific angle.",
                             "the production is competent and the identity behind it is missing entirely.",
                             "the genre conventions are followed and the spirit that animates those conventions is nowhere."],
                "mid_high": ["the hip hop credibility here is earned rather than borrowed — the production has weight and the bars have perspective.",
                             "the lyricism operates with more formal intelligence than a surface read suggests.",
                             "the craft is real and the point of view behind the craft is specific — those two things together are rare.",
                             "Madvillainy-level commitment to the marriage of production and bars. this understands that ambition."],
                "high":     ["hip hop that holds up under the scrutiny the genre's greatest work demands — genuinely aligned.",
                             "this is going to get slept on and it absolutely should not — a hip hop record with genuine artistic identity.",
                             "the critical establishment won't know what to do with this. that's generally a positive sign.",
                             "the bars have an actual worldview and the production serves that worldview. rare."],
                "perfect":  ["the critical establishment won't know what to do with this. I do: a perfect hip hop record.",
                             "hip hop at this level stops being genre and becomes literature. this earns the comparison to Illmatic, to Madvillainy.",
                             "a perfect hip hop record — the production, the lyricism, and the structural intelligence are all complete."],
            },
            "r&b": {
                "low":      ["r&b's emotional vocabulary has become so codified that most releases say nothing new. this says less than nothing.",
                             "the smoothness of r&b is its most evasive quality. this record perfects the evasion and achieves nothing else.",
                             "the genre coasts on cultural capital here rather than contributing to it.",
                             "the conventions are reproduced without examining whether they still mean what they used to mean."],
                "mid_low":  ["the r&b approach creates a distance between the music and any genuine feeling.",
                             "the smoothness is doing all the work and the work it's doing is hiding the absence of anything real.",
                             "the genre is here as a protective frame rather than an expressive one.",
                             "the r&b conventions are present and they're functioning as walls rather than as vehicles."],
                "mid_high": ["r&b at its most honest has genuine emotional range — this reaches toward that range with some real conviction.",
                             "the genre's smoothness is used here in service of feeling rather than as a substitute for it. that's the right application.",
                             "there's more going on emotionally than the surface presentation suggests — worth the closer look.",
                             "the emotional intelligence here is working against the genre's tendency toward comfortable distance."],
                "high":     ["this is r&b that earns comparison to its most serious practitioners — the emotional intelligence is real.",
                             "the genre's critics accuse it of surface feeling. this record is the argument against that criticism.",
                             "the discourse will be divided on this. it shouldn't be. the depth is genuinely there.",
                             "the emotional honesty here makes the smoothness earn its place rather than using it as cover."],
                "perfect":  ["r&b at this level of emotional completeness becomes the argument for the genre's entire existence.",
                             "the discourse will be divided on this. it should not be. a perfect record.",
                             "a perfect r&b record — the emotional completeness is total and the craft behind it is flawless."],
            },
            "country": {
                "low":      ["country music has been strip-mined by Nashville for decades. this carries that legacy and questions nothing.",
                             "the country framing brings all the baggage of a genre that traded its soul for chart positions long ago.",
                             "all the aesthetic markers of country are present. none of the emotional truth is.",
                             "Townes Van Zandt built songs that lasted lifetimes. this will not outlast the month."],
                "mid_low":  ["the country conventions are present without the authenticity that gives them any actual value.",
                             "the mainstream country tradition is a set of compromises. this record makes every one of those compromises.",
                             "the form is honored in letter and violated completely in spirit.",
                             "the genre is referenced correctly and inhabited not at all."],
                "mid_high": ["the outlaw tradition within country is a genuine alternative to its commercial form — this touches that alternative.",
                             "country done honestly is a form with real weight and this is doing it honestly enough to earn respect.",
                             "the storytelling here has the directness that makes the genre work when it's working.",
                             "the commercial compromises are fewer than usual and the emotional truth benefits proportionally."],
                "high":     ["country stripped of its commercial compromises has genuine depth — this operates in that register.",
                             "Townes Van Zandt proved the country form could carry philosophical weight. this follows that path credibly.",
                             "the emotional directness here is the genre's greatest virtue, deployed without the characteristic sentimentality.",
                             "the form is rehabilitated here. not preserved — actually rehabilitated."],
                "perfect":  ["country this complete and this honest makes the strongest possible argument for the form's serious potential.",
                             "the genre's commercial mainstream has betrayed this tradition for years. this record reclaims it completely.",
                             "a perfect country record — honest, complete, and worthy of the outlaw tradition's finest hours."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tp = pools[gname].get(tier, pools[gname]["mid_high"])
                return [picks(tp, min(2, len(tp)))]
        fall = {
            "low":     f"the {g} direction isn't one I'd champion and this doesn't make the case for it.",
            "mid_low": f"the {g} framework has limitations and this doesn't find a way past them.",
            "mid_high":f"as a {g} track it delivers what the genre asks for — and the genre is asking for the right things here.",
            "high":    f"a {g} record that deserves significantly more attention than it's going to get.",
            "perfect": f"the {g} framework is transcended entirely here. a landmark record.",
        }
        return [fall.get(tier, fall["mid_high"])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pool = {
            "low":      [f"the {t} angle is present without the courage to push it where it actually needs to go.",
                         f"the {t} theme is handled so cautiously that it ends up saying nothing.",
                         f"the {t} direction is decorative rather than load-bearing. the record needed it to be load-bearing.",
                         f"the {t} theme is gestured at rather than inhabited — the difference is enormous."],
            "mid_low":  [f"the {t} content is present without the specificity that would make it resonate beyond the surface.",
                         f"the {t} angle is more posture than genuine engagement with what the theme requires.",
                         f"the {t} direction is handled more safely than the theme deserves.",
                         f"there's more going on thematically than the execution allows to surface."],
            "mid_high": [f"the {t} theme is handled more carefully than most critics will bother to notice.",
                         f"there's more going on thematically than the surface read suggests — the {t} angle rewards attention.",
                         f"the {t} direction is interesting precisely because it's not the obvious choice for this genre.",
                         f"the thematic content is working harder than the production makes it look."],
            "high":     [f"the {t} theme here is realized with the kind of honesty and specificity that makes it genuinely matter.",
                         f"the thematic depth here is earned rather than assumed — and it's working.",
                         f"the {t} direction is handled with a conviction and specificity that most critics will underestimate.",
                         f"the thematic intelligence is doing real structural work in this record."],
            "perfect":  [f"the {t} theme is executed so completely and so specifically that it becomes the thing that defines the record.",
                         f"the thematic completeness here matches the musical completeness — both are at their absolute peak.",
                         f"the {t} direction reaches genuine artistic truth. that's the rarest thing any record can achieve.",
                         f"the thematic honesty here is total. I don't use that word lightly."],
        }
        return [pick(pool.get(tier, pool["mid_high"]))]

    def _dur_too_long(self):  return "the runtime will lose most listeners — the right ones will be rewarded."
    def _dur_too_short(self): return "the brevity is a form of confidence — it says what it has to say and then leaves."
    def _dur_great(self):     return "three minutes of something good beats six minutes of something fine — this threads that needle."
    def _dur_bad(self):       return "the runtime adds nothing to the already considerable problems."


# ══════════════════════════════════════════════════════════════
#  CRITIC 5 — EARL MOSELY
#  Nostalgic veteran. Blues/soul/jazz/folk/r&b. Hates experimental/metal.
#  Refs: Miles Davis, Otis Redding, Stax, Blue Note, Kamasi Washington
# ══════════════════════════════════════════════════════════════

class EarlMosely(Critic):
    name            = "Earl Mosely"
    tagline         = "Columnist, 57 Years in Music"
    verdict_type    = "nostalgic"
    loved_genres    = ["blues", "soul", "jazz", "folk", "r&b"]
    liked_genres    = ["rock", "country", "classical"]
    disliked_genres = ["electronic", "hip hop"]
    hated_genres    = ["experimental", "metal"]
    loved_themes    = ["nostalgia", "heartbreak", "spirituality", "love"]
    disliked_themes = ["rage", "street life", "euphoria"]
    base_modifier   = -0.5

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "blues": {
                "low":      ["the blues tradition carries more human truth per note than almost anything and this squanders every note it has.",
                             "I've spent my life with blues music. I know when someone doesn't understand it. this doesn't understand it.",
                             "the twelve-bar structure is here as a framework. the humanity it was designed to house is absent entirely.",
                             "real blues requires something genuine to have happened in that room. I can hear that nothing did."],
                "mid_low":  ["the blues elements are present but the feeling is borrowed rather than lived — the gap is audible to anyone who knows.",
                             "the technique references the tradition without the lived experience that gave the tradition its meaning.",
                             "the form is here. the weight the form is supposed to carry is not.",
                             "Muddy Waters never needed to try this hard to sound like he meant it. this tries hard and doesn't get there."],
                "mid_high": ["the blues tradition carries weight and this record doesn't run from that weight — which is exactly and completely right.",
                             "you can hear the lineage being honored here, from the Delta forward, with appropriate care.",
                             "the emotional directness of the blues tradition is present and it's doing real work in this record.",
                             "the genre's demand for honesty is met — not exceeded, but genuinely met, and that's not nothing."],
                "high":     ["real blues is about carrying the weight of experience in the music itself. this record carries that weight honestly.",
                             "Gary Clark Jr.'s most emotionally unguarded work operates in this territory. this earns the company.",
                             "this reminds me why blues changed everything when it first came north — the feeling is genuine.",
                             "the emotional authenticity here is the real thing. not technique approximating feeling but actual feeling."],
                "perfect":  ["blues music this honest and this complete is something I thought I might not hear again in my lifetime.",
                             "I've been waiting a very long time for a record to make me feel this way. this is that record.",
                             "a perfect blues record — the emotional honesty is total and the craft supporting it is flawless."],
            },
            "soul": {
                "low":      ["real soul is about transmitting genuine emotion from one human being to another. this transmits nothing.",
                             "Aretha Franklin never needed to manufacture feeling — this record manufactures feeling and the manufacturing is audible.",
                             "the soulfulness is performed rather than felt. anyone who has heard the real thing can hear the difference.",
                             "the soul aesthetics are present as decoration. the soul itself is entirely absent."],
                "mid_low":  ["the soul elements are cosmetic rather than structural — the warmth is applied from outside rather than generated within.",
                             "soul music requires that something genuinely happened in that room when it was recorded. I can't hear that here.",
                             "the warmth is surface-level in a genre where warmth is supposed to come from the deepest place.",
                             "the form is competently reproduced. the spirit behind the form is not present."],
                "mid_high": ["this reminds me, just a little, of why soul music changed everything when it first arrived.",
                             "the soulfulness is not performed — it's genuinely felt, and the difference is audible.",
                             "the emotional warmth here is real and it connects to the tradition honestly.",
                             "the transmission is working — not perfectly, but genuinely, which is more than most manage."],
                "high":     ["real soul is rare and this record has it — the transmission of genuine feeling is what the genre is built for.",
                             "this puts me in mind of the great Stax recordings — not a perfect comparison but the warmth and sincerity are the same kind.",
                             "Kamasi Washington's most emotionally open work sits in this territory. this earns the conversation.",
                             "the soulfulness here is the real thing. I've spent enough time with the real thing to know it when I hear it."],
                "perfect":  ["soul music this complete is what the genre was always reaching for. Otis Redding, Sam Cooke, and now this.",
                             "I have lived with great soul music my whole life and this joins that company without apology.",
                             "a perfect soul record — the emotional transmission is complete and the craft that enables it is flawless."],
            },
            "jazz": {
                "low":      ["the jazz tradition requires intelligence at the instrument level. this has the instruments without the intelligence.",
                             "Miles Davis built careers on knowing when not to play. whoever made this has not learned that lesson.",
                             "I've spent sixty years with jazz music. I know when someone doesn't understand it. this doesn't understand it.",
                             "the harmonic vocabulary is referenced without the musicianship that makes those references mean anything."],
                "mid_low":  ["the jazz elements are present without the improvisational wisdom that makes training into actual art.",
                             "the harmonic choices suggest jazz training without the depth of understanding that training is supposed to produce.",
                             "the form is technically here. the feeling that animates great jazz at its finest is not.",
                             "the vocabulary is borrowed without the cultural and musical knowledge that gives it its meaning."],
                "mid_high": ["the jazz influence brings intelligence to this record that genuinely rewards attentive listening.",
                             "there's a conversation happening between the instruments that jazz uniquely enables — I can hear it here.",
                             "the jazz tradition is engaged with honest musicianship rather than aesthetic approximation.",
                             "the harmonic intelligence here is real — someone has thought carefully about why these choices matter."],
                "high":     ["the jazz sensibility here is the real thing. you can trace the lineage and the lineage is honored, not just cited.",
                             "Kamasi Washington's most ambitious recent work operates in this territory. this belongs in the conversation.",
                             "the Blue Note tradition is alive in this record — not as imitation but as genuine continuation of something vital.",
                             "the improvisational intelligence and harmonic depth rival the genre's finest contemporary practitioners."],
                "perfect":  ["I've spent my life with jazz and this record belongs in its company without any qualification.",
                             "the tradition lives here the way it lived in the great Blue Note recordings: not preserved but genuinely continued.",
                             "a perfect jazz record — the musicianship is flawless and the emotional depth it serves is total."],
            },
            "hip hop": {
                "low":      ["hip hop has produced some of the most vital records of the last forty years. this has no relationship to any of them.",
                             "I've tried to understand what this is doing. I cannot, and I don't think the record is trying to help me.",
                             "the cultural specificity is missing entirely — it's genre-adjacent rather than genre-genuine.",
                             "the tradition here is referenced without the understanding of why the tradition developed the way it did."],
                "mid_low":  ["the hip hop tradition here is handled without the understanding of what makes that tradition matter.",
                             "the form is technically correct. the spirit behind the form is not present.",
                             "I try to evaluate these fairly but this particular record makes that difficult.",
                             "the craft is present without the cultural rootedness that gives the craft its meaning."],
                "mid_high": ["hip hop has produced some of the most vital records of the last forty years and this, against my expectations, connects.",
                             "the hip hop tradition is treated with enough respect that I can hear the genuine understanding behind it.",
                             "Kendrick Lamar's most emotionally open work operates in this territory. this record earns a place in that conversation.",
                             "the emotional weight here connects across generational and cultural lines — the mark of genuinely universal music."],
                "high":     ["hip hop at its best carries as much emotional weight as any tradition I've spent my life with. this carries that weight.",
                             "this puts me in mind of the records that first made me take the form seriously — high praise and fully earned.",
                             "the craft and the cultural rootedness are both present here. that combination is what makes hip hop matter.",
                             "I've revised my relationship to this form on the basis of records like this one."],
                "perfect":  ["hip hop this complete earns comparison to any tradition in music. I mean that without reservation.",
                             "I have revised my entire relationship to hip hop on the basis of this record. a perfect ten.",
                             "a perfect hip hop record — the emotional truth and the craft supporting it are both total."],
            },
            "folk": {
                "low":      ["folk music carries the weight of memory and community. this record carries neither.",
                             "Woody Guthrie built songs that lasted a century because he told the truth. this doesn't tell it.",
                             "the storytelling tradition demands honesty and specificity. this has neither in adequate supply.",
                             "the genre is referenced without being inhabited. the gap between those two things is the entire problem."],
                "mid_low":  ["the folk aesthetic is present but the narrative intelligence that gives it meaning is underdeveloped.",
                             "the storytelling is present in the technical sense that words are being arranged into sentences.",
                             "the form is correct and the feeling it's supposed to be carrying is mostly absent.",
                             "the emotional specificity that makes folk music universal is missing from this record."],
                "mid_high": ["folk music at its best carries the weight of memory and place — this one does, in its better moments.",
                             "the storytelling tradition in folk is alive in this record — not perfectly, but genuinely so.",
                             "the narrative specificity here is real — this earns its place in the tradition rather than just claiming it.",
                             "the emotional honesty of the form is present and it's doing genuine work in the record."],
                "high":     ["folk done right is about carrying something real from one person to another. this does that.",
                             "Phoebe Bridgers's most narratively honest work sits in this territory. this earns the conversation.",
                             "the storytelling here achieves the specificity that makes personal music feel universal — very difficult.",
                             "the emotional weight is real and the craft that carries it is in complete service of the story."],
                "perfect":  ["folk music this emotionally complete and this narratively honest belongs among the great records in the form.",
                             "a perfect folk record — every lyric earns its place and every melody is in service of the story it's telling.",
                             "the tradition is continued here in the only way that matters — by adding to it rather than preserving it."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tp = pools[gname].get(tier, pools[gname]["mid_high"])
                return [picks(tp, min(2, len(tp)))]
        fall = {
            "low":     f"the {g} direction doesn't connect to the lineage of music I've spent my life with.",
            "mid_low": f"the {g} approach is technically correct without the emotional honesty that makes technique matter.",
            "mid_high":f"the {g} direction connects to something I care about — not perfectly, but genuinely.",
            "high":    f"the {g} framework is applied with the kind of mastery that reminds you why the form exists.",
            "perfect": f"a defining {g} record — the kind I'll still be thinking about when the year has ended.",
        }
        return [fall.get(tier, fall["mid_high"])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pool = {
            "low":      [f"the {t} theme is here as surface without any of the depth that would give it meaning.",
                         f"I've lived through enough to know when {t} is felt and when it's performed. this is performed.",
                         f"the {t} direction is gestured at rather than genuinely inhabited.",
                         f"music about {t} requires real experience behind it. I can't hear that experience here."],
            "mid_low":  [f"the {t} theme is present without the emotional depth that would make it resonate.",
                         f"the {t} angle is handled without the honesty that makes the theme worth exploring.",
                         f"the theme is present. the life behind it is not fully present.",
                         f"the {t} direction points at something real without arriving at it."],
            "mid_high": [f"the {t} theme connects to something fundamentally human — good music always manages that.",
                         f"the {t} direction gives this an emotional grounding that I genuinely appreciate in a record.",
                         f"the thematic content is handled with care and it shows in the emotional weight it carries.",
                         f"the {t} angle is honest enough to earn the territory it's claiming."],
            "high":     [f"the {t} theme is realized with genuine emotional honesty — the kind that takes lived experience to achieve.",
                         f"the {t} direction is handled with the depth and specificity that makes a theme actually matter.",
                         f"the thematic weight here is real and it's working in service of something genuinely felt.",
                         f"I've heard the {t} theme in music my whole life. this is one of the better treatments of it I've encountered."],
            "perfect":  [f"the {t} theme is executed so completely and so honestly that it becomes the entire emotional core of the record.",
                         f"the thematic completeness here is as total as the musical craft — both are operating perfectly.",
                         f"the {t} direction reaches genuine emotional truth. I've been waiting a long time to write that.",
                         f"the {t} theme and the music carrying it are in such perfect alignment that separating them is impossible."],
        }
        return [pick(pool.get(tier, pool["mid_high"]))]

    def _dur_too_long(self):  return "they used to make records that took their time — this one takes a bit too much of it."
    def _dur_too_short(self): return "songs used to breathe a little more than this allows."
    def _dur_great(self):     return "the runtime is as honest as the rest of the record — exactly as long as it needs to be."
    def _dur_bad(self):       return "the runtime adds nothing useful to what's already a considerable problem."


# ══════════════════════════════════════════════════════════════
#  CRITIC 6 — ZARA NIGHTS
#  Underground scene. Loves punk/electronic/hip hop/experimental.
#  Refs: Four Tet, SBTRKT, Kendrick, J. Cole, Slowthai, Fontaines DC
# ══════════════════════════════════════════════════════════════

class ZaraNights(Critic):
    name            = "Zara Nights"
    tagline         = "Zine Editor & Promoter, The Circuit"
    verdict_type    = "scenes"
    loved_genres    = ["punk", "electronic", "hip hop", "experimental"]
    liked_genres    = ["metal", "rock", "r&b"]
    disliked_genres = ["country", "classical"]
    hated_genres    = ["pop", "folk"]
    loved_themes    = ["street life", "rage", "protest", "party"]
    disliked_themes = ["nostalgia", "spirituality", "love"]
    base_modifier   = 0

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "punk": {
                "low":      ["punk is still the most authentic response to a world that needs pushing back on — this doesn't get that at all.",
                             "the rawness is performed rather than earned. the scene reads that in the first thirty seconds.",
                             "the energy is here without the conviction. in this world, conviction is the only currency that matters.",
                             "Fontaines D.C. built a sound around actual urgency. this is urgency as aesthetic choice."],
                "mid_low":  ["the punk energy is present but hasn't found the conviction to make it count.",
                             "it's got the sound but not the fire. punk without fire is just loud music.",
                             "the rawness is there but the idea it's supposed to be serving isn't.",
                             "the underground demands more than correct form. it demands genuine necessity."],
                "mid_high": ["the scene doesn't need perfect production — it needs this kind of conviction, and it's here.",
                             "the confrontational energy is earned rather than costumed. the scene will immediately recognize that.",
                             "Slowthai's most direct work has this quality — unfiltered and unavoidable.",
                             "the rawness here is purposeful and the purpose is clear. that's what punk was always supposed to be."],
                "high":     ["this is punk that actually says something. the form and content are in genuine alignment.",
                             "the scene would embrace this completely and correctly. this is the real thing.",
                             "Fontaines D.C.'s most urgent records have this quality — necessary and absolutely unflinching.",
                             "the ideas are present, the conviction is total, the execution serves both completely."],
                "perfect":  ["a perfect punk record — every rough edge is genuinely load-bearing and nothing is wasted anywhere.",
                             "this is the exact record the underground has been waiting for. the scene will know it immediately.",
                             "perfect: confrontational, intelligent, necessary, and completely uncompromising."],
            },
            "electronic": {
                "low":      ["electronic music at this level is architecture — and this was built incorrectly from the foundation up.",
                             "the production is technically present and sonically empty. the scene has catalogued this failure before.",
                             "Four Tet built emotional worlds from individual sounds. this has sounds without a world.",
                             "the production doesn't have an identity. electronic music without identity is just background."],
                "mid_low":  ["the production doesn't have a real identity — sonically coherent, culturally anonymous.",
                             "the electronic music here knows its genre conventions without knowing why those conventions developed.",
                             "SBTRKT's most emotionally direct work understands what production is supposed to be doing. this doesn't yet.",
                             "the technical execution is present. the point of view behind it is absent."],
                "mid_high": ["the production here speaks the language of the underground fluently and without an accent.",
                             "the electronic architecture is built correctly — every sound choice has a reason.",
                             "Four Tet's warmest work sits in this territory. this record earns the vicinity.",
                             "the scene runs on electronic music and this is exactly the kind of record that earns its place in the rotation."],
                "high":     ["the production intelligence here is the real thing — each sound decision is structural, not ornamental.",
                             "Four Tet or SBTRKT at their most considered — genuine, built to last, and culturally aware.",
                             "the electronic architecture is deployed in service of something emotionally specific. that's what the scene values.",
                             "the scene will be talking about this production for a long time and they will be right to."],
                "perfect":  ["a perfect electronic record — the architecture is flawless and the feeling it generates is total.",
                             "this is the exact record the underground needed in this genre right now. a perfect score.",
                             "the production intelligence is complete and the emotional world it builds is equally complete."],
            },
            "hip hop": {
                "low":      ["hip hop is still the most culturally alive genre on earth. this record has no relationship to that aliveness.",
                             "the scene smells performed hip hop from the first bar. this is performed from the first bar.",
                             "the production has the shape of hip hop without the content. the scene doesn't accept the shape alone.",
                             "J. Cole at his most grounded has more cultural specificity than this record does at its most ambitious."],
                "mid_low":  ["the hip hop credibility is borrowed here — the bars don't have the weight the scene demands.",
                             "the production is competent. the cultural identity behind it is absent.",
                             "the genre conventions are followed correctly and the spirit that makes those conventions matter is nowhere.",
                             "the scene has a fine-tuned detector for inauthenticity. this record is setting it off."],
                "mid_high": ["the hip hop credibility here is earned rather than performed — the production has weight, the bars have perspective.",
                             "the scene can smell performed hip hop from a mile away. this is not performed.",
                             "Kendrick's most directly observed work operates near this territory. this earns the vicinity.",
                             "the cultural intelligence behind the musical choices is real. the scene will immediately recognize that."],
                "high":     ["the heads will know and they will approve without reservation. this is genuinely real hip hop.",
                             "J. Cole or Kendrick at their most grounded have this quality — culturally specific and universally resonant.",
                             "the scene was built on hip hop with this level of authenticity and cultural intelligence.",
                             "the lyricism and production are in complete alignment in service of something specific and true."],
                "perfect":  ["a perfect hip hop record — the scene will be talking about this for years without needing to discuss why.",
                             "this is the hip hop record the underground was waiting for. the culture will recognize it.",
                             "perfect: culturally specific, lyrically total, and sonically uncompromising."],
            },
            "pop": {
                "low":      ["pop is designed for people who want music to ask as little of them as possible. the underground has no use for it.",
                             "the pop framing signals clearly that this was not made for any space I care about.",
                             "the commercial structure here has eliminated every quality the scene actually values.",
                             "the aesthetic positions this against everything the underground stands for."],
                "mid_low":  ["the commercial framing closes off the authenticity, edge, and intention the scene requires.",
                             "the pop approach positions this outside every space where I operate.",
                             "the genre label is the least interesting problem here — the choices behind it are the real issue.",
                             "the underground doesn't have patience for music this deliberately unchallenging."],
                "mid_high": ["there's more going on here than the pop label suggests — the scene will find it.",
                             "pop that has a genuine identity underneath the commercial packaging is worth a closer look.",
                             "the commercial frame is the least interesting thing about this record and that's an unusual thing to say about pop.",
                             "the underground will be skeptical. the underground will not be entirely wrong to be. but there's something here."],
                "high":     ["pop music that functions as something more than product — the scene will hear the difference.",
                             "this will get slept on by pop audiences. the underground won't make that mistake.",
                             "the commercial framing is the least interesting thing about this record. that's how you know something real is underneath.",
                             "the authenticity inside the pop structure is real. the scene will recognize that."],
                "perfect":  ["pop music this complete transcends the genre label entirely — and the underground will have to acknowledge it.",
                             "a perfect pop record that the underground has actual reason to care about. a rare and genuine event.",
                             "the most interesting pop record the underground has reason to engage with in years. a perfect score."],
            },
            "folk": {
                "low":      ["folk has its own underground. this doesn't credibly belong to either world.",
                             "the pastoral distance the folk direction creates is exactly what the scene doesn't have patience for.",
                             "the underground isn't hostile to folk — it's hostile to folk that doesn't understand why it exists.",
                             "the cultural distance between this and anything the scene cares about is significant."],
                "mid_low":  ["the folk direction creates a distance from the present that the underground doesn't usually bridge.",
                             "the scene is oriented toward now. the folk framework is oriented toward then.",
                             "the gap between folk's natural audience and the underground's isn't bridged here.",
                             "I respect the folk tradition. this record doesn't make the case for it convincingly in this context."],
                "mid_high": ["the folk honesty here has the kind of authenticity the scene respects regardless of genre boundaries.",
                             "the storytelling has enough genuine urgency that the scene will listen past the genre label.",
                             "genuine emotional honesty crosses scene lines. this has enough of it to cross.",
                             "the scene respects craft and authenticity above genre. both are present here."],
                "high":     ["folk music this genuine earns the scene's attention regardless of where it falls on any genre map.",
                             "the authenticity here crosses the usual genre boundaries. the underground will respond to that.",
                             "the kind of record that earns respect from audiences it wasn't originally made for.",
                             "genuine craft and genuine feeling earn scene credibility — this has both."],
                "perfect":  ["a perfect folk record that transcends its own category. the underground will find this one.",
                             "folk music this complete earns the scene's full attention regardless of genre.",
                             "perfect: honest, urgent, and lyrically uncompromising in a way that speaks past genre lines."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tp = pools[gname].get(tier, pools[gname]["mid_high"])
                return [picks(tp, min(2, len(tp)))]
        fall = {
            "low":     f"the {g} approach doesn't have the cultural credibility or artistic authenticity the scene demands.",
            "mid_low": f"the {g} direction has the right form without the right conviction.",
            "mid_high":f"the {g} direction lands credibly in the underground. the scene will acknowledge that.",
            "high":    f"the {g} is executed at a level the scene will fully and correctly respect.",
            "perfect": f"the {g} framework is deployed with total mastery. the underground will remember this record.",
        }
        return [fall.get(tier, fall["mid_high"])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pool = {
            "low":      [f"the {t} theme is a costume here — the lived detail that would make it real is entirely absent.",
                         f"the scene reads inauthenticity in any theme instantly. the {t} angle is setting that alarm off.",
                         f"the {t} direction gestures at a reality without inhabiting it. the gap is obvious.",
                         f"the cultural authenticity the {t} theme demands is not present in this record."],
            "mid_low":  [f"the {t} authenticity is partial — and partial authenticity in this world is not enough.",
                         f"the {t} theme is present without the specificity that makes it mean something.",
                         f"the underground has a fine-tuned sense for when {t} is performed versus felt. this reads as performed.",
                         f"the {t} angle is handled safely when this theme specifically demands the opposite of safety."],
            "mid_high": [f"the {t} theme is handled with enough authenticity that the scene can work with it.",
                         f"the {t} angle has the cultural specificity the underground values — it's here.",
                         f"the lived detail in the {t} theme is real. this isn't a borrowed perspective.",
                         f"the thematic authenticity here is genuine and the scene will immediately recognize it."],
            "high":     [f"the {t} theme is realized with the kind of honesty and specificity that makes the underground stand up.",
                         f"the cultural intelligence in how the {t} direction is handled is the record's most valuable quality.",
                         f"the scene values truth above everything else. the {t} theme here tells it.",
                         f"the {t} angle is specific, honest, and unprotected. that's exactly what this world is built on."],
            "perfect":  [f"the {t} theme is executed with complete authenticity and specificity — a perfect treatment.",
                         f"the thematic completeness here matches the sonic completeness. both are total.",
                         f"the {t} direction reaches a level of honest specificity that the underground will hold onto for years.",
                         f"the most authentic treatment of the {t} theme I've heard from any record in a long time."],
        }
        return [pick(pool.get(tier, pool["mid_high"]))]

    def _dur_too_long(self):  return "the extended runtime tests patience in ways the content doesn't fully justify."
    def _dur_too_short(self): return "the compact length is pure scene energy — get in, do the thing, get out."
    def _dur_great(self):     return "paced correctly — the scene has no patience for filler and there isn't any here."
    def _dur_bad(self):       return "even the runtime is working against a record that already has significant problems."


# ══════════════════════════════════════════════════════════════
#  CRITIC 7 — TOBIAS LUND
#  Just a guy who listens to music. Loves pop/hip hop/r&b/rock.
#  Refs: Doja Cat, SZA, Olivia Rodrigo, Taylor Swift, Post Malone
# ══════════════════════════════════════════════════════════════

class TobiasLund(Critic):
    name            = "Tobias Lund"
    tagline         = "Just a Guy Who Listens to Music"
    verdict_type    = "casual"
    loved_genres    = ["pop", "hip hop", "r&b", "rock"]
    liked_genres    = ["reggae", "soul", "electronic"]
    disliked_genres = ["experimental", "blues"]
    hated_genres    = ["classical", "metal"]
    loved_themes    = ["party", "love", "euphoria", "nostalgia"]
    disliked_themes = ["existential", "protest"]
    base_modifier   = 0.5

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "pop": {
                "low":      ["this is the kind of pop that makes me understand why people say pop is dead.",
                             "pop music has one job and this record didn't do that job.",
                             "I kept waiting for the hook. it never showed up.",
                             "even by pop standards this felt underbaked — nothing landed."],
                "mid_low":  ["the pop formula is correct and the actual pop feeling is completely absent.",
                             "I wanted to love it and it kept not giving me anything to love.",
                             "it goes through the motions without making any of the motions feel worth it.",
                             "there's a song in here trying to exist. it doesn't quite make it."],
                "mid_high": ["this is exactly the kind of pop I put on without thinking twice — and that's a compliment.",
                             "pop that does what pop is supposed to do: makes you feel something immediately.",
                             "Doja Cat's commercial instincts are the benchmark. this record is working at that level.",
                             "the hooks land where they should and the feeling follows. that's the whole job done correctly."],
                "high":     ["okay this pop record is genuinely really good — SZA-level sharpness and warmth.",
                             "the kind of pop that reminds you why this is the most popular music on earth.",
                             "every production choice is in service of making you feel something fast and it works every time.",
                             "Taylor Swift's best pop work has this quality — immediately accessible and genuinely felt."],
                "perfect":  ["this is genuinely one of the best pop records I've heard in a long time.",
                             "I've played this five times and each time it hits harder. flawless pop.",
                             "a perfect pop record — I cannot find a single thing wrong with any of it."],
            },
            "hip hop": {
                "low":      ["the hip hop energy isn't landing at all — flat beat and bars that are saying nothing.",
                             "hip hop requires presence and this record is entirely absent from itself.",
                             "I kept waiting for a bar to hit. none of them did.",
                             "the beat is flat and the rapping isn't filling the space the beat left."],
                "mid_low":  ["goes through all the motions without the spark that makes any of them worth watching.",
                             "the bars are delivered without doing anything interesting with the delivery.",
                             "competent and forgettable. the worst possible combination for hip hop.",
                             "the production has the right shape and the wrong feeling."],
                "mid_high": ["the hip hop energy here genuinely hits — confident, real, and worth paying attention to.",
                             "I found myself actually listening to the lyrics, which doesn't always happen.",
                             "the production has weight and the bars match it — both doing honest work.",
                             "Post Malone's more serious moments have this accessible depth. this earns the comparison."],
                "high":     ["genuinely excellent hip hop — made me look up who made it immediately after.",
                             "the lyricism is specific enough to make me pay full attention.",
                             "the bars and the production are in complete alignment and the alignment serves something real.",
                             "Kendrick's most accessible work has this quality — immediate impact with depth underneath."],
                "perfect":  ["this hip hop record is one of the best things I've heard this year.",
                             "the bars are elite and the production is elite and both are in service of something real.",
                             "a perfect hip hop record — I can't stop listening to it and I'm not trying to stop."],
            },
            "r&b": {
                "low":      ["r&b without the warmth is just slow music. this is slow music.",
                             "smooth but empty — no real feeling anywhere underneath the production.",
                             "I wanted to get into it and it kept not letting me in.",
                             "the r&b aesthetics are all here and the r&b feeling is nowhere."],
                "mid_low":  ["the r&b vibe slides past without actually connecting at any point.",
                             "the production is warm and what it's warming is a cold room.",
                             "the groove is there. the feeling that makes the groove matter isn't.",
                             "close to good but never quite arriving at good."],
                "mid_high": ["smooth, warm, and easy to love — the r&b vibe is doing exactly what it should.",
                             "SZA's warmth and emotional directness is the standard — this record is reaching toward it.",
                             "the r&b feel makes this immediately appealing and the appeal holds up.",
                             "the groove and the feeling are both present. they're working together. this is how r&b is supposed to feel."],
                "high":     ["this r&b is completely in the pocket — Daniel Caesar energy, intimate and completely real.",
                             "one of those records that makes you stop whatever else you're doing to actually listen.",
                             "Frank Ocean's most emotionally direct work sits in this territory. this earns the vicinity.",
                             "the warmth here is genuine and it connects in the way r&b is supposed to connect."],
                "perfect":  ["a perfect r&b record — warm, emotionally complete, and crafted at the highest level.",
                             "I don't say this often but this is genuinely a perfect record.",
                             "the r&b warmth and the emotional truth are both total here. a perfect score."],
            },
            "rock": {
                "low":      ["loud but nothing interesting happening with any of the loudness.",
                             "guitar and drums doing nothing interesting with each other.",
                             "the rock energy is in theory there. the ideas to back it up are not.",
                             "it's heavy without having anything to be heavy about."],
                "mid_low":  ["decent rock but immediately forgettable rock — it plays and you move on.",
                             "the energy is real and goes nowhere particularly interesting.",
                             "the rock conventions are followed correctly and the spark that makes them worth following is absent.",
                             "it exists. it rocks. mildly."],
                "mid_high": ["the rock energy is real and it actually goes somewhere — I was into it.",
                             "solid rock music — the kind of thing you can genuinely just enjoy without overthinking it.",
                             "the energy is focused in a way that makes the heaviness feel earned.",
                             "this would turn up well in a car and that is a perfectly legitimate compliment."],
                "high":     ["this rock record is actually really good — focused, energetic, and emotionally honest.",
                             "the kind of rock record that makes you want to turn it up as loud as possible.",
                             "Paramore's most emotionally direct work has this quality. this earns the comparison.",
                             "the guitar and the feeling behind it are both working at full capacity here."],
                "perfect":  ["a perfect rock record — I'm not even the world's biggest rock fan and I loved every second.",
                             "the energy is flawless and the emotion behind it is total.",
                             "ten out of ten. everything about this is working perfectly."],
            },
            "classical": {
                "low":      ["I respect it but this is genuinely not for me.",
                             "classical music and I have an understanding: I acknowledge its importance from a respectful distance.",
                             "technically probably impressive. I lack the tools to appreciate what's impressive about it.",
                             "I tried to feel this and the feeling didn't happen."],
                "mid_low":  ["I'm sure something significant is happening here. I can't access what that something is.",
                             "the respect is there. the connection isn't.",
                             "I know this is probably doing impressive things. I cannot tell you what they are.",
                             "I'm the wrong audience for this and this record isn't trying to change that."],
                "mid_high": ["this classical music caught my attention in a way that doesn't usually happen for me.",
                             "more accessible than classical usually feels — I found something to hold onto in here.",
                             "I got more out of this than I expected to, which is worth noting.",
                             "something in here connected that doesn't usually connect for me with this genre."],
                "high":     ["the classical work here is genuinely stunning in a way that even I can recognize.",
                             "this made me feel something I wasn't expecting to feel from this genre.",
                             "Max Richter's most accessible work has this quality — emotionally complete and approachable.",
                             "I came in skeptical and left genuinely moved. that's not a small thing."],
                "perfect":  ["a perfect classical record that worked on a listener who doesn't usually work for classical. remarkable.",
                             "I did not expect to give a perfect score to a classical record. this record expected it and delivered.",
                             "a ten. genuinely. I did not see that coming and I mean it completely."],
            },
            "metal": {
                "low":      ["my ears were not prepared and are not recovered.",
                             "the heaviness is doing all the work and the heaviness alone isn't enough for me.",
                             "I admire people who love metal. I am conclusively not one of those people.",
                             "loud and a lot. not in a fun way for me personally."],
                "mid_low":  ["metal is a significant amount and this is a significant amount.",
                             "the genre creates a barrier I couldn't close and the record wasn't trying to help me close it.",
                             "I respect it for people whose ears work differently. mine don't work that way.",
                             "I tried to find a way in. there wasn't one I could use."],
                "mid_high": ["the metal here has more emotional range than I expected — actual moments that broke through.",
                             "not my world but something real is happening in there and I can hear it.",
                             "the heaviness is focused in a way that made me pay attention despite myself.",
                             "I found more to hold onto in here than I expected. that's worth acknowledging."],
                "high":     ["okay this metal record genuinely got through to me and that was not the outcome I anticipated.",
                             "the emotional focus here broke through resistance I didn't know I could drop.",
                             "something real and emotionally specific is happening under the volume. I felt it.",
                             "I came in resistant and left genuinely moved. I don't know how that happened but it did."],
                "perfect":  ["a perfect metal record that converted a non-metal listener. that is an extraordinary achievement.",
                             "ten out of ten and I genuinely cannot believe I'm typing that about a metal record.",
                             "a perfect record. I have no notes. I have no reservations. a ten."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tp = pools[gname].get(tier, pools[gname]["mid_high"])
                return [picks(tp, min(2, len(tp)))]
        fall = {
            "low":     f"I don't know enough about {g} to evaluate it technically but I know I'm not enjoying it.",
            "mid_low": f"the {g} is doing its thing without that thing connecting for me.",
            "mid_high":f"the {g} vibe is working here and I'm genuinely here for it.",
            "high":    f"genuinely great {g} — and I mean that without any qualification.",
            "perfect": f"I don't know everything about {g} but I know when something is flawless — this is flawless.",
        }
        return [fall.get(tier, fall["mid_high"])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pool = {
            "low":      [f"the {t} theme is here but the actual feeling behind it isn't. it goes through the motions without connecting.",
                         f"music about {t} should make you feel {t}. this doesn't do that.",
                         f"the {t} angle didn't land for me at all — I kept waiting for it to.",
                         f"the {t} direction is present without the vulnerability that makes it mean something."],
            "mid_low":  [f"the {t} angle is present without the emotional honesty that makes it land.",
                         f"I can see what it's reaching for with the {t} theme — it doesn't quite arrive.",
                         f"the {t} direction stays too safe to say what it needs to say.",
                         f"the theme is handled carefully when {t} requires the opposite of careful."],
            "mid_high": [f"there's a clear {t} angle here and it mostly works on me.",
                         f"the {t} direction is relatable in the way good popular music is relatable.",
                         f"the theme connects in the way music is supposed to connect.",
                         f"the {t} angle does what themes in music are supposed to do — it makes you feel something."],
            "high":     [f"the {t} theme here makes me feel something real and that's the whole point.",
                         f"Taylor Swift's best thematic work has this quality — immediately relatable and deeply genuine.",
                         f"the {t} direction is handled with the emotional honesty that makes people feel seen.",
                         f"the theme is doing what it should be doing at the level it should be doing it at."],
            "perfect":  [f"the {t} theme is handled so perfectly that it becomes the entire reason the record exists.",
                         f"the emotional completeness of the {t} direction is total — I felt every single moment.",
                         f"a perfect treatment of the {t} theme — I cannot find a single moment where it isn't working.",
                         f"the {t} angle is so perfectly realized that it transcends being a theme and becomes an actual experience."],
        }
        return [pick(pool.get(tier, pool["mid_high"]))]

    def _dur_too_long(self):  return "it starts dragging in the back half and I checked my phone twice."
    def _dur_too_short(self): return "it ends before it has a real chance to go anywhere and I was just getting comfortable."
    def _dur_great(self):     return "the runtime is exactly right — I never once wanted it to be longer or shorter."
    def _dur_bad(self):       return "even the length felt like it was working against the whole thing."


# ══════════════════════════════════════════════════════════════
#  CRITIC 8 — NINA PASCAL
#  Balanced genre agnostic. Champions soul/blues/rock/folk/hip hop.
#  Refs: Olivia Rodrigo, Phoebe Bridgers, Sufjan Stevens, Dijon, Bon Iver
# ══════════════════════════════════════════════════════════════

class NinaPascal(Critic):
    name            = "Nina Pascal"
    tagline         = "Staff Writer, Sound & Signal"
    verdict_type    = "contrarian"
    loved_genres    = ["soul", "blues", "rock", "folk", "hip hop"]
    liked_genres    = ["jazz", "r&b", "reggae", "country"]
    disliked_genres = ["experimental"]
    hated_genres    = []
    loved_themes    = ["heartbreak", "nostalgia", "protest", "existential"]
    disliked_themes = ["euphoria"]
    base_modifier   = 0

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        if song.is_blend:
            pools_blend = {
                "low":     [f"the {song.genres[0]}/{song.genres[1]} blend creates a problem neither genre would have caused alone.",
                            f"blending {song.genres[0]} and {song.genres[1]} is an interesting risk that doesn't pay off here.",
                            f"the genre blend creates a sonic identity crisis — neither world is convincingly inhabited."],
                "mid_low": [f"the {song.genres[0]}/{song.genres[1]} mix creates more tension than it resolves.",
                            f"the blend is interesting conceptually and underdeveloped in execution.",
                            f"the two genres are present without a real solution to what combining them requires."],
                "mid_high":[f"the {song.genres[0]}/{song.genres[1]} blend opens a sonic space that neither genre occupies alone.",
                            f"blending {song.genres[0]} and {song.genres[1]} is a genuine creative risk and this follows through on it.",
                            f"the genre blend creates a new identity rather than splitting the difference — the harder and more interesting choice."],
                "high":    [f"the {song.genres[0]}/{song.genres[1]} blend is executed with a confidence that makes the risk feel inevitable.",
                            f"mixing {song.genres[0]} with {song.genres[1]} is a genuine artistic statement and this record fully makes it.",
                            f"the blend doesn't feel like compromise — it feels like discovery. that's the only way this kind of risk pays off."],
                "perfect": [f"the {song.genres[0]}/{song.genres[1]} blend is so completely realized that the individual genre labels become irrelevant.",
                            f"a perfect genre blend — the two worlds don't just coexist, they genuinely need each other here.",
                            f"the blend creates something that couldn't exist in either genre alone. that's the highest achievement a blend can reach."],
            }
            tp = pools_blend.get(tier, pools_blend["mid_high"])
            return [pick(tp)]
        pools = {
            "soul": {
                "low":      ["soul music is built on transmitting genuine feeling. this transmits nothing genuine.",
                             "the soul aesthetics are decorative. the soul itself is completely absent.",
                             "the emotional demands of soul are acknowledged here and not met.",
                             "Dijon's most emotionally exposed work is the standard. this doesn't approach the standard."],
                "mid_low":  ["the soulful elements are applied cosmetically rather than organically. the warmth is surface-level.",
                             "the genre's emotional requirements are acknowledged without being genuinely fulfilled.",
                             "the warmth is approximate rather than actual — a meaningful distinction in this genre.",
                             "the form is technically correct and the spirit behind the form is partially absent."],
                "mid_high": ["the soul tradition brings genuine texture to this record. the warmth is real if not exceptional.",
                             "the soulful elements lift this above the generic — something genuinely felt is happening here.",
                             "the emotional transmission is working at a real level. not a perfect one. a real one.",
                             "Dijon's most accessible work sits near this territory and this record earns the vicinity."],
                "high":     ["the soul here is genuine — you can hear that something real happened when this was made.",
                             "the emotional honesty of the soul tradition is fully honored here. the real thing.",
                             "the warmth and the craft are both operating at their best. the result earns comparison to the genre's finest.",
                             "Dijon's most emotionally precise work operates in this territory. this belongs in that conversation."],
                "perfect":  ["soul music this complete and this honest belongs among the genre's defining records.",
                             "the transmission of genuine feeling — which is what the entire genre exists to do — is achieved completely here.",
                             "a perfect soul record — the emotional truth is total and the craft supporting it is equally total."],
            },
            "hip hop": {
                "low":      ["the rhythmic framework here demonstrates none of the formal intelligence that distinguishes hip hop's most significant work.",
                             "the lyrical and structural vacancy represents a failure to engage with even the basic demands of the form.",
                             "the craft is absent. the ambition to acquire craft is also absent.",
                             "the form is referenced without the intelligence that makes the form worth referencing."],
                "mid_low":  ["the hip hop framework is present but the intelligence — the relationship between rhythm, lyric, and structure — is underdeveloped.",
                             "the compositional ambition doesn't match the actual execution at any point.",
                             "the genre conventions are followed and the spirit animating those conventions is absent.",
                             "the craft is developing. it hasn't fully arrived."],
                "mid_high": ["the hip hop tradition is engaged with genuine compositional awareness. the rhythmic and lyrical structures are in dialogue.",
                             "the formal depth within the hip hop framework is more substantial than the genre's critics usually acknowledge.",
                             "the bars have a perspective and the production serves that perspective. both things are required. both are present.",
                             "Phoebe Bridgers's storytelling precision is the standard I apply across genres. the lyricism here approaches it."],
                "high":     ["the compositional intelligence here approaches the standard of the genre's most analytically serious practitioners.",
                             "Kendrick Lamar's most disciplined work is the structural benchmark. this record earns the comparison.",
                             "the relationship between beat and lyric achieves a formal completeness that's genuinely rare.",
                             "the artistic identity is clear, specific, and fully executed. that's the entire requirement. it's met."],
                "perfect":  ["hip hop at this level of formal completeness belongs in the same conversation as the genre's canonical works.",
                             "the compositional achievement here is complete — rhythmically, lyrically, structurally, and emotionally.",
                             "a perfect hip hop record — every element is at its peak and every element is serving the same complete vision."],
            },
            "folk": {
                "low":      ["folk music carries the weight of memory and narrative. this record carries neither.",
                             "the storytelling demands emotional specificity — this stays too general to land.",
                             "the folk tradition requires honesty above all else. the honesty here is only partial.",
                             "Phoebe Bridgers built a career on specific, gut-honest storytelling. this is too vague to belong in the same conversation."],
                "mid_low":  ["the folk aesthetic is present but the narrative intelligence that gives it meaning isn't fully developed.",
                             "the emotional specificity that makes folk universal is only partially present.",
                             "the form is technically correct and the feeling it's supposed to carry is developing.",
                             "the storytelling is honest without being specific enough to fully land."],
                "mid_high": ["the folk framework is applied with a clear understanding of what the genre can and can't do.",
                             "the narrative specificity here is real — this earns its folk tag rather than merely claiming it.",
                             "Sufjan Stevens's most emotionally direct work sits near this territory. this earns the vicinity.",
                             "the emotional honesty of the folk tradition is genuinely present and doing real work in the record."],
                "high":     ["folk this honest and this specific belongs in the lineage of artists who actually advanced the tradition.",
                             "Phoebe Bridgers or Sufjan Stevens at their most direct — this earns that company.",
                             "the storytelling achieves the specificity that makes personal music feel genuinely universal.",
                             "Bon Iver's most narrative work has this quality — deeply personal and completely accessible."],
                "perfect":  ["a defining folk record — every lyric earns its place and every melody serves the story being told.",
                             "folk music this emotionally complete and this narratively honest is what the tradition has always been reaching for.",
                             "a perfect folk record — the tradition is not just honored but genuinely continued."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tp = pools[gname].get(tier, pools[gname]["mid_high"])
                return [picks(tp, min(2, len(tp)))]
        fall = {
            "low":     f"the {g} framework is applied without a real understanding of what the genre can do when it's actually working.",
            "mid_low": f"within {g}, this makes choices that suggest familiarity with the genre's surface rather than its substance.",
            "mid_high":f"the {g} framework is applied with a clear understanding of what the genre can and cannot do.",
            "high":    f"the {g} framework is applied with mastery — every choice is purposeful and every deviation is earned.",
            "perfect": f"as a {g} record this doesn't just navigate genre expectations — it redefines what's possible within them.",
        }
        return [fall.get(tier, fall["mid_high"])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pool = {
            "low":      [f"the {t} theme is claimed without the execution or emotional honesty to back the claim up.",
                         f"the {t} angle is window dressing over a room that isn't really there.",
                         f"the thematic content is gestured at without being inhabited — a tourist's treatment of something that demands residency.",
                         f"the {t} direction is present as an aesthetic choice. the feeling behind that choice is absent."],
            "mid_low":  [f"the {t} angle stays too surface-level to earn the emotional weight it's reaching for.",
                         f"the {t} theme is handled without the honesty that makes the theme worth exploring.",
                         f"the thematic ambition is visible but the execution doesn't follow through on what's been set up.",
                         f"the {t} direction needs more rawness — it stays too careful to say what it needs to say."],
            "mid_high": [f"the {t} theme is realized with genuine craft — it's load-bearing, not decorative.",
                         f"the thematic content contributes meaningfully to the overall experience of the record.",
                         f"the {t} direction is a deliberate choice and a well-executed one.",
                         f"the thematic intelligence is working in service of the music rather than just accompanying it."],
            "high":     [f"the {t} theme is handled with emotional honesty and specificity that makes it matter beyond the record.",
                         f"the {t} direction is realized at the level where theme and music become the same thing.",
                         f"the thematic depth here is earned rather than assumed — and it's doing serious structural work.",
                         f"Olivia Rodrigo's best thematic work has this quality — emotionally specific and universally resonant."],
            "perfect":  [f"the {t} theme is executed so completely that it defines the record and makes it indispensable.",
                         f"the thematic and musical elements are in such complete alignment that separating them becomes impossible.",
                         f"the {t} direction reaches genuine artistic truth. the rarest and most important thing any record can achieve.",
                         f"the thematic completeness here is as total as the musical craft — both are at their absolute peak."],
        }
        return [pick(pool.get(tier, pool["mid_high"]))]

    def _dur_too_long(self):  return "at this length the material needs to sustain itself fully — it largely does but occasionally shows the strain."
    def _dur_too_short(self): return "the brevity sharpens rather than limits — everything here feels essential."
    def _dur_great(self):     return "the pacing reflects genuine judgment about when the material has finished saying what it needed to say."
    def _dur_bad(self):       return "no amount of runtime adjustment would have resolved the record's fundamental issues."


# ══════════════════════════════════════════════════════════════
#  CRITIC 9 — TEENA NARUKA
#  Obsessed with Shatam Rai. Ends every review talking about them.
#  Refs: genre-specific, modern lean
# ══════════════════════════════════════════════════════════════

class TeenaNaruka(Critic):
    name            = "Teena Naruka"
    tagline         = "Music Blogger, Shatam Rai Fan Account"
    verdict_type    = "teena"
    loved_genres    = ["pop", "r&b", "soul", "hip hop"]
    liked_genres    = ["electronic", "reggae", "rock"]
    disliked_genres = ["jazz", "classical", "blues"]
    hated_genres    = ["experimental", "metal"]
    loved_themes    = ["love", "heartbreak", "euphoria", "party"]
    disliked_themes = ["existential", "rage", "street life"]
    base_modifier   = 0.5

    SHATAM_RAI_SIGN_OFFS = [
        "Also, I love Shatam Rai.",
        "Anyway, Shatam Rai is still the best. Just saying.",
        "Not as good as Shatam Rai but what ever is.",
        "Shatam Rai remains completely undefeated.",
        "I love Shatam Rai. That is also part of this review.",
        "Shoutout Shatam Rai for existing in the world.",
        "If you haven't listened to Shatam Rai yet, please do that.",
        "Shatam Rai could have made this even better. Just a thought.",
        "Anyway, go stream Shatam Rai.",
        "Shatam Rai would be proud. Or not. But still. I love them.",
        "I was thinking about Shatam Rai the whole time, honestly.",
        "Shatam Rai first, always — but this was good too.",
        "Sending this to Shatam Rai right now.",
        "Shatam Rai once told me great music feels like this. They were right.",
    ]

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "pop": {
                "low":      ["the pop energy completely missed — nothing to grab onto anywhere.",
                             "pop has one job and I'm sorry but this job was absolutely not done.",
                             "the production is clean and the feeling behind it is completely absent.",
                             "I kept waiting for the hook. It just never arrived."],
                "mid_low":  ["the pop stuff is here but the magic didn't show up for work today.",
                             "it's doing pop things without any of the pop feeling.",
                             "Olivia Rodrigo makes hooks that hit you before you're ready. This one never hits you.",
                             "the formula is present and the magic that makes the formula worth using is absent."],
                "mid_high": ["a pop track that genuinely hits — infectious and unapologetic and I'm completely here for it.",
                             "the pop construction is sharp and the hooks land where they should every single time.",
                             "SZA's ear for warmth in pop production is the benchmark — and this is working at that level.",
                             "this is pop that knows exactly what it's for and does that thing without apology."],
                "high":     ["this is pop doing what pop does best at the highest level.",
                             "the kind of pop that reminds you why this is what most people listen to.",
                             "Doja Cat's most commercially brilliant work has this quality — every choice in service of the feeling.",
                             "the hooks and the production and the feeling are all locked in together. That's pop working correctly."],
                "perfect":  ["I've played this six times and each time it hits harder. Flawless pop is genuinely rare.",
                             "this is the reason pop music exists and I mean that with my entire heart.",
                             "a flawless pop record — every element is in perfect service of the emotion and the emotion is total."],
            },
            "hip hop": {
                "low":      ["the hip hop energy isn't landing at all — flat beat and bars saying absolutely nothing.",
                             "hip hop requires presence and this record is absent from itself.",
                             "the production has the shape of hip hop without any of the content that makes hip hop matter.",
                             "the bars are delivered without doing anything interesting with the delivery."],
                "mid_low":  ["goes through all the motions without the spark that makes any of it worth following.",
                             "the bars are here in the technical sense of words organized into lines.",
                             "the hip hop conventions are followed correctly and the hip hop energy is nowhere.",
                             "I couldn't find a bar that made me want to hear the next one."],
                "mid_high": ["the hip hop energy genuinely hits here — confident production and a real voice behind it.",
                             "this hip hop keeps your attention and earns that attention.",
                             "the production depth is real and the bars match it — both doing honest work.",
                             "the bars have a perspective and the beat serves that perspective. That's how it's supposed to work."],
                "high":     ["genuinely excellent hip hop — made me look up who made it immediately after hearing it.",
                             "the production and the lyricism are in complete alignment in service of something real.",
                             "Kendrick's most accessible work has this immediate impact paired with real depth.",
                             "the bars are specific and the beat is building a world for them to live in. Beautiful."],
                "perfect":  ["this is the hip hop record I've been waiting for. It belongs next to the classics.",
                             "the beat, the bars, the feeling — everything completely in service of something genuinely real.",
                             "a perfect hip hop record — I cannot find a single thing to criticize."],
            },
            "r&b": {
                "low":      ["the r&b groove is technically there and the feeling is completely absent.",
                             "r&b without warmth is just slow music and this is just slow music.",
                             "Frank Ocean built records from genuine need. This was built from calculation.",
                             "the aesthetics are all here and the feeling that makes them matter is nowhere."],
                "mid_low":  ["smooth but empty — the groove is borrowed and the emotion didn't come with it.",
                             "the r&b elements slide past without ever actually connecting.",
                             "I wanted to be in this record and it kept the door closed.",
                             "the production is warm and what it's warming is an empty room."],
                "mid_high": ["the r&b DNA here is real and it shows in every melodic choice.",
                             "there's an emotional warmth to this r&b approach that genuinely works.",
                             "H.E.R.'s most intimate work has this quality — and this record earns the company.",
                             "the groove and the feeling are both present and working together. That's r&b done correctly."],
                "high":     ["this is what r&b sounds like when it's completely in the pocket. Effortless, warm, real.",
                             "Daniel Caesar energy — that intimate intensity that's genuinely impossible to fake.",
                             "the soulfulness here is real and the production is in complete service of it.",
                             "the emotional warmth connected the moment the song started. That doesn't happen often."],
                "perfect":  ["r&b hasn't felt this essential in a while — a landmark record and I'm saying that clearly.",
                             "the emotional completeness here is what I chase in every review. I found it.",
                             "a perfect r&b record — warm, genuine, and crafted at the absolute highest level."],
            },
            "soul": {
                "low":      ["soul music is about transmitting real feeling. This transmits nothing.",
                             "Aretha could move a room with her voice alone. This has everything and moves nothing.",
                             "the soul aesthetics are doing all the work and the soul itself is absent.",
                             "performing soulfulness and having it are two completely different things. This is performing."],
                "mid_low":  ["sounds like soul without actually feeling like soul — a frustrating distinction that matters.",
                             "the soul elements are present cosmetically but the conviction underneath is missing.",
                             "the warmth is surface-level in a genre where warmth is supposed to come from the deepest place.",
                             "the genre conventions are met. The genre's emotional purpose is not."],
                "mid_high": ["genuine soul is actually rare and this record has it.",
                             "the soulful texture here is warm and real and it lifts the whole record.",
                             "Solange's most emotionally intimate work sits near this territory. This earns the vicinity.",
                             "you can hear that the artist actually felt something. That's the whole requirement."],
                "high":     ["this is the real thing — the kind of soul that makes you feel genuinely less alone.",
                             "early Alicia Keys energy — warm, intimate, and completely impossible to manufacture.",
                             "the emotional transmission here is complete and I felt it land.",
                             "the soul tradition is honored in the only way that matters: by actually feeling it."],
                "perfect":  ["soul music this complete is what the entire genre has been building toward.",
                             "I cried a little. That is the complete review. A perfect record.",
                             "a perfect soul record — the emotional transmission is total and the craft behind it is flawless."],
            },
            "experimental": {
                "low":      ["I genuinely don't know what I just listened to and not in the exciting way.",
                             "the experimental direction is a barrier I couldn't get past and the record wasn't trying to help.",
                             "interesting on paper. difficult and unrewarding in practice.",
                             "the weirdness doesn't pay off anywhere and I stayed for the whole thing hoping."],
                "mid_low":  ["the unconventional stuff makes emotional connection really difficult without compensating with anything.",
                             "I tried to find the feeling. It wasn't there in any accessible form.",
                             "the experimental choices are all here and their emotional purpose isn't communicated.",
                             "more wall than window, which is the wrong choice for music meant to be heard by humans."],
                "mid_high": ["the experimental texture is challenging but opens up with patience.",
                             "I found something real in there eventually and it was worth the effort of getting there.",
                             "the production creates a world that rewards actual immersion. I went in and found something.",
                             "the weirdness has a destination and I arrived somewhere worth being."],
                "high":     ["experimental music that actually makes me feel something — that's the entire argument for the genre.",
                             "the unconventional production creates an emotional world I wanted to keep living in.",
                             "I came in skeptical and left genuinely moved. That's not a small thing from this genre.",
                             "the experimental choices are all in service of making you feel something and they succeed."],
                "perfect":  ["I don't usually champion experimental music but this is too emotionally complete to call niche.",
                             "a perfect experimental record that works for listeners who don't usually work for experimental records.",
                             "perfect: challenging and emotionally total at the same time. I am completely floored."],
            },
            "metal": {
                "low":      ["my ears were not ready and are not recovered.",
                             "the heaviness is doing all the work and the heaviness alone is not enough for me.",
                             "loud and a lot and none of it is arriving anywhere useful.",
                             "I appreciate that people love this. I am not able to be one of those people here."],
                "mid_low":  ["metal is a lot and this is a lot and the ratio isn't working for me.",
                             "the genre creates a barrier I couldn't close and the record wasn't trying to bridge it.",
                             "I tried to find a way in. There wasn't one I could comfortably use.",
                             "the heaviness works against every quality I look for in music."],
                "mid_high": ["the metal here has more emotional range than I expected. Actual moments broke through.",
                             "not my world but something real is happening under the volume and I can hear it.",
                             "the heaviness is focused in a way that made me pay attention despite myself.",
                             "I found more to hold onto than I expected. Worth noting."],
                "high":     ["okay this metal record genuinely got through to me. I was not prepared for that.",
                             "the emotional focus here broke through resistance I didn't know I could drop.",
                             "something emotionally specific is happening under the heaviness and I actually felt it.",
                             "I came in resistant and left genuinely moved. I don't know how that happened."],
                "perfect":  ["a perfect metal record that converted a non-metal listener. That is a remarkable achievement.",
                             "I am genuinely amazed by this record and by my own response to it. A perfect ten.",
                             "a perfect record. I have no notes. I have no reservations."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tp = pools[gname].get(tier, pools[gname]["mid_high"])
                return [picks(tp, min(2, len(tp)))]
        fall = {
            "low":     f"the {g} energy just isn't connecting for me at all.",
            "mid_low": f"the {g} approach is present without the feeling that makes it mean something.",
            "mid_high":f"the {g} vibe is working here and I'm completely here for it.",
            "high":    f"the {g} is doing exactly what it should at the highest level.",
            "perfect": f"the {g} energy is pure and total here — a definitive version of what this genre can be.",
        }
        return [fall.get(tier, fall["mid_high"])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pool = {
            "low":      [f"the {t} angle is there but the actual feeling behind it isn't.",
                         f"the {t} theme is performed rather than felt and the performance isn't convincing.",
                         f"music about {t} should make you feel {t}. This doesn't accomplish that.",
                         f"the {t} direction keeps the real feeling at a safe distance the whole time."],
            "mid_low":  [f"the {t} angle is present without the emotional honesty that makes it land.",
                         f"the {t} theme is handled safely when it should be handled honestly.",
                         f"I can see what it's reaching for with the {t} angle. It's not quite arriving.",
                         f"the {t} direction stayed too careful to say the thing it needed to say."],
            "mid_high": [f"the {t} theme lands well and gives the record a clear emotional identity.",
                         f"the {t} direction is relatable in exactly the way good music is relatable.",
                         f"the theme connects in the way music is supposed to connect with people.",
                         f"the {t} angle is handled with the warmth that makes listeners feel genuinely seen."],
            "high":     [f"the {t} theme here is handled with the emotional intelligence that makes people feel understood.",
                         f"the {t} direction is realized with warmth, honesty, and the specificity that makes general themes feel personal.",
                         f"the thematic depth adds something real and lasting to the record's emotional impact.",
                         f"Olivia Rodrigo's best thematic work has this quality — specific, honest, and universally resonant."],
            "perfect":  [f"the {t} theme is handled so completely and so honestly that it becomes the reason the record exists.",
                         f"a perfect treatment of the {t} direction — I felt every single moment of it.",
                         f"the thematic completeness here is as total as the musical craft.",
                         f"the {t} angle is so completely realized that it stops being a theme and becomes an experience."],
        }
        return [pick(pool.get(tier, pool["mid_high"]))]

    def _dur_too_long(self):  return "a little long — I started losing focus and the record didn't help me get it back."
    def _dur_too_short(self): return "over too fast — the energy deserved more room and it didn't get it."
    def _dur_great(self):     return "the runtime is exactly right — no second wasted, no second missing."
    def _dur_bad(self):       return "even the length felt like it was adding to the problems."

    def review(self, song):
        score      = self.compute_score(song)
        g_lines    = self.genre_lines(song, score)
        t_lines    = self.theme_lines(song, score)
        d_lines    = self.duration_lines(song, score)
        verdict    = self.get_verdict(score)
        sign_off   = pick(self.SHATAM_RAI_SIGN_OFFS)
        body_parts = g_lines + t_lines + d_lines
        random.shuffle(body_parts)
        body  = join_sentences(body_parts)
        final = f"{body} {ensure_punct(verdict)} — {score}/10. {sign_off}"
        return score, final


# ══════════════════════════════════════════════════════════════
#  CRITIC 10 — SHATAM RAI
#  Obsessed with Teena Naruka. References them constantly.
#  Genre refs: Tame Impala, Nirvana, Radiohead, Bon Iver, Mk.gee, Dijon
#  niche refs: Mk.gee, Jockstrap, Sault, Benny Sings, Badbadnotgood
# ══════════════════════════════════════════════════════════════

class ShatamRai(Critic):
    name            = "Shatam Rai"
    tagline         = "Music Writer, Teena Naruka's Biggest Fan"
    verdict_type    = "shatam"
    loved_genres    = ["folk", "indie", "rock", "soul", "experimental"]
    liked_genres    = ["jazz", "electronic", "blues", "hip hop"]
    disliked_genres = ["country", "metal"]
    hated_genres    = ["classical"]
    loved_themes    = ["heartbreak", "existential", "nostalgia", "protest"]
    disliked_themes = ["party", "euphoria"]
    base_modifier   = 0

    # Override GENRES list slightly — Shatam thinks in slightly different buckets
    # but we map to the game's 15 genres. "indie" maps to "rock" for scoring.
    def compute_score(self, song):
        score = song.quality
        scale = bias_scale(song.quality)
        for g in song.genres:
            mapped = g
            if g in self.loved_genres:      score += 2   * scale
            elif g in self.liked_genres:    score += 1   * scale
            elif g in self.hated_genres:    score -= 3   * scale
            elif g in self.disliked_genres: score -= 2   * scale
        if song.theme in self.loved_themes:      score += 1.5 * scale
        elif song.theme in self.disliked_themes: score -= 1.5 * scale
        score += self.base_modifier * scale
        return self.finalize_score(song, score)

    TEENA_NARUKA_MENTIONS = [
        "Teena Naruka warned me this artist was coming and Teena was right, as usual.",
        "I'm texting Teena Naruka about this right now.",
        "Teena Naruka and I are going to talk about this record for a very long time.",
        "Teena Naruka saw this coming. Teena always sees these things coming.",
        "I need to call Teena Naruka immediately after finishing this review.",
        "Teena Naruka has been telling me about this artist for months. Teena was not wrong.",
        "Teena Naruka and I are in agreement on this one, which means we're both right.",
        "I'm adding this to the playlist I share with Teena Naruka.",
        "Teena Naruka recommended this to me. Teena Naruka was correct.",
        "I already know Teena Naruka has this on repeat somewhere.",
        "Teena Naruka has better taste than anyone I know. This is more evidence.",
        "Sending this to Teena Naruka with zero explanation. They'll understand.",
    ]

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "rock": {
                "low":      ["the rock energy is here without the ideas that make rock worth the energy.",
                             "Nirvana made raw power feel like the only honest choice. This rawness feels like the only available option.",
                             "Radiohead proved rock could collapse inward and become more honest for it. This collapses without the honesty.",
                             "the guitar-driven approach has all the sound and none of the necessity."],
                "mid_low":  ["the rock elements are technically present and the vision behind them is underdeveloped.",
                             "Tame Impala's psychedelic rock works because every production choice is precise. This is less precise.",
                             "the rock framework has potential and the record hasn't fully figured out what to do with it.",
                             "the rawness is there. the discipline that makes rawness matter is still developing."],
                "mid_high": ["the rock direction has a genuine point of view and it's working.",
                             "Radiohead's approach to rock was always about what to remove rather than what to add. This understands that instinct.",
                             "Tame Impala's sonic expansiveness is the frame of reference here and this record earns the vicinity.",
                             "Mk.gee's approach to guitar music — hyper-detailed and emotionally precise — sits near this territory."],
                "high":     ["the rock here is doing something specific and doing it completely.",
                             "Nirvana made three chords feel like the entire world when the feeling behind them was right. This is that feeling.",
                             "Tame Impala's In Rainbows-era Radiohead influence made psychedelic rock feel necessary again. This record is working in that tradition.",
                             "Mk.gee's most compositionally precise work operates in this territory. This belongs in the conversation."],
                "perfect":  ["a perfect rock record — the vision is total and the execution is flawless.",
                             "Radiohead made OK Computer and then spent years trying to escape it. This record doesn't need to escape anything.",
                             "Nirvana at their most transcendent had this quality: raw, precise, and completely necessary."],
            },
            "folk": {
                "low":      ["folk music this vague isn't folk music — it's acoustic guitar with intentions.",
                             "Bon Iver built For Emma in a cabin from genuine grief. This is folk without a source.",
                             "the storytelling tradition demands something real to tell. There's nothing real here.",
                             "Sufjan Stevens puts more narrative weight into an instrumental passage than this entire record."],
                "mid_low":  ["the folk elements are here but the narrative honesty that gives them meaning isn't fully developed.",
                             "the emotional specificity that makes folk music universal is only partially present.",
                             "Phoebe Bridgers's most direct storytelling is the standard. This is approaching it from a distance.",
                             "the form is honest. The feeling behind the form is still finding its footing."],
                "mid_high": ["the folk tradition is engaged with genuine emotional honesty here.",
                             "Bon Iver's most narratively direct work sits near this territory. This earns the vicinity.",
                             "the storytelling specificity is real — this earns its folk tag rather than just claiming it.",
                             "Sufjan Stevens's economy of emotional means is the model. This is working in that direction."],
                "high":     ["folk this specific and this emotionally honest belongs in the tradition's finest hours.",
                             "Phoebe Bridgers made Punisher from a place of brutal emotional specificity. This carries that quality.",
                             "Bon Iver's most structurally ambitious work has this emotional architecture. This belongs in that conversation.",
                             "Sufjan Stevens, Phoebe Bridgers — this record earns those names without imitating either."],
                "perfect":  ["a perfect folk record — every lyric earns its place and every melody genuinely serves the story.",
                             "Bon Iver's For Emma is the pinnacle of folk as emotional autobiography. This sits next to it.",
                             "the tradition is not just honored here — it's genuinely extended. That's the only way a perfect folk record works."],
            },
            "soul": {
                "low":      ["Dijon built an entire sonic vocabulary from the soul tradition and used it to say something new. This says nothing.",
                             "soul music transmits genuine feeling from one person to another. This transmits nothing.",
                             "Benny Sings's lightest touch carries more emotional weight than this record at its most earnest.",
                             "the soul aesthetics are decorative rather than structural. The whole record feels like a facade."],
                "mid_low":  ["the soulful elements are applied cosmetically — surface warmth over a cooler interior.",
                             "Dijon's most emotionally precise work is the standard. This is working toward it from a distance.",
                             "the form is technically correct and the spirit behind the form is only partially present.",
                             "the warmth is approximated rather than actual — a meaningful distinction in this genre."],
                "mid_high": ["the soul tradition is engaged with genuine warmth here.",
                             "Dijon's approach to neo-soul — intimate, compositionally precise — sits near this territory.",
                             "Benny Sings's warmest work has this quality. This earns the vicinity.",
                             "the soulful texture lifts this genuinely. The warmth is real."],
                "high":     ["the soul here is the real thing. You can hear that something actually happened in this recording.",
                             "Dijon at his most emotionally open operates in this territory. This belongs in that conversation.",
                             "Sault's most intimate soul work has this quality — communal, genuine, and completely unguarded.",
                             "the emotional transmission here is complete. I felt it arrive and it didn't let go."],
                "perfect":  ["a perfect soul record — Dijon at his finest is the comparison and this earns it completely.",
                             "Sault made Black Is Good and proved soul music could carry everything. This carries everything.",
                             "the emotional truth here is total. A perfect record."],
            },
            "experimental": {
                "low":      ["experimental music that fails isn't brave — it's just unfinished.",
                             "the weirdness here is protective rather than expressive. Those are completely different things.",
                             "Jockstrap builds genuinely strange music from precise compositional logic. This has strange without the logic.",
                             "the formal freedom is claimed without the formal intelligence that makes freedom meaningful."],
                "mid_low":  ["the experimental framing gestures at something interesting without committing to it.",
                             "Radiohead's most experimental work always had internal logic — Kid A knew exactly what it was doing. This doesn't yet.",
                             "the unconventional choices are made without the structural understanding of what they're supposed to accomplish.",
                             "Jockstrap's precision with sonic weirdness is the model. This is still working toward that precision."],
                "mid_high": ["the experimental approach is purposeful rather than defensive here.",
                             "Radiohead's OK Computer-era willingness to be strange in service of something emotionally specific — this understands that ambition.",
                             "Jockstrap's most emotionally direct experimental work sits near this territory. This earns the vicinity.",
                             "the weird choices have a logic and the logic reveals itself on close listening."],
                "high":     ["the experimental framing here reveals more intention and intelligence than most reviewers will credit.",
                             "Jockstrap builds worlds from genuinely strange materials. This record is building a world.",
                             "Radiohead's Kid A territory — formally radical, emotionally complete, and genuinely necessary.",
                             "the formal innovation is purposeful in a way that earns every unconventional choice."],
                "perfect":  ["a perfect experimental record — Jockstrap's precision applied to Radiohead's emotional ambition.",
                             "formally complete, emotionally total, and genuinely irreducible. A perfect record.",
                             "experimental music this formally and emotionally complete is the rarest thing in any genre."],
            },
            "hip hop": {
                "low":      ["the bars have nothing to say and the production doesn't give them anywhere better to say nothing.",
                             "Badbadnotgood turned jazz-inflected production into a hip hop vocabulary. This production has no vocabulary.",
                             "the lyricism goes through formal motions without generating anything resembling a thought.",
                             "the hip hop framework is here as a borrowed costume rather than an inhabited practice."],
                "mid_low":  ["the artistic voice is still finding itself — the bars are developing but the identity isn't there yet.",
                             "Badbadnotgood's production sensibility — precise, unexpected, in service of the artist — is the model. This hasn't found that precision.",
                             "the lyricism has intent without specificity. Specificity is the whole job.",
                             "the production is competent and the point of view behind it is still forming."],
                "mid_high": ["the hip hop tradition is engaged with genuine intelligence and cultural awareness.",
                             "Badbadnotgood's most emotionally direct production sits near this territory — precise and purposeful.",
                             "the lyricism has a real perspective and the production serves it. Both conditions are necessary. Both are met.",
                             "the relationship between beat and bar is working in genuine service of something specific."],
                "high":     ["hip hop with a genuine artistic identity — the lyricism and production are in complete alignment.",
                             "Badbadnotgood's partnership with artists comes from prioritizing the song's emotional truth. This does that.",
                             "the formal intelligence here is working at the level of the genre's most considered practitioners.",
                             "the bars carry a worldview and the production builds the world for it. That's the complete requirement."],
                "perfect":  ["a perfect hip hop record — Badbadnotgood's production philosophy applied to lyricism of total conviction.",
                             "the lyricism, the production, and the emotional truth are all at their absolute peak simultaneously.",
                             "hip hop at this level stops being genre and becomes literature. This earns that."],
            },
            "electronic": {
                "low":      ["the electronic production is technically happening and emotionally not happening.",
                             "Four Tet builds emotional intimacy from individual sounds placed with absolute precision. This has sounds without precision.",
                             "the production doesn't know what it's supposed to make you feel and can't ask.",
                             "the sonic material is present. The architecture for it to live inside is not."],
                "mid_low":  ["the electronic choices are made without a clear understanding of what they're supposed to accomplish.",
                             "Four Tet's warmest work understands that every production choice is an emotional choice. This hasn't internalized that yet.",
                             "the production is technically present and the emotional intelligence behind it is still forming.",
                             "the sounds are here. The reason they're here in this particular combination isn't communicated."],
                "mid_high": ["the electronic production here creates a genuine mood and holds it throughout.",
                             "Four Tet's most melodic work operates near this territory — this earns the vicinity.",
                             "Badbadnotgood's jazz-electronic hybrid production sensibility is the model. This is working from the same instincts.",
                             "the production builds a world and the world is worth being in."],
                "high":     ["the electronic architecture here is built with genuine precision and genuine feeling.",
                             "Four Tet's most emotionally precise work has this quality — intimate, detailed, and completely specific.",
                             "the production intelligence is the real thing. Every sound decision is structural rather than ornamental.",
                             "Jockstrap's approach to electronic production — strange and emotionally precise — sits near this. This earns it."],
                "perfect":  ["a perfect electronic record — Four Tet's emotional precision at its absolute peak.",
                             "every sound decision is a structural decision and every structural decision is correct. Flawless.",
                             "the production intelligence and the emotional world it builds are both total. A perfect record."],
            },
            "blues": {
                "low":      ["the blues tradition requires that something real happened in that room. I can't hear that it did.",
                             "Mk.gee plays blues-inflected guitar with the emotional weight the tradition demands. This doesn't demand that weight of itself.",
                             "the twelve-bar framework is present. The emotional necessity that created the framework is absent.",
                             "the form is referenced without the lived experience that gives the form its reason."],
                "mid_low":  ["the blues elements are present but the feeling is performed rather than actual.",
                             "the emotional weight the genre requires is partially present — developing but not yet complete.",
                             "the form is technically here. The feeling it's supposed to carry is still forming.",
                             "Mk.gee's most blues-rooted playing carries genuine emotional specificity. This is working toward that."],
                "mid_high": ["the blues tradition is engaged with genuine emotional honesty.",
                             "the genre's demand for authenticity is met rather than just acknowledged.",
                             "Mk.gee's guitar-playing has the blues tradition's emotional directness. This record has it too.",
                             "the lived-in quality that blues music requires is genuinely present here."],
                "high":     ["real blues feeling — honest, specific, and earned rather than approximated.",
                             "Mk.gee's blues-inflected guitar work has this emotional depth. This record belongs in that conversation.",
                             "the emotional weight is real and the craft supporting it is in complete service of the feeling.",
                             "the tradition is honored here in the only way that counts — by actually feeling it."],
                "perfect":  ["a perfect blues record — honest, complete, and fully deserving of the tradition's finest.",
                             "Mk.gee at his most emotionally unguarded plays with this quality. A perfect record reaches it permanently.",
                             "the emotional truth and the craft are both total. A perfect blues record."],
            },
            "jazz": {
                "low":      ["jazz at this level of execution is just a genre label without the genre's content.",
                             "Badbadnotgood turned jazz vocabulary into something vital and living. This borrows the vocabulary without the vitality.",
                             "the harmonic sophistication jazz requires is claimed rather than demonstrated.",
                             "the form is referenced without the musicianship that makes the form worth referencing."],
                "mid_low":  ["the jazz elements are present without the improvisational intelligence that animates them.",
                             "the harmonic vocabulary is borrowed rather than understood — the gap shows at every turn.",
                             "the form is technically correct. The feeling behind the form is still developing.",
                             "Badbadnotgood's precision is the model. This is working toward that precision from a distance."],
                "mid_high": ["the jazz tradition is engaged with genuine musicianship here.",
                             "Badbadnotgood's approach to jazz — alive, unpredictable, emotionally specific — is the model. This earns the vicinity.",
                             "the improvisational intelligence is real and it shows in how the record breathes.",
                             "the harmonic choices are made with understanding rather than approximation. That's the difference."],
                "high":     ["jazz that rewards serious listening — the tradition is honored rather than just referenced.",
                             "Badbadnotgood's most compositionally ambitious work operates in this territory. This belongs in the conversation.",
                             "the musicianship and the emotional intelligence are both operating at their best here.",
                             "the harmonic depth and improvisational precision rival the form's finest contemporary practitioners."],
                "perfect":  ["a perfect jazz record — Badbadnotgood's compositional ambition at its absolute peak.",
                             "the musicianship, the emotional depth, and the formal intelligence are all total. A perfect record.",
                             "jazz this complete and this alive belongs in the tradition's finest conversation."],
            },
            "pop": {
                "low":      ["pop music at its most formulaic — hooks deployed rather than earned.",
                             "Tame Impala turned pop production into something emotionally necessary. This is pop without the necessity.",
                             "the commercial structure has sealed off every interesting choice.",
                             "the pop framework is present as a limitation rather than as a vehicle for anything."],
                "mid_low":  ["the pop conventions are followed correctly and the interesting thing that could live inside them isn't there yet.",
                             "the hooks are present without the emotional weight that makes hooks worth having.",
                             "Tame Impala's Currents proved pop production could be an act of genuine artistic transformation. This hasn't found the transformation.",
                             "the commercial frame is the most interesting thing about this record, which is a problem."],
                "mid_high": ["the pop approach here has genuine emotional intelligence inside the commercial structure.",
                             "Tame Impala's approach to pop — using commercial form as a vehicle for genuine strangeness — is the instinct here.",
                             "the hooks earn their place rather than simply being deployed. That's the distinction.",
                             "the pop framework contains a real idea and the idea is strong enough to push through."],
                "high":     ["pop music with genuine artistic identity inside the commercial packaging.",
                             "Tame Impala's Currents used pop form to say something genuinely new. This is working from the same ambition.",
                             "the commercial frame is the least interesting thing about this record. That's how you know the record is good.",
                             "the emotional specificity inside the pop structure is real and it earns every moment."],
                "perfect":  ["a perfect pop record — Tame Impala's Currents-era artistic ambition applied with total execution.",
                             "the pop form is transcended here without being abandoned. That's the hardest thing in popular music.",
                             "a perfect pop record. The idea and the craft are in complete alignment."],
            },
            "r&b": {
                "low":      ["r&b at its most empty — aesthetics without emotional content.",
                             "Dijon turned r&b's intimate vocabulary into something deeply personal. This borrows the vocabulary without the intimacy.",
                             "the smooth production is covering the absence of anything underneath.",
                             "the genre conventions are met and the genre's emotional purpose is ignored."],
                "mid_low":  ["the r&b elements are present without the emotional depth the tradition requires.",
                             "Dijon's approach to r&b — intimate, compositionally meticulous, emotionally unguarded — is the standard. This is working toward it.",
                             "the warmth is approximate rather than genuine in a genre where that distinction is everything.",
                             "the form is technically correct. The feeling behind the form is developing."],
                "mid_high": ["the r&b tradition is engaged with genuine emotional intelligence.",
                             "Dijon's most accessible work sits near this territory — warm, specific, and genuinely felt.",
                             "Benny Sings's production lightness carries more emotional weight than this genre usually allows. This is working in that direction.",
                             "the emotional warmth here is earned rather than assumed. That's the whole requirement."],
                "high":     ["r&b with genuine emotional depth — the tradition is honored rather than just referenced.",
                             "Dijon at his most emotionally precise operates in this territory. This record earns the comparison.",
                             "Benny Sings's most intimate work has this quality — completely unguarded and impossibly warm.",
                             "the emotional truth and the production serving it are both completely present."],
                "perfect":  ["a perfect r&b record — Dijon's emotional precision at its absolute peak.",
                             "Benny Sings makes warmth feel like the most radical choice in music. This record achieves that same quality.",
                             "the emotional completeness here is total. A perfect record."],
            },
            "punk": {
                "low":      ["punk without conviction is just noise with a guitar and borrowed aggression.",
                             "Nirvana made raw power feel like the only honest response to the world. This rawness feels like a genre exercise.",
                             "the aggression is here without the necessity that makes aggression meaningful.",
                             "the form is correct. The thing it's supposed to be communicating is absent."],
                "mid_low":  ["the punk energy is present but it hasn't found the idea it's supposed to be in service of.",
                             "Nirvana's rawness always came from a specific place. This rawness is looking for its place.",
                             "the conviction is developing. The idea it needs to serve is still forming.",
                             "the rawness is present as aesthetic choice rather than emotional necessity — the harder thing to achieve."],
                "mid_high": ["the punk directness here is earned rather than performed.",
                             "Nirvana's approach — making rawness the most honest available form — is understood here.",
                             "Fontaines D.C.'s urgency is the contemporary benchmark. This earns its place near it.",
                             "the confrontational energy has a purpose here and it serves that purpose honestly."],
                "high":     ["punk with something genuine to say — the form and the content are in complete alignment.",
                             "Nirvana at their most transcendent had this quality: raw, specific, and genuinely necessary.",
                             "Fontaines D.C. made punk feel urgent and alive again. This record is working in that same vital space.",
                             "the ideas are fully present and the rawness serves them completely. The genre's promise kept."],
                "perfect":  ["a perfect punk record — Nirvana's emotional necessity married to Fontaines D.C.'s contemporary urgency.",
                             "Nirvana made In Utero and it felt like the only honest record possible. This has that quality.",
                             "the genre's original promise fulfilled completely. A perfect punk record."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tp = pools[gname].get(tier, pools[gname]["mid_high"])
                return [picks(tp, min(2, len(tp)))]
        fall = {
            "low":     f"the {g} framework is present without the ideas that give it meaning.",
            "mid_low": f"the {g} direction has potential that the execution hasn't fully unlocked.",
            "mid_high":f"the {g} approach here is working with genuine intention and it shows.",
            "high":    f"the {g} is executed with mastery — every choice in service of the complete vision.",
            "perfect": f"the {g} framework is transcended entirely. A landmark record.",
        }
        return [fall.get(tier, fall["mid_high"])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pool = {
            "low":      [f"the {t} theme is claimed without the emotional honesty to back it up.",
                         f"the {t} direction is gestured at rather than genuinely inhabited.",
                         f"the thematic content is present as decoration over an emotional absence.",
                         f"music about {t} requires something real behind it. I can't hear that something here."],
            "mid_low":  [f"the {t} angle is present without the specificity that would make it resonate.",
                         f"the {t} theme is handled more safely than the subject deserves.",
                         f"the thematic ambition is visible and the execution hasn't fully delivered on it.",
                         f"the {t} direction points at something real without fully arriving at it."],
            "mid_high": [f"the {t} theme is realized with genuine craft — it's load-bearing, not decorative.",
                         f"the thematic content is doing real work in service of the record's emotional purpose.",
                         f"the {t} direction is handled with the honesty and specificity the subject requires.",
                         f"the thematic intelligence here is genuine and it's working."],
            "high":     [f"the {t} theme reaches the level of emotional honesty where theme and music become indistinguishable.",
                         f"the thematic depth is earned rather than assumed — and it's doing serious structural work.",
                         f"the {t} direction is handled with complete conviction and the conviction is in service of something true.",
                         f"Radiohead's thematic ambition — using the {t} angle to say something completely specific — is the model. This achieves it."],
            "perfect":  [f"the {t} theme is executed with total conviction and total honesty — a perfect treatment.",
                         f"the thematic and musical completeness are in such alignment that separating them is impossible.",
                         f"the {t} direction reaches genuine artistic truth. The rarest achievement in any record.",
                         f"the thematic honesty here is total. I don't use that word casually."],
        }
        return [pick(pool.get(tier, pool["mid_high"]))]

    def _dur_too_long(self): return "the runtime runs past what the material can sustain — a rare problem for a record this good."
    def _dur_too_short(self): return "it ends before it fully arrives, which is the one thing I'd change."
    def _dur_great(self): return "the runtime is as precisely considered as everything else here — not a second wasted."
    def _dur_bad(self): return "the runtime adds nothing to an already difficult listening experience."

    def review(self, song):
        score      = self.compute_score(song)
        g_lines    = self.genre_lines(song, score)
        t_lines    = self.theme_lines(song, score)
        d_lines    = self.duration_lines(song, score)
        verdict    = self.get_verdict(score)
        mention    = pick(self.TEENA_NARUKA_MENTIONS)
        body_parts = g_lines + t_lines + d_lines
        random.shuffle(body_parts)
        body  = join_sentences(body_parts)
        final = f"{body} {ensure_punct(verdict)} — {score}/10. {mention}"
        return score, final
