# -*- coding: utf-8 -*-
"""Model ucznia: wektor umiejętności 0-100, mapowanie CEFR, estymator czasu.

Aktualizacja w stylu Elo: wynik zadania vs trudność zadania przesuwa ocenę.
Czas odpowiedzi moduluje siłę aktualizacji (szybka poprawna > wolna poprawna).
"""
import datetime

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
# progi na skali 0-100
THRESH = {"A1": 8, "A2": 25, "B1": 45, "B2": 65, "C1": 82, "C2": 95}
LEVEL_SCORE = {"A1": 15, "A2": 35, "B1": 55, "B2": 72, "C1": 88, "C2": 97}

# szacowany zasób słów wymagany na poziom (za listami frekwencyjnymi / Nation)
VOCAB_SIZE = {"A1": 600, "A2": 1400, "B1": 2600, "B2": 4200, "C1": 6500, "C2": 9000}


def score_to_level(score: float) -> str:
    lvl = "A1"
    for L in LEVELS:
        if score >= THRESH[L]:
            lvl = L
    return lvl


def level_to_score(level: str) -> float:
    return LEVEL_SCORE.get(level, 15)


def update_skill(current: float, task_level: str, correct: bool, rt_ms=None) -> float:
    """Elo-podobna aktualizacja. task_level: poziom CEFR zadania."""
    task = level_to_score(task_level)
    expected = 1.0 / (1.0 + 10 ** ((task - current) / 25.0))
    outcome = 1.0 if correct else 0.0
    k = 3.0
    if rt_ms is not None and correct:
        if rt_ms < 4000:
            k = 3.6          # pewna, szybka odpowiedź
        elif rt_ms > 15000:
            k = 2.0          # poprawna, ale z trudem
    new = current + k * (outcome - expected)
    return round(min(100.0, max(0.0, new)), 2)


def overall(skills: dict) -> float:
    core = [skills.get("vocab", 0), skills.get("grammar", 0),
            skills.get("reading", 0), skills.get("listening", 0),
            skills.get("writing", 0)]
    core = [c for c in core if c > 0] or [0]
    return round(sum(core) / len(core), 1)


def weakest(skills: dict):
    pairs = [(k, skills.get(k, 0)) for k in
             ("vocab", "grammar", "reading", "listening", "writing")]
    pairs.sort(key=lambda p: p[1])
    return pairs


def cefr_profile(skills: dict) -> dict:
    return {k: score_to_level(skills.get(k, 0)) for k in
            ("vocab", "grammar", "reading", "listening", "writing")}


def estimate_weeks(profile: dict, cards: dict, target_level: str) -> dict:
    """Prognoza: ile tygodni do celu przy obecnym tempie.

    Podstawa: ile słów 'opanowanych' przybywa tygodniowo + dystans w skali skills.
    """
    from . import fsrs
    mature = sum(1 for c in cards.values() if fsrs.is_mature(c["fsrs"]))
    need_words = VOCAB_SIZE.get(target_level, 2600)
    words_left = max(0, need_words - profile["skills"].get("vocab_size_est", 0) - mature)

    # tempo z ostatnich 14 dni
    today = datetime.date.today()
    days = [(today - datetime.timedelta(days=i)).isoformat() for i in range(14)]
    xp14 = sum(profile.get("daily", {}).get(d, {}).get("xp", 0) for d in days)
    ans14 = sum(profile.get("daily", {}).get(d, {}).get("answers", 0) for d in days)
    # ~przyjęcie: 1 nowe opanowane słowo na ~9 odpowiedzi (nauka+powtórki)
    words_per_week = max(1.0, (ans14 / 2.0) / 9.0)

    cur = overall(profile["skills"])
    target = LEVEL_SCORE.get(target_level, 55)
    skill_gap = max(0.0, target - cur)
    # ~1 pkt skali na 90 XP przy zrównoważonej nauce
    xp_per_week = max(10.0, xp14 / 2.0)
    weeks_by_skill = skill_gap * 90.0 / xp_per_week
    weeks_by_words = words_left / words_per_week
    weeks = round(max(weeks_by_skill, weeks_by_words), 1)
    return {
        "weeks": weeks,
        "words_left": words_left,
        "mature_words": mature,
        "pace_answers_14d": ans14,
        "xp_14d": xp14,
        "confidence": "niska" if ans14 < 60 else ("średnia" if ans14 < 300 else "dobra"),
    }


def register_activity(profile: dict, correct: bool, xp: int):
    today = datetime.date.today().isoformat()
    d = profile.setdefault("daily", {}).setdefault(
        today, {"answers": 0, "correct": 0, "xp": 0})
    d["answers"] += 1
    d["correct"] += 1 if correct else 0
    d["xp"] += xp
    profile["xp"] = profile.get("xp", 0) + xp
    # streak
    last = profile.get("last_active_day")
    if last != today:
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        profile["streak"] = profile.get("streak", 0) + 1 if last == yesterday else 1
        profile["last_active_day"] = today
