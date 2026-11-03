# ============================================================
#  CHAPTER 9 — CORN (Mais)
#  Expert | 15 story panels | Total growing days: 102
#  Characters: Lucas, Lola Maria, Blight Baron, Chef Agapita
#  BARON MECHANIC: 30-sec timer on challenge slides (timer=True)
#  PLOT: Baron panics as the 9th memory is unlocked
# ============================================================

CHAPTER = {
    "id":         "ch09",
    "crop":       "Corn",
    "level":      "advanced",
    "memory":     "Mais Memory",
    "total_days": 102,
 
    "slides": [
 
        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "chapter9.png",
        },
 
        # ── Scene 1 — Baron raises the stakes ──────────────────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Walo na! Walo na ang naibalik ninyong alaala! Hindi ko hahayaang maging siyam!"),
                ("baron", "Ang hangin ang magiging sandata ko! Itutumba ko ang bawat pananim ninyo!"),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "At hindi pa tapos ang sumpa ng oras! Tatlumpung segundo pa rin sa bawat mahalagang kilos!"),
                ("baron", "Bilisan ninyo habang humihihip ang hangin! HAHAHAHAHA!"),
            ],
        },
        {
            "id": "S1P3",
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
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Hangin at oras na naman po ang gagamitin niya!"),
                ("lucas", "Paano po natin poprotektahan ang mga pananim?"),
            ],
        },
        {
            "id":    "S1P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "left", "expression": "talking", "flip": False}},
            "lines": [
                ("chef", "Narinig ko ang ingay at dumating ako agad, Lucas. Huwag kang matakot, may paraan tayo."),
            ],
        },
        {
            "id":    "S1P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Chef Agapita! Mabuti po at nandito kayo. Ano po ang maitutulong ninyo sa amin?"),
            ],
        },
        {
            "id":    "S1P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "left", "expression": "worried", "flip": False}},
            "lines": [
                ("chef", "Alam mo, Lucas, mais ang unang sangkap na pumapasok sa isip ko kapag iniisip ko ang paborito kong lutuin."),
                ("chef", "Ngunit kahit anong pilit ko, hindi ko matandaan kung ano iyon, at kung bakit ito mahalaga sa baryo."),
            ],
        },
        {
            "id":    "S1P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Kung ganoon po, magtanim po tayo ng mais, Chef! Baka maalala ninyo ang lahat kapag nakita ninyo ang ani."),
            ],
        },
        {
            "id":    "S1P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("chef", "Magandang ideya! Ngunit kailangan nating maghanda."),
                ("chef", "Matangkad at manipis ang tangkay ng mais, kaya madali itong matumba ng hangin."),
                ("chef", "Kailangan nito ng malalim na ugat at lupang nakatambak sa paligid ng puno."),
            ],
        },
        {
            "id":    "S1P10",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "talking", "flip": False}},
            "lines": [
                ("chef", "Una, bubungkalin natin nang malalim ang lupa at gagawa tayo ng mga tudling, o furrows, para sa mga buto."),
            ],
        },
        {
            "id":    "S1P11",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Simula na ang orasan, bata! Tatlumpung segundo!"),
            ],
        },
        {
            "id":    "S1P12",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Hindi po ako magpapadala sa pananakot mo, Baron. Handa na po ako!"),
            ],
        },
 
        # ── Deep furrows — choice (TIMER) ──────────────────────
        {
            "id":            "S1P13",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Bilis! Alin ang tamang kagamitan para bungkalin nang malalim ang lupa at gumawa ng tudling para sa mais?",
            "retry_question": "Mabilis! Aling kagamitan ang may lakas na bumungkal ng malalim na lupa?",
            "choices": [
                {"img": "buttons/choice_hoe.png",    "label": "", "frame": False},
                {"img": "buttons/choice_trowel.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S1P13_right_1",
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
                ("lucas", "Tama at mabilis! Ang asarol ang pambungkal ng malalim na lupa, kaya makakapasok nang malalim ang mga ugat ng mais."),
            ],
        },
        {
            "id":          "S1P13_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Magaling, Lucas! Ang malalim na ugat ang pinakamainam na panlaban sa hangin."),
            ],
        },
        {
            "id":              "S1P13_wrong_1",
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
                ("lucas", "Naku po! Masyadong maliit ang dulo para sa malalim na tudling. Humanap tayo ng mas malakas na kagamitan!"),
            ],
        },
        {
            "id":              "S1P13_wrong_2",
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
                ("baron", "HAHAHA! Naubos na ang oras ninyo! Ang bagal ninyo!"),
            ],
        },
 
        # ── Day 1 — Planting and deep watering ─────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },
        {
            "id": "S2P1",
            "type": "narration_overlay",
            "day": 1,
            "bg": "background/scenebg_planter.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Unang araw ng pagtatanim. "
                "Naghukay si Lucas ng mga tudling at nagtanim ng dalawa hanggang tatlong buto "
                "sa bawat butas, tatlo hanggang limang sentimetro ang lalim."
            ),
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "talking", "flip": False}},
            "lines": [
                ("chef", "Ngayon, didiligan natin ang mga buto nang malalim, at hindi nang madalas at mababaw."),
                ("chef", "Sa ganoong paraan, hahabulin ng mga ugat ang tubig pailalim, kaya lalo silang kakapit sa lupa."),
            ],
        },
        {
            "id":       "S2P3",
            "type":     "scan",
            "day":      1,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "waters", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-01 Water Card",
            "dialogue": "Lucas: Diligan natin nang malalim ang mga buto, Chef, para lumalim din ang ugat ng mais. I-scan natin ang Water Card, bilis!",
            "question": "Scan the Water Card to water the corn seeds deeply to build strong roots against Baron's wind.",
        },
        {
            "id":    "S2P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Mahusay! Basa na hanggang sa ilalim ang lupa. Hintayin na lang nating sumibol ang mga buto."),
            ],
        },
 
        # ── Day 35 — Side-dressing ─────────────────────────────
        {
            "id":   "day35_fade",
            "type": "transition",
        },
        {
            "id": "S3P1",
            "type": "narration_overlay",
            "day": 35,
            "bg": "background/scenebg_planter.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "35 araw na ang lumipas. "
                "Hanggang tuhod na ang taas ng mga mais, "
                "at may anim na dahon na ang bawat halaman."
            ),
        },
        {
            "id":    "S3P2",
            "type":  "dialogue",
            "day":   35,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "talking", "flip": False}},
            "lines": [
                ("chef", "Panahon na para sa side-dressing, ang pagdaragdag ng pataba sa tabi ng hilera."),
                ("chef", "Mabilis kumain ng sustansya ang mais sa yugtong ito, kaya kailangan nila ng dagdag na pagkain."),
            ],
        },
        {
            "id":    "S3P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Saan po natin ilalagay ang pataba, Chef?"),
            ],
        },
        {
            "id":            "S3P4",
            "type":          "choice",
            "day":           35,
            "bg":            "background/scenebg_planter.png",
            "question":       "Magdaragdag si Lucas ng organikong pataba sa mga mais. Saan dapat niya itong ilagay?",
            "retry_question": "Sandali, baka masunog ang mga ugat kapag doon ito inilagay. Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_side_band.png", "label": "", "frame": False},
                {"img": "buttons/choice_at_stem.png",   "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S3P4_right_1",
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
                ("lucas", "Tama! Ilalagay natin ang pataba sa tabi ng hilera, mga apat na pulgada mula sa puno, at hindi ito dumidikit sa tangkay."),
            ],
        },
        {
            "id":          "S3P4_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Magaling! Kapag dumikit ang pataba sa tangkay at sa ugat, maaari itong makasunog sa halaman."),
            ],
        },
        {
            "id":              "S3P4_wrong_1",
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
                ("lucas", "Naku po! Kapag tinambak ang pataba mismo sa puno, maaaring masunog ang mga ugat ng mais."),
            ],
        },
        {
            "id":              "S3P4_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"chef_wrong": "right"},
            "lines": [
                ("chef_wrong", "Mag-ingat tayo! Ang pataba na nakadikit sa puno ay napakakonsentrado at madaling makasunog ng ugat!"),
            ],
        },
        {
            "id":    "S3P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Tatlumpung segundo na naman, bata! Piliin mo ang kagamitan!"),
            ],
        },
 
        # ── Side-dressing tool — choice (TIMER) ────────────────
        {
            "id":            "S3P6",
            "type":          "choice",
            "day":           35,
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Bilis! Alin ang tamang kagamitan para maingat na ilagay ang pataba sa tabi ng hilera ng mais?",
            "retry_question": "Mabilis! Aling kagamitan ang tumpak at hindi makakasira sa mga ugat?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "", "frame": False},
                {"img": "buttons/choice_hoe.png",    "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S3P6_right_1",
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
                ("lucas", "Tama at mabilis! Maliit at tumpak ang dulo, kaya mailalagay natin ang pataba sa tamang lugar."),
            ],
        },
        {
            "id":          "S3P6_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Magaling, Lucas! Maingat ang pagkakahukay kaya hindi nasira ang mga ugat."),
            ],
        },
        {
            "id":              "S3P6_wrong_1",
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
                ("lucas", "Naku po! Masyadong malapad ang asarol at maaari nitong masira ang mga ugat ng mais."),
            ],
        },
        {
            "id":              "S3P6_wrong_2",
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
                ("baron", "HA! Nagkamali ka na naman! Tumatakbo ang oras, bata!"),
            ],
        },
 
        # ── Day 40 — Weeding and hilling up ────────────────────
        {
            "id":   "day40_fade",
            "type": "transition",
        },
        {
            "id":    "S4P1",
            "type":  "dialogue",
            "day":   40,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "talking", "flip": False}},
            "lines": [
                ("chef", "Ngayon, itatambak natin ang lupa sa paligid ng bawat puno. Hilling up ang tawag dito."),
                ("chef", "Ngunit alisin muna natin ang mga damo, kung hindi, matatabunan din natin ang mga ito at tutubo silang muli."),
            ],
        },
        {
            "id":       "S4P2",
            "type":     "scan",
            "day":      40,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-03 Weed Removal Card",
            "dialogue": "Lucas: Alisin muna natin ang mga damo, Chef, bago itambak ang lupa sa paligid ng puno. I-scan natin ang Weed Removal Card, bilis!",
            "question": "Scan the Weed Removal Card to clear the weeds before hilling up the corn for wind support.",
        },
        {
            "id":    "S4P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Gamit ang asarol, itataas ko ang lupa sa gilid ng bawat puno ng mais."),
            ],
        },
        {
            "id":    "S4P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Tama, Lucas! Ang tambak na lupa ay sumusuporta sa tangkay."),
                ("chef", "Tutubuan din ng dagdag na mga ugat ang ibabang bahagi ng puno, kaya lalo itong tatatag laban sa hangin."),
            ],
        },
 
        # ── Day 58 — Wind and pollination ──────────────────────
        {
            "id":   "day58_fade",
            "type": "transition",
        },
        {
            "id": "S5P1",
            "type": "narration_overlay",
            "day": 58,
            "bg": "background/scenebg_planter.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "58 araw na ang lumipas. "
                "Matatangkad na ang mga mais, at namumukadkad na ang mga bulaklak sa tuktok nito."
            ),
        },
        {
            "id":    "S5P2",
            "type":  "dialogue",
            "day":   58,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Ito na ang aking hangin! Titingnan natin kung may matitirang nakatayo!"),
            ],
        },
        {
            "id": "S5P3",
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
            "id":    "S5P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Chef! Napakalakas ng hangin!"),
            ],
        },
        {
            "id":    "S5P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Nakatayo pa rin po sila! Hindi natumba ang kahit isa!"),
            ],
        },
        {
            "id":    "S5P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Dahil iyan sa malalim na ugat at sa tambak na lupa na ginawa mo, Lucas!"),
            ],
        },
        {
            "id":    "S5P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Hmp! Kung hindi ninyo kayang ibagsak sa hangin, babasain ko ang mga bulaklak!"),
                ("baron", "Diligan ninyo ang tuktok ng mga mais ngayong umaga! Mas maganda iyon para sa kanila!"),
            ],
        },
        {
            "id":    "S5P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "talking", "flip": False}},
            "lines": [
                ("chef", "Mag-ingat, Lucas. Ang mais ay pina-pollinate ng hangin, hindi ng mga bubuyog."),
                ("chef", "Ang pollen mula sa mga bulaklak sa tuktok ang dapat bumagsak sa mga seda, o hibla, ng bawat mais."),
            ],
        },
 
        # ── Pollination — choice ───────────────────────────────
        {
            "id":            "S5P9",
            "type":          "choice",
            "day":           58,
            "bg":            "background/scenebg_planter.png",
            "question":       "Kumakalat na ang pollen ng mais sa hangin. Paano dapat magdilig si Lucas ngayong umaga?",
            "retry_question": "Sandali, isipin natin kung saan dapat pumunta ang tubig para hindi mahugasan ang pollen. Subukan nating muli.",
            "choices": [
                {"img": "buttons/choice_water_roots.png",  "label": "", "frame": False},
                {"img": "buttons/choice_sprinkle_top.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S5P9_right_1",
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
                ("lucas", "Tama! Sa ugat tayo magdidilig, kaya hindi mababasa at mahuhugasan ang pollen sa itaas."),
            ],
        },
        {
            "id":          "S5P9_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Magaling! Kapag tuyo ang pollen, mas madali itong dadalhin ng hangin sa mga seda."),
            ],
        },
        {
            "id":              "S5P9_wrong_1",
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
                ("lucas", "Naku po! Kapag winisikan ang tuktok, mahuhugasan ang pollen at hindi ito makakarating sa mga seda."),
            ],
        },
        {
            "id":              "S5P9_wrong_2",
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
                ("baron", "HAHAHA! Basain ninyo ang lahat ng bulaklak! Mas kaunti ang butil, mas masaya!"),
            ],
        },
 
        # ── Day 65 — Brown silk ────────────────────────────────
        {
            "id":   "day65_fade",
            "type": "transition",
        },
        {
            "id":    "S6P1",
            "type":  "dialogue",
            "day":   65,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Tingnan mo ang mga seda ng mais, apo. Ang bawat hibla ay nakakabit sa isang butil sa loob ng bunga."),
                ("lola", "Kailangang dapuan ng pollen ang bawat hibla para mabuo ang butil."),
            ],
        },
        {
            "id":            "S6P2",
            "type":          "choice",
            "day":           65,
            "bg":            "background/scenebg_planter.png",
            "question":       "Alin sa dalawang mais ang nagpapakitang natanggap na ang pollen at lumalaki na ang mga butil?",
            "retry_question": "Sandali, tingnan nating mabuti ang kulay ng seda. Pag-isipan natin muli.",
            "choices": [
                {"img": "buttons/choice_brown_silk.png", "label": "", "frame": False},
                {"img": "buttons/choice_white_silk.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S6P2_right_1",
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
                ("lucas", "Tama! Kapag kayumanggi at tuyo na ang seda, ibig sabihin ay tapos na ang pollination at lumalaki na ang mga butil."),
            ],
        },
        {
            "id":          "S6P2_right_2",
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
                ("lola", "Magaling, apo! Ang sariwang puting seda ay naghihintay pa ng pollen."),
            ],
        },
        {
            "id":              "S6P2_wrong_1",
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
                ("lucas", "Naku po! Sariwa pa ang puting seda, kaya naghihintay pa ito ng pollen."),
            ],
        },
        {
            "id":              "S6P2_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"chef_wrong": "right"},
            "lines": [
                ("chef_wrong", "Hindi pa iyan! Hintayin muna nating maging kayumanggi ang seda bago tayo magtiwalang natapos ang pollination."),
            ],
        },
 
        # ── Day 70 — Corn borers ───────────────────────────────
        {
            "id":   "day70_fade",
            "type": "transition",
        },
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   70,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Heto ang pinakamagandang sandata ko! Mga corn borer!"),
                ("baron", "Papasok sila sa loob ng tangkay at ng mais, at uubusin nila ang mga butil! HAHAHAHA!"),
            ],
        },
        {
            "id":    "S7P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "lines": [
                ("lucas", "Chef! May maliliit na butas po sa mga tangkay, at may pinong serbuk na parang kahoy sa paligid."),
            ],
        },
        {
            "id":    "S7P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "worried", "flip": False}},
            "lines": [
                ("chef", "Corn borers nga iyan. Pumapasok ang mga uod sa loob, kaya mahirap silang maabot."),
                ("chef", "Kailangan natin ng natural na pestisidyo, para hindi tayo makasakit ng mga kapaki-pakinabang na insekto."),
            ],
        },
        {
            "id":       "S7P4",
            "type":     "scan",
            "day":      70,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-04 Pesticide Card",
            "dialogue": "Lucas: I-scan natin ang Pesticide Card, Chef, para piliin ang natural na pestisidyo laban sa corn borers. Bilis!",
            "question": "Scan the Pesticide Card to choose the natural pesticide against corn borers.",
        },
        {
            "id":    "S7P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "nervous"}},
            "lines": [
                ("baron", "Hindi... Bakit hindi pa rin sila bumabagsak? Anong klaseng mga pananim ang mga ito?"),
            ],
        },
 
        # ── Day 80 — Kernel fill ───────────────────────────────
        {
            "id":   "day80_fade",
            "type": "transition",
        },
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   80,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "talking", "flip": False}},
            "lines": [
                ("chef", "Namamaga na ang mga butil at napupuno ng katas na parang gatas."),
                ("chef", "Kailangan nila ng sapat na tubig ngayon para maging malaki at matambok ang bawat isa."),
            ],
        },
        {
            "id":       "S8P2",
            "type":     "scan",
            "day":      80,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "waters", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-01 Water Card",
            "dialogue": "Lucas: Diligan natin ang mga mais, Chef, para maging malaki at matambok ang mga butil. I-scan natin ang Water Card, bilis!",
            "question": "Scan the Water Card to water the corn during kernel plumping stage for full, juicy kernels.",
        },
 
        # ── Day 95 — Harvest ───────────────────────────────────
        {
            "id":   "day95_fade",
            "type": "transition",
        },
        {
            "id":    "S9P1",
            "type":  "dialogue",
            "day":   95,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Tingnan mo, Lucas! Tuyo at kayumanggi na ang mga seda, at mukhang masikip na ang mga butil."),
                ("chef", "Oras na para umani!"),
            ],
        },
        {
            "id":    "S9P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Kailangan ko pong pumili agad ng mais na handa na, Chef. Hindi po ako magkakamali!"),
            ],
        },
 
        # ── Harvest — choice (TIMER) ───────────────────────────
        {
            "id":            "S9P3",
            "type":          "choice",
            "day":           95,
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Bilis! Alin ang mais na handa nang anihin?",
            "retry_question": "Mabilis! Ang handang anihing mais ay may kayumangging seda at masikip na mga butil.",
            "choices": [
                {"img": "buttons/choice_corn_ready.png",  "label": "", "frame": False},
                {"img": "buttons/choice_corn_unripe.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S9P3_right_1",
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
                ("lucas", "Tama at mabilis! Kayumanggi ang seda at masikip ang mga butil, kaya handa na itong anihin."),
            ],
        },
        {
            "id":          "S9P3_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Magaling, Lucas! Iyan ang mais na pinakamatamis at pinakamasarap."),
            ],
        },
        {
            "id":              "S9P3_wrong_1",
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
                ("lucas", "Naku po! Puti pa ang seda at hindi pa puno ang mga butil, kaya hindi pa ito hinog."),
            ],
        },
        {
            "id":              "S9P3_wrong_2",
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
                ("baron", "HAHAHA! Anihin ninyo na kahit hilaw pa! Mas kaunti ang aanihin ninyo!"),
            ],
        },
        {
            "id":       "S9P4",
            "type":     "scan",
            "day":      95,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-05 Harvest Card",
            "dialogue": "Lucas: Napili na po natin ang tamang mais, Chef! I-scan natin ang Harvest Card para makumpirma ang pag-aani. Bilis!",
            "question": "Scan the Harvest Card to confirm the corn with brown silks and plump, shiny kernels is ready to harvest.",
        },
        {
            "id":    "S9P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": {"side": "left", "expression": "talking", "flip": False}},
            "lines": [
                ("chef", "Ang ilan sa mga ito ay lulutuin natin nang sariwa. Ang iba ay patutuyuin natin at itatago, para sa popcorn at sa susunod na taniman."),
            ],
        },
 
        # ── Drying ─────────────────────────────────────────────
        {
            "id":    "S10P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Ilagay ninyo agad sa sako ang mga mais habang basa pa! Baka maunahan kayo ng ulan!"),
            ],
        },
        {
            "id":    "S10P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "angry", "flip": False}},
            "lines": [
                ("lola", "Huwag kang maniwala sa kaniya, apo! Ang basang butil sa saradong sako ay aamagin."),
            ],
        },
        {
            "id":            "S10P3",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Bagong ani ang mais na itatago at basa pa ang mga butil. Ano ang dapat gawin bago ito itago?",
            "retry_question": "Sandali, isipin natin kung ano ang mangyayari sa basang butil sa loob ng sako. Subukan nating muli.",
            "choices": [
                {"img": "buttons/choice_sun_dry_corn.png",  "label": "", "frame": False},
                {"img": "buttons/choice_wet_corn_sack.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S10P3_right_1",
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
                ("lola", "Tama! Dapat bumaba sa halos labintatlo hanggang labing-apat na porsiyento ang halumigmig ng butil bago itago, para hindi ito amagin."),
            ],
        },
        {
            "id":          "S10P3_right_2",
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
                ("lucas", "Magaling! Ilalatag po natin ang mais sa araw at hahaluin paminsan-minsan para pantay ang pagkatuyo."),
            ],
        },
        {
            "id":              "S10P3_wrong_1",
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
                ("lucas", "Naku po! Ang basang mais sa saradong sako ay aamagin at hindi na ligtas kainin."),
            ],
        },
        {
            "id":              "S10P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"chef_wrong": "right"},
            "lines": [
                ("chef_wrong", "Huwag munang itago! Ang halumigmig sa loob ng sako ay nagpapabilis ng pagkabulok."),
            ],
        },
 
        # ── Day 100 — Ventilated storage ───────────────────────
        {
            "id":   "day100_fade",
            "type": "transition",
        },
        {
            "id":    "S11P1",
            "type":  "dialogue",
            "day":   100,
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "left", "expression": "talking", "flip": False}},
            "lines": [
                ("chef", "Tuyo na ang mga butil, Lucas. Ngayon, pag-isipan natin kung saan at paano ito itatago."),
            ],
        },
        {
            "id":            "S11P2",
            "type":          "choice",
            "day":           100,
            "bg":            "background/scenebg_default.png",
            "question":       "Paano dapat itago ang tuyong mais para hindi ito amagin at pamugaran ng insekto?",
            "retry_question": "Sandali, isipin natin kung saan madaling pasukin ng halumigmig at insekto ang mais. Subukan nating muli.",
            "choices": [
                {"img": "buttons/choice_ventilated_crib.png", "label": "", "frame": False},
                {"img": "buttons/choice_floor_sack.png",      "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S11P2_right_1",
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
                ("lucas", "Tama! Ang tuyo at mahangin na imbakan na nakataas mula sa sahig ang nagpoprotekta sa mais laban sa amag at insekto."),
            ],
        },
        {
            "id":          "S11P2_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Magaling, Lucas! Ang maayos na imbakan ang huling hakbang para manatiling masarap at ligtas ang ating mais."),
            ],
        },
        {
            "id":              "S11P2_wrong_1",
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
                ("lucas", "Naku po! Ang sako sa sahig ay madaling pasukin ng halumigmig at insekto."),
            ],
        },
        {
            "id":              "S11P2_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"chef_wrong": "right"},
            "lines": [
                ("chef_wrong", "Mag-ingat! Mawawala ang ani natin kapag nakapasok sa mais ang halumigmig at mga insekto."),
            ],
        },
 
        # ── Day 102 — The Mais memory and Baron's panic ────────
        {
            "id":   "day102_fade",
            "type": "transition",
        },
        {
            "id": "S12P1",
            "type": "narration_overlay",
            "day": 102,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "102 araw na ang lumipas. "
                "Nilaga ni Lucas ang ilang bagong aning mais, "
                "at ang mabangong singaw ay napuno ang munting kusina ni Chef Agapita."
            ),
        },
        {
            "id":    "S12P2",
            "type":  "dialogue",
            "day":   102,
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "left", "expression": "worried", "flip": False}},
            "lines": [
                ("chef", "Ang bangong ito... ang tamis ng sariwang mais..."),
                ("chef", "Teka, parang may bumabalik sa alaala ko."),
            ],
        },
        {
            "id":    "S12P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Mais! Ang mais na sopas, ang inihaw na mais sa tabi ng ilog, ang popcorn tuwing Pista ng Baryo!"),
                ("chef", "Naaalala ko na ang lahat ng inihanda ko para sa buong baryo!"),
            ],
        },
        {
            "id":    "S12P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Napakasaya ko pong marinig iyan, Chef! Matagal na pong naghihintay ang baryo sa mga luto ninyo."),
            ],
        },
        {
            "id": "S12P5",
            "type": "narration_overlay",
            "day": 102,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Sa sandaling iyon, lumiwanag ang paligid at bumalik ang alaala ni Chef Agapita. "
                "Naibalik na ang Mais Memory."
            ),
        },
        {
            "id":    "S12P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "nervous"}},
            "lines": [
                ("baron", "Hindi... hindi puwede! Siyam na? Paano nangyari ito?!"),
                ("baron", "Isang alaala na lang... ISANG ALAALA NA LANG ang natitirang nagpoprotekta sa akin!"),
            ],
        },
        {
            "id": "S12P7",
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
            "id":    "S12P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "lines": [
                ("lucas", "Lola, hindi po siya mukhang galit. Mukha po siyang takot na takot."),
            ],
        },
        {
            "id":    "S12P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "worried", "flip": False}},
            "lines": [
                ("lola", "Napansin ko rin iyon, apo. Mukhang may mas malalim na dahilan si Baron kaysa sa inaakala natin."),
                ("lola", "Ngunit kailangan muna nating tapusin ang ating sinimulan."),
            ],
        },
        {
            "id": "S12P10",
            "type": "narration_overlay",
            "day": 102,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Siyam na alaala na ang naibalik. "
                "Isa na lamang ang natitira."
            ),
        },
    ],
}