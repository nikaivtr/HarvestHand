# ============================================================
#  CHAPTER 4 — SQUASH (Kalabasa)
#  Intermediate | 11 story panels | Total growing days: 90
#  Characters: Lucas, Chef Pablo, Lola Maria, Blight Baron
#  NEW MECHANICS: Compost, Weeds, Pests
# ============================================================

CHAPTER = {
    "id":         "ch04",
    "crop":       "Squash",
    "level":      "intermediate",
    "memory":     "Ginataang Kalabasa Memory",
    "total_days": 90,

    "slides": [

        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/kitchenbg.jpg",
            "logo": "chapter4.png",    # placeholder — replace with ch4 logo
        },

        # ── Panel 1 — Lucas is worried for Chef Pablo ────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "day":   55,
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "right", "expression": "wrong"}},
            "lines": [
                ("lucas", "Chef Pablo meron ka pa bang naaalalang luto na maaari mong magawa? Baka hindi okra ang kailangan para mapabalik ang iyong mga alala"),
                ("lucas", "Baka hindi okra ang kailangan para mapabalik ang iyong mga alala"),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Iisang putahe nalang ang hindi ko pa natitikman na tiyak akong makakapagpabalik ng aking ala-ala!"),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "tired", "flip": False}},
            "lines": [
                ("lola", "Ano ang putaheng ito Chef Pablo?"),
            ],
        },
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Ito ay ang Ginataang Kalabasa."),
                ("chef", "May problema tayo, wala na akong kalabasa."),
            ],
        },
        {
            "id":    "S1P5",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Meron akong mga natitira pang buto ng kalabasa sa hardin ko, bakit hindi nalang natin iyon itanim?"),
                ("lola", "Sandali at kukunin ko."),
            ],
        },
        {
            "id":    "S1P6",
            "type":  "dialogue",
            "day":   55,
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Kami na po ni Chef Pablo ang mag hahanda ng hardin para taniman ng mga buto ng kalabasa."),
                ("lucas", "Alin sa mga gamit na ito ang kailangan natin?"),
            ],
        },
        {
            "id":            "S1P7",
            "type":          "choice",
            "day":   55,
            "bg":            "background/scenebg_default.png",
            "question":       "Alin ang tamang kagamitan para gumawa ng maliliit na butas para sa buto ng Kalabasa?",
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
            "id":          "S1P8_right_1",
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
            "id":         "S1P9_right_2",
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
            "id":          "S1P10_wrong_1",
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
            "id":              "S1P11_wrong_2",
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
            "id":   "day0_fade",
            "type": "transition",
        },
        {
            "id":    "S1P11",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "right", "expression": "default"}},
            "lines": [
                ("chef", "Handa na ang ating mga pagtataniman."),
            ],
        },
        {
            "id":    "S1P12",
            "type":  "dialogue",
            "day":   55,
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Magaling! Dala na din ni Lola Maria ang mga buto ng kalabasa."),
            ],
        },
        {
            "id":    "S1P13",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Eto na ang mga buto, maaari nyo na itong itanim."),
            ],
        },
        {
            "id":    "S1P14",
            "type":  "dialogue",
            "day":   55,
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Itatanim ko po ang 3 hanggang apat na buto kada burol na may 1 hanggang 2 pulgadang espasyo sa bawat isa. Upang hindi kakatay sa ibang binhi ang mga ugat nito."),
                ("lucas", "Ano po ang susunod na mga hakbang na gagawin natin Lola Maria?"),
            ],
        },
        {
            "id":    "S1P15",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Maglalagay tayo ng katamtaman na dami ng pang-abono, para mas maging maganda ang drainage ng ating taniman."),
                ("lola", "Kailangang nasa 1 hanggang 2 pulgadang dami ng tubig lamang ang ating ididilig upang hindi masobrahan sa tubig ang mga buto ng kalabasa."),
            ],
        },
        {
            "id":    "S1P16",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "right", "expression": "default"}},
            "lines": [
                ("chef", "Ngayon ay mag aantay nalang tayo na tumubo ang mga ito."),
            ],
        },
        # ── Day 10 transition - Scene 2 ───────────────────────────────────
        {
            "id":   "day10_fade",
            "type": "transition",
        },
        {
            "id": "S2P1",
            "type": "narration_overlay",
            "day": 10,
            "bg": "background/scenebg_default.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",

            "narration": (
                "10 araw na ang lumipas mula nang itanim nila "
                "Lucas ang mga binhi ng kalabasa. "
                "Araw-araw nila itong inaalagaan "
                "ngunit may nag aambang panganib parin galing kay Baron."
            ),
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "day":   4,
            "bg":    "background/squashsprout.jpg",
            "lines": [
                ("lucas", "10 araw na ang nakalipas, ngayon ay tumutubo na ang mga buto ng kalabasa."),
                ("lucas", "Maibabalik na rin natin ang iyong mga ala-ala Chef Pablo."),
            ],
        },
        {
            "id":    "S2P3",
            "type":  "dialogue",
            "bg":    "background/squashsprout.jpg",
            "chars": {"chef": {"side": "right", "expression": "default"}},
            "lines": [
                ("chef", "Sa wakas may nakikita na akong umuusbong na pananim."),
            ],
        },
        {
            "id": "S2P4",
            "type": "scene",
            "bg": "background/baronsquashbg.jpg",
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
            "id":    "S2P5",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Ayaw nyo talagang sumuko ah?"),
                ("baron", "Pwes! matitikman nyo ngayon ang bagsik ng aking kapangyarihan!"),
            ],
        },
        {
            "id": "S2P6",
            "type": "scene",
            "day": 10,
            "bg": "background/baronsquashbgswarmed.jpg",
            "shake": True,   # camera shake on arrival (S2P35 -> S2P36)
        },
        {
            "id":    "S2P7",
            "type":  "dialogue",
            "bg":    "background/baronsquashbgswarmed.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "HAHAHAHAHAHAHA!!!"),
            ],
        },
        {
            "id":    "S2P8",
            "type":  "dialogue",
            "bg":    "background/baronsquashbgswarmed.jpg",
            "chars": {"chef": {"side": "right", "expression": "angry"}},
            "lines": [
                ("chef", "Wala ka talagang puso baron!"),
            ],
        },
        {
            "id": "S2P9",
            "type": "scene",
            "bg": "background/baronsquashbgswarmed.jpg",
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
            "id":    "S2P10",
            "type":  "dialogue",
            "bg":    "background/baronsquashbgswarmed.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Hindi maaari ito! Dapat natin itong mapigilan agad!"),
                ("lucas", "Bilis puksain natin ang mga nilalang na ito!"),
            ],
        },
         # Action Challenge
        {
            "id": "S2P11",
            "type": "action_challenge",
            "bg": "background/baronsquashbgswarmed.jpg",
            "overlay": "naturalpesticidecard.png",
            "dim_inactive": False,
        },
        {
            "id": "whack_a_pest_1",
            "type": "whack_a_pest",
        },
        {
            "id":    "S2P12",
            "type":  "dialogue",
            "bg":    "background/squashbg.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Phew! Mabuti nalang napigilan kaagad natin ang mga insekto na kumalat."),
                ("lucas", "kailangan natin ang natural na pestecida para mas maprotektahan ang mga halaman laban sa mga gustong sumira at kumain nito."),
            ],
        },
        {
            "id":    "S2P13",
            "type":  "dialogue",
            "bg":    "background/squashbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Naku Lucas! Dahil sa ginawang iyon ni baron, nauhaw ang ating mga halaman."),
            ],
        },
        {
            "id":    "S2P14",
            "type":  "dialogue",
            "bg":    "background/squashbg.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Malumanay nating diligan ito ng tubig."),
                ("lucas", "Dahan dahan at wag padalos dalos."),
            ],
        },
         # Action Challenge
        {
            "id": "S2P15",
            "type": "action_challenge",
            "bg": "background/squashbg.jpg",
            "overlay": "WaterCard.png",
            "dim_inactive": False,
        },
        {
            "id":    "S2P16",
            "type":  "dialogue",
            "bg":    "background/squashbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy"}},
            "lines": [
                ("chef", "Unti unti nang bumabalik ang sigla ng mga halaman."),
            ],
        },
        {
            "id":    "S2P17",
            "type":  "dialogue",
            "bg":    "background/squashbg.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Tama kayo Chef Pablo."),
                ("lucas", "Ngayon mas mabuting tutukan nating maigi ang paglago ng mga halaman."),
                ("lucas", "Mas mainam rin na mag lagay na tayo ng pampataba."),
            ],
        },
        {
            "id": "S2P18",
            "type": "scene",
            "bg": "background/baronsquashbg.jpg",
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
            "id":    "S2P19",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Hmmm... Ang mga patabang inyong gagamitin ay napakabagal!"),
                ("baron", "Mas mainam ang pampatabang gamit ko sa aking mga pananim"),
            ],
        },
        {
            "id":    "S2P20",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Tumigil ka Baron!"),
                ("lucas", "Masyado na po kayong nakakapinsala sa ating baryo at sa aming mga pananim."),
                ("lucas", "Kailan man ay hindi mo na kami malilinlang"),
            ],
        },
        {
            "id":    "S2P21",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"chef": {"side": "left", "expression": "angry", "flip": True}},
            "lines": [
                ("chef", "Kahit na ano pang sabihin mo hindi na kami maniniwala!"),
            ],
        },
        {
            "id":    "S2P22",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Naku! Kahit na basahin nyo pa ang nakalagay sa pampatabang ginagamit ko."),
                ("baron", "Walang kahit ano dyan ang makakapinsala sa inyong mga tanim."),
            ],
        },
        {
            "id":    "S2P23",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"chef": {"side": "left", "expression": "angry", "flip": True}},
            "lines": [
                ("chef", "Kahit na Baron! Alam kong may binabalak ka na namang masama."),
            ],
        },
        {
            "id":    "S2P24",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "defeated"}},
            "lines": [
                ("baron", "Grabe ka naman kung makapanghusga."),
                ("baron", "Gusto ko lang namang makatulong. Nararamdaman ko kasing nagbabago na ako dahil sa hindi ko rin naman kayang guluhin kayo. Ang espiritu ng kalikasan na yata ang bumabago sa akin."),
            ],
        },
        {
            "id":    "S2P25",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Pauumanhin po Baron."),
                ("lucas", "Pero kahit na ano pong sabihin nyo, ang hirap maniwala."),
                ("lucas", "Lalo nat nakikita ko sa iyong mga mata na hindi ka nagsisisi sa mga ginagawa mo."),
            ],
        },
        {
            "id":    "S2P26",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "defeated"}},
            "lines": [
                ("baron", "Sige na Lucas! Gusto ko lang namang makatulong."),
                ("baron", "Gamitin nyo na ang dala kong pampataba."),
            ],
        },
        {
            "id":    "S2P27",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Bigyan mo ako ng matinong dahilan para paniwalaan kita."),
            ],
        },
        {
            "id":    "S2P28",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Ang mga ito ay nag tataglay ng mga chemical na nagmamaniubra sa mga nutrisyon upang higit na makabenepisyo ang mga halaman sa dagdag nitong nutrisyon!"),
                ("baron", "Sa mas madaling salita, kemikal na pataba. Walang side effects, puro at subok ko na!"),
            ],
        },
        {
            "id":    "S2P29",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"chef": {"side": "left", "expression": "default", "flip": True}},
            "lines": [
                ("chef", "Mukhang wala namang masama sa bagay na ito Lucas."),
            ],
        },
        {
            "id":    "S2P30",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Hindi mo ako maloloko Baron! Alam kong nakakapaminsala yan ng mga organismo sa aking lupa na syang nagbibigay rin ng mga importanteng nutrisyon at proteksyon sa aking mga pananim!"),
            ],
        },
        {
            "id":    "S2P31",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "HAHAHAHA andami nyong satsat!"),
                ("baron", "Maghirap kayo dyang mag antay sa pagtubo nyan!"),
            ],
        },
        {
            "id": "S2P32",
            "type": "scene",
            "bg": "background/baronsquashbg.jpg",
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
            "id":    "S1P33",
            "type":  "dialogue",
            "bg":    "background/squashbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Magaling apo! Hindi ka nagpadaig sa mga sinasabi ni Baron."),
                ("lola", "Kailangang tandaan na ang pag gamit ng kemikal na pampataba ay hindi kinakailangan sa panahong lumalago pa ang mga pananim."),
                ("lola", "Mabisa ang mga ito ngunit meron din itong kaakibat na masamang epekto sa taniman. Lalong lalo na sa lupang tinataniman at sa mga hayop na nakatira sa ilog."),
                ("lola", "Ang labis na pag gamit ng kemikal na pataba ay nagdudulot ng pagkasunog ng mga ugat, dahon at mga binhi. Nagdudulot din ito ng soil acidification at nutrient imbalance."),
                ("lola", "Kaya ugaliing maging mapanuri at wag basta bastang gumamit ng mga kemikal na pataba. Kahit gaano ka tagal ang epekto ng mga organikong pataba, mas mainam parin ito dahil sa nagbibigay ito ng organic matter sa ating mga pananim."),
            ],
        },
        {
            "id":    "S2P34",
            "type":  "dialogue",
            "bg":    "background/squashbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "default", "flip": False}},
            "lines": [
                ("chef", "ngayon ay naiintindihan ko na kung ano ang ibig nyong sabihin sa ang pagtatanim ay nangangailangan ng mahabang pasensya at pagtatyaga."),
            ],
        },
        {
            "id":    "S2P35",
            "type":  "dialogue",
            "bg":    "background/squashbg.jpg",
            "chars": {"lucas": {"side": "right", "expression": "determined", "flip": False}},
            "lines": [
                ("lucas", "Mas mabuting hindi tayo maniwala agad sa mga sinasabi sa label ng mga kemikal na pataba. Ugaliing suriin at alamin ng mabuti ang mga ito."),
            ],
        },
        # ── Day 60 transition - Scene 3 ───────────────────────────────────
        {
            "id":   "day60_fade",
            "type": "transition",
        },
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "bg":    "background/squashmidbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Tignan mo Lucas malapit nang mahinog ang ating mga pananim na kalabasa!"),
            ],
        },
        {
            "id":    "S3P2",
            "type":  "dialogue",
            "bg":    "background/squashmidbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Nakakatuwa namang makita na ang ating sikap ay nag bubunga na!"),
            ],
        },
        {
            "id":    "S3P3",
            "type":  "dialogue",
            "bg":    "background/squashmidbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Ipagpatuloy lang natin ang ating ginagawang pagaalaga sa mga ito! Bunutin at linisin natin ang mga lantang dahon at mga sirang parte ng halaman para hindi maapektohan ang mga masisiglang parte."),
            ],
        },
        {
            "id": "S3P4",
            "type": "action_challenge",
            "bg": "background/squashmidbg.jpg",
            "overlay": "weedremovalcard.png",
            "dim_inactive": False,
        },
        {
            "id":    "S3P5",
            "type":  "dialogue",
            "bg":    "background/squashmidbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Ngayon antayin nalang nating mamunga ang mga ito para maluto ko na ang aking espesyal na Ginataang Kalabasa."),
            ],
        },
        {
            "id":    "S3P6",
            "type":  "dialogue",
            "bg":    "background/squashmidbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Puntahan muna natin si Lola Maria, mukhang may ipapatulong siya sa atin Chef Pablo."),
            ],
        },
        {
            "id":   "day60_fade",
            "type": "transition",
        },
        {
            "id": "S3P7",
            "type": "scene",
            "day": 60,
            "bg": "background/squashmidbg.jpg",
        },
        {
            "id": "S3P8",
            "type": "scene",
            "bg": "background/baronsquashmidbg.jpg",
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
            "id":    "S3P9",
            "type":  "dialogue",
            "bg":    "background/baronsquashmidbg.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Sinusubukan nyo talaga ang pasensya ko ha?"),
                ("baron", "Ngayon subukan nyong salbahin ito!"),
            ],
        },
        {
            "id": "S3P10",
            "type": "scene",
            "bg": "background/baronsquashmidbg.jpg",
            "shake": True,   
        },
        {
            "id": "S3P11",
            "type": "scene",
            "bg": "background/squashdrought.jpg",
            "shake": True,   
        },
        {
            "id":    "S3P12",
            "type":  "dialogue",
            "bg":    "background/squashdrought.jpg",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "HAHAHAHA! Hindi nyo na ito masasalba pa!"),
            ],
        },
        {
            "id": "S3P13",
            "type": "scene",
            "bg": "background/squashdrought.jpg",
            "shake": True,   
            "smoke": True,  

            "chars": {
                "baron": {
                    "side": "center",
                    "expression": "explosion",
                    "flip": False,
                },
            },
        },
        {
            "id": "S3P14",
            "type": "scene",
            "bg": "background/squashdroughtnew.jpg",
        },
        {
            "id":   "day60_fade",
            "type": "transition",
        },
        {
            "id":    "S3P15",
            "type":  "dialogue",
            "bg":    "background/squashdroughtnew.jpg",
            "chars": {"lucas": {"side": "left", "expression": "confused", "flip": True}},
            "lines": [
                ("lucas", "Anong nangyari dito?"),
            ],
        },
        {
            "id":    "S3P16",
            "type":  "dialogue",
            "bg":    "background/squashdroughtnew.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried", "flip": False}},
            "lines": [
                ("chef", "Mukhang lumaki ang araw! Naging mas mainit."),
            ],
        },
        {
            "id":    "S3P17",
            "type":  "dialogue",
            "bg":    "background/squashdroughtnew.jpg",
            "chars": {"lucas": {"side": "left", "expression": "wrong", "flip": True}},
            "lines": [
                ("lucas", "Anong gagawin natin ngayon?"),
            ],
        },
        {
            "id":    "S3P18",
            "type":  "dialogue",
            "bg":    "background/squashdroughtnew.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Bilis, basain muna natin ang lupa ng paunti unti."),
                ("lola", "Siguraduhing may sapat silang tubig."),
            ],
        },
        {
            "id": "S3P19",
            "type": "action_challenge",
            "bg": "background/squashdroughtnew.jpg",
            "overlay": "WaterCard.png",
            "dim_inactive": False,
        },
        {
            "id":    "S3P20",
            "type":  "dialogue",
            "bg":    "background/squashdroughtnew.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Takpan natin ng tuyong mga dahon ang lupa sa ilalim ng mga halaman."),
                ("lola", "Iwasan ang matatapang na pataba, at pangalagaan ang umuusbong nitong mga bunga."),
            ],
        },
        {
            "id":   "day60_fade",
            "type": "transition",
        },
        {
            "id": "S3P21",
            "type": "narration_overlay",
            "bg": "background/scenebg_night.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",

            "narration": (
                "Araw-araw, dinidiligan ni Lucas ang tanim. "
                "Banayad na patak lang, tulad ng pangako niya "
                "kay Lola. Sa loob ng 30 araw, nagbunga na  "
                "ang kanyang pagsisikap."
            ),
        },
        {
            "id":   "day60_fade",
            "type": "transition",
        },
        {
            "id": "S3P22",
            "type": "scene",
            "day": 70,
            "bg": "background/lucassquashbg1.jpg",
        },
        {
            "id":   "day70_fade",
            "type": "transition",
        },
        {
            "id": "S3P23",
            "type": "scene",
            "day": 80,
            "bg": "background/lucassquashbg2.jpg",
        },
        {
            "id":   "day80_fade",
            "type": "transition",
        },
        {
            "id":    "S3P20",
            "type":  "dialogue",
            "bg":    "background/squashgrownbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Magaling apo!"),
                ("lola", "Tuluyan nang nag bunga ang pagsisikap mo."),
                ("lola", "Lumago na ng mabuti ang mga halaman!"),
            ],
        },
        {
            "id":    "S3P16",
            "type":  "dialogue",
            "bg":    "background/squashgrownbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Salamat Lucas! Dahil sayo maluluto ko na muli ang aking ginataang Kalabasa!"),
            ],
        },
        {
            "id":    "S3P17",
            "type":  "dialogue",
            "bg":    "background/squashgrownbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "waters", "flip": True}},
            "lines": [
                ("lucas", "Walang anuman po Chef Pablo! Masaya po akong makakatulong na ako sa inyo!"),
            ],
        },
        {
            "id":    "S3P20",
            "type":  "dialogue",
            "bg":    "background/squashgrownbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Puwede na natin itong anihin!"),
            ],
        },
        {
            "id": "S4P8",
            "type": "action_challenge",
            "bg": "background/squashgrownbg.jpg",
            "overlay": "harvestcardscan.png",
            "dim_inactive": False,
        },
        {
            "id":   "day90_fade",
            "type": "transition",
        },
        {
            "id":    "S3P16",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "right", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Puwede na tayong mag luto!"),
            ],
        },
        {
            "id":   "day90_fade",
            "type": "transition",
        },
        {
            "id": "S3P23",
            "type": "scene",
            "day": 90,
            "bg": "background/squashcooking.jpg",
        },
        {
            "id":    "S3P20",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ano na ang pakiramdam mo Chef Pablo?"),
            ],
        },
        {
            "id":    "S3P16",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Naaalala ko na ang lahat ng aking mga ala-ala! Salamat Lola Maria! Salamat Lucas!"),
            ],
        },
        {
            "id":    "S3P17",
            "type":  "dialogue",
            "bg":    "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "waters", "flip": True}},
            "lines": [
                ("lucas", "Walang anuman po Chef Pablo! Masaya po akong makakatulong na ako sa inyo!"),
            ],
        },
        {
            "id":   "end_fade",
            "type": "transition",
        },
    ],
}
