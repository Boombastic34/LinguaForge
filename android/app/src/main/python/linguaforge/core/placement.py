# -*- coding: utf-8 -*-
"""Adaptacyjny test poziomujący 2.0.

Sekcje: vocab (wybór, pasma frekwencyjne) -> vocab_produce (wpisz słowo)
-> grammar (drabinka adaptacyjna) -> reading (parafrazowane pytania)
-> translation -> listening EN (dyktando) -> listening PL->EN.
Każde pytanie losowane z banku. Odpowiedź "zgadywałem" liczy się z wagą 0.35.
"""
import random
from . import storage, skills, grader

GRAMMAR_Q = 14
VOCAB_Q = 10
PRODUCE_Q = 8
READING_TEXTS = 2
TRANSLATION_Q = 4
LISTEN_Q = 4
LISTEN_PL_Q = 3

LEVELS = ["A1", "A2", "B1", "B2", "C1"]
GUESS_W = 0.35   # waga poprawnej odpowiedzi oznaczonej jako "zgadywałem"


def _data():
    return storage.load_data("testy/poziomujacy.json", {})


def _options_fb(q, chosen):
    """Wszystkie opcje z tłumaczeniami — do feedbacku."""
    pls = q.get("options_pl", [])
    out = []
    for i, o in enumerate(q["options"]):
        out.append({"en": o, "pl": pls[i] if i < len(pls) else "",
                    "correct": i == q["answer"], "chosen": chosen == i})
    return out


def new_state():
    d = _data()
    easy = [i for i, t in enumerate(d["reading"]) if t["level"] in ("A1", "A2")]
    hard = [i for i, t in enumerate(d["reading"]) if t["level"] in ("B1", "B2", "C1")]
    random.shuffle(easy)
    random.shuffle(hard)
    texts = (easy[:1] + hard[:1]) or (easy + hard)[:READING_TEXTS]
    return {
        "module": "vocab",
        "vocab": {"asked": [], "results": []},
        "produce": {"asked": [], "results": []},
        "grammar": {"level_idx": 1, "asked": [], "results": []},
        "reading": {"texts": texts, "text_pos": 0, "q_idx": 0, "results": []},
        "translation": {"ids": random.sample([t["id"] for t in d["translation"]],
                                             min(TRANSLATION_Q, len(d["translation"]))),
                        "idx": 0, "results": []},
        "listening": {"ids": random.sample([t["id"] for t in d["listening"]],
                                           min(LISTEN_Q, len(d["listening"]))),
                      "idx": 0, "results": []},
        "listening_pl": {"ids": random.sample([t["id"] for t in d["listening_pl"]],
                                              min(LISTEN_PL_Q, len(d["listening_pl"]))),
                         "idx": 0, "results": []},
        "done": False,
        "last": None,   # ostatnie pytanie czekające na "wiedziałem/zgadywałem"
    }


def total_questions():
    return (GRAMMAR_Q + VOCAB_Q + PRODUCE_Q + READING_TEXTS * 3 +
            TRANSLATION_Q + LISTEN_Q + LISTEN_PL_Q)


def _progress(state):
    done = (len(state["vocab"]["results"]) + len(state["produce"]["results"]) +
            len(state["grammar"]["results"]) + len(state["reading"]["results"]) +
            len(state["translation"]["results"]) + len(state["listening"]["results"]) +
            len(state["listening_pl"]["results"]))
    return round(done / total_questions(), 3)


