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
            "logo": "logos/chapter2.png",
        },

        # ── Panel 1 — Kapitan Ernesto has lost his memories ────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Paano ako napunta dito? Wala akong naaalala sa mga nangyari sa nakalipas na ilang araw."),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Kapitan Ernesto, magandang araw! Nais ko po sanang makahingi ng tulong sa inyo."),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Kapitan? Tulong? Anong pinagsasabi mo bata? At tsaka, sino ka ba?"),
            ],
        },
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "shocked", "flip": False}},
            "lines": [
                ("lola", "Kapitan Ernesto! Hindi mo rin ba maalala ang mga nangyari sa nakalipas na ilang araw?"),
            ],
        },
        {
            "id":    "S1P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Hindi ko maalala ang mga nangyari sa akin sa mga nakalipas na araw. Hindi ko rin matandaan ang batang ito! Tsaka Lola Maria, bakit mo ako tinatawag na Kapitan?"),
            ],
        },
        {
            "id":    "S1P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "shocked", "flip": False}},
            "lines": [
                ("lola", "Kapitan Ernesto! Ikaw ang namumuno at punong tagappagpatupad ng batas sa ating baranggay? Hindi mo ba naaalala?"),
            ],
        },
        {
            "id":    "S1P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "wrong", "flip": True}},
            "lines": [
                ("lucas", "Sigurado akong kagagawan na naman ito ni Baron lola. Nais niyang sirain ang ating kaalaman at mga alaala. Kailangan nating tulungan si Kapitan Ernesto na maibalik ang kanyang mga alaala."),
            ],
        },
        {
            "id":    "S1P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Baron? Ano na naman ang ginawa ni Baron sa baryo natin? Bakit ko naaalala ang pangalan niya? Ngunit ang mga nangyari sa nakalipas na ilang araw ay parang isang panaginip lamang. Hindi ko maalala ang mga nangyari sa baryo natin."),
            ],
        },
        {
            "id":    "S1P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Ipapaliwanag ko po sa inyo mamaya kapitan. Sa ngayon, kailangan muna nating malaman ang pinaka mahalagang alaala na inyong matatandaan? Maaaring ito ay galing sa inyong kabataan, o pagkain na paborito nyong kainin lagi."),
            ],
        },
        {
            "id":    "S1P10",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Katulad ng sa akin kapitan. Ang paborito kong pagkain ay ang Petchay Soup na laging inihahanda sa akin ng aking ina nuong bata pa ako. Nang matikman ko ito, naalala ko na ang mga panyayari sa nakalipas na araw."),
            ],
        },
        {
            "id":    "S1P11",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "May paborito akong pagkain na inihahanda ng aking ina nuon bata pa ako. Ngunit hindi ko maalala kung ano ito. Ang naaalala ko lang ay ang pangunahing sangkap nito na Monggo."),
            ],
        },
        {
            "id":    "S1P12",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Kung ganon simulan natin sa pagtatanim ng Monggo upang maluto at maibalik natin ang iyong mga alala kapitan."),
            ],
        },
        {
            "id":    "S1P13",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "HAHAHAHAH! Monggo?! Kahit gaano pa kadami ang itanim nyo, hindi nito ibabalik ang mga alaala ng Kapitan! Binura ko na ang inyong kaalaman sa pagtatanim ng anumang uri ng halaman."),
            ],
        },
        {
            "id":    "S1P14",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Tumigil ka Baron! Hindi mo kami mapipigilang tulungan si kapitan Ernesto na maibalik ang kanyang mga alaala!"),
            ],
        },
        {
            "id":    "S1P15",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "HAHAHAHAH! Sige! Magaksaya ka ng panahon sa iyong kahibangan! Hindi mo maibabalik ang mga alaala ng Kapitan Ernesto! HAHAHAHAHA!"),
            ],
        },
        {
            "id": "S1P16",
            "type": "scene",
            "bg": "background/scenebg_baron.png",
            "shake": True,   # camera shake on arrival (S1P15 -> S1P16)
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
            "id": "S1P17",
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
        {
            "id":    "S1P18",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Walang sino man ang makakapigil sa akin na tulungan si Kapitan Ernesto na maibalik ang kanyang mga alaala! Kaya't simulan na natin ang pagtatanim ng Monggo!"),
            ],
        },

        # Timeline: Day 1 begins in the next scene as planting starts.
        {
            "id":   "day1_fade",
            "type": "transition",
        },
        {
            "id":    "S2P19",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Ano ang una nating gagawin sa pagtatanim ng Monggo?"),
                ("kapitan", "Ang tanging naaalala ko lamang ay ang mga nararapat na kagamitan sa pagtatanim ng Monggo. Ngunit hindi ko maalala kung paano ito gagawin."),
            ],
        },
        {
            "id":    "S2P20",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Eto po kapitan ang mga buto ng monggo."),
            ],
        },

        # ── Panel 21 — Tool-choice setup ──
        {
            "id":    "S2P21",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Buto lang ito, Lucas. Parang walang kabuluhan. Paano natin ito ibabaon?"),
            ],
        },
        {
            "id":    "S2P22",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Kailangan po muna nating pausbungin ang maliit na halaman mula buto ng monggo. Paragawin ito ibabad muna natin sa tubig ang mga buto ng monggo sa loob ng tatlong oras. Saka ilipat sa planggana na may malinis na tela."),
                ("lucas", "Tatakpan naman natin ito ng isa pang malinis na tela at plato sa ibabaw. Ilagay natin sa lugar na may sapat na liwanag at hindi direktang maarawan. Pagkatapos ng tatlong araw, makikita natin ang mga buto ng monggo na unti-unting sumisibol."),
            ],
        },
        # Timeline: Day 4 begins in the next scene, after three days of sprouting.
        {
            "id":   "day4_fade",
            "type": "transition",
        },
        {
            "id":    "S2P23",
            "type":  "dialogue",
            "day":   4,
            "bg":    "background/MonggoSproutbg.jpg",
            "lines": [
                ("lucas", "Tatlong araw na ang nakalipas kapitan."),
                ("lucas", "At mukhang sumisibol na ang mga buto ng monggo. Ngayon ay ililipat natin ito sa paso na may lupa para tuluyang tumubo ang mga punla."),
            ],
        },
        {
            "id":    "S2P24",
            "type":  "dialogue",
            "bg":    "background/MonggoSproutbg.jpg",
            "lines": [
                ("lucas", "May dalawang kagamitan na maaari nating gamitin para mag hukay ng butas sa lupang tataniman para sa mga buto ng monggo."),
            ],
        },
        {
            "id":    "S2P25",
            "type":  "dialogue",
            "day":   4,
            "bg":    "background/MonggoSproutbg.jpg",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Sa palagay ko dapat maliit na butas lamang ang ating gagamitin upang hindi maibaon ng malalim ang mga buto."),
            ],
        },
         # ── Panel 26 - choices ───────────────
        {
            "id":            "S2P26",
            "type":          "choice",
            "bg":            "background/MonggoSproutbg.jpg",
            "question":       "Alin ang tamang kagamitan para gumawa ng maliliit na butas para sa buto ng Monggo?",
            "retry_question": "Sandali... pakiramdam ko masyadong malalim ang hukay nito para sa ddirektang pagtatanim.",
            "choices": [
                # These cards are finished art -- own frame and baked-in
                # "DULO"/"ASAROL" text -- so no engine panel or label.
                {"img": "buttons/choice_trowel.png", "label": "", "frame": False},
                {"img": "buttons/choice_hoe.png",    "label": "", "frame": False},
            ],
            "correct": 0,
        },
    # ── Panel 27 - Feedback Correct - Lucas Thumbs up ───────────────
        {
            "id":          "S2P27_right_1",
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
                ("lucas", "Tama! Dulo ang tamang sagot! Mababaw at maingat ang hukay nito, kaya nararapat ito para sa direktang pagtatanim."),
            ],
        },
    # ── Panel 28 - Feedback: Correct — Lola thumbs up ───────────────
        {
            "id":         "S2P28_right_2",
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

    # ── Panel 29 ── Feedback: Wrong — Lucas worried ───────────────────
        {
            "id":          "S2P29_wrong_1",
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
                ("lucas", "Sandali... pakiramdam ko masyadong malalim ang hukay nito para sa direktang pagtatanim."),
            ],
        },
    # ── Panel 30 ── Feedback: Wrong — Kapitan warns ───────────────────
    {
        "id":              "S2P30_wrong_2",
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
    # Timeline: Day 5 begins in the next scene, one day after transplanting.
        {
            "id":   "day5_fade",
            "type": "transition",
        },
        {
            "id":    "S2P31",
            "type":  "dialogue",
            "day":   5,
            "bg":    "background/Monggobg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Kailangan nating palaguin ang mga monggo ngayong nailipat na natin ito mula sa paso patungo sa lupa. Ano sa tingin nyo ang dapat nating gawin kapitan?"),
            ],
        },
        {
            "id":    "S2P32",
            "type":  "dialogue",
            "bg":    "background/Monggobg.jpg",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "kailangan nating diligan ang mga ito ng malumanay at sapat na tubig."),
            ],
        },
        # ── Panel 33 - Card Scan Event ──────────────────────
            # TEMPORARY stand-in for the real card scan. The instruction art is
            # drawn on top of the default scene background and the player picks
            # the blue square. This slide type is replaced once the camera-based
            # cardscan feature is wired in.
        {
            "id": "S2P33",
            "type": "action_challenge",
            "bg": "background/scenebg_default.png",
            "overlay": "background/Action_Challenge-Water.png",
            "dim_inactive": False,
        },
        {
            "id": "S2P34",
            "type": "scene",
            "bg": "background/baronmonggobgnew.jpg",
            "shake": True,   # camera shake on arrival (S2P33 -> S2P34)
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
            "id":    "S2P35",
            "type":  "dialogue",
            "bg":    "background/baronmonggobgnew.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Mga hangal! Ginagalit nyo ako sa mga pinagagagawa nyo! Akala nyo ba kaya nyo akong talunin sa kakarampot na kaalamang naaalala ninyo?"),
                ("baron", "Matitikman nyo ngayon ang lupit ng kapangyarihan ko!"),
            ],
        },
        # Timeline: Still Day 5; the Baron summons pests in the next scene.
        {
            "id":   "day5_fade",
            "type": "transition",
        },
        {
            "id": "S2P36",
            "type": "scene",
            "day": 5,
            "bg": "background/baronmonggoswarmed.jpg",
            "shake": True,   # camera shake on arrival (S2P35 -> S2P36)
        },
        {
            "id":    "S2P37",
            "type":  "dialogue",
            "bg":    "background/baronmonggoswarmed.jpg",
            "dark":  True,
            "chars": {"lola": {"side": "left", "expression": "shocked", "flip": False}},
            "lines": [
                ("lola", "Naku po! Ang daming mga peste sa ating taniman!"),
                ("lola", "Paano natin to mapipigilan?"),
            ],
        },
        {
            "id":    "S2P38",
            "type":  "dialogue",
            "bg":    "background/baronmonggoswarmed.jpg",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Hindi maaari ito kapitan. Kailangan nating maagapan agad ang mga peste upang ating maprotektahan ang mga halaman."),
            ],
        },
        {
            "id":    "S2P39",
            "type":  "dialogue",
            "bg":    "background/baronmonggoswarmed.jpg",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Kailangan nating puksain ang mga ito!"),
                ("kapitan", "Biilis Lucas kunin mo ang Natural na Pestesidyo upang maprotektahan ang mga halaman!"),
            ],
        },
        # ── Panel 40 - Card Scan Event ──────────────────────
            # TEMPORARY stand-in for the real card scan. The instruction art is
            # drawn on top of the default scene background and the player picks
            # the blue square. This slide type is replaced once the camera-based
            # cardscan feature is wired in.
        {
            "id": "S2P40",
            "type": "action_challenge",
            "bg": "background/baronmonggoswarmed.jpg",
            "overlay": "naturalpesticidecard.png",
            "dim_inactive": False,
        },
        {
            "id":    "S2P41",
            "type":  "dialogue",
            "bg":    "background/baronmonggoswarmed.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Magaling! nagawa nating pigilan ang mga peste sa ating taniman!"),
                ("lucas", "Unti unti na silang nagsisialisan at nawala sa ating taniman!"),
            ],
        },
        {
            "id":    "S2P42",
            "type":  "dialogue",
            "bg":    "background/baronmonggobgnew.jpg",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Walang maidudulot na maganda ang ginawa mo Baron! Masmabuti pang itigil mo na ang mga panggugulo mo sa baryo natin!"),
            ],
        },
        {
            "id":    "S2P43",
            "type":  "dialogue",
            "bg":    "background/baronmonggobgnew.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Mga hangal! Naisahan nyo ako ngayon ngunit hindi nyo na ito magagawa pa sa susunod na pagbabalik ko!")
            ],
        },
        {
            "id": "S2P44",
            "type": "scene",
            "bg": "background/baronmonggobgnew.jpg",
            "shake": True,   # camera shake on arrival (S2P43 -> S2P44)
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
            "id":    "S2P45",
            "type":  "dialogue",
            "bg":    "background/Monggobg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Magaling! nagawa nating maitaboy si Baron sa ating taniman!"),
                ("lucas", "Ngayon ay maaari na nating alagaan ang mga halaman ng Monggo at hintayin ang mga ito na tuluyang sumibol!"),
            ],
        },
        {
            "id":    "S2P46",
            "type":  "dialogue",
            "bg":    "background/Monggobg.jpg",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Tama ka Lucas! Ngayon ay maaari na nating hintayin ang mga halaman ng Monggo na tuluyang sumibol!"),
            ],
        },
        # Timeline: Day 10 begins in the next scene after five days of watering and growth.
        {
            "id":   "day5_fade",
            "type": "transition",
        },
        {
            "id": "S2P47",
            "type": "narration_overlay",
            "day": 10,
            "bg": "background/scenebg_night.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",

            "narration": (
                "Limang araw pang dumaan, at  "
                "araw araw dinidiligan ni lucas ang mga halaman "
                "Kinaumagahan napansin nyang unti-unti "
                "na itong lumalago at lumalaki."
            ),
        },
        {
            "id":    "S2P48",
            "type":  "dialogue",
            "bg":    "background/Monggobg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Mahusay unti unti nang lumalago ang mga pananim!"),
            ],
        },
         # Timeline: Day 15 begins in the next scene, five days later.
        {
            "id":   "day5_fade",
            "type": "transition",
        },
        {
            "id": "S2P49",
            "type": "scene",
            "day": 15,
            "bg": "background/lucasmonggobg.jpg",
        },
         # Timeline: Day 30 begins in the next scene, fifteen days later.
        {
            "id":   "day30_fade",
            "type": "transition",
        },
        {
            "id":    "S3P50",
            "type":  "dialogue",
            "day":   30,
            "bg":    "background/baronmonggobgnew.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Hehehe... Matitikman nyo ngayon ang aking ganti, buburahin ko ang alala ni Lola Maria kung paano gumawa ng Ginisang Monggo!")
            ],
        },
        {
            "id": "S3P51",
            "type": "scene",
            "bg": "background/baronmonggobgnew.jpg",
            "shake": True,   # camera shake on arrival (S3P50 -> S3P51)
            "smoke": True,   # smoke rises from the bottom of the screen

            "chars": {
                "baron": {
                    "side": "center",
                    "expression": "explosion",
                    "flip": False,
                },
            },
        },
        # Timeline: Day 65 begins in the next scene at harvest.
        {
            "id":   "day65_fade",
            "type": "transition",
        },
        {
            "id":    "S3P52",
            "type":  "dialogue",
            "day":   65,
            "bg":    "background/monggobgnew.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Magaling! lumago na ang ating mga pananim!"),
                ("lucas", "Ngayon ay maaari na natin itong anihin!"),
                ("lucas", "Ihanda na natin ang mga gagamitin natin"),
            ],
        },
         {
            "id": "S3P53",
            "type": "action_challenge",
            "bg": "background/monggobgnew.jpg",
            "overlay": "harvestcardscan.png",
            "dim_inactive": False,
        },
        {
            "id":    "S3P54",
            "type":  "dialogue",
            "bg":    "background/monggobgnew.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Naani na namin ang lahat ng monggo lola!"),
                ("lucas", "Puwede na nating lutuin ang Ginisang Monggo at matulungang ibalik ang alala ni Kapitan Ernesto!"),
            ],
        },
        {
            "id":    "S3P55",
            "type":  "dialogue",
            "bg":    "background/monggobgnew.jpg",
            "chars": {"lola": {"side": "left", "expression": "shocked", "flip": False}},
            "lines": [
                ("lola", "Apo! Meron akong problema. Hindi ko maalala ang tamang paraan ng pagluluto ng Ginisang Monggo!"),
                ("lola", "Nagkagulo-gulo ang aking mga listahan ng sangkap."),
                ("lola", "Kailangan ko ng tulong para maiayos ang mga ito ngunit hindi ko ito maalala."),
            ],
        },
        {
            "id":    "S3P56",
            "type":  "dialogue",
            "bg":    "background/monggobgnew.jpg",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "lines": [
                ("lucas", "Naku! Meron na namang sumpang ginawa si baron."),
                ("lucas", "Dapat nating tulungan si Lola Maria upang maalala nya ang mga ito."),
            ],
        },
        {
            "id":    "S3P57",
            "type":  "dialogue",
            "bg":    "background/monggobgnew.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Handa na ba kayo?"),
            ],
        },
        {
            "id": "memory_challenge",
            "type": "memory_game",
            "bg": "background/monggobgnew.jpg",
        },
        {
            "id":    "S3P58",
            "type":  "dialogue",
            "day":   65,
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "celebrates", "flip": False}},
            "lines": [
                ("lola", "Magaling! Naaalala ko na ulit paano gawin ang Ginisang Monggo! Hali na kayo at gawin na natin ito!!"),
            ],
        },
        # Timeline: Still Day 65 as Kapitan's memories return in the next scene.
        {
            "id":   "day65_fade",
            "type": "transition",
        },
        {
            "id":    "S3P59",
            "type":  "dialogue",
            "day":   65,
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Naalala ko na ang lahat! Ako nga talaga ang kapitan ng ating baryo. Salamat sa tulong nyo Lucas at Lola maria!"),
                ("kapitan", "Ngayon kailangan na nating tulungan ang iba pa nating mga kasama."),
            ],
        },
        {
            "id":    "S3P60",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Puntahan naman natin si Chef Pablo"),
            ],
        },
    ],
}
