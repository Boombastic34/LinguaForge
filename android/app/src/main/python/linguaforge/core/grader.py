# -*- coding: utf-8 -*-
"""Ocena tłumaczeń i pisania: 3 osie — sens (słowa kluczowe), czas gramatyczny,
kompletność. Synonimy dozwolone, czas jest twardym wymogiem.
Zwraca też klasyfikację błędu do 'mapy słabości'.
"""
import re
import difflib

ERROR_TYPES = {
    "tense": "Zły czas gramatyczny",
    "keyword": "Brak kluczowego słowa / złe słowo",
    "spelling": "Literówka / pisownia",
    "article": "Przedimek (a/an/the)",
    "order": "Szyk zdania",
    "incomplete": "Zdanie niekompletne",
}


# Skróty oficjalne i potoczne — uznajemy je za odpowiedniki pełnych form.
CONTRACTIONS = {
    "u": "you", "ur": "your", "r": "are", "im": "i'm", "ive": "i've",
    "id": "i'd", "ill": "i'll", "dont": "don't", "doesnt": "doesn't",
    "didnt": "didn't", "cant": "can't", "wont": "won't", "isnt": "isn't",
    "arent": "aren't", "wasnt": "wasn't", "werent": "weren't",
    "havent": "haven't", "hasnt": "hasn't", "hadnt": "hadn't",
    "couldnt": "couldn't", "shouldnt": "shouldn't", "wouldnt": "wouldn't",
    "gonna": "going to", "wanna": "want to",
}
EXPAND = {
    "i'm": "i am", "you're": "you are", "he's": "he is", "she's": "she is",
    "it's": "it is", "we're": "we are", "they're": "they are",
    "i've": "i have", "you've": "you have", "we've": "we have", "they've": "they have",
    "i'll": "i will", "you'll": "you will", "he'll": "he will", "she'll": "she will",
    "we'll": "we will", "they'll": "they will", "i'd": "i would",
    "don't": "do not", "doesn't": "does not", "didn't": "did not",
    "can't": "cannot", "won't": "will not", "isn't": "is not",
    "aren't": "are not", "wasn't": "was not", "weren't": "were not",
    "haven't": "have not", "hasn't": "has not", "hadn't": "had not",
}


