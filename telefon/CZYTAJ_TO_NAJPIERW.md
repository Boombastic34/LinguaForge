# LinguaForge na telefonie — bez komputera

Aplikacja działa wtedy **w całości na telefonie**: własne konto, własne postępy,
bez potrzeby włączania komputera i bez internetu (po instalacji).

Są dwie drogi. **Droga A (Pydroid 3)** jest łatwiejsza, **droga B (Termux)** pewniejsza.

---

## DROGA A — Pydroid 3 (najprostsza, Android)

**Pełna instrukcja krok po kroku ze zrzutami kolejnych ekranów i tabelą problemów:
plik `PYDROID_KROK_PO_KROKU.md` w tym folderze.** Poniżej wersja skrócona.

1. Zainstaluj ze Sklepu Play aplikację **Pydroid 3 — IDE for Python**.
2. Skopiuj folder `LinguaForge` do pamięci telefonu (np. przez kabel USB albo
   wysyłając sobie plik ZIP i rozpakowując go menedżerem plików).
3. Otwórz Pydroid 3 → menu ☰ → **Pip** → wpisz `fastapi` → *Install*.
   Powtórz dla `uvicorn`. (Pydroid ma gotowe paczki, nic się nie kompiluje.)
4. Menu ☰ → **Open** → wskaż plik `main.py` z folderu LinguaForge.
5. Naciśnij żółty przycisk ▶ (uruchom).
6. Otwórz przeglądarkę w telefonie i wejdź na: **http://127.0.0.1:8177**

Aby wyglądało jak aplikacja: w Chrome menu ⋮ → *Dodaj do ekranu głównego*.

---

## DROGA B — Termux (pełna kontrola)

1. Zainstaluj **Termux** z **F-Droid** (wersja ze Sklepu Play jest przestarzała):
   https://f-droid.org/packages/com.termux/
2. Skopiuj folder `LinguaForge` do pamięci telefonu, np. do `Pobrane`.
3. Otwórz Termux i wpisz kolejno:
   ```
   termux-setup-storage
   cp -r /sdcard/Download/LinguaForge ~/
   cd ~/LinguaForge/telefon
   bash instaluj.sh
   ```
   Instalacja trwa kilka–kilkanaście minut (jednorazowo).
4. Uruchamianie aplikacji — za każdym razem:
   ```
   cd ~/LinguaForge/telefon
   bash start.sh
   ```
5. Nie zamykaj Termuksa, przełącz się na przeglądarkę i wejdź na
   **http://127.0.0.1:8177**

### Skrót jednym dotknięciem (opcjonalnie)
Zainstaluj z F-Droid **Termux:Widget**, potem:
```
mkdir -p ~/.shortcuts
ln -s ~/LinguaForge/telefon/start.sh ~/.shortcuts/LinguaForge
```
Dodaj widget Termux na ekran główny — jedno dotknięcie uruchamia aplikację.

---

## Przeniesienie postępów z komputera na telefon

1. Na komputerze: **Pulpit → Ustawienia → Kopia postępów → Pobierz kopię**
   (powstanie plik `LinguaForge_postepy_....json`).
2. Prześlij plik na telefon (mail, chmura, kabel).
3. Na telefonie załóż konto o **tej samej nazwie**, zaloguj się i wybierz
   **Ustawienia → Kopia postępów → Wgraj kopię**.

Postępy, fiszki, powtórki i historia zostaną odtworzone. Hasło pozostaje to
z urządzenia, na którym wgrywasz. W drugą stronę działa tak samo.

---

## Uwagi

- Materiały (słówka, ćwiczenia) są w folderze `data` — kopiują się razem z aplikacją.
- Aktualizacja: podmieniasz folder aplikacji, ale **zostaw folder `accounts`**,
  bo w nim są Twoje postępy.
- Lektor korzysta z syntezatora mowy telefonu. Android: Ustawienia → Ułatwienia dostępu →
  Zamiana tekstu na mowę (warto dodać język polski).
- Katalog PDF dla administratora może wymagać biblioteki `reportlab`; jeśli się nie
  zainstaluje, aplikacja odda katalog w formacie HTML — treść jest identyczna.
