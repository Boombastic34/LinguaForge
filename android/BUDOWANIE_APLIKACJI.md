# Prawdziwa aplikacja na Androida (APK) i droga do Sklepu Play

W folderze `android/` jest **kompletny projekt Android Studio**. Po zbudowaniu powstaje
zwykła aplikacja: ikona w menu telefonu, własne okno, **serwer w środku aplikacji**
(nie potrzebujesz Pydroida ani Termuksa), działający jako usługa pierwszoplanowa —
czyli nie wyłącza się po wyjściu z aplikacji.

> **Uczciwie:** tego projektu nie da się zbudować na telefonie. Potrzebny jest komputer
> z Android Studio; pierwsze budowanie pobiera kilka GB narzędzi i trwa 20–40 minut.
> Kolejne trwają 1–2 minuty.

---

## Jak to działa w środku

| Element | Rola |
|---|---|
| `MainActivity.kt` | pełnoekranowe okno pokazujące interfejs LinguaForge |
| `ServerService.kt` | usługa pierwszoplanowa (stałe powiadomienie) trzymająca serwer przy życiu |
| `start_server.py` | uruchamia `main.py` wewnątrz aplikacji, ustawia katalog zapisu |
| Chaquopy | wtyczka Gradle osadzająca Pythona 3.11 razem z FastAPI i uvicornem |

Dane (konta, postępy, dodane treści) trafiają do prywatnego katalogu aplikacji — nikt inny
nie ma do nich dostępu, a odinstalowanie aplikacji je usuwa (wcześniej zrób
**Ustawienia → Kopia postępów → Pobierz kopię**).

---

## KROK 1 — Zainstaluj narzędzia (jednorazowo, na komputerze)

1. Pobierz **Android Studio**: https://developer.android.com/studio (Windows, ~1 GB).
2. Zainstaluj z domyślnymi ustawieniami. Przy pierwszym uruchomieniu kreator pobierze
   **Android SDK** — zgódź się.
3. W Android Studio: **More Actions → SDK Manager → SDK Tools** → zaznacz
   **Android SDK Build-Tools**, **NDK (Side by side)** i **CMake** → Apply.

## KROK 2 — Przygotuj kod aplikacji

W folderze `android/` uruchom **`przygotuj_zrodla.bat`** (Windows) lub
`bash przygotuj_zrodla.sh` (Linux/Mac). Skrypt kopiuje aktualny `main.py`, `core/`,
`data/` i `static/` do projektu. **Rób to po każdej zmianie treści lub kodu.**

> **Ważne:** projekt ma przypiętą wersję Gradle 8.7 i wtyczek. Jeśli Android Studio
> zaproponuje ich aktualizację — **odmów**. Gdy pojawi się błąd
> `Unable to load class 'org.gradle.util.VersionNumber'`, otwórz plik
> **`NAPRAWA_BLEDOW_GRADLE.md`** w tym folderze.

## KROK 3 — Otwórz projekt

Android Studio → **Open** → wskaż folder **`android`** (nie `LinguaForge`).
Poczekaj, aż zakończy się „Gradle sync" (pasek na dole). Pierwszy raz potrwa długo —
pobierane są biblioteki i Python dla Androida.

## KROK 4 — Zbuduj plik APK

Menu **Build → Build Bundle(s) / APK(s) → Build APK(s)**.
Gotowy plik znajdziesz w:
```
android/app/build/outputs/apk/debug/app-debug.apk
```
Przenieś go na telefon (kabel, Dysk Google) i otwórz — Android zapyta o zgodę na
instalację z nieznanego źródła. Zgódź się i gotowe: **LinguaForge jest w menu telefonu**.

### Szybciej: instalacja prosto z komputera
Podłącz telefon kablem, włącz w nim **Opcje programisty → Debugowanie USB**,
a w Android Studio naciśnij zielony ▶ **Run**. Aplikacja zainstaluje się sama.

---

## Aktualizacja aplikacji po zmianach

1. `przygotuj_zrodla.bat`
2. W `app/build.gradle` podnieś `versionCode` (o 1) i `versionName`.
3. Build → Build APK(s) → zainstaluj nowy plik.

Postępy i konta zostają — są w prywatnym katalogu aplikacji, nie w pliku APK.

---

## DROGA DO SKLEPU PLAY

Aplikacja techniczne nadaje się do publikacji już teraz. Formalnie potrzebujesz:

