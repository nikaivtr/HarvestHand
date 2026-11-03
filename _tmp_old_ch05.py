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
            "id":    "S2P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Hindi muna apo, gagawa muna tayo ng mga munting silungan para sa kanila."),
            ],
        },
        {
            "id":    "S2P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Silungan po? Bakit po?"),
            ],
        },
        {
            "id":    "S2P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ang mga buto ng kamatis ay napakaselan at hindi ito dapat tinatanim na direkta masyado sa araw."),
                ("lola", "Dapat ring kontrolado natin ang halamigmig at ang init ng lupa para mainam ang pag tubo."),
            ],
        },
        {
            "id":    "S2P7",
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
            "id": "S2P8",
            "type": "scene",
            "bg": "background/lucastomato2.jpg",
        },
        # ── Day 10 Transition ──
        {
            "id":   "day10_fade",
            "type": "transition",
        },
        {
            "id": "S2P9",
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
            "id":    "S2P10",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Wow! Nakakamangha tumubo na nga ang mga binhi ng kamatis."),
                ("lucas", "Siguradong matutuwa na si lola Maria nito."),
            ],
        },
        {
            "id": "S2P11",
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
            "id":    "S2P12",
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
            "id":    "S2P13",
            "type":  "dialogue",
            "bg":    "background/barontomatobg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Andito na na naman Baron!"),
                ("lucas", "Ano na namang gagawin mo?"),
            ],
        },
        {
            "id":    "S2P14",
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
            "id":    "S2P15",
            "type":  "dialogue",
            "bg":    "background/barontomatobg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Ano na naman ang binabalak mo Baron?"),
                ("lucas", "Puwede po bang tumigil ka na."),
            ],
        },
        {
            "id":    "S2P16",
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
            "id": "S2P17",
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
            "id":    "S2P18",
            "type":  "dialogue",
            "bg":    "background/tomatobgsnow.jpg",
            "chars": {"lucas": {"side": "left", "expression": "cold", "flip": True}},
            "lines": [
                ("lucas", "Ang lamig!"),
                ("lucas", "Delikado ang mga halaman nito! Ano ang gagawin ko?"),
            ],
        },
        {
            "id":            "S1P19",
            "type":          "choice",
            "day":   10,
            "bg":            "background/scenebg_default.png",
            "question":       "Naging malamig ang klima sa baryo, kailangan ng tulong ni lucas na masalba ang mga halaman. Alin sa dalawa ang tamang gamit upang mapanatiling mainit ang lupang pinagtaniman ng mga kamatis?",
            "retry_question": "Sandali, pakiramdam ko masyadong mainit ang gamit na ito....",
            "choices": [
                {"img": "buttons/choice_heatmats.png", "label": "", "frame": False},
                {"img": "buttons/choice_fire.png",    "label": "", "frame": False},
            ],
            "correct": 0,
        },
        # ── Panel 20 - Feedback Correct - Lucas Thumbs up ───────────────
        {
            "id":          "S2P20_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lucas": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lucas", "Magaling! Ang heat mats at light source ay maaaring gamitin upang mapainit ang mga halaman."),
            ],
        },
        # ── Panel 21 - Feedback: Correct — Lola thumbs up ───────────────
        {
            "id":         "S2P21_right_2",
            "type":       "feedback",
            "if_correct": True,
            "random_pick": True,
            "bg":         "background/scenebg_right.png",
            "chars":           {
                    "lola": {
                        "side": "left",
                        "expression": "thumbs",
                        "flip": True,
                    }
                },
            "lines": [
                ("lola", "Magaling, apo! Hindi kailangang gumamit ng mga delikadong kagamitan para lang mapangalagaan ang mga halaman."),
            ],
        },
        # ── Panel 22 ── Feedback: Wrong — Lucas worried ───────────────────
        {
            "id":          "S2P22_wrong_1",
            "type":        "feedback",
            "if_correct":  False,
            "random_pick": True,
            "retry_to_choice": True,
            "bg":          "background/scenebg_wrong.png",
            "chars":       {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Naku po! Napakadelikado nito, maaari masunog ang bodega dahil sa apoy! Hindi ito ang kagamitang dapat gagamitin natin."),
            ],
        },
        # ── Panel 23 ── Feedback: Wrong — Kapitan warns ───────────────────
        {
            "id":              "S2P23_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Magingat sa pag gamit ng apoy!. Ito ay nakakasunog at napaka delikado ng mga ito."),
            ],
        },
        {
            "id":   "day10_fade",
            "type": "transition",
        },
        {
            "id":    "S2P24",
            "type":  "dialogue",
            "bg":    "background/tomatobgsnow.jpg",
            "chars": {"lucas": {"side": "left", "expression": "cold", "flip": True}},
            "lines": [
                ("lucas", "Magaling, magiging epektibo na ito para mapainit ang mga halaman."),
            ],
        },
        {
            "id":   "day10_fade",
            "type": "transition",
        },
        {
            "id":    "S2P25",
            "type":  "dialogue",
            "bg":    "background/baronairconbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "cold", "flip": True}},
            "lines": [
                ("lucas", "Ang lamig!"),
                ("lucas", "Papaano ko mapapawalang bisa ang ginawa ni baron?"),
            ],
        },
         # ── Scene 2, Panel 26 - choices ───────────────
        {
            "id":            "S2P26",
            "type":          "choice",
            "bg":            "background/baronairconbg.jpg",
            "question":       "Parang may isang kagamitan ang tumatakip sa araw. Kaya siguro napaka lamig. Dapat ba natin itong alisin?",
            "retry_question": "Nagkamali ata tayo ng ating piniling sagot. Basahin nating maigi at intindihin ang tanong bago pumili ng sagot.",
            "choices": [
                {"img": "buttons/choice1.png", "frame": False},
                {"img": "buttons/choice3.png", "frame": False},
            ],
            "correct": 0,
        },
        # ── Scene 2, Panel 27 - Feedback Correct - Lucas Thumbs up ───────────────
        {
            "id":          "S2P27_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lucas": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lucas", "Tama! Kailangan nating alisin ang Airconditioner upang maibalik natin ang init sa baryo."),
            ],
        },              
        # ── Scene 2, Panel 28 -Feedback: Correct — Lola thumbs up ───────────────
        {
            "id":         "S2P28_right_2",
            "type":       "feedback",
            "if_correct": True,
            "random_pick": True,
            "bg":         "background/scenebg_right.png",
            "chars":           {
                    "lola": {
                        "side": "left",
                        "expression": "thumbs",
                        "flip": True,
                    }
                },
            "lines": [
                ("lola", "Magaling apo! Hindi uso ang snow sa Pilipinas."),
            ],
        },
        # ── Scene 2, Panel 29 ── Feedback: Wrong — Lucas worried ───────────────────
        {
            "id":          "S2P29_wrong_1",
            "type":        "feedback",
            "if_correct":  False,
            "random_pick": True,
            "retry_to_choice": True,
            "bg":          "background/scenebg_wrong.png",
            "chars":       {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Huwag! Kung mananatili sa malamig na klima ang baryo, masisisra ang mga pananim, at masyadong delikado sa kalusugan."),
            ],
        }, 
        # ── Scene 2, Panel 30 ── Feedback: Wrong — Kapitan warns ───────────────────
        {
            "id":              "S2P30_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "baron": {
                    "side": "right",
                    "expression": "laugh",
                    "flip": False,
                    }
                },
            "lines": [
                ("baron", "HA! Tamang-tama! Manatili sila sa lamig!"),
            ],
        },
        {
            "id":   "day10_fade",
            "type": "transition",
        },
        
    ],
}
