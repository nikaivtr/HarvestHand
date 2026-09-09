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
            "logo": "logos/ch1logo.png",
        },

        # ── Panel 1 — Lola Maria's faint memory of sourness ───
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "May hinahanap ang dila ko, apo... mapula, may kaasiman. Hindi ko hawak ito sa isip."),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Kamatis, Lola! Pero hindi tayo tuwirang magtatanim. Gagawa muna tayo ng maliit na silungan para protektado ang mga seedlings habang bata pa sila."),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Silungan? Ang mga halaman ay para sa bukid! Direkta nang itanim sa labas — patayin ko sila sa matinding panahon! HAHAHA!"),
            ],
        },

        # ── Panel 2 — Trivia: indirect planting ───────────────
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Bakit kailangan munang sa maliit na lalagyan, hindi diretso sa bukid, apo?"),
            ],
        },
        {
            "id":            "S2P2",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Totoo ba na ang indirect planting ay nagpoprotekta sa mahina pang seedlings?",
            "retry_question": "Isipin muli! Ano ang maaaring mangyari sa napakabatang halaman na diretso ilantad sa malakas na panahon?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Totoo — protektado sila"},
                {"img": "buttons/choice_hoe.png",    "label": "Mali — diretso sa bukid"},
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
                ("lola_thumbs", "Tama! Ang indirect planting ay nagbibigay ng proteksyon sa mahina pang seedlings. Tulad ng isang bata bago pumasok sa malaking paaralan."),
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
                ("lucas_wrong", "Huwag pakinggan si Baron! Ang direktang pagtatanim ay maaaring mamatay ang mga maliliit na seedlings sa matinding panahon."),
            ],
        },

        # ── Day 14 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day14_fade",
            "type": "transition",
        },

        # ── Panel 3 — Tool: Dulo for transplanting ────────────
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "day":   14,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Handa na ang mga seedlings para ilipat, Lola. Sandukhin natin nang buo — kasama ang lupa at ugat, hindi puro tangkay."),
            ],
        },
        {
            "id":            "S3P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Alin ang tamang kagamitan para maingat na sandukhin ang Kamatis seedlings kasama ang ugat?",
            "retry_question": "Isipin muli! Kailangan ng kagamitang tumpak para hindi masira ang maliliit na ugat ng seedlings.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Dulo — maingat at tumpak"},
                {"img": "buttons/choice_hoe.png",    "label": "Asarol — malawak ang hukay"},
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
                ("lucas_thumbs", "Tama! Ang Dulo ang pinaka-angkop para maingat na sandukhin ang bawat seedlings kasama ang lupa at ugat nito."),
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
                ("lucas_wrong", "Ang Asarol ay masyadong malawak at maaaring masira ang mga maliliit na ugat ng Kamatis seedlings. Gamitin ang mas maingat na kagamitan."),
            ],
        },

        # ── Panel 4 — Companion: marigolds ────────────────────
        {
            "id":    "S4P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Sa tabi ng Kamatis, magtanim din tayo ng bulaklak — natatandaan ko, may pakinabang ito laban sa mga peste."),
            ],
        },
        {
            "id":            "S4P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Anong bulaklak ang natural na nagtataboy ng mga insekto sa paligid ng Kamatis?",
            "retry_question": "Isipin muli! Anong bulaklak ang may malakas na amog na kinakatakutan ng mga kulisap?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Marigold — natural na pangontra"},
                {"img": "buttons/choice_hoe.png",    "label": "Plastik na bulaklak"},
            ],
            "correct": 0,
        },
        {
            "id":          "S4P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Tama! Ang amoy ng Marigold ang nagtataboy sa mga kulisap — natural na depensa, hindi kailangan ng kemikal na lason."),
            ],
        },
        {
            "id":               "S4P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Ang plastik na bulaklak ay walang amoy at walang buhay — hindi nito matatakot ang mga insekto. Kailangan ng tunay!"),
            ],
        },

        # ── Panel 5 — Water scan: roots only ──────────────────
        {
            "id":       "S5P1",
            "type":     "scan",
            "day":      15,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-01 Water Card",
            "dialogue": "Sa lupa lang ang dilig, Lola — kung mababasa ang mga dahon ng Kamatis, mabilis itong magkasakit. I-scan ang Water Card.",
            "question": "Scan the Water Card to water the soil at the base only, keeping the tomato leaves dry.",
        },

        # ── Day 35 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day35_fade",
            "type": "transition",
        },

        # ── Panel 6 — Staking ─────────────────────────────────
        {
            "id":    "S6P1",
            "type":  "dialogue",
            "day":   35,
            "bg":    "background/scenebg_planter.png",
            "chars": {"baron": "right"},
            "dark":  True,
            "lines": [
                ("baron", "Hayaan mo lang silang gumapang sa putik at mabulok! Mas masaya para sa akin na makita silang natumba!"),
            ],
        },
        {
            "id":    "S6P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Hindi, apo! Kailangan nating itali ang mga tanim sa kawayan — ginawa namin ito sa hardin ng iyong Lolo noon."),
            ],
        },
        {
            "id":            "S6P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Ano ang dapat gawin sa mga Kamatis na nahihilig na sa bigat ng bunga?",
            "retry_question": "Isipin muli! Ano ang mangyayari sa bunga ng Kamatis kung pahihintulutan itong gumapang sa lupa?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Itali sa trellis — ligtas"},
                {"img": "buttons/choice_hoe.png",    "label": "Hayaang gumapang sa lupa"},
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
                ("lucas_thumbs", "Tama! Ang trellising ay nagpapanatiling malinis ang bunga at umiiwas sa pagkabulok. Nagpapalakas din ito ng daloy ng hangin sa pagitan ng dahon."),
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
                ("lucas_wrong", "Huwag pakinggan si Baron! Kapag gumapang ang bunga sa lupa, mabilis itong mabulok at masisira."),
            ],
        },

        # ── Day 45 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day45_fade",
            "type": "transition",
        },

        # ── Panel 7 — Weed method: careful vs careless ────────
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   45,
            "bg":    "background/scenebg_planter.png",
            "chars": {"baron": "right"},
            "dark":  True,
            "lines": [
                ("baron", "Bunutin lahat ng damo nang sabay-sabay! Mas mabilis — huwag nang mag-ingat sa mga tangkay ng Kamatis!"),
            ],
        },
        {
            "id":    "S7P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Mag-ingat, apo — ang mga ugat ng Kamatis ay malapit sa ibabaw ng lupa. Paano tayo mag-aalis ng damo nang hindi nasasira ang halaman?"),
            ],
        },
        {
            "id":       "S7P3",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-03 Weed Removal Card",
            "dialogue": "I-scan ang Weed Removal Card para alamin ang tamang paraan ng pag-aalis ng damo sa paligid ng mga Kamatis!",
            "question": "Scan the Weed Removal Card to learn the careful weeding technique that protects tomato roots.",
        },

        # ── Day 50 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day50_fade",
            "type": "transition",
        },

        # ── Panel 8 — Fertilizer choice: Organic vs Chemical ──
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   50,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Oras na para pakainin ang lupa, Lola — ang mga Kamatis ay nagbubunga na. Alin ang pipiliin natin para maging masustansya ang bunga?"),
            ],
        },
        {
            "id":       "S8P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-02 Fertilizer Card",
            "dialogue": "I-scan ang Fertilizer Card para piliin ang tamang pataba para sa malusog na lupa ng Kamatis!",
            "question": "Scan the Fertilizer Card to choose the organic fertilizer for healthy tomato soil.",
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
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Fruit flies! Ang aking mga langaw ay nagbubutas na sa inyong mga Kamatis — wala kayong magagawa!"),
            ],
        },
        {
            "id":    "S9P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Fruit flies, Lola! Kailangan agad ng aksyon — pero mag-ingat tayo sa pipiliin, baka pati kapaki-pakinabang na insekto ay masaktan!"),
            ],
        },
        {
            "id":       "S9P3",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-04 Pesticide Card",
            "dialogue": "I-scan ang Pesticide Card para piliin ang tamang pestisidyo laban sa fruit flies na ligtas sa kalikasan!",
            "question": "Scan the Pesticide Card to choose the natural pesticide against fruit flies.",
        },

        # ── Day 75 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day75_fade",
            "type": "transition",
        },

        # ── Panel 10 — Harvest scan ───────────────────────────
        {
            "id":    "S10P1",
            "type":  "dialogue",
            "day":   75,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Huwag sobrang lambot, apo — mapula at makintab ang pinakamasarap na Kamatis para sa ating ulam."),
            ],
        },
        {
            "id":            "S10P2_choice",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":      "Alin ang tamang Kamatis para sa Sarciado ni Lola?",
            "retry_question": "Isipin muli! Ang tamang Kamatis ay mapula, makintab, at bahagyang matigas — hindi berde o masyadong malambot.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Mapula, makintab, bahagyang matigas"},
                {"img": "buttons/choice_hoe.png",    "label": "Berde pa, o sobrang lambot at may bitak"},
            ],
            "correct": 0,
        },
        {
            "id":          "S10P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Tama! Mapula at makintab — iyon ang tamang Kamatis para sa ating Sarciado!"),
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
                ("lucas_wrong", "Hindi pa handa iyan! Kailangan pang pumula at tumigas ng bahagya ang Kamatis bago anihin."),
            ],
        },
        {
            "id":       "S10P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-05 Harvest Card",
            "dialogue": "Napili mo na ang tamang Kamatis! I-scan ang Harvest Card para ma-confirm ang pag-aani!",
            "question": "Scan the Harvest Card to confirm the bright red, shiny, slightly firm tomato is ready to pick.",
        },

        # ── Panel 11 — End: Sarciado memory ───────────────────
        {
            "id":    "S11P1",
            "type":  "dialogue",
            "day":   75,
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Kamatis, itlog, bawang... SARCIADO! Niluluto ko ito tuwing Linggo para sa iyong Lolo bago siya umalis papuntang bukid!"),
            ],
        },
        {
            "id":    "S11P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Kalahati na tayo, Lola! Lima nang alaala ang ating hawak. Tatlong recipe pa ang naghihintay sa atin."),
                ("lucas", "Kamatis Sarciado Memory — UNLOCKED!"),
            ],
        },

    ],
}
