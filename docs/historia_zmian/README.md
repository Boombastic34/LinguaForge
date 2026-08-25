# LinguaForge — historia zmian

Każda wersja aplikacji ma tutaj swój plik: co się zmieniło, jakie funkcje dodano/usunięto,
napotkane problemy i ogólny zarys stanu aplikacji.

## O aplikacji
LinguaForge to lokalna aplikacja do nauki angielskiego (Python + FastAPI + przeglądarka, port 8177).
Moduły: test poziomujący, fiszki FSRS, czasowniki w czasach, lekcje-podręcznik ze sprawdzianami,
gramatyka (tematy + trening mieszany), tłumaczenia PL→EN, słuchanie dwukierunkowe, gry,
programy od nauczyciela, panel nauczyciela z arkuszami prac i kreatorem zadań.
Dane w plikach JSON w `data/` — treści dodaje się przez edycję/dodanie plików.
Konta w `accounts/<login>/` — profil, karty, logi dzienne (JSONL).

## Wersje
- v0.1.0 — pierwsza wersja (silnik: FSRS, Elo, test adaptacyjny, grader 3-osiowy)
- v0.2.0 — feedback z tłumaczeniami, lekcje, czasowniki, arkusze nauczyciela, kreator 2.0
- v0.2.1 — poprawki: skróty w ocenie, częściowa punktacja, pełne zdania EN+PL w feedbacku,
  łatwe teksty czytania z tłumaczeniami, nazwy czasów przy formach czasowników, fiszki
  z wpisywaniem dwukierunkowym, fix podwójnego pulpitu