### 1. Konto dewelopera
- https://play.google.com/console — **jednorazowa opłata 25 USD**.
- Weryfikacja tożsamości (dowód) — dla kont osobistych także adres.
- Od 2023 nowe konta osobiste muszą przed publikacją przeprowadzić
  **test zamknięty z 12 testerami przez 14 dni** (osoby, które zainstalują aplikację
  z linku testowego). To zwykle największa przeszkoda — warto zebrać znajomych.

### 2. Podpisany plik AAB (nie APK)
W Android Studio: **Build → Generate Signed Bundle / APK → Android App Bundle**.
Utwórz **keystore** i zapisz go w bezpiecznym miejscu wraz z hasłami — jego utrata
uniemożliwia aktualizowanie aplikacji na zawsze.

### 3. Wymagane materiały w konsoli
- ikona 512×512 (masz: `static/icons/icon-512.png`),
- grafika promocyjna 1024×500,
- 2–8 zrzutów ekranu z telefonu,
- krótki (80 znaków) i pełny opis,
- **polityka prywatności** pod publicznym adresem — w tej aplikacji jest łatwa:
  dane nie opuszczają telefonu, brak reklam, brak analityki,
- ankieta bezpieczeństwa danych (Data safety) — zaznaczasz „nie zbieramy danych",
- klasyfikacja treści (ankieta),
- deklaracja, że aplikacja nie jest skierowana do dzieci (albo spełnia zasady Family).

### 4. Wymogi techniczne Google
- **targetSdk** musi odpowiadać wymogom Google (obecnie 34; podnosi się co roku),
- obsługa ekranów i Androida 14+,
- brak zakazanych uprawnień — Ty używasz tylko `INTERNET`, `FOREGROUND_SERVICE`,
  `POST_NOTIFICATIONS` i `WAKE_LOCK`, co jest bezpieczne,
- **uzasadnienie usługi pierwszoplanowej** — w formularzu opisujesz, że serwer nauki
  musi działać w tle, aby postęp nie ginął (typ `dataSync`).

### 5. Rozmiar
APK z Pythonem i bibliotekami waży ok. **40–60 MB** na architekturę.
W AAB Google sam wysyła telefonowi tylko właściwą wersję.

---

## Alternatywa na przyszłość (gdybyś chciał wersję „lżejszą")

Obecna aplikacja niesie w sobie Pythona. Gdyby kiedyś zależało Ci na kilku megabajtach
i uruchamianiu bez serwera, drugą drogą jest **przepisanie logiki na JavaScript**
i zapisywanie danych w pamięci przeglądarki. To duża praca (cały silnik powtórek,
ocenianie odpowiedzi, ścieżka nauki), ale daje aplikację działającą offline bez Pythona
i publikowaną jako zwykła aplikacja webowa (TWA). Nie jest to potrzebne, aby wejść
do Sklepu Play — obecne rozwiązanie jest w pełni wystarczające.

---

## Najczęstsze problemy przy budowaniu

| Komunikat | Rozwiązanie |
|---|---|
| `NDK not configured` | SDK Manager → SDK Tools → zainstaluj **NDK (Side by side)** |
| `Could not resolve com.chaquo.python` | Sprawdź internet i wpis `maven { url "https://chaquo.com/maven" }` w `settings.gradle` |
| `Unsupported Java version` | File → Settings → Build Tools → Gradle → **Gradle JDK: 17** |
| `Unable to load class 'org.gradle.util.VersionNumber'` | Za nowy Gradle — patrz `NAPRAWA_BLEDOW_GRADLE.md` (skasuj `C:\Users\TY\.gradle\caches` i otwórz projekt ponownie) |
| Aplikacja wstaje, ale biały ekran | Poczekaj 10–20 s przy pierwszym starcie (kopiowanie materiałów); potem sprawdź Logcat, filtr `python` |
| `pip install` nie znajduje pakietu | Chaquopy wymaga wersji z gotowymi paczkami — trzymaj się wersji podanych w `app/build.gradle` |
| `python.exe finished with non-zero exit value 1` | Nieudana instalacja bibliotek Pythona — patrz `NAPRAWA_BLEDU_PYTHON.md` |
| Menu „Build APK(s)" nie istnieje | W nowszych wersjach nazywa się **Generate APKs** (podwójny Shift → wpisz „Generate APKs") |