def next_question(state):
    d = _data()
    m = state["module"]

    if m == "vocab":
        s = state["vocab"]
        if len(s["results"]) >= VOCAB_Q:
            state["module"] = "produce"
            return next_question(state)
        pool = [q for q in d["vocab"] if q["id"] not in s["asked"]]
        q = random.choice(pool)
        s["asked"].append(q["id"])
        return {"module": "vocab", "progress": _progress(state),
                "q": {"id": q["id"], "type": "choice", "text": q["text"],
                      "options": q["options"]}}

    if m == "produce":
        s = state["produce"]
        if len(s["results"]) >= PRODUCE_Q:
            state["module"] = "grammar"
            return next_question(state)
        pool = [q for q in d["vocab_produce"] if q["id"] not in s["asked"]]
        # naprzemiennie rzeczownik/czasownik
        want = "verb" if len(s["results"]) % 2 else "noun"
        cat_pool = [q for q in pool if q["cat"] == want] or pool
        q = random.choice(cat_pool)
        s["asked"].append(q["id"])
        return {"module": "produce", "progress": _progress(state),
                "q": {"id": q["id"], "type": "text",
                      "text": ("Czasownik: " if q["cat"] == "verb" else "Rzeczownik: ") +
                              "napisz po angielsku „" + q["pl"] + "”",
                      "hint": q.get("hint", "")}}

    if m == "grammar":
        s = state["grammar"]
        if len(s["results"]) >= GRAMMAR_Q:
            state["module"] = "reading"
            return next_question(state)
        lvl = LEVELS[s["level_idx"]]
        pool = [q for q in d["grammar"] if q["level"] == lvl and q["id"] not in s["asked"]]
        if not pool:
            pool = [q for q in d["grammar"] if q["id"] not in s["asked"]]
        q = random.choice(pool)
        s["asked"].append(q["id"])
        return {"module": "grammar", "progress": _progress(state),
                "q": {"id": q["id"], "type": "choice", "level": q["level"],
                      "text": q["text"], "options": q["options"]}}

    if m == "reading":
        s = state["reading"]
        if s["text_pos"] >= len(s["texts"]):
            state["module"] = "translation"
            return next_question(state)
        t = d["reading"][s["texts"][s["text_pos"]]]
        if s["q_idx"] >= len(t["questions"]):
            s["text_pos"] += 1
            s["q_idx"] = 0
            return next_question(state)
        q = t["questions"][s["q_idx"]]
        return {"module": "reading", "progress": _progress(state),
                "q": {"id": f"r{s['text_pos']}_{s['q_idx']}", "type": "choice",
                      "level": t["level"], "passage": t["text"], "title": t["title"],
                      "passage_pl": t.get("text_pl", ""),
                      "text": q["text"], "options": q["options"]}}

    if m == "translation":
        s = state["translation"]
        if s["idx"] >= len(s["ids"]):
            state["module"] = "listening"
            return next_question(state)
        it = next(x for x in d["translation"] if x["id"] == s["ids"][s["idx"]])
        return {"module": "translation", "progress": _progress(state),
                "q": {"id": it["id"], "type": "text", "level": it["level"],
                      "text": "Przetłumacz na angielski: „" + it["pl"] + "”"}}

    if m == "listening":
        s = state["listening"]
        if s["idx"] >= len(s["ids"]):
            state["module"] = "listening_pl"
            return next_question(state)
        it = next(x for x in d["listening"] if x["id"] == s["ids"][s["idx"]])
        return {"module": "listening", "progress": _progress(state),
                "q": {"id": it["id"], "type": "dictation", "level": it["level"],
                      "tts": it["en"],
                      "text": "Posłuchaj i zapisz zdanie PO ANGIELSKU."}}

    if m == "listening_pl":
        s = state["listening_pl"]
        if s["idx"] >= len(s["ids"]):
            state["done"] = True
            return {"module": "done", "progress": 1.0}
        it = next(x for x in d["listening_pl"] if x["id"] == s["ids"][s["idx"]])
        return {"module": "listening_pl", "progress": _progress(state),
                "q": {"id": it["id"], "type": "dictation_pl", "level": it["level"],
                      "tts_pl": it["pl"],
                      "text": "Usłyszysz zdanie PO POLSKU — zapisz je PO ANGIELSKU."}}

    state["done"] = True
    return {"module": "done", "progress": 1.0}


def answer(state, qid, answer_value, rt_ms=0):
    """Zwraca feedback z tłumaczeniem; wynik zapisuje dopiero confirm()."""
    d = _data()
    m = state["module"]
    fb = {"correct": False}
    rec = {"id": qid, "rt": rt_ms}

    if m == "vocab":
        q = next(x for x in d["vocab"] if x["id"] == qid)
        correct = answer_value == q["answer"]
        rec.update({"band": q["band"], "correct": correct})
        fb = {"correct": correct, "answer": q["options"][q["answer"]],
              "your": q["options"][answer_value] if isinstance(answer_value, int) and 0 <= answer_value < len(q["options"]) else str(answer_value),
              "pl": q.get("pl", ""), "question": q["text"],
              "options": _options_fb(q, answer_value)}
    elif m == "produce":
        q = next(x for x in d["vocab_produce"] if x["id"] == qid)
        ans = str(answer_value if answer_value != -1 else "").strip().lower()
        correct = ans in [a.lower() for a in q["accept"]]
        rec.update({"band": q["band"], "cat": q["cat"], "correct": correct})
        fb = {"correct": correct, "answer": q["accept"][0], "your": str(answer_value),
              "pl": q["pl"], "question": "„" + q["pl"] + "” po angielsku"}
    elif m == "grammar":
        q = next(x for x in d["grammar"] if x["id"] == qid)
        correct = answer_value == q["answer"]
        rec.update({"level": q["level"], "topic": q.get("topic"), "correct": correct})
        idx = state["grammar"]["level_idx"]
        state["grammar"]["level_idx"] = min(len(LEVELS) - 1, idx + 1) if correct else max(0, idx - 1)
        good = q["options"][q["answer"]]
        if q["text"].count("___") == 1:
            full_en = q["text"].replace("___", good)
        elif "___" not in q["text"]:
            full_en = good
        else:
            full_en = None
        fb = {"correct": correct, "answer": good, "en": full_en, "tts": full_en,
              "your": q["options"][answer_value] if isinstance(answer_value, int) and 0 <= answer_value < len(q["options"]) else str(answer_value),
              "pl": q.get("pl", ""), "explain": q.get("explain", ""), "question": q["text"]}
    elif m == "reading":
        s = state["reading"]
        t = d["reading"][s["texts"][s["text_pos"]]]
        q = t["questions"][s["q_idx"]]
        correct = answer_value == q["answer"]
        rec.update({"level": t["level"], "correct": correct})
        s["q_idx"] += 1
        fb = {"correct": correct, "answer": q["options"][q["answer"]],
              "your": q["options"][answer_value] if isinstance(answer_value, int) and 0 <= answer_value < len(q["options"]) else str(answer_value),
              "pl": q.get("pl", ""), "question": q["text"],
              "options": _options_fb(q, answer_value)}
    elif m == "translation":
        s = state["translation"]
        it = next(x for x in d["translation"] if x["id"] == s["ids"][s["idx"]])
        res = grader.grade_translation(str(answer_value), it)
        rec.update({"level": it["level"], "score": res["score"]})
        s["idx"] += 1
        fb = {"correct": res["score"] >= 0.7, "detail": res, "answer": res["ref"],
              "en": res["ref"], "tts": res["ref"],
              "your": str(answer_value), "pl": it["pl"],
              "explain": it.get("tense_hint", ""),
              "question": "Tłumaczenie: „" + it["pl"] + "”"}
    elif m == "listening":
        s = state["listening"]
        it = next(x for x in d["listening"] if x["id"] == s["ids"][s["idx"]])
        res = grader.grade_dictation(str(answer_value), it["en"])
        rec.update({"level": it["level"], "score": res["score"]})
        s["idx"] += 1
        fb = {"correct": res["score"] >= 0.75, "detail": res, "answer": it["en"],
              "en": it["en"], "your": str(answer_value), "pl": it.get("pl", ""),
              "tts": it["en"], "question": "Dyktando"}
    elif m == "listening_pl":
        s = state["listening_pl"]
        it = next(x for x in d["listening_pl"] if x["id"] == s["ids"][s["idx"]])
        res = grader.grade_translation(str(answer_value), it)
        rec.update({"level": it["level"], "score": res["score"]})
        s["idx"] += 1
        fb = {"correct": res["score"] >= 0.7, "detail": res, "answer": it["en_ref"],
              "en": it["en_ref"], "your": str(answer_value), "pl": it["pl"],
              "tts": it["en_ref"], "explain": "Konstrukcja: " + it.get("tense_name", ""),
              "question": "Ze słuchu PL→EN: „" + it["pl"] + "”"}

    state["last"] = {"module": m, "rec": rec, "correct": fb["correct"]}
    fb["ask_known"] = bool(fb["correct"]) and m in ("vocab", "grammar", "reading")
    return fb


