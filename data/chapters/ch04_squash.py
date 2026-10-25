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
            "day":   1,
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
            "chars": {"baron": {"side": "right", "expression": "angry"}},
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
            "id": "S2P11",
            "type": "action_challenge",
            "bg": "background/squashbg.jpg",
            "overlay": "WaterCard.png",
            "dim_inactive": False,
        },
        {
            "id":    "S2P13",
            "type":  "dialogue",
            "bg":    "background/squashbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy"}},
            "lines": [
                ("chef", "Unti unti nang bumabalik ang sigla ng mga halaman."),
            ],
        },
        {
            "id":    "S2P14",
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
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Hmmm... Ang mga patabang inyong gagamitin ay napakabagal!"),
                ("baron", "Mas mainam ang pampatabang gamit ko sa aking mga pananim"),
            ],
        },
        {
            "id":    "S2P14",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Tumigil ka Baron!"),
                ("lucas", "Masyado na po kayong nakakapinsala sa ating baryo at sa aming mga pananim."),
                ("lucas", "Kailan man ay hindi mo na kami malilinlang"),
            ],
        },
        {
            "id":    "S2P13",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"chef": {"side": "left", "expression": "angry", "flip": "True"}},
            "lines": [
                ("chef", "Kahit na ano pang sabihin mo hindi na kami maniniwala!"),
            ],
        },
        {
            "id":    "S2P5",
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
            "id":    "S2P13",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"chef": {"side": "left", "expression": "angry", "flip": "True"}},
            "lines": [
                ("chef", "Kahit na Baron! Alam kong may binabalak ka na namang masama."),
            ],
        },
        {
            "id":    "S2P5",
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
            "id":    "S2P14",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": "True"}},
            "lines": [
                ("lucas", "Pauumanhin po Baron."),
                ("lucas", "Pero kahit na ano pong sabihin nyo, ang hirap maniwala."),
                ("lucas", "Lalo nat nakikita ko sa iyong mga mata na hindi ka nagsisisi sa mga ginagawa mo."),
            ],
        },
        {
            "id":    "S2P5",
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
            "id":    "S2P14",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": "True"}},
            "lines": [
                ("lucas", "Bigyan mo ako ng matinong dahilan para paniwalaan kita."),
            ],
        },
        {
            "id":    "S2P5",
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
            "id":    "S2P13",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"chef": {"side": "left", "expression": "default", "flip": "True"}},
            "lines": [
                ("chef", "Mukhang wala namang masama sa bagay na ito Lucas."),
            ],
        },
        {
            "id":    "S2P14",
            "type":  "dialogue",
            "bg":    "background/baronsquashbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": "True"}},
            "lines": [
                ("lucas", "Hindi mo ako maloloko Baron! Alam kong nakakapaminsala yan ng mga organismo sa aking lupa na syang nagbibigay rin ng mga importanteng nutrisyon at proteksyon sa aking mga pananim!"),
            ],
        },
        {
            "id":    "S2P5",
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
        # ── Day 60 transition - Scene 3 ───────────────────────────────────
        {
            "id":   "day60_fade",
            "type": "transition",
        },
    ],
}
