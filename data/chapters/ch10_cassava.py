# ============================================================
#  CHAPTER 10 — CASSAVA (Kamoteng Kahoy) — THE FINAL STAND
#  Expert | 15 story panels | Total growing days: 201
#  Characters: Lucas, Lola Maria, Blight Baron (revealed lonely),
#              Kapitan Ernesto, Chef Agapita
#  MECHANIC: timer=True on all challenge slides (30-sec future impl)
#  PLOT CLIMAX: All 10 memories return. Baron is revealed as lonely.
#               Lola Maria invites Baron to the Fiesta.
#               Baron gifts a basket of fresh soil. Pista is restored.
# ============================================================

CHAPTER = {
    "id":         "ch10",
    "crop":       "Cassava",
    "level":      "advanced",
    "memory":     "Kamoteng Kahoy Memory",
    "total_days": 201,

    "slides": [

        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "logos/ch1logo.png",
        },

        # ── Panel 1 — The Final Stand: Baron's last gamble ────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "..."),
                ("baron", "Isang alaala na lang... Ang huling alaala... Kung ito ay maalis ko rin, ang Pista ay mananatiling nakalimutan magpakailanman."),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Kamoteng kahoy... Naaaalala ko na ang lahat, apo. Ang kamoteng kahoy na pinirito, ang suman, ang ginataang kamote... Naaaalala ko na ang lahat."),
                ("lola", "Ngunit isa pa ang hindi ko pa maalala — ang pinaka-mahalaga sa lahat ng alaala sa Pista."),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Huli na itong kamoteng kahoy, Lola — ngunit ito ang pinaka-matibay sa lahat ng ating pananim. Kaya natin ito, kahit sino pa ang kaharap natin."),
            ],
        },

        # ── Panel 2 — Raised beds for drainage (TIMER) ────────
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Kailangan ng mataas na bungkal para sa kamoteng kahoy — ayaw nito ng basa. Gumawa tayo ng raised beds!"),
            ],
        },
        {
            "id":            "S2P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Alin ang tamang kagamitan para gumawa ng raised beds para sa kamoteng kahoy?",
            "retry_question": "Mabilis! Alin ang ginagamit para mag-angat ng lupa sa pagtatanim ng kamoteng kahoy?",
            "choices": [
                {"img": "buttons/choice_hoe.png",    "label": "Asarol — para sa raised beds"},
                {"img": "buttons/choice_trowel.png", "label": "Sprayer — para sa tubig"},
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
                ("lucas_thumbs", "Tama at mabilis! Ang Asarol ang tamang kagamitan para gumawa ng raised beds para sa kamoteng kahoy na ayaw ng labis na tubig sa ugat!"),
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
                ("lucas_wrong", "Ang Sprayer ay para sa tubig, hindi para sa paghukay ng raised beds. Kailangan ng Asarol para sa tamang paghahanda ng lupa!"),
            ],
        },

        # ── Day 1 transition ───────────────────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },

        # ── Panel 3 — Light watering (TIMER) ──────────────────
        {
            "id":       "S3P1",
            "type":     "scan",
            "day":      1,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lola": "left"},
            "active":   "lola",
            "timer":    True,
            "card":     "AC-01 Water Card",
            "dialogue": "Lola: Bahagya lang ang tubig, apo — ang kamoteng kahoy ay madaling mabulok ang ugat kapag masyadong basa. I-scan, ngunit banayad!",
            "question": "Scan the Water Card to lightly water the cassava cuttings — just enough to settle the soil, not flood it.",
        },

        # ── Day 30 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day30_fade",
            "type": "transition",
        },

        # ── Panel 4 — Drought defense ─────────────────────────
        {
            "id":    "S4P1",
            "type":  "dialogue",
            "day":   30,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Tagtuyot! Tatuyuin ko ang inyong lupa! Tingnan natin kung kayang matuklasan ng inyong kamoteng kahoy!"),
            ],
        },
        {
            "id":    "S4P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Lola, kaya ba ng kamoteng kahoy ang tagtuyot? Ano ang dapat nating gawin?"),
            ],
        },
        {
            "id":            "S4P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Totoo ba na ang kamoteng kahoy ay may kakayahang mabuhay sa matagal na tagtuyot?",
            "retry_question": "Isipin muli! Bakit tinanim ang kamoteng kahoy sa mga lugar na may tagtuyot?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Totoo — drought-resistant ang kamoteng kahoy"},
                {"img": "buttons/choice_hoe.png",    "label": "Mali — mamamatay ito sa tagtuyot"},
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
                ("lucas_thumbs", "Tama! Ang kamoteng kahoy ay isa sa pinaka-drought-resistant na pananim — nagtatago ng tubig sa ugat nito para mabuhay sa tagtuyot!"),
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
                ("lucas_wrong", "Ang kamoteng kahoy ay isa sa pinaka-matibay na pananim laban sa tagtuyot! Iyan ang dahilan kung bakit ito tinanim sa buong mundo bilang pangkain sa panahon ng gutom."),
            ],
        },

        # ── Day 45 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day45_fade",
            "type": "transition",
        },

        # ── Panel 5 — Reject toxic dump ───────────────────────
        {
            "id":    "S5P1",
            "type":  "dialogue",
            "day":   45,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Itapon dito ang mga lumang kemikal — ang toxic waste na ito ay magpapabilis ng paglaki ng kamoteng kahoy niyo!"),
            ],
        },
        {
            "id":    "S5P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Huwag! Ang toxic chemicals sa lupa ay mapupunta sa kamoteng kahoy — at sa mga tao at hayop na kakain nito. Ito ay krimen laban sa komunidad!"),
            ],
        },
        {
            "id":            "S5P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Saan dapat itapon ang mga lumang kemikal na ibinigay ng Baron?",
            "retry_question": "Isipin muli! Ang mga toxic chemicals sa lupa ay mapupunta saan?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Tamang pasilidad ng basura — hindi sa lupa"},
                {"img": "buttons/choice_hoe.png",    "label": "Sa lupa ng hardin — para mabilis lumaki"},
            ],
            "correct": 0,
        },
        {
            "id":          "S5P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": "right"},
            "lines": [
                ("kapitan", "Tama! Ang mga kemikal na basura ay kailangang dalhin sa tamang pasilidad — hindi sa lupa ng ating pagkain. Responsibilidad nating lahat ito!"),
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
                ("lucas_wrong", "Hindi! Ang toxic chemicals sa lupa ay mapupunta sa ugat ng kamoteng kahoy at sa lahat ng kakain nito. Kailangan ng tamang pagtatapon!"),
            ],
        },

        # ── Day 60 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day60_fade",
            "type": "transition",
        },

        # ── Panel 6 — Fertilizer choice: Organic vs Chemical (TIMER) ──
        {
            "id":    "S6P1",
            "type":  "dialogue",
            "day":   60,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Oras na para pakainin ang lupa, apo — alin ang pipiliin natin para lumaki nang malusog ang mga ugat ng kamoteng kahoy?"),
            ],
        },
        {
            "id":       "S6P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-02 Fertilizer Card",
            "dialogue": "I-scan ang Fertilizer Card para piliin ang tamang pataba para sa malusog na lupa ng kamoteng kahoy — bilis!",
            "question": "Scan the Fertilizer Card to choose the organic fertilizer for healthy cassava soil.",
        },

        # ── Day 90 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day90_fade",
            "type": "transition",
        },

        # ── Panel 7 — Weed method: careful vs careless (TIMER) ─
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   90,
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Bunutin ang damo nang hindi natatamaan ang lumalaking ubod sa ilalim!"),
            ],
        },
        {
            "id":       "S7P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-03 Weed Removal Card",
            "dialogue": "I-scan ang Weed Removal Card para alamin ang tamang paraan ng pag-aalis ng damo nang hindi nasasira ang ubod ng kamoteng kahoy — bilis!",
            "question": "Scan the Weed Removal Card to learn careful weeding that protects the cassava tuber underground.",
        },

        # ── Day 120 transition (TIME SKIP) ────────────────────
        {
            "id":   "day120_fade",
            "type": "transition",
        },

        # ── Panel 8 — Falling leaves trivia ───────────────────
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   120,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Ang mga dahon ng kamoteng kahoy ay nagsisimulang mahulog — huwag matakot, apo. Ito ay normal na senyales na ang halaman ay naghahanda para sa pag-aani."),
            ],
        },
        {
            "id":            "S8P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Ano ang ibig sabihin ng paghuhulog ng mga dahon ng kamoteng kahoy malapit na sa pag-aani?",
            "retry_question": "Isipin muli! Ano ang nangyayari sa loob ng kamoteng kahoy habang nanghuhugot ng enerhiya mula sa mga dahon?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Normal — naghahanda ang halaman para sa pag-aani"},
                {"img": "buttons/choice_hoe.png",    "label": "Sakit — kailangan ng kemikal na lunas agad"},
            ],
            "correct": 0,
        },
        {
            "id":          "S8P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Tama! Ang paghuhulog ng dahon ay senyales ng senescence — ang halaman ay naglilipat ng lahat ng enerhiya papunta sa mga ugat. Mabuting palatandaan!"),
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
                ("lucas_wrong", "Hindi sakit ito! Ito ay natural na proseso ng paglipat ng enerhiya mula sa mga dahon papunta sa mga ugat. Handa na ang kamoteng kahoy!"),
            ],
        },

        # ── Day 140 transition (TIME SKIP) ────────────────────
        {
            "id":   "day140_fade",
            "type": "transition",
        },

        # ── Panel 9 — Spider mites: Sprayer (TIMER) ───────────
        {
            "id":    "S9P1",
            "type":  "dialogue",
            "day":   140,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Spider mites! Ang aking mga gagamba ay susuhop ng katas mula sa mga dahon ng inyong kamoteng kahoy! Tingnan nating kung kaya ninyo ito!"),
            ],
        },
        {
            "id":    "S9P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Spider mites, Lola! Kailangan agad ng aksyon — pero mag-ingat tayo sa pipiliin, baka pati kapaki-pakinabang na insekto ay masaktan!"),
            ],
        },
        {
            "id":       "S9P3",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-04 Pesticide Card",
            "dialogue": "I-scan ang Pesticide Card para piliin ang tamang pestisidyo laban sa spider mites — bilis!",
            "question": "Scan the Pesticide Card to choose the natural pesticide against spider mites.",
        },

        # ── Day 170 transition (TIME SKIP) ────────────────────
        {
            "id":   "day170_fade",
            "type": "transition",
        },

        # ── Panel 10 — Cracking soil — harvest sign ───────────
        {
            "id":    "S10P1",
            "type":  "dialogue",
            "day":   170,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Tingnan ang lupa sa paligid ng kamoteng kahoy, apo — may mga bitak na, at ang lupa ay nagtataas? Ito ay senyales na ang mga ugat ay malaki na at puno na."),
            ],
        },
        {
            "id":            "S10P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Ano ang ibig sabihin ng mga bitak sa lupa sa paligid ng kamoteng kahoy?",
            "retry_question": "Isipin muli! Bakit nagkakaroon ng bitak ang lupa sa paligid ng kamoteng kahoy na malapit nang anihin?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Ang ugat ay malaki na — malapit nang anihin"},
                {"img": "buttons/choice_hoe.png",    "label": "Masamang tanda — kailangan ng tubig agad"},
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
                ("lola_thumbs", "Tama! Ang bitak sa lupa ay dahil sa paglaki ng mga ugat — tinutulak ng kamoteng kahoy ang lupa sa labas habang lumalaki. Malapit na ang pag-aani!"),
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
                ("lucas_wrong", "Ang bitak ay mabuting palatandaan — ibig sabihin, puno na ang mga ugat at tinutulak na ang lupa. Huwag magdagdag ng tubig — oras na para mag-ani!"),
            ],
        },

        # ── Day 195 transition (TIME SKIP) ────────────────────
        {
            "id":   "day195_fade",
            "type": "transition",
        },

        # ── Panel 11 — Final harvest scan (TIMER) ─────────────
        {
            "id":    "S11P1",
            "type":  "dialogue",
            "day":   195,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Ang mga bitak ay laganap na, ang mga dahon ay halos lahat ay nahulog na — oras na, apo. Ang pinakamahalaga at pinakamatibay na pananim ay handa na."),
            ],
        },
        {
            "id":            "S11P2_choice",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":      "Alin ang senyales na handa na ang kamoteng kahoy para anihin? (30 segundo!)",
            "retry_question": "Mabilis! Ang handa nang kamoteng kahoy ay may maraming nahulog na dahon at bitak na lupa — hindi pa berde at maayos ang lupa.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Maraming nahulog na dahon, bitak na lupa"},
                {"img": "buttons/choice_hoe.png",    "label": "Berde pa lahat ng dahon, walang bitak ang lupa"},
            ],
            "correct": 0,
        },
        {
            "id":          "S11P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Tama at mabilis! Nahulog na ang mga dahon at bitak na ang lupa — handa na ang ating kamoteng kahoy, apo!"),
            ],
        },
        {
            "id":               "S11P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Hindi pa — kailangan pang lumaki ang tuber at mahulog ang mga dahon. Mabilis — subukan ulit!"),
            ],
        },
        {
            "id":       "S11P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-05 Harvest Card",
            "dialogue": "Napili mo na ang tamang senyales! I-scan ang Harvest Card para ma-confirm ang pag-aani — bilis!",
            "question": "Scan the Harvest Card to confirm the cassava tubers — firm, pale, and fully grown — are ready for the final harvest.",
        },

        # ── Panel 12 — Raw cassava toxic trivia ───────────────
        {
            "id":    "S12P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Hala! Kainin na raw ang kamoteng kahoy na hilaw! Sige, subukan ninyo!"),
            ],
        },
        {
            "id":    "S12P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Huwag! Ang hilaw na kamoteng kahoy ay naglalaman ng cyanogenic glycosides — isang lason na makakapanganib sa buhay kapag kinain nang hilaw!"),
            ],
        },
        {
            "id":            "S12P3",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Totoo ba na ang hilaw na kamoteng kahoy ay naglalaman ng nakakalasong sangkap at hindi dapat kainin nang hilaw?",
            "retry_question": "Isipin muli! Bakit kailangan lutuin ang kamoteng kahoy bago kainin?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Totoo — kailangan lutuin para mawala ang lason"},
                {"img": "buttons/choice_hoe.png",    "label": "Mali — ligtas na kainin nang hilaw"},
            ],
            "correct": 0,
        },
        {
            "id":          "S12P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": "right"},
            "lines": [
                ("kapitan", "Tama! Ang pagluluto ay nagtatanggal ng hydrocyanic acid mula sa kamoteng kahoy. Laging lutuin bago kainin — ito ang tamang paraan!"),
            ],
        },
        {
            "id":               "S12P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Huwag maniwala kay Baron! Ang hilaw na kamoteng kahoy ay naglalaman ng cyanogenic glycosides na nakakalason. Laging lutuin bago kainin!"),
            ],
        },

        # ── Panel 13 — Raw cassava and animals ────────────────
        {
            "id":    "S13P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Ibigay ang hilaw na kamoteng kahoy sa mga hayop! Makakatipid kayo sa pagkain nila!"),
            ],
        },
        {
            "id":            "S13P2",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Ligtas ba na ibigay ang hilaw na kamoteng kahoy bilang pagkain sa mga hayop?",
            "retry_question": "Isipin muli! Ang cyanogenic glycosides sa kamoteng kahoy — nakaapekto rin ba ito sa mga hayop?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Hindi — kailangan din lutuin o ibabad muna"},
                {"img": "buttons/choice_hoe.png",    "label": "Oo — ligtas para sa mga hayop ang hilaw"},
            ],
            "correct": 0,
        },
        {
            "id":          "S13P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Ang mga hayop ay maaari ring maapektuhan ng cyanide mula sa hilaw na kamoteng kahoy. Laging lutuin o ibabad bago ibigay sa mga hayop!"),
            ],
        },
        {
            "id":               "S13P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Hindi ligtas! Ang lason ng kamoteng kahoy ay maaaring makaapekto rin sa mga hayop. Huwag ibigay nang hilaw — laging lutuin o ibabad muna!"),
            ],
        },

        # ── Day 200 transition ────────────────────────────────
        {
            "id":   "day200_fade",
            "type": "transition",
        },

        # ── Panel 14 — Baron's revelation: lonely, not evil ───
        {
            "id":    "S14P1",
            "type":  "dialogue",
            "day":   200,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "..."),
                ("baron", "Lahat ng alaala ay nabalik na. Tapos na kayo. Natalo na ako."),
            ],
        },
        {
            "id":    "S14P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Hindi ko alam kung bakit ko ginawa ito. Nainggit lang siguro ako. Kayo ay nagkakasama, nagtatrabaho, nagdiriwang — at ako..."),
                ("baron", "Ako ay nag-iisa."),
            ],
        },
        {
            "id":    "S14P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Baron... inimbita ka namin sa Pista noon, ngunit hindi ka dumating. Naghintay kami."),
            ],
        },
        {
            "id":    "S14P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  False,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Naghintay kayo?"),
            ],
        },
        {
            "id":    "S14P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Lagi. Ang Pista ng Nakalimutang Baryo ay para sa lahat — kasama na ang mga nag-iisa. Lalo na sila."),
                ("lola", "Baron... gusto mo bang sumama sa ating Handaan?"),
            ],
        },
        {
            "id":    "S14P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Ako... Ako ay... Oo. Oo, gusto ko."),
                ("baron", "Heto — isang basket ng sariwang lupa mula sa aking pinaka-mapagmahal na hardin. Para sa inyong susunod na pananim."),
            ],
        },
        {
            "id":    "S14P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Nagbibigay ng lupa... si Baron?"),
            ],
        },
        {
            "id":    "S14P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Oo, apo. Ang dating kaaway ay ang bagong kaibigan ng baryo. Ganyan ang kapangyarihan ng pagkain at ng pagdiriwang — pinagsasama ang lahat."),
            ],
        },

        # ── Panel 15 — Grand Finale: All memories return ──────
        {
            "id":    "S15P1",
            "type":  "dialogue",
            "day":   201,
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Naaalala ko na ang lahat!"),
                ("lola", "Ang pechay na nilagang inihanda para sa aking unang palengke. Ang monggo guisado na niluto ko para sa mahirap na Linggo. Ang okra na sinigang sa hapunan ng pamilya."),
            ],
        },
        {
            "id":    "S15P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Ang kalabasa sa gata na paboritong ulam ng inyong lolo. Ang kamatis na sarciado na ginagawa ko tuwing tag-ulan. Ang kare-kare na may talong — espesyal para sa binyag."),
                ("lola", "Ang kamote cue na pambenta natin sa palengke. Ang sinangag sa umaga. Ang mais soup at ang popcorn sa Pista. At ang kamoteng kahoy — ang pagkain ng lakas at tibay."),
            ],
        },
        {
            "id":    "S15P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Lola... naaalala mo na ang lahat. Lahat ng sampung alaala. Ang Nakalimutang Pista ng Baryo..."),
            ],
        },
        {
            "id":    "S15P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "...ay natuklasan na! Ang sampung pananim. Ang sampung alaala. Ang sampung tao. Isang baryo — isang handaan."),
            ],
        },
        {
            "id":    "S15P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "left"},
            "lines": [
                ("chef", "At ngayon — kasama na rin ang dating kaaway! Mas maraming pagkain, mas maraming kwento, mas makulay ang ating handaan!"),
            ],
        },
        {
            "id":    "S15P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Salamat, Lola. Salamat sa lahat ng inyong itinuro sa akin. Hindi lang pagtatanim — kundi ang pagmamahal sa lupa, sa pagkain, at sa isa't isa."),
                ("lucas", "Ang Pista ng Nakalimutang Baryo ay nagsisimula na uli!"),
            ],
        },
        {
            "id":    "S15P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Kamoteng Kahoy Memory — UNLOCKED!"),
                ("lola", "At ang lahat ng sampung alaala ng Pista ng Nakalimutang Baryo — ay NABALIK NA!"),
            ],
        },

    ],
}
