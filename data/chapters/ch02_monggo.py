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
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Kapitan? Tulong? Anong pinagsasabi mo bata? At tsaka, sino ka ba?"),
            ],
        },
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "shocked", "flip": False}},
            "lines": [
                ("lola", "Kapitan Ernesto! Hindi mo rin ba maalala ang mga nangyari sa nakalipas na ilang araw?"),
            ],
        },
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Hindi ko maalala ang mga nangyari sa akin sa mga nakalipas na araw. Hindi ko rin matandaan ang batang ito! Tsaka Lola Maria, bakit mo ako tinatawag na Kapitan?"),
            ],
        },
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "shocked", "flip": False}},
            "lines": [
                ("lola", "Kapitan Ernesto! Ikaw ang namumuno at punong tagappagpatupad ng batas sa ating baranggay? Hindi mo ba naaalala?"),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "wrong", "flip": True}},
            "lines": [
                ("lucas", "Sigurado akong kagagawan na naman ito ni Baron lola. Nais niyang sirain ang ating kaalaman at mga alaala. Kailangan nating tulungan si Kapitan Ernesto na maibalik ang kanyang mga alaala."),
            ],
        },
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Baron? Ano na naman ang ginawa ni Baron sa baryo natin? Bakit ko naaalala ang pangalan niya? Ngunit ang mga nangyari sa nakalipas na ilang araw ay parang isang panaginip lamang. Hindi ko maalala ang mga nangyari sa baryo natin."),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Ipapaliwanag ko po sa inyo mamaya kapitan. Sa ngayon, kailangan muna nating malaman ang pinaka mahalagang alaala na inyong matatandaan? Maaaring ito ay galing sa inyong kabataan, o pagkain na paborito nyong kainin lagi."),
            ],
        },
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Katulad ng sa akin kapitan. Ang paborito kong pagkain ay ang Petchay Soup na laging inihahanda sa akin ng aking ina nuong bata pa ako. Nang matikman ko ito, naalala ko na ang mga panyayari sa nakalipas na araw."),
            ],
        },
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "May paborito akong pagkain na inihahanda ng aking ina nuon bata pa ako. Ngunit hindi ko maalala kung ano ito. Ang naaalala ko lang ay ang pangunahing sangkap nito na Monggo."),
            ],
        },
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "KUng ganon simulan natin sa pagtatanim ng Monggo upang maluto at maibalik natin ang iyong mga alala kapitan."),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "HAHAHAHAH! Monggo?! Kahit gaano pa kadami ang itanim nyo, hindi nito ibabalik ang mga alaala ng Kapitan! Binura ko na ang inyong kaalaman sa pagtatanim ng anumang uri ng halaman."),
            ],
        },
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Tumigil ka Baron! Hindi mo kami mapipigilang tulungan si kapitan Ernesto na maibalik ang kanyang mga alaala!"),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "HAHAHAHAH! Sige! Magaksaya ka ng panahon sa iyong kahibangan! Hindi mo maibabalik ang mga alaala ng Kapitan Ernesto! HAHAHAHAHA!"),
            ],
        },
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
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Walang sino man ang makakapigil sa akin na tulungan si Kapitan Ernesto na maibalik ang kanyang mga alaala! Kaya't simulan na natin ang pagtatanim ng Monggo!"),
            ],
        },

        # ── Day 1 transition ───────────────────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },

        {
            "id":    "S2P0",
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
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Eto po kapitan ang mga buto ng monggo."),
            ],
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
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Kailangan po muna nating pausbungin ang maliit na halaman mula buto ng monggo. Paragawin ito ibabad muna natin sa tubig ang mga buto ng monggo sa loob ng tatlong oras. Saka ilipat sa planggana na may malinis na tela."),
                ("lucas", "Tatakpan naman natin ito ng isa pang malinis na tela at plato sa ibabaw. Ilagay natin sa lugar na may sapat na liwanag at hindi direktang maarawan. Pagkatapos ng tatlong araw, makikita natin ang mga buto ng monggo na unti-unting sumisibol."),
            ],
        },
        # ── Day 4 transition ───────────────────────────────────
        {
            "id":   "day4_fade",
            "type": "transition",
        },
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/MonggoSproutbg.jpg",
            "lines": [
                ("lucas", "Tatlong araw na ang nakalipas kapitan."),
                ("lucas", "At mukhang sumisibol na ang mga buto ng monggo. Ngayon ay ililipat natin ito sa paso na may lupa para tuluyang tumubo ang mga punla."),
            ],
        },
        # ── Day 5 transition ───────────────────────────────────
            {
                "id":   "day5_fade",
                "type": "transition",
            },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/Monggobg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Kailangan nating palaguin ang mga monggo ngayong nailipat na natin ito mula sa paso patungo sa lupa. Ano sa tingin nyo ang dapat nating gawin kapitan?"),
            ],
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/Monggobg.jpg",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "kailangan nating diligan ang mga ito ng malumanay at sapat na tubig."),
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
        {
            "id": "S2P21",
            "type": "scene",
            "bg": "background/baronmonggobgnew.jpg",
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
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "bg":    "background/baronmonggobgnew.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Mga hangal! Ginagalit nyo ako sa mga pinagagagawa nyo! Akala nyo ba kaya nyo akong talunin sa kakarampot na kaalamang naaalala ninyo?"),
                ("baron", "Matitikman nyo ngayon ang lupit ng kapangyarihan ko!"),
            ],
        },
        {
            "id":   "day5_fade",
            "type": "transition",
        },
        {
            "id": "S2P26",
            "type": "scene",
            "bg": "background/baronmonggoswarmed.jpg",
            "shake": True,   # camera shake on arrival (S2P25 -> S2P26)
        },
        {
            "id":    "S3P1",
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
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/baronmonggoswarmed.jpg",
            "chars": {"lucas": {"side": "left", "expression": "afraid", "flip": True}},
            "lines": [
                ("lucas", "Hindi maaari ito kapitan. Kailangan nating maagapan agad ang mga peste upang ating maprotektahan ang mga halaman."),
            ],
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/baronmonggoswarmed.jpg",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Kailangan nating puksain ang mga ito!"),
                ("kapitan", "Biilis Lucas kunin mo ang Natural na Pestesidyo upang maprotektahan ang mga halaman!"),
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
            "bg": "background/baronmonggoswarmed.jpg",
            "overlay": "naturalpesticidecard.png",
            "dim_inactive": False,
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/baronmonggoswarmed.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Magaling! nagawa nating pigilan ang mga peste sa ating taniman!"),
                ("lucas", "Unti unti na silang nagsisialisan at nawala sa ating taniman!"),
            ],
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/baronmonggobgnew.jpg",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Walang maidudulot na maganda ang ginawa mo Baron! Masmabuti pang itigil mo na ang mga panggugulo mo sa baryo natin!"),
            ],
        },
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "bg":    "background/baronmonggobgnew.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Mga hangal! Naisahan nyo ako ngayon ngunit hindi nyo na ito magagawa pa sa susunod na pagbabalik ko!")
            ],
        },
        {
            "id": "S2P21",
            "type": "scene",
            "bg": "background/baronmonggobgnew.jpg",
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
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/Monggobg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Magaling! nagawa nating maitaboy si Baron sa ating taniman!"),
                ("lucas", "Ngayon ay maaari na nating alagaan ang mga halaman ng Monggo at hintayin ang mga ito na tuluyang sumibol!"),
            ],
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/Monggobg.jpg",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Tama ka Lucas! Ngayon ay maaari na nating hintayin ang mga halaman ng Monggo na tuluyang sumibol!"),
            ],
        },
        {
            "id":   "day5_fade",
            "type": "transition",
        },
        {
            "id":            "S2P3",
            "type":          "choice",
            "bg":            "background/baronmonggoswarmed.png",
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
            "lines": [
                ("lucas", "Tama! Gamitin ang Dulo para gumawa ng maliliit at mababaw na butas. Ganyan ang tamang simula para sa buto ng Monggo."),
            ],
            "chars": {
                "lucas": {"side": "left", "expression": "thumbs", "flip": True},
            },
        },
        {
            "id":          "S2P3_right_2",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": "left"},
            "lines": [
                ("kapitan", "Nauunawaan ko na. Kailangan ng maliliit na buto ang tamang lalim ng tanim."),
            ],
        },
        {
            "id":               "S2P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":       {
                "lucas": {"side": "right", "expression": "concerned"},
            },
            "lines": [
                ("lucas", "Hindi pa iyon ang angkop na kagamitan. Subukan ang Dulo para makagawa tayo ng maliliit na butas nang maingat."),
            ],
        },

        # ── Panel 3 — Baron tricks: siksikin! ─────────────────
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Ilagay ninyo ang lahat ng buto sa iisang butas! Mag-unahan kayo sa tubig at sustansya — mas madaling masira ang tanim ninyo! HAHAHA!"),
            ],
        },
        {
            "id":    "S3P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Kung pagsisiksikin natin, mas marami agad ang maitatanim. Pero... hindi ba dapat bigyan ng sariling puwang ang bawat isa?"),
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
            "chars":       {
                "lucas": {"side": "left", "expression": "thumbs", "flip": True},
            },
            "lines": [
                ("lucas", "Tama. Bawat buto ay nangangailangan ng puwang para sa tubig, liwanag, at sustansya. Kapag maayos ang pagitan, mas madaling alagaan ang buong hanay."),
            ],
        },
        {
            "id":               "S3P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {
                "lucas": {"side": "right", "expression": "concerned"},
            },
            "lines": [
                ("lucas", "Kapag masyadong siksik ang tanim, mag-aagawan ang mga halaman sa tubig at sustansya. Subukan nating ayusin ang pagitan para maalagaan ang bawat punla."),
            ],
        },

        # ── Day 3 transition ───────────────────────────────────
        {
            "id":   "day3_fade",
            "type": "transition",
        },

        {
            "id":    "S4P0",
            "type":  "dialogue",
            "day":   3,
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Inayos ko ang pagitan ng mga buto. Ngayon ay gusto kong diligan agad ang buong taniman para walang maiwan."),
                ("lucas", "Titingnan muna natin kung ano ang kailangan ng lupa. Ang maingat na pag-aalaga ay hindi nangangahulugang laging gumawa ng higit pa."),
            ],
        },

        # ── Panel 4 — Water scan: soften the soil ─────────────
        {
            "id":      "S4P1",
            "type":    "dialogue",
            "day":     3,
            "bg":      "background/scenebg_planter.png",
            "chars":   {"kapitan": "right"},
            "lines": [
                ("kapitan", "Tuyo na ang lupa rito, Lucas. Ano ang dapat nating gawin bago tuluyang sumibol ang Monggo?"),
            ],
        },
        {
            "id":       "S4P2",
            "type":     "scan",
            "day":      3,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "active":   "lucas",
            "card":     "AC-01 Water Card",
            "dialogue": "Dahan-dahan lang, Kapitan. I-scan ang Water Card para mamasa-masa ang lupa at matulungan ang mga buto na sumibol.",
            "question": "I-scan ang Water Card para diligan nang sapat ang bagong tanim na Monggo.",
        },

        {
            "id": "day7_fade",
            "type": "transition",
        },
        {
            "id": "S4P3",
            "type": "narration_overlay",
            "day": 7,
            "bg": "background/scenebg_night.jpg",
            "overlay": "woodbg.png",
            "narration": (
                "Ilang araw na maingat na sinuri ni Kapitan Ernesto ang lupa. "
                "Hindi niya diniligan dahil lamang sa kaba. Sa ikapitong araw, "
                "sumilip ang maliliit na usbong sa hanay ng mga buto."
            ),
        },
        {
            "id":    "S4P4",
            "type":  "dialogue",
            "day":   7,
            "bg":    "background/scenebg_planter.png",
            "chars": {
                "kapitan": "right",
                "lucas": {"side": "left", "expression": "talking", "flip": True},
            },
            "lines": [
                ("kapitan", "Akala ko kailangang bantayan ang lahat sa bawat sandali. Pero ang kailangan pala ng mga buto ay tamang pag-aalaga at panahon."),
                ("kapitan", "May naaalala akong tunog ng kampana sa bulwagan. Kapag naririnig iyon ng mga tao, alam nilang may pagtitipon at may tutulong sa kanila."),
                ("lucas", "Tama, Kapitan. Hindi ibig sabihin ng paghihintay na pinababayaan natin sila. Patuloy lang nating susuriin ang lupa at mga usbong."),
            ],
        },

        # ── Day 25 transition: Baron tempts him to overwater ───
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
                ("baron", "Diligin mo ulit! Oras-oras! Kapag hindi mo sila binantayan bawat sandali, mamamatay ang mga iyan — at mabibigo ka na naman sa mga tao mo!"),
            ],
        },
        {
            "id":    "S5P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Basa pa ang lupa matapos ang ulan. Gusto kong tiyaking ligtas ang mga punla, pero baka lalo ko silang mapahamak kung susundin ko siya."),
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
            "chars": {
                "lucas": {"side": "left", "expression": "thumbs", "flip": True},
                "kapitan": "right",
            },
            "lines": [
                ("lucas", "Tama. Hindi kailangang diligan kapag basa pa ang lupa. Ang pagtingin at paghihintay ay bahagi rin ng pag-aalaga."),
                ("kapitan", "Kung gayon, hindi ko kailangang kontrolin ang bawat patak. Kailangan kong tingnan ang kalagayan ng lupa at magpasya para sa ikabubuti ng lahat."),
            ],
        },
        {
            "id":               "S5P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {
                "lucas": {"side": "right", "expression": "concerned"},
            },
            "lines": [
                ("lucas", "Kapag palaging basa ang lupa, maaaring kapusin sa hangin ang mga ugat at mabulok. Hintayin muna nating matuyo nang kaunti."),
            ],
        },

        {
            "id": "day30_fade",
            "type": "transition",
        },
        {
            "id":    "S5P4",
            "type":  "dialogue",
            "day":   30,
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Mas luntian na ang mga dahon. May iniwang supot ng pataba sa tabi ng taniman. Sabi ni Baron, iyon daw ang magpapabilis sa paglaki."),
                ("kapitan", "Pero ayaw kong madaliin ang mga ito kung makakasama naman sa lupa. Ano kaya ang mas maingat na piliin?"),
            ],
        },
        {
            "id":    "S5P5",
            "type":  "dialogue",
            "day":   30,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Gamitin mo ang kemikal na pataba! Mabilis na resulta, walang paghihintay. Hindi ba iyan ang gusto ng isang Kapitan na kailangang patunayan ang sarili?"),
            ],
        },
        {
            "id":       "S5P6",
            "type":     "scan",
            "day":      30,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "active":   "lucas",
            "card":     "AC-02 Organic Fertilizer Card",
            "dialogue": "Hindi kailangang pilitin ang Monggo na lumaki agad. Piliin ang organikong pataba para suportahan ang lupa nang maingat; huwag gamitin ang kemikal na pataba bilang madaling kapalit.",
            "question": "I-scan ang Organic Fertilizer Card para suportahan nang maingat ang lupa ng Monggo.",
        },
        {
            "id":    "S5P7",
            "type":  "dialogue",
            "day":   30,
            "bg":    "background/scenebg_planter.png",
            "chars": {
                "kapitan": "right",
                "lucas": {"side": "left", "expression": "talking", "flip": True},
            },
            "lines": [
                ("kapitan", "Organikong pataba ang pinili natin. Hindi natin kailangang gumamit ng kemikal para piliting lumaki ang tanim."),
                ("lucas", "Tama. Kaunti lang ang kailangan. Ang Monggo ay legume, kaya huwag sobrahan sa patabang mayaman sa nitrogen; panatilihing maayos ang lupa."),
                ("kapitan", "May mga tao akong pinangakuan noon na hindi ko isasapanganib ang kanilang pagkain para lang makapagpakitang-gilas. Hindi ko pa maalala ang lahat, pero alam kong mahalaga iyon."),
            ],
        },

        {
            "id": "day45_fade",
            "type": "transition",
        },
        {
            "id": "S6P0",
            "type": "narration_overlay",
            "day": 45,
            "bg": "background/scenebg_night.jpg",
            "overlay": "woodbg.png",
            "narration": (
                "Lumipas ang mga linggo. May mga bulaklak at maliliit na pods "
                "na ang Monggo. Hindi pare-pareho ang laki ng bawat halaman, "
                "ngunit pantay-pantay ang puwang at pag-aalaga sa hanay. "
                "Natutuhan ni Kapitan Ernesto na hindi kailangang pilitin "
                "ang bawat isa para sabay-sabay silang umunlad."
            ),
        },

        # ── Day 50 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day50_fade",
            "type": "transition",
        },

        # ── Panel 6 — Kapitan sees the pods forming ──────────
        {
            "id":      "S6P1",
            "type":    "dialogue",
            "day":     50,
            "bg":      "background/scenebg_planter.png",
            "chars":   {"kapitan": "right"},
            "lines": [
                ("kapitan", "May mga pods na! Noong una, akala ko ang pagiging pinuno ay ang mag-utos at tiyaking walang magkakamali. Pero ngayon, nakikita kong mahalaga ring bigyan ng panahon ang bawat isa."),
                ("kapitan", "Kapag hinog na ang ani, gusto kong tipunin ang mga tao sa bulwagan. May pakiramdam akong may pagkaing inihahanda namin noon para sa lahat."),
            ],
        },
        {
            "id":       "S6P2",
            "type":     "dialogue",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Natututo kang magtiwala sa proseso, Kapitan. Ituloy natin ang pagtingin sa lupa at diligan lamang kapag kailangan."),
            ],
        },

        # ── Day 65 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day65_fade",
            "type": "transition",
        },

        # ── Panel 7 — Harvest readiness ──────────────────────
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   65,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Kapitan, handa na ang ilan sa mga pods. Alin ang dapat nating anihin?"),
            ],
        },
        {
            "id":    "S7P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"kapitan": "right"},
            "lines": [
                ("kapitan", "Puno at matigas na ang mga butil, at nagsisimula nang matuyo ang pods. Iyon ang dapat hanapin."),
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
                ("kapitan", "Iyan nga! Puno na ang mga butil at bahagyang tuyo ang pods. Handa na ang mga iyan para anihin!"),
            ],
        },
        {
            "id":               "S7P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {
                "lucas": {"side": "right", "expression": "concerned"},
            },
            "lines": [
                ("lucas", "Hindi pa hinog ang patag at malambot na pods. Hintayin nating mapuno at magsimulang matuyo ang mga ito."),
            ],
        },

        # ── Panel 8 — End: Monggo Guisado memory restored ─────
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   65,
            "bg":    "background/scenebg_default.png",
            "chars": {
                "kapitan": "right",
                "lucas": {"side": "left", "expression": "talking", "flip": True},
            },
            "lines": [
                ("kapitan", "Ang amoy ng ginisang bawang... kamatis... at Monggo! MONGGO GUISADO! Inihahanda namin ito tuwing nagtitipon ang mga tao sa bulwagan."),
                ("kapitan", "Hindi lang pala ako namumuno. Tinitiyak kong may makakain ang lahat at walang naiiwan. Iyon ang dahilan kung bakit ako naging Kapitan!"),
            ],
        },
        {
            "id":    "S8P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Hindi lang Monggo ang pinalago natin. Naalala mo kung paano pag-isahin at protektahan ang mga tao sa baryo. Ikalawang alaala na ang naibalik natin."),
                ("lucas", "Monggo Guisado Memory — UNLOCKED!"),
            ],
        },
        {
            "id":    "S8P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Isang alaala lang ang naibalik ninyo! Hindi pa tapos ang laban, Kapitan!"),
            ],
        },

    ],
}
