# ============================================================
#  CHAPTER 6 — EGGPLANT (Talong)
#  Intermediate | 11 story panels | Total growing days: 80
#  Characters: Lucas, Kapitan Ernesto, Blight Baron
#  MECHANICS: Hardening off, vermicast, mulching, shoot borers
# ============================================================

CHAPTER = {
    "id":         "ch06",
    "crop":       "Eggplant",
    "level":      "intermediate",
    "memory":     "Kare-Kare Memory",
    "total_days": 80,
 
    "slides": [
 
        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "chapter6.png",
        },
 
        # ── Scene 1 — Kapitan lost his purpose ─────────────────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Magandang umaga, Lucas. Mabuti at napadaan ka."),
                ("kapitan", "May gusto sana akong ipakiusap sa iyo."),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Magandang umaga rin po, Kapitan Ernesto. Ano po ang maitutulong ko?"),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Dati, tuwing may handaan sa barangay hall, ako ang pinakamasaya sa lahat."),
                ("kapitan", "Ngunit ngayon, hindi ko na maalala kung paano ako gagalaw bilang Kapitan."),
            ],
        },
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "lines": [
                ("lucas", "Bakit po ninyo nasabi iyan, Kapitan?"),
            ],
        },
        {
            "id":    "S1P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Mula nang masira ang mga pananim natin, wala na akong maihandang pagkain para sa lahat."),
                ("kapitan", "Unti-unti nang hindi nagtitipon ang mga tao. Pakiramdam ko, wala na akong silbi bilang Kapitan."),
            ],
        },
        {
            "id":    "S1P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Hindi po totoo iyan, Kapitan. Kayo po ang dahilan kung bakit magkakakilala ang buong baryo."),
            ],
        },
        {
            "id":    "S1P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Salamat, hijo. Kaya naisip kong magtanim muli ng talong."),
                ("kapitan", "Natatandaan kong may talong sa pagkaing inihahain ko noon, ngunit nawala na ang pangalan at lasa nito sa isip ko."),
                ("kapitan", "Baka maalala ko ito kapag nakita ko ulit ang mismong bunga."),
            ],
        },
        {
            "id":    "S1P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Ang problema, noong nakaraang taon ay naninilaw ang mga dahon ng talong ko at maliliit ang mga bunga nito."),
                ("kapitan", "Sa palagay ko, kulang sila sa sustansya."),
            ],
        },
        {
            "id":    "S1P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Huwag po kayong mag-alala, Kapitan. Marami na po akong natutunan kay Lola Maria noong nagtanim kami ng kamatis."),
                ("lucas", "Tutulungan ko po kayo."),
            ],
        },
        {
            "id":    "S1P10",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Maraming salamat, Lucas. May mga punla na ako sa nursery."),
                ("kapitan", "Puwede na ba natin silang itanim sa hardin ngayon din?"),
            ],
        },
        {
            "id":    "S1P11",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Hindi pa po, Kapitan. Kailangan muna silang masanay sa labas ng nursery."),
            ],
        },
        {
            "id":    "S1P12",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Parang sundalo pala, ano? Kailangan munang masanay sa init at hangin bago ipadala sa parada."),
            ],
        },
        {
            "id":    "S1P13",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Opo, Kapitan! Hardening off po ang tawag diyan."),
                ("lucas", "Unti-unti po natin silang ilalabas sa lilim, at dadagdagan natin ang oras at tindi ng sikat ng araw araw-araw."),
            ],
        },
 
        # ── Hardening off — choice ─────────────────────────────
        {
            "id":            "S1P14",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Nais ni Kapitan na ilipat agad sa hardin ang mga punla ng talong. Paano dapat sanayin ang mga ito sa labas bago itanim?",
            "retry_question": "Sandali, masyadong biglaan ang paraang iyon para sa mga murang dahon. Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_gradual_sun.png", "label": "", "frame": False},
                {"img": "buttons/choice_noon_sun.png",    "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S1P14_right_1",
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
                ("lucas", "Tama! Sisimulan natin sa isang oras sa lilim, tapos dadagdagan natin ang oras araw-araw hanggang masanay sila sa buong sikat ng araw."),
            ],
        },
        {
            "id":          "S1P14_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Magaling! Tulad ng sundalong nagsasanay, unti-unti ang dagdag ng pagod para hindi mabigla ang katawan."),
            ],
        },
        {
            "id":              "S1P14_wrong_1",
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
                ("lucas", "Naku po! Kapag biglang tinamaan ng matinding sikat ng araw ang mga punla, pumuputi at nalalanta ang kanilang mga dahon. Transplant shock po ang tawag dito."),
            ],
        },
        {
            "id":              "S1P14_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Mag-ingat tayo! Hindi pa kayang tiisin ng murang dahon ang init ng tanghaling tapat."),
            ],
        },
 
        # ── Day 21 — Transplanting ─────────────────────────────
        {
            "id":   "day21_fade",
            "type": "transition",
        },
        {
            "id": "S2P1",
            "type": "narration_overlay",
            "day": 21,
            "bg": "background/scenebg_planter.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "21 araw na ang lumipas. "
                "Sa loob ng isang linggo, unti-unting inilabas nina Lucas "
                "at Kapitan Ernesto ang mga punla sa lilim, "
                "at dinagdagan nila ang oras ng pagkakabilad nito sa araw "
                "hanggang sa masanay ang mga ito."
            ),
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "day":   21,
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Tingnan mo, Lucas! Hindi na nalalanta ang mga dahon nila at matitigas na ang kanilang mga tangkay."),
            ],
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Handa na po sila, Kapitan! Maaari na natin silang ilipat sa hardin."),
                ("lucas", "Dalawang talampakan po ang layo ng bawat isa para hindi sila magsiksikan."),
            ],
        },
        {
            "id":    "S2P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Ibabaon ba natin ang tangkay hanggang sa mga unang dahon, tulad ng ginawa ninyo sa kamatis?"),
            ],
        },
        {
            "id":    "S2P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Hindi po, Kapitan. Iba po ang talong sa kamatis."),
                ("lucas", "Itatanim lamang natin ito sa parehong lalim ng pagkakatanim nito sa lalagyan, dahil madaling mabulok ang tangkay nito kapag natabunan."),
            ],
        },
        {
            "id":    "S2P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Kaya pala. Ano ang dapat kong gamitin sa paghuhukay?"),
            ],
        },
 
        # ── Digging tool — choice ──────────────────────────────
        {
            "id":            "S2P7",
            "type":          "choice",
            "day":           21,
            "bg":            "background/scenebg_planter.png",
            "question":       "Alin ang mas angkop na kagamitan sa paghuhukay ng butas na sakto lamang sa laki ng ugat ng punla ng talong?",
            "retry_question": "Sandali, masyadong malaki ang kagamitang iyon para sa maliit na butas. Subukan nating muli.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "", "frame": False},
                {"img": "buttons/choice_hoe.png",    "label": "", "frame": False},
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
                ("lucas", "Tama! Ang dulo ang pinakaangkop sa paghuhukay ng butas na sakto sa laki ng ugat ng punla."),
            ],
        },
        {
            "id":          "S2P7_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Magaling, Lucas! Maliit at maingat ang kamay, kaya hindi masisira ang mga ugat."),
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
                ("lucas", "Naku po! Ang asarol ay masyadong malaki at maaaring makasira sa mga maliliit na ugat ng punla."),
            ],
        },
        {
            "id":              "S2P7_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Hindi iyan ang tamang kagamitan! Para sa malalawak na hukay ang asarol, hindi para sa maliliit na punla."),
            ],
        },
        {
            "id":    "S2P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Dahan-dahan po nating ilalagay ang bawat punla sa butas, at tatabunan natin ito nang marahan."),
            ],
        },
        {
            "id":    "S2P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Dapat bang diligan na natin sila agad pagkatapos ilipat?"),
            ],
        },
 
        # ── Water Card scan ────────────────────────────────────
        {
            "id":       "S2P10",
            "type":     "action_challenge",
            "day":      21,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "waters", "flip": True}},
            "active":   "lucas",
            "card":     "AC-01 Water Card",
            "overlay": "WaterCard.png",
            "dialogue": "Lucas: Opo, Kapitan! Diligin natin agad ang mga punla pagkatapos ilipat. Aayos ang lupa sa paligid ng ugat at mawawala ang mga bulsa ng hangin sa ilalim nito.",
            "question": "Scan the Water Card to settle the soil around the newly transplanted eggplants.",
        },
        {
            "id":    "S2P11",
            "type":  "dialogue",
            "bg":    "background/eggplantbg.jpg",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Ang ganda tingnan! Parang nakahinga na ang mga punla."),
            ],
        },
 
        # ── Day 30 — Earthworms and vermicast ──────────────────
        {
            "id":   "day30_fade",
            "type": "transition",
        },
        {
            "id": "S3P1",
            "type": "narration_overlay",
            "day": 30,
            "bg": "background/eggplantbg.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "30 araw na ang lumipas. "
                "Mas malalago na ang mga punla ng talong, "
                "ngunit may kakaibang gumagalaw sa ilalim ng lupa."
            ),
        },
        {
            "id":    "S3P2",
            "type":  "dialogue",
            "day":   30,
            "bg":    "background/eggplantbg3.jpg",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Lucas! May mga bulate sa lupa! Nakakadiri!"),
                ("kapitan", "Tanggalin natin silang lahat bago masira ang mga halaman!"),
            ],
        },
        {
            "id":    "S3P3",
            "type":  "dialogue",
            "bg":    "background/eggplantbg3.jpg",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "lines": [
                ("lucas", "Sandali po, Kapitan! Huwag po muna!"),
                ("lucas", "Hindi po lahat ng gumagalaw sa lupa ay peste."),
            ],
        },
        {
            "id":    "S3P4",
            "type":  "dialogue",
            "bg":    "background/eggplantbg3.jpg",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Kung hindi sila peste, ano ang gagawin ko sa kanila?"),
            ],
        },
 
        # ── Vermicast — choice ─────────────────────────────────
        {
            "id":            "S3P5",
            "type":          "choice",
            "day":           30,
            "bg":            "background/eggplantbg3.jpg",
            "question":       "Nandidiri si Kapitan sa mga bulate sa lupa ng taniman. Ano ang dapat nating gawin sa mga ito?",
            "retry_question": "Sandali, baka may mahalagang trabaho ang mga bulate sa lupa. Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_keep_worms.png",   "label": "", "frame": False},
                {"img": "buttons/choice_remove_worms.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S3P5_right_1",
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
                ("lucas", "Tama! Binubungkal ng mga bulate ang lupa, at ang dumi nila ay tinatawag na vermicast. Isa itong napakasustansyang organikong pataba!"),
            ],
        },
        {
            "id":          "S3P5_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Aba, kaya pala mas maitim at mas mabango ang lupa dito kaysa sa dati kong taniman!"),
            ],
        },
        {
            "id":              "S3P5_wrong_1",
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
                ("lucas", "Naku po! Kapag inalis natin ang mga bulate, mawawala ang libre nating tagapagpayaman ng lupa."),
            ],
        },
        {
            "id":              "S3P5_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Teka muna! Baka mas makasama pa kung aalisin natin ang mga tagapag-ayos ng lupa."),
            ],
        },
        {
            "id":    "S3P6",
            "type":  "dialogue",
            "bg":    "background/eggplantbg3.jpg",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Hindi ko akalaing may silbi pala ang mga bulate. Pasensya na sa inyo, mga bulate!"),
            ],
        },
        {
            "id":    "S3P7",
            "type":  "dialogue",
            "bg":    "background/eggplantbg3.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Libre pa po ang pataba, Kapitan. Hayaan lang po nating gawin nila ang kanilang trabaho."),
            ],
        },
 
        # ── Day 35 — Fertilizer ────────────────────────────────
        {
            "id":   "day35_fade",
            "type": "transition",
        },
        {
            "id":    "S4P1",
            "type":  "dialogue",
            "day":   35,
            "bg":    "background/eggplantbg5.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Kapitan, dumarami na po ang dahon ng talong. Oras na po para dagdagan ang pagkain ng lupa."),
                ("lucas", "Ilalagay po natin ito malapit sa ugat, pero hindi dapat dumikit sa tangkay."),
            ],
        },
        {
            "id":    "S4P2",
            "type":  "dialogue",
            "bg":    "background/eggplantbg5.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "May natira akong supot ng kemikal na pataba. Maaari na ba nating gamitin iyon?"),
            ],
        },
        {
            "id":    "S4P3",
            "type":  "dialogue",
            "bg":    "background/eggplantbg5.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Mas mainam po ang organikong pataba tulad ng compost at vermicast, Kapitan."),
                ("lucas", "Dahan-dahan itong nagbibigay ng sustansya, hindi nakakasunog ng ugat, at pinapabuti pa nito ang lupa."),
            ],
        },
        {
            "id":       "S4P4",
            "type":     "action_challenge",
            "day":      35,
            "bg":       "background/eggplantbg5.png",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "card":     "AC-02A Organic Fertilizer Card",
            "overlay": "organicfertilizercard.png",
            "dialogue": "Lucas: I-scan natin ang Fertilizer Card, Kapitan, para piliin ang organikong pataba para sa malusog na lupa ng talong!",
            "question": "Scan the Fertilizer Card to choose the organic fertilizer for healthy eggplant soil.",
        },
        {
            "id":    "S4P5",
            "type":  "dialogue",
            "bg":    "background/eggplantbg5.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Ang bango ng lupa! Parang pinakain natin ang mga halaman ng masarap na handaan."),
            ],
        },
 
        # ── Day 40 — Weeding and mulching ──────────────────────
        {
            "id":   "day40_fade",
            "type": "transition",
        },
        {
            "id":    "S5P1",
            "type":  "dialogue",
            "day":   40,
            "bg":    "background/eggplantbg5.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Lucas, mabilis matuyo ang lupa sa init ng araw, at tumutubo na naman ang mga damo."),
            ],
        },
        {
            "id":    "S5P2",
            "type":  "dialogue",
            "bg":    "background/eggplantbg5.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Bubunutin muna po natin ang mga damo gamit ang kamay, Kapitan, para hindi masugatan ang tangkay ng talong."),
                ("lucas", "Pagkatapos po, may maitatakip tayo sa lupa para mabawasan ang pagsingaw ng tubig."),
            ],
        },
        {
            "id":    "S5P3",
            "type":  "dialogue",
            "bg":    "background/eggplantbg5.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Mayroon akong natirang dayami sa bodega. Maaari ba nating gamitin iyon?"),
            ],
        },
        {
            "id":            "S5P4",
            "type":          "choice",
            "day":           40,
            "bg":            "background/eggplantbg5.png",
            "question":       "Nabunot na ang mga damo. Paano dapat protektahan ang lupa sa paligid ng mga halamang talong mula sa matinding init?",
            "retry_question": "Sandali, hindi mapoprotektahan ng paraang iyan ang lupa sa init ng araw. Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_mulch_straw.png", "label": "", "frame": False},
                {"img": "buttons/choice_bare_soil.png",   "label": "", "frame": False},
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
                ("lucas", "Tama! Ang mulch ay parang kumot ng lupa. Pinapanatili nitong basa at malamig ang lupa, at pinipigilan din nitong tumubo ang mga damo."),
            ],
        },
        {
            "id":          "S5P4_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Magaling! Mas kaunti na ang pagdidilig natin at mas kaunti na rin ang bubunuting damo."),
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
                ("lucas", "Naku po! Kapag hubad ang lupa, mabilis itong matutuyo at madaling tutubuan ng damo."),
            ],
        },
        {
            "id":              "S5P4_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Mag-ingat! Ang lupang walang takip ay madaling matuyo sa matinding init."),
            ],
        },
        {
            "id":    "S5P5",
            "type":  "dialogue",
            "bg":    "background/eggplantbg5.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Maglalagay po tayo ng dayami sa paligid ng bawat halaman, pero mag-iiwan po tayo ng maliit na espasyo sa tabi ng tangkay."),
                ("lucas", "Sa ganitong paraan, hindi mababasa at mabubulok ang tangkay."),
            ],
        },
 
        # ── Day 60 — The Blight Baron and the shoot borers ─────
        {
            "id":   "day60_fade",
            "type": "transition",
        },
        {
            "id": "S6P1",
            "type": "narration_overlay",
            "day": 60,
            "bg": "background/eggplantbg5.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "60 araw na ang lumipas. "
                "Namumulaklak na at namumunga ang mga talong ni Kapitan Ernesto, "
                "ngunit may panibagong panganib na paparating."
            ),
        },
        {
            "id": "S6P2",
            "type": "scene",
            "bg": "background/eggplantbg5.png",
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
            "id":    "S6P3",
            "type":  "dialogue",
            "bg":    "background/eggplantbg5.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Kumusta, bata? Ang ganda ng hardin ninyo ngayon."),
                ("baron", "Sayang naman kung may sisira nito."),
            ],
        },
        {
            "id":    "S6P4",
            "type":  "dialogue",
            "bg":    "background/eggplantbg5.png",
            "chars": {"lucas": {"side": "left", "expression": "defense", "flip": True}},
            "lines": [
                ("lucas", "Baron! Ano na naman ang binabalak mo?"),
                ("lucas", "Hindi mo na masisira ang mga halaman namin!"),
            ],
        },
        {
            "id":    "S6P5",
            "type":  "dialogue",
            "bg":    "background/eggplantbg5.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Hahahaha! Ang tapang mo na ngayon, ha."),
                ("baron", "Hayaan mong ipakilala ko sa iyo ang mga anak kong shoot borers! Uubusin nila ang bawat talong!"),
                ("baron", "HAHAHAHAHAHA!"),
            ],
        },
        {
            "id": "S6P6",
            "type": "scene",
            "bg": "background/baroneggplantbg2.jpg",
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
            "id":   "day60_fade",
            "type": "transition",
        },
        {
            "id":    "S6P7",
            "type":  "dialogue",
            "bg":    "background/eggplantbg6.jpg",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Lucas! Nalalanta ang mga dulo ng sanga ng talong ko, at may mga butas pa sa mga bunga!"),
            ],
        },
        {
            "id":    "S6P8",
            "type":  "dialogue",
            "bg":    "background/eggplantbg6.jpg",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "lines": [
                ("lucas", "Shoot borers po ito, Kapitan. Pumapasok ang mga uod sa loob ng tangkay at bunga, kaya nalalanta ang dulo ng sanga."),
            ],
        },
        {
            "id":    "S6P9",
            "type":  "dialogue",
            "bg":    "background/eggplantbg6.jpg",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Anong gagawin natin? Mas gusto kong mag-spray na lang ng malakas na kemikal para mawala sila agad!"),
            ],
        },
        {
            "id":    "S6P10",
            "type":  "dialogue",
            "bg":    "background/eggplantbg6.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Mag-ingat po tayo, Kapitan. Baka pati ang mga kapaki-pakinabang na insekto, tulad ng mga bubuyog na tumutulong sa pamumulaklak, ay masaktan din."),
                ("lucas", "Puputulin muna po natin at itatapon sa malayo ang mga nalantang sanga at mga butas na bunga. Pagkatapos, gagamit tayo ng natural na pestisidyo."),
            ],
        },
        {
            "id":       "S6P11",
            "type":     "action_challenge",
            "day":      60,
            "bg":       "background/eggplantbg6.jpg",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "card":     "AC-04A Natural Pesticide Card",
            "overlay": "naturalpesticidecard.png",
            "dialogue": "Lucas: I-scan natin ang Pesticide Card, Kapitan, para piliin ang natural na pestisidyo laban sa shoot borers na hindi makakasama sa kalikasan!",
            "question": "Scan the Pesticide Card to choose the natural pesticide against eggplant shoot borers.",
        },
        {
            "id":    "S6P12",
            "type":  "dialogue",
            "bg":    "background/eggplantbg7.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "nervous"}},
            "lines": [
                ("baron", "Ano?! Ang mga anak ko! Bakit hindi sila nakakapasok sa mga talong?!"),
            ],
        },
        {
            "id":    "S6P13",
            "type":  "dialogue",
            "bg":    "background/eggplantbg7.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Natutunan ko po sa mga kamatis at sa mga talong na kapag maayos ang pag-aalaga, mas madaling labanan ang mga peste."),
                ("lucas", "Hindi mo na kami matatakot, Baron."),
            ],
        },
        {
            "id":    "S6P14",
            "type":  "dialogue",
            "bg":    "background/eggplantbg7.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Hmp! Hindi pa tayo tapos, bata!"),
            ],
        },
        {
            "id": "S6P15",
            "type": "scene",
            "bg": "background/eggplantbg7.jpg",
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
 
        # ── Day 80 — Harvest ───────────────────────────────────
        {
            "id":   "day80_fade",
            "type": "transition",
        },
        {
            "id": "S7P1",
            "type": "narration_overlay",
            "day": 80,
            "bg": "background/eggplantbg7.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "80 araw na ang lumipas. "
                "Sa pangangalaga nina Lucas at Kapitan Ernesto, "
                "nakaligtas ang mga talong at dumami ang mga bunga nito."
            ),
        },
        {
            "id":    "S7P2",
            "type":  "dialogue",
            "day":   80,
            "bg":    "background/eggplantbg8.jpg",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Lucas, napakaraming bunga na ang nakabitin sa mga halaman!"),
                ("kapitan", "Ngunit alin sa mga ito ang tamang anihin para sa lutuing hinahanap ko?"),
            ],
        },
        {
            "id":    "S7P3",
            "type":  "dialogue",
            "bg":    "background/eggplantbg8.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Hanapin po natin ang makinis, makinang, at matingkad na lilang talong, Kapitan."),
                ("lucas", "Kapag sobra na ang pagkahinog nito, magiging dilaw ang balat at malambot na ang laman."),
            ],
        },
        {
            "id":            "S7P4",
            "type":          "choice",
            "day":           80,
            "bg":            "background/eggplantbg8.jpg",
            "question":       "Alin sa dalawang talong ang tamang anihin ngayon?",
            "retry_question": "Sandali, tingnan nating mabuti ang kulay at hitsura ng balat ng talong. Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_eggplant_ripe.png", "label": "", "frame": False},
                {"img": "buttons/choice_eggplant_old.png",  "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S7P4_right_1",
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
                ("lucas", "Tama! Makinis, makinang, at matingkad na lila ang balat ng talong na handa nang anihin."),
            ],
        },
        {
            "id":          "S7P4_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Iyan na nga! Makinang at matigas, perpekto para sa lutuing hinahanap ko!"),
            ],
        },
        {
            "id":              "S7P4_wrong_1",
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
                ("lucas", "Naku po! Ang talong na malambot at dilaw na ang balat ay sobra na sa hinog at hindi na masarap kainin."),
            ],
        },
        {
            "id":              "S7P4_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Hindi iyan! Kapag malambot at kulubot na ang balat, lampas na ito sa tamang panahon ng pag-ani."),
            ],
        },
        {
            "id":       "S7P5",
            "type":     "action_challenge",
            "day":      80,
            "bg":       "background/eggplantbg8.jpg",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "card":     "AC-05 Harvest Card",
            "overlay": "harvestcardscan.png",
            "dialogue": "Lucas: Napili na po natin ang tamang talong! I-scan natin ang Harvest Card para makumpirma ang pag-aani.",
            "question": "Scan the Harvest Card to confirm the smooth, shiny deep-purple eggplant is ready to harvest.",
        },
        {
            "id":    "S7P6",
            "type":  "dialogue",
            "bg":    "background/eggplantbg8.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Puputulin po natin ang tangkay gamit ang malinis na gunting, Kapitan, at iiwan natin ang maliit na bahagi nito sa bunga."),
            ],
        },
 
        # ── The Kare-Kare memory ───────────────────────────────
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Ang bango at ang bigat ng talong na ito... Teka, naaalala ko na!"),
                ("kapitan", "KARE-KARE! May talong, may karne, may sarsang mani, at nagtitipon ang buong baryo sa barangay hall para sabay-sabay na kumain!"),
            ],
        },
        {
            "id":    "S8P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Iyon ang dahilan kung bakit ako naging Kapitan, Lucas. Hindi dahil sa tungkulin, kundi para mapagsama-sama ang lahat."),
            ],
        },
        {
            "id":    "S8P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Matagal na pong naghihintay ang baryo para sa inyo, Kapitan."),
                ("lucas", "Tutulungan ko po kayong magluto at magtipon muli ng lahat."),
            ],
        },
        {
            "id":    "S8P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Salamat, hijo. Dahil sa iyo, bumalik hindi lamang ang aking mga talong kundi pati ang aking layunin."),
            ],
        },
        {
            "id": "S8P5",
            "type": "narration_overlay",
            "day": 80,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Muling napuno ng tawanan at masarap na amoy ang barangay hall. "
                "Naibalik na ang Kare-Kare Memory."
            ),
        },
    ],
}