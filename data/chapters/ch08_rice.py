# ============================================================
#  CHAPTER 8 — RICE (Palay / Bigas)
#  Expert | 15 story panels | Total growing days: 113
#  Characters: Lucas, Lola Maria, Blight Baron, Kapitan Ernesto
#  NEW MECHANIC: timer=True marks slides with a future 30-sec challenge
#  NEW CONTENT: plowing, harrowing, golden snails, sun-drying, storage
# ============================================================

CHAPTER = {
    "id":         "ch08",
    "crop":       "Rice",
    "level":      "advanced",
    "memory":     "Bigas Memory",
    "total_days": 113,
 
    "slides": [
 
        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "chapter8.png",
        },
 
        # ── Scene 1 — Baron's Time-Warp Hex ────────────────────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Kumusta, Lucas? Kumusta, Lola Maria? Narinig kong marami na kayong naibalik na alaala."),
                ("baron", "Ngunit ang palay ang pinakamahirap sa lahat ng pananim. Tingnan natin kung kakayanin ninyo ito!"),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Narito ang aking sumpa ng oras! Mula ngayon, tatlumpung segundo lamang ang makukuha ninyo sa bawat mahalagang kilos!"),
                ("baron", "Bilisan ninyo, kung kaya ninyo! HAHAHAHAHAHA!"),
            ],
        },
        {
            "id": "S1P3",
            "type": "scene",
            "bg": "background/scenebg_baron.png",
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
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Tatlumpung segundo lang po? Lola, napakarami pong dapat gawin sa palayan!"),
            ],
        },
        {
            "id":    "S1P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Huminahon ka, apo. Ang palay ang puso ng ating baryo, kaya dapat natin itong igalang."),
                ("lola", "Hindi kailangang magmadali ang taong handa. Ang tamang kaalaman ang magpapabilis ng ating mga kamay."),
            ],
        },
        {
            "id":    "S1P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Tama po kayo, Lola. Marami na po akong natutunan sa kamatis at sa talong."),
                ("lucas", "Haharapin po natin ito nang maingat at may tamang hakbang."),
            ],
        },
        {
            "id":    "S1P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Iyan ang apo ko! Simulan natin sa mga buto."),
            ],
        },
        {
            "id":    "S1P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Bago natin ihasik ang mga buto ng palay, may kailangan muna tayong gawin sa mga ito."),
            ],
        },
        {
            "id":    "S1P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Ano po iyon, Lola?"),
            ],
        },
 
        # ── Seed soaking — choice ──────────────────────────────
        {
            "id":            "S1P10",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Handa nang ihasik nina Lucas at Lola Maria ang mga buto ng palay. Ano ang dapat nilang gawin sa mga buto bago ito ihasik?",
            "retry_question": "Sandali, isipin natin kung ano ang kailangan ng buto para magsimulang sumibol. Subukan nating muli.",
            "choices": [
                {"img": "buttons/choice_soak_seeds.png", "label": "", "frame": False},
                {"img": "buttons/choice_dry_seeds.png",  "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S1P10_right_1",
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
                ("lucas", "Tama! Pumapasok ang tubig sa loob ng buto at ginigising ito, kaya mas mabilis at mas pantay ang pagsibol."),
            ],
        },
        {
            "id":          "S1P10_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Kaya laging ibinababad ng lolo mo ang binhi bago ito ihasik."),
            ],
        },
        {
            "id":              "S1P10_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Naku po! Kapag tuyo ang buto at agad itong inihasik, mabagal at hindi pantay ang pagsibol nito."),
            ],
        },
        {
            "id":              "S1P10_wrong_2",
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
                ("baron", "HAHAHA! Ihasik ninyo agad! Mas marami ang hindi tutubo!"),
            ],
        },
        {
            "id":    "S1P11",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ibabad natin ang mga buto sa malinis na tubig sa loob ng dalawampu't apat na oras."),
                ("lola", "Pagkatapos, ibabalot natin ang mga ito sa basang sako sa loob ng isa pang araw, hanggang sa lumitaw ang maliliit na puting usbong."),
            ],
        },
 
        # ── Day 1 — Seedbed, plowing and harrowing ─────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },
        {
            "id": "S2P1",
            "type": "narration_overlay",
            "day": 1,
            "bg": "background/scenebg_planter.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Unang araw ng pagtatanim. "
                "Ihinasik nina Lucas at Lola Maria ang mga sumibol na buto sa seedbed, "
                "isang maliit na bahagi ng palayan kung saan muna palalakihin ang mga punla."
            ),
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Aabutin ng halos dalawampung araw bago maging handa ang mga punla."),
                ("lola", "Habang naghihintay tayo, ihahanda natin ang palayan."),
            ],
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Ano po ang uunahin natin, Lola?"),
            ],
        },
        {
            "id":    "S2P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Babasagin muna natin ang matigas na lupa upang lumuwag ito. Plowing ang tawag dito."),
                ("lola", "Noon, araro at kalabaw ang gamit ng lolo mo. Ngunit sa maliit nating palayan, sapat na ang tamang kagamitang pang-kamay."),
            ],
        },
        {
            "id":    "S2P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Tatlumpung segundo, bata! Pumili ka na!"),
            ],
        },
        {
            "id":    "S2P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Heto na po ang sumpa! Kailangan ko pong pumili agad!"),
            ],
        },
 
        # ── Plowing — choice (TIMER) ───────────────────────────
        {
            "id":            "S2P7",
            "type":          "choice",
            "day":           1,
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Bilis! Alin ang tamang kagamitan para basagin ang matigas na lupa ng palayan?",
            "retry_question": "Mabilis! Aling kagamitan ang may lakas na makabasag ng matigas na lupa?",
            "choices": [
                {"img": "buttons/choice_hoe.png",    "label": "", "frame": False},
                {"img": "buttons/choice_trowel.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S2P7_right_1",
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
                ("lucas", "Tama at mabilis! Ang asarol ang tamang kagamitan sa pagbasag ng matigas na lupa ng palayan."),
            ],
        },
        {
            "id":          "S2P7_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Malapad at matibay ang asarol, kaya nito ang matigas na lupa."),
            ],
        },
        {
            "id":              "S2P7_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Naku po! Masyadong maliit ang dulo para sa ganito kalaking palayan. Humanap tayo ng mas malakas na kagamitan!"),
            ],
        },
        {
            "id":              "S2P7_wrong_2",
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
                ("baron", "HAHAHA! Naubos na ang oras ninyo! Mag-isip kayo nang mas mabilis!"),
            ],
        },
        {
            "id":    "S2P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Susunod, pantayin natin ang putik at tanggalin ang mga ugat ng damo bago tayo magtanim ng mga punla."),
                ("lola", "Harrowing ang tawag dito. Kapag hindi ito ginawa, aagawan ng damo ang palay sa sustansya."),
            ],
        },
 
        # ── Harrowing — Weed Removal Card scan (TIMER) ─────────
        {
            "id":       "S2P9",
            "type":     "scan",
            "day":      1,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lola": {"side": "left", "expression": "default", "flip": False}},
            "active":   "lola",
            "timer":    True,
            "card":     "AC-03 Weed Removal Card",
            "dialogue": "Lola: Pantayin natin ang lupa at alisin ang mga ugat ng damo bago tayo magtanim, apo! I-scan ang Weed Removal Card, bilis!",
            "question": "Scan the Weed Removal Card to harrow the paddy — level the soil and clear weed roots before transplanting.",
        },
        {
            "id":    "S2P10",
            "type":  "dialogue",
            "bg":    "background/ricebg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Pantay na pantay na po ang palayan, Lola! Parang malambot na higaan para sa mga punla."),
            ],
        },
 
        # ── Day 20 — Transplanting ─────────────────────────────
        {
            "id":   "day20_fade",
            "type": "transition",
        },
        {
            "id": "S3P1",
            "type": "narration_overlay",
            "day": 20,
            "bg": "background/ricebg.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "20 araw na ang lumipas. "
                "Matitibay na at malalago ang mga punla sa seedbed, "
                "at handa na rin ang palayan na tatanggap sa kanila."
            ),
        },
        {
            "id":    "S3P2",
            "type":  "dialogue",
            "day":   20,
            "bg":    "background/ricebg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Dahan-dahan mong hugutin ang mga punla, apo, at huwag mong kalimutang isama ang putik sa kanilang mga ugat."),
                ("lola", "Dalawa hanggang tatlong punla sa bawat butas, at mababaw lamang ang pagkakatanim."),
            ],
        },
        {
            "id":    "S3P3",
            "type":  "dialogue",
            "bg":    "background/ricebg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Opo, Lola. Ngayon po, kailangan kong pumili agad kung paano ko sila itatanim!"),
            ],
        },
 
        # ── Transplanting — choice (TIMER) ─────────────────────
        {
            "id":            "S3P4",
            "type":          "choice",
            "day":           20,
            "bg":            "background/ricebg.jpg",
            "timer":         True,
            "question":       "Bilis! Paano dapat itanim ang mga punla ng palay sa palayan?",
            "retry_question": "Mabilis! Isipin kung paano makakadaan ang hangin at sikat ng araw sa mga halaman.",
            "choices": [
                {"img": "buttons/choice_straight_rows.png",   "label": "", "frame": False},
                {"img": "buttons/choice_scattered_rows.png",  "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S3P4_right_1",
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
                ("lucas", "Tama at mabilis! Sa tuwid na hilera, nakakadaan ang hangin at sikat ng araw, at mas madaling bunutan ng damo."),
            ],
        },
        {
            "id":          "S3P4_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Ang tuwid na hilera ay nakakatulong ding maiwasan ang sakit na dulot ng sobrang siksik na tanim."),
            ],
        },
        {
            "id":              "S3P4_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Naku po! Kapag magulo at siksik ang tanim, mahirap itong alagaan at madaling dapuan ng sakit."),
            ],
        },
        {
            "id":              "S3P4_wrong_2",
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
                ("baron", "HAHAHA! Itanim ninyo kung saan-saan! Mas magulo, mas masaya!"),
            ],
        },
        {
            "id":    "S3P5",
            "type":  "dialogue",
            "bg":    "background/ricebg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ngayon, papasukin na natin ang tubig sa palayan. Mababaw lamang ang kailangan natin."),
            ],
        },
 
        # ── Water level — Water Card scan (TIMER) ──────────────
        {
            "id":       "S3P6",
            "type":     "scan",
            "day":      20,
            "bg":       "background/ricebg.jpg",
            "chars":    {"lola": {"side": "left", "expression": "default", "flip": False}},
            "active":   "lola",
            "timer":    True,
            "card":     "AC-01 Water Card",
            "dialogue": "Lola: Papasukin natin ang tubig sa tamang lalim, apo. Hindi sobrang lalim at hindi rin tuyo. I-scan ang Water Card ngayon din!",
            "question": "Scan the Water Card to flood the rice paddy to the correct water level.",
        },
        {
            "id":    "S3P7",
            "type":  "dialogue",
            "bg":    "background/ricebg2.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Kapag mababaw ang tubig, hindi malulunod ang mga punla, at mas madali silang sumuwi."),
            ],
        },
 
        # ── Day 25 — Golden apple snails ───────────────────────
        {
            "id":   "day25_fade",
            "type": "transition",
        },
        {
            "id":    "S4P1",
            "type":  "dialogue",
            "day":   25,
            "bg":    "background/ricebg2.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Naghanda ako ng aking mga bagong kasama! Mga GOLDEN APPLE SNAILS!"),
                ("baron", "Uubusin ng aking mga kuhol ang mga bagong tanim ninyong palay! HAHAHAHA!"),
            ],
        },
        {
            "id":    "S4P2",
            "type":  "dialogue",
            "bg":    "background/ricebg3.jpg",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Lola! May mga kulay-rosas na itlog sa mga tangkay, at kinakain ng mga kuhol ang mga murang punla!"),
            ],
        },
        {
            "id":    "S4P3",
            "type":  "dialogue",
            "bg":    "background/ricebg3.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Huwag kang mataranta, apo. Ang mga bagong tanim ang pinakamadaling masira ng golden apple snail."),
                ("lola", "May paraan tayong hindi gumagamit ng lason."),
            ],
        },
 
        # ── Golden snails — choice ─────────────────────────────
        {
            "id":            "S4P4",
            "type":          "choice",
            "day":           25,
            "bg":            "background/ricebg3.jpg",
            "question":       "Dumarami ang mga golden apple snail sa palayan. Alin ang mas ligtas at mas napapanatiling paraan ng pagkontrol sa kanila?",
            "retry_question": "Sandali, baka makasama sa ibang buhay sa palayan ang paraang iyon. Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_handpick_ducks.png",  "label": "", "frame": False},
                {"img": "buttons/choice_chemical_spray.png",  "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S4P4_right_1",
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
                ("lucas", "Tama! Pupulutin natin ang mga kuhol at ang kanilang mga itlog, at ipapakain natin ang mga kuhol sa mga bibe."),
            ],
        },
        {
            "id":          "S4P4_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Nawawala ang peste at nabubusog pa ang ating mga bibe. Walang nasasayang."),
            ],
        },
        {
            "id":              "S4P4_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Naku po! Ang kemikal na lason ay maaaring makasama rin sa mga isda at palaka sa palayan."),
            ],
        },
        {
            "id":              "S4P4_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Mag-ingat sa paggamit ng lason! Madali itong kumalat sa tubig ng palayan at makasama sa lahat ng nakatira roon."),
            ],
        },
 
        # ── Day 30 — Baron's synthetic fertilizer ──────────────
        {
            "id":   "day30_fade",
            "type": "transition",
        },
        {
            "id":    "S5P1",
            "type":  "dialogue",
            "day":   30,
            "bg":    "background/ricebg4.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Heto ang regalo ko sa inyo! Isang sakong sintetikong urea!"),
                ("baron", "Isaboy ninyo ang buong sako, at tataas agad ang inyong mga palay!"),
            ],
        },
        {
            "id":    "S5P2",
            "type":  "dialogue",
            "bg":    "background/ricebg4.jpg",
            "chars": {"lucas": {"side": "left", "expression": "defense", "flip": True}},
            "lines": [
                ("lucas", "Huwag po, Lola! Kapag sobra ang kemikal na pataba, dadaloy ito sa tubig ng palayan at makakasama sa mga isda, mga palaka, at sa lupa."),
            ],
        },
        {
            "id":    "S5P3",
            "type":  "dialogue",
            "bg":    "background/ricebg4.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Tama ka, apo. Hindi ang pinakamabilis ang hanap natin, kundi ang tamang pagkain para sa lupa at sa halaman."),
                ("lola", "Ano ang gagawin natin sa regalong ito ni Baron?"),
            ],
        },
        {
            "id":            "S5P4",
            "type":          "choice",
            "day":           30,
            "bg":            "background/ricebg4.jpg",
            "question":       "Inalok ni Baron ang mag-lola ng isang sakong sintetikong urea. Ano ang dapat nilang gawin dito?",
            "retry_question": "Sandali, baka masira ang buong palayan kapag iyan ang ginawa natin. Subukan nating muli.",
            "choices": [
                {"img": "buttons/choice_decline_sack.png", "label": "", "frame": False},
                {"img": "buttons/choice_pour_sack.png",    "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S5P4_right_1",
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
                ("lucas", "Tama! Tatanggihan natin ang sako at gagamit tayo ng mas ligtas na organikong pataba para sa palayan."),
            ],
        },
        {
            "id":          "S5P4_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Mas mainam ang dahan-dahang pagpapakain sa lupa kaysa sa biglaang sobrang pataba."),
            ],
        },
        {
            "id":              "S5P4_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Naku po! Kapag isinaboy natin ang buong sako, maaaring masira ang tubig ng palayan at mapahamak ang mga isda at palaka."),
            ],
        },
        {
            "id":              "S5P4_wrong_2",
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
                ("baron", "HA! Isaboy ninyo lahat! Mas marami, mas mabilis na masisira ang palayan ninyo!"),
            ],
        },
        {
            "id":    "S5P5",
            "type":  "dialogue",
            "bg":    "background/ricebg4.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Hmp! Mga matitigas ang ulo! Tingnan natin kung hanggang kailan kayo tatagal!"),
            ],
        },
 
        # ── Day 35 — Organic fertilizer ────────────────────────
        {
            "id":   "day35_fade",
            "type": "transition",
        },
        {
            "id":    "S6P1",
            "type":  "dialogue",
            "day":   35,
            "bg":    "background/ricebg4.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Lola, nagsusuwi na po ang mga palay! Parami nang parami ang mga bagong usbong sa bawat puno."),
            ],
        },
        {
            "id":    "S6P2",
            "type":  "dialogue",
            "bg":    "background/ricebg4.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ibig sabihin, malakas ang mga halaman, ngunit kailangan nila ng sapat na pagkain."),
                ("lola", "Gagamitin natin ang compost mula sa dayami ng nakaraang ani, at dadagdagan natin ng vermicast na ibinigay ni Kapitan."),
            ],
        },
        {
            "id":       "S6P3",
            "type":     "scan",
            "day":      35,
            "bg":       "background/ricebg4.jpg",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-02 Fertilizer Card",
            "dialogue": "Lucas: I-scan natin ang Fertilizer Card, Lola, para piliin ang organikong pataba na ligtas para sa palayan. Bilis!",
            "question": "Scan the Fertilizer Card to choose organic fertilizer safe for the rice paddy ecosystem.",
        },
        {
            "id":    "S6P4",
            "type":  "dialogue",
            "bg":    "background/ricebg4.jpg",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Ayan, apo! Hindi nasira ang tubig, at buhay na buhay pa rin ang mga palaka at isda sa ating palayan."),
            ],
        },
 
        # ── Day 45 — Weeding ───────────────────────────────────
        {
            "id":   "day45_fade",
            "type": "transition",
        },
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   45,
            "bg":    "background/ricebg5.jpg",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "lines": [
                ("lucas", "Lola, tumutubo na naman po ang mga damo sa pagitan ng mga hilera ng palay."),
                ("lucas", "Aagawan nila ng sustansya ang mga suwi."),
            ],
        },
        {
            "id":    "S7P2",
            "type":  "dialogue",
            "bg":    "background/ricebg5.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Tanggalin natin ang mga ito, apo. Ngunit dahan-dahan lamang para hindi masira ang mga puno ng palay."),
            ],
        },
 
        # ── Weeding — choice (TIMER) ───────────────────────────
        {
            "id":            "S7P3",
            "type":          "choice",
            "day":           45,
            "bg":            "background/ricebg5.jpg",
            "timer":         True,
            "question":       "Bilis! Alin ang tamang kagamitan para maingat na alisin ang damo sa pagitan ng mga puno ng palay?",
            "retry_question": "Mabilis! Kailangan ng kagamitang tumpak at hindi makakasira sa mga puno ng palay.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "", "frame": False},
                {"img": "buttons/choice_hoe.png",    "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S7P3_right_1",
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
                ("lucas", "Tama at mabilis! Maliit at tumpak ang dulo, kaya maaalis natin ang damo nang hindi nasisira ang mga suwi."),
            ],
        },
        {
            "id":          "S7P3_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Maingat ang kamay mo, kaya hindi nasaktan ang mga palay."),
            ],
        },
        {
            "id":              "S7P3_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Naku po! Masyadong malapad ang asarol at maaaring masira ang mga puno ng palay sa pagitan ng hilera."),
            ],
        },
        {
            "id":              "S7P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Mag-ingat! Ang malapad na kagamitan ay madaling makasugat sa mga ugat ng palay."),
            ],
        },
 
        # ── Day 96 — Pre-harvest drainage ──────────────────────
        {
            "id":   "day96_fade",
            "type": "transition",
        },
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   96,
            "bg":    "background/ricebg5.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Baha! Bibigyan ko ng tubig ang palayan ninyo hanggang sa huling araw!"),
                ("baron", "Hayaan ninyong lumubog ang bawat butil! HAHAHAHA!"),
            ],
        },
        {
            "id":    "S8P2",
            "type":  "dialogue",
            "bg":    "background/ricebg6.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Malapit nang mahinog ang palay, apo. Kailangan na nating gawin ang isang mahalagang hakbang."),
            ],
        },
        {
            "id":            "S8P3",
            "type":          "choice",
            "day":           96,
            "bg":            "background/ricebg6.jpg",
            "question":       "Halos dalawang linggo na lang bago ang pag-ani. Ano ang dapat gawin sa tubig sa palayan?",
            "retry_question": "Sandali, isipin natin kung ano ang kailangan ng lupa at ng mga butil bago anihin. Subukan nating muli.",
            "choices": [
                {"img": "buttons/choice_drain_field.png", "label": "", "frame": False},
                {"img": "buttons/choice_flood_field.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S8P3_right_1",
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
                ("lucas", "Tama! Pinatutuyo natin ang palayan para tumigas ang lupa at mas madali tayong makapag-ani."),
            ],
        },
        {
            "id":          "S8P3_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Mas pantay rin ang paghinog ng mga butil kapag pinatuyo ang palayan bago anihin."),
            ],
        },
        {
            "id":              "S8P3_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Naku po! Kapag basa pa ang lupa, mahirap ang pag-ani at maaaring mabulok ang ilang butil."),
            ],
        },
        {
            "id":              "S8P3_wrong_2",
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
                ("baron", "HAHAHA! Bahain ninyo hanggang huli! Mas mahirap anihin, mas masaya!"),
            ],
        },
 
        # ── Day 110 — Harvest ──────────────────────────────────
        {
            "id":   "day110_fade",
            "type": "transition",
        },
        {
            "id":    "S9P1",
            "type":  "dialogue",
            "day":   110,
            "bg":    "background/ricebg7.jpg",
            "chars": {"lola": {"side": "left", "expression": "celebrates", "flip": False}},
            "lines": [
                ("lola", "Tingnan mo, apo! Kulay ginto na ang palay at nakayuko na sa bigat ng mga butil."),
                ("lola", "Oras na para umani!"),
            ],
        },
        {
            "id":    "S9P2",
            "type":  "dialogue",
            "bg":    "background/ricebg7.jpg",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Kailangan ko pong pumili agad ng palay na handa nang anihin, Lola. Hindi po ako magkakamali!"),
            ],
        },
 
        # ── Harvest — choice (TIMER) ───────────────────────────
        {
            "id":            "S9P3",
            "type":          "choice",
            "day":           110,
            "bg":            "background/ricebg7.jpg",
            "timer":         True,
            "question":       "Bilis! Alin ang palay na handa nang anihin?",
            "retry_question": "Mabilis! Ang handa nang anihing palay ay kulay ginto at nakayuko sa bigat ng butil.",
            "choices": [
                {"img": "buttons/choice_rice_golden.png", "label": "", "frame": False},
                {"img": "buttons/choice_rice_green.png",  "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S9P3_right_1",
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
                ("lucas", "Tama at mabilis! Kulay ginto at nakayuko ang palay na puno ng butil at handa nang anihin."),
            ],
        },
        {
            "id":          "S9P3_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Ang tamang pagpili ng oras ng pag-ani ay nagbibigay ng pinakamasarap at pinakamaraming bigas."),
            ],
        },
        {
            "id":              "S9P3_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Naku po! Berde pa ang mga butil na iyan, kaya hindi pa sila ganap na hinog."),
            ],
        },
        {
            "id":              "S9P3_wrong_2",
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
                ("baron", "HAHAHA! Anihin ninyo na kahit berde pa! Mas kaunti ang bigas ninyo!"),
            ],
        },
        {
            "id":       "S9P4",
            "type":     "scan",
            "day":      110,
            "bg":       "background/ricebg7.jpg",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-05 Harvest Card",
            "dialogue": "Lucas: Napili na po natin ang tamang palay, Lola! I-scan natin ang Harvest Card para makumpirma ang pag-aani. Bilis!",
            "question": "Scan the Harvest Card to confirm the golden, bowing-down rice stalks are ready to harvest.",
        },
        {
            "id":    "S9P5",
            "type":  "dialogue",
            "bg":    "background/ricebg7.jpg",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Gagapasin natin ang mga uhay gamit ang karit, apo, at ihihiwalay natin ang mga butil sa tangkay."),
            ],
        },
 
        # ── Sun-drying ─────────────────────────────────────────
        {
            "id":    "S10P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Ipasok ninyo na agad sa sako habang basa pa! Mabubulok na iyan kung maghihintay pa kayo!"),
            ],
        },
        {
            "id":    "S10P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "angry", "flip": False}},
            "lines": [
                ("lola", "Huwag kang maniwala sa kaniya, apo! Ang basang palay sa saradong sako ay aamagin."),
            ],
        },
        {
            "id":            "S10P3",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Bagong gapas ang palay at basa pa ang mga butil. Ano ang dapat gawin dito bago itago?",
            "retry_question": "Sandali, isipin natin kung ano ang nangyayari sa basang butil sa loob ng saradong sako. Subukan nating muli.",
            "choices": [
                {"img": "buttons/choice_sun_dry.png", "label": "", "frame": False},
                {"img": "buttons/choice_wet_sack.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S10P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Tama! Pinatutuyo natin ang palay sa araw para hindi ito amagin. Ang amag ay maaaring gumawa ng aflatoxin, isang lason na mapanganib sa kakain."),
            ],
        },
        {
            "id":          "S10P3_right_2",
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
                ("lucas", "Magaling! Ilalatag po natin ang palay sa malinis na trapal at hahaluin natin ito paminsan-minsan para pantay ang pagkatuyo."),
            ],
        },
        {
            "id":              "S10P3_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Naku po! Ang basang palay sa saradong sako ay aamagin, at mapanganib itong kainin."),
            ],
        },
        {
            "id":              "S10P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Huwag munang itago! Ang kahalumigmigan sa loob ng sako ay nagpapabilis ng pagkabulok."),
            ],
        },
 
        # ── Day 113 — Safe storage, the hex breaks ─────────────
        {
            "id":   "day113_fade",
            "type": "transition",
        },
        {
            "id":    "S11P1",
            "type":  "dialogue",
            "day":   113,
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Lucas! Lola Maria! Narinig kong tapos na kayong magpatuyo ng palay."),
                ("kapitan", "May bodega sa barangay hall na puwedeng paglagyan ng inyong ani."),
            ],
        },
        {
            "id":    "S11P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Salamat po, Kapitan! Ngunit kailangan po nating ihanda nang tama ang pag-iimbak nito."),
            ],
        },
        {
            "id":            "S11P3",
            "type":          "choice",
            "day":           113,
            "bg":            "background/scenebg_default.png",
            "question":       "Paano dapat itago ang tuyong palay para manatili itong ligtas at malinis?",
            "retry_question": "Sandali, isipin natin kung paano mapipigilan ang daga at kahalumigmigan. Subukan nating muli.",
            "choices": [
                {"img": "buttons/choice_sealed_raised.png", "label": "", "frame": False},
                {"img": "buttons/choice_open_basket.png",   "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S11P3_right_1",
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
                ("lucas", "Tama! Ang saradong sako na nakataas mula sa sahig ay iniingatan ang palay laban sa daga at sa halumigmig ng sahig."),
            ],
        },
        {
            "id":          "S11P3_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Magaling, Lucas! Ang maayos na imbakan ang huling hakbang para siguradong ligtas ang ating pagkain."),
            ],
        },
        {
            "id":              "S11P3_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Naku po! Ang bukas na basket sa lupa ay madaling maabot ng daga at ng halumigmig."),
            ],
        },
        {
            "id":              "S11P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Mag-ingat! Mawawala ang buong ani natin kapag nakapasok ang mga daga at ang halumigmig."),
            ],
        },
        {
            "id":   "day113_fade",
            "type": "transition",
        },
        {
            "id":    "S11P4",
            "type":  "dialogue",
            "bg":    "background/storage.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "nervous"}},
            "lines": [
                ("baron", "Imposible! Natapos ninyo ang lahat ng gawain, at hindi kayo nagmadali!"),
                ("baron", "Paanong hindi tumalab ang sumpa ng oras?"),
            ],
        },
        {
            "id":    "S11P5",
            "type":  "dialogue",
            "bg":    "background/storage.jpg",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Hindi po kami nagmadali, Baron. Naghanda po kami."),
                ("lucas", "Alam po namin ang tamang gagawin sa bawat hakbang, kaya kahit anong sumpa, hindi kami natinag."),
            ],
        },
        {
            "id":    "S11P6",
            "type":  "dialogue",
            "bg":    "background/storage.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "defeated"}},
            "lines": [
                ("baron", "Hmp... Hindi pa ito ang katapusan."),
            ],
        },
        {
            "id": "S11P7",
            "type": "scene",
            "bg": "background/storage.jpg",
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
 
        # ── The Bigas memory ───────────────────────────────────
        {
            "id":    "S12P1",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Bigas... Ang bangong ito ng bagong lutong kanin..."),
                ("lola", "Naaalala ko na! Lugaw ang unang pagkaing inihain ko sa nanay mo noong sanggol pa siya, at sinangag ang almusal namin ng lolo mo tuwing umaga!"),
            ],
        },
        {
            "id":    "S12P2",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "celebrates", "flip": False}},
            "lines": [
                ("lola", "Kanin din ang laging nasa mesa tuwing may handaan sa ating pamilya. Hindi ito kailanman nawala."),
            ],
        },
        {
            "id":    "S12P3",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Walo na po ang naibalik nating alaala, Lola. Dalawa na lang po ang natitira bago ang Pista."),
            ],
        },
        {
            "id": "S12P4",
            "type": "narration_overlay",
            "day": 113,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Muling nagkaroon ng amoy ng bagong lutong kanin ang munting kusina ni Lola Maria. "
                "Naibalik na ang Bigas Memory."
            ),
        },
    ],
}