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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Phew! Nakuha rin natin sa wakas ang mga buto ng kamatis Lola."),
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
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
        # ── Scene 3 — The warmth returns ───────────────────────
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Mainit na ulit ang hangin, apo. Salamat at nawala na ang kakaibang lamig."),
            ],
        },
        {
            "id":    "S3P2",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Opo, lola. Mabuti na lang po at hindi nalanta ang mga punla."),
            ],
        },
        {
            "id":    "S3P3",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Matatag sila dahil sa maayos mong pag-aalaga."),
                ("lola", "Hindi ko akalaing makikita kong muling tumutubo ang mga kamatis sa ating bakuran."),
            ],
        },
        {
            "id":    "S3P4",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Kailan po natin sila ililipat sa hardin?"),
            ],
        },
        {
            "id":    "S3P5",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Hindi pa ngayon, apo. Hihintayin muna nating magkaroon sila ng dalawang pares ng tunay na dahon."),
                ("lola", "Ang unang dalawang dahon ay pang-umpisa lamang. Ang tunay na dahon ay mas mahaba at may bingot-bingot na gilid."),
            ],
        },
        {
            "id":    "S3P6",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Ibig sabihin po, hudyat iyon na sapat na ang lakas ng kanilang mga ugat?"),
            ],
        },
        {
            "id":    "S3P7",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Tama ka, Lucas! Mabilis kang matuto."),
                ("lola", "Sa mga susunod na araw, ilalabas natin sila sa araw nang ilang oras lamang bawat araw. Hardening off ang tawag dito."),
                ("lola", "Sa ganitong paraan, masasanay silang unti-unti bago natin itanim sa lupa."),
            ],
        },
        {
            "id":   "day21_fade",
            "type": "transition",
        },
        {
            "id": "S3P8",
            "type": "narration_overlay",
            "day": 21,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "21 araw na ang lumipas. "
                "Araw-araw na inilabas ni Lucas ang mga punla sa sikat ng araw, "
                "ilang oras lamang sa simula, hanggang sa masanay ang mga ito. "
                "Ngayon, may dalawang pares na sila ng tunay na dahon."
            ),
        },
 
        # ── Transplanting (indirect planting) ──────────────────
        {
            "id":    "S3P9",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Handa na sila, apo. Maaari na nating ilipat ang mga punla sa hardin."),
                ("lola", "Maghukay ka ng butas na may layong dalawang talampakan sa bawat isa, para hindi sila magsiksikan."),
            ],
        },
        {
            "id":    "S3P10",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Sige po, lola. Ngayon, puwede na po akong maghukay!"),
                ("lucas", "Gaano po kalalim ang dapat kong hukayin?"),
            ],
        },
        {
            "id":    "S3P11",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Sapat na ang lalim para matabunan ang tangkay hanggang sa ibaba ng mga unang dahon."),
                ("lola", "Tutubo ang mga dagdag na ugat mula sa nakabaong tangkay, kaya lalong titibay ang halaman."),
            ],
        },
        {
            "id":    "S3P12",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Kaya po pala hindi natin itinanim nang direkta ang mga buto sa hardin."),
                ("lucas", "Mas ligtas po silang alagaan habang maliliit pa, at saka lang natin sila inilipat."),
            ],
        },
        {
            "id":    "S3P13",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Tama! Indirect planting ang tawag diyan, apo."),
                ("lola", "Diligan mo sila nang marahan. Mas mainam kung hapon o maulap ang langit, para hindi sila mabigla sa init."),
            ],
        },
        {
            "id":    "S3P14",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lucas": {"side": "right", "expression": "thumbs", "flip": False}},
            "lines": [
                ("lucas", "Ayan po, lola! Nakatanim na ang lahat. Mukhang masaya na silang nasa hardin."),
            ],
        },
 
        # ── Companion planting ─────────────────────────────────
        {
            "id":    "S3P15",
            "type":  "dialogue",
            "bg":    "background/tomatobg1.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "May isa pa tayong gagawin, Lucas. Ang kamatis ay mas masaya kapag may kasamang kaibigang halaman."),
                ("lola", "Ang mga ito ay maaaring magtaboy ng peste at tumulong sa paglaki ng ating mga pananim."),
            ],
        },
        {
            "id":            "S3P16",
            "type":          "choice",
            "day":           21,
            "bg":            "background/scenebg_default.png",
            "question":       "May dalawang halamang puwedeng itanim sa tabi ng mga kamatis. Alin ang mas mainam na kasama nito upang maitaboy ang mga peste?",
            "retry_question": "Hmm, baka may peste pang naaakit ng halamang iyan. Pag-isipan natin ulit.",
            "choices": [
                {"img": "buttons/choice_basil.png", "label": "", "frame": False},
                {"img": "buttons/choice_corn.png",  "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S3P17_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lucas": {
                    "side": "right",
                    "expression": "thumbs",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Tama! Ang balanoy ay may matapang na amoy na nagtataboy ng mga langaw at uod na kumakain ng kamatis."),
            ],
        },
        {
            "id":         "S3P18_right_2",
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
                ("lola", "Magaling, apo! Magkaibigan ang balanoy at kamatis. Pareho silang mahilig sa araw at sa regular na pagdilig."),
            ],
        },
        {
            "id":          "S3P19_wrong_1",
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
                ("lucas", "Naku po! Ang mais ay dinadapuan ng parehong uod na kumakain din ng kamatis. Mas lalo lang silang darami."),
            ],
        },
        {
            "id":              "S3P20_wrong_2",
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
                ("baron", "HAHAHA! Ilagay mo iyan! Kapag maraming uod, mas masaya!"),
            ],
        },
        {
            "id":    "S3P21",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Itatanim ko po ang balanoy sa tabi ng bawat kamatis, lola."),
            ],
        },
        {
            "id":    "S3P22",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Maglalagay rin tayo ng ilang marigold sa gilid ng hardin. Pinaniniwalaang naitataboy nila ang mga maliliit na uod sa lupa."),
                ("lola", "Ngayon, may bantay na ang ating mga kamatis."),
            ],
        },
 
        # ── Staking ────────────────────────────────────────────
        {
            "id":   "day35_fade",
            "type": "transition",
        },
        {
            "id": "S3P23",
            "type": "narration_overlay",
            "day": 35,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "35 araw na ang lumipas. "
                "Mabilis na tumangkad ang mga kamatis, "
                "at may mga unang bulaklak nang lumilitaw sa kanilang mga sanga."
            ),
        },
        {
            "id":    "S3P24",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lucas": {"side": "right", "expression": "afraid", "flip": False}},
            "lines": [
                ("lucas", "Lola! Yumuyuko na po ang mga halaman at halos dumikit na sa lupa ang ilang sanga!"),
            ],
        },
        {
            "id":    "S3P25",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Huwag kang mag-alala, apo. Natural lang iyan sa mga halamang kamatis."),
                ("lola", "Kapag bumigat sila sa bulaklak at bunga, hindi na kaya ng kanilang tangkay na tumayo nang mag-isa."),
                ("lola", "Kailangan na nating suportahan sila."),
            ],
        },
        {
            "id":    "S3P26",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Ano po ang dapat kong gamitin, lola?"),
            ],
        },
        {
            "id":            "S3P27",
            "type":          "choice",
            "day":           35,
            "bg":            "background/scenebg_default.png",
            "question":       "Kailangan ni Lucas ng pangsuporta sa mga halamang kamatis. Alin ang tamang paraan ng pagsuporta?",
            "retry_question": "Sandali, baka masaktan ang halaman sa paraang iyan. Subukan nating muli.",
            "choices": [
                {"img": "buttons/choice_stake.png", "label": "", "frame": False},
                {"img": "buttons/choice_wire.png",  "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S3P28_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lucas": {
                    "side": "right",
                    "expression": "thumbs",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Tama! Itatali natin ang tangkay sa kawayan gamit ang malambot na tela, at hindi ito hihigpitan."),
            ],
        },
        {
            "id":         "S3P29_right_2",
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
                ("lola", "Magaling, apo! Dahil nakataas ang mga bunga, hindi sila mabubulok sa basang lupa at mas makakadaan ang hangin."),
            ],
        },
        {
            "id":          "S3P30_wrong_1",
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
                ("lucas", "Naku po! Ang manipis na alambre na mahigpit ang pagkakatali ay maaaring humiwa sa malambot na tangkay."),
            ],
        },
        {
            "id":              "S3P31_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Mag-ingat sa pagtali! Ang masikip na tali ay nakakasugat sa halaman at hindi nito hahayaang lumaki ang tangkay."),
            ],
        },
        {
            "id":    "S3P32",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lucas": {"side": "right", "expression": "thumbs", "flip": False}},
            "lines": [
                ("lucas", "Ayan po! Tuwid na tuwid na ang mga kamatis, lola."),
                ("lucas", "Parang mga batang sundalo na handang lumaban."),
            ],
        },
        {
            "id":    "S3P33",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Hehe, tama ka. Habang naglalagay ka ng mga tali, hindi na nanginginig ang kamay ko sa tuwa."),
                ("lola", "Ikaw na ang nagtuturo sa akin ngayon, apo."),
            ],
        },
 
        # ── Pruning ────────────────────────────────────────────
        {
            "id":   "day45_fade",
            "type": "transition",
        },
        {
            "id": "S3P34",
            "type": "narration_overlay",
            "day": 45,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "45 araw na ang lumipas. "
                "Umaabot na ang mga kamatis sa baywang ni Lucas, "
                "ngunit napakarami na ring dahon at mga bagong sanga ang tumutubo."
            ),
        },
        {
            "id":    "S3P35",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Lola, parang gubat na po ang mga kamatis. Ang daming bagong sanga!"),
                ("lucas", "Hindi po kaya sila mahirapang huminga?"),
            ],
        },
        {
            "id":    "S3P36",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Magandang obserbasyon, Lucas. Kapag sobrang siksik ang mga dahon, naiipon ang halumigmig at madaling dapuan ng sakit ang halaman."),
                ("lola", "Pati ang lakas ng halaman ay napupunta sa mga dahon at sanga sa halip na sa mga bunga."),
                ("lola", "Kaya kailangan nating gawin ang pruning."),
            ],
        },
        {
            "id":    "S3P37",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Pruning po? Ano po ang puputulin ko?"),
            ],
        },
        {
            "id":    "S3P38",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Hanapin mo ang maliliit na sanga na tumutubo sa pagitan ng pangunahing tangkay at ng malaking sanga."),
                ("lola", "Sucker ang tawag sa mga iyon. Kapag nasa umaga at tuyo ang halaman, ligtas silang putulin gamit ang malinis na gunting."),
            ],
        },
        {
            "id":            "S3P39",
            "type":          "choice",
            "day":           45,
            "bg":            "background/scenebg_default.png",
            "question":       "Maingat na lumapit si Lucas sa halaman. Alin sa dalawa ang dapat niyang putulin upang maging mas malusog ang halamang kamatis?",
            "retry_question": "Sandali, baka maapektuhan ang magiging bunga natin kapag iyan ang pinutol. Subukan ulit.",
            "choices": [
                {"img": "buttons/choice_sucker.png", "label": "", "frame": False},
                {"img": "buttons/choice_flower.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S3P40_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lucas": {
                    "side": "right",
                    "expression": "thumbs",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Tama! Ang mga sucker ang puputulin natin upang mapunta ang lakas ng halaman sa mga bunga."),
            ],
        },
        {
            "id":         "S3P41_right_2",
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
                ("lola", "Magaling, apo! Putulin mo na rin ang mga dahong dumidikit sa lupa para hindi sila mahawaan ng sakit."),
            ],
        },
        {
            "id":          "S3P42_wrong_1",
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
                ("lucas", "Naku po! Mga bulaklak ang magiging bunga. Kapag pinutol ko sila, mawawalan tayo ng kamatis."),
            ],
        },
        {
            "id":              "S3P43_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Huwag putulin ang mga bulaklak! Sila ang magiging prutas ng halaman."),
            ],
        },
        {
            "id":    "S3P44",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lucas": {"side": "right", "expression": "thumbs", "flip": False}},
            "lines": [
                ("lucas", "Ayan po! Mas maluwag at mas maaliwalas na ang mga halaman."),
                ("lucas", "Madali nang dumaan ang hangin at sikat ng araw sa pagitan ng mga dahon."),
            ],
        },
 
        # ── The Blight Baron returns ───────────────────────────
        {
            "id":   "day55_fade",
            "type": "transition",
        },
        {
            "id": "S3P45",
            "type": "narration_overlay",
            "day": 55,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "55 araw na ang lumipas. "
                "Namumunga na ang mga kamatis ni Lucas, "
                "ngunit may nagbabantang dumating sa baryo."
            ),
        },
        {
            "id": "S3P46",
            "type": "scene",
            "bg": "background/barontomatobg2.jpg",
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
            "id":    "S3P47",
            "type":  "dialogue",
            "bg":    "background/barontomatobg2.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Hindi mo ako matatakasan, bata!"),
                ("baron", "Ang gaganda ng mga kamatis mo, sayang kung masisira ang mga iyan."),
            ],
        },
        {
            "id":    "S3P48",
            "type":  "dialogue",
            "bg":    "background/barontomatobg2.jpg",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Baron! Ano na namang plano mo sa mga halaman ko?"),
            ],
        },
        {
            "id":    "S3P49",
            "type":  "dialogue",
            "bg":    "background/barontomatobg2.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Ulan! Ulan! Ulan! At halumigmig na kakapit sa bawat dahon!"),
                ("baron", "Hayaan mong dumating ang amag at blight, at magdilim ang bawat kamatis mo. HAHAHAHAHA!"),
            ],
        },
        {
            "id": "S3P50",
            "type": "scene",
            "bg": "background/barontomatobg2.jpg",
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
            "id":   "day55b_fade",
            "type": "transition",
        },
        {
            "id":    "S3P51",
            "type":  "dialogue",
            "bg":    "background/barontomatobg2.jpg",
            "chars": {"lucas": {"side": "right", "expression": "afraid", "flip": False}},
            "lines": [
                ("lucas", "Lola! May mga itim na batik sa ilang dahon, at basang-basa ang buong hardin!"),
            ],
        },
        {
            "id":    "S3P52",
            "type":  "dialogue",
            "bg":    "background/barontomatobg2.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Blight ang tawag diyan, apo. Dumarami ito kapag basa at siksik ang mga dahon."),
                ("lola", "Pero huwag kang mataranta. Naaalala ko ang tinuro sa akin ng lolo mo noon."),
            ],
        },
        {
            "id":    "S3P53",
            "type":  "dialogue",
            "bg":    "background/barontomatobg2.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Putulin at itapon sa malayo ang mga dahong may batik para hindi na kumalat."),
                ("lola", "Diligan ang ugat sa umaga, at iwasang mabasa ang mga dahon."),
                ("lola", "Maglagay din tayo ng dayami sa lupa para hindi tumalsik sa dahon ang putik kapag umuulan."),
            ],
        },
        {
            "id": "S3P54",
            "type": "action_challenge",
            "bg": "background/tomatobg2.jpg",
            "overlay": "weedremovalcard.png",
            "dim_inactive": False,
        },
        {
            "id":    "S3P55",
            "type":  "dialogue",
            "bg":    "background/barontomatobg2.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Sige po, lola. Gagawin ko po ito nang maingat."),
                ("lucas", "Buti na lang po at pinutol natin ang mga sucker at itinali natin ang mga kamatis sa kawayan. Hindi na gaanong siksik at nakataas ang mga halaman."),
            ],
        },
        {
            "id":   "day60_fade",
            "type": "transition",
        },
        {
            "id":    "S3P56",
            "type":  "dialogue",
            "bg":    "background/tomatobg2.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Lola, nakaligtas po ang halos lahat ng halaman. Wala nang kumalat na batik sa mga bagong dahon!"),
            ],
        },
        {
            "id":    "S3P57",
            "type":  "dialogue",
            "bg":    "background/barontomatobg2.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Ano?! Imposible ito! Dapat ay nalanta na ang mga iyan!"),
            ],
        },
        {
            "id":    "S3P58",
            "type":  "dialogue",
            "bg":    "background/barontomatobg2.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Hindi na ako natatakot sa iyo, Baron."),
                ("lucas", "Alam ko na kung paano alagaan ang bawat halaman, at hindi ko sila iiwan."),
            ],
        },
        {
            "id":    "S3P59",
            "type":  "dialogue",
            "bg":    "background/barontomatobg2.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Hmp! Pagbibigyan kita ngayon, bata. Pero hindi pa tapos ang laban natin!"),
            ],
        },
        {
            "id": "S3P60",
            "type": "scene",
            "bg": "background/barontomatobg2.jpg",
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
 
        # ── Harvest and the Kamatis Sarciado memory ────────────
        {
            "id":   "day75_fade",
            "type": "transition",
        },
        {
            "id": "S3P61",
            "type": "narration_overlay",
            "day": 75,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "75 araw na ang lumipas mula nang unang kunin ni Lucas "
                "ang mga buto mula sa luma nilang kamatis. "
                "Ngayon, pulang-pula at makinang na ang mga bunga sa hardin."
            ),
        },
        {
            "id":    "S3P62",
            "type":  "dialogue",
            "bg":    "background/tomatobg3.jpg",
            "chars": {"lucas": {"side": "right", "expression": "thumbs", "flip": False}},
            "lines": [
                ("lucas", "Lola, tingnan po ninyo! Pulang-pula at makinang na ang mga kamatis!"),
                ("lucas", "Katulad po ito ng mga kamatis na pinipili ni Lolo."),
            ],
        },
        {
            "id":    "S3P63",
            "type":  "dialogue",
            "bg":    "background/tomatobg3.jpg",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Napakaganda nila, apo. Dahan-dahan mong pitasin at huwag mong pipigain."),
                ("lola", "Kapag handa na, madaling kumakalas ang bunga sa tangkay."),
            ],
        },
        {
            "id": "S3P64",
            "type": "action_challenge",
            "bg": "background/tomatobg3.jpg",
            "overlay": "harvestcardscan.png",
            "dim_inactive": False,
        },
        {
            "id":    "S3P65",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ah! Naaalala ko na! Ang lutuing ito ay tinatawag na Kamatis na Sarciado!"),
                ("lola", "Iginigisa ito ng lolo mo kasama ang bawang at sibuyas, saka hahaluan ng binating itlog."),
            ],
        },
        {
            "id":    "S3P66",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Sarciado po pala! Matutulungan ko po kayong magluto, lola."),
            ],
        },
        {
            "id":    "S3P67",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Alam mo, Lucas, sinabi ng lolo mo na ang tamang paghihintay ang nagbibigay ng tunay na lasa sa pagkain."),
                ("lola", "Ngayon, naiintindihan ko na ang ibig niyang sabihin."),
            ],
        },
        {
            "id":    "S3P68",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "right", "expression": "thumbs", "flip": False}},
            "lines": [
                ("lucas", "Hindi lang po ang mga kamatis ang lumago, lola. Mas marami rin po akong natutunan."),
                ("lucas", "Tara na po, magluto na tayo. Itatabi ko rin po ang ilang buto para sa susunod na taniman."),
            ],
        },
        {
            "id":    "S3P69",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Napakabait at napakatalino ng apo ko. Siguradong ipinagmamalaki ka ng lolo mo."),
            ],
        },
        {
            "id": "S3P70",
            "type": "narration_overlay",
            "day": 75,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Muling nagkaroon ng amoy ng bawang at kamatis ang munting kusina ni Lola Maria. "
                "Naibalik na ang Kamatis Sarciado Memory."
            ),
        },
    ],
}
