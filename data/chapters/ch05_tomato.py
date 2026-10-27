# ============================================================
#  CHAPTER 5 — TOMATO (Kamatis)
#  Intermediate | 11 story panels | Total growing days: 75
#  Characters: Lucas, Lola Maria, Blight Baron
#  MECHANICS: Indirect planting, companion plants, staking, pruning
# ============================================================

CHAPTER = {
    "id":         "ch05",
    "crop":       "Tomato",
    "level":      "intermediate",
    "memory":     "Kamatis Sarciado Memory",
    "total_days": 75,

    "slides": [

        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "chapter5.png", 
        },

        # ── Panel 1 — Lola Maria's faint memory of sourness ───
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Nais ko sanang mag luto ng isang espesyal na pagkain na inihahanda ko noon sa iyong lolo apo."),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Ano naman po ito lola?"),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Hindi ko nga matandaan ang tawag nito apo eh. Pero dati ay inihahanda namin ito ng lolo mo tuwing linggo. Ngunit hindi ko na ito naaalala ngayon."),
            ],
        },
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Siguro naman ay may mga sangkap na alam nyo parin po kahit ngayon."),
            ],
        },
        {
            "id":    "S1P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Kamatis ang pangunahing sangkap nito. Ngunit niluluto lamang ito ng lolo mo kung ang kamatis ay pulang pula at makinang. Hindi sya gumagamit ng hindi mapula at makinang."),
            ],
        },
        {
            "id":    "S1P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Bakit naman po?"),
            ],
        },
        {
            "id":    "S1P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Nag iiba daw kasi ang lasa apo. "),
            ],
        },
        {
            "id":    "S1P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Meron po ba tayong hinog na mga kamatis lola?"),
            ],
        },
        {
            "id":    "S1P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Nasira ang mga kamatis natin nung nakaraan dahil sa ginawa ni Baron."),
                ("lola", "Nadamay ang mga ito dahil sa dami ng insektong bumalot sa lugar natin."),
            ],
        },
        {
            "id":    "S1P10",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Hindi na po ba natin ito mapapakinabangan lola?"),
            ],
        },
        {
            "id":    "S1P11",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Puwedeng puwede pa natin itong mapakinabangan Lucas."),
                ("lola", "Kailangan lang natin makuha o mahiwalay ang mga buto ng kamatis upang maitanim pa natin ang mga ito."),
                ("lola", "Kaya lang, masyado nang manginig ang mga kamay ko para makuha ang mga buto ng hindi ito nasisira o nalalaglag."),
            ],
        },
        {
            "id":    "S1P12",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Tara po lola, tutulungan po kita."),
            ],
        },
        {
            "id":    "S1P13",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ang bait naman talga ng apo ko. Kunin mo ng maingat ang kutsilyo at ang tweezers doon sa kabinet."),
            ],
        },
        {
            "id":    "S1P14",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Okay po lola."),
            ],
        },
        {
            "id":    "S1P15",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Simulan na natin apo."),
            ],
        },
        {
            "id":   "day0_fade",
            "type": "transition",
        },
        {
            "id":    "S1P16",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Eto na po lola."),
            ],
        },
        # ── Tomato Seed Extraction Minigame ──
        {
            "id":    "tomato_seed_extraction_1",
            "type":  "tomato_seed_extraction",
            "bg":    "background/scenebg_default.png",
        },
        {
            "id":    "S1P17",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Phew! Nakura rin natin sa wakas ang mga buto ng kamatis Lola."),
                ("lucas", "Ano na po ang susunod nito?"),
            ],
        },
        {
            "id":    "S1P18",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Kailangan muna nating ilagay ang mga ito sa lalagyanan at lagyan ng tubig upang maging handa ang mga ito para itanim."),
            ],
        },
        {
            "id":    "S1P19",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Ang tawag sa gagawin natin ay fermintation."),
                ("lucas", "Kung saan gumagamit tayo ng lalagyang selyado at tubig para ma break-down ang germination-inhibiting gel mula sa pulp ng kamatis."),
                ("lucas", "Nakakatulong ito para mapuksa ang mga bacteria. Matapos itong ilagay sa garapon at lagyan ng tubig. Tatakpan natin ito ng malinis na tela. Diba po lola Maria?"),
            ],
        },
        {
            "id":    "S1P20",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Oo Lucas! Tama ka. Magaantay tayo ngayon ng 3 hanggan 4 na araw bago ito banlawan at itanim."),
            ],
        },
        # ── Day 1 Transition ──
        {
            "id":   "day1_fade",
            "type": "transition",
        },
        # ── Scene 2 ──
        {
            "id": "S2P1",
            "type": "scene",
            "bg": "background/lucastomato.jpg",
        },
        # ── Day 3 Transition ──
        {
            "id":   "day3_fade",
            "type": "transition",
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Tatlong araw na ang lumipas apo. Maaari na natin itong ilipat sa hardin."),
            ],
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Sige po lola Maria, maghuhukay na po ako."),
            ],
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Hindi muna apo, gagawa muna tayo ng mga munting silungan para sa kanila."),
            ],
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Silungan po? Bakit po?"),
            ],
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ang mga buto ng kamatis ay napakaselan at hindi ito dapat tinatanim na direkta masyado sa araw."),
                ("lola", "Dapat ring kontrolado natin ang halamigmig at ang init ng lupa para mainam ang pag tubo."),
            ],
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Sigi po lola, ihahanda ko lang po ang mga gamit."),
            ],
        },
        {
            "id":   "day3_fade",
            "type": "transition",
        },
        {
            "id": "S2P1",
            "type": "scene",
            "bg": "background/lucastomato2.jpg",
        },
        # ── Day 10 Transition ──
        {
            "id":   "day10_fade",
            "type": "transition",
        },
        {
            "id": "S2P1",
            "type": "narration_overlay",
            "day": 10,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",

            "narration": (
                "10 araw na ang lumipas mula nang itanim nila "
                "Lucas ang mga binhi ng kamatis. "
                "Araw-araw nila itong inaalagaan "
                "at ngayon umuusbong na ang mga ito."
            ),
        },
        {
            "id":   "day10_fade",
            "type": "transition",
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Wow! Nakakamangha tumubo na nga ang mga binhi ng kamatis."),
                ("lucas", "Siguradong matutuwa na si lola Maria nito."),
            ],
        },
        {
            "id": "S2P4",
            "type": "scene",
            "bg": "background/barontomatobg.jpg",
            "shake": True,  
            "smoke": True,   # smoke rises from the bottom of the screen

            "chars": {
                "baron": {
                    "side": "center",
                    "expression": "explosion",
                    "flip": False,
                },
            },
        },
        {
            "id":    "S2P5",
            "type":  "dialogue",
            "bg":    "background/barontomatobg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Kumusta bata?"),
                ("baron", "Ano na namang kahibangan ang ginagawa mo?"),
            ],
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/barontomatobg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Andito na na naman Baron!"),
                ("lucas", "Ano na namang gagawin mo?"),
            ],
        },
        {
            "id":    "S2P5",
            "type":  "dialogue",
            "bg":    "background/barontomatobg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Relax! Wala akong gagawin."),
                ("baron", "Andito lang ako para balaan ka hehehe."),
            ],
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/barontomatobg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Ano na naman ang binabalak mo Baron?"),
                ("lucas", "Puwede po bang tumigil ka na."),
            ],
        },
        {
            "id":    "S2P5",
            "type":  "dialogue",
            "bg":    "background/barontomatobg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Gusto mo ba ang malamig?"),
                ("baron", "HAHAHAHAHAHA!"),
            ],
        },
        {
            "id": "S2P4",
            "type": "scene",
            "bg": "background/barontomatobg.jpg",
            "shake": True,   
            "smoke": True,   # smoke rises from the bottom of the screen

            "chars": {
                "baron": {
                    "side": "center",
                    "expression": "explosion",
                    "flip": False,
                },
            },
        },
        {
            "id":   "day10_fade",
            "type": "transition",
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/tomatobgsnow.jpg",
            "chars": {"lucas": {"side": "left", "expression": "cold", "flip": True}},
            "lines": [
                ("lucas", "Ang lamig!"),
                ("lucas", "Delikado ang mga halaman nito! Ano ang gagawin ko?"),
            ],
        },

    ],
}
