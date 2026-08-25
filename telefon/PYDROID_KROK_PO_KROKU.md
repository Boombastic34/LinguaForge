# LinguaForge na telefonie przez Pydroid 3 — instrukcja krok po kroku

Po tej instalacji aplikacja działa **w całości na telefonie**. Komputer nie jest potrzebny,
internet też nie (poza jednorazowym pobraniem dwóch bibliotek w kroku 3).

Czas: około 15 minut. Miejsce na telefonie: około 400 MB.

---

## KROK 1 — Zainstaluj Pydroid 3

1. Otwórz **Sklep Play**.
2. Wyszukaj: **Pydroid 3 — IDE for Python 3**.
3. Zainstaluj (wersja darmowa wystarczy — wyświetla reklamy, ale działa bez ograniczeń).
4. Uruchom aplikację. Przy pierwszym starcie sama doinstaluje Pythona — poczekaj,
   aż zniknie napis o instalacji.
5. Gdy zapyta o **dostęp do plików / zdjęć i multimediów** — zezwól.

---

## KROK 2 — Przenieś aplikację na telefon

Potrzebujesz folderu `LinguaForge` w pamięci telefonu. Wybierz jeden ze sposobów:

**Sposób z kablem (najszybszy):**
1. Podłącz telefon do komputera kablem USB.
2. Na telefonie wybierz tryb **Przesyłanie plików** (nie „tylko ładowanie").
3. Na komputerze otwórz telefon w Eksploratorze plików.
4. Skopiuj CAŁY folder `LinguaForge` do pamięci wewnętrznej telefonu, do katalogu **Documents**.
   Docelowo ma być: `Pamięć wewnętrzna / Documents / LinguaForge`

**Sposób bez kabla:**
1. Wyślij sobie plik ZIP z aplikacją (Dysk Google, e-mail, WhatsApp do siebie).
2. Pobierz go na telefonie.
3. Otwórz aplikację **Pliki** (albo zainstaluj darmowy **ZArchiver**), znajdź plik ZIP.
4. Rozpakuj go do katalogu **Documents**.

**Sprawdź po rozpakowaniu:** w folderze `LinguaForge` musi znajdować się plik **`main.py`**
oraz katalogi `core`, `data`, `static`. Jeśli po rozpakowaniu widzisz folder w folderze
(`LinguaForge/LinguaForge/main.py`) — przenieś wewnętrzny folder poziom wyżej.

---

## KROK 3 — Doinstaluj dwie biblioteki (jednorazowo, wymaga internetu)

1. Otwórz **Pydroid 3**.
2. Dotknij ikony **☰** (trzy kreski) w lewym górnym rogu.
3. Wybierz **Pip**.
4. Przejdź na zakładkę **SEARCH LIBRARIES** (albo „Quick install").
5. W pole wpisz: `fastapi` → dotknij **INSTALL**.
   Poczekaj, aż na dole pojawi się `Successfully installed…` (może potrwać 1–3 minuty;
   razem z fastapi doinstalują się dodatkowe składniki — to normalne).
6. Wyczyść pole, wpisz: `uvicorn` → **INSTALL**. Znowu poczekaj na `Successfully installed`.
7. (Opcjonalnie, tylko dla katalogu PDF administratora) wpisz: `reportlab` → **INSTALL**.
   Jeśli się nie uda — nic nie szkodzi, katalog zostanie wtedy wygenerowany jako plik HTML.

> Gdyby instalacja zgłosiła błąd: sprawdź połączenie z internetem i spróbuj ponownie.
> W Pydroid warto mieć włączone **Use prebuilt libraries repository** (☰ → Settings) —
> dzięki temu biblioteki pobierają się gotowe, bez kompilowania.

---

## KROK 4 — Otwórz plik aplikacji

1. W Pydroid 3 dotknij **☰** → **Open**.
2. Przejdź do: `Documents` → `LinguaForge`.
3. Dotknij pliku **`main.py`** (kod pojawi się na ekranie — nic w nim nie zmieniaj).

---

## KROK 5 — Uruchom

1. Dotknij żółtego przycisku **▶** (prawy dolny róg).
2. Na dole otworzy się okno terminala. Po chwili zobaczysz ramkę:

```
   LinguaForge v0.7.2
   Tryb telefonu — aplikacja działa samodzielnie na tym urządzeniu.
   Otwórz w przeglądarce:  http://127.0.0.1:8177
   Nie zamykaj tego okna w trakcie nauki.
```

3. **Nie zamykaj Pydroida** — zminimalizuj go przyciskiem HOME (nie zamykaj przesunięciem
   z listy ostatnich aplikacji, bo to zatrzyma serwer).

---

## KROK 6 — Otwórz aplikację w przeglądarce

1. Uruchom **Chrome** (albo dowolną przeglądarkę).
2. W pasku adresu wpisz dokładnie: **`127.0.0.1:8177`** i zatwierdź.
3. Pojawi się ekran logowania LinguaForge. Załóż konto lub zaloguj się.

---

## KROK 7 — Ikona na ekranie głównym (żeby wyglądało jak aplikacja)

1. Mając otwartą aplikację w Chrome, dotknij **⋮** (trzy kropki, prawy górny róg).
2. Wybierz **Dodaj do ekranu głównego** → **Dodaj**.
3. Na pulpicie telefonu pojawi się ikona LinguaForge. Otwarta z niej aplikacja działa
   pełnoekranowo, bez paska przeglądarki.

> Pamiętaj: ikona otwiera tylko ekran aplikacji. **Silnik musi być uruchomiony w Pydroid 3** —
> jeśli po dotknięciu ikony widzisz błąd połączenia, wróć do Pydroida i naciśnij ▶.

---

## Codzienne używanie

1. Otwórz **Pydroid 3** → naciśnij **▶** (plik `main.py` zostaje zapamiętany).
2. Przełącz się na ikonę LinguaForge na ekranie głównym.
3. Po nauce: wróć do Pydroida i naciśnij **■ (stop)**, aby zwolnić pamięć.

---

## Ustawienia, które warto włączyć

**Żeby Android nie zabijał aplikacji w tle:**
Ustawienia telefonu → Aplikacje → **Pydroid 3** → Bateria → wybierz **Bez ograniczeń**
(nazwa różni się zależnie od producenta: „Nieograniczone", „Nie optymalizuj").

**Żeby lektor mówił po polsku:**
Ustawienia telefonu → Ułatwienia dostępu → **Zamiana tekstu na mowę** → Silnik Google →
Instalacja danych głosowych → **Polski**. Bez tego polskie zdania czyta głos angielski.

**Dźwięk:** przy pierwszym odtworzeniu w sesji dotknij przycisku ▶ Odtwórz — telefony
blokują dźwięk, dopóki użytkownik czegoś nie dotknie. To normalne zachowanie Androida.

---

## Przeniesienie postępów z komputera

1. **Na komputerze:** Pulpit → Ustawienia → Kopia postępów → **⬇ Pobierz kopię postępów**.
   Powstanie plik `LinguaForge_postepy_TWOJELOGIN_data.json`.
2. Prześlij go na telefon (Dysk Google, e-mail, kabel).
3. **Na telefonie:** załóż konto o **tej samej nazwie** co na komputerze, zaloguj się,
   wejdź w Ustawienia → Kopia postępów → **⬆ Wgraj kopię** → wskaż pobrany plik.
4. Wrócą: poziom, XP, wszystkie fiszki z terminami powtórek, ukończone ogniwa Ścieżki,
   zaliczone rozmowy, przeczytane teksty i historia.

W drugą stronę działa tak samo. Hasło zawsze zostaje to z urządzenia, na którym wgrywasz.

---

## Gdy coś nie działa

| Komunikat / objaw | Przyczyna i rozwiązanie |
|---|---|
| `ModuleNotFoundError: No module named 'core'` | Występował w wersjach starszych niż 0.7.2 — Pydroid uruchamia plik przez własny skrypt i Python nie znajdował katalogu aplikacji. Rozwiązanie: użyj paczki 0.7.2 lub nowszej (aplikacja sama odnajduje swój folder). |
| `ModuleNotFoundError: No module named 'fastapi'` | Biblioteka się nie zainstalowała. Wróć do kroku 3 i zainstaluj `fastapi` ponownie. |
| `ModuleNotFoundError: No module named 'uvicorn'` | To samo dla `uvicorn`. |
| Chrome: „Nie można połączyć się ze stroną" | Serwer nie działa — wróć do Pydroida i naciśnij ▶. Sprawdź też, czy adres to dokładnie `127.0.0.1:8177`. |
| `[Errno 98] Address already in use` | Aplikacja już działa. Wystarczy przejść do przeglądarki. Ewentualnie naciśnij ■ i ▶ ponownie. |
| `PermissionError` przy zakładaniu konta | Android blokuje zapis w tym katalogu. Przenieś folder `LinguaForge` do katalogu domowego Pydroida: w oknie **Open** jest skrót do folderu aplikacji — wklej tam folder i otwórz `main.py` z nowej lokalizacji. |
| Serwer zatrzymuje się po chwili | Android uśpił aplikację. Ustaw baterię Pydroida na **Bez ograniczeń** (patrz wyżej) i nie usuwaj Pydroida z listy ostatnich aplikacji. |
| Wersja w rogu inna niż w paczce | Odśwież stronę: przytrzymaj przycisk odświeżania w Chrome → **Wymuś odświeżenie**. |
| Brak dźwięku | Dotknij ▶ Odtwórz (pierwszy dźwięk wymaga dotknięcia) i sprawdź, czy telefon nie jest wyciszony. |

---

## Czego ta wersja NIE potrzebuje

- Nie potrzebuje komputera.
- Nie potrzebuje internetu do nauki (tylko raz, przy instalacji bibliotek w kroku 3).
- Nie potrzebuje konta w żadnej usłudze — wszystkie dane zostają na Twoim telefonie,
  w folderze `LinguaForge/accounts`.
