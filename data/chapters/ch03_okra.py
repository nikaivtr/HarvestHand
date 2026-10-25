# ============================================================
#  CHAPTER 3 — OKRA
#  Beginner | 8 story panels | Total growing days: 55
#  Characters: Lucas, Chef Pablo, Blight Baron
# ============================================================

CHAPTER = {
    "id":         "ch03",
    "crop":       "Okra",
    "level":      "beginner",
    "memory":     "Sinigang na Baboy Memory",
    "total_days": 55,

    "slides": [

        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "logos/chapter3.png",    # placeholder — replace with ch3 logo
        },

        # ── Panel 1 — Chef Pablo's empty kitchen - Day 0 ───────────────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "day":   0,
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Magandang umaga Chef Pablo!"),
                ("lucas", "Bakit po kayo nakasimagot?"),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Walang maganda sa araw ko Lucas."),
                ("chef", "Wala akong maalala sa aking mga sangkap sa pagluluto! Nais ko sanang kumain nang aking espesyal na Sinigang na Baboy."),
                ("chef", "Ngunit hindi ko makita ang mga sangkap nito! Nawawala ang mga okra ko, at hindi ko maalala ang iba pang pampalasang gamit ko."),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": "True"}},
            "lines": [
                ("lucas", "Kagagawan ito ni Baron Chef Pablo."),
                ("lucas", "Binura nya ang mga ala-ala ng mga taong nakatira sa baryo natin!"),
                ("lucas", "Wag kang mag-alala Chef Pablo. Tutulungan kita sa iyong problema."),
            ],
        },
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "angry"}},
            "lines": [
                ("chef", "Ano naman ang maitutulong mo sa akin Lucas? Isa ka lang bata, hindi mo alam ang mga gagawin sa loob ng kusina!"),
                ("chef", "Wala na! Wala nang makakatulong sa akin! Wala nang sinuman ang makakapagpabalik ng mga ala-ala ko!"),
            ],
        },
        {
            "id": "S1P5",
            "type": "scene",
            "bg": "background/baronkitchenbg.jpg",
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
        {
            "id":    "S1P6",
            "type":  "dialogue",
            "bg":    "background/baronkitchenbg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "HAHAHA! Tama ka Chef Pablo! Mawalan ka nalang nag pag-asa! Hindi ka na muling makakapagluto pa!"),
                ("baron", "At ikaw bata! Sumuko ka na rin, nagtagumpay ka sa nakaraan kong mga pagsubok, pero sa isang to? Hinding-hindi ka magtatagumpay!"),
            ],
        },
        {
            "id":    "S1P7",
            "type":  "dialogue",
            "bg":    "background/baronkitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": "True"}},
            "lines": [
                ("lucas", "Tigilan mo kami Baron!"),
                ("lucas", "Kailan man ay wala kaming ginawang masama sa iyo para gawin ito sa amin!"),
                ("lucas", "Kahit na gaano ka hirap ang mga hamon mo, hinding hindi mo kami mapapasuko!"),
            ],
        },
        {
            "id":    "S1P8",
            "type":  "dialogue",
            "bg":    "background/baronkitchenbg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "HAHAHA! Tignan nalang natin bata!"),
                ("baron", "Tignan natin kung gaano ka mainipin ang tutulungan mo!"),
            ],
        },
        {
            "id": "S1P9",
            "type": "scene",
            "bg": "background/baronkitchenbg.jpg",
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
        {
            "id": "S1P10",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",

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
            "id":    "S1P11",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Paano na ako nito lucas? Paano na ang aking kakayanan at talento sa pagluluto?"),
                ("chef", "Hindi na ba maibabalik ang aking ala-ala?"),
            ],
        },
        {
            "id":    "S1P12",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": "True"}},
            "lines": [
                ("lucas", "Wag kang mag-alala Chef Pablo!"),
                ("lucas", "Tutulungan kita na ma-alala ang iyong mga ala-ala."),
            ],
        },
        {
            "id":    "S1P13",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Paano naman natin ito gagawin!?"),
            ],
        },
        {
            "id":    "S1P14",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Tukuyin muna natin ang pinakasentro ng iyong ala-ala."),
                ("lucas", "Alamin natin kung ano ang ala-alang mas may natural na halaga sa iyo."),
                ("lucas", "Alam kong mahal mo ang pagluluto, may espesyal ka bang putahe na maaaring magpabalik sa iyong ala-ala?"),
            ],
        },
        {
            "id":    "S1P15",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "talking"}},
            "lines": [
                ("chef", "Oo! Ang aking sinigang na baboy! Ngunit hindi ko maalala ang mga sangkap nito!"),
            ],
        },
        {
            "id":    "S1P16",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Wag kang mag-alala Chef Pablo."),
                ("lucas", "Tutulungan ka namin ng mga kasama ko."),
                ("lucas", "Puwede ba nating tulungan si Chef Pablo sa mga kinakailangan nyang sangkap?"),
            ],
        },
        {
            "id":    "S1P17",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": "True"}},
            "lines": [
                ("lucas", "Magaling!"),
            ],
        },
        # ── Ingredient Jigsaw Challenge: Sinigang na Baboy ──
        {
            "id":    "ingredient_puzzle_1",
            "type":  "ingredient_puzzle",
            "bg":    "background/scenebg_default.png",
        },
        {
            "id":    "S1P18",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": "True"}},
            "lines": [
                ("lucas", "Magaling! Nakuha na natin ang lahat ng sangkap sa pag gawa ng Sinigang na baboy!"),
                ("lucas", "Meron ka ba ng mga ito Chef Pablo?"),
            ],
        },
        {
            "id":    "S1P19",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "talking"}},
            "lines": [
                ("chef", "Teka at titignan ko kung meron."),
            ],
        },
        # ── Scene1 transition ───────────────────────────────────
        {
            "id":   "scene1_fade",
            "type": "transition",
        },
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Meron ako ng iba, tanging ang okra lamang ang wala sa akin."),
                ("chef", "Magiiba ang lasa ng aking sinigang kung wala ang okra na ito.")
            ],
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Wag kayong mag-alala Chef Pablo, tutulungan namin kayo ni Lola Maria sa pagtatanim ng okra."),
                ("lucas", "Meron ka bang binhi ng mga okra Chef Pablo?"),
            ],
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Meron ako sa taniman sa likod. Pero hindi ito tumutubo."),
            ],
        },
        {
            "id":    "S2P4",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": "True"}},
            "lines": [
                ("lucas", "Wag kayong mag-alala Chef Pablo, sigurado akong alam ni lola Maria paano iito palaguin"),
                ("lucas", "Tawagin ko muna si lola Maria, magkita nalang tayo sayong taniman."),
            ],
        },
        # ── Scene2 fade ───────────────────────────────────
        {
            "id":   "scene2_fade",
            "type": "transition",
        },
        {
            "id":    "S2P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Andito na po kami Chef Pablo."),
                ("lucas", "Lola Maria maaari nyo po bang tignan ang mga tanim na okra ni Chef Pablo?"),
            ],
        },
        {
            "id":    "S2P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Walang problema apo."),
            ],
        },
        {
            "id":    "S2P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "shocked", "flip": False}},
            "lines": [
                ("lola", "Naku! Mali ang pamamaraan nang pagtanim ng mga buto na ito."),
            ],
        },
        {
            "id":    "S2P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Dapat muna nating ibabad ito ng 10 hanggang 12 oras sa tubig upang lumambot ang panlabas na shell ng buto."),
                ("lola", "Para rin maging mas mabilis ang pagsibol ng okra."),
            ],
        },
        {
            "id":    "S2P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "right", "expression": "angry"}},
            "lines": [
                ("chef", "Ang tagal naman ng ating aantayin para dyan!"),
            ],
        },
        {
            "id":    "S2P10",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Mas mainam na dahan-dahan at sigurado ang ating mga hakbang Chef Pablo."),
                ("lucas", "Upang maiwasan na rin ang mga hindi kaaya-ayang resulta."),
            ],
        },
        {
            "id":    "S2P11",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Nararapat na ituring ang mga halaman bilang tao rin."),
                ("lola", "Katulad ng sanggol, masyadong maselan ang mga buto at dapat itong unti unting patubuin sa kontroladong lugar."),
            ],
        },
        {
            "id":    "S2P12",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Hindi na ako makapag-antay!"),
                ("chef", "Gagawa ako ng sarili kong paraan. Tignan natin kung sino ang mas mabisa."),
            ],
        },
        {
            "id":    "S2P13",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Hindi ka dapat masyadong mainipin Chef Pablo, sapagkat mas mainam na sundin ang tamang pamamaraan ng pagtatanim upang hindi masira at mas makapagdulot ng di kaaya-ayang resulta sa huli."),
            ],
        },
        {
            "id":    "S2P14",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "right", "expression": "angry"}},
            "lines": [
                ("chef", "Hindi ko na kailangan ang mga iyan lola Maria."),
                ("chef", "Mas alam ko ang ginagawa ko!"),
            ],
        },
        {
            "id":    "S2P15",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Hayaan nalang muna nating gawin ni Chef Pablo ang gusto nya lola. Mukhang wala po tayong magagawa."),
                ("lucas", "Mag tanim nalang po tayo sa paraang alam natin, at para narin hindi masayang ang panahon kung sakaling hindi umubra ang paraang gagawin nya."),
            ],
        },
        {
            "id":    "S2P16",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Mabuti pa nga apo. Simulan na natin ang tamang pamamaraan ng pagtatanim."),
            ],
        },
        # ── Day 1 transition ───────────────────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },
        {
            "id":    "S2P17",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Isang araw na ang lumipas apo. Puwede na nating ilipat ang mga buto ng okra sa mas mainam na lugar. Tiyakin lang nating may sapat na araw sila."),
                ("lola", "Piliin natin ang lugar kung saan nasisikatan ng araw sa loob ng 6 hanggang 8 oras kada araw para tiyak ang sustansyang nakukuha nila mura sa araw."),
            ],
        },
        {
            "id":    "S2P18",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Okay po lola!"),
                ("lucas", "Anong kagamitan po sa paghuhukay ng butas ang dapat kong gamitin?"),
            ],
        },
        {
            "id":            "S2P19",
            "type":          "choice",
            "day":   1,
            "bg":            "background/scenebg_default.png",
            "question":       "Alin ang tamang kagamitan para gumawa ng maliliit na butas para sa buto ng Okra?",
            "retry_question": "Sandali... pakiramdam ko masyadong malalim ang hukay nito para sa direktang pagtatanim.",
            "choices": [
                # These cards are finished art -- own frame and baked-in
                # "DULO"/"ASAROL" text -- so no engine panel or label.
                {"img": "buttons/choice_trowel.png", "label": "", "frame": False},
                {"img": "buttons/choice_hoe.png",    "label": "", "frame": False},
            ],
            "correct": 0,
        },
        # ── Panel 20 - Feedback Correct - Lucas Thumbs up ───────────────
        {
            "id":          "S2P20_right_1",
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
        # ── Panel 23 - Feedback: Correct — Lola thumbs up ───────────────
        {
            "id":         "S2P23_right_2",
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
        # ── Panel 24 ── Feedback: Wrong — Lucas worried ───────────────────
        {
            "id":          "S2P24_wrong_1",
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
        # ── Panel 25 ── Feedback: Wrong — Kapitan warns ───────────────────
        {
            "id":              "S2P25_wrong_2",
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
        {
            "id":    "S2P26",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Okay na po lola! Naitanim na nating maigi ang mga binhi."),
                ("lucas", "May sapat na rin sila na espasyong 12 hanggang 18 pulgada upang maiwasan ang pagkabuholbuhol nila sa isat isa."),
            ],
        },
        {
            "id":    "S2P27",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Panatilihin lang nating basa ang mga lupang pinagtaniman natin hanggang umusbong ang mga halaman mula sa ilalim ng lupa apo."),
            ],
        },
        {
            "id": "S2P28",
            "type": "action_challenge",
            "day":   1,
            "bg": "background/scenebg_default.png",
            "overlay": "background/Action_Challenge-Water.png",
            "dim_inactive": False,
        },
        # ── Day 2 transition ───────────────────────────────────
        {
            "id":   "day2_fade",
            "type": "transition",
        },
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "day":   2,
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Paano ba itong ginagawa ko? Bakit ang tagal tumubo ng mga pananim ko?"),
                ("chef", "Humingi na kaya ako ng tulong kina lola Maria?"),
            ],
        },
        {
            "id": "S3P2",
            "type": "scene",
            "bg": "background/scenebg_baron.png",
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
        {
            "id":    "S3P3",
            "type":  "dialogue",
            "day":   2,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "HEHEHE! Walang mali sa ginagawa mo Chef!"),
                ("baron", "Hindi alam ng dalawang yun kung ano ang pinaggagagawa nila"),
            ],
        },
        {
            "id":    "S3P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "chars": {"chef": {"side": "left", "expression": "angry", "flip": "True"}},
            "lines": [
                ("chef", "Nililinlang mo ba ako baron?"),
                ("chef", "Umalis ka nga sa harap ko!"),
            ],
        },
        {
            "id":    "S3P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "HEHEHE! Hindi kita nililinlang Chef!"),
                ("baron", "Hindi ko kinuha ang kaalaman mo sa pag-tatanim. Nagkamali akong kunin ang kaalaman mo sa pag-luluto pero ang kaalaman mo sa pag-tatanim ay nananatili pa rin!"),
                ("baron", "Kung ano man yang ginagawa mo, tama yan! Sapagkat ikaw ang lamang ang nakakaalala at nakaka-alam nyan! HEHEHEHE!"),
            ],
        },
        {
            "id":    "S3P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "chars": {"chef": {"side": "left", "expression": "worried", "flip": "True"}},
            "lines": [
                ("chef", "Totoo ba?"),
                ("chef", "Paano ko maibabalik ang aking ala-ala?"),
            ],
        },
        {
            "id":    "S3P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Ipagpatuloy mo lang yan!"),
                ("baron", "Unti-unti babalik ang ala-ala mo! HAHAHA"),
            ],
        },
        {
            "id": "S3P8",
            "type": "scene",
            "bg": "background/scenebg_baron.png",
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
        {
            "id":    "S3P9",
            "type":  "dialogue",
            "day":   2,
            "bg":    "background/scenebg_baron.png",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Siguro naman nag-sasabi sya nag totoo?"),
                ("chef", "Ipagpapatuloy ko lang to!"),
            ],
        },
        # Scene 3 fade
        {
            "id":   "scene3_fade",
            "type": "transition",
        },
        # Scene day 10
        {
            "id": "S3P10",
            "type": "narration_overlay",
            "day": 10,
            "bg": "background/chefokra.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",

            "narration": (
                "10 araw nang nasa taniman si Chef Pablo, "
                "araw araw nyang dinidiligan ang mga halaman "
                "ngunit mali ang ginagawa nyang paraan ng pagtatanim "
                "na hindi ito lumalago at lumalaki."
            ),
        },
        {
            "id":   "scene3_fade",
            "type": "transition",
        },
        # Scene day 45
        {
            "id": "S3P11",
            "type": "narration_overlay",
            "day": 45,
            "bg": "background/lucasokra.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",

            "narration": (
                "Samantalang lumalago ng maayos ang okrang itinanim  "
                "nila Lucas at Lola Maria."
                "Araw araw nya rin itong dinidiligan at inaalagaan,"
                "ngayon ay malago at malalaki na ang mga bunga nito."
            ),
        },
        # Scene day 55
        {
            "id":    "S3P12",
            "type":  "dialogue",
            "day":   55,
            "bg":    "background/okrabgweed.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Mukhang marami-rami na po ang mga dahon sa paligid ng ating mga tanim lola, kailangan na po ata natin itong tabasan at kunin."),
            ],
        },
        {
            "id":    "S3P13",
            "type":  "dialogue",
            "bg":    "background/okrabgweed.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Oo nga apo, mukhang kailangan natin ng espesyal na kagamitan para matanggal ang mga ito."),
            ],
        },
        {
            "id": "S3P14",
            "type": "action_challenge",
            "bg": "background/okrabgweed.jpg",
            "overlay": "weedremovalcard.png",
            "dim_inactive": False,
        },
        {
            "id":    "S3P15",
            "type":  "dialogue",
            "bg":    "background/okrabg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": "True"}},
            "lines": [
                ("lucas", "Sa wakas, nakuha na rin natin ang mga nakaharang at hindi kaaya ayang mga dahon sa paligid ng ating mga tanim na Okra!"),
                ("lucas", "Bisitahin ko muna po si Chef Pablo, at titignan ko kung ano na po ang kalagayan ng kanyang taniman Lola Maria."),
            ],
        },
        {
            "id":   "scene3_fade",
            "type": "transition",
        },
        {
            "id":    "S3P16",
            "type":  "dialogue",
            "bg":    "background/okrabgchef.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "San ako nagkamali? Bakit ang pangit ng tubo ng aking mga tanim?"),
                ("chef", "Sinungaling talaga itong si Blight Baron!"),
            ],
        },
        {
            "id":    "S3P17",
            "type":  "dialogue",
            "bg":    "background/okrabgchef.jpg",
            "chars": {"lucas": {"side": "left", "expression": "confused", "flip": "True"}},
            "lines": [
                ("lucas", "Naku! Anong nangyari sa taniman mo Chef Pablo?"),
                ("lucas", "Bakit andaming tuyong dahon at nalalantang mga pananim?"),
            ],
        },
        {
            "id":    "S3P18",
            "type":  "dialogue",
            "bg":    "background/okrabgchef.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Pasensya ka na Lucas, kung nakinig lang sana ako sa inyo."),
                ("chef", "Hindi na sana ako malilinlang ni Baron."),
            ],
        },
        {
            "id":    "S3P19",
            "type":  "dialogue",
            "bg":    "background/okrabgchef.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Baka puwede pa nating maisalba ang mga pananim mo Chef Pablo?"),
                ("lucas", "Maaari tayong humingi ng tulong sa ating mga kaibigan."),
            ],
        },
        {
            "id":    "S3P20",
            "type":  "dialogue",
            "bg":    "background/okrabgchef.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Kung kaya pang isalba Lucas, tulungan mo ako."),
                ("chef", "Baka dahil dito hindi na makabalik ang ala-ala ko sa pagluluto."),
            ],
        },
        {
            "id":    "S3P21",
            "type":  "dialogue",
            "bg":    "background/okrabgchef.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Wag kang mag-alala chef pablo."),
                ("lucas", "Handa tayong tulungan ng ating mga kaibigan."),
            ],
        },
        {
            "id":    "S3P23",
            "type":  "dialogue",
            "bg":    "background/okrabgchef.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Handa na ba kayong tulungan natin si Chef Pablo?"),
            ],
        },
        {
            "id":    "S3P24",
            "type":  "dialogue",
            "bg":    "background/okrabgchef.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": "True"}},
            "lines": [
                ("lucas", "Magaling!"),
            ],
        },
        {
            "id":    "S3P25",
            "type":  "dialogue",
            "bg":    "background/okrabgchef.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Kailangan muna nating bunutin at kunin ang mga nakakaabalang lantang mga dahon sa paligid ng tanim."),
                ("lucas", "Anong gamit ang dapat nating gamitin?"),
            ],
        },
        {
            "id": "S3P26",
            "type": "action_challenge",
            "bg": "background/okrabgchef.jpg",
            "overlay": "analyzecard.png",
            "dim_inactive": False,
        },
        {
            "id": "S3P27",
            "type": "narration_overlay",
            "day": 55,
            "bg": "background/okrabgchef.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",

            "narration": (
                "Kailangan ng matinding kagamitan "
                "upang matanggal ang mga damo at halaman "
                "sa paligid ng tanim"
                "gumamit ng weed removal card upang magawa ito."
            ),
        },
        {
            "id": "S3P28",
            "type": "action_challenge",
            "bg": "background/okrabgchef.jpg",
            "overlay": "weedremovalcard.png",
            "dim_inactive": False,
        },
        {
            "id":    "S3P29",
            "type":  "dialogue",
            "bg":    "background/okrabgchefnew.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": "True"}},
            "lines": [
                ("lucas", "Magaling! Natanggal na natin ang mga dahon."),
            ],
        },
        {
            "id":    "S3P30",
            "type":  "dialogue",
            "bg":    "background/okrabgchefnew.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Ngunit lanta parin tignan ang mga tanim. Ano po ba ang mga hakbang na ginawa nyo Chef Pablo sa pagtatanim ng Okra?"),
            ],
        },
        {
            "id":    "S3P31",
            "type":  "dialogue",
            "bg":    "background/okrabgchefnew.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Ibinaon ko ang mga buto ng mas malalim pa sa isang pulgada, walang espasyong malaki sa pagitan ng mga ito."),
                ("chef", "Dinidiligan ko rin ng mas maraming tubig ito, kahit gabi sa pag-aakalang mas magiging mabilis ang pag tubo at pag lago nito."),
                ("chef", "Kung ano anong chemical na pampataba rin ang ginamit ko sa pag-aakalang mas magiging masibol ang mga ito."),
            ],
        },
        {
            "id":    "S3P32",
            "type":  "dialogue",
            "bg":    "background/okrabgchefnew.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Sa tingin ko ay sumobra po ang mga nailagay nyong pampataba at pag-dilig sa mga halaman."),
                ("lucas", "Laging tandaan na ang sobrang paggamit ng pataba at pagdilig ng tubig ay nakakasagabal sa natural at sensitibong balanse ng oxygen at minerals sa cellular na lebel."),
                ("lucas", "Mainam na maging maingat at malumanay sa dami ng tubig na ididilig, at sa dami ng patabang gagamitin."),
                ("lucas", "Laging tatandaan na ang pagtatanim ay katulad rin ng pagluluto, kailangang may sapat na pasensya sa bawat hakbang o sangkap na gagamitin."),
                ("lucas", "Sa ngayon hayaan muna nating lumago ang okra at hindi muna natin ito didiligan. Mainam rin na kunin ang mga sobrang pataba na nasa lupa, ito ay tinatawag na Fertilizer Burn."),
                ("lucas", "Hayaan nating makahinga ang halaman sa loob ng 4 hanggang 6 na linggo."),
            ],
        },
        {
            "id":    "S3P33",
            "type":  "dialogue",
            "bg":    "background/okrabgchefnew.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Napagtanto ko na ngayon ang kahalagahan ng mataas na pasensya sa pagtatanim Lucas."),
                ("chef", "Dahil sa aking kapabayaan at sa sobrang pagmamadali, hindi ko na napansing mas pinapalala ko pa lalo ang mga pangyayari."),
                ("chef", "At dahil dito mukhang hindi ko na talaga makukuha pa ang aking mga ala-ala."),
            ],
        },
        {
            "id":    "S3P34",
            "type":  "dialogue",
            "bg":    "background/okrabgchefnew.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": "True"}},
            "lines": [
                ("lucas", "Wag kayong mag-alala Chef Pablo. May inihanda na kami ni lola Maria para sa inyo."),
                ("lucas", "Tara po samahan nyo ako sa aming taniman."),
            ],
        },
        # Scene 4 fade
        {
            "id":   "scene4_fade",
            "type": "transition",
        },
        {
            "id":    "S4P1",
            "type":  "dialogue",
            "bg":    "background/okrabg.jpg",
            "chars": {"lucas": {"side": "right", "expression": "thumbs"}},
            "lines": [
                ("lucas", "Lola Maria, kasama ko po si Chef Pablo."),
                ("lucas", "Kumusta po ang mga tanim natin?"),
            ],
        },
        {
            "id":    "S4P2",
            "type":  "dialogue",
            "bg":    "background/okrabg.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Magandang araw po lola Maria. Nais ko po sanang humingi nang paumanhin sa aking mga sinabi nung nakaraang mga araw."),
            ],
        },
        {
            "id":    "S4P3",
            "type":  "dialogue",
            "bg":    "background/okrabg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ano ka ba, walang problema yan sa akin Chef Pablo. Alam ko naman ang nararamdaman mo kaya ka nagkaganon."),
                ("lola", "Hali na kayo, Tulungan nyo akong anihin ang mga bunga ng okrang ating itinanim."),
            ],
        },
        {
            "id":    "S4P4",
            "type":  "dialogue",
            "bg":    "background/okrabg.jpg",
            "chars": {"chef": {"side": "right", "expression": "talking"}},
            "lines": [
                ("chef", "Naging masagana po pala ang mga bunga ng okrang inyong naani Lola Maria!"),
            ],
        },
        {
            "id":    "S4P5",
            "type":  "dialogue",
            "bg":    "background/okrabg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ano ka ba, walang problema yan sa akin Chef Pablo. Alam ko naman ang nararamdaman mo kaya ka nagkaganon."),
                ("lola", "Hali na kayo, Tulungan nyo akong anihin ang mga bunga ng okrang ating itinanim."),
            ],
        },
        {
            "id":    "S4P6",
            "type":  "dialogue",
            "bg":    "background/okrabg.jpg",
            "chars": {"chef": {"side": "right", "expression": "default"}},
            "lines": [
                ("chef", "Ano po ang gagamitin natin lola?"),
            ],
        },
        {
            "id":    "S4P7",
            "type":  "dialogue",
            "bg":    "background/okrabg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Gamitin ang mga gamit pang ani, para anihin ang mga ito."),
            ],
        },
        {
            "id": "S4P8",
            "type": "action_challenge",
            "bg": "background/scenebg_default.png",
            "overlay": "harvestcardscan.png",
            "dim_inactive": False,
        },
        {
            "id":   "scene4_fade",
            "type": "transition",
        },
        {
            "id": "S4P9",
            "type": "narration_overlay",
            "day": 55,
            "bg": "background/okraharvest.jpg",
            "dim_inactive": False,
        },
        {
            "id":   "scene4_fade",
            "type": "transition",
        },
        {
            "id": "S4P10",
            "type": "narration_overlay",
            "day": 55,
            "bg": "background/okracooking.jpg",
            "dim_inactive": False,
        },
        {
            "id":   "scene4_fade",
            "type": "transition",
        },
        {
            "id":    "S4P11",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Ano po itong nangyayari sa akin? Hindi ko pa rin po ma-alala ang mga sangkap sa kahit anu mang lutuin maliban sa okra!"),
            ],
        },
        {
            "id":    "S4P12",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "shocked", "flip": False}},
            "lines": [
                ("lola", "Bakit hindi gumana sayo ang ating ginawa?"),
            ],
        },
        {
            "id": "S4P13",
            "type": "scene",
            "bg": "background/baronkitchenbg.jpg",
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
        {
            "id":    "S4P14",
            "type":  "dialogue",
            "bg":    "background/baronkitchenbg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "HAHAHA! Mga hung-hang! Akala nyo ba matatalo nyo ako dahil lang nakakain na siya ng kanyang espesyal na Sinigang na Okra!?"),
                ("baron", "HAHAHA! Ako ang nag tagumpay ngayon bata! HAHAHAHAHA!"),
            ],
        },
        {
            "id": "S4P15",
            "type": "scene",
            "bg": "background/baronkitchenbg.jpg",
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
        {
            "id":    "S4P16",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "right", "expression": "defense"}},
            "lines": [
                ("lucas", "!!!"),
            ],
        },
        # Scene end of day 55
        {
            "id":    "S4P17",
            "type":  "dialogue",
            "day":   55,
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "right", "expression": "wrong"}},
            "lines": [
                ("lucas", "Hindi maaari ito!"),
                ("lucas", "Saan tayo nagkamali?"),
            ],
        },
    ],
}
