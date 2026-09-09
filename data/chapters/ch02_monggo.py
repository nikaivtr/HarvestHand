# ============================================================
#  CHAPTER 2 — MONGGO (Mung Bean)
#  Beginner | 8 story panels | Total growing days: 65
#  Characters: Lucas, Kapitan Ernesto, Blight Baron
# ============================================================

CHAPTER = {
    "id":         "ch02",
    "crop":       "Monggo",
    "level":      "beginner",
    "memory":     "Monggo Guisado Memory",
    "total_days": 65,

    "slides": [

        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "logos/ch1logo.png",    # placeholder — replace with ch2 logo
        },

        # ── Panel 1 — Kapitan Ernesto has lost his memories ────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Lucas... bakit parang may kulang sa katawan ko? Hindi ko maalala kung paano ako naging Kapitan ng baryong ito."),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Kapitan, kailangan natin ng lakas at protina para maibalik ang inyong sigla. May tanim akong perpekto para diyan — Monggo!"),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Monggo?! Kahit na itanim ninyo ang buong taniman ng Monggo, hindi magiging lakas ang katawan n'yo! Sapagkat ako — ang Blight Baron — ang nagnanakaw ng inyong lakas! HAHAHA!"),
            ],
        },
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Huwag pakinggan si Baron, Kapitan. Maliit man ang buto ng Monggo, malakas ang lutusin. Simulan na natin."),
            ],
        },

        # ── Day 1 transition ───────────────────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },

        # ── Panel 2 — Tool choice: Dulo for small seed holes ──
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Buto lang ito, Lucas. Parang walang kabuluhan. Paano natin ito ibabaon?"),
            ],
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Hindi lahat ng malakas ay mukhang malaki, Kapitan. Ang Monggo ay kailangan lang ng maliliit at maingat na butas. Alin sa dalawa ang gagamitin natin?"),
            ],
        },
        {
            "id":            "S2P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Alin ang tamang kagamitan para gumawa ng maliliit na butas para sa buto ng Monggo?",
            "retry_question": "Hindi pa! Ang Monggo ay nangangailangan ng maliliit at mababaw na butas — hindi malalim na hukay.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Dulo"},
                {"img": "buttons/choice_hoe.png",    "label": "Asarol"},
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
                ("lucas_thumbs", "Tama! Ang Dulo ay para sa maliliit at maingat na butas. Perpekto para sa maliit na buto ng Monggo!"),
            ],
        },
        {
            "id":          "S2P3_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Napakagaling! Ang maliliit na buto ay nangangailangan ng tamang lalim ng hukay — hindi masyadong malalim o mababaw."),
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
                ("lucas_wrong", "Sandali... masyadong malaki ang Asarol para sa maliit na buto ng Monggo. Piliin ang mas angkop na kagamitan."),
            ],
        },

        # ── Panel 3 — Baron tricks: siksikin! ─────────────────
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Siksikin n'yo lahat ng buto sa iisang butas! Mas marami sa isang lugar, mas mabilis matatapos — at mas madaling masisira! HAHAHA!"),
            ],
        },
        {
            "id":    "S3P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Parang efficient nga... dapat ba nating subukan, Lucas?"),
            ],
        },
        {
            "id":            "S3P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Dapat bang isiksikin ang lahat ng buto ng Monggo sa isang butas?",
            "retry_question": "Mag-isip muli! Ano ang mangyayari kung mag-aagawan ang mga buto sa sustansya at tubig?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Hindi — bigyan ng espasyo"},
                {"img": "buttons/choice_hoe.png",    "label": "Oo — isiksikin"},
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
                ("lucas_thumbs", "Tama! Kapag siksik ang mga buto, mag-aagawan sila sa tubig at sustansya. Ang tamang espasyo ang sikreto ng malusog na Monggo!"),
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
                ("lucas_wrong", "Huwag maniwala kay Baron! Kung siksik ang buto, mamamatay ang mahina at mananalo lang ang malakas. Hindi 'yan mabuti."),
            ],
        },

        # ── Day 3 transition ───────────────────────────────────
        {
            "id":   "day3_fade",
            "type": "transition",
        },

        # ── Panel 4 — Water scan: soften the soil ─────────────
        {
            "id":      "S4P1",
            "type":    "dialogue",
            "day":     3,
            "bg":      "background/scenebg_planter.png",
            "chars":   {"kapitan": "right"},
            "lines": [
                ("kapitan", "Tigang at mabato ang lupa dito, Lucas. Parang ayaw painom ng lupa natin."),
            ],
        },
        {
            "id":       "S4P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-01 Water Card",
            "dialogue": "Kaya natin 'yan, Kapitan! I-scan ang Water Card para palambutin ang lupa at lumabas ang mga sibol ng Monggo.",
            "question": "Scan the Water Card to soften the stubborn soil so the Monggo sprouts can push through.",
        },

        # ── Day 25 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day25_fade",
            "type": "transition",
        },

        # ── Panel 5 — Trivia: don't overwater ─────────────────
        {
            "id":    "S5P1",
            "type":  "dialogue",
            "day":   25,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Diligin mo ulit, Kapitan! Oras-oras, walang pahinga! Ibahao mo sila sa tubig!"),
            ],
        },
        {
            "id":    "S5P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Pero Lucas, maulap pa rin at basa pa ang lupa kanina lang. Tama ba si Baron?"),
            ],
        },
        {
            "id":            "S5P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Dapat bang diligan ang halaman kahit basa pa ang lupa mula sa ulan?",
            "retry_question": "Isipin muli! Ano ang nangyayari sa ugat ng Monggo kapag laging basa ang lupa?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Hindi — hayaang matuyo muna"},
                {"img": "buttons/choice_hoe.png",    "label": "Oo — diligin palagi"},
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
                ("lucas_thumbs", "Tama! Kapag palaging basa ang lupa, mabilis magkasakit ang ugat at maaaring mabulok. Hayaan munang huminga ang lupa."),
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
                ("lucas_wrong", "Huwag pakinggan si Baron! Ang sobrang tubig ay kamatayan ng ugat ng Monggo. Hayaan munang lumarga ang tubig."),
            ],
        },

        # ── Day 50 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day50_fade",
            "type": "transition",
        },

        # ── Panel 6 — Water scan: fill the pods ───────────────
        {
            "id":      "S6P1",
            "type":    "dialogue",
            "day":     50,
            "bg":      "background/scenebg_planter.png",
            "chars":   {"kapitan": "right"},
            "lines": [
                ("kapitan", "Ito ba ang tinatawag mong pods? Parang maliit na sundalo, nakahanay sa bawat baging!"),
            ],
        },
        {
            "id":       "S6P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-01 Water Card",
            "dialogue": "Tamang-tama, Kapitan! Kailangan ng mga pods ng huling dilig para mapuno ng butil ang loob nila.",
            "question": "Scan the Water Card to help the Monggo pods plump up with seeds inside.",
        },

        # ── Day 65 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day65_fade",
            "type": "transition",
        },

        # ── Panel 7 — Harvest scan (AC-05) ───────────────────
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   65,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Bilang Kapitan, ikaw ang dapat mamili — alin sa mga ito ang handa nang anihin?"),
            ],
        },
        {
            "id":    "S7P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Kung ako bahala... iyong matigas, di na malambot, pero hindi rin basag-basag."),
            ],
        },
        {
            "id":            "S7P3_choice",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":      "Alin ang tamang Monggo pods na handa nang anihin?",
            "retry_question": "Isipin muli! Ang tamang Monggo ay puno na, malutong, at bahagyang tuyo — hindi pa malambot at patag.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Puno, malutong, medyo tuyo na pods"},
                {"img": "buttons/choice_hoe.png",    "label": "Luntian, patag, malambot pa"},
            ],
            "correct": 0,
        },
        {
            "id":          "S7P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": "right"},
            "lines": [
                ("kapitan", "Iyan nga! Puno at malutong — hindi rin basag-basag. Iyon ang eksaktong Monggo na handa nang anihin!"),
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
                ("lucas_wrong", "Hindi pa iyon handa! Ang patag at malambot na pods ay di pa mature. Hanapin ang puno at malutong na pods!"),
            ],
        },
        {
            "id":       "S7P3",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "card":     "AC-05 Harvest Card",
            "dialogue": "Napili mo na ang tamang Monggo! I-scan ang Harvest Card para ma-confirm ang pag-aani!",
            "question": "Scan the Harvest Card to confirm the plump, slightly dry Monggo pods are ready to harvest.",
        },

        # ── Panel 8 — End: Monggo Guisado memory restored ─────
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   65,
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Bawang, kamatis, at ito... MONGGO GUISADO! Niluluto ito ng asawa ko tuwing may pulong sa barangay hall! Naalala ko na!"),
            ],
        },
        {
            "id":    "S8P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Dalawang alaala na ang naibalik, Kapitan. At tila bumabalik na rin ang tindig mo bilang pinuno."),
                ("lucas", "Monggo Guisado Memory — UNLOCKED!"),
            ],
        },

    ],
}