def confirm(state, guessed=False):
    """Zapisuje wynik ostatniego pytania (z wagą za zgadywanie)."""
    last = state.get("last")
    if not last:
        return
    rec = dict(last["rec"])
    if guessed and last["correct"]:
        rec["guessed"] = True
        if "correct" in rec:
            rec["weight"] = GUESS_W
    m = last["module"]
    key = {"vocab": "vocab", "produce": "produce", "grammar": "grammar",
           "reading": "reading", "translation": "translation",
           "listening": "listening", "listening_pl": "listening_pl"}[m]
    state[key]["results"].append(rec)
    state["last"] = None


def _w(r):
    return r.get("weight", 1.0)


def finalize(state):
    pts = {"A1": 12, "A2": 30, "B1": 50, "B2": 68, "C1": 85}

    # gramatyka
    g = state["grammar"]["results"]
    topics = {}
    gvals = []
    for r in g:
        base = pts[r["level"]]
        eff = (1.0 if r["correct"] else 0.0) * _w(r)
        gvals.append(base * (0.35 + 0.65 * eff))
        if r.get("topic"):
            t = topics.setdefault(r["topic"], {"n": 0, "ok": 0.0})
            t["n"] += 1
            t["ok"] += eff
    gscore = sum(gvals) / len(gvals) if gvals else 0

    # słownictwo: wybór + produkcja -> zasób słów
    bands = {}
    for r in state["vocab"]["results"]:
        b = bands.setdefault(r["band"], {"n": 0, "ok": 0.0})
        b["n"] += 1
        b["ok"] += (1.0 if r["correct"] else 0.0) * _w(r)
    for r in state["produce"]["results"]:
        b = bands.setdefault(r["band"], {"n": 0, "ok": 0.0})
        b["n"] += 1
        b["ok"] += 1.2 if r["correct"] else 0.0   # produkcja warta więcej
    vocab_size = 0
    for band, bb in bands.items():
        acc = min(1.0, bb["ok"] / bb["n"])
        vocab_size += int(band * 0.4 * acc)
    vocab_size = min(9000, vocab_size)
    vscore = max(min(100, vocab_size / 90),
                 next((skills.LEVEL_SCORE[L] for L in reversed(skills.LEVELS)
                       if vocab_size >= skills.VOCAB_SIZE[L] * 0.8), 0))

    def module_score(results, scored=False):
        if not results:
            return 0
        vals = []
        for r in results:
            base = pts.get(r.get("level", "B1"), 40)
            eff = (r.get("score", 0) if scored else (1.0 if r.get("correct") else 0.0)) * _w(r)
            vals.append(base * (0.35 + 0.65 * eff))
        return sum(vals) / len(vals)

    rscore = module_score(state["reading"]["results"])
    tscore = module_score(state["translation"]["results"], scored=True)
    l_en = module_score(state["listening"]["results"], scored=True)
    l_pl = module_score(state["listening_pl"]["results"], scored=True)
    lscore = (l_en * 0.6 + l_pl * 0.4) if state["listening_pl"]["results"] else l_en
    wscore = (tscore * 0.7 + l_pl * 0.3) if state["listening_pl"]["results"] else tscore

    grammar_topics = {t: round(100.0 * v["ok"] / v["n"], 1) for t, v in topics.items()}
    prof_skills = {
        "vocab": round(vscore, 1), "grammar": round(gscore, 1),
        "reading": round(rscore, 1), "listening": round(lscore, 1),
        "writing": round(wscore, 1),
        "grammar_topics": grammar_topics,
        "vocab_size_est": vocab_size,
    }
    guessed_n = sum(1 for sec in ("vocab", "grammar", "reading")
                    for r in state[sec]["results"] if r.get("guessed"))
    level = skills.score_to_level(skills.overall(prof_skills))
    return {"skills": prof_skills, "level": level,
            "cefr": skills.cefr_profile(prof_skills),
            "vocab_size_est": vocab_size, "guessed": guessed_n,
            "questions": total_questions()}
