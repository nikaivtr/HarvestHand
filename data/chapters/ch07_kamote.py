# ============================================================
#  CHAPTER 7 — KAMOTE (Sweet Potato)
#  Intermediate | 11 story panels | Total growing days: 120
#  Characters: Lucas, Chef Pablo, Lola Maria, Blight Baron
#  MECHANICS: Vine cuttings, drought tolerance, ash fertilizer
# ============================================================

CHAPTER = {
    "id":         "ch07",
    "crop":       "Kamote",
    "level":      "intermediate",
    "memory":     "Kamote Cue Memory",
    "total_days": 120,

    "slides": [

        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "logos/ch1logo.png",
        },

        # ── Panel 1 — Underground treasure ────────────────────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "May meryenda noon na sobrang gusto ng mga bata sa Pista, pero hindi ko matandaan kung ano. May mainit, may tamis..."),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Nasa ilalim ng lupa ang sagot mo, Pablo. Naaalala ko iyon — Kamote!"),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Tama, Lola! At sa pagkakataong ito, hindi tayo magtatanim ng buto. Gagamit tayo ng baging — vine cuttings — para mas mabilis mamunga."),
            ],
        },

        # ── Panel 2 — Trivia: vine cuttings need planting now ─
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Ang Kamote ay hindi nagsisimula sa buto, kundi sa pinutol na baging? Kailangan ba itong itanim agad?"),
            ],
        },
        {
            "id":            "S2P2",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Totoo ba na ang vine cuttings ay kailangang itanim agad bago matuyo para mas mabilis mag-ugat?",
            "retry_question": "Isipin muli! Ano ang mangyayari sa isang pinutol na baging kapag natuyo na bago pa itanim?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Totoo — itanim agad habang sariwa"},
                {"img": "buttons/choice_hoe.png",    "label": "Mali — itago muna nang matagal"},
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
                ("lucas_thumbs", "Tama! Mas mabilis mag-ugat ang sariwang vine cuttings kaysa sa natuyo na. Itanim agad para siguradong mabubuhay!"),
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
                ("lucas_wrong", "Hindi! Kapag natuyo na ang baging bago itanim, hindi na siya mabubuhay. Itanim habang sariwa pa!"),
            ],
        },

        # ── Day 1 transition ───────────────────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },

        # ── Panel 3 — Tool: Asarol for planting ridges ────────
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Itatanim natin ang baging patagilid, 45-degrees, sa ibabaw ng matataas na bunton ng lupa?"),
            ],
        },
        {
            "id":    "S3P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Eksakto, Chef — at para sa mataas na bunton na iyon, kailangan natin ng tamang kagamitan."),
            ],
        },
        {
            "id":            "S3P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Alin ang tamang kagamitan para gumawa ng mataas na bunton ng lupa para sa Kamote?",
            "retry_question": "Isipin muli! Kailangan nating gumawa ng mataas, maayos na bunton — hindi maliit na butas.",
            "choices": [
                {"img": "buttons/choice_hoe.png",    "label": "Asarol — para sa mataas na bunton"},
                {"img": "buttons/choice_trowel.png", "label": "Gunting — para sa paggupit"},
            ],
            "correct": 0,
        },
        {
            "id":          "S3P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Ang Asarol ang perpektong kagamitan para bumuo ng mataas na bunton ng lupa para sa Kamote."),
            ],
        },
        {
            "id":               "S3P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Ang Gunting ay para sa paggupit ng dahon o baging — hindi para gumawa ng bunton ng lupa."),
            ],
        },

        # ── Panel 4 — Water scan: help vines root ─────────────
        {
            "id":       "S4P1",
            "type":     "scan",
            "day":      1,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lola": "left"},
            "active":   "lola",
            "card":     "AC-01 Water Card",
            "dialogue": "Lola: Diligin agad, apo, para mabuhay ang mga bagong-putol na baging at magsimulang mag-ugat sila.",
            "question": "Scan the Water Card to help the newly planted vine cuttings form roots in the soil.",
        },

        # ── Day 40 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day40_fade",
            "type": "transition",
        },

        # ── Panel 5 — Drought defense ─────────────────────────
        {
            "id":    "S5P1",
            "type":  "dialogue",
            "day":   40,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Matutuyo ang inyong Kamote! Walang ulan ang darating, walang pag-asa! Ibaha sila ngayon na sa tubig!"),
            ],
        },
        {
            "id":    "S5P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Lucas... kailangan ba nating ibuhos ng tubig agad? Ilang linggong walang ulan na!"),
            ],
        },
        {
            "id":            "S5P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Dapat bang i-flood ang bukid ng Kamote tuwing magtatagtuyot?",
            "retry_question": "Isipin muli! Ang Kamote ay kilala sa kakayahang mabuhay sa tagtuyot — bakit kaya?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Hindi — sanay sa tagtuyot ang Kamote"},
                {"img": "buttons/choice_hoe.png",    "label": "Oo — ibaha agad sa tubig"},
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
                ("lucas_thumbs", "Tama! Sa overwatering, mabubulok ang ugat ng Kamote. Sanay siya sa tagtuyot — haayaan nating lumago ang ugat pababa!"),
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
                ("lucas_wrong", "Huwag maniwala kay Baron! Ang sobrang tubig ang kaaway ng Kamote. Hayaan mo siyang humukay nang mas malalim para sa tubig."),
            ],
        },

        # ── Day 50 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day50_fade",
            "type": "transition",
        },

        # ── Panel 6 — Ash fertilizer ──────────────────────────
        {
            "id":    "S6P1",
            "type":  "dialogue",
            "day":   50,
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Huwag mong itapon ang malamig na abo, Pablo — gusto ito ng Kamote. Naaalala ko kung bakit."),
            ],
        },
        {
            "id":            "S6P2",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Bakit ang malamig na abo ng kahoy ay mabuti para sa root crops tulad ng Kamote?",
            "retry_question": "Isipin muli! Anong sustansya ang nakatutulong para lumaki ang ubod o tuber sa ilalim?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "May Potassium — nagpapalaki ng ubod"},
                {"img": "buttons/choice_hoe.png",    "label": "Para magmukhang puti lang ang lupa"},
            ],
            "correct": 0,
        },
        {
            "id":          "S6P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Tama! Ang abo ay mayaman sa Potassium — ang siyang nagpapalaki ng ubod ng Kamote sa ilalim ng lupa. Sikreto ng lola mo iyan!"),
            ],
        },
        {
            "id":               "S6P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Hindi aesthetics ang dahilan! Ang abo ay puno ng Potassium na nagpapalaki ng ubod ng Kamote sa ilalim ng lupa."),
            ],
        },

        # ── Day 55 transition ─────────────────────────────────
        {
            "id":   "day55_fade",
            "type": "transition",
        },

        # ── Panel 7 — Fertilizer choice: Organic vs Chemical ──
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   55,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Oras na para pakainin ulit ang lupa, Chef — hindi sa ugat mismo, sa gilid lang. Alin ang gagamitin natin?"),
            ],
        },
        {
            "id":       "S7P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-02 Fertilizer Card",
            "dialogue": "I-scan ang Fertilizer Card para piliin ang tamang pataba para sa malusog na lupa ng Kamote!",
            "question": "Scan the Fertilizer Card to choose the organic fertilizer for healthy sweet potato soil.",
        },

        # ── Day 70 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day70_fade",
            "type": "transition",
        },

        # ── Panel 8 — Weed removal scan: between vines (AC-03) ─
        {
            "id":       "S8P1",
            "type":     "scan",
            "day":      70,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-03 Weed Removal Card",
            "dialogue": "Napakaraming damo na humalo sa mga baging! I-scan ang Weed Removal Card para maingat na alisin ang damo nang hindi nasasira ang mga baging ng Kamote.",
            "question": "Scan the Weed Removal Card to carefully clear the weeds tangled through the sweet potato vines.",
        },

        # ── Day 100 transition (TIME SKIP) ────────────────────
        {
            "id":   "day100_fade",
            "type": "transition",
        },

        # ── Panel 9 — Trivia: cracking soil signals ready tuber
        {
            "id":    "S9P1",
            "type":  "dialogue",
            "day":   100,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Bumubuka ang lupa sa paligid ng mga halaman! Nanlilindol ba?!"),
            ],
        },
        {
            "id":    "S9P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Hindi, Chef — kalmado lang! Ito ang pinakamabuting senyales na puwede mong makita sa taniman ng Kamote."),
            ],
        },
        {
            "id":            "S9P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Totoo ba na ang bumibukang lupa sa paligid ng Kamote ay senyales na malaki na ang tuber sa ilalim?",
            "retry_question": "Isipin muli! Ano ang nagdudulot ng pagbuka ng lupa sa paligid ng halaman ng Kamote?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Totoo — itutulak palabas ng malaking tuber"},
                {"img": "buttons/choice_hoe.png",    "label": "Mali — senyales ng sakit ang pagbuka"},
            ],
            "correct": 0,
        },
        {
            "id":          "S9P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Itinutulak palabas ng lumalaking ubod ang lupa mismo — pagbubukas ng lupa ay senyales ng magandang ani!"),
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
                ("lucas_wrong", "Hindi senyales ng sakit! Ang bumibukang lupa ay ibig sabihin, napakalaki na ng ubod at itutulak niya palabas ang lupa!"),
            ],
        },

        # ── Day 120 transition (TIME SKIP) ────────────────────
        {
            "id":   "day120_fade",
            "type": "transition",
        },

        # ── Panel 10 — Harvest scan ───────────────────────────
        {
            "id":    "S10P1",
            "type":  "dialogue",
            "day":   120,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Pag nanilaw na ang dahon sa ibaba at bumuka nang husto ang lupa — oras na, Pablo. Kalugin natin ang taniman!"),
            ],
        },
        {
            "id":            "S10P2_choice",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":      "Alin ang senyales na handa na ang Kamote para anihin?",
            "retry_question": "Isipin muli! Ang handa nang Kamote ay may nanilaw na dahon sa ibaba at bumibukang lupa — hindi lahat berde at tahimik ang lupa.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Nanilaw na dahon sa ibaba, bumibukang lupa"},
                {"img": "buttons/choice_hoe.png",    "label": "Berde pa lahat ng dahon, walang galaw ang lupa"},
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
                ("lola_thumbs", "Tama! Ang nanilaw na dahon at bumibukang lupa — senyales ng malaking tuber na naghihintay sa ilalim!"),
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
                ("lucas_wrong", "Hindi pa — kailangan pang lumaki ang tuber sa ilalim. Hintayin ang nanilaw na dahon at bumibukang lupa!"),
            ],
        },
        {
            "id":       "S10P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-05 Harvest Card",
            "dialogue": "Napili mo na ang tamang senyales! I-scan ang Harvest Card para ma-confirm ang pag-aani ng Kamote!",
            "question": "Scan the Harvest Card to confirm the yellowing base leaves and cracking soil signal a ready harvest.",
        },

        # ── Panel 11 — End: Kamote Cue memory ─────────────────
        {
            "id":    "S11P1",
            "type":  "dialogue",
            "day":   120,
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "KAMOTE CUE! Ito! Ang meryenda na hinahanap-hanap ng mga bata sa Pista, nasa mainit na asukal! Naalala ko na!"),
            ],
        },
        {
            "id":    "S11P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "PITONG ALAALA?! HINDI! Isang crop na lang sila! Isa na lang bago maging sampung alaala!"),
            ],
        },
        {
            "id":    "S11P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Tatlong pinto na lang, Chef. Papasok na tayo sa pinakamahirap na yugto — handa ka na?"),
                ("lucas", "Kamote Cue Memory — UNLOCKED!"),
            ],
        },

    ],
}
