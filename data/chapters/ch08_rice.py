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
            "logo": "logos/ch1logo.png",
        },

        # ── Panel 1 — Baron's Time-Warp Hex ───────────────────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Kung hindi kayo natinag ng panahon, tatinagin ko kayo ng ORAS! Mula ngayon, tatlumpung segundo lang bawat galaw! Bilisan ninyo kung kaya!"),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Palay ang puso ng ating baryo, apo. Kung ito ang pinakamahirap, kailangan nating igalang ito nang mabuti. Maingat, maingat."),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Handa na tayo, Lola. Tara, bilisan natin — at huwag mag-alala. Bawat hakbang natin, may tama."),
            ],
        },

        # ── Panel 2 — Trivia: soak seeds to break dormancy ────
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Ibabad muna sa tubig ang mga buto ng palay — dalawampu't apat na oras — bago itanim. Para mas mabilis sumibol."),
            ],
        },
        {
            "id":            "S2P2",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Totoo ba na ang pagbabad ng buto ay nagpapalabas ng pagtulog nito para mas mabilis sumibol?",
            "retry_question": "Isipin muli! Ano ang ginagawa ng tubig sa loob ng buto ng palay?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Totoo — nagigising ang buto"},
                {"img": "buttons/choice_hoe.png",    "label": "Mali — walang epekto ang pagbabad"},
            ],
            "correct": 0,
        },
        {
            "id":          "S2P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Tama! Ang pagbabad ay nagigising ang buto mula sa pagtulog nito — tatlong araw na hintay, naiiwasan sa isang gabing pagbabad!"),
            ],
        },
        {
            "id":               "S2P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Mali! Ang tubig ay pumapasok sa buto at ginigising ang proseso ng pagsisibol. Malaking pagkakaiba nito sa bilis ng pag-ani."),
            ],
        },

        # ── Day 1 transition ───────────────────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },

        # ── Panel 3 — Tool: Asarol for plowing (TIMER) ────────
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Kailangan nating basagin ang matigas na lupa ng palayan, Lola — bilis! Ang Baron ay nagbibilang ng segundo!"),
            ],
        },
        {
            "id":            "S3P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Alin ang tamang kagamitan para basagin ang matigas na lupa ng palayan (plowing)?",
            "retry_question": "Mabilis! Anong kagamitan ang nakaka-basag ng matigas na lupa?",
            "choices": [
                {"img": "buttons/choice_hoe.png",    "label": "Asarol — para sa plowing"},
                {"img": "buttons/choice_trowel.png", "label": "Gunting — para sa paggupit"},
            ],
            "correct": 0,
        },
        {
            "id":          "S3P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama at mabilis! Ang Asarol ang tamang kagamitan para sa plowing — paghahanda ng lupa ng palayan."),
            ],
        },
        {
            "id":               "S3P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Mabilis! Ang Gunting ay hindi para sa lupa — para sa mga dahon iyon. Piliin ang tamang kagamitan para sa plowing!"),
            ],
        },

        # ── Panel 4 — Weed removal scan: harrowing (TIMER) ───
        {
            "id":       "S4P1",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lola": "left"},
            "active":   "lola",
            "timer":    True,
            "card":     "AC-03 Weed Removal Card",
            "dialogue": "Lola: Pantayin natin ang lupa, alisin ang ugat ng damo, bago tayo mag-transplant! I-scan ang Weed Removal Card, mabilis!",
            "question": "Scan the Weed Removal Card to harrow the paddy — level the soil and clear weed roots before transplanting.",
        },

        # ── Day 20 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day20_fade",
            "type": "transition",
        },

        # ── Panel 5 — Transplant seedlings (TIMER) ────────────
        {
            "id":    "S5P1",
            "type":  "dialogue",
            "day":   20,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Ilipat na ang mga seedlings sa putik, Lola — tuwid ang hilera para makadaan ang hangin at maiwasan ang sakit!"),
            ],
        },
        {
            "id":            "S5P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Alin ang tamang kagamitan para itanim ang mga palay seedlings nang isa-isa sa putik nang tuwid?",
            "retry_question": "Mabilis! Anong kagamitan ang maingat sa pagtatanim ng isa-isang seedlings?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Dulo — maingat, isa-isa"},
                {"img": "buttons/choice_hoe.png",    "label": "Asarol — para sa malalim na hukay"},
            ],
            "correct": 0,
        },
        {
            "id":          "S5P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Ang Dulo ang tamang kagamitan para itanim ang bawat palay seedlings nang tumpak at maingat sa putik."),
            ],
        },
        {
            "id":               "S5P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Ang Asarol ay masyadong malawak para sa maingat na pagtatanim ng isa-isang palay seedlings. Subukan muli!"),
            ],
        },

        # ── Panel 6 — Water scan: flood the paddy (TIMER) ─────
        {
            "id":       "S6P1",
            "type":     "scan",
            "day":      20,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lola": "left"},
            "active":   "lola",
            "timer":    True,
            "card":     "AC-01 Water Card",
            "dialogue": "Lola: Buksan ang tubig sa tamang antas, apo — hindi sapaw, hindi rin tuyo. I-scan ang Water Card ngayon!",
            "question": "Scan the Water Card to flood the rice paddy to the correct water level.",
        },

        # ── Day 30 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day30_fade",
            "type": "transition",
        },

        # ── Panel 7 — Reject synthetic fertilizer ─────────────
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   30,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Heto, gumamit kayo ng synthetic urea na ito! Mabilis kayong matatapos — at mabilis din ang pagkasira ng inyong ecosystem!"),
            ],
        },
        {
            "id":    "S7P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Huwag, Lola! Ang synthetic urea ay lalasunin ang mga palaka at isda sa ating palayan — at ang buong ecosystem natin!"),
            ],
        },
        {
            "id":            "S7P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Saan dapat itapon ang synthetic urea na ibinigay ng Baron?",
            "retry_question": "Isipin muli! Ang synthetic urea ay makakalason sa ating palayan at sa mga hayop dito.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Basurahan — protektahan ang ecosystem"},
                {"img": "buttons/choice_hoe.png",    "label": "Sa palayan — para mabilis"},
            ],
            "correct": 0,
        },
        {
            "id":          "S7P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Rice straw compost na lang ang sikreto natin — hindi kemikal. Protektahan natin ang mga palaka at isda sa ating palayan!"),
            ],
        },
        {
            "id":               "S7P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Hindi! Ang synthetic urea ay maaaring patayin ang mga buhay na hayop sa palayan at makakalason sa ating pagkain."),
            ],
        },

        # ── Day 35 transition ─────────────────────────────────
        {
            "id":   "day35_fade",
            "type": "transition",
        },

        # ── Panel 8 — Fertilizer choice: Organic vs Chemical (TIMER) ──
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   35,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Lola, oras na para pakainin ang buong palayan — alin ang pipiliin natin para maging malusog ang lupa ng palay?"),
            ],
        },
        {
            "id":       "S8P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-02 Fertilizer Card",
            "dialogue": "I-scan ang Fertilizer Card para piliin ang tamang pataba para sa malusog na palayan — bilis!",
            "question": "Scan the Fertilizer Card to choose organic fertilizer safe for the rice paddy ecosystem.",
        },

        # ── Day 50 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day50_fade",
            "type": "transition",
        },

        # ── Panel 9 — Golden snails ────────────────────────────
        {
            "id":    "S9P1",
            "type":  "dialogue",
            "day":   50,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "GOLDEN APPLE SNAILS — heto na ang aking pinaghandang pest! Kainin na ng aking mga kuhol ang inyong palay!"),
            ],
        },
        {
            "id":    "S9P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Pulutin lang natin sila nang kamay, apo, at ipakain sa ating mga bibe. Mas mabuti pa sa kahit anong lason!"),
            ],
        },
        {
            "id":            "S9P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Totoo ba na ang pag-pulot ng golden apple snails gamit ang kamay at pagpakain sa mga bibe ay sustainable pest control?",
            "retry_question": "Isipin muli! Ano ang pinakamabuting paraan para kontrolin ang golden snails nang hindi gumagamit ng lason?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Totoo — sustainable at eco-friendly"},
                {"img": "buttons/choice_hoe.png",    "label": "Mali — kailangan ng kemikal na lason"},
            ],
            "correct": 0,
        },
        {
            "id":          "S9P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Tama! Ang pag-pulot at pagpakain sa mga bibe ay sustainable — walang nasayang, pagkain pa ng bibe ang dating pest!"),
            ],
        },
        {
            "id":               "S9P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Hindi kailangan ng kemikal! Ang mga bibe ang natural na kontrol sa mga golden snail — mas ligtas at mas mabilis pa!"),
            ],
        },

        # ── Day 55 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day55_fade",
            "type": "transition",
        },

        # ── Panel 10 — Mid-season weeding (TIMER) ─────────────
        {
            "id":    "S10P1",
            "type":  "dialogue",
            "day":   55,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Tanggalin natin ang damo sa pagitan ng mga puno ng palay, Lola — bago pa makinig nito ng sustansya!"),
            ],
        },
        {
            "id":            "S10P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Alin ang tamang kagamitan para maingat na alisin ang damo sa pagitan ng mga puno ng palay?",
            "retry_question": "Mabilis! Kailangan ng tumpak na kagamitan para sa gitna ng mga puno ng palay.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Dulo — tumpak sa pagitan ng palay"},
                {"img": "buttons/choice_hoe.png",    "label": "Kalaykay — malawak, baka masira ang palay"},
            ],
            "correct": 0,
        },
        {
            "id":          "S10P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama at mabilis! Ang Dulo ang tamang kagamitan para maingat na alisin ang damo sa pagitan ng mga puno ng palay."),
            ],
        },
        {
            "id":               "S10P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Ang Kalaykay ay masyadong malawak at maaaring masira ang mga puno ng palay. Gamitin ang mas tumpak na kagamitan!"),
            ],
        },

        # ── Day 96 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day96_fade",
            "type": "transition",
        },

        # ── Panel 11 — Pre-harvest drainage ───────────────────
        {
            "id":    "S11P1",
            "type":  "dialogue",
            "day":   96,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Baha! Bibahain ko ulit ang palayan ngayon! Hayaan ang tubig na tumaas sa huli!"),
            ],
        },
        {
            "id":    "S11P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Patuyuin muna ang lupa, apo — dalawang linggo bago mag-ani — para tumigas ang lupa at hindi masira ang makinarya at butil."),
            ],
        },
        {
            "id":            "S11P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Ano ang dapat gawin dalawang linggo bago anihin ang palay?",
            "retry_question": "Isipin muli! Bakit kailangan patigas ng lupa bago mag-ani ng palay?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Patuyuin ang tubig — patigas ang lupa"},
                {"img": "buttons/choice_hoe.png",    "label": "Baha pa lalo para mas madaling maani"},
            ],
            "correct": 0,
        },
        {
            "id":          "S11P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Sa basang lupa, masasira ang makinarya at mabubulok ang butil ng palay. Patuyuin muna ang palayan bago mag-ani!"),
            ],
        },
        {
            "id":               "S11P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Huwag maniwala kay Baron! Sa laging basang palayan, masisira ang mga makinarya at mabubulok ang ating palay."),
            ],
        },

        # ── Day 110 transition (TIME SKIP) ────────────────────
        {
            "id":   "day110_fade",
            "type": "transition",
        },

        # ── Panel 12 — Harvest scan (TIMER) ───────────────────
        {
            "id":    "S12P1",
            "type":  "dialogue",
            "day":   110,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Kulay ginto na ang palay at nakayuko na sa bigat ng butil... oras na, apo. I-scan natin ngayon!"),
            ],
        },
        {
            "id":            "S12P2_choice",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":      "Alin ang tamang palay na handa nang anihin? (30 segundo!)",
            "retry_question": "Mabilis! Ang tamang palay ay gintong kulay at nakayuko sa bigat ng butil — hindi berde at tuwid.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Gintong butil, nakayuko sa bigat"},
                {"img": "buttons/choice_hoe.png",    "label": "Berde pa ang butil, tuwid ang tangkay"},
            ],
            "correct": 0,
        },
        {
            "id":          "S12P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Tama at mabilis! Ginto at nakayuko — puno ng butil, handa nang anihin!"),
            ],
        },
        {
            "id":               "S12P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Hindi pa! Berde pa iyan — kailangan pang lumutog ang butil at maging ginto bago anihin. Mabilis!"),
            ],
        },
        {
            "id":       "S12P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-05 Harvest Card",
            "dialogue": "Napili mo na ang tamang palay! I-scan ang Harvest Card para ma-confirm ang pag-aani — bilis!",
            "question": "Scan the Harvest Card to confirm the golden, bowing-down rice stalks are ready to harvest.",
        },

        # ── Panel 13 — Sun drying ──────────────────────────────
        {
            "id":    "S13P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Ipasok na agad sa sako habang basa! Bilisan niyo, mabibulok na siya!"),
            ],
        },
        {
            "id":    "S13P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Huwag maniwala, apo! Ang basang palay sa kulob na sako ay aamagin at lalasunin ang lahat ng kakain nito."),
            ],
        },
        {
            "id":            "S13P3",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Totoo ba na ang palay ay kailangan munang matuyo sa araw bago itago sa sako?",
            "retry_question": "Isipin muli! Ano ang mangyayari sa basang palay na agad na inilagay sa kulob na lalagyan?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Totoo — iiwasan ang mapanganib na amag"},
                {"img": "buttons/choice_hoe.png",    "label": "Mali — diretso sa sako habang basa"},
            ],
            "correct": 0,
        },
        {
            "id":          "S13P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Tama! Ang sun-drying ay nagpoprotekta laban sa mapanganib na aflatoxin — isang uri ng amag na nakamamatay. Siguraduhing tuyo bago itago!"),
            ],
        },
        {
            "id":               "S13P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Huwag pakinggan si Baron! Ang basang palay ay aamagin at makakalason sa lahat. Ipatuyo muna sa araw!"),
            ],
        },

        # ── Day 113 transition ────────────────────────────────
        {
            "id":   "day113_fade",
            "type": "transition",
        },

        # ── Panel 14 — Safe storage ───────────────────────────
        {
            "id":    "S14P1",
            "type":  "dialogue",
            "day":   113,
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Saan natin itatago ito na ligtas sa mga daga at insekto, Lola? Kailangan ng tamang lugar para sa ating ani."),
            ],
        },
        {
            "id":            "S14P2",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Paano dapat itago ang tuyong palay para manatiling ligtas at malinis?",
            "retry_question": "Isipin muli! Paano mapipigilan ang daga at kahalumigmigan mula sa ating tuyong palay?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Saradong sako, itaas mula sa sahig"},
                {"img": "buttons/choice_hoe.png",    "label": "Bukas na basket sa lupa"},
            ],
            "correct": 0,
        },
        {
            "id":          "S14P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Ang naka-angat na imbakan ay nagpoprotekta sa palay mula sa daga at kahalumigmigan ng sahig. Food safety ang huling hakbang!"),
            ],
        },
        {
            "id":               "S14P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Ang bukas na basket sa lupa ay madaling maabot ng daga at mabibigo ng kahalumigmigan. Kailangan ng saradong lalagyan na nakataas!"),
            ],
        },

        # ── Panel 15 — End: Bigas memory ──────────────────────
        {
            "id":    "S15P1",
            "type":  "dialogue",
            "day":   113,
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Bigas... para sa sinangag, para sa kanin sa aming handaan... Naaalala ko na! Lahat ng inihanda ko para sa pamilya, simula pa noong bata pa ang iyong ina!"),
            ],
        },
        {
            "id":    "S15P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Walo na, Lola! Dalawa na lang ang natitira. Parang mas malinaw na ang lahat ngayon — at mas malapit na tayo sa Pista."),
                ("lucas", "Bigas Memory — UNLOCKED!"),
            ],
        },

    ],
}
