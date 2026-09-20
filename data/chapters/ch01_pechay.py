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
            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "talking",
                    "flip": True,
                    }
                    },
            "lines": [
                ("lucas", "Ako si Lucas, Ang apo ni Lola Maria. Ngayong araw  tutulungan ko si Lola Maria sa aming taniman ng Petchay."),
            ],
        },

        # ── Scene 1, Panel 2 — Lucas introduces himself ───────
            {
                "id":    "S1P2",
                "type":  "dialogue",
                "bg":    "background/scenebg_default.png",
                "chars": {
                    "lucas": {
                        "side": "left",
                        "expression": "default",
                        "flip": True,
                        }
                        },
                "lines": [
                    ("lucas", "Sigurado akong matutuwa si Lola Maria dahil may tutulong na sa kanya sa taniman."),
                ],
            },

        # ── Scene 1, Panel 3 — Lucas asks you to come with him ───────
            {
                "id":    "S1P2",
                "type":  "dialogue",
                "bg":    "background/scenebg_default.png",
                "chars": {
                    "lucas": {
                        "side": "left",
                        "expression": "thumbs",
                        "flip": True,
                        }
                        },
                "lines": [
                    ("lucas", "Tara! Samahan nyo ako."),
                ],
            },

        # ── transition ───────
        {
            "id": "TRANSITION_1",
            "type": "transition",
        },

        # ── Scene 2, Panel 1 — lola looking worried ───────
            {
                "id":    "S1P1",
                "type":  "dialogue",
                "bg":    "background/scenebg_default.png",
                "chars": {
                    "lola": {
                        "side": "left",
                        "expression": "tired",
                        }
                        },
                "lines": [
                    ("lola", "..."),
                ],
            },

        # ── Scene 2, Panel 2 — Lola asks about the tool ──────
            {
                "id": "S2P2",
                "type": "scene",
                "bg": "background/scenebg_default.png",

                "chars": {
                    "lucas": {
                        "side": "right",
                        "expression": "default",
                        "position": 0.5,
                        "flip": False,
                    },
                    "lola": {
                        "side": "left",
                        "expression": "tired",
                        "position": 0.5,
                    },
                },
            },

        # ── Scene 2, Panel 3 — Lucas is concerned ───────
        {
            "id": "S2P3",
            "type": "dialogue",
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            
            "chars": {
                "lucas": {
                    "side": "right",
                    "expression": "concerned",
                    "flip": False,
                },
                "lola": {
                    "side": "left",
                    "expression": "tired",
                },
            },
            "lines": [
                ("lucas", "Anong Problema Lola Maria?"),
            ],
        },

        # ── Scene 2, Panel 4 — lucas concerned about lola ───────
            {
                "id": "S2P4",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
                "dim_inactive": False,
        
                "chars": {
                    "lucas": {
                        "side": "right",
                        "expression": "concerned",
                        "flip": False,
                    },
                    "lola": {
                        "side": "left",
                        "expression": "tired",
                    },
                },
                "lines": [
                    ("lola", "Bakit may lupang nakaungkat dito sa likod ng bahay? At... sino ka, batang nakatayo sa gitna ng aking halamanan?"),
                ],
            },

        # ── Scene 2, Panel 5 - Lola talks to lucas ───────────────
        {
            "id": "S2P5",
            "type": "dialogue",
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
    
            "chars": {
                "lucas": {
                    "side": "right",
                    "expression": "concerned",
                    "flip": False,
                },
                "lola": {
                    "side": "left",
                    "expression": "tired",
                },
            },
            "lines": [
                ("lola", "Lola, ako ito ang apo mong si Lucas! Andito ako para tulungan kang mag tanim ng petchay!"),
            ],
        },
        # ── Scene 2, Panel 6 - Lola is confused ───────────────
        {
            "id": "S2P6",
            "type": "dialogue",
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "right",
                    "expression": "concerned",
                    "flip": False,
                },
                "lola": {
                    "side": "left",
                    "expression": "tired",
                },
            },
            "lines": [
                ("lola", "Apo? Tanim? Petchay? Anong pinagsasabi mo bata?"),
            ],
        },

        # ── Scene 2, Panel 7 - Lucas is confused ───────────────
        {
            "id": "S2P7",
            "type": "dialogue",
            "bg": "background/scenebg_default.png",

            "chars": {
                "lucas": {
                    "side": "right",
                    "expression": "afraid",
                    "flip": False,
                },
                "lola": {
                    "side": "left",
                    "expression": "tired",
                    "dim_inactive": True,
                },
            },
            "lines": [
                ("lucas", "Naku! Hindi ata ako naa-alala ni Lola Maria. Ano ba ang nangyayari dito?"),
            ],
        },

        # ── Scene 2, Panel 8 - Baron Arrives ───────────────
            {
                "id": "S2P8",
                "type": "dialogue",
                "bg": "background/scenebg_baron.png",
        
                "chars": {
                    "baron": {
                        "side": "right",
                        "expression": "default",
                        "flip": False,
                    },
                },
                "lines": [
                    ("baron", "HA! Gumana nga ang aking sumpang ginawa kagabi!"),
                ],
            },
        # ── Scene 2, Panel 9 - Lucas is confused ───────────────
            {
                "id": "S2P9",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
        
                "chars": {
                    "lucas": {
                        "side": "left",
                        "expression": "confused",
                        "flip": False,
                    },
                },
                "lines": [
                    ("lucas", "Sinong nandyan?!"),
                ],
            },
        # ── Scene 2, Panel 10 - Baron introduce himself ───────────────
            {
                "id": "S2P10",
                "type": "dialogue",
                "bg": "background/scenebg_baron.png",

                "chars": {
                    "baron": {
                        "side": "right",
                        "expression": "smile",
                        "flip": False,
                    },
                },
                "lines": [
                    ("baron", "Ako si Blight Baron! Ang tagapaghasik ng lagim sa sinu-mang nagbabalak magtanim dito sa aking lupain!"),
                ],
            },
        # ── Scene 2, Panel 11 - Baron revealed his plan ───────────────
            {
                "id": "S2P11",
                "type": "dialogue",
                "bg": "background/scenebg_baron.png",

                "chars": {
                    "baron": {
                        "side": "right",
                        "expression": "smile",
                        "flip": False,
                    },
                },
                "lines": [
                    ("baron", "Simula ngayon wala nang sinu-man ang makaka-alala kung paano mag tanim ng tama at masagana!"),
                ],
            },
        # ── Scene 2, Panel 12 - Lucas is confused ───────────────
            {
                "id": "S2P12",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
    
                "chars": {
                    "lucas": {
                        "side": "left",
                        "expression": "confused",
                        "flip": False,
                    },
                },
                "lines": [
                    ("lucas", "Bakit mo po ito ginagawa?"),
                ],
            },
        # ── Scene 2, Panel 13 - Baron mocks Lucas ───────────────
            {
                "id": "S2P13",
                "type": "dialogue",
                "bg": "background/scenebg_baron.png",

                "chars": {
                    "baron": {
                        "side": "right",
                        "expression": "smile",
                        "flip": False,
                    },
                },
                "lines": [
                    ("baron", "Wala ka nang pakialam kung bakit bata! Sapagkat wala ka nang magagawa pa!"),
                ],
            },
        # ── Scene 2, Panel 14 - Baron threathens Lucas ───────────────
            {
                "id": "S2P14",
                "type": "dialogue",
                "bg": "background/scenebg_baron.png",

                "chars": {
                    "baron": {
                        "side": "right",
                        "expression": "laugh",
                        "flip": False,
                    },
                },
                "lines": [
                    ("baron", "Ipagkakait ko sa inyo ngayon, ang minsan nyo nang ipinagkait sa akin! HAHAHAHA!"),
                ],
            },
        # ── Scene 2, Panel 15 - Lucas is begging Baron not to do it ───────────────
            {
                "id": "S2P15",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
    
                "chars": {
                    "lucas": {
                        "side": "left",
                        "expression": "confused",
                        "flip": False,
                    },
                },
                "lines": [
                    ("lucas", "Pakiusap po, wag nyo po itong gawin. Maawa po kayo sa amin!"),
                ],
            },
        # ── Scene 2, Panel 16 - Baron threathens Lucas ───────────────
            {
                "id": "S2P16",
                "type": "dialogue",
                "bg": "background/scenebg_baron.png",

                "chars": {
                    "baron": {
                        "side": "right",
                        "expression": "default",
                        "flip": False,
                    },
                },
                "lines": [
                    ("baron", "Hindi mo na ito mapipigilan bata! Kaya sumuko ka nalang at kalimutan ang ano mang may kinalaman sa pagtatanim!"),
                ],
            },
        # ── Scene 2, Panel 17 - Lucas is determined to stop Baron ───────────────
            {
                "id": "S2P17",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
    
                "chars": {
                    "lucas": {
                        "side": "left",
                        "expression": "determined",
                        "flip": True,
                    },
                },
                "lines": [
                    ("lucas", "Dyan po kayo nagkakamali! Hindi ako susuko hanggat hindi ako nakakahanap ng lunas sa sumpa!"),
                ],
            },
        # ── Scene 2, Panel 18 - Lucas is thinking a strategy to stop Baron ───────────────
            {
                "id": "S2P18",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
    
                "chars": {
                    "lucas": {
                        "side": "left",
                        "expression": "wrong",
                        "flip": True,
                    },
                },
                "lines": [
                    ("lucas", "Kailangan kong ipaalala kay Lola Maria ang lahat upang matulungan ko syang makawala sa sumpa."),
                ],
            },
        # ── Scene 2, Panel 19 - Lucas is thinking a strategy to stop Baron ───────────────
            {
                "id": "S2P19",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
    
                "chars": {
                    "lucas": {
                        "side": "left",
                        "expression": "wrong",
                        "flip": True,
                    },
                },
                "lines": [
                    ("lucas", "Kailangan kong ipaalala kay Lola Maria ang lahat upang matulungan ko syang makawala sa sumpa."),
                ],
            },
        # ── Scene 2, Panel 20 - Baron threathens Lucas ───────────────
            {
                "id": "S2P20",
                "type": "dialogue",
                "bg": "background/scenebg_baron.png",

                "chars": {
                    "baron": {
                        "side": "right",
                        "expression": "laugh",
                        "flip": False,
                    },
                },
                "lines": [
                    ("baron", "HAHAHA! Kahit ano pa man yang gagawin mo, walang makakapagpa-walang bisa ng sumpang ginawa ko! Kailangan muna nilang maalala ang mga bagay na nakakapagpasaya sa kanila upang mawala ang sumpa!"),
                ],
            },
        # ── Scene 2, Panel 21 - Baron Disappears ───────────────
            {
                "id": "S2P21",
                "type": "scene",
                "bg": "background/scenebg_baron.png",
                "shake": True,   # camera shake on arrival (S2P20 -> S2P21)
                "smoke": True,   # smoke rises from the bottom of the screen

                "chars": {
                    "baron": {
                        "side": "center",
                        "expression": "explosion",
                        "flip": False,
                    },
                },
            },
        # ── Scene 2, Panel 22 - Lucas blocks the attack ───────────────
            {
                "id": "S2P22",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
    
                "chars": {
                    "lucas": {
                        "side": "left",
                        "expression": "defense",
                        "flip": True,
                    },
                },
                "lines": [
                    ("lucas", "!!!"),
                ],
            },
        # ── Scene 2, Panel 23 - Lola is confused ───────────────
            {
                "id": "S2P23",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
                "dim_inactive": False,
    
                "chars": {
                    "lucas": {
                        "side": "right",
                        "expression": "concerned",
                        "flip": False,
                    },
                    "lola": {
                        "side": "left",
                        "expression": "tired",
                    },
                },
                "lines": [
                    ("lucas", "Lola, isang ispiritung itim ang naglagay nang sumpa sa ating bayan, kailangan nating maalala ang lahat upang mawala ang sumpa!"),
                ],
            },
        # ── Scene 2, Panel 24 - Lola is confused ───────────────
            {
                "id": "S2P24",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
                "dim_inactive": False,
    
                "chars": {
                    "lucas": {
                        "side": "right",
                        "expression": "waters",
                        "flip": False,
                    },
                    "lola": {
                        "side": "left",
                        "expression": "tired",
                    },
                },
                "lines": [
                    ("lucas", "Tignan nyo po, nandito pa ang mga kagamitan nyo sa pagtatanim, naaalala nyo pa po ba ang mga ito?"),
                ],
            },
        # ── Scene 2, Panel 25 - Lola is confused ───────────────
            {
                "id": "S2P25",
                "type": "scene",
                "bg": "background/scenebg_default.png",
                "dim_inactive": False,
    
                "chars": {
                    "lola": {
                        "side": "center",
                        "expression": "tired",
                    },
                },
            },
        # ── transition ───────
            {
                "id": "TRANSITION_1",
                "type": "transition",
            },
        # ── Scene 2, Panel 26 - Lola is confused ───────────────
            {
                "id": "S2P26",
                "type": "scene",
                "bg": "background/Lucas-baby.jpg",
            },
        # ── Scene 2, Panel 27 - Lola is remembering something ───────────────
            {
                "id": "S2P27",
                "type": "dialogue",
                "bg": "background/Lucas-baby.jpg",

                "lines": [
                    ("lola", "Lu..."),
                ],
            },
        # ── Scene 2, Panel 28 - Lola remembered Lucas ───────────────
            {
                "id": "S2P28",
                "type": "dialogue",
                "bg": "background/Lucas-baby.jpg",

                "lines": [
                    ("lola", "Lu..cas?"),
                ],
            },
        # ── Scene 2, Panel 29 - Lola is shocked to remember Lucas ───────────────
            {
                "id": "S2P29",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
                "dim_inactive": False,
    
                "chars": {
                    "lucas": {
                        "side": "right",
                        "expression": "waters",
                        "flip": False,
                    },
                    "lola": {
                        "side": "left",
                        "expression": "shocked",
                    },
                },
                "lines": [
                    ("lola", "Lucas?! Apo? Ikaw ba yan?"),
                ],
            },
        # ── Scene 2, Panel 30 - Lola is delighted ───────────────
            {
                "id": "S2P30",
                "type": "dialogue",
                "bg": "background/scenebg_default.png",
                "dim_inactive": False,
    
                "chars": {
                    "lucas": {
                        "side": "right",
                        "expression": "thumbs",
                        "flip": False,
                    },
                    "lola": {
                        "side": "left",
                        "expression": "celebrates",
                    },
                },
                "lines": [
                    ("lola", "Ikaw nga Apo!"),
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
