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
            "day":   0,
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
        # ── Scene 2, Panel 31 - Lucas is delighted ───────────────
            {
                "id": "S2P31",
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
                    ("lucas", "Ako nga po Lola! Masaya po ako at naaalala nyo na po ako"),
                ],
            },
        # ── Scene 2, Panel 32 - Lola asked a question ───────────────
                {
                    "id": "S2P32",
                    "type": "dialogue",
                    "bg": "background/scenebg_default.png",
                    "dim_inactive": False,
        
                    "chars": {
                        "lucas": {
                            "side": "right",
                            "expression": "default",
                            "flip": False,
                        },
                        "lola": {
                            "side": "left",
                            "expression": "default",
                        },
                    },
                    "lines": [
                        ("lola", "Bakit ka naparito apo? Ano ba ang nangyayari?"),
                    ],
                },
        # ── Scene 2, Panel 33 - Lucas answered ───────────────
                {
                    "id": "S2P33",
                    "type": "dialogue",
                    "bg": "background/scenebg_default.png",
                    "dim_inactive": False,
        
                    "chars": {
                        "lucas": {
                            "side": "right",
                            "expression": "talking",
                            "flip": False,
                        },
                        "lola": {
                            "side": "left",
                            "expression": "default",
                        },
                    },
                    "lines": [
                        ("lucas", "Isang masamang ispiritu po ang naglagay ng sumpa sa ating bayan. Upang mapawalang bisa ang sumpa, kailangan nating maalala ang lahat ng bagay na nakakapagpasaya sa atin."),
                    ],
                },
        # ── Scene 2, Panel 34 - Lucas answered ───────────────
                {
                    "id": "S2P34",
                    "type": "dialogue",
                    "bg": "background/scenebg_default.png",
                    "dim_inactive": False,
        
                    "chars": {
                        "lucas": {
                            "side": "right",
                            "expression": "talking",
                            "flip": False,
                        },
                        "lola": {
                            "side": "left",
                            "expression": "default",
                        },
                    },
                    "lines": [
                        ("lucas", "Naaalala nyo po ba kung ano ang nakakapagpasaya sa inyo?"),
                    ],
                },
        # ── Scene 2, Panel 35 - Lola explains to lucas ───────────────
                {
                    "id": "S2P35",
                    "type": "dialogue",
                    "bg": "background/scenebg_default.png",
                    "dim_inactive": False,
        
                    "chars": {
                        "lola": {
                            "side": "left",
                            "expression": "tired",
                        },
                    },
                    "lines": [
                        ("lola", "Ang alam ko, masaya akong magtanim ng aking mga tanim, ngunit nalimutan ko na kung paano. Bakit hindi ko ito maalala?"),
                    ],
                },
        # ── Scene 2, Panel 36 - Lucas answered ───────────────
                {
                    "id": "S2P36",
                    "type": "dialogue",
                    "bg": "background/scenebg_default.png",
                    "dim_inactive": False,
        
                    "chars": {
                        "lucas": {
                            "side": "right",
                            "expression": "talking",
                            "flip": False,
                        },
                        "lola": {
                            "side": "left",
                            "expression": "default",
                        },
                    },
                    "lines": [
                        ("lucas", "Wag kayong mag-alala Lola, tutulungan ko po kayo kasama ang aking mga kaibigan."),
                    ],
                },
        # ── Scene 2, Panel 38 - Lucas answered ───────────────
                {
                    "id": "S2P38",
                    "type": "dialogue",
                    "bg": "background/scenebg_default.png",
                    "dim_inactive": False,
        
                    "chars": {
                        "lucas": {
                            "side": "right",
                            "expression": "talking",
                            "flip": False,
                        },
                        "lola": {
                            "side": "left",
                            "expression": "default",
                            "dim_inactive": True,
                        },
                    },
                    "lines": [
                        ("lucas", "Maaari nyo ba kaming tulungan ng aking lola?"),
                    ],
                },
        # ── Scene 2, Panel 39 - Lucas answered ───────────────
                {
                    "id": "S2P39",
                    "type": "dialogue",
                    "bg": "background/scenebg_default.png",
                    "dim_inactive": False,
        
                    "chars": {
                        "lucas": {
                            "side": "right",
                            "expression": "talking",
                            "flip": False,
                        },
                        "lola": {
                            "side": "left",
                            "expression": "default",
                            "dim_inactive": True,
                        },
                    },
                    "lines": [
                        ("lucas", "Magaling!"),
                    ],
                },
        # ── Scene 2, Panel 40 - Lucas answered ───────────────
            {
                "id": "S2P40",
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
                        "expression": "default",
                    },
                },
                "lines": [
                    ("lucas", "Simulan natin sa pagtukoy ng tawag sa gamit para gumawa ng hukay, kung saan ilalagay ang binhi ng pechay. "),
                ],
            },
        # ── Scene 2, Panel 41 - choices ───────────────
            {
                "id":            "S2P41",
                "type":          "choice",
                "bg":            "background/scenebg_planter.png",
                "question":       "Alin ang tamang kagamitan para gumawa ng maliliit na butas para sa buto ng Petchay?",
                "retry_question": "Sandali... pakiramdam ko masyadong malalim ang hukay nito para sa direct planting.",
                "choices": [
                    # These cards are finished art -- own frame and baked-in
                    # "DULO"/"ASAROL" text -- so no engine panel or label.
                    {"img": "buttons/choice_trowel.png", "label": "", "frame": False},
                    {"img": "buttons/choice_hoe.png",    "label": "", "frame": False},
                ],
                "correct": 0,
            },
        # ── Scene 2, Panel 42 - Feedback Correct - Lucas Thumbs up ───────────────
            {
                "id":          "S2P42_right_1",
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
                    ("lucas", "Tama! Dulo ang tamang sagot! Mababaw at maingat ang hukay nito, kaya safe ito para sa direct planting."),
                ],
            },              
        # ── Scene 2, Panel 43 -Feedback: Correct — Lola thumbs up ───────────────
            {
                "id":         "S2P43_right_2",
                "type":       "feedback",
                "if_correct": True,
                "random_pick": True,
                "bg":         "background/scenebg_right.png",
                "chars":           {
                        "lola": {
                            "side": "left",
                            "expression": "thumbs",
                            "flip": True,
                        }
                    },
                "lines": [
                    ("lola", "Magaling, apo! Kapag mababaw lang ang itatanim na buto, sapat na ang Dulo. Hindi natin laging kailangan ng malakas na kasangkapan."),
                ],
            },

        # ── Scene 2, Panel 44 ── Feedback: Wrong — Lucas worried ───────────────────
            {
                "id":          "S2P44_wrong_1",
                "type":        "feedback",
                "if_correct":  False,
                "random_pick": True,
                "retry_to_choice": True,
                "bg":          "background/scenebg_wrong.png",
                "chars":       {
                    "lucas": {
                        "side": "right",
                        "expression": "wrong",
                        "flip": False,
                    }
                },
                "lines": [
                    ("lucas", "Sandali... pakiramdam ko masyadong malalim ang hukay nito para sa direct planting."),
                ],
            }, 
        # ── Scene 2, Panel 45 ── Feedback: Wrong — Kapitan warns ───────────────────
        {
            "id":              "S2P45_wrong_2",
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
    # ── Scene 2, Panel 46 - Lola explains to lucas ───────────────
        {
            "id": "S2P46",
            "type": "dialogue",
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,

            "chars": {
                "lola": {
                    "side": "left",
                    "expression": "sad",
                },
            },
            "lines": [
                ("lola", "Natanim na natin sila… pero mukhang sobrang tuyo ang lupa, apo."),
            ],
        },    
    # ── Scene 2, Panel 47 - Lucas explains to lola ───────────────
        {
            "id": "S2P47",
            "type": "dialogue",
            "bg": "background/scenebg_planter.png",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "waters",
                    "flip": True,
                },
            },
            "lines": [
                ("lucas", "Kailangan nila ng tubig para lumusog at tumubo sila Lola. Kaya gagamit tayo ng regadera.."),
            ],
        },
    # ── Scene 2, Panel 48 - Card Scan Event ──────────────────────
    # TEMPORARY stand-in for the real card scan. The instruction art is
    # drawn on top of the default scene background and the player picks
    # the blue square. This slide type is replaced once the camera-based
    # cardscan feature is wired in.
            {
                "id": "S2P48",
                "type": "action_challenge",
                "bg": "background/scenebg_default.png",
                "overlay": "background/Action_Challenge-Water.png",
                "dim_inactive": False,
            },
    # ── Scene 2, Panel 49 - Lucas explains to lola ───────────────
            {
                "id": "S2P49",
                "type": "dialogue",
                "bg": "background/scenebg_wet.jpg",
                "dim_inactive": False,
    
                "chars": {
                    "lucas": {
                        "side": "left",
                        "expression": "waters",
                        "flip": True,
                    },
                },
                "lines": [
                    ("lucas", "Ayan na, Lola. Nadiligan na natin ng unang tubig. Ang natitira na lang nating gawin ay maghintay."),
                ],
            },
    # ── Scene 2, Panel 50 - Narration: the days that followed ───
    # A time-skip beat, so it is told rather than spoken: the
    # passage is written on a wooden board instead of a dialogue
    # box, sized up so kids can read it comfortably.
            {
                "id": "S2P50",
                "type": "narration_overlay",
                "bg": "background/scenebg_night.jpg",
                "dim_inactive": False,
                "overlay": "woodbg.png",

                "narration": (
                    "Araw-araw, dinidiligan ni Lucas ang tanim. "
                    "Banayad na patak lang, tulad ng pangako niya "
                    "kay Lola. Sa ikalimang araw, may sumilip na "
                    "munting berdeng dahon sa ibabaw ng lupa"
                ),
            },
    # ── Scene 2, Panel 51 - Lucas is excited to show Lola the Petchay ───────────────
            {
                "id": "S2P51",
                "type": "dialogue",
                "day": 5,
                "bg": "background/lucas-waters-plant-scene.jpg",
                "dim_inactive": False,
                # Lucas is painted into the left of this background
                # rather than placed as a sprite, so the automatic
                # layout has nothing to measure and would centre the
                # box over him. Keep the text clear on the right.
                "dbox_side": "right",
                "lines": [
                    ("lucas", "Sa wakas! Tingnan mo ito, Lola. Tumubo na ang Pechay natin."),
                ],
            },
    # ── Scene 2, Panel 52 - Baron arrives and mocks them ───────────────
            {
                "id": "S2P52",
                "type": "dialogue",
                "bg": "background/baron-right-scene.jpg",
                "dim_inactive": False,
    
                "chars": {
                    "baron": {
                        "side": "left",
                        "expression": "waters",
                        "flip": True,
                    },
                },
                "lines": [
                    ("baron", "Hah! Nagawa niyong pausbongin ang halaman. Kung walang sikat ng araw, hindi na ito tutubo ulit! Tikman n'yo ang dilim mga Pechay!"),
                ],
            },
    # ── Scene 2, Panel 53 - Baron arrives and mocks them ───────────────
            {
                "id": "S2P53",
                "type": "dialogue",
                "bg": "background/baron-right-scene2.jpg",
                "dim_inactive": False,
    
                "chars": {
                    "lucas": {
                        "side": "left",
                        "expression": "wrong",
                        "flip": True,
                    },
                },
                "lines": [
                    ("lucas", "Lola, tingnan mo 'yung payong, tinatakpan ang araw! Gawa 'yan ng Baron. Dapat ba natin itong alisin?"),
                ],
            },
    # ── Scene 2, Panel 54 - Baron arrives and mocks them ───────────────
            {
                "id": "S2P54",
                "type": "dialogue",
                "bg": "background/baron-right-scene2.jpg",
                "dim_inactive": False,
    
                "chars": {
                    "lola": {
                        "side": "left",
                        "expression": "sad",
                        "flip": False,
                    },
                },
                "lines": [
                    ("baron", "Parang... parang gusto kong sabihing oo. May naaalala akong dahilan kung bakit."),
                ],
            },
    # ── Scene 2, Panel 55 - choices ───────────────
        {
            "id":            "S2P55",
            "type":          "choice",
            "bg":            "background/baron-right-scene2.jpg",
            "question":       "Gumagamit ang mga halaman ng sikat ng araw para gumawa ng sariling pagkain sa loob ng kanilang mga dahon (photosynthesis). Dapat bang manatili o alisin ang payong?",
            "retry_question": "Nagkamali ata tayo ng ating piniling sagot. Basahin nating maigi at intindihin ang tanong bago pumili ng sagot.",
            "choices": [
                {"img": "buttons/choice1.png", "frame": False},
                {"img": "buttons/choice2.png", "frame": False},
            ],
            "correct": 0,
        },
    # ── Scene 2, Panel 56 - Feedback Correct - Lucas Thumbs up ───────────────
        {
            "id":          "S2P56_right_1",
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
                ("lucas", "Tama! Kailangan ng Pechay ng liwanag para gumawa ng sariling pagkain sa loob ng dahon. Kaya dapat alisin ang payong upang makapasok ang sikat ng araw sa mga dahon ng Pechay."),
            ],
        },              
    # ── Scene 2, Panel 57 -Feedback: Correct — Lola thumbs up ───────────────
        {
            "id":         "S2P57_right_2",
            "type":       "feedback",
            "if_correct": True,
            "random_pick": True,
            "bg":         "background/scenebg_right.png",
            "chars":           {
                    "lola": {
                        "side": "left",
                        "expression": "thumbs",
                        "flip": True,
                    }
                },
            "lines": [
                ("lola", "Oo nga, apo! Tila naaalala ko na rin ito. Kailangan nila ng araw, hindi dilim."),
            ],
        },

    # ── Scene 2, Panel 58 ── Feedback: Wrong — Lucas worried ───────────────────
        {
            "id":          "S2P58_wrong_1",
            "type":        "feedback",
            "if_correct":  False,
            "random_pick": True,
            "retry_to_choice": True,
            "bg":          "background/scenebg_wrong.png",
            "chars":       {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Huwag! Kung mananatili sa dilim ang Pechay, hindi sila lalago. Subukan nating muli."),
            ],
        }, 
    # ── Scene 2, Panel 59 ── Feedback: Wrong — Kapitan warns ───────────────────
        {
            "id":              "S2P59_wrong_2",
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
                ("baron", "HA! Tamang-tama! Manatili sila sa dilim!"),
            ],
        },
    # ── Scene 2, Panel 60 - Lucas explains to us ───────────────
        {
            "id": "S2P60",
            "type": "dialogue",
            "bg": "background/petchaybg.jpg",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "talking",
                    "flip": True,
                },
            },
            "lines": [
                ("lucas", "Phew! Buti nalang at naalala nyo lola ang tungkulin ng araw sa mga halaman!"),
            ],
        },
    # ── Scene 2, Panel 61 - Lucas explains to us ───────────────
        {
            "id": "S2P61",
            "type": "dialogue",
            "bg": "background/petchaybg.jpg",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "talking",
                    "flip": True,
                },
            },
            "lines": [
                ("lucas", "Ang araw ang isa sa mga nag bibigay ng sustansya sa mga halaman para lumago ang mga ito."),
            ],
        },
    # ── Scene 2, Panel 62 - Lucas explains to us ───────────────
        {
            "id": "S2P62",
            "type": "dialogue",
            "bg": "background/petchaybg.jpg",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "talking",
                    "flip": True,
                },
            },
            "lines": [
                ("lucas", "Ginagamit nila ang araw para maging enerhiya upang makalikha sila nang sarili nilang pagkain."),
            ],
        },
    # ── Scene 2, Panel 63 - Lucas explains to us ───────────────
        {
            "id": "S2P63",
            "type": "dialogue",
            "bg": "background/petchaybg.jpg",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "talking",
                    "flip": True,
                },
            },
            "lines": [
                ("lucas", "Ito ang tinatawag na Photosynthesis. Ang proseso kung saan gumagawa ang mga halaman ng sarili nilang pagkain upang mabuhay."),
            ],
        },
    # ── Scene 2, Panel 64 - baron is angry ───────────────
        {
            "id": "S2P64",
            "type": "dialogue",
            "bg": "background/petchaybg.jpg",
            "dim_inactive": False,

            "chars": {
                "baron": {
                    "side": "left",
                    "expression": "nervous",
                    "flip": True,
                },
            },
            "lines": [
                ("baron", "Ano ang ginawa mo!? Paano mo nalamang ang araw ang nagbibigay sigla sa kanila?"),
            ],
        },
    # ── Scene 2, Panel 65 - baron is worried ───────────────
        {
            "id": "S2P65",
            "type": "dialogue",
            "bg": "background/petchaybg.jpg",
            "dim_inactive": False,

            "chars": {
                "baron": {
                    "side": "left",
                    "expression": "nervous",
                    "flip": True,
                },
            },
            "lines": [
                ("baron", "Humanda ka bata! Babalik ako para sirain ang mga pananim mo!"),
            ],
        },
    # ── Scene 2, Panel 66 - lola econgratulates lucas ───────────────
        {
            "id": "S2P66",
            "type": "dialogue",
            "bg": "background/petchaybg.jpg",
            "dim_inactive": False,

            "chars": {
                "lola": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                },
            },
            "lines": [
                ("lola", "Magaling apo, ngayon ay masigla na ang ating mga pananim!"),
            ],
        },
    # ── Scene 2, Panel 67 - Lucas explains to lola ───────────────
        {
            "id": "S2P67",
            "type": "dialogue",
            "bg": "background/petchaybg.jpg",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "default",
                    "flip": True,
                },
            },
            "lines": [
                ("lola", "Oo nga po lola. Pero nababahala po ako sa mga banta ni Baron."),
            ],
        },
    # ── Scene 2, Panel 68 - Lola assures lucas ───────────────
        {
            "id": "S2P68",
            "type": "dialogue",
            "bg": "background/petchaybg.jpg",
            "dim_inactive": False,

            "chars": {
                "lola": {
                    "side": "left",
                    "expression": "default",
                    "flip": False,
                },
            },
            "lines": [
                ("lola", "Wag kang mag-alala apo, paghahandaan natin ang mga susunod nyang gagawin."),
            ],
        },
    # ── Scene 2, Panel 69 - Narration: the days that followed ───
        {
            "id": "S2P69",
            "type": "narration_overlay",
            "bg": "background/scenebg_night.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",

            "narration": (
                "Limang araw pang dumaan, at  "
                "biglang umulan nang malakas "
                "kagabi. Kinaumagahan, basa pa at "
                "malusak ang lupa sa paligid ng taniman."
            ),
        },
    # ── Scene 2, Panel 70 - Lucas is sad ───────────────
        {
            "id": "S2P70",
            "type": "dialogue",
            "day": 10,
            "bg": "background/rainybg.jpg",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "wrong",
                    "flip": True,
                },
            },
            "lines": [
                ("lucas", "Naku po, nasira ang aming mga pananim dahil sa malakas na ulan kagabi. Ano na ang gagawin namin ngayon?"),
            ],
        },
    # ── Scene 2, Panel 70 - Lucas is talking ───────────────
        {
            "id": "S2P70",
            "type": "dialogue",
            "bg": "background/rainybg.jpg",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "talking",
                    "flip": True,
                },
            },
            "lines": [
                ("lucas", "Maari nyo ba akong tulungan na ayusin ang taniman namin ng petchay?"),
            ],
        },
    # ── Scene 2, Panel 70 - Lucas is grateful ───────────────
        {
            "id": "S2P70",
            "type": "dialogue",
            "bg": "background/rainybg.jpg",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                },
            },
            "lines": [
                ("lucas", "Magaling! Ano ang una nating gagawin?"),
            ],
        },
    # ── Scene 2, Panel 71 - choices ───────────────
        {
            "id":            "S2P71",
            "type":          "choice",
            "bg":            "background/rainybg.jpg",
            "question":       "Ano ang una nating gagawin kapag nasira ang bagong tanim natin na gulay ng malakas na ulan sa nagdaang gabi?",
            "retry_question": "Nagkamali ata tayo ng ating piniling sagot. Basahin nating maigi at intindihin ang tanong bago pumili ng sagot.",
            # These answers are full sentences, so each sits on its own
            # wooden board ("dbox") with the text wrapped inside the
            # recessed panel -- the small card art has no room for this.
            # The left one is the wrong answer.
            "choices": [
                {
                    "dbox": "woodbg.png",
                    "label": "Gumamit ng hair dryer at patuyuin ang bawat dahon nang paisa-isa gamit ang high blast ng hair dryer.",
                },
                {
                    "dbox": "woodbg.png",
                    "label": "Patubuin o padaanin agad ang naipong tubig sa pamamagitan ng paggawa ng maliliit na kanal upang maiwasan ang pagkaagnas ng mga ugat.",
                },
            ],
            "correct": 1,
        },
    # ── Scene 2, Panel 72 - Feedback Correct - Lucas Thumbs up ───────────────
        {
            "id":          "S2P72_right_1",
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
                ("lucas", "Tama ang sagot mo! Hawakan ang mga pala at humukay ng kanal! Hindi natin hahayaang mabulok ang ating mga pananim. Oras na para isalba ang mga petchay!"),
            ],
        },              
    # ── Scene 2, Panel 73 -Feedback: Correct — Lola thumbs up ───────────────
        {
            "id":         "S2P73_right_2",
            "type":       "feedback",
            "if_correct": True,
            "random_pick": True,
            "bg":         "background/scenebg_right.png",
            "chars":           {
                    "lola": {
                        "side": "left",
                        "expression": "thumbs",
                        "flip": True,
                    }
                },
            "lines": [
                ("lola", "Tama ka apo! Inililigtas nito ang mga ugat: Ang nakaimbak na tubig ay nag-aalis ng oksihina sa lupa. Kapag walang hangin, ang mga ugat ay nalulunod at mabilis na nabubulok (root rot)."),
            ],
        },

    # ── Scene 2, Panel 74 ── Feedback: Wrong — Lucas worried ───────────────────
        {
            "id":          "S2P74_wrong_1",
            "type":        "feedback",
            "if_correct":  False,
            "random_pick": True,
            "retry_to_choice": True,
            "bg":          "background/scenebg_wrong.png",
            "chars":       {
                "lucas": {
                    "side": "right",
                    "expression": "wrong",
                    "flip": False,
                }
            },
            "lines": [
                ("lucas", "Mali ang sagot mo! Seryoso ka ba sa hair dryer?! Walang 'Ctrl + Z' sa totoong buhay—magseryoso ka naman kung ayaw mong maging seaweed farm ito!"),
            ],
        }, 
    # ── Scene 2, Panel 75 ── Feedback: Wrong — Kapitan warns ───────────────────
        {
            "id":              "S2P75_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Imposible at mapanganib: Ang paggamit ng kuryente at hair dryer sa basang bukid ay magdudulot lang ng makuryenteng magsasaka, hindi tuyong lupa."),
            ],
        },
    # ── Scene 2, Panel 76 - Lucas is grateful ───────────────
        {
            "id": "S2P76",
            "type": "dialogue",
            "bg": "background/baron-right-scene.jpg",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                },
            },
            "lines": [
                ("lucas", "Magaling, nagawa nating maisalba ang ating mga tanim na petchay!"),
            ],
        },
    # ── transition ───────
            {
                "id": "TRANSITION_2",
                "type": "transition",
            },
    # ── Scene 2, Panel 77 - Lola is happy ───────────────
        {
            "id": "S2P77",
            "type": "dialogue",
            "day": 30,
            "bg": "background/Petchaybgnew.jpg",
            "dim_inactive": False,

            "chars": {
                "lola": {
                    "side": "left",
                    "expression": "default",
                    "flip": False,
                },
            },
            "lines": [
                ("lola", "Napaka talino nang inyong nagawang solusyon! Ngayon, ulitin lang natin ang proseso ng tamang pagdilig araw araw, hanggang sa tumubo at lumago ang mga petchay na ating itinanim."),
            ],
        },
    # ── Scene 2, Panel 78 - Lucas is grateful ───────────────
        {
            "id": "S2P78",
            "type": "dialogue",
            "bg": "background/Petchaybgnew.jpg",
            "dim_inactive": False,

            "chars": {
                "lucas": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                },
            },
            "lines": [
                ("lucas", "Sa wakas! Sa loob nang matagal na mga araw na ating hinintay, lumago at tumubo na ang ating mga Petchay!"),
            ],
        },
    # ── Scene 2, Panel 79 - Lola celebrates ───────────────
        {
            "id": "S2P79",
            "type": "dialogue",
            "bg": "background/Petchaybgnew.jpg",
            "dim_inactive": False,

            "chars": {
                "lola": {
                    "side": "left",
                    "expression": "celebrates",
                    "flip": False,
                },
            },
            "lines": [
                ("lola", "Ngayon ay makakakain narin ako ng petchay! Naalala ko tuloy nuong bata pa ako, paborito ko ang petchay soup!"),
            ],
        },
    # ── Scene 2, Panel 80 - Baron is angry ───────────────
        {
            "id": "S2P80",
            "type": "dialogue",
            "bg": "background/baronPetchaybgnew.jpg",
            "dim_inactive": False,

            "chars": {
                "baron": {
                    "side": "right",
                    "expression": "angry",
                    "flip": False,
                },
            },
            "lines": [
                ("baron", "Nakakainis kang bata ka! Paano mo nalalaman ang mga ito?! Humanda ka sa pagbabalik ko!"),
            ],
        },
    ],
}
