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
            "logo": "logos/ch1logo.png",
        },

        # ── Panel 1 — Baron raises the stakes ─────────────────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Siyam na alaala na lang, at maaari akong manalo! Ngunit... ngunit hindi pa rin iyan MAGIGING! Patakbuhin ko ang hangin laban sa inyo!"),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "left"},
            "lines": [
                ("chef", "Mais! Mais na nilalagyan ko ng mantikilya at dinudurog para sa mais soup, at sinisimula ng Lucas na lutuin para sa pamilya..."),
            ],
        },
        {
            "id":    "S1P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Lola Chef, makaka-daya ba ang hangin sa mais? Ano ang dapat nating gawin para protektahan ito?"),
            ],
        },
        {
            "id":    "S1P4",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "left"},
            "lines": [
                ("chef", "Ang mais ay kailangan ng matibay na paa sa lupa para hindi matumba ng hangin. Kailangan ng malalim na bungkal at mataas na tumpok ng lupa sa paligid ng puno."),
            ],
        },

        # ── Panel 2 — Wind-ready furrows: tool choice (TIMER) ─
        {
            "id":    "S2P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Bungkalin natin nang malalim ang mga hilera para lumusog ang ugat — at mabilis, si Baron ay gumagalaw pa rin!"),
            ],
        },
        {
            "id":            "S2P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Alin ang tamang kagamitan para gumawa ng malalim na furrow para sa tanim ng mais?",
            "retry_question": "Mabilis! Anong kagamitan ang para sa malalim na bungkal ng lupa?",
            "choices": [
                {"img": "buttons/choice_hoe.png",    "label": "Asarol — malalim na bungkal ng lupa"},
                {"img": "buttons/choice_trowel.png", "label": "Sprayer — pandilig"},
            ],
            "correct": 0,
        },
        {
            "id":          "S2P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama at mabilis! Ang Asarol ang para sa malalim na furrow — ibabaw na ito sa paglakas ng ugat ng mais laban sa hangin ni Baron!"),
            ],
        },
        {
            "id":               "S2P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Ang Sprayer ay para sa tubig, hindi para sa paghukay ng malalim na furrow. Piliin ang tamang kagamitan!"),
            ],
        },

        # ── Day 1 transition ───────────────────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },

        # ── Panel 3 — Deep watering scan (TIMER) ──────────────
        {
            "id":       "S3P1",
            "type":     "scan",
            "day":      1,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-01 Water Card",
            "dialogue": "Lucas: Diligan nang malalim ang mga buto — kailangan ng malusog na ugat para hindi matumba ng hangin. I-scan ngayon, bilis!",
            "question": "Scan the Water Card to water the corn seeds deeply to build strong roots against Baron's wind.",
        },

        # ── Day 35 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day35_fade",
            "type": "transition",
        },

        # ── Panel 4 — Side-dressing placement ─────────────────
        {
            "id":    "S4P1",
            "type":  "dialogue",
            "day":   35,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "left"},
            "lines": [
                ("chef", "Sa ikaanim na dahon, oras na para sa side-dressing — pagdaragdag ng pataba sa gilid ng puno, hindi sa gitna, para hindi masunog ang ugat."),
            ],
        },
        {
            "id":            "S4P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Saan dapat ilagay ang side-dressing fertilizer sa puno ng mais?",
            "retry_question": "Isipin muli! Saan ang tamang lugar para ilagay ang pataba sa mais para hindi masunog ang ugat?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Sa gilid — hindi sa ugat mismo"},
                {"img": "buttons/choice_hoe.png",    "label": "Sa gitna ng puno, sa ugat mismo"},
            ],
            "correct": 0,
        },
        {
            "id":          "S4P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef_thumbs": "left"},
            "lines": [
                ("chef_thumbs", "Tama! Ang pataba sa gitna ng ugat ay maaaring masunog ang mais. Sa gilid — dalawang pulgada — ang tamang posisyon!"),
            ],
        },
        {
            "id":               "S4P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"chef_wrong": "left"},
            "lines": [
                ("chef_wrong", "Ang direktang paglalagay ng pataba sa ugat ay maaaring masunog ang ating mais! Sa gilid lang, hindi sa gitna ng puno!"),
            ],
        },

        # ── Panel 5 — Side-dressing apply (TIMER) ─────────────
        {
            "id":            "S5P1",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":       "Alin ang tamang kagamitan para maingat na mag-side-dress ng pataba sa gilid ng mais?",
            "retry_question": "Mabilis! Alin ang naglalagay ng pataba nang tumpak sa tamang lugar?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Dulo — maingat sa gilid ng puno"},
                {"img": "buttons/choice_hoe.png",    "label": "Asarol — masyadong malawak"},
            ],
            "correct": 0,
        },
        {
            "id":          "S5P1_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lucas_thumbs": "left"},
            "lines": [
                ("lucas_thumbs", "Tama at mabilis! Ang Dulo ang tamang kagamitan para maingat na mag-side-dress sa tamang posisyon!"),
            ],
        },
        {
            "id":               "S5P1_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Ang Asarol ay masyadong malawak para sa side-dressing. Kailangan ng mas tumpak na kagamitan para hindi masira ang mais!"),
            ],
        },

        # ── Day 40 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day40_fade",
            "type": "transition",
        },

        # ── Panel 6 — Weed removal scan: before hilling up (TIMER) ──
        {
            "id":       "S6P1",
            "type":     "scan",
            "day":      40,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-03 Weed Removal Card",
            "dialogue": "Lucas: Alisin natin muna ang damo bago itambak ang lupa paitaas sa puno (hilling up) — suporta laban sa hangin! I-scan, bilis!",
            "question": "Scan the Weed Removal Card to clear the weeds before hilling up the corn for wind support.",
        },

        # ── Day 58 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day58_fade",
            "type": "transition",
        },

        # ── Panel 7 — Wind pollination (don't wash pollen) ────
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   58,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Dilugan niyo ang mais! Hugasan ang mga bulaklak! O hindi, ipapalakad ko ang hangin para matanggal lahat ng pollen!"),
            ],
        },
        {
            "id":    "S7P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "left"},
            "lines": [
                ("chef", "Huwag diligan ngayong umaga — gumagalaw ang pollen ng mais sa tulong ng hangin, hindi ng tubig. Kung mabasa ang pollen, hindi na ito makakarating sa mais!"),
            ],
        },
        {
            "id":            "S7P3",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Bakit hindi dapat diligan ang mais sa umaga habang namumukadkad ang bulaklak nito?",
            "retry_question": "Isipin muli! Ano ang mangyayari sa pollen ng mais kung mabasa ito bago makarating sa mais?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Mabibigo ang pollination — ang pollen ay para sa hangin"},
                {"img": "buttons/choice_hoe.png",    "label": "Mabuti ang tubig — mas maraming mais"},
            ],
            "correct": 0,
        },
        {
            "id":          "S7P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef_thumbs": "left"},
            "lines": [
                ("chef_thumbs", "Tama! Ang mais ay wind-pollinated — kailangan ng tuyo at malinis na pollen para makarating sa bawat butil. Gabing pagdidilig, hindi umaga!"),
            ],
        },
        {
            "id":               "S7P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"chef_wrong": "left"},
            "lines": [
                ("chef_wrong", "Ang basang pollen ay hindi makakarating sa mais — mabibigo ang pollination at magiging walang butil ang ating mais. Huwag diligan sa umaga!"),
            ],
        },

        # ── Day 65 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day65_fade",
            "type": "transition",
        },

        # ── Panel 8 — Brown silk trivia ────────────────────────
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   65,
            "bg":    "background/scenebg_planter.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Tingnan ang buhok ng mais, apo — kapag kumupas na at naging kulay-kayumanggi ang lahat ng seda nito, ibig sabihin, matagumpay na ang pollination."),
            ],
        },
        {
            "id":            "S8P2",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "question":       "Ano ang ibig sabihin ng lahat ng mais silk (buhok) na kumukulay kayumanggi?",
            "retry_question": "Isipin muli! Ang mais silk ay nagbibigay ng senyales — ano ang mensahe nito?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Matagumpay ang pollination — lumaki ang butil"},
                {"img": "buttons/choice_hoe.png",    "label": "Namatay ang mais — alisin na ito"},
            ],
            "correct": 0,
        },
        {
            "id":          "S8P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Tama! Ang kayumangging seda ay ibig sabihin, bawat butil ay nakatanggap ng pollen at lumalaki na ang butil sa loob ng mais. Maayos tayo!"),
            ],
        },
        {
            "id":               "S8P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Hindi! Ang kumukulay na seda ay hudyat ng matagumpay na pollination — lumalaki na ang mga butil sa loob ng mais. Huwag itanggal!"),
            ],
        },

        # ── Day 70 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day70_fade",
            "type": "transition",
        },

        # ── Panel 9 — Pesticide choice: Natural vs Chemical (TIMER) ──
        {
            "id":    "S9P1",
            "type":  "dialogue",
            "day":   70,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Mga corn borers — ang aking pinakamagandang sandata! Kainin na ang mga butil mula sa loob ng mais!"),
            ],
        },
        {
            "id":    "S9P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_planter.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Corn borers — kailangan agad ng aksyon! Alin ang gagamitin nating pestisidyo, Chef?"),
            ],
        },
        {
            "id":       "S9P3",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-04 Pesticide Card",
            "dialogue": "I-scan ang Pesticide Card para piliin ang tamang pestisidyo laban sa corn borers — bilis!",
            "question": "Scan the Pesticide Card to choose the natural pesticide against corn borers.",
        },

        # ── Day 80 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day80_fade",
            "type": "transition",
        },

        # ── Panel 10 — Kernel plumping water scan (TIMER) ─────
        {
            "id":       "S10P1",
            "type":     "scan",
            "day":      80,
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-01 Water Card",
            "dialogue": "Lucas: Ang mga butil ng mais ay puno na ng gatas — kailangan ng tubig para maging malusog at malaki ang bawat butil. I-scan, bilis!",
            "question": "Scan the Water Card to water the corn during kernel plumping stage for full, juicy kernels.",
        },

        # ── Day 95 transition (TIME SKIP) ─────────────────────
        {
            "id":   "day95_fade",
            "type": "transition",
        },

        # ── Panel 11 — Harvest scan (TIMER) ───────────────────
        {
            "id":    "S11P1",
            "type":  "dialogue",
            "day":   95,
            "bg":    "background/scenebg_planter.png",
            "chars": {"chef": "left"},
            "lines": [
                ("chef", "Tingnan — ang seda ay kulay-kayumanggi na, ang mga butil ay masikip at maliwanag... oras na, Lucas!"),
            ],
        },
        {
            "id":            "S11P2_choice",
            "type":          "choice",
            "bg":            "background/scenebg_planter.png",
            "timer":         True,
            "question":      "Alin ang tamang Mais na handa nang anihin? (30 segundo!)",
            "retry_question": "Mabilis! Ang tamang Mais ay may kayumangging seda at masikip na maliwanag na butil — hindi puti pa ang seda.",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Kayumanggi na seda, masikip at maliwanag na butil"},
                {"img": "buttons/choice_hoe.png",    "label": "Puti pa ang seda, berde pa ang balot"},
            ],
            "correct": 0,
        },
        {
            "id":          "S11P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef_thumbs": "right"},
            "lines": [
                ("chef_thumbs", "Tama at mabilis! Kayumanggi na ang seda, masikip ang butil — oras na talaga para mag-ani!"),
            ],
        },
        {
            "id":               "S11P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Hindi pa! Kailangan pang maging kayumanggi ang seda at maging masikip ang butil. Mabilis — subukan ulit!"),
            ],
        },
        {
            "id":       "S11P2",
            "type":     "scan",
            "bg":       "background/scenebg_planter.png",
            "chars":    {"lucas": "left"},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-05 Harvest Card",
            "dialogue": "Napili mo na ang tamang Mais! I-scan ang Harvest Card para ma-confirm ang pag-aani — bilis!",
            "question": "Scan the Harvest Card to confirm the corn with brown silks and plump, shiny kernels is ready to harvest.",
        },

        # ── Panel 12 — Wet storage danger ─────────────────────
        {
            "id":    "S12P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Itago agad ang mais na basa — bilisan niyo! Baka masira pa ang inyong ani!"),
            ],
        },
        {
            "id":    "S12P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Huwag, apo! Ang mais ay dapat matuyo muna nang mabuti bago itago — kung hindi, aamagin at mababawasan ang kalidad ng mais natin."),
            ],
        },
        {
            "id":            "S12P3",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Totoo ba na ang mais ay kailangan munang matuyo bago itago para maiwasan ang amag?",
            "retry_question": "Isipin muli! Ano ang mangyayari sa mais kung itatago ito habang basa pa?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Totoo — maiwasan ang amag at pagkasira"},
                {"img": "buttons/choice_hoe.png",    "label": "Mali — diretso itago habang basa"},
            ],
            "correct": 0,
        },
        {
            "id":          "S12P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"lola_thumbs": "left"},
            "lines": [
                ("lola_thumbs", "Tama! Ang mais ay dapat mababa ang moisture content — 13-14% — bago itago para maiwasan ang amag at pagkasira."),
            ],
        },
        {
            "id":               "S12P3_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"lucas_wrong": "right"},
            "lines": [
                ("lucas_wrong", "Huwag maniwala kay Baron! Ang basang mais sa saradong lalagyan ay aamagin at lalasunin ang lahat. Ipatuyo muna!"),
            ],
        },

        # ── Day 100 transition (TIME SKIP) ────────────────────
        {
            "id":   "day100_fade",
            "type": "transition",
        },

        # ── Panel 13 — Ventilated storage ─────────────────────
        {
            "id":    "S13P1",
            "type":  "dialogue",
            "day":   100,
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "left"},
            "lines": [
                ("chef", "Pag-usapan natin ang tamang pag-iimbak ng mais. Ano ang pinakamabuting paraan para manatiling sariwa at ligtas ang mais natin?"),
            ],
        },
        {
            "id":            "S13P2",
            "type":          "choice",
            "bg":            "background/scenebg_default.png",
            "question":       "Paano dapat itago ang tuyong mais para maiwasan ang amag at insekto?",
            "retry_question": "Isipin muli! Paano natin mapipigilan ang amag at insekto sa ating tuyong mais?",
            "choices": [
                {"img": "buttons/choice_trowel.png", "label": "Mahangin na lalagyan — may daloy ng hangin"},
                {"img": "buttons/choice_hoe.png",    "label": "Kulob na lalagyan — walang hangin"},
            ],
            "correct": 0,
        },
        {
            "id":          "S13P2_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef_thumbs": "left"},
            "lines": [
                ("chef_thumbs", "Tama! Ang mahangin na imbakan ay nagpoprotekta sa mais mula sa amag at insekto. Mahalaga ang tamang daloy ng hangin sa pag-iimbak!"),
            ],
        },
        {
            "id":               "S13P2_wrong_1",
            "type":             "feedback",
            "if_correct":       False,
            "random_pick":      True,
            "retry_to_choice":  True,
            "bg":               "background/scenebg_wrong.png",
            "chars":            {"chef_wrong": "left"},
            "lines": [
                ("chef_wrong", "Ang kulob na lalagyan ay nagpapalakas ng amag at init sa mais — mas lalong mabibigo ang ating ani. Kailangan ng daloy ng hangin!"),
            ],
        },

        # ── Panel 14 — Baron panics ────────────────────────────
        {
            "id":    "S14P1",
            "type":  "dialogue",
            "day":   102,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": "right"},
            "lines": [
                ("baron", "Siyam... siyam na na alaala! Paano ito nangyari?! Wala akong natapos na harang — lahat ng plano ko ay nabigo!"),
                ("baron", "Isang alaala na lang... ISANG ALAALA NA LANG ang nagpoprotekta sa akin!"),
            ],
        },
        {
            "id":    "S14P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Lola, natitingnan ko na ang iyong mukha... mas malinaw na ito ngayon kaysa dati. Halos lahat ay naaalala ko na tungkol sa ating pamilya."),
            ],
        },
        {
            "id":    "S14P3",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": "left"},
            "lines": [
                ("lola", "Huminto muna tayo at makinig — mukhang may ibang nangyayari kay Baron kaysa sa iniisip natin, apo."),
            ],
        },

        # ── Panel 15 — End: Mais memory ───────────────────────
        {
            "id":    "S15P1",
            "type":  "dialogue",
            "day":   102,
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": "left"},
            "lines": [
                ("chef", "Mais! Ang mais soup, ang inihaw na mais sa tabi ng ilog, ang popcorn sa Pista ng Baryo... Naaalala ko na ang lahat ng lutuin ko para sa baryo!"),
            ],
        },
        {
            "id":    "S15P2",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": "left"},
            "lines": [
                ("lucas", "Siyam! Isang alaala na lang ang natitirang nakalimutan, Lola. Halos magtagumpay na tayo — at halos magsimula nang umiyak si Baron."),
                ("lucas", "Mais Memory — UNLOCKED!"),
            ],
        },

    ],
}
