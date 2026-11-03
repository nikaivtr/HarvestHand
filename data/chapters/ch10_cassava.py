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
            "logo": "chapter10.png",
        },
 
        # ── Scene 1 — The Final Stand: Baron's last gamble ─────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "default"}},
            "lines": [
                ("baron", "..."),
                ("baron", "Isang alaala na lang. Isa na lang ang natitira."),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Hindi ko hahayaang bumalik ang huling alaala! Ibubuhos ko ang lahat ng aking sumpa!"),
                ("baron", "Tagtuyot! Peste! Lason! At ang sumpa ng oras, sabay-sabay!"),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Ito na ang aking huling paninindigan! Tatlumpung segundo sa bawat kilos, bata! HAHAHAHAHA!"),
            ],
        },
        {
            "id": "S1P4",
            "type": "scene",
            "bg": "background/scenebg_baron.png",
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
            "id":    "S1P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Lahat po ng sumpa niya, sabay-sabay! Lola, paano po natin ito malalampasan?"),
            ],
        },
        {
            "id":    "S1P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Huwag kang matakot, apo. Hindi na tayo nag-iisa."),
            ],
        },
        {
            "id":    "S1P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Lucas! Lola Maria! Narinig namin ni Chef na bumalik si Baron, kaya nagmadali kaming pumunta rito."),
            ],
        },
        {
            "id":    "S1P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "left", "expression": "talking", "flip": False}},
            "lines": [
                ("chef", "Kayo ang tumulong sa aming maibalik ang aming mga alaala. Ngayon, kami naman ang tutulong sa inyo."),
            ],
        },
        {
            "id":    "S1P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Maraming salamat po, Kapitan! Salamat po, Chef!"),
            ],
        },
        {
            "id":    "S1P10",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "worried", "flip": False}},
            "lines": [
                ("lola", "Siyam na alaala na ang bumalik, apo. Ngunit may isang bagay pa akong hindi maalala."),
                ("lola", "Tuwing Pista, may bakanteng upuan sa mesa at isang plato ng kamoteng kahoy na walang kumakain."),
                ("lola", "Hindi ko maalala kung para kanino iyon."),
            ],
        },
        {
            "id":    "S1P11",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Kamoteng kahoy po ang huling pananim natin, Lola, at ito ang pinakamatibay sa lahat."),
                ("lucas", "Baka po maalala ninyo ang lahat kapag naani na natin ito."),
            ],
        },
        {
            "id":    "S1P12",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Tama ka, apo. Simulan na natin."),
            ],
        },
 
        # ── Scene 2 — Raised beds ──────────────────────────────
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ayaw ng kamoteng kahoy ang lupang laging basa. Madaling mabulok ang mga ugat nito kapag nakababad sa tubig."),
                ("lola", "Kailangan nito ng mataas at maluwag na tambak ng lupa, o raised beds."),
            ],
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Tatlumpung segundo! Magsimula na kayo!"),
            ],
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Handa na po ako. Alam ko na po ang gagawin!"),
            ],
        },
 
        # ── Raised beds — choice (TIMER) ───────────────────────
        {
            "id":            "S2P4",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Bilis! Alin ang tamang kagamitan para gumawa ng mataas na tambak ng lupa para sa kamoteng kahoy?",
            "retry_question": "Mabilis! Aling kagamitan ang kayang mag-angat ng maraming lupa?",
            "choices": [
                {"img": "buttons/choice_hoe.png",    "label": "", "frame": False},
                {"img": "buttons/choice_trowel.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S2P4_right_1",
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
                ("lucas", "Tama at mabilis! Ang asarol ang pang-angat ng lupa para sa mga tambak na hindi pinipigilan ng tubig."),
            ],
        },
        {
            "id":          "S2P4_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Sa mataas na tambak, hindi tatayo ang tubig, at madaling lalaki ang mga ugat sa maluwag na lupa."),
            ],
        },
        {
            "id":              "S2P4_wrong_1",
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
                ("lucas", "Naku po! Masyadong maliit ang dulo para sa pag-angat ng maraming lupa. Humanap tayo ng mas malakas na kagamitan!"),
            ],
        },
        {
            "id":              "S2P4_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "baron": {
                    "side": "right",
                    "expression": "laugh",
                    "flip": False,
                    }
                },
            "lines": [
                ("baron", "HAHAHA! Naubos na ang oras ninyo! Hindi kayo aabot!"),
            ],
        },
 
        # ── Day 1 — Planting the cuttings ──────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },
        {
            "id": "S3P1",
            "type": "narration_overlay",
            "day": 1,
            "bg": "background/scenebg_planter.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Unang araw ng pagtatanim. "
                "Gumupit si Lucas ng mga tangkay ng kamoteng kahoy na halos isang talampakan ang haba, "
                "at itinanim ang mga ito sa mga mataas na tambak ng lupa."
            ),
        },
        {
            "id":    "S3P2",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Hindi buto ang itinatanim natin sa kamoteng kahoy, apo, kundi pinutol na tangkay. Cutting ang tawag dito."),
                ("lola", "Siguraduhin mong nakaharap pataas ang mga buko, o mata, nito. Doon sisibol ang mga bagong dahon."),
            ],
        },
        {
            "id":       "S3P3",
            "type":     "scan",
            "day":      1,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lola": {"side": "left", "expression": "default", "flip": False}},
            "active":   "lola",
            "timer":    True,
            "card":     "AC-01 Water Card",
            "dialogue": "Lola: Bahagya lamang ang tubig, apo. Madaling mabulok ang ugat ng kamoteng kahoy kapag sobrang basa. I-scan ang Water Card, ngunit banayad lang!",
            "question": "Scan the Water Card to lightly water the cassava cuttings — just enough to settle the soil, not flood it.",
        },
 
        # ── Day 30 — Drought ───────────────────────────────────
        {
            "id":   "day30_fade",
            "type": "transition",
        },
        {
            "id":    "S4P1",
            "type":  "dialogue",
            "day":   30,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Tagtuyot! Wala nang ulan sa baryo ninyo! Tingnan natin kung kaya ng kamoteng kahoy ang uhaw!"),
            ],
        },
        {
            "id":    "S4P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "lines": [
                ("lucas", "Lola, matagal na pong hindi umuulan. Ano po ang dapat nating gawin para sa mga kamoteng kahoy?"),
            ],
        },
        {
            "id":            "S4P3",
            "type":          "choice",
            "day":           30,
            "bg":            "background/scenebg_planter.png",
            "question":       "Matagal nang hindi umuulan sa baryo. Paano dapat tulungan ni Lucas ang mga kamoteng kahoy?",
            "retry_question": "Sandali, baka masira ang mga ugat ng kamoteng kahoy sa paraang iyon. Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_mulch_field.png",   "label": "", "frame": False},
                {"img": "buttons/choice_flood_cassava.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S4P3_right_1",
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
                ("lucas", "Tama! Magtatakip tayo ng mulch para manatiling mamasa-masa ang lupa, at hindi natin lulunurin ang mga ugat."),
            ],
        },
        {
            "id":          "S4P3_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Malalim ang ugat ng kamoteng kahoy, at nakakatipid ito ng tubig sa pamamagitan ng paglalagas ng ilang dahon. Kaya nitong magtiis sa tagtuyot."),
            ],
        },
        {
            "id":              "S4P3_wrong_1",
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
                ("lucas", "Naku po! Kapag binaha ang taniman, mabubulok ang mga ugat ng kamoteng kahoy."),
            ],
        },
        {
            "id":              "S4P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "baron": {
                    "side": "right",
                    "expression": "laugh",
                    "flip": False,
                    }
                },
            "lines": [
                ("baron", "HA! Bahain ninyo! Mabubulok ang lahat ng ugat!"),
            ],
        },
 
        # ── Day 45 — Baron's "gift" of old chemicals ───────────
        {
            "id":   "day45_fade",
            "type": "transition",
        },
        {
            "id":    "S5P1",
            "type":  "dialogue",
            "day":   45,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Heto ang mga lumang kemikal ko! Ibuhos ninyo sa lupa ng taniman, at lalaki nang mabilis ang kamoteng kahoy ninyo!"),
            ],
        },
        {
            "id":    "S5P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Huwag! Ang mga kemikal na iyan ay mapupunta sa lupa, sa kamoteng kahoy, at sa lahat ng kakain nito."),
            ],
        },
        {
            "id":            "S5P3",
            "type":          "choice",
            "day":           45,
            "bg":            "background/scenebg_planter.png",
            "question":       "Ano ang dapat gawin sa mga lumang kemikal na inalok ni Baron?",
            "retry_question": "Sandali, saan mapupunta ang mga kemikal kapag inilagay natin ito sa lupa? Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_proper_disposal.png", "label": "", "frame": False},
                {"img": "buttons/choice_dump_soil.png",       "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S5P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Tama! Dadalhin natin ang mga kemikal sa tamang pasilidad ng basura, at hindi sa lupa ng ating pagkain."),
            ],
        },
        {
            "id":          "S5P3_right_2",
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
                ("lucas", "Magaling po! Ang tamang pagtatapon ay responsibilidad nating lahat, para ligtas ang taniman at ang buong baryo."),
            ],
        },
        {
            "id":              "S5P3_wrong_1",
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
                ("lucas", "Naku po! Ang kemikal sa lupa ay mapupunta sa ugat ng kamoteng kahoy at sa lahat ng kakain nito."),
            ],
        },
        {
            "id":              "S5P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Mag-ingat tayo! Hindi dapat ihalo sa lupa ng ating pagkain ang mga lumang kemikal!"),
            ],
        },
        {
            "id":    "S5P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "nervous"}},
            "lines": [
                ("baron", "Bakit... bakit hindi ninyo tinatanggap ang anumang ibigay ko?"),
            ],
        },
        {
            "id":    "S5P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "confused", "flip": True}},
            "lines": [
                ("lucas", "Parang... malungkot po ang boses niya, Lola."),
            ],
        },
 
        # ── Day 60 — Organic fertilizer ────────────────────────
        {
            "id":   "day60_fade",
            "type": "transition",
        },
        {
            "id":    "S6P1",
            "type":  "dialogue",
            "day":   60,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Oras na para pakainin ang lupa, apo. Ang kamoteng kahoy ay nag-iimbak ng pagkain sa mga ugat nito, kaya kailangan nito ng malusog na lupa."),
                ("lola", "Gagamitin natin ang compost at vermicast na natutunan nating gawin."),
            ],
        },
        {
            "id":       "S6P2",
            "type":     "scan",
            "day":      60,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-02 Fertilizer Card",
            "dialogue": "Lucas: I-scan natin ang Fertilizer Card, Lola, para piliin ang organikong pataba para sa malusog na lupa ng kamoteng kahoy. Bilis!",
            "question": "Scan the Fertilizer Card to choose the organic fertilizer for healthy cassava soil.",
        },
 
        # ── Day 90 — Careful weeding ───────────────────────────
        {
            "id":   "day90_fade",
            "type": "transition",
        },
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   90,
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Lucas, tumutubo na naman ang mga damo. Bunutin natin ang mga ito nang maingat."),
                ("kapitan", "Malapit lang sa ibabaw ng lupa ang mga ugat na lumalaki, kaya huwag nating masugatan ang mga ito."),
            ],
        },
        {
            "id":       "S7P2",
            "type":     "scan",
            "day":      90,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-03 Weed Removal Card",
            "dialogue": "Lucas: I-scan natin ang Weed Removal Card, Kapitan, para maalis ang mga damo nang hindi nasisira ang mga ugat ng kamoteng kahoy. Bilis!",
            "question": "Scan the Weed Removal Card to learn careful weeding that protects the cassava tuber underground.",
        },
 
        # ── Day 120 — Normal leaf drop ─────────────────────────
        {
            "id":   "day120_fade",
            "type": "transition",
        },
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   120,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Lola! Naglalagas po ang mga dahon ng kamoteng kahoy! May sakit po ba sila?"),
            ],
        },
        {
            "id":    "S8P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Huwag kang mag-alala, apo. Natural na naglalagas ang mga matatandang dahon ng kamoteng kahoy."),
                ("lola", "Ang dapat nating bantayan ay ang mga dahong may batik o kulot."),
            ],
        },
        {
            "id":            "S8P3",
            "type":          "choice",
            "day":           120,
            "bg":            "background/scenebg_planter.png",
            "question":       "Alin sa dalawang tanawin ang normal at hindi dapat ikabahala?",
            "retry_question": "Sandali, tingnan nating mabuti kung alin ang natural na paglalagas ng matatandang dahon. Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_old_leaves_drop.png", "label": "", "frame": False},
                {"img": "buttons/choice_leaf_spots.png",      "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S8P3_right_1",
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
                ("lucas", "Tama! Normal ang paglalagas ng mga matatandang dahon sa ibaba, at patuloy pa ring tumutubo ang mga bagong dahon sa itaas."),
            ],
        },
        {
            "id":          "S8P3_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Kailangan lang nating mag-ingat kapag maraming dahon ang may batik o kulot."),
            ],
        },
        {
            "id":              "S8P3_wrong_1",
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
                ("lucas", "Naku po! Iyan ang mga dahong may batik at kulot, kaya dapat natin itong bantayan."),
            ],
        },
        {
            "id":              "S8P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Hindi iyan ang natural na paglalagas! Tingnan nating muli ang dalawang tanawin."),
            ],
        },
 
        # ── Day 140 — Spider mites ─────────────────────────────
        {
            "id":   "day140_fade",
            "type": "transition",
        },
        {
            "id":    "S9P1",
            "type":  "dialogue",
            "day":   140,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Spider mites! Sisipsipin ng aking maliliit na gagamba ang katas ng mga dahon ninyo!"),
            ],
        },
        {
            "id":    "S9P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "lines": [
                ("lucas", "Chef! May maliliit na tuldok na dilaw sa mga dahon, at may pinong sapot sa ilalim nito!"),
            ],
        },
        {
            "id":    "S9P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "worried", "flip": False}},
            "lines": [
                ("chef", "Spider mites nga iyan, Lucas. Mahilig sila sa tuyo at mainit na panahon."),
                ("chef", "Pumili tayo ng natural na pestisidyo para hindi madamay ang mga kapaki-pakinabang na insekto."),
            ],
        },
        {
            "id":       "S9P4",
            "type":     "scan",
            "day":      140,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-04 Pesticide Card",
            "dialogue": "Lucas: I-scan natin ang Pesticide Card, Chef, para piliin ang natural na pestisidyo laban sa spider mites. Bilis!",
            "question": "Scan the Pesticide Card to choose the natural pesticide against spider mites.",
        },
 
        # ── Day 170 — Cracking soil ────────────────────────────
        {
            "id":   "day170_fade",
            "type": "transition",
        },
        {
            "id":    "S10P1",
            "type":  "dialogue",
            "day":   170,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Tingnan mo ang lupa sa paligid ng mga puno, apo. May mga bitak na at bahagyang umaangat ang lupa."),
                ("lola", "Senyales iyan na lumalaki na ang mga ugat sa ilalim at itinutulak nito ang lupa paitaas."),
            ],
        },
        {
            "id":    "S10P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Ibig sabihin po, malapit na tayong umani. Hindi po tayo dapat magdagdag ng tubig."),
            ],
        },
 
        # ── Day 195 — Harvest ──────────────────────────────────
        {
            "id":   "day195_fade",
            "type": "transition",
        },
        {
            "id":    "S11P1",
            "type":  "dialogue",
            "day":   195,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Halos lahat ng matatandang dahon ay nalagas na, at laganap na ang mga bitak sa lupa."),
                ("lola", "Bago tayo mag-ani nang marami, maghuhukay muna tayo ng isang halaman para subukan kung malalaki na ang mga ugat."),
            ],
        },
        {
            "id":    "S11P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Dahan-dahan ko pong huhukayin ang isa. Heto na po! Malalaki at matitigas ang mga ugat!"),
                ("lucas", "Ngayon po, kailangan kong pumili agad ng tamang senyales!"),
            ],
        },
 
        # ── Harvest — choice (TIMER) ───────────────────────────
        {
            "id":            "S11P3",
            "type":          "choice",
            "day":           195,
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Bilis! Alin sa dalawang halaman ang handa nang anihin?",
            "retry_question": "Mabilis! Ang handang anihing kamoteng kahoy ay may malalaking ugat at bitak na lupa.",
            "choices": [
                {"img": "buttons/choice_ready_cassava.png",   "label": "", "frame": False},
                {"img": "buttons/choice_unready_cassava.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S11P3_right_1",
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
                ("lucas", "Tama at mabilis! Malalaki ang mga ugat at bitak ang lupa, kaya handa na itong anihin."),
            ],
        },
        {
            "id":          "S11P3_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Natapos na ng halaman ang pagpupuno ng mga ugat nito."),
            ],
        },
        {
            "id":              "S11P3_wrong_1",
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
                ("lucas", "Naku po! Maliliit pa ang mga ugat niyan, kaya hindi pa ito handang anihin."),
            ],
        },
        {
            "id":              "S11P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "baron": {
                    "side": "right",
                    "expression": "laugh",
                    "flip": False,
                    }
                },
            "lines": [
                ("baron", "HAHAHA! Anihin ninyo na iyan! Mas kaunti ang makukuha ninyo!"),
            ],
        },
        {
            "id":       "S11P4",
            "type":     "scan",
            "day":      195,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-05 Harvest Card",
            "dialogue": "Lucas: Napili na po natin ang tamang halaman, Lola! I-scan natin ang Harvest Card para makumpirma ang pag-aani. Bilis!",
            "question": "Scan the Harvest Card to confirm the cassava tubers — firm, pale, and fully grown — are ready for the final harvest.",
        },
        {
            "id":    "S11P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Tulungan kita, Lucas. Puputulin muna natin ang tangkay mga isang talampakan sa ibabaw ng lupa."),
                ("kapitan", "Pagkatapos, luluwagan natin ang lupa sa paligid, at hihilahin natin nang dahan-dahan ang tangkay para lumabas ang mga ugat nang hindi napuputol."),
            ],
        },
 
        # ── Cyanide safety — humans ────────────────────────────
        {
            "id":    "S12P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Ang dami ninyong naani! Kainin na ninyo agad nang hilaw!"),
            ],
        },
        {
            "id":    "S12P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "left", "expression": "angry", "flip": False}},
            "lines": [
                ("chef", "Huwag! Ang hilaw na kamoteng kahoy ay may natural na lason na tinatawag na cyanogenic glycosides."),
                ("chef", "Kailangan itong balatan, hugasan, at lutuin nang mabuti bago kainin."),
            ],
        },
        {
            "id":            "S12P3",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Bagong ani ang kamoteng kahoy. Ano ang ligtas na paraan ng paghahanda nito bago kainin?",
            "retry_question": "Sandali, isipin natin ang lason na natural na nasa hilaw na kamoteng kahoy. Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_cooked_cassava.png", "label": "", "frame": False},
                {"img": "buttons/choice_raw_cassava.png",    "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S12P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Tama! Kapag binalatan, hinugasan, at niluto nang mabuti, nawawala ang lason at ligtas na itong kainin."),
            ],
        },
        {
            "id":          "S12P3_right_2",
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
                ("lucas", "Magaling po, Chef! Laging luto at balat ang kamoteng kahoy bago ihain."),
            ],
        },
        {
            "id":              "S12P3_wrong_1",
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
                ("lucas", "Naku po! Delikado ang hilaw na kamoteng kahoy dahil may natural itong lason."),
            ],
        },
        {
            "id":              "S12P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"chef_wrong": "right"},
            "lines": [
                ("chef_wrong", "Mag-ingat! Huwag kakain ng hilaw na kamoteng kahoy, kahit kaunti lang!"),
            ],
        },
 
        # ── Cyanide safety — animals ───────────────────────────
        {
            "id":    "S12P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Kung hindi para sa tao, ibigay ninyo sa mga hayop! Makakatipid kayo sa pakain!"),
            ],
        },
        {
            "id":            "S12P5",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Gusto ni Lucas na gamitin ang mga balat ng kamoteng kahoy bilang pagkain ng mga hayop. Ano ang ligtas na paraan?",
            "retry_question": "Sandali, nakakaapekto rin sa mga hayop ang lason ng hilaw na kamoteng kahoy. Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_cooked_feed.png", "label": "", "frame": False},
                {"img": "buttons/choice_raw_feed.png",    "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S12P5_right_1",
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
                ("lucas", "Tama! Lulutuin, patutuyuin, o ibababad muna natin bago ibigay sa mga hayop."),
            ],
        },
        {
            "id":          "S12P5_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lola", "Magaling, apo! Para sa tao man o hayop, hindi dapat hilaw ang kamoteng kahoy."),
            ],
        },
        {
            "id":              "S12P5_wrong_1",
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
                ("lucas", "Naku po! Maaaring magkasakit ang mga hayop kapag kumain sila ng hilaw na kamoteng kahoy."),
            ],
        },
        {
            "id":              "S12P5_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Mag-ingat! Huwag basta ipakain ang hilaw na kamoteng kahoy sa mga hayop!"),
            ],
        },
 
        # ── Day 200 — The last memory and Baron's confession ───
        {
            "id":   "day200_fade",
            "type": "transition",
        },
        {
            "id": "S13P1",
            "type": "narration_overlay",
            "day": 200,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "200 araw na ang lumipas. "
                "Sa barangay hall, nagluto sina Chef Agapita at Lucas ng cassava cake at suman "
                "mula sa bagong aning kamoteng kahoy."
            ),
        },
        {
            "id":    "S13P2",
            "type":  "dialogue",
            "day":   200,
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "shocked", "flip": False}},
            "lines": [
                ("lola", "Ang bangong ito... ang tamis ng ginataang kamoteng kahoy..."),
                ("lola", "Naaalala ko na! Naaalala ko na ang bakanteng upuan!"),
            ],
        },
        {
            "id":    "S13P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "nervous"}},
            "lines": [
                ("baron", "..."),
                ("baron", "Naamoy ko ang kamoteng kahoy mula sa labas. Alam kong naaalala na ninyo."),
            ],
        },
        {
            "id":    "S13P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "defeated"}},
            "lines": [
                ("baron", "Lahat ng alaala ay nabalik na. Tapos na kayo. Natalo na ako."),
            ],
        },
        {
            "id":    "S13P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "defeated"}},
            "lines": [
                ("baron", "Hindi ko alam kung bakit ko ito ginawa. Nainggit lang siguro ako."),
                ("baron", "Kayo ay nagkakasama, nagtatrabaho, nagdiriwang, at ako..."),
                ("baron", "Ako ay nag-iisa."),
            ],
        },
        {
            "id":    "S13P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "lines": [
                ("lucas", "Baron..."),
            ],
        },
        {
            "id":    "S13P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "sad", "flip": False}},
            "lines": [
                ("lola", "Baron, inimbita ka namin sa Pista noon, ngunit hindi ka dumating. Naghintay kami."),
            ],
        },
        {
            "id":    "S13P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  False,
            "chars": {"baron": {"side": "right", "expression": "nervous"}},
            "lines": [
                ("baron", "Naghintay kayo?"),
            ],
        },
        {
            "id":    "S13P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Lagi. Kaya tuwing Pista, may bakanteng upuan sa mesa at isang plato ng kamoteng kahoy."),
                ("lola", "Para iyon sa iyo, Baron."),
            ],
        },
        {
            "id":    "S13P10",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  False,
            "chars": {"baron": {"side": "right", "expression": "defeated"}},
            "lines": [
                ("baron", "Para sa akin..."),
                ("baron", "Nahiya ako noon. Sirang-sira ang taniman ko, at wala akong maibibigay sa inyo."),
                ("baron", "Mas madali pang magalit kaysa humarap sa inyo nang walang dala."),
                ("baron", "Kaya pinalimot ko kayo sa Pista, para hindi ninyo maalalang may upuang walang nakaupo. Patawad."),
            ],
        },
        {
            "id":    "S13P11",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ang Pista ng Nakalimutang Baryo ay para sa lahat, Baron, kasama ang mga nag-iisa. Lalo na sila."),
                ("lola", "Gusto mo bang sumama sa ating handaan?"),
            ],
        },
        {
            "id":    "S13P12",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"baron": {"side": "right", "expression": "renewed"}},
            "lines": [
                ("baron", "Ako... Oo. Oo, gusto ko."),
                ("baron", "Heto, isang basket ng sariwang lupa mula sa pinakamamahal kong hardin. Para sa inyong susunod na pananim."),
            ],
        },
        {
            "id":    "S13P13",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Nagbibigay po ng lupa... si Baron?"),
                ("lucas", "Hindi ko po agad malilimutan ang lahat ng nangyari, ngunit tinatanggap po namin ang iyong paghingi ng tawad."),
            ],
        },
        {
            "id":    "S13P14",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Ang dating kaaway ay ang bagong kaibigan ng baryo, apo."),
                ("lola", "Ganyan ang kapangyarihan ng pagkain at ng pagdiriwang. Pinagsasama nito ang lahat."),
            ],
        },
 
        # ── Day 201 — Grand Finale: the Pista is restored ──────
        {
            "id":   "day201_fade",
            "type": "transition",
        },
        {
            "id": "S14P1",
            "type": "narration_overlay",
            "day": 201,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Kinabukasan, napuno ng tao, tawanan, at mabangong pagkain ang barangay hall. "
                "Sa gitna ng mesa, may upuang laging nakalaan, "
                "at sa unang pagkakataon, may nakaupo na roon."
            ),
        },
        {
            "id":    "S14P2",
            "type":  "dialogue",
            "day":   201,
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "celebrates", "flip": False}},
            "lines": [
                ("lola", "Naaalala ko na ang lahat!"),
                ("lola", "Ang pechay na nilaga para sa una kong paglalako sa palengke. Ang monggo guisado para sa mga araw na kapos tayo. Ang okra na sinigang sa hapunan ng pamilya."),
            ],
        },
        {
            "id":    "S14P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ang kalabasa sa gata na paboritong ulam ng lolo mo. Ang kamatis na sarciado na niluluto namin tuwing Linggo."),
                ("lola", "Ang kamote cue na paninda natin sa palengke. Ang lugaw, ang sinangag, at ang kanin sa bawat handaan."),
            ],
        },
        {
            "id":    "S14P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "At ang kare-kare, kung saan nagtitipon ang buong baryo sa barangay hall!"),
            ],
        },
        {
            "id":    "S14P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "At ang mais na sopas, ang inihaw na mais sa tabi ng ilog, at ang popcorn tuwing Pista!"),
                ("chef", "Ngayon, mas marami pa tayong lulutuin dahil may bago na tayong kasalo."),
            ],
        },
        {
            "id":    "S14P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "At ang kamoteng kahoy, ang pagkain ng lakas at tibay."),
                ("lola", "Ito ang laging inihahain namin sa bakanteng upuan, para sa sinumang nag-iisa."),
            ],
        },
        {
            "id":    "S14P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Lola, naaalala mo na po ang lahat ng sampung alaala. Ang Pista ng Nakalimutang Baryo ay nagbalik na."),
            ],
        },
        {
            "id":    "S14P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Salamat po, Lola, sa lahat ng itinuro ninyo sa akin."),
                ("lucas", "Hindi lang po pagtatanim ang natutunan ko, kundi ang pagmamahal sa lupa, sa pagkain, at sa isa't isa."),
            ],
        },
        {
            "id":    "S14P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "celebrates", "flip": False}},
            "lines": [
                ("lola", "Ikaw ang nagbalik ng aming mga alaala, apo. Siguradong ipinagmamalaki ka ng lolo mo."),
            ],
        },
        {
            "id":    "S14P10",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"baron": {"side": "right", "expression": "renewed"}},
            "lines": [
                ("baron", "Salamat... sa upuan. At sa paanyaya."),
            ],
        },
        {
            "id": "S14P11",
            "type": "narration_overlay",
            "day": 201,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Naibalik na ang Kamoteng Kahoy Memory, at kasama nito ang lahat ng sampung alaala. "
                "Muling nagsimula ang Pista ng Nakalimutang Baryo, at sa unang pagkakataon, "
                "walang naiwang nag-iisa."
            ),
        },
    ],
}