# ============================================================
#  CHAPTER 3 — OKRA
#  Beginner | 8 story panels | Total growing days: 55
#  Characters: Lucas, Chef Pablo, Blight Baron
# ============================================================

CHAPTER = {
    "id":         "ch03",
    "crop":       "Okra",
    "level":      "beginner",
    "memory":     "Sinigang na Baboy Memory",
    "total_days": 55,

    "slides": [

        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "logos/ch1logo.png",    # placeholder — replace with ch3 logo
        },

        # ── Panel 1 — Chef Pablo's empty kitchen ───────────────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Nakatitig lang ako sa pamalo ng kaldero buong umaga, Lucas. Parang may dapat akong lutuin — pero blangko ang isip ko."),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Magsisimula tayo sa simpleng gulay ngunit may sekreto ito, Chef — Okra! Tingnan mo kung paano siya tumutubo. Susundan natin siya mula buto hanggang hapag."),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Okra?! Nakakatawa! Isang gulay na 'yan ang mag-aalis ng inyong gana sa pagluluto? Panaginip na lang 'yan, mga musmos!"),
            ],
        },
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Huwag tayong pakinggan si Baron, Lucas. Kung kaya nating palaguin ang Okra, baka makuha natin ang receta na hinahanap ko."),
            ],
        },

        # ── Day 1 transition ───────────────────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },

        # ── Panel 2 — Tool choice: Asarol for sun-warmed row ──
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Mainit at maaraw ang gusto ng Okra, tama ba? Parang ako sa kusina tuwing tanghali!"),
            ],
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Eksakto, Chef! Kaya kailangan nating gumawa ng maayos na hilera sa mainit na lupa. Alin sa dalawa ang gagamitin natin?"),
            ],
        },
        {
            "id":            "S2P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Alin ang tamang kagamitan para gumawa ng hilera para sa Okra sa mainit na lupa?",
            "retry_question": "Hindi pa! Kailangan nating gumawa ng mas malalim na hilera para sa Okra na may malalim na ugat.",
            "choices": [
                {"img": "buttons/choice_hoe.png",    "label": "Asarol"},
                {"img": "buttons/choice_trowel.png", "label": "Dulo"},
            ],
            "correct": 0,
        },
        {
            "id":          "S2P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Ang Asarol ang perpekto para gumawa ng maayos na hilera sa mainit na lupa para sa Okra. Maganda ang ginawa mo!"),
            ],
        },
        {
            "id":          "S2P3_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef_thumbs": "right"},
            "lines": [
                ("chef_thumbs", "Puwede! Akala ko wala na ako sa ganito... pero parang may lumalabas na sa aking memorya. Tama ang Asarol!"),
            ],
        },
        {
            "id":               "S2P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Hmm... ang Dulo ay para sa maliliit na butas, hindi para sa mahahabang hilera ng Okra. Subukan muli."),
            ],
        },

        # ── Panel 3 — Water scan: deep roots ──────────────────
        {
            "id":      "S3P1",
            "type":    "dialogue",
            "day":     2,
            "bg":      "background/scenebg_planter.png",
            "chars":   {"chef": "right"},
            "lines": [
                ("chef", "Malalim ang ugat ng Okra, sabi mo. Kailangan din bang malalim ang dilig para sundan nila pababa?"),
            ],
        },
        {
            "id":       "S3P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-01 Water Card",
            "dialogue": "Tama ka, Chef! Bigyan natin sila ng sapat na tubig — hindi paunti-unti para sumunod ang ugat pababa.",
            "question": "Scan the Water Card to encourage the Okra roots to dig deep into the soil.",
        },

        # ── Day 40 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day40_fade",
            "type": "transition",
        },

        # ── Panel 4 — Observe: don't pick the flower ──────────
        {
            "id":    "S4P1",
            "type":  "dialogue",
            "day":   40,
            "bg":    "background/scenebg_planter.png",
            "chars": {"baron": "right"},
            "dark":  True,
            "lines": [
                ("baron", "Pitasin ang bulaklak! Gagawin nating dekorasyon sa aking ulap-palasyo! Mas maganda roon kaysa sa boring na taniman ninyo!"),
            ],
        },
        {
            "id":    "S4P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Huwag! Pakiramdam ko... kung pipitasin natin iyan, mawawala ang... ang..."),
            ],
        },
        {
            "id":            "S4P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Ano ang mangyayari kung pipitasin ang bulaklak ng Okra?",
            "retry_question": "Mag-isip muli! Saan galing ang bunga ng Okra — mula sa bulaklak ba o sa ibang parte ng halaman?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Hindi tutubuin ang Okra pod"},
                {"img": "buttons/choice_hoe.png",    "label": "Tutubo pa rin agad"},
            ],
            "correct": 0,
        },
        {
            "id":          "S4P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Kung pipitasin ang bulaklak, walang magiging Okra pod sa lugar na iyon. Hayaan nating malaglag ang petals nang natural."),
            ],
        },
        {
            "id":               "S4P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Huwag maniwala kay Baron! Ang bulaklak ang pinagmumulan ng Okra pod. Pag nawala, wala ring bunga."),
            ],
        },

        # ── Day 45 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day45_fade",
            "type": "transition",
        },

        # ── Panel 5 — Water scan: support growing pod ─────────
        {
            "id":      "S5P1",
            "type":    "dialogue",
            "day":     45,
            "bg":      "background/scenebg_planter.png",
            "chars":   {"lucas": "left"},
            "lines": [
                ("lucas", "Tingnan mo, Chef — lumalaki na nang mabilis ang Okra pod. Kailangan niya ng tubig para manatiling malusog."),
            ],
        },
        {
            "id":       "S5P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"chef": "right"},
            "active":   "chef",
            "card":     "AC-01 Water Card",
            "dialogue": "Okay, I-scan na natin ang Water Card para suportahan ang mabilis na paglaki ng Okra pod.",
            "question": "Scan the Water Card to support this fast-growing Okra pod.",
        },

        # ── Panel 6 — Trivia: farming takes patience ──────────
        {
            "id":    "S6P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Bagal! Dapat malaki na 'yan kahapon! Magpalaki ng Okra sa isang gabi, ganun lang 'yan!"),
            ],
        },
        {
            "id":    "S6P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Naku, Lucas... totoo kaya 'yon? Puwede bang lumaki ang halaman sa isang gabi?"),
            ],
        },
        {
            "id":            "S6P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Totoo ba na maaaring lumaki nang buo ang halaman sa loob ng isang gabi?",
            "retry_question": "Isipin muli — may narinig ka bang halaman na lumaki nang ganun kabilis?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Mali — kailangan ng panahon"},
                {"img": "buttons/choice_hoe.png",    "label": "Totoo — isang gabi lang"},
            ],
            "correct": 0,
        },
        {
            "id":          "S6P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Walang minamadaling kalikasan. Magsasaka at kusinero, pareho silang may pinaka-importanteng katangian — pasensya!"),
            ],
        },
        {
            "id":               "S6P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Huwag pakinggan si Baron! Walang halaman ang lumalaki sa isang gabi. Kailangan ng tamang pag-aalaga at pasensya."),
            ],
        },

        # ── Day 55 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day55_fade",
            "type": "transition",
        },

        # ── Panel 7 — Harvest scan (AC-05) ───────────────────
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   55,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Ayoko ng matigas at makahoy — gusto ko 'yong malutong pa, bata pa para sa Sinigang."),
            ],
        },
        {
            "id":            "S7P2_choice",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":      "Alin ang tamang Okra para sa Sinigang ng Chef?",
            "retry_question": "Isipin muli! Ang tamang Okra ay bata pa, makinang na berde, at malutong na snap — hindi malaki at makahoy.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Makinang na berde, 8cm, malutong na snap"},
                {"img": "buttons/choice_hoe.png",    "label": "Malaki, matigas, makahoy na pod"},
            ],
            "correct": 0,
        },
        {
            "id":          "S7P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef_thumbs": "right"},
            "lines": [
                ("chef_thumbs", "Iyan nga! Bata pa, malutong pa, at makinang na berde — perpekto para sa aking Sinigang!"),
            ],
        },
        {
            "id":               "S7P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Ang malaki at matigas na Okra ay makahoy na — hindi masarap iyon sa Sinigang. Hanapin ang bata at malutong pa!"),
            ],
        },
        {
            "id":       "S7P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-05 Harvest Card",
            "dialogue": "Napili mo na ang tamang Okra! I-scan ang Harvest Card para ma-confirm ang pag-aani para sa Sinigang!",
            "question": "Scan the Harvest Card to confirm the bright green, 8cm, easily-snapping Okra ready for Chef's Sinigang.",
        },

        # ── Panel 8 — End: Sinigang na Baboy memory ───────────
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   55,
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "SINIGANG! Sinigang na baboy may Okra, may sampalok... ang asim, ang lambot ng gulay... bumalik na sa dila ko ang lasa!"),
            ],
        },
        {
            "id":    "S8P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Tatlong pinto na ang nabuksan, Chef. At sa tuwing nakukuha mo ang lasa, parang may kasunod pang gusto mong matuklasan."),
                ("lucas", "Sinigang na Baboy Memory — UNLOCKED!"),
            ],
        },

    ],
}
