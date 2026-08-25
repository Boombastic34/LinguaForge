# Jak sprawić, żeby aplikacja nie wyłączała się po wyjściu z niej

Android agresywnie zamyka programy działające w tle — to on zatrzymuje serwer, nie sama
aplikacja. Poniżej wszystko, co realnie pomaga, od najskuteczniejszego.

---

## 1. Zawsze: wyłącz oszczędzanie baterii dla aplikacji z Pythonem

To najważniejszy krok — bez niego reszta niewiele da.

**Ustawienia telefonu → Aplikacje → (Pydroid 3 albo Termux) → Bateria → Bez ograniczeń.**

Nazwa różni się zależnie od producenta:
- Samsung: *Bateria → Nieograniczone*, dodatkowo **Ustawienia → Bateria → Limity użycia
  w tle → Aplikacje w trybie uśpienia** — upewnij się, że nie ma tam Pydroida/Termuksa.
- Xiaomi / Redmi: *Oszczędzanie baterii → Brak ograniczeń*, a w menu ostatnich aplikacji
  przytrzymaj kartę aplikacji i **dotknij kłódki** (blokada przed zamknięciem).
- Huawei: *Uruchamianie aplikacji → zarządzaj ręcznie → wszystko włączone*.
- OnePlus / Oppo / realme: *Zaawansowana optymalizacja → wyłącz „Głębokie oczyszczanie"*.

Dodatkowo: **nie usuwaj aplikacji z listy ostatnich aplikacji** (nie przesuwaj karty w bok) —
to natychmiast zabija serwer.

---

## 2. Termux — rozwiązanie najpewniejsze

Termux potrafi działać jako aplikacja pierwszoplanowa ze stałym powiadomieniem, dzięki czemu
Android jej nie zamyka.

1. Zainstaluj z **F-Droid** dodatek **Termux:API** (obok samego Termuksa),
   a w Termuksie wykonaj raz: `pkg install termux-api`
2. Uruchamiaj aplikację przez:
   ```
   cd ~/LinguaForge/telefon
   bash start.sh
   ```
   Skrypt sam włącza **blokadę uśpienia procesora** (`termux-wake-lock`) i tworzy
   **stałe powiadomienie „LinguaForge działa"**. Dopóki widzisz to powiadomienie,
   serwer żyje — możesz swobodnie przełączać się między aplikacjami.

3. Wariant jeszcze mocniejszy — serwer działa nawet po zamknięciu okna Termuksa:
   ```
   bash telefon/start_w_tle.sh      # uruchom
   bash telefon/stop.sh             # zatrzymaj
   ```

4. Automatyczny start po włączeniu telefonu: zainstaluj z F-Droid **Termux:Boot**, potem:
   ```
   mkdir -p ~/.termux/boot
   printf '#!/data/data/com.termux/files/usr/bin/bash\nbash ~/LinguaForge/telefon/start_w_tle.sh\n' > ~/.termux/boot/linguaforge
   chmod +x ~/.termux/boot/linguaforge
   ```
   Od tej pory aplikacja startuje sama i praktycznie nigdy nie trzeba jej włączać ręcznie.

---

## 3. Pydroid 3 — co można zrobić

Pydroid nie ma trybu pierwszoplanowego, więc jest bardziej narażony na zamknięcie.
Pomaga:
- ustawienie baterii na **Bez ograniczeń** (punkt 1),
- **niezamykanie** Pydroida z listy ostatnich aplikacji,
- pozostawienie ekranu włączonego przy dłuższej nauce (aplikacja sama prosi o blokadę
  wygaszania, gdy przeglądarka to obsługuje),
- zamknięcie ciężkich aplikacji w tle (gry, mapy) — Android zabija procesy przy braku pamięci.

Jeśli mimo to serwer bywa zatrzymywany, przejdź na Termuksa z punktu 2.

---

## 4. Co robi sama aplikacja (od wersji 0.9.1)

Nawet gdy system uśpi serwer, **nic nie tracisz**:

- Na dole ekranu pojawia się pasek **„⏸ Aplikacja uśpiona przez system"**, a aplikacja
  **sama próbuje wznowić połączenie** co kilka sekund.
- Gdy serwer wróci (np. po otwarciu Pydroida i naciśnięciu ▶), strona **odświeża się
  automatycznie i wraca dokładnie do tego samego miejsca** — z komunikatem
  „Wznowiono — możesz uczyć się dalej".
- **Nie trzeba się logować ponownie** — sesje są zapisywane na dysku i ważne 90 dni.
- **Postęp zadania jest zapisywany na bieżąco** — odpowiedzi udzielone przed uśpieniem
  są zapamiętane.
- Dopóki uczysz się przy włączonym ekranie, aplikacja **odpytuje serwer co 25 sekund**,
  co samo w sobie ogranicza usypianie.

---

## Krótkie podsumowanie

| Chcę… | Zrób |
|---|---|
| Najprościej, ale bywa zamykane | Pydroid 3 + bateria „Bez ograniczeń" |
| Ma działać zawsze | Termux + Termux:API + `bash start.sh` |
| Ma startować samo po restarcie telefonu | Termux:Boot (punkt 2.4) |
| Nie chcę nic konfigurować | Zostaw jak jest — aplikacja sama wznowi połączenie po powrocie |
