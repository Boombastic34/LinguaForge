# -*- coding: utf-8 -*-
"""FSRS (Free Spaced Repetition Scheduler) — uproszczona implementacja v4.5.

Każda karta ma: difficulty (D, 1-10), stability (S, dni), reps, lapses, state,
last_review, due. Ocena: 1=Again, 2=Hard, 3=Good, 4=Easy.
Planowanie na moment, gdy przewidywane przypomnienie spada do ~90%.
"""
import math, time

# Domyślne wagi FSRS-4.5 (wytrenowane na dużych zbiorach powtórek Anki)
W = [0.4872, 1.4003, 3.7145, 13.8206, 5.1618, 1.2298, 0.8975, 0.031,
     1.6474, 0.1367, 1.0461, 2.1072, 0.0793, 0.3246, 1.587, 0.2272, 2.8755]

REQUEST_RETENTION = 0.90
DAY = 86400.0
FACTOR = 19.0 / 81.0
DECAY = -0.5


def new_card():
    return {"state": "new", "D": 0.0, "S": 0.0, "reps": 0, "lapses": 0,
            "last": 0.0, "due": time.time(), "history": []}


def retrievability(card, now=None):
    if card["state"] == "new" or card["S"] <= 0:
        return 0.0
    now = now or time.time()
    t = max(0.0, (now - card["last"]) / DAY)
    return (1.0 + FACTOR * t / card["S"]) ** DECAY


def _init_difficulty(rating):
    d = W[4] - math.exp(W[5] * (rating - 1)) + 1
    return min(10.0, max(1.0, d))


def _init_stability(rating):
    return max(0.1, W[rating - 1])


def _next_difficulty(d, rating):
    nd = d - W[6] * (rating - 3)
    nd = W[7] * _init_difficulty(4) + (1 - W[7]) * nd  # mean reversion
    return min(10.0, max(1.0, nd))


def _stability_success(d, s, r, rating):
    hard = W[15] if rating == 2 else 1.0
    easy = W[16] if rating == 4 else 1.0
    inc = (math.exp(W[8]) * (11 - d) * (s ** -W[9]) *
           (math.exp(W[10] * (1 - r)) - 1) * hard * easy)
    return s * (1 + inc)


def _stability_fail(d, s, r):
    ns = (W[11] * (d ** -W[12]) * ((s + 1) ** W[13] - 1) *
          math.exp(W[14] * (1 - r)))
    return max(0.1, min(ns, s))


def interval_for(stability):
    ivl = stability / FACTOR * (REQUEST_RETENTION ** (1 / DECAY) - 1)
    return max(1, round(ivl))


def review(card, rating, now=None):
    """Aktualizuje kartę po ocenie. Zwraca kartę."""
    now = now or time.time()
    r = retrievability(card, now)
    if card["state"] == "new":
        card["D"] = _init_difficulty(rating)
        card["S"] = _init_stability(rating)
        card["state"] = "learning"
    else:
        card["D"] = _next_difficulty(card["D"], rating)
        if rating == 1:
            card["S"] = _stability_fail(card["D"], card["S"], r)
            card["lapses"] += 1
            card["state"] = "relearning"
        else:
            card["S"] = _stability_success(card["D"], card["S"], r, rating)
            card["state"] = "review"
    card["reps"] += 1
    card["last"] = now
    if rating == 1:
        due_in = 10 * 60          # 10 minut — jeszcze w tej sesji
    elif card["state"] == "learning" and card["reps"] <= 1 and rating < 4:
        due_in = 30 * 60
    else:
        due_in = interval_for(card["S"]) * DAY
    card["due"] = now + due_in
    card["history"].append({"ts": now, "rating": rating,
                            "S": round(card["S"], 2), "D": round(card["D"], 2)})
    if len(card["history"]) > 50:
        card["history"] = card["history"][-50:]
    return card


def is_mature(card):
    """Karta 'opanowana': stabilność >= 21 dni i >=4 powtórki bez świeżej wpadki."""
    return card["state"] == "review" and card["S"] >= 21 and card["reps"] >= 4


def is_leech(card):
    return card["lapses"] >= 4
