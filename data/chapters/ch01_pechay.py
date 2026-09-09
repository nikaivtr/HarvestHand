CHAPTER = {
    "id":    "ch01",
    "crop":  "Pechay",
    "level": "beginner",
    "memory": "Awakening Memory",

    "slides": [

        # ── Title card ────────────────────────────────────────
        {
            "id":   "intro",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "logos/ch1logo.png",
        },

        # ── Scene 1, Panel 1 — Lola notices the intruder ─────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Bakit may lupang nakaungkat dito sa likod ng bahay? At... sino ka, batang nakatayo sa gitna ng aking halamanan?"),
            ],
        },

        # ── Scene 1, Panel 2 — Lucas introduces himself ───────
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Ako si Lucas, Lola ang apo mo! Mukhang gumana talaga ang mahika ni Blight Baron!"),
            ],
        },

        # ── Scene 1, Panel 3 — Blight Baron taunts ────
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "HA! Tingnan mo sila... wala na silang ala-ala ng pagsasaka, salamat sa akin! Lahat ng alam nila tungkol sa pagtatanim ay nawala, HAHAHA! Bakit ka pa nagsusumikap, bata? Sa lahat ng tao rito... kayo lang ni Lucas ang nakaka-alala. Tingnan natin kung kaya niyo itong sagipin!"),
            ],
        },

        # ── Scene 1, Panel 4 — Lucas resolves to fight back ──
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Hindi kami susuko, Lola. Andito kami ng aking kaibigan para tulungan ang ating baryo. Tingnan mo! Narito pa rin ang mga kagamitan mo. Kinabukasan, simulan na natin sa unang hakbang."),
            ],
        },

        # ── Day 1 transition ──────────────────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },

        # ── Scene 2, Panel 1 — Lola asks about the tool ──────
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Hmm... sige na. Turuan mo ako, apo. Ano itong hawak mo?"),
            ],
        },

        # ── Scene 2, Panel 2 — Lucas explains the tool ───────
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Gamit ito para gumawa ng hukay, dun ilalagay ang binhi ng pechay."),
            ],
        },

        # ── Scene 2, Panel 3 — Choice: Dulo or Asarol? ───────
        {
            "id":            "S2P3",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Alam mo ba kung alin ang tamang kagamitan para gumawa ng hukay sa pagtatanim ng pechay? Piliin ang tamang sagot!",
            "retry_question": "Hindi pa tama! Isipin mo muli, alin ang gagamitin para sa mababaw na hukay ng binhi?",
            "choices": [
                {"img": "buttons/choice_trowel.png"},
                {"img": "buttons/choice_hoe.png"},
            ],
            "correct": 0,
        },

        # ── Feedback: Correct — Lucas thumbs up ───────────────
        {
            "id":         "S2P3_right_1",
            "type":       "feedback",
            "if_correct": True,
            "random_pick": True,
            "bg":         "background/scenebg_right.png",
            "chars":      {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama! Dulo ang tamang sagot! Mababaw at maingat ang hukay nito, kaya safe ito para sa direct planting."),
            ],
        },

        # ── Feedback: Correct — Lola thumbs up ───────────────
        {
            "id":         "S2P3_right_2",
            "type":       "feedback",
            "if_correct": True,
            "random_pick": True,
            "bg":         "background/scenebg_right.png",
            "chars":      {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Magaling, anak! Kapag mababaw lang ang itatanim na buto, sapat na ang Dulo. Hindi natin laging kailangan ng malakas na kasangkapan."),
            ],
        },

        # ── Feedback: Wrong — Lucas worried ───────────────────
        {
            "id":              "S2P3_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Sandali... pakiramdam ko masyadong malalim ang hukay nito para sa direct planting."),
            ],
        },

        # ── Feedback: Wrong — Kapitan warns ───────────────────
        {
            "id":              "S2P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Mag-ingat. Ang Asarol ay para sa malalim na paghukay. Baka masira natin ang mga buto kung gagamitin natin ito dito. Subukan mong hanapin ang kasanggamit para sa mababaw na hukay."),
            ],
        },

    ],
}
