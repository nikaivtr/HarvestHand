# ============================================================
#  CHAPTER 10 — CASSAVA (Kamoteng Kahoy) — THE FINAL STAND
#  Expert | 15 story panels | Total growing days: 201
#  Characters: Lucas, Lola Maria, Blight Baron (revealed lonely),
#              Kapitan Ernesto, Chef Agapita
#  MECHANIC: timer=True on all challenge slides (30-sec future impl)
#  PLOT CLIMAX: All 10 memories return. Baron is revealed as lonely.
#               Lola Maria invites Baron to the Fiesta.
#               Baron gifts a basket of fresh soil. Pista is restored.
# ============================================================

CHAPTER = {
    "id":         "ch10",
    "crop":       "Cassava",
    "level":      "advanced",
    "memory":     "Kamoteng Kahoy Memory",
    "total_days": 201,
 
    "slides": [
 
        # ── Title card ─────────────────────────────────────────
        {
            "id":   "title",
            "type": "title",
            "bg":   "background/scenebg_default.png",
            "logo": "chapter10.png",
        },
 
        # ── Scene 1 — The Final Stand: Baron's last gamble ─────
        {
            "id":    "S1P1",
            "type":  "dialogue",
            "bg":    "background/cassava_baron_final.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "nervous"}},
            "lines": [
                ("baron", "..."),
                ("baron", "Isang alaala na lang... ang huli."),
                ("baron", "Kapag bumalik iyon, tapos na ang lahat. Hindi ko hahayaang mangyari iyon!"),
            ],
        },
        {
            "id":    "S1P2",
            "type":  "dialogue",
            "bg":    "background/cassava_baron_final.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Gagamitin ko ang lahat ng kaya ko! Ang tagtuyot, ang lason, ang mga peste, at ang sumpa ng oras!"),
                ("baron", "Ito na ang huli kong laban! Tatlumpung segundo sa bawat kilos ninyo, at hindi ninyo ito matatapos!"),
            ],
        },
        {
            "id": "S1P3",
            "type": "scene",
            "bg": "background/cassava_baron_final.png",
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
            "chars": {"lucas": {"side": "right", "expression": "afraid", "flip": False}},
            "lines": [
                ("lucas", "Lola, ito na po yata ang pinakamalakas niyang pananakot."),
            ],
        },
        {
            "id":    "S1P5",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "sad", "flip": False}},
            "lines": [
                ("lola", "Kamoteng kahoy ang huli nating pananim, apo."),
                ("lola", "Pakiramdam ko, may nakatago pang alaala sa likod nito na higit na mahalaga kaysa sa lahat ng nauna. Ngunit hindi ko pa maalala kung ano iyon."),
            ],
        },
        {
            "id":    "S1P6",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lucas": {"side": "right", "expression": "determined", "flip": False}},
            "lines": [
                ("lucas", "Kaya po natin ito, Lola. Isa po ang kamoteng kahoy sa pinakamatibay na pananim, at marami na po tayong natutunan."),
            ],
        },
        {
            "id":    "S1P7",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Lucas! Lola Maria! Narinig namin ang pagsabog, kaya nandito kami ni Chef Agapita para tumulong."),
                ("kapitan", "Ikaw ang nagbalik ng aking layunin, hijo. Panahon na para suklian ko iyon."),
            ],
        },
        {
            "id":    "S1P8",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"chef": {"side": "right", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "At ako naman ang magtuturo kung paano ligtas na lutuin ang ani. Sama-sama tayo hanggang dulo!"),
            ],
        },
        {
            "id":    "S1P9",
            "type":  "dialogue",
            "bg":    "background/scenebg_default.png",
            "chars": {"lola": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lola", "Napakaganda ng mga pagkakaibigang naitanim mo, apo. Sige, simulan na natin."),
            ],
        },
        {
            "id":    "S1P10",
            "type":  "dialogue",
            "bg":    "background/cassava_raisedbeds.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Hindi buto ang itinatanim sa kamoteng kahoy, kundi mga pinutol na tangkay, o cuttings."),
                ("lola", "Pipili tayo ng malusog at hinog na tangkay, at puputulin natin ito nang halos dalawampu hanggang tatlumpung sentimetro, na may lima hanggang pitong buko, o nodes."),
            ],
        },
        {
            "id":    "S1P11",
            "type":  "dialogue",
            "bg":    "background/cassava_raisedbeds.png",
            "chars": {"lucas": {"side": "right", "expression": "talking", "flip": False}},
            "lines": [
                ("lucas", "Ano po ang uunahin natin, Lola?"),
            ],
        },
        {
            "id":    "S1P12",
            "type":  "dialogue",
            "bg":    "background/cassava_raisedbeds.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ang lupa, apo. Ayaw ng kamoteng kahoy ng ugat na laging basa."),
                ("lola", "Gagawa tayo ng mataas na tambak, o raised bed, para umagos ang sobrang tubig."),
            ],
        },
        {
            "id":    "S1P13",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Tatlumpung segundo, bata! Magsimula ka na!"),
            ],
        },
        {
            "id":    "S1P14",
            "type":  "dialogue",
            "bg":    "background/cassava_raisedbeds.png",
            "chars": {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "lines": [
                ("lucas", "Hindi mo na ako matitinag, Baron. Handa na po ako!"),
            ],
        },
 
        # ── Raised beds — choice (TIMER) ───────────────────────
        {
            "id":            "S1P15",
            "type":          "choice",
            "bg":            "background/cassava_raisedbeds.png",
            "timer":         True,
            "question":       "Bilis! Alin ang tamang kagamitan para gumawa ng mataas na tambak para sa kamoteng kahoy?",
            "retry_question": "Mabilis! Aling kagamitan ang may lakas na mag-angat ng maraming lupa?",
            "choices": [
                {"img": "buttons/choice_hoe.png",    "label": "", "frame": False},
                {"img": "buttons/choice_trowel.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S1P15_right_1",
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
                ("lucas", "Tama at mabilis! Ang asarol ang pang-angat ng lupa para sa tambak na hindi mababaha."),
            ],
        },
        {
            "id":          "S1P15_right_2",
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
                ("lola", "Magaling, apo! Sa mataas na tambak, hindi mananatili ang tubig sa mga ugat ng kamoteng kahoy."),
            ],
        },
        {
            "id":              "S1P15_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "left",
                    "expression": "wrong",
                    "flip": True,
                }
            },
            "lines": [
                ("lucas", "Naku po! Masyadong maliit ang dulo para mag-angat ng ganito karaming lupa. Humanap tayo ng mas malakas na kagamitan!"),
            ],
        },
        {
            "id":              "S1P15_wrong_2",
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
        {
            "id":    "S1P16",
            "type":  "dialogue",
            "bg":    "background/cassava_raisedbeds.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ngayon, itatanim natin ang mga cuttings. Mahalaga ang posisyon ng bawat tangkay, apo."),
            ],
        },
 
        # ── Planting cuttings — choice (TIMER) ─────────────────
        {
            "id":            "S1P17",
            "type":          "choice",
            "bg":            "background/cassava_raisedbeds.png",
            "timer":         True,
            "question":       "Bilis! Alin ang tamang posisyon ng tangkay ng kamoteng kahoy kapag itinatanim?",
            "retry_question": "Mabilis! Aling dulo ng tangkay ang may mga usbong na tutubo paitaas?",
            "choices": [
                {"img": "buttons/choice_buds_up.png",   "label": "", "frame": False},
                {"img": "buttons/choice_buds_down.png", "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S1P17_right_1",
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
                ("lucas", "Tama at mabilis! Nakaharap sa itaas ang mga usbong, para tumubo paitaas ang mga bagong sanga."),
            ],
        },
        {
            "id":          "S1P17_right_2",
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
                ("lola", "Magaling, apo! Ibabaon natin ang halos kalahati ng tangkay para magkaroon ng matibay na ugat."),
            ],
        },
        {
            "id":              "S1P17_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "left",
                    "expression": "wrong",
                    "flip": True,
                }
            },
            "lines": [
                ("lucas", "Naku po! Kapag nakabaligtad ang tangkay, mahihirapan itong tumubo."),
            ],
        },
        {
            "id":              "S1P17_wrong_2",
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
                ("baron", "HA! Itanim ninyo nang pabaligtad! Mas matagal tumubo, mas masaya!"),
            ],
        },
 
        # ── Day 1 — Light watering ─────────────────────────────
        {
            "id":   "day1_fade",
            "type": "transition",
        },
        {
            "id": "S2P1",
            "type": "narration_overlay",
            "day": 1,
            "bg": "background/cassava_raisedbeds.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Unang araw ng huling taniman. "
                "Magkakasamang itinanim nina Lucas, Lola Maria, Kapitan Ernesto at Chef Agapita "
                "ang mga tangkay ng kamoteng kahoy sa mataas na tambak."
            ),
        },
        {
            "id":    "S2P2",
            "type":  "dialogue",
            "day":   1,
            "bg":    "background/cassava_raisedbeds.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Bahagya lamang ang tubig na ibibigay natin, apo. Madaling mabulok ang tangkay at ugat ng kamoteng kahoy kapag masyadong basa."),
            ],
        },
        {
            "id":       "S2P3",
            "type":     "action_challenge",
            "day":      1,
            "bg":       "background/cassava_raisedbeds.png",
            "chars":    {"lucas": {"side": "right", "expression": "waters", "flip": False}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-01 Water Card",
            "overlay": "WaterCard.png",
            "dialogue": "Lucas: Bahagya lang po ang ibibigay nating tubig, Lola, sapat para umayos ang lupa. I-scan natin ang Water Card, pero banayad!",
            "question": "Scan the Water Card to lightly water the cassava cuttings — just enough to settle the soil, not flood it.",
        },
 
        # ── Day 30 — Drought defense ───────────────────────────
        {
            "id":   "day30_fade",
            "type": "transition",
        },
        {
            "id":    "S3P1",
            "type":  "dialogue",
            "day":   30,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Tagtuyot! Tutuyuin ko ang lupa ninyo! Tingnan natin kung kaya ng inyong kamoteng kahoy!"),
            ],
        },
        {
            "id":    "S3P2",
            "type":  "dialogue",
            "bg":    "background/cassava_drought.png",
            "chars": {"lucas": {"side": "right", "expression": "concerned", "flip": False}},
            "lines": [
                ("lucas", "Lola, bitak-bitak na po ang lupa at lumalaylay ang ilang dahon. Ano po ang dapat nating gawin?"),
            ],
        },
        {
            "id":    "S3P3",
            "type":  "dialogue",
            "bg":    "background/cassava_drought.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Huwag kang mag-alala, apo. Matibay ang kamoteng kahoy at kayang magtiis ng tuyong panahon."),
                ("lola", "Ang kailangan lamang natin ay tulungan itong panatilihin ang kaunting halumigmig sa lupa."),
            ],
        },
 
        # ── Drought — choice (TIMER) ───────────────────────────
        {
            "id":            "S3P4",
            "type":          "choice",
            "day":           30,
            "bg":            "background/cassava_drought.png",
            "timer":         True,
            "question":       "Tuyo ang lupa dahil sa tagtuyot ni Baron. Ano ang dapat gawin para tulungan ang mga kamoteng kahoy?",
            "retry_question": "Mabilis! Isipin kung ano ang nangyayari sa ugat ng kamoteng kahoy kapag labis ang tubig.",
            "choices": [
                {"img": "buttons/choice_mulch_straw.png", "label": "", "frame": False},
                {"img": "buttons/choice_flood_field.png", "label": "", "frame": False},
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
                ("lucas", "Tama at mabilis! Tatakpan natin ng dayami ang lupa para manatili ang kaunting halumigmig, at hindi na natin kailangang bahain ang mga ugat."),
            ],
        },
        {
            "id":          "S3P4_right_2",
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
                ("lola", "Magaling, apo! Mas kaya ng kamoteng kahoy ang tagtuyot kaysa sa labis na tubig na nagpapabulok sa ugat."),
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
                    "side": "left",
                    "expression": "wrong",
                    "flip": True,
                }
            },
            "lines": [
                ("lucas", "Naku po! Mabubulok ang mga ugat ng kamoteng kahoy kapag binaha ang taniman."),
            ],
        },
        {
            "id":              "S3P4_wrong_2",
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
                ("baron", "HAHAHA! Bahain ninyo ang taniman! Mabubulok ang lahat!"),
            ],
        },
 
        # ── Day 45 — Reject the toxic dump ─────────────────────
        {
            "id":   "day45_fade",
            "type": "transition",
        },
        {
            "id":    "S4P1",
            "type":  "dialogue",
            "day":   45,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "smile"}},
            "lines": [
                ("baron", "Heto ang regalo ko! Mga lumang lalagyan ng kemikal!"),
                ("baron", "Ibaon ninyo ang laman nito sa lupa, at lalaki raw agad ang inyong kamoteng kahoy!"),
            ],
        },
        {
            "id":    "S4P2",
            "type":  "dialogue",
            "bg":    "background/cassava_toxic.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Huwag! Ang mga mapanganib na kemikal sa lupa ay mapupunta sa tubig, sa pananim, at sa mga taong kakain nito."),
                ("kapitan", "Hindi ito paraan ng pagpapalaki ng pananim. Panganib ito sa buong baryo!"),
            ],
        },
 
        # ── Toxic waste — choice (TIMER) ───────────────────────
        {
            "id":            "S4P3",
            "type":          "choice",
            "day":           45,
            "bg":            "background/cassava_toxic.png",
            "timer":         True,
            "question":       "Inalok ni Baron ang mga lumang lalagyan ng kemikal. Ano ang dapat gawin sa mga ito?",
            "retry_question": "Mabilis! Isipin kung saan mapupunta ang kemikal kapag inilibing ito sa lupa ng taniman.",
            "choices": [
                {"img": "buttons/choice_return_waste.png", "label": "", "frame": False},
                {"img": "buttons/choice_bury_waste.png",   "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S4P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Tama! Ang mga mapanganib na basura ay dapat dalhin sa tamang tanggapan para sa ligtas na pagtatapon, at hindi sa lupa ng ating pagkain."),
            ],
        },
        {
            "id":          "S4P3_right_2",
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
                ("lucas", "Magaling po, Kapitan! Mas mabuting protektahan ang lupa kaysa magmadali sa paglaki ng pananim."),
            ],
        },
        {
            "id":              "S4P3_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "left",
                    "expression": "wrong",
                    "flip": True,
                }
            },
            "lines": [
                ("lucas", "Naku po! Kapag inilibing ang kemikal sa lupa, mapupunta ito sa ugat ng kamoteng kahoy at sa lahat ng kakain nito."),
            ],
        },
        {
            "id":              "S4P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"kapitan_wrong": "right"},
            "lines": [
                ("kapitan_wrong", "Huwag! Mapanganib iyan sa buong baryo, hindi lang sa taniman!"),
            ],
        },
 
        # ── Day 60 — Fertilizer ────────────────────────────────
        {
            "id":   "day60_fade",
            "type": "transition",
        },
        {
            "id":    "S5P1",
            "type":  "dialogue",
            "day":   60,
            "bg":    "background/cassava_growing.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Oras na para pakainin ang lupa, apo. Kailangan ng kamoteng kahoy ng sapat na sustansya para lumaki nang malusog ang mga ugat."),
                ("lola", "Compost at abo ng kahoy ang magandang pagkain para dito."),
            ],
        },
        {
            "id":       "S5P2",
            "type":     "action_challenge",
            "day":      60,
            "bg":       "background/cassava_growing.png",
            "chars":    {"lucas": {"side": "right", "expression": "determined", "flip": False}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-02A Organic Fertilizer Card",
            "overlay": "organicfertilizercard.png",
            "dialogue": "Lucas: I-scan natin ang Fertilizer Card, Lola, para piliin ang organikong pataba na ligtas para sa lupa ng kamoteng kahoy. Bilis!",
            "question": "Scan the Fertilizer Card to choose the organic fertilizer for healthy cassava soil.",
        },
 
        # ── Day 90 — Weeding ───────────────────────────────────
        {
            "id":   "day90_fade",
            "type": "transition",
        },
        {
            "id":    "S6P1",
            "type":  "dialogue",
            "day":   90,
            "bg":    "background/cassava_growing.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Lucas, tumataas na ang mga damo sa pagitan ng mga hilera. Aagawan nila ng sustansya ang kamoteng kahoy."),
                ("kapitan", "Bunutin natin ang mga ito nang hindi nasasaktan ang mga ugat sa ilalim ng lupa."),
            ],
        },
        {
            "id":       "S6P2",
            "type":     "action_challenge",
            "day":      90,
            "bg":       "background/cassava_growing.png",
            "chars":    {"lucas": {"side": "left", "expression": "determined", "flip": True}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-03 Weed Removal Card",
            "overlay": "weedremovalcard.png",
            "dialogue": "Lucas: I-scan natin ang Weed Removal Card, Kapitan, para maalis ang mga damo nang hindi nasisira ang mga ugat ng kamoteng kahoy. Bilis!",
            "question": "Scan the Weed Removal Card to learn careful weeding that protects the cassava roots underground.",
        },
 
        # ── Day 120 — Falling leaves ───────────────────────────
        {
            "id":   "day120_fade",
            "type": "transition",
        },
        {
            "id":    "S7P1",
            "type":  "dialogue",
            "day":   120,
            "bg":    "background/cassava_mature.png",
            "chars": {"lucas": {"side": "right", "expression": "concerned", "flip": False}},
            "lines": [
                ("lucas", "Lola, naglalagasan po ang mga ibabang dahon ng kamoteng kahoy. May sakit po ba ang mga ito?"),
            ],
        },
        {
            "id":    "S7P2",
            "type":  "dialogue",
            "bg":    "background/cassava_mature.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Huwag kang mag-alala, apo. Natural na naglalagas ang mga lumang dahon sa ibaba habang tumatangkad ang halaman."),
                ("lola", "Hangga't berde at malusog ang mga bagong dahon sa itaas, walang dapat ikabahala."),
            ],
        },
        {
            "id":    "S7P3",
            "type":  "dialogue",
            "bg":    "background/cassava_mature.png",
            "chars": {"lucas": {"side": "right", "expression": "thumbs", "flip": False}},
            "lines": [
                ("lucas", "Salamat po, Lola. Mabuti na lang at hindi ako nagmadaling mag-spray ng kung anu-ano."),
            ],
        },
 
        # ── Day 140 — Spider mites ─────────────────────────────
        {
            "id":   "day140_fade",
            "type": "transition",
        },
        {
            "id":    "S8P1",
            "type":  "dialogue",
            "day":   140,
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "laugh"}},
            "lines": [
                ("baron", "Spider mites! Susuhop ng katas ang aking mga munting gagamba sa bawat dahon ng inyong kamoteng kahoy!"),
                ("baron", "Tingnan natin kung kaya ninyo ito! HAHAHAHA!"),
            ],
        },
        {
            "id":    "S8P2",
            "type":  "dialogue",
            "bg":    "background/cassava_mites.png",
            "chars": {"lucas": {"side": "right", "expression": "concerned", "flip": False}},
            "lines": [
                ("lucas", "Lola, may maliliit na batik na dilaw at pinong sapot sa ilalim ng mga dahon!"),
            ],
        },
        {
            "id":    "S8P3",
            "type":  "dialogue",
            "bg":    "background/cassava_mites.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Spider mites nga iyan, apo. Mahilig sila sa tuyo at mainit na panahon."),
                ("lola", "Kailangan nating gumamit ng natural na pestisidyo, para hindi masaktan ang mga kapaki-pakinabang na insekto."),
            ],
        },
        {
            "id":       "S8P4",
            "type":     "action_challenge",
            "day":      140,
            "bg":       "background/cassava_mites.png",
            "chars":    {"lucas": {"side": "right", "expression": "determined", "flip": False}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-04A Natural Pesticide Card",
            "overlay": "naturalpesticidecard.png",
            "dialogue": "Lucas: I-scan natin ang Pesticide Card, Lola, para piliin ang natural na pestisidyo laban sa spider mites. Bilis!",
            "question": "Scan the Pesticide Card to choose the natural pesticide against spider mites.",
        },
 
        # ── Day 170 — Root-bulking sign ────────────────────────
        {
            "id":   "day170_fade",
            "type": "transition",
        },
        {
            "id":    "S9P1",
            "type":  "dialogue",
            "day":   170,
            "bg":    "background/cassava_mature.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Tingnan mo ang lupa sa paligid ng bawat puno, apo. May mga bitak at bahagyang pag-umbok."),
            ],
        },
        {
            "id":            "S9P2",
            "type":          "choice",
            "day":           170,
            "bg":            "background/cassava_mature.png",
            "timer":         True,
            "question":       "Bilis! Ano ang kadalasang ibig sabihin ng mga bitak at pag-umbok ng lupa sa paligid ng puno ng kamoteng kahoy?",
            "retry_question": "Mabilis! Isipin kung ano ang lumalaki sa ilalim ng lupa.",
            "choices": [
                {"img": "buttons/choice_tuber_growing.png", "label": "", "frame": False},
                {"img": "buttons/choice_need_water.png",    "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S9P2_right_1",
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
                ("lucas", "Tama at mabilis! Tinutulak ng lumalaking mga ugat ang lupa, kaya nagbibitak at umuumbok ito."),
            ],
        },
        {
            "id":          "S9P2_right_2",
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
                ("lola", "Magaling, apo! Magandang palatandaan iyan na malapit na tayong umani."),
            ],
        },
        {
            "id":              "S9P2_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "left",
                    "expression": "wrong",
                    "flip": True,
                }
            },
            "lines": [
                ("lucas", "Naku po! Hindi lang kakulangan sa tubig ang ibig sabihin niyan. Lumalaki na ang mga ugat sa ilalim."),
            ],
        },
        {
            "id":              "S9P2_wrong_2",
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
                ("baron", "HAHAHA! Diligan ninyo ang lahat! Mas mabulok, mas masaya!"),
            ],
        },
 
        # ── Day 195 — Harvest ──────────────────────────────────
        {
            "id":   "day195_fade",
            "type": "transition",
        },
        {
            "id":    "S10P1",
            "type":  "dialogue",
            "day":   195,
            "bg":    "background/cassava_mature.png",
            "chars": {"lola": {"side": "left", "expression": "celebrates", "flip": False}},
            "lines": [
                ("lola", "Malaki na ang mga bitak at halos wala nang dahon sa ibaba, apo."),
                ("lola", "Oras na para anihin ang pinakamatibay nating pananim!"),
            ],
        },
        {
            "id":    "S10P2",
            "type":  "dialogue",
            "bg":    "background/cassava_mature.png",
            "chars": {"lucas": {"side": "right", "expression": "determined", "flip": False}},
            "lines": [
                ("lucas", "Kailangan ko pong tiyakin kung alin ang handa na, Lola. Hindi po ako magmamadali."),
            ],
        },
 
        # ── Harvest — choice (TIMER) ───────────────────────────
        {
            "id":            "S10P3",
            "type":          "choice",
            "day":           195,
            "bg":            "background/cassava_mature.png",
            "timer":         True,
            "question":       "Bilis! Alin ang halamang kamoteng kahoy na handa nang anihin?",
            "retry_question": "Mabilis! Ang handa nang anihin ay may bitak na lupa at kaunti na lang ang dahon sa ibaba.",
            "choices": [
                {"img": "buttons/choice_cassava_ready.png", "label": "", "frame": False},
                {"img": "buttons/choice_cassava_young.png", "label": "", "frame": False},
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
                "lucas": {
                    "side": "left",
                    "expression": "thumbs",
                    "flip": True,
                }
            },
            "lines": [
                ("lucas", "Tama at mabilis! Bitak ang lupa at kaunti na lang ang dahon sa ibaba, kaya handa na ang mga ugat."),
            ],
        },
        {
            "id":          "S10P3_right_2",
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
                ("lola", "Magaling, apo! Ang pasensya mo ang nagbigay sa atin ng pinakamalalaking ugat."),
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
                    "side": "left",
                    "expression": "wrong",
                    "flip": True,
                }
            },
            "lines": [
                ("lucas", "Naku po! Bata pa ang halamang iyan at maliit pa ang mga ugat nito."),
            ],
        },
        {
            "id":              "S10P3_wrong_2",
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
                ("baron", "HAHAHA! Hukayin ninyo na iyan kahit bata pa! Mas maliit ang aanihin ninyo!"),
            ],
        },
        {
            "id":       "S10P4",
            "type":     "action_challenge",
            "day":      195,
            "bg":       "background/cassava_harvest.png",
            "chars":    {"lucas": {"side": "right", "expression": "determined", "flip": False}},
            "active":   "lucas",
            "timer":    True,
            "card":     "AC-05 Harvest Card",
            "overlay": "harvestcardscan.png",
            "dialogue": "Lucas: Napili na po natin ang tamang halaman, Lola! I-scan natin ang Harvest Card para makumpirma ang pag-aani. Bilis!",
            "question": "Scan the Harvest Card to confirm the cassava roots — firm, pale, and fully grown — are ready for the final harvest.",
        },
        {
            "id":    "S10P5",
            "type":  "dialogue",
            "bg":    "background/cassava_harvest.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Paluwagin muna natin ang lupa sa paligid gamit ang asarol, tapos hugutin natin ang halaman sa tangkay."),
                ("lola", "Iwan natin ang mga tatlumpung sentimetro ng tangkay para may mahawakan tayo, at mag-ingat na huwag mabali ang mga ugat."),
            ],
        },
        {
            "id":    "S10P6",
            "type":  "dialogue",
            "bg":    "background/cassava_kitchen.png",
            "chars": {"chef": {"side": "right", "expression": "worried", "flip": False}},
            "lines": [
                ("chef", "Dapat nating iproseso o lutuin ang mga ito sa loob ng isa hanggang dalawang araw."),
                ("chef", "Mabilis magbago at masira ang kamoteng kahoy pagkatapos anihin."),
            ],
        },
 
        # ── Raw cassava is toxic ───────────────────────────────
        {
            "id":    "S11P1",
            "type":  "dialogue",
            "bg":    "background/scenebg_baron.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "angry"}},
            "lines": [
                ("baron", "Hindi na kailangang magluto! Kainin ninyo na agad ang kamoteng kahoy nang hilaw!"),
            ],
        },
        {
            "id":    "S11P2",
            "type":  "dialogue",
            "bg":    "background/cassava_kitchen.png",
            "chars": {"chef": {"side": "left", "expression": "angry", "flip": False}},
            "lines": [
                ("chef", "Huwag kayong maniniwala sa kaniya! May natural na sangkap na may cyanide ang kamoteng kahoy."),
                ("chef", "Mapanganib ito kapag hindi inihanda nang tama."),
            ],
        },
        {
            "id":            "S11P3",
            "type":          "choice",
            "bg":            "background/cassava_kitchen.png",
            "timer":         True,
            "question":       "Bilis! Ano ang tamang paghahanda sa bagong aning kamoteng kahoy bago ito kainin?",
            "retry_question": "Mabilis! Isipin kung ano ang nagtatanggal ng lason sa kamoteng kahoy.",
            "choices": [
                {"img": "buttons/choice_cook_cassava.png", "label": "", "frame": False},
                {"img": "buttons/choice_eat_raw.png",      "label": "", "frame": False},
            ],
            "correct": 0,
        },
        {
            "id":          "S11P3_right_1",
            "type":        "feedback",
            "if_correct":  True,
            "random_pick": True,
            "bg":          "background/scenebg_right.png",
            "chars":       {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Tama at mabilis! Binabalatan, hinuhugasan, at niluluto nang mabuti ang kamoteng kahoy, at doon nawawala ang mapanganib na sangkap nito."),
            ],
        },
        {
            "id":          "S11P3_right_2",
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
                ("lucas", "Magaling po, Chef! Hindi rin ligtas ibigay sa mga hayop ang hilaw na kamoteng kahoy, kaya lutuin din natin ito para sa kanila."),
            ],
        },
        {
            "id":              "S11P3_wrong_1",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {
                "lucas": {
                    "side": "left",
                    "expression": "wrong",
                    "flip": True,
                }
            },
            "lines": [
                ("lucas", "Naku po! Ang hilaw na kamoteng kahoy ay maaaring makalason kapag kinain."),
            ],
        },
        {
            "id":              "S11P3_wrong_2",
            "type":            "feedback",
            "if_correct":      False,
            "random_pick":     True,
            "retry_to_choice": True,
            "bg":              "background/scenebg_wrong.png",
            "chars":           {"chef_wrong": "right"},
            "lines": [
                ("chef_wrong", "Mag-ingat! Huwag kainin ang hilaw na kamoteng kahoy. Lutuin muna nang mabuti!"),
            ],
        },
 
        # ── Day 196 — The empty chair ──────────────────────────
        {
            "id":   "day196_fade",
            "type": "transition",
        },
        {
            "id":    "S11P4",
            "type":  "dialogue",
            "day":   196,
            "bg":    "background/cassava_kitchen.png",
            "chars": {"chef": {"side": "right", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "Heto na ang pinakuluan at pinritong kamoteng kahoy. Tikman ninyo, Lola Maria."),
            ],
        },
        {
            "id":    "S11P5",
            "type":  "dialogue",
            "bg":    "background/cassava_emptychair.png",
            "chars": {"lola": {"side": "left", "expression": "shocked", "flip": False}},
            "lines": [
                ("lola", "Ang tamis at ang lambot... Teka."),
                ("lola", "May bakanteng upuan sa mesa. Isang upuan na lagi naming iniiwang nakalaan, ngunit hindi ko maalala kung para kanino."),
            ],
        },
        {
            "id":    "S11P6",
            "type":  "dialogue",
            "bg":    "background/cassava_emptychair.png",
            "chars": {"lucas": {"side": "right", "expression": "concerned", "flip": False}},
            "lines": [
                ("lucas", "Huwag po ninyong pilitin, Lola. Darating din po iyan."),
            ],
        },
 
        # ── Day 200 — Baron's revelation: lonely, not evil ─────
        {
            "id":   "day200_fade",
            "type": "transition",
        },
        {
            "id":    "S12P1",
            "type":  "dialogue",
            "day":   200,
            "bg":    "background/cassava_dusk.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "defeated"}},
            "lines": [
                ("baron", "..."),
                ("baron", "Nabalik na ang halos lahat ng alaala. Natalo na ako."),
            ],
        },
        {
            "id":    "S12P2",
            "type":  "dialogue",
            "bg":    "background/cassava_dusk.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "defeated"}},
            "lines": [
                ("baron", "Hindi ko alam kung bakit ko ginawa ang lahat ng ito. Siguro ay naiinggit ako."),
                ("baron", "Kayo ay nagtutulungan, nagtatawanan, at nagdiriwang... at ako ay nag-iisa."),
            ],
        },
        {
            "id":    "S12P3",
            "type":  "dialogue",
            "bg":    "background/cassava_dusk.png",
            "dark":  True,
            "chars": {"baron": {"side": "right", "expression": "defeated"}},
            "lines": [
                ("baron", "Narinig kong may Pista noon, ngunit nasira ang mga pananim ko at wala akong maibigay na handog. Kaya hindi na ako nagpakita."),
                ("baron", "Mas madali pang kalimutan ng lahat ang Pista kaysa isipin kong walang naghahanap sa akin."),
            ],
        },
        {
            "id":    "S12P4",
            "type":  "dialogue",
            "bg":    "background/cassava_emptychair.png",
            "chars": {"lucas": {"side": "left", "expression": "concerned", "flip": True}},
            "lines": [
                ("lucas", "Kaya po pala... Hindi po kayo galit, Baron. Nasaktan lang po kayo."),
            ],
        },
        {
            "id":    "S12P5",
            "type":  "dialogue",
            "bg":    "background/cassava_emptychair.png",
            "chars": {"lola": {"side": "left", "expression": "sad", "flip": False}},
            "lines": [
                ("lola", "Baron... Naaalala ko na."),
                ("lola", "Noon pa man, tuwing Pista, nag-iiwan kami ng bakanteng upuan sa mesa. Para iyon sa iyo."),
            ],
        },
        {
            "id":    "S12P6",
            "type":  "dialogue",
            "bg":    "background/cassava_dusk.png",
            "dark":  False,
            "chars": {"baron": {"side": "right", "expression": "nervous"}},
            "lines": [
                ("baron", "Para... sa akin?"),
            ],
        },
        {
            "id":    "S12P7",
            "type":  "dialogue",
            "bg":    "background/cassava_emptychair.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Oo, Baron. Naghintay kami, bawat taon."),
                ("lola", "Ang Pista ng Nakalimutang Baryo ay para sa lahat, lalo na sa mga nag-iisa. Hindi mo kailangang magdala ng handog para maupo sa aming mesa."),
                ("lola", "Gusto mo bang sumama sa aming handaan?"),
            ],
        },
        {
            "id":    "S12P8",
            "type":  "dialogue",
            "bg":    "background/cassava_dusk.png",
            "dark":  False,
            "chars": {"baron": {"side": "right", "expression": "renewed"}},
            "lines": [
                ("baron", "Ako... Oo. Oo, gusto ko."),
                ("baron", "Wala akong ibang maibibigay kundi ito. Isang basket ng sariwang lupa mula sa maliit kong hardin, para sa susunod ninyong pananim."),
            ],
        },
        {
            "id":    "S12P9",
            "type":  "dialogue",
            "bg":    "background/cassava_emptychair.png",
            "chars": {"lola": {"side": "left", "expression": "celebrates", "flip": False}},
            "lines": [
                ("lola", "Iyan na ang pinakamagandang handog na natanggap ko."),
            ],
        },
        {
            "id":    "S12P10",
            "type":  "dialogue",
            "bg":    "background/cassava_emptychair.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "Hindi mabubura ng regalong ito ang pinsalang ginawa mo sa mga pananim namin, Baron."),
                ("kapitan", "Ngunit magandang simula ang pananagutan. Tutulong ka sa muling pagtatanim ng baryo."),
            ],
        },
        {
            "id":    "S12P11",
            "type":  "dialogue",
            "bg":    "background/cassava_dusk.png",
            "dark":  False,
            "chars": {"baron": {"side": "right", "expression": "renewed"}},
            "lines": [
                ("baron", "Gagawin ko, Kapitan. Pangako."),
            ],
        },
        {
            "id":    "S12P12",
            "type":  "dialogue",
            "bg":    "background/cassava_emptychair.png",
            "chars": {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "At marami pang kaldero ang hugasan sa kusina pagkatapos ng handaan!"),
            ],
        },
        {
            "id":    "S12P13",
            "type":  "dialogue",
            "bg":    "background/cassava_emptychair.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Hindi na po kayo nag-iisa, Baron."),
            ],
        },
        {
            "id":    "S12P14",
            "type":  "dialogue",
            "bg":    "background/cassava_emptychair.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ganyan ang kapangyarihan ng pagkain at ng pagtitipon, apo. Pinagsasama nito ang lahat, pati ang mga dating magkaaway."),
            ],
        },
 
        # ── Day 201 — Grand Finale: all memories return ────────
        {
            "id":   "day201_fade",
            "type": "transition",
        },
        {
            "id":    "S13P1",
            "type":  "dialogue",
            "day":   201,
            "bg":    "background/cassava_fiesta.png",
            "chars": {"lola": {"side": "left", "expression": "celebrates", "flip": False}},
            "lines": [
                ("lola", "Naaalala ko na ang lahat!"),
                ("lola", "Ang nilagang pechay na inihanda ko para sa una kong palengke. Ang monggo guisado na niluto ko tuwing mahirap na Linggo. Ang sinigang na okra sa hapunan ng pamilya."),
            ],
        },
        {
            "id":    "S13P2",
            "type":  "dialogue",
            "bg":    "background/cassava_fiesta.png",
            "chars": {"lola": {"side": "left", "expression": "default", "flip": False}},
            "lines": [
                ("lola", "Ang kalabasa sa gata na paboritong ulam ng lolo mo. Ang kamatis na sarciado na inihahanda namin tuwing Linggo. Ang kamote cue na ibinebenta natin sa palengke."),
                ("lola", "Ang sinangag at lugaw mula sa bigas. Ang kamoteng kahoy na pinirito, ang suman, at ang bibingka, ang pagkaing nagbibigay ng lakas at tibay."),
            ],
        },
        {
            "id":    "S13P3",
            "type":  "dialogue",
            "bg":    "background/cassava_fiesta.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "At ang kare-kare na nagpapaalala sa akin kung bakit ako naging Kapitan: para magtipon ang buong baryo sa iisang mesa."),
            ],
        },
        {
            "id":    "S13P4",
            "type":  "dialogue",
            "bg":    "background/cassava_fiesta.png",
            "chars": {"chef": {"side": "left", "expression": "happy", "flip": False}},
            "lines": [
                ("chef", "At ang mais na sopas, ang inihaw na mais sa tabi ng ilog, at ang popcorn tuwing Pista!"),
                ("chef", "Ngayon, kasama pa natin si Baron. Mas maraming pagkain, mas maraming kuwento, at mas makulay ang ating handaan!"),
            ],
        },
        {
            "id":    "S13P5",
            "type":  "dialogue",
            "bg":    "background/cassava_fiesta.png",
            "chars": {"lucas": {"side": "left", "expression": "talking", "flip": True}},
            "lines": [
                ("lucas", "Lola, naaalala na po ninyo ang lahat ng sampung alaala. Ang Pista ng Nakalimutang Baryo..."),
            ],
        },
        {
            "id":    "S13P6",
            "type":  "dialogue",
            "bg":    "background/cassava_fiesta.png",
            "chars": {"kapitan": {"side": "right", "flip": False}},
            "lines": [
                ("kapitan", "...ay muling mabubuhay! Sampung pananim. Sampung alaala. Isang baryo, isang handaan."),
            ],
        },
        {
            "id":    "S13P7",
            "type":  "dialogue",
            "bg":    "background/cassava_fiesta.png",
            "chars": {"lucas": {"side": "left", "expression": "thumbs", "flip": True}},
            "lines": [
                ("lucas", "Salamat po, Lola, sa lahat ng itinuro ninyo sa akin. Hindi lang po ang pagtatanim, kundi ang pagmamahal sa lupa, sa pagkain, at sa isa't isa."),
                ("lucas", "Magsisimula na pong muli ang Pista ng Nakalimutang Baryo!"),
            ],
        },
        {
            "id":    "S13P8",
            "type":  "dialogue",
            "bg":    "background/cassava_fiesta.png",
            "chars": {"lola": {"side": "left", "expression": "celebrates", "flip": False}},
            "lines": [
                ("lola", "Kamoteng Kahoy Memory — UNLOCKED!"),
                ("lola", "At ang lahat ng sampung alaala ng Pista ng Nakalimutang Baryo ay nabalik na!"),
            ],
        },
        {
            "id": "S13P9",
            "type": "narration_overlay",
            "day": 201,
            "bg": "background/cassava_fiesta.png",
            "dim_inactive": False,
            "overlay": "woodbg.png",
 
            "narration": (
                "Sa unang pagkakataon, may upuan ang lahat sa mesa, "
                "pati si Baron. "
                "Naibalik na ang Kamoteng Kahoy Memory, at hindi na muling nakalimutan "
                "ang Pista ng Nakalimutang Baryo."
            ),
        },
 
    ],
}