# ============================================================
#  CHAPTER 7 — SWEET POTATO (Kamote)
#  Intermediate | Story chapter | Total growing days: 120
#  Characters: Lucas, Chef Pablo, Lola Maria, Blight Baron
#  NEW MECHANICS: Vine Cuttings, Wood Ash Application, Tuber Checks
# ============================================================

CHAPTER = {
    "id":         "ch07",
    "crop":       "Sweet Potato",
    "level":      "intermediate",
    "memory":     "Kamote Cue Memory",
    "total_days": 120,

    "slides": [

        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/kitchenbg.jpg",
            "logo": "chapter7.png",
        },

        # ── Scene 1: A familiar smell ──────────────────────────
        {
            "id":   "S1P1",
            "type": "dialogue",
            "bg":   "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Lucas, may naaalala akong amoy mula sa pista noong bata pa ako. Matamis, mainit, at parang bagong luto."),
                ("chef", "Pero kapag sinusubukan kong alalahanin kung ano iyon, nawawala rin agad sa isip ko."),
            ],
        },
        {
            "id":   "S1P2",
            "type": "dialogue",
            "bg":   "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Baka may kinalaman iyon sa isa sa mga pagkaing inihahanda ninyo tuwing pista."),
                ("lucas", "Ano pa po ang naaalala ninyo? Kahit maliit na detalye lang."),
            ],
        },
        {
            "id":   "S1P3",
            "type": "dialogue",
            "bg":   "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "confused"}},
            "lines": [
                ("chef", "May mga batang naghihintay sa tabi ng kawali. May hawak silang maliliit na patpat, at tuwang-tuwa sila sa bawat pirasong inilalabas ko."),
                ("chef", "Parang may asukal na kumakapit sa labas ng pagkain... Kamote ba iyon?"),
            ],
        },
        {
            "id":   "S1P4",
            "type": "dialogue",
            "bg":   "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("lola", "Kamote Cue! Paborito iyan ng mga bata tuwing pista."),
                ("lola", "Chef Pablo, ikaw ang naghahanda niyan noon. Madalas, nauubos pa bago matapos ang programa."),
            ],
        },
        {
            "id":   "S1P5",
            "type": "dialogue",
            "bg":   "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "surprised"}},
            "lines": [
                ("chef", "Kamote Cue... Pamilyar nga ang pangalan."),
                ("chef", "Gusto kong maalala kung paano ko iyon ginagawa. Pero wala na tayong sapat na kamote sa kusina."),
            ],
        },
        {
            "id":   "S1P6",
            "type": "dialogue",
            "bg":   "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "May itatanim tayong kamote sa likod ng bahay. Hindi natin kailangang magsimula sa buto; maaari tayong gumamit ng malulusog na bahagi ng baging."),
                ("lola", "Kung aalagaan natin ito, magkakaroon tayo ng sariling aanihin pagdating ng panahon."),
            ],
        },
        {
            "id":   "S1P7",
            "type": "dialogue",
            "bg":   "background/scenebg_default.png",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Tutulungan namin kayo, Lola. Chef, ihanda po natin ang taniman."),
                ("lucas", "Pero bago tayo magsimula, kailangan nating pumili ng tamang pantanim."),
            ],
        },

        # ── Choice: identify the planting material ─────────────
        {
            "id": "S1P8",
            "type": "choice",
            "bg": "background/scenebg_default.png",
            "question": "Ano ang pinakamainam na gamitin sa pagpaparami ng kamote?",
            "retry_question": "Hindi lahat ng bahagi ng halaman ay magandang pantanim. Maghanap ng malusog na baging na may mga buhol o nodes.",
            "choices": [
                {"img": "buttons/choice_sweetpotato_vine.png", "label": "Malusog na baging", "frame": True},
                {"img": "buttons/choice_dry_leaf.png", "label": "Tuyong dahon", "frame": True},
            ],
            "correct": 0,
        },
        {
            "id": "S1P9_right",
            "type": "feedback",
            "if_correct": True,
            "bg": "background/scenebg_right.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Tama! Karaniwang pinatutubo ang kamote mula sa mga pinagputulang baging."),
                ("lucas", "Pumili tayo ng malusog na baging na may ilang buhol dahil dito maaaring tumubo ang mga ugat at bagong dahon."),
            ],
        },
        {
            "id": "S1P10_wrong",
            "type": "feedback",
            "if_correct": False,
            "retry_to_choice": True,
            "bg": "background/scenebg_wrong.png",
            "chars": {"chef": {"side": "right", "expression": "confused"}},
            "lines": [
                ("chef", "Hindi yata magiging maayos na pantanim ang tuyong dahon. Kailangan natin ng bahaging may kakayahang tumubo."),
                ("chef", "Subukan nating piliin ang malusog na baging."),
            ],
        },
        {
            "id":   "S1P11",
            "type": "dialogue",
            "bg":   "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Magaling. Pumili tayo ng mga baging na walang palatandaan ng sakit o matinding pinsala."),
                ("lola", "Mas mainam ding ihanda muna ang lupa upang madaling kumalat ang mga ugat at lumaki ang mga tuber sa ilalim."),
            ],
        },
        {
            "id":   "S1P12",
            "type": "dialogue",
            "bg":   "background/scenebg_default.png",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Aayusin ko po ang lupa at aalisin ang malalaking bato. Pagkatapos, maaari na nating itanim ang mga pinagputulang baging."),
                ("lucas", "Saan po ba dapat nakabaon ang mga ito?"),
            ],
        },
        {
            "id": "S1P13",
            "type": "dialogue",
            "bg": "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ibaon ang ilang buhol sa mamasa-masang lupa at hayaang may bahagi ng baging na nakalitaw."),
                ("lola", "Huwag siksikin ang tanim. Kailangan nito ng sapat na espasyo para gumapang at lumago."),
            ],
        },
        {
            "id": "S1P14",
            "type": "action_challenge",
            "bg": "background/scenebg_default.png",
            "overlay": "sweetpotatoplantingcard.png",
            "dim_inactive": False,
        },
        {
            "id":   "S1P15",
            "type": "dialogue",
            "bg":   "background/sweetpotatobed.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy"}},
            "lines": [
                ("chef", "Ayan, maayos na ang pagkakatanim. Hindi ko akalaing baging lang pala ang kailangan natin para makapagsimula."),
                ("chef", "Ano naman ang dapat nating gawin habang hindi pa lumalago ang mga ito?"),
            ],
        },
        {
            "id":   "S1P16",
            "type": "dialogue",
            "bg":   "background/sweetpotatobed.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Panatilihing mamasa-masa ang lupa habang nag-uugat ang mga pinagputulan, pero huwag itong bahain."),
                ("lola", "Tingnan din natin nang regular kung may damo o peste. Mas madaling maagapan ang problema kapag maaga natin itong napansin."),
            ],
        },
        {
            "id": "day0_fade",
            "type": "transition",
        },

        # ── Scene 2: Early growth, day 15 ───────────────────────
        {
            "id": "S2P1",
            "type": "narration_overlay",
            "day": 15,
            "bg": "background/sweetpotatosprout.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",
            "narration": (
                "Lumipas ang labinlimang araw. Nagsimula nang "
                "maglabasan ang mga bagong dahon mula sa mga "
                "buhol ng baging. Araw-araw itong sinusuri nina "
                "Lucas at Chef Pablo upang matiyak na maayos ang "
                "pag-uugat ng mga tanim."
            ),
        },
        {
            "id": "S2P2",
            "type": "dialogue",
            "day": 15,
            "bg": "background/sweetpotatosprout.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy"}},
            "lines": [
                ("chef", "Lucas, tingnan mo! May mga bagong dahon na. Mukhang kumakapit na sa lupa ang mga pinagputulan."),
                ("chef", "Kung ganito kabilis, baka makapag-ani na tayo agad."),
            ],
        },
        {
            "id": "S2P3",
            "type": "dialogue",
            "bg": "background/sweetpotatosprout.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Magandang senyales po iyan, Chef, pero hindi pa ibig sabihin na handa nang anihin ang kamote."),
                ("lucas", "Kailangan pa nitong panahon para lumaki ang mga ugat na magiging tuber."),
            ],
        },
        {
            "id": "S2P4",
            "type": "scene",
            "bg": "background/baronsweetpotato.jpg",
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
            "id": "S2P5",
            "type": "dialogue",
            "bg": "background/baronsweetpotato.jpg",
            "dark": True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Napakasaya ninyo sa ilang dahon? Akala ninyo ba sapat na iyan para mapuno ang inyong mga palayok?"),
                ("baron", "Tingnan natin kung ganyan pa rin kayo kasigla kapag sinubukan kong guluhin ang inyong taniman!"),
            ],
        },
        {
            "id": "S2P6",
            "type": "scene",
            "bg": "background/sweetpotatopest.jpg",
            "shake": True,
        },
        {
            "id": "S2P7",
            "type": "dialogue",
            "bg": "background/sweetpotatopest.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Naku! May mga insektong kumakain sa mga dahon. Kapag dumami pa ang mga ito, hihina ang ating mga tanim."),
            ],
        },
        {
            "id": "S2P8",
            "type": "dialogue",
            "bg": "background/sweetpotatopest.jpg",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Huwag po tayong mataranta, Chef. Suriin muna natin kung aling mga dahon ang may pinsala at kung anong peste ang naroon."),
                ("lucas", "Aalisin natin ang mga peste na nakikita at gagamit lamang ng angkop na paraan ng pagkontrol."),
            ],
        },
        {
            "id": "S2P9",
            "type": "action_challenge",
            "bg": "background/sweetpotatopest.jpg",
            "overlay": "pestinspectioncard.png",
            "dim_inactive": False,
        },
        {
            "id": "S2P10",
            "type": "dialogue",
            "bg": "background/sweetpotatobed.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Mabuti at maagap ninyong nasuri ang mga dahon. Ipagpatuloy natin ang regular na pagtingin sa ilalim at ibabaw ng mga ito."),
                ("lola", "Huwag basta magwisik ng anumang panlaban sa peste. Dapat alam muna natin kung ano ang problema at kung ligtas gamitin ang paraan na pipiliin natin."),
            ],
        },
        {
            "id": "S2P11",
            "type": "dialogue",
            "bg": "background/sweetpotatobed.jpg",
            "chars": {"chef": {"side": "right", "expression": "default"}},
            "lines": [
                ("chef", "Naiintindihan ko. Hindi sapat na basta may gawin tayo; kailangan ding tama ang gagawin natin."),
                ("chef", "Sige, babantayan ko ang mga dahon habang lumalaki ang mga baging."),
            ],
        },

        # ── Scene 3: Feeding the crop, day 35 ───────────────────
        {
            "id": "day35_fade",
            "type": "transition",
        },
        {
            "id": "S3P1",
            "type": "narration_overlay",
            "day": 35,
            "bg": "background/sweetpotatogrowth1.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",
            "narration": (
                "Pagsapit ng ika-35 araw, mas mahaba na ang mga "
                "baging at mas malawak na ang mga dahon. Maayos "
                "ang paglago ng tanim, ngunit nais ni Chef Pablo "
                "na matiyak na sapat ang sustansiyang nakukuha "
                "nito habang patuloy na umuunlad ang mga ugat."
            ),
        },
        {
            "id": "S3P2",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth1.jpg",
            "chars": {"chef": {"side": "right", "expression": "confused"}},
            "lines": [
                ("chef", "Lola, kailangan ba nating lagyan ng pataba ang kamote? Ayokong magkulang ito sa sustansiya."),
                ("chef", "May nakita akong abo mula sa malinis na kahoy. May silbi ba iyon sa ating taniman?"),
            ],
        },
        {
            "id": "S3P3",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth1.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "May potassium ang abo mula sa malinis at hindi pininturahang kahoy. Maaari itong makatulong sa lupa, pero hindi ito dapat basta-basta ikalat."),
                ("lola", "Maaaring tumaas ang pH ng lupa kapag nasobrahan ang abo. Kaya kaunti lamang ang gagamitin natin, at hindi ito angkop sa lahat ng uri ng lupa."),
            ],
        },
        {
            "id": "S3P4",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth1.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Ibig sabihin po, kailangan muna nating tiyakin na malinis ang pinanggalingan ng abo at tama ang dami bago ito ilagay."),
                ("lucas", "Hindi tayo gagamit ng abo mula sa pininturahan o ginamot na kahoy, basura, o anumang materyal na maaaring may mapanganib na kemikal."),
            ],
        },
        {
            "id": "S3P5",
            "type": "scene",
            "bg": "background/baronsweetpotato.jpg",
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
            "id": "S3P6",
            "type": "dialogue",
            "bg": "background/baronsweetpotato.jpg",
            "dark": True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Abo? Iyan ang plano ninyo? Napakaliit ng pag-asa ninyong makakuha ng malaking ani!"),
                ("baron", "Gamitin ninyo ang lahat ng dala kong pampabilis. Hindi na ninyo kailangang maghintay!"),
            ],
        },
        {
            "id": "S3P7",
            "type": "dialogue",
            "bg": "background/baronsweetpotato.jpg",
            "chars": {"chef": {"side": "left", "expression": "angry", "flip": True}},
            "lines": [
                ("chef", "Hindi kami basta gagamit ng kung anu-ano dahil lang nangangako kang bibilis ang paglaki ng tanim."),
                ("chef", "Gusto naming matutunan kung paano ito alagaan nang tama."),
            ],
        },
        {
            "id": "S3P8",
            "type": "dialogue",
            "bg": "background/baronsweetpotato.jpg",
            "dark": True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Kung ganoon, subukan ninyong alagaan ang inyong mga baging nang walang tulong ko. Tingnan natin kung may aanihin kayo!"),
            ],
        },
        {
            "id": "S3P9",
            "type": "scene",
            "bg": "background/sweetpotatogrowth1.jpg",
        },
        {
            "id": "S3P10",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth1.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Huwag nating hayaang madaliin tayo ni Baron. Kung gagamit tayo ng abo, siguraduhin muna nating angkop ito sa lupa at kaunti lamang ang ilalagay."),
                ("lola", "Iwasang ilagay ito nang dikit sa mga baging. Ikalat nang pantay sa lupa ayon sa pangangailangan, at huwag itong gawing kapalit ng lahat ng ibang sustansiya."),
            ],
        },
        {
            "id": "S3P11",
            "type": "action_challenge",
            "bg": "background/sweetpotatogrowth1.jpg",
            "overlay": "woodashcard.png",
            "dim_inactive": False,
        },
        {
            "id": "S3P12",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth1.jpg",
            "chars": {"lucas": {"side": "right", "expression": "happy"}},
            "lines": [
                ("lucas", "Maayos ang pagkakalagay natin. Natutuhan natin na hindi paramihan ng pataba ang sikreto sa magandang tanim."),
                ("lucas", "Mas mahalaga ang pag-alam kung ano ang kailangan ng lupa at kung gaano lamang karami ang nararapat."),
            ],
        },
        {
            "id": "S3P13",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth1.jpg",
            "chars": {"chef": {"side": "left", "expression": "happy", "flip": True}},
            "lines": [
                ("chef", "Kung ganoon, patuloy nating aalagaan ang mga ito. Hindi naman kailangang madaliin ang lahat."),
            ],
        },

        # ── Scene 4: The vines spread, day 60 ───────────────────
        {
            "id": "day60_fade",
            "type": "transition",
        },
        {
            "id": "S4P1",
            "type": "narration_overlay",
            "day": 60,
            "bg": "background/sweetpotatogrowth2.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",
            "narration": (
                "Pagsapit ng ika-60 araw, gumapang na sa paligid "
                "ng taniman ang mahahabang baging. Naging mas "
                "makapal ang mga dahon at natakpan na ang malaking "
                "bahagi ng lupa. Patuloy na nag-aalis ng damo at "
                "nagsusuri ng peste sina Lucas at Chef Pablo."
            ),
        },
        {
            "id": "S4P2",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth2.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy"}},
            "lines": [
                ("chef", "Ang lawak na ng mga baging! Halos natatakpan na nila ang buong taniman."),
                ("chef", "Ibig bang sabihin nito ay malalaki na rin ang mga kamote sa ilalim?"),
            ],
        },
        {
            "id": "S4P3",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth2.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Hindi pa natin masasabi base sa dami ng dahon lang, Chef. Ang mga tuber ay nasa ilalim ng lupa, kaya kailangan natin silang bigyan pa ng panahon."),
                ("lucas", "Patuloy lang po nating alagaan ang tanim at iwasang masugatan ang mga ugat kapag naglilinis sa paligid."),
            ],
        },
        {
            "id": "S4P4",
            "type": "scene",
            "bg": "background/baronsweetpotato.jpg",
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
            "id": "S4P5",
            "type": "dialogue",
            "bg": "background/baronsweetpotato.jpg",
            "dark": True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Hindi pa rin kayo sumusuko? Kung hindi ko kayo mapapahinto, sisirain ko ang tanim na ipinagmamalaki ninyo!"),
            ],
        },
        {
            "id": "S4P6",
            "type": "scene",
            "bg": "background/sweetpotatobed.jpg",
            "shake": True,
        },
        {
            "id": "S4P7",
            "type": "dialogue",
            "bg": "background/sweetpotatobed.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "May ilang bahagi ng taniman na natabunan ng damo. Kapag pinabayaan natin, baka makipag-agawan ito sa tubig at sustansiya ng kamote."),
            ],
        },
        {
            "id": "S4P8",
            "type": "dialogue",
            "bg": "background/sweetpotatobed.jpg",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Aalisin natin ang mga damo, pero maingat lang. Huwag nating hilahin nang malakas ang mga baging o hukayin ang paligid dahil baka masugatan ang mga tuber."),
            ],
        },
        {
            "id": "S4P9",
            "type": "action_challenge",
            "bg": "background/sweetpotatobed.jpg",
            "overlay": "weedremovalcard.png",
            "dim_inactive": False,
        },
        {
            "id": "S4P10",
            "type": "dialogue",
            "bg": "background/sweetpotatobed.jpg",
            "chars": {"lola": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("lola", "Maayos ang ginawa ninyo. Kapag malinis ang paligid, mas madaling makita kung may peste o sakit na kailangang tugunan."),
                ("lola", "Tandaan, hindi kailangang galawin nang galawin ang lupa sa paligid ng kamote. Maraming bahagi ng ani ang nabubuo sa ilalim nito."),
            ],
        },

        # ── Scene 5: Learning to read the soil, day 90 ─────────
        {
            "id": "day90_fade",
            "type": "transition",
        },
        {
            "id": "S5P1",
            "type": "narration_overlay",
            "day": 90,
            "bg": "background/sweetpotatogrowth3.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",
            "narration": (
                "Siyamnapung araw na ang lumipas. Masigla pa rin "
                "ang mga baging, ngunit may ilang bahagi ng lupa "
                "na nagsisimula nang magkaroon ng maliliit na "
                "bitak. Napansin ito ni Chef Pablo habang "
                "sinusuri nila ang taniman."
            ),
        },
        {
            "id": "S5P2",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth3.jpg",
            "chars": {"chef": {"side": "right", "expression": "confused"}},
            "lines": [
                ("chef", "Lucas, bakit may mga bitak sa lupa sa ilalim ng ilang baging? Natutuyo ba ang taniman?"),
            ],
        },
        {
            "id": "S5P3",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth3.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Posibleng lumalaki na ang mga tuber sa ilalim at itinutulak nila ang lupa habang lumalaki."),
                ("lucas", "Pero hindi sapat ang mga bitak para masabing handa na silang anihin. Kailangan pa nating tingnan ang edad at kalagayan ng tanim."),
            ],
        },
        {
            "id": "S5P4",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth3.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Tama. Maaaring palatandaan ang pagbitak ng lupa na lumalaki na ang mga tuber, kaya magandang senyales iyon."),
                ("lola", "Pero huwag tayong basta maghukay sa bawat bitak. Maaari nating masugatan ang kamote. Maghintay pa tayo at magsuri nang maingat."),
            ],
        },
        {
            "id": "S5P5",
            "type": "scene",
            "bg": "background/baronsweetpotato.jpg",
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
            "id": "S5P6",
            "type": "dialogue",
            "bg": "background/baronsweetpotato.jpg",
            "dark": True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Kung may bitak na, hukayin na ninyo! Baka maunahan pa kayo ng panahon!"),
                ("baron", "O baka naman takot kayong makita na wala talagang laman ang lupa?"),
            ],
        },
        {
            "id": "S5P7",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth3.jpg",
            "chars": {"chef": {"side": "right", "expression": "angry"}},
            "lines": [
                ("chef", "Hindi mo kami mapapamadali, Baron. Hindi porke may nakikita tayong palatandaan ay dapat na agad tayong mag-ani."),
            ],
        },
        {
            "id": "S5P8",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth3.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Titingnan natin ang mga palatandaan, pero susundin pa rin natin ang tamang panahon ng pag-aani."),
                ("lucas", "Sa ngayon, maingat lang nating susuriin ang lupa at iiwasang masugatan ang mga tuber."),
            ],
        },
        {
            "id": "S5P9",
            "type": "choice",
            "bg": "background/sweetpotatogrowth3.jpg",
            "question": "Ano ang dapat gawin kapag may nakitang bitak sa lupa sa paligid ng kamote?",
            "retry_question": "Ang bitak ay maaaring palatandaan ng paglaki ng tuber, pero hindi ito nag-iisang batayan para mag-ani.",
            "choices": [
                {"img": "buttons/choice_dig_immediately.png", "label": "Hukayin agad ang lahat", "frame": True},
                {"img": "buttons/choice_check_soil.png", "label": "Suriin at maghintay sa tamang panahon", "frame": True},
            ],
            "correct": 1,
        },
        {
            "id": "S5P10_right",
            "type": "feedback",
            "if_correct": True,
            "bg": "background/scenebg_right.png",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Tama, apo. Ang mga bitak ay maaaring magpahiwatig na lumalaki ang mga tuber, pero kailangan pa ring isaalang-alang ang edad at kalagayan ng halaman."),
                ("lola", "Maingat na pagsusuri at tamang tiyempo ang makatutulong para hindi masayang ang ating ani."),
            ],
        },
        {
            "id": "S5P11_wrong",
            "type": "feedback",
            "if_correct": False,
            "retry_to_choice": True,
            "bg": "background/scenebg_wrong.png",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "Sandali. Kapag hinukay natin agad ang lahat, baka masugatan ang mga tuber o masyado pa silang maliit."),
                ("chef", "Mas mabuting suriin muna natin ang tanim at hintayin ang tamang panahon."),
            ],
        },
        {
            "id": "S5P12",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth3.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy"}},
            "lines": [
                ("chef", "Mas naiintindihan ko na ngayon. Hindi lang pala dahon ang dapat nating bantayan; kailangan ding alamin kung ano ang nangyayari sa ilalim ng lupa."),
            ],
        },

        # ── Scene 6: Waiting for maturity, day 110 ─────────────
        {
            "id": "day110_fade",
            "type": "transition",
        },
        {
            "id": "S6P1",
            "type": "narration_overlay",
            "day": 110,
            "bg": "background/sweetpotatogrowth4.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",
            "narration": (
                "Pagsapit ng ika-110 araw, patuloy na lumaki ang "
                "mga tuber. May ilang dahon nang naninilaw, ngunit "
                "hindi pa pare-pareho ang kalagayan ng bawat "
                "halaman. Nagpasya silang maghintay pa at "
                "maghanda para sa maingat na pag-aani."
            ),
        },
        {
            "id": "S6P2",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth4.jpg",
            "chars": {"chef": {"side": "right", "expression": "worried"}},
            "lines": [
                ("chef", "May mga dahon nang naninilaw. Ibig bang sabihin ay malapit na tayong mag-ani?"),
            ],
        },
        {
            "id": "S6P3",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth4.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Maaari itong maging isa sa mga palatandaan ng paghinog, pero tingnan din natin kung nasa angkop nang edad ang tanim at kung maayos ang kalagayan nito."),
                ("lola", "Huwag nating ipagkamali ang paninilaw dahil sa paghinog sa paninilaw na dulot ng sakit o kakulangan sa tubig."),
            ],
        },
        {
            "id": "S6P4",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth4.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Ilang araw na lang po at aabot na tayo sa ika-120 araw. Ihanda na natin ang mga kagamitan, pero mag-ingat tayo sa paghuhukay."),
                ("lucas", "Kapag nasugatan ang mga kamote, mas madali silang masira habang iniimbak."),
            ],
        },
        {
            "id": "S6P5",
            "type": "dialogue",
            "bg": "background/sweetpotatogrowth4.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy"}},
            "lines": [
                ("chef", "Sige. Gusto kong maihanda ang Kamote Cue para sa mga bata, pero mas gusto kong maayos ang ating aanihin kaysa magmadali."),
            ],
        },

        # ── Scene 7: Harvest, day 120 ──────────────────────────
        {
            "id": "day120_fade",
            "type": "transition",
        },
        {
            "id": "S7P1",
            "type": "narration_overlay",
            "day": 120,
            "bg": "background/sweetpotatoharvest.jpg",
            "dim_inactive": False,
            "overlay": "woodbg.png",
            "narration": (
                "Dumating ang ika-120 araw. Matapos ang ilang "
                "buwang pag-aalaga, handa na ang mga kamote "
                "para sa pag-aani. Sinuri muna nina Lucas, "
                "Chef Pablo, at Lola Maria ang mga baging at "
                "ang lupa bago nila simulan ang paghuhukay."
            ),
        },
        {
            "id": "S7P2",
            "type": "dialogue",
            "bg": "background/sweetpotatoharvest.jpg",
            "chars": {"lola": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("lola", "Ito na ang hinihintay natin. Nasa tamang panahon na ang ating tanim. Hukayin natin nang maingat upang hindi magasgas o maputol ang mga kamote."),
            ],
        },
        {
            "id": "S7P3",
            "type": "dialogue",
            "bg": "background/sweetpotatoharvest.jpg",
            "chars": {"lucas": {"side": "right", "expression": "talking"}},
            "lines": [
                ("lucas", "Luwagan muna natin ang lupa sa gilid ng tanim. Huwag itusok ang kagamitan malapit sa mga tuber para hindi natin sila masugatan."),
                ("lucas", "Dahan-dahan nating iaangat ang lupa at kukunin ang mga kamote kapag nakalantad na."),
            ],
        },
        {
            "id": "S7P4",
            "type": "action_challenge",
            "bg": "background/sweetpotatoharvest.jpg",
            "overlay": "sweetpotatoharvestcard.png",
            "dim_inactive": False,
        },
        {
            "id": "S7P5",
            "type": "dialogue",
            "bg": "background/sweetpotatoharvest.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy"}},
            "lines": [
                ("chef", "Ang dami natin! At ang gaganda pa ng mga kamote. Sulit ang ilang buwang paghihintay at pag-aalaga."),
                ("chef", "Ngayon, maaari ko nang subukang gawin ang pagkaing hindi mawala sa isip ko."),
            ],
        },
        {
            "id": "S7P6",
            "type": "dialogue",
            "bg": "background/sweetpotatoharvest.jpg",
            "chars": {"lola": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("lola", "Kamote Cue ang ihahanda mo, hindi ba? Naalala ko kung paano ka magtusok ng mga piraso sa kawayan at magbalot ng mainit-init na kamote sa asukal."),
                ("lola", "May mga batang pumipila noon sa labas ng kusina para makatikim."),
            ],
        },
        {
            "id": "S7P7",
            "type": "dialogue",
            "bg": "background/sweetpotatoharvest.jpg",
            "chars": {"chef": {"side": "right", "expression": "confused"}},
            "lines": [
                ("chef", "Kawayan... asukal... mainit na kawali..."),
                ("chef", "Parang naririnig ko na naman ang tawanan ng mga bata. Pero may kulang pa rin sa alaala ko."),
            ],
        },

        # ── Scene 8: Preparing the Kamote Cue ──────────────────
        {
            "id": "day120_kitchen_fade",
            "type": "transition",
        },
        {
            "id": "S8P1",
            "type": "scene",
            "bg": "background/kitchenbg.jpg",
        },
        {
            "id": "S8P2",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "happy", "flip": True}},
            "lines": [
                ("lucas", "Chef, handa na ang mga kamote. Ano po ang una nating gagawin?"),
            ],
        },
        {
            "id": "S8P3",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "talking"}},
            "lines": [
                ("chef", "Huhugasan muna natin ang mga kamote at aalisin ang anumang dumi. Pagkatapos, babalatan at puputulin natin ang mga ito sa magkakaparehong laki para pantay ang pagkakaluto."),
                ("chef", "Ihahanda rin natin ang asukal at ang kawali. Mag-ingat tayo dahil mainit ang mantika at tunaw na asukal."),
            ],
        },
        {
            "id": "S8P4",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Dahan-dahan lang, Pablo. Huwag mong hahayaang mapalapit ang mga bata sa mainit na kawali."),
                ("lola", "Mas masaya ang pista kapag ligtas ang lahat."),
            ],
        },
        {
            "id": "S8P5",
            "type": "action_challenge",
            "bg": "background/kitchenbg.jpg",
            "overlay": "kamotecuecookingcard.png",
            "dim_inactive": False,
        },
        {
            "id": "S8P6",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy"}},
            "lines": [
                ("chef", "Ayan na... Kamote Cue! Ang kulay ng asukal, ang amoy ng bagong lutong kamote..."),
                ("chef", "Sandali. Naalala ko na kung bakit espesyal sa akin ang pagkaing ito."),
            ],
        },
        {
            "id": "S8P7",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "surprised"}},
            "lines": [
                ("chef", "Tuwing pista, may mga batang walang pambili ng meryenda. Kaya naghahanda ako ng dagdag na Kamote Cue para may maiuwi sila."),
                ("chef", "Sabi ko noon, walang batang dapat umuwi nang gutom mula sa pista."),
            ],
        },
        {
            "id": "S8P8",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("lola", "Iyan ang naaalala ko, Pablo. Hindi lang masarap ang mga inihahanda mo. Lagi mo ring iniisip kung paano makikibahagi ang lahat."),
                ("lola", "Iyon ang dahilan kung bakit gustong-gusto ka ng mga tao sa baryo."),
            ],
        },
        {
            "id": "S8P9",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy"}},
            "lines": [
                ("chef", "Naalala ko na! Ang Kamote Cue ay hindi lang basta pagkaing inihahanda ko tuwing pista. Paalala ito na dapat may maibahagi tayo sa iba."),
                ("chef", "Salamat, Lucas. Salamat, Lola. Unti-unti nang bumabalik ang mga alaala ko."),
            ],
        },

        # ── Scene 9: The Baron appears ─────────────────────────
        {
            "id": "S9P1",
            "type": "scene",
            "bg": "background/baronkitchen.jpg",
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
            "id": "S9P2",
            "type": "dialogue",
            "bg": "background/baronkitchen.jpg",
            "dark": True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Muli na naman kayong nagdiriwang! Bakit ba hindi kayo mapagod sa pagtutulungan?"),
                ("baron", "Akala ninyo ba isang pagkaing matamis ang makapagpapabago sa lahat?"),
            ],
        },
        {
            "id": "S9P3",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "determined"}},
            "lines": [
                ("chef", "Hindi lang pagkain ang ipinaglalaban namin, Baron. Ang bawat ani ay bunga ng pagtutulungan at pag-aalaga ng buong baryo."),
                ("chef", "At kapag may sapat kami, gusto naming ibahagi iyon sa iba."),
            ],
        },
        {
            "id": "S9P4",
            "type": "dialogue",
            "bg": "background/baronkitchen.jpg",
            "dark": True,
            "chars": {"baron": {"side": "right", "expression": "defeated"}},
            "lines": [
                ("baron", "Madali para sa inyong sabihin iyan. Hindi ninyo alam ang pakiramdam na laging naiiwan habang sama-sama kayong nagdiriwang."),
            ],
        },
        {
            "id": "S9P5",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Baron, hindi tama ang ginawa mong pagsira sa mga alaala ng mga tao. Pero kung gusto mong mapabilang, puwede mo kaming kausapin sa halip na saktan ang baryo."),
            ],
        },
        {
            "id": "S9P6",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Hindi pa man natin kayang ayusin ang lahat ngayon, may puwang pa rin sa hapag para sa taong handang magbago."),
                ("lola", "Hindi kailangang sirain ang kasiyahan ng iba para lang mapansin ka."),
            ],
        },
        {
            "id": "S9P7",
            "type": "dialogue",
            "bg": "background/baronkitchen.jpg",
            "dark": True,
            "chars": {"baron": {"side": "right", "expression": "confused"}},
            "lines": [
                ("baron", "Pagkatapos ng lahat ng ginawa ko, bibigyan ninyo pa rin ako ng pagkakataong makisalo?"),
            ],
        },
        {
            "id": "S9P8",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"chef": {"side": "right", "expression": "happy"}},
            "lines": [
                ("chef", "Hindi namin sinasabing walang nangyari. Pero kung talagang gusto mong magbago, maaari kang magsimula sa paghingi ng tawad at pagtulong sa baryo."),
                ("chef", "May Kamote Cue pa rito. Maaari kang makisalo kapag handa ka nang makibahagi nang maayos."),
            ],
        },
        {
            "id": "S9P9",
            "type": "dialogue",
            "bg": "background/baronkitchen.jpg",
            "chars": {"baron": {"side": "right", "expression": "defeated"}},
            "lines": [
                ("baron", "Hindi ko alam kung paano magsisimula... pero pagod na rin akong mag-isa."),
                ("baron", "Patawad sa mga pananim at alaalang sinira ko. Susubukan kong itama ang mga nagawa ko."),
            ],
        },
        {
            "id": "S9P10",
            "type": "dialogue",
            "bg": "background/kitchenbg.jpg",
            "chars": {"lola": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("lola", "Kung ganoon, magsimula tayo sa simpleng bagay. Tulungan mo kaming ihanda ang mga pagkain para sa pista."),
                ("lola", "Mas magiging masaya ang pagdiriwang kung lahat ay may pagkakataong makibahagi."),
            ],
        },
        {
            "id": "end_fade",
            "type": "transition",
        },
    ],
}