def _norm(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    words = [CONTRACTIONS.get(w, w) for w in text.split()]
    text = " ".join(words)
    for c, full in EXPAND.items():
        text = text.replace(c, full)
    return text.strip()


# Słowa funkcyjne — trafienie ich samo w sobie nie świadczy o znajomości zdania.
STOPWORDS = {"a", "an", "the", "i", "you", "he", "she", "it", "we", "they", "my", "your",
             "his", "her", "our", "their", "is", "am", "are", "was", "were", "be", "been",
             "do", "does", "did", "to", "of", "in", "on", "at", "for", "and", "or", "but",
             "this", "that", "these", "those", "not", "with", "as", "by", "from"}


def word_similarity(answer: str, ref: str):
    """(0..1, %) — pokrycie słów wzorca, z naciskiem na słowa TREŚCIOWE."""
    a, b = _words(answer), _words(ref)
    if not a or not b:
        return 0.0, 0

    def cover(target):
        if not target:
            return None
        matched, used = 0, [False] * len(a)
        for w in target:
            for i, x in enumerate(a):
                if used[i]:
                    continue
                if x == w or difflib.SequenceMatcher(None, x, w).ratio() >= 0.82:
                    used[i] = True
                    matched += 1
                    break
        return matched / len(target)

    all_cov = cover(b)
    content = [w for w in b if w not in STOPWORDS]
    con_cov = cover(content)
    order = difflib.SequenceMatcher(None, a, b).ratio()
    if con_cov is None:          # zdanie z samych słów funkcyjnych
        base = all_cov
    else:                        # treść waży najwięcej
        base = 0.65 * con_cov + 0.20 * all_cov + 0.15 * order
    return round(base, 3), round(100 * (con_cov if con_cov is not None else all_cov))


def _words(text: str):
    return _norm(text).split()


def check_keywords(answer: str, keyword_groups):
    """keyword_groups: [["went","travelled"], ["yesterday"]] — z każdej grupy min. 1."""
    words = set(_words(answer))
    text = _norm(answer)
    hits, misses = [], []
    for group in keyword_groups:
        ok = False
        for kw in group:
            kwn = _norm(kw)
            if (" " in kwn and kwn in text) or kwn in words:
                ok = True
                hits.append(kw)
                break
        if not ok:
            # tolerancja literówek (odległość edycyjna przez difflib)
            best = None
            for kw in group:
                for w in words:
                    ratio = difflib.SequenceMatcher(None, _norm(kw), w).ratio()
                    if ratio >= 0.82:
                        best = (kw, w)
            if best:
                hits.append(best[0])
                misses.append({"type": "spelling", "expected": best[0], "got": best[1]})
            else:
                misses.append({"type": "keyword", "expected": group[0]})
                continue
    score = len(hits) / max(1, len(keyword_groups))
    return score, hits, misses


def check_tense(answer: str, tense_patterns, forbidden_patterns=None):
    """tense_patterns: lista regexów, z których min. 1 musi wystąpić.
    forbidden_patterns: regexy typowych pomyłek (np. Past Simple zamiast Perfect)."""
    text = " " + _norm(answer) + " "
    ok = any(re.search(p, text) for p in tense_patterns) if tense_patterns else True
    wrong = None
    if forbidden_patterns:
        for entry in forbidden_patterns:
            label, pats = entry[0], entry[1:]
            if any(re.search(p, text) for p in pats):
                wrong = label
                break
    if wrong:
        ok = False
    return ok, wrong


def grade_translation(answer: str, item: dict) -> dict:
    """item: {en_ref, keywords, tense_name, tense_patterns, forbidden, level}"""
    answer = answer.strip()
    if len(_words(answer)) < 2:
        return {"score": 0, "sense": 0, "tense_ok": False,
                "errors": [{"type": "incomplete"}],
                "feedback": "Zdanie jest niekompletne — napisz pełne zdanie.",
                "ref": item.get("en_ref", "")}

    sense, hits, misses = check_keywords(answer, item.get("keywords", []))
    tense_ok, wrong_tense = check_tense(
        answer, item.get("tense_patterns", []),
        item.get("forbidden", []))

    errors = list(misses)
    fb = []
    if sense >= 0.99:
        fb.append("Sens: ✔ wszystkie kluczowe elementy są.")
    elif sense >= 0.6:
        fb.append(f"Sens: częściowo ({int(sense*100)}%). Zabrakło: " +
                  ", ".join(m.get("expected", "?") for m in misses if m["type"] == "keyword"))
    else:
        fb.append("Sens: zdanie mija się z oryginałem.")

    if tense_ok:
        fb.append(f"Czas: ✔ poprawny ({item.get('tense_name','')}).")
    else:
        errors.append({"type": "tense", "expected": item.get("tense_name", "")})
        if wrong_tense:
            fb.append(f"Czas: ✘ użyłeś {wrong_tense}, a wymagany jest "
                      f"{item.get('tense_name','inny czas')}. {item.get('tense_hint','')}")
        else:
            fb.append(f"Czas: ✘ wymagany {item.get('tense_name','')}. {item.get('tense_hint','')}")

    for m in misses:
        if m["type"] == "spelling":
            fb.append(f"Pisownia: '{m['got']}' → '{m['expected']}'.")

    # wynik: sens 45% + czas 30% + podobieństwo słów do wzorca 25%
    sim, word_pct = word_similarity(answer, item.get("en_ref", ""))
    fb.append(f"Zgodność ze wzorcem: {word_pct}% słów.")
    score = round(sense * 0.45 + (1.0 if tense_ok else 0.0) * 0.30 + sim * 0.25, 2)
    if sense < 0.6:              # brak kluczowych słów = najwyżej „prawie”
        score = min(score, 0.45)
        fb.append("Brakuje kluczowego słownictwa — to jeszcze nie jest poprawna odpowiedź.")
    return {"score": score, "sense": round(sense, 2), "tense_ok": tense_ok,
            "word_pct": word_pct, "errors": errors, "feedback": " ".join(fb),
            "hint": item.get("tense_hint", ""),
            "ref": item.get("en_ref", "")}


def grade_dictation(answer: str, target: str) -> dict:
<<<<<<< HEAD
    """Dyktando: porównanie słowo po słowie."""
    a, t = _words(answer), _words(target)
    sm = difflib.SequenceMatcher(None, t, a)
    ratio = sm.ratio()
    diff = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            diff.append({"ok": " ".join(t[i1:i2])})
        elif op == "replace":
            diff.append({"exp": " ".join(t[i1:i2]), "got": " ".join(a[j1:j2])})
        elif op == "delete":
            diff.append({"exp": " ".join(t[i1:i2]), "got": ""})
        elif op == "insert":
            diff.append({"exp": "", "got": " ".join(a[j1:j2])})
    return {"score": round(ratio, 2), "diff": diff, "target": target}
=======
    """Dyktando: ocena słowo po słowie.

    Wynik = odsetek TRAFIONYCH SŁÓW (nie podobieństwo tekstu). Wcześniej używany
    SequenceMatcher.ratio() liczył podobieństwo znaków całego zdania, przez co
    "way" zamiast "wear" dawało ~97% i przechodziło jako poprawne.
    Każde słowo jest teraz albo trafione, albo nie — bez półśrodków.
    """
    a, t = _words(answer), _words(target)
    sm = difflib.SequenceMatcher(None, t, a)
    diff, hits = [], 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for w in t[i1:i2]:
                diff.append({"w": w, "ok": True})
            hits += (i2 - i1)
        elif op == "replace":
            exp, got = t[i1:i2], a[j1:j2]
            for k in range(max(len(exp), len(got))):
                diff.append({"w": got[k] if k < len(got) else "",
                             "exp": exp[k] if k < len(exp) else "",
                             "ok": False, "kind": "wrong"})
        elif op == "delete":                 # uczeń pominął słowo
            for w in t[i1:i2]:
                diff.append({"w": "", "exp": w, "ok": False, "kind": "missing"})
        elif op == "insert":                 # uczeń dopisał coś zbędnego
            for w in a[j1:j2]:
                diff.append({"w": w, "exp": "", "ok": False, "kind": "extra"})
    total = max(1, len(t))
    score = hits / total
    wrong_words = [d for d in diff if not d.get("ok")]
    return {"score": round(score, 2), "diff": diff, "target": target,
            "hits": hits, "total": total,
            "pct": round(100 * score),
            "wrong": [d.get("exp") or d.get("w") for d in wrong_words]}
>>>>>>> 8f567b6 (LinguaForge v1.6.0 update)


PL_MAP = str.maketrans("ąćęłńóśźż", "acelnoszz")


def _norm_pl(text: str) -> str:
    text = text.lower().strip().translate(PL_MAP)
    text = re.sub(r"[^a-z0-9' -]+", " ", text)
    return re.sub(r"\s+", " ", text)


def grade_open_pl(answer: str, keyword_groups):
    """Ocena odpowiedzi opisowej po polsku: z każdej grupy pojęć min. 1 trafienie
    (wystarczy rdzeń słowa, np. 'przeszł' łapie 'przeszłości')."""
    text = _norm_pl(answer)
    if len(text.split()) < 3:
        return {"score": 0.0, "hit": [], "missed": [g[0] for g in keyword_groups],
                "msg": "Odpowiedź jest zbyt krótka — opisz pełnym zdaniem."}
    hit, missed = [], []
    for group in keyword_groups:
        if any(_norm_pl(k) in text for k in group):
            hit.append(group[0])
        else:
            missed.append(group[0])
    score = round(len(hit) / max(1, len(keyword_groups)), 2)
    if score >= 0.99:
        msg = "Wszystkie kluczowe elementy odpowiedzi są. ✔"
    elif score >= 0.5:
        msg = "Częściowo dobrze — w odpowiedzi zabrakło wątku: " + ", ".join(missed) + "."
    else:
        msg = "Odpowiedź mija się z sednem. Kluczowe wątki: " + ", ".join(missed) + "."
    return {"score": score, "hit": hit, "missed": missed, "msg": msg}


# ---------- wspólny werdykt: dobrze / prawie / źle ----------
PASS = 0.7          # od tego progu zadanie jest zaliczone
PARTIAL = 0.4       # poniżej PASS, ale od tego progu to „prawie”


def verdict(score, pass_at=PASS, partial_at=PARTIAL):
    """Zwraca ('good'|'partial'|'bad', etykieta) — używane wszędzie tak samo."""
    if score >= pass_at:
        return "good", "Dobrze!"
    if score >= partial_at:
        return "partial", "Prawie — częściowo dobrze"
    return "bad", "Niestety nie"


# ---------- ocena dłuższych wypowiedzi pisemnych ----------
COMMON_WRITING_ERRORS = [
    (r"\bi\s", "„i” piszemy zawsze wielką literą: I", lambda t: re.search(r"(?<![a-z])i(?=\s)", t) is not None),
]


def grade_writing(text, task):
    """Trzy osie: kompletność (czy są wymagane elementy), długość, poprawność językowa."""
    raw = (text or "").strip()
    words = [w for w in re.findall(r"[A-Za-z']+", raw)]
    n = len(words)
    low = " " + raw.lower() + " "

    # 1) kompletność — wymagane elementy treści
    hit, missed = [], []
    for i, group in enumerate(task.get("must", [])):
        label = task.get("must_pl", [])[i] if i < len(task.get("must_pl", [])) else group[0]
        if any(k.lower() in low for k in group):
            hit.append(label)
        else:
            missed.append(label)
    completeness = len(hit) / max(1, len(task.get("must", [])))

    # 2) długość
    minw = task.get("min_words", 40)
    length = min(1.0, n / minw)

    # 3) poprawność — proste, pewne reguły
    issues = []
    sentences = [s.strip() for s in re.split(r"[.!?]+", raw) if s.strip()]
    if re.search(r"(?<![A-Za-z])i(?![A-Za-z'])", raw):
        issues.append("Zaimek „I” (ja) zawsze piszemy wielką literą.")
    for s in sentences:
        if s and s[0].islower():
            issues.append("Zdanie zaczynaj wielką literą: „" + s[:26] + "…”.")
            break
    if sentences and not re.search(r"[.!?]\s*$", raw):
        issues.append("Ostatnie zdanie nie ma kropki.")
    if re.search(r"\bi\s+am\s+agree\b|\bi\s+have\s+\d+\s+years\b", low):
        issues.append("Kalka z polskiego: mów „I agree” oraz „I am 30 years old”.")
    if re.search(r"\bdon't\s+\w+s\b", low):
        issues.append("Po don't/doesn't czasownik zostaje w formie podstawowej (bez -s).")
    if n and len(set(w.lower() for w in words)) / n < 0.45 and n > 25:
        issues.append("Sporo powtórzeń — spróbuj użyć bardziej różnorodnych słów.")
    avg = n / max(1, len(sentences))
    if sentences and avg < 4 and n > 20:
        issues.append("Zdania są bardzo krótkie — spróbuj łączyć je przez „and”, „but”, „because”.")
    correctness = max(0.0, 1.0 - 0.18 * len(issues))

    score = round(completeness * 0.5 + length * 0.2 + correctness * 0.3, 2)
    state, label = verdict(score, pass_at=0.65, partial_at=0.4)
    return {"score": score, "state": state, "label": label,
            "completeness": round(completeness, 2), "length_ratio": round(length, 2),
            "correctness": round(correctness, 2), "words": n,
            "sentences": len(sentences), "hit": hit, "missed": missed,
            "issues": issues[:6]}
