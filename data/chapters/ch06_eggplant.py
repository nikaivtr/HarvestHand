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
            "logo": "logos/ch1logo.png",
        },

        # ── Panel 1 — Kapitan lost his purpose ────────────────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Lucas... bakit ba mahalaga ang barangay hall? Nakalimutan ko pati kung para saan ako naging Kapitan ng baryong ito."),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Doon tayo nagtitipon, Kapitan — kumakain, nagpaplano, naghihilom. Tandaan natin ito gamit ang Talong. Sundan mo ako."),
            ],
        },

        # ── Panel 2 — Trivia: hardening off ───────────────────
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Parang training ng sundalo — kailangan sanay muna sa labas bago tuluyang dalhin sa parada. Ganyan din ang halaman?"),
            ],
        },
        {
            "id":            "S2P2",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Totoo ba na ang dahan-dahanang pagsanay ng seedlings sa araw ay nagpipigil ng transplant shock?",
            "retry_question": "Isipin muli! Ano ang mangyayari kapag biglang ilantad ang seedlings sa matinding araw mula sa malamig na silid?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Totoo — unti-unting sanay"},
                {"img": "buttons/choice_hoe.png",    "label": "Mali — diretso sa araw"},
            ],
            "correct": 0,
        },
        {
            "id":          "S2P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Ang 'hardening off' ay dahan-dahanang pagsanay ng seedlings sa labas — tulad ng training ng sundalo bago lumaban!"),
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
                ("lucas_wrong", "Kung biglang ilantad ang seedlings sa matinding sikat, malalanta sila. Unti-unting pagsanay ang tamang paraan."),
            ],
        },

        # ── Day 21 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day21_fade",
            "type": "transition",
        },

        # ── Panel 3 — Tool: Dulo for deep holes ───────────────
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "day":   21,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Mabigat na ang Talong kapag lumaki, Kapitan — kaya malalim ang butas na kailangan para hindi matumba."),
            ],
        },
        {
            "id":            "S3P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Alin ang tamang kagamitan para humukay ng malalim at matatag na butas para sa Talong seedlings?",
            "retry_question": "Isipin muli! Kailangan ng kagamitang angkop sa pagpasok ng malalim na butas para sa malaking Talong.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Dulo — malalim at tumpak"},
                {"img": "buttons/choice_hoe.png",    "label": "Kalaykay — para sa ibabaw lang"},
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
                ("lucas_thumbs", "Tama! Ang Dulo ang perpekto para humukay ng malalim at matatag na butas na tatanggap sa malaking Talong."),
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
                ("lucas_wrong", "Ang Kalaykay ay para sa pag-aayos ng ibabaw ng lupa, hindi para sa malalim na paghuhukay. Subukan ang ibang kagamitan."),
            ],
        },

        # ── Panel 4 — Water scan: settle roots ────────────────
        {
            "id":       "S4P1",
            "type":     "scan",
            "day":      21,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"kapitan": "right"},
            "active":   "kapitan",
            "card":     "AC-01 Water Card",
            "dialogue": "Kapitan: Diligin agad pagkatapos ilipat, di ba? Para mawala ang hanging nakulong sa ilalim at masigurado ang ugat.",
            "question": "Scan the Water Card to settle the soil around the newly transplanted eggplants.",
        },

        # ── Day 30 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day30_fade",
            "type": "transition",
        },

        # ── Panel 5 — Earthworms: vermicast ───────────────────
        {
            "id":    "S5P1",
            "type":  "dialogue",
            "day":   30,
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Lucas! May mga bulate na gumagalaw sa lupa! Nandidiri ako — alisin natin sila?"),
            ],
        },
        {
            "id":    "S5P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Huwag, Kapitan! Sila ang lihim na gumagawa ng pinakamagandang pataba dito. Ano ang tinatawag na produkto ng mga bulate?"),
            ],
        },
        {
            "id":            "S5P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Ano ang ginagawa ng mga bulate (earthworms) para sa lupa ng ating taniman?",
            "retry_question": "Isipin muli! Ang mga bulate ay nagpapabunga ng lupa — sino ang nakikinabang sa kanilang trabaho?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Gumagawa ng vermicast na pataba"},
                {"img": "buttons/choice_hoe.png",    "label": "Sinasamantala lang ang lupa"},
            ],
            "correct": 0,
        },
        {
            "id":          "S5P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Ang vermicast — dumi ng bulate — ay parang ginto para sa lupa. Pinakamakapangyarihang organic na pataba!"),
            ],
        },
        {
            "id":               "S5P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Mali! Ang mga bulate ang pinaka-masipag na manggagawa ng lupa. Ginagawa nila ang pinakamayamang pataba — vermicast."),
            ],
        },

        # ── Day 35 transition ─────────────────────────────────
        {
            "id":   "day35_fade",
            "type": "transition",
        },

        # ── Panel 6 — Fertilizer choice: Organic vs Chemical ──
        {
            "id":    "S6P1",
            "type":  "dialogue",
            "day":   35,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Oras na para pakainin ang lupa malapit sa ugat ng Talong, Kapitan — alin ang pipiliin natin?"),
            ],
        },
        {
            "id":       "S6P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-02 Fertilizer Card",
            "dialogue": "I-scan ang Fertilizer Card para piliin ang tamang pataba para sa malusog na lupa ng Talong!",
            "question": "Scan the Fertilizer Card to choose the organic fertilizer for healthy eggplant soil.",
        },

        # ── Day 40 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day40_fade",
            "type": "transition",
        },

        # ── Panel 7 — Mulching ────────────────────────────────
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   40,
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Lucas, mabilis na natutuyo ang lupa sa init ng araw. Kailangan ba nating lagyan ng dayami sa ibabaw?"),
            ],
        },
        {
            "id":            "S7P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Bakit mahalaga ang mulch (dayami o dahon) sa paligid ng halaman?",
            "retry_question": "Isipin muli! Ano ang nagagawa ng mulch para sa lupa tuwing malakas ang araw?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Nagpapanatili ng halumigmig — kontra-damo"},
                {"img": "buttons/choice_hoe.png",    "label": "Para magmukhang maayos lang"},
            ],
            "correct": 0,
        },
        {
            "id":          "S7P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Ang mulch ay parang kumot ng halaman — nagpapanatili ng halumigmig sa lupa at pumipigil sa paglaki ng damo!"),
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
                ("lucas_wrong", "Hindi puro aesthetics ang mulch! Mahalaga ito para mapanatili ang tubig sa lupa at hadangan ang mga ligaw na damo."),
            ],
        },

        # ── Day 50 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day50_fade",
            "type": "transition",
        },

        # ── Panel 8 — Weeding around base ─────────────────────
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   50,
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Dahan-dahan nating alisin ang damo sa paanan ng Talong, Lucas — ayoko masugatan pa ang punong ito."),
            ],
        },
        {
            "id":            "S8P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Alin ang tamang kagamitan para maingat na bunutin ang damo sa paligid ng tangkay ng Talong?",
            "retry_question": "Isipin muli! Malapit tayo sa tangkay — kailangan ng kagamitang tumpak at hindi lalabas sa hangganan ng halaman.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Dulo — tumpak sa maliit na lugar"},
                {"img": "buttons/choice_hoe.png",    "label": "Asarol — malawak na hukay"},
            ],
            "correct": 0,
        },
        {
            "id":          "S8P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Ang Dulo ang tamang kagamitan para maingat na bunutin ang damo malapit sa tangkay nang hindi nasasira ang halaman."),
            ],
        },
        {
            "id":               "S8P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Ang Asarol ay masyadong malawak — maaaring masugatan ang tangkay ng Talong. Gamitin ang mas tumpak na kagamitan."),
            ],
        },

        # ── Day 60 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day60_fade",
            "type": "transition",
        },

        # ── Panel 9 — Pesticide choice: Natural vs Chemical ───
        {
            "id":    "S9P1",
            "type":  "dialogue",
            "day":   60,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Shoot borers, Kapitan! Kailangan agad ng aksyon — pero mag-ingat tayo sa pipiliin, baka pati kapaki-pakinabang na insekto ay masaktan!"),
            ],
        },
        {
            "id":       "S9P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-04 Pesticide Card",
            "dialogue": "I-scan ang Pesticide Card para piliin ang tamang pestisidyo laban sa shoot borers na hindi makakasama sa kalikasan!",
            "question": "Scan the Pesticide Card to choose the natural pesticide against eggplant shoot borers.",
        },

        # ── Day 80 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day80_fade",
            "type": "transition",
        },

        # ── Panel 10 — Harvest scan ───────────────────────────
        {
            "id":    "S10P1",
            "type":  "dialogue",
            "day":   80,
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Kapag makinang, mahaba, at matingkad na lila — iyon ang pinakamainam para sa inihaw na Talong!"),
            ],
        },
        {
            "id":            "S10P2_choice",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":      "Alin ang tamang Talong para sa inihaw na Talong ng Kapitan?",
            "retry_question": "Isipin muli! Ang tamang Talong ay makinang, matigas, at malalim na lila — hindi maputla o malambot.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Makinis, makinang na lila, mahaba at matigas"},
                {"img": "buttons/choice_hoe.png",    "label": "Maputla na, malambot, may mga bitak"},
            ],
            "correct": 0,
        },
        {
            "id":          "S10P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": "right"},
            "lines": [
                ("kapitan", "Iyan ang hinahanap ko! Makinang, matigas, malalim na lila — perpekto para sa inihaw na Talong!"),
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
                ("lucas_wrong", "Hindi — ang maputla at malambot na Talong ay sobrang lutog na. Hanapin ang makinang at matigas pa!"),
            ],
        },
        {
            "id":       "S10P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-05 Harvest Card",
            "dialogue": "Napili mo na ang tamang Talong! I-scan ang Harvest Card para ma-confirm ang pag-aani!",
            "question": "Scan the Harvest Card to confirm the smooth, shiny deep-purple eggplant is ready to harvest.",
        },

        # ── Panel 11 — End: Kare-Kare memory ──────────────────
        {
            "id":    "S11P1",
            "type":  "dialogue",
            "day":   80,
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "KARE-KARE! May talong, may karne, may mani — at lahat ng tao, nagtitipon sa barangay hall para sabay kumain. Ito ang dahilan kung bakit ako Kapitan — para mapasama silang lahat!"),
            ],
        },
        {
            "id":    "S11P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Anim na pinto na, Kapitan. Tunay nang bumabalik ang iyong tungkulin — at ang baryo ay mas malusog na ngayon."),
                ("lucas", "Kare-Kare Memory — UNLOCKED!"),
            ],
        },

    ],
}
