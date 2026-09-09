# ============================================================
#  CHAPTER 4 — SQUASH (Kalabasa)
#  Intermediate | 11 story panels | Total growing days: 90
#  Characters: Lucas, Chef Pablo, Lola Maria, Blight Baron
#  NEW MECHANICS: Compost, Weeds, Pests
# ============================================================

CHAPTER = {
    "id":         "ch04",
    "crop":       "Squash",
    "level":      "intermediate",
    "memory":     "Ginataang Kalabasa Memory",
    "total_days": 90,

    "slides": [

        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "logos/ch1logo.png",    # placeholder — replace with ch4 logo
        },

        # ── Panel 1 — Baron escalates with weeds and pests ────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Akala n'yo tapos na ako? Mula sa aking tirahan sa ulap, may dalawang bagong kasama na ako — DAMO at INSEKTO! Pakikipagaway pa rin kayo sa kalikasan ngayon!"),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Lucas, hiniling sa akin ni Lola Maria ang isang matamis na ulam gawa sa Kalabasa. Kakayanin kaya natin sa harap ng bagong gulo niya?"),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Oo, Chef. Susundan natin ang damo, pati na rin ang mga insekto. Isa-isang harapin — isang hakbang sa isang pagkakataon."),
            ],
        },

        # ── Panel 2 — Trivia: floating seeds ──────────────────
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Lucas, bago itanim, ilubog muna sa tubig ang mga buto. Ang lumulutang — hindi na tama ang mga iyon."),
            ],
        },
        {
            "id":            "S2P2",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Ang mga buto ng Kalabasa na lumulutang sa tubig — dapat pa rin ba itanim?",
            "retry_question": "Isipin muli! Kung lumulutang ang buto, ano ang ibig sabihin nito tungkol sa loob nito?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Hindi — itapon sa compost"},
                {"img": "buttons/choice_hoe.png",    "label": "Oo — itanim pa rin"},
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
                ("lola_thumbs", "Tama! Ang lumulutang na buto ay puno ng hangin sa loob — hindi sila magiging malusog na halaman. Direkta sa compost na lang sila."),
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
                ("lucas_wrong", "Hindi! Ang lumulutang na buto ay hollow o walang laman — hindi ito tutubo nang maayos. Itapon na sa compost."),
            ],
        },

        # ── Day 1 transition ───────────────────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },

        # ── Panel 3 — Tool choice: Asarol for mounds ──────────
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Kailangan ng mataas na bunton ng lupa para sa Kalabasa para makagapang nang malayo ang baging, tama ba?"),
            ],
        },
        {
            "id":    "S3P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Eksakto, Chef! Mas malaki ang bunton, mas malayo ang puwedeng lakbayin ng ugat. Alin ang gagamitin natin para gumawa ng mataas na bunton?"),
            ],
        },
        {
            "id":            "S3P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Alin ang tamang kagamitan para gumawa ng mataas na bunton ng lupa para sa Kalabasa?",
            "retry_question": "Hindi pa! Kailangan natin ng kagamitan na makapagbubuo ng mataas na bunton ng lupa.",
            "choices": [
                {"img": "buttons/choice_hoe.png",    "label": "Asarol"},
                {"img": "buttons/choice_trowel.png", "label": "Dulo"},
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
                ("lucas_thumbs", "Tama! Ang Asarol ang perpekto para bumuo ng mataas na bunton ng lupa. Magiging maayos na tirahan ito ng Kalabasa!"),
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
                ("lucas_wrong", "Ang Dulo ay para sa maliliit na butas, hindi para sa pagbuo ng mataas na bunton. Subukan muli."),
            ],
        },

        # ── Panel 4 — Water scan: moisten the mound ───────────
        {
            "id":       "S4P1",
            "type":     "scan",
            "day":      1,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-01 Water Card",
            "dialogue": "I-scan ang Water Card para basain ang bagong bunton at gisingin ang mga buto ng Kalabasa na natutulog sa loob.",
            "question": "Scan the Water Card to moisten the freshly mounded soil for the squash seeds.",
        },

        # ── Day 7 transition (TIME SKIP) ──────────────────────
        {
            "id":   "day7_fade",
            "type": "transition",
        },

        # ── Panel 5 — Sort: what goes into compost? ───────────
        {
            "id":    "S5P1",
            "type":  "dialogue",
            "day":   7,
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Gusto ng Kalabasa ng maraming sustansya, Chef. Gagawa tayo ng compost — parang inihahanda natin ang pagkain bago pa ito kailanganin."),
            ],
        },
        {
            "id":    "S5P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Compost? Anong ilalagay natin doon — balat ng prutas at dahon, o 'yung plastik na nagkalat sa paligid?"),
            ],
        },
        {
            "id":            "S5P3",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Ano ang tamang ilalagay sa compost pit para sa Kalabasa?",
            "retry_question": "Isipin muli! Ang compost ay gawa sa mga bagay na maaaring mabulok at maging sustansya sa lupa.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Tuyong dahon at balat ng prutas"},
                {"img": "buttons/choice_hoe.png",    "label": "Plastik at bote"},
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
                ("lucas_thumbs", "Tama! Ang mga organic na bagay tulad ng dahon, balat ng prutas, at dumi ng hayop ay nagbubulok at nagiging mayamang pataba para sa Kalabasa."),
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
                ("lucas_wrong", "Hindi! Ang plastik at bote ay hindi nabubulok at makakalason pa sa lupa. Organic na basura lang ang pwede sa compost."),
            ],
        },

        # ── Day 21 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day21_fade",
            "type": "transition",
        },

        # ── Panel 6 — Observe: is the compost ready? ──────────
        {
            "id":    "S6P1",
            "type":  "dialogue",
            "day":   21,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Ang amoy ng compost... parang tsokolate na! Hindi na amoy basura. Handa na kaya ito?"),
            ],
        },
        {
            "id":            "S6P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Ang compost na maitim, mabuhaghag, at amoy-lupa — handa na ba itong gamitin?",
            "retry_question": "Isipin muli! Ano ang katangian ng compost na handa na para sa halaman?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Oo — handa na, ihalo sa lupa"},
                {"img": "buttons/choice_hoe.png",    "label": "Hindi — kailangan pa ng bulok na amoy"},
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
                ("lola_thumbs", "Tama! Ang handang compost ay amoy-gubat, hindi amoy-bulok. Kapag maitim at mabuhaghag na, handa na itong ihalo sa lupa."),
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
                ("lucas_wrong", "Hindi! Kapag amoy-bulok pa, hindi pa tapos ang proseso. Pero kapag amoy-lupa na at maitim — handa na."),
            ],
        },

        # ── Day 25 transition ─────────────────────────────────
        {
            "id":   "day25_fade",
            "type": "transition",
        },

        # ── Panel 7 — Fertilizer choice: Organic vs Chemical ──
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   25,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Oras na para pakainin ang lupa, Chef — hindi 'yung banayad, o yung mabilis pero mapanganib sa lupa?"),
            ],
        },
        {
            "id":       "S7P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-02 Fertilizer Card",
            "dialogue": "I-scan ang Fertilizer Card para piliin ang tamang pataba para sa malusog na lupa ng Kalabasa!",
            "question": "Scan the Fertilizer Card to choose the organic fertilizer that keeps the soil healthy.",
        },

        # ── Day 40 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day40_fade",
            "type": "transition",
        },

        # ── Panel 8 — Weed method: careful vs careless ────────
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   40,
            "bg":    "background/scenebg_planter.png",
            "chars": {"baron": "right"},
            "dark":  True,
            "lines": [
                ("baron", "Bunutin lahat ng damo nang sabay-sabay! Mas mabilis, mas maganda — huwag nang mag-ingat!"),
            ],
        },
        {
            "id":    "S8P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Lucas, may mga baging ng Kalabasa sa paligid ng damo. Paano natin aalisin ang damo nang hindi nasasira ang baging?"),
            ],
        },
        {
            "id":       "S8P3",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-03 Weed Removal Card",
            "dialogue": "I-scan ang Weed Removal Card para alamin ang tamang paraan ng pag-aalis ng damo sa paligid ng mga baging ng Kalabasa!",
            "question": "Scan the Weed Removal Card to learn the careful weeding technique that protects the squash vines.",
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
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Lucas, nilalanggam at puno ng maliit na insekto ang mga dahon!"),
            ],
        },
        {
            "id":    "S9P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Walang aalala, Lola — pero mag-ingat tayo sa pipiliin, baka pati kaibigan nating insekto ay masaktan!"),
            ],
        },
        {
            "id":       "S9P3",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-04 Pesticide Card",
            "dialogue": "I-scan ang Pesticide Card para piliin ang tamang pestisidyo na ligtas sa kalikasan at hindi makakasamang sa mga kaibigan nating insekto!",
            "question": "Scan the Pesticide Card to choose the natural pesticide that won't harm beneficial insects.",
        },

        # ── Day 90 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day90_fade",
            "type": "transition",
        },

        # ── Panel 10 — Harvest scan ───────────────────────────
        {
            "id":    "S10P1",
            "type":  "dialogue",
            "day":   90,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "Kapag matigas na ang balat at tuyo na ang tangkay — tamang-tama na ang tamis sa loob ng Kalabasa!"),
            ],
        },
        {
            "id":            "S10P2_choice",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":      "Alin ang tamang Kalabasa na handa nang anihin?",
            "retry_question": "Isipin muli! Ang tamang Kalabasa ay matigas na ang balat, kulay-kahel na, at tuyo na ang tangkay.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Matigas na balat, kahel-kayumanggi, tuyo ang tangkay"},
                {"img": "buttons/choice_hoe.png",    "label": "Malambot pa ang balat, matingkad na berde"},
            ],
            "correct": 0,
        },
        {
            "id":          "S10P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef_thumbs": "right"},
            "lines": [
                ("chef_thumbs", "Tama! Matigas na ang balat at tuyo na ang tangkay — perpekto ang tamis ng Kalabasa para sa ating ulam!"),
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
                ("lucas_wrong", "Hindi pa! Bata pa iyan — kailangan pang lumaki, tumigas ang balat, at matuyo ang tangkay bago anihin."),
            ],
        },
        {
            "id":       "S10P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-05 Harvest Card",
            "dialogue": "Napili mo na ang tamang Kalabasa! I-scan ang Harvest Card para ma-confirm ang pag-aani!",
            "question": "Scan the Harvest Card to confirm the squash with the hard orange shell and dry stem is ready.",
        },

        # ── Panel 11 — End: Ginataang Kalabasa memory ─────────
        {
            "id":    "S11P1",
            "type":  "dialogue",
            "day":   90,
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "right"},
            "lines": [
                ("chef", "GINATAANG KALABASA! May gata, may sitaw, lutuin sa katamtamang apoy — niluluto ko ito tuwing may salu-salo sa baryo!"),
            ],
        },
        {
            "id":    "S11P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Apat na alaala na?! HINDI DAPAT GANITO! Ang damo ko, ang aphids ko... lahat ay hindi sapat?!"),
            ],
        },
        {
            "id":    "S11P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Hindi sapat, Baron. Sipag lang ang panlaban namin. Apat pa, Chef — at kalahati na tayo sa lahat."),
                ("lucas", "Ginataang Kalabasa Memory — UNLOCKED!"),
            ],
        },

    ],
}
