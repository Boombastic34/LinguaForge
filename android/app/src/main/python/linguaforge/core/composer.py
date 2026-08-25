# -*- coding: utf-8 -*-
"""Kompozytor sesji: miesza typy zadań (interleaving) i waży je tak,
by najsłabsza umiejętność dostawała najwięcej pracy, a mocne były nośnikiem.
"""
from . import skills as sk


def session_plan(profile, due_cards: int, session_len: int = 12):
    """Zwraca plan sesji: lista typów zadań w kolejności."""
    weak = sk.weakest(profile["skills"])  # [(nazwa, wartość)...] rosnąco
    weights = {"flash_review": 0.0, "flash_new": 0.0, "grammar": 0.0,
               "translate": 0.0, "listen": 0.0}
    # powtórki zawsze priorytetem (spacing effect)
    weights["flash_review"] = min(0.45, 0.08 * due_cards)
    name_map = {"vocab": ["flash_new"], "grammar": ["grammar"],
                "writing": ["translate"], "listening": ["listen"],
                "reading": ["translate"]}
    # najsłabsza -> waga 3, kolejna 2, potem 1
    boost = [3.0, 2.0, 1.2, 1.0, 0.8]
    for i, (name, _val) in enumerate(weak):
        for t in name_map.get(name, []):
            weights[t] += boost[min(i, 4)]
    total = sum(weights.values()) or 1
    plan = []
    import random
    types = list(weights.keys())
    probs = [weights[t] / total for t in types]
    for _ in range(session_len):
        r = random.random()
        acc = 0
        for t, p in zip(types, probs):
            acc += p
            if r <= acc:
                plan.append(t)
                break
        else:
            plan.append("flash_review")
    # interleaving: nie więcej niż 3 tego samego pod rząd
    for i in range(2, len(plan)):
        if plan[i] == plan[i - 1] == plan[i - 2]:
            for t in types:
                if t != plan[i]:
                    plan[i] = t
                    break
    return plan


def focus_message(profile):
    weak = sk.weakest(profile["skills"])
    names = {"vocab": "słownictwo", "grammar": "gramatyka", "reading": "czytanie",
             "listening": "słuchanie", "writing": "pisanie/tłumaczenie"}
    w = weak[0]
    s = weak[-1]
    return (f"Najsłabszy obszar: {names[w[0]]} ({sk.score_to_level(w[1])}). "
            f"Najmocniejszy: {names[s[0]]} ({sk.score_to_level(s[1])}). "
            f"Sesje kładą teraz nacisk na {names[w[0]]}, podane w kontekście "
            f"Twojego mocniejszego poziomu.")
