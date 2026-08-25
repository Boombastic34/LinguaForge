# LinguaForge na Androida — instrukcja od zera, krok po kroku

Ten dokument zakłada, że nie masz nic zainstalowane. Każdy krok mówi wprost:
**na jakim urządzeniu** (💻 komputer / 📱 telefon), **w jakim programie**,
**w którym miejscu** i **co dokładnie zrobić**.

Całość zajmuje z pierwszym budowaniem około **1–1,5 godziny** (większość to czekanie
na pobieranie, nie klikanie). Kolejne aktualizacje — 5 minut.

---

# CZĘŚĆ A — Instalacja narzędzi (💻 komputer, raz)

## A1. Sprawdź miejsce na dysku
💻 Potrzebujesz **co najmniej 10 GB** wolnego miejsca na dysku C.
- Otwórz **Eksplorator plików** → kliknij **Ten komputer** → sprawdź ile wolnego miejsca
  jest przy dysku **(C:)**.

## A2. Pobierz Android Studio
💻 Przeglądarka internetowa (Chrome/Edge):
1. Wejdź na adres: **https://developer.android.com/studio**
2. Kliknij duży zielony przycisk **„Download Android Studio"**.
3. Zaznacz zgodę na warunki licencji (checkbox) → **Download Android Studio for Windows**.
4. Poczekaj, aż pobierze się plik (ok. 1 GB) — zobaczysz go na pasku pobierania
   przeglądarki albo w folderze **Pobrane**.

## A3. Zainstaluj Android Studio
💻 Folder **Pobrane** (albo pasek pobierania w przeglądarce):
1. Kliknij dwa razy plik **android-studio-*.exe**.
2. Jeśli Windows zapyta „Czy zezwolić tej aplikacji na wprowadzanie zmian" → **Tak**.
3. W oknie instalatora klikaj kolejno: **Next → Next → Next → Install**.
4. Poczekaj (kilka minut), na końcu **Next → Finish**.
5. Android Studio uruchomi się samo.

## A4. Kreator pierwszego uruchomienia
💻 Program **Android Studio** (właśnie otwarty):
1. Jeśli pojawi się okno „Import Android Studio Settings" → zaznacz
   **Do not import settings** → **OK**.
2. Ekran powitalny „Welcome" → kliknij **Next**.
3. Ekran „Install Type" → zaznacz **Standard** → **Next**.
4. Ekran z motywem kolorystycznym → wybierz dowolny → **Next**.
5. Ekran „Verify Settings" → **Next**.
6. Ekran licencji „License Agreement" → po lewej stronie zaznacz **każdą** pozycję
   na liście, przy każdej klikając **Accept** → gdy wszystkie mają zielony znaczek →
   **Finish**.
7. Zacznie się pobieranie SDK (pasek postępu, kilka GB) — **czekaj, nie zamykaj**
   (5–15 minut, zależnie od internetu).
8. Na końcu → **Finish**. Otworzy się okno „Welcome to Android Studio" (jeszcze puste).

## A5. Doinstaluj brakujące składniki (NDK i CMake)
💻 Okno **Welcome to Android Studio** (to, które zostało otwarte):
1. Kliknij **More Actions** (może być też ikona trzech kropek albo koła zębatego)
   → **SDK Manager**.
   - Jeśli nie widzisz „More Actions": kliknij ikonę **☰** w lewym górnym rogu okna.
2. W nowym oknie u góry kliknij zakładkę **SDK Tools** (obok „SDK Platforms").
3. Zaznacz checkboxy przy:
   - **NDK (Side by side)**
   - **CMake**
   - **Android SDK Build-Tools**
   - **Android SDK Command-line Tools (latest)**
4. Kliknij **Apply** (prawy dolny róg okna).
5. Pojawi się lista do pobrania → **OK**.
6. Zaakceptuj licencje, jeśli wyskoczą → **Next** → czekaj (kolejne kilka GB, 5–15 min).
7. Na końcu → **Finish** → **OK**, żeby zamknąć SDK Manager.

**Koniec części A.** Android Studio jest gotowe. Ten etap robisz **tylko raz**.

---

# CZĘŚĆ B — Przygotowanie projektu LinguaForge (💻 komputer)

## B1. Pobierz i rozpakuj paczkę aplikacji
💻 Przeglądarka → miejsce, gdzie masz plik **LinguaForge_v1.0.2.zip**
(np. folder **Pobrane**):
1. Kliknij prawym przyciskiem myszy na plik ZIP.
2. Wybierz **Wyodrębnij wszystko...** (albo „Extract All...").
3. W oknie kliknij **Wyodrębnij** (możesz zmienić miejsce docelowe, np. na Pulpit —
   zapamiętaj tę ścieżkę, będzie potrzebna).
4. Powstanie folder, np.: `C:\Users\TwojaNazwa\Downloads\LinguaForge_v1.0.2`
5. **Otwórz ten folder** — w środku musi być podfolder **`LinguaForge`**
   (nie mylić z folderem ZIP-a). Wejdź do niego.

Sprawdź, czy widzisz w nim m.in.: `main.py`, folder `core`, folder `data`,
folder `static`, folder **`android`**. Jeśli tak — jesteś we właściwym miejscu.

## B2. Skopiuj kod aplikacji do projektu Androida
💻 Ten sam folder **`LinguaForge`**, Eksplorator plików:
1. Wejdź do podfolderu **`android`** (czyli: `...\LinguaForge\android`).
2. Znajdź plik **`przygotuj_zrodla.bat`**.
3. Kliknij go **dwukrotnie**.
4. Otworzy się czarne okno (Wiersz polecenia). Zobaczysz komunikaty kopiowania,
   na końcu: **„Gotowe: ..."**
5. Naciśnij dowolny klawisz, żeby zamknąć okno (jest tam napis „Naciśnij dowolny klawisz...").

> ⚠️ **Ten krok powtarzasz za każdym razem**, gdy pobierzesz nowszą wersję aplikacji
> albo sam coś zmienisz w plikach — inaczej zbudujesz starą wersję.

## B3. Otwórz projekt w Android Studio
💻 Program **Android Studio**:
1. Jeśli jest już otwarty jakiś projekt: menu **File** (lewy górny róg) → **Close Project**.
   Wrócisz do okna powitalnego.
2. W oknie powitalnym kliknij **Open** (ikona folderu, środek okna).
3. W oknie wyboru folderu przejdź do: `...\LinguaForge\android`
   (czyli **ten sam folder `android`**, w którym uruchamiałeś `przygotuj_zrodla.bat`).
4. Zaznacz folder **`android`** (**kliknij go raz, nie wchodź do środka**).
5. Kliknij **OK**.
6. Jeśli wyskoczy okno **„Trust Project?"** → kliknij **Trust Project**.

## B4. Poczekaj na synchronizację (Gradle Sync)
💻 Android Studio, dolny pasek okna:
1. Zobaczysz pasek postępu i napisy typu „Gradle Sync in progress...".
2. **To potrwa 10–30 minut za pierwszym razem** — pobierane są biblioteki i Python
   dla Androida. Nie zamykaj programu, możesz robić coś innego na komputerze.
3. Mogą pojawić się żółte paski z ostrzeżeniami (np. o Windows Defender albo o JDK) —
   **na razie je zignoruj**, przejdź do kroku B5.
4. Koniec synchronizacji poznasz po napisie na dole: **„Gradle sync finished"** albo
   gdy pasek postępu zniknie, a po lewej stronie pojawi się drzewo plików projektu
   (foldery: `app`, `manifests`, `kotlin+java`, `res`).

### Jeśli wyskoczy żółty pasek o JDK / JAVA_HOME
To tylko ostrzeżenie, nie błąd — możesz kontynuować. Dla porządku:
1. Menu **File** → **Settings**.
2. Po lewej: **Build, Execution, Deployment** → **Build Tools** → **Gradle**.
3. Pole **Gradle JDK** → z listy wybierz pozycję zawierającą **„21"** albo opisaną
   jako domyślna dla Android Studio.
4. **OK**.

### Jeśli wyskoczy pasek o Microsoft Defender
1. Kliknij przycisk **„Exclude folders"** w tym pasku.
2. Jeśli Windows zapyta o uprawnienia administratora → **Tak**.
(To tylko przyspiesza budowanie — możesz też kliknąć „Ignore for this project" i pominąć.)

### Jeśli synchronizacja zakończy się błędem
Patrz sekcja **„ROZWIĄZYWANIE PROBLEMÓW"** na końcu tego dokumentu.

**Koniec części B**, gdy widzisz drzewo plików po lewej i brak paska postępu na dole.

---

# CZĘŚĆ C — Budowanie pliku aplikacji (💻 komputer, Android Studio)

## C1. Uruchom budowanie
💻 Android Studio, z otwartym projektem `android`:
1. Naciśnij klawisz **Shift dwa razy szybko** (Shift, Shift) — otworzy się okienko
   wyszukiwania poleceń na środku ekranu.
2. Wpisz: **`Generate APKs`**
   (w niektórych wersjach nazywa się „Build APK(s)" — wpisz `apk` i zobacz, co się pojawi).
3. Na liście wyników kliknij pozycję **„Generate APKs"** (albo „Build APK(s)").
4. Naciśnij **Enter**.

## C2. Czekaj na zakończenie
💻 Android Studio, dolny pasek:
1. Zobaczysz „Executing tasks..." i pasek postępu.
2. **Pierwsze budowanie: 10–30 minut.** Pobierane są dodatkowe biblioteki Pythona.
3. **Nie zamykaj programu** w trakcie.
4. Zakończenie poznasz po zielonym dymku w prawym dolnym rogu ekranu:
   **„APK(s) generated successfully"** z niebieskim odnośnikiem **„locate"**.

### Jeśli budowanie zakończy się błędem (czerwony pasek „Build: failed")
Patrz sekcja **„ROZWIĄZYWANIE PROBLEMÓW"** na końcu.

## C3. Znajdź gotowy plik
💻 Dwa sposoby:
- **Łatwiejszy:** kliknij niebieski odnośnik **„locate"** w dymku z kroku C2 —
  otworzy się Eksplorator z zaznaczonym plikiem.
- **Ręcznie:** w Eksploratorze plików wejdź do:
  ```
  ...\LinguaForge\android\app\build\outputs\apk\debug\
  ```
  Zobaczysz plik **`app-debug.apk`**.

**Koniec części C.** Masz gotowy plik instalacyjny.

---

# CZĘŚĆ D — Instalacja na telefonie (📱 telefon + 💻 komputer)

Wybierz **jeden** z dwóch sposobów.

## SPOSÓB D1 — kablem, najszybszy (zalecany)

### D1.1 Włącz opcje programisty w telefonie
📱 Telefon, aplikacja **Ustawienia**:
1. Wejdź w **Ustawienia** → przewiń na sam dół → **Informacje o telefonie**
   (na niektórych telefonach: **O telefonie**).
2. Znajdź pozycję **Numer kompilacji** (albo „Numer kompilacji oprogramowania").
3. Dotknij ją **7 razy szybko pod rząd**. Po kilku dotknięciach pojawi się
   odliczanie „Jeszcze X dotknięć do trybu programisty".
4. Na końcu zobaczysz komunikat: **„Jesteś teraz programistą!"**
   (telefon może poprosić o PIN/hasło — podaj je).

### D1.2 Włącz debugowanie USB
📱 Telefon, aplikacja **Ustawienia**:
1. Wróć do głównego ekranu Ustawień → znajdź nową pozycję
   **Opcje programisty** (zwykle blisko „System" albo „Informacje o telefonie").
2. Wejdź w nią → znajdź przełącznik **Debugowanie USB** → włącz go (przesuń w prawo).
3. Jeśli wyskoczy ostrzeżenie → **OK**.

### D1.3 Podłącz telefon do komputera
📱 + 💻:
1. Podłącz telefon do komputera **oryginalnym kablem USB** (nie tylko do ładowania —
   kabel musi przesyłać dane).
2. 📱 Na telefonie może pojawić się powiadomienie „Ładowanie tego urządzenia przez USB" →
   dotknij je → wybierz **Przesyłanie plików** (nie „Tylko ładowanie").
3. 📱 Wyskoczy okno **„Zezwolić na debugowanie USB?"** z kodem odcisku palca komputera →
   zaznacz **„Zawsze zezwalaj z tego komputera"** → **Zezwól/OK**.

### D1.4 Zainstaluj z Android Studio
💻 Android Studio (projekt `android` nadal otwarty):
1. Spójrz na górny pasek narzędzi — obok przycisku ▶ powinna pojawić się nazwa
   Twojego telefonu (zamiast „No devices").
   - Jeśli pokazuje **„No devices"**: poczekaj kilka sekund, telefon musi zostać wykryty.
   - Jeśli nadal nic: sprawdź krok D1.3, spróbuj innego portu USB.
2. Kliknij zielony trójkąt **▶ Run 'app'** (górny pasek, obok nazwy urządzenia).
3. Android Studio samo zainstaluje i uruchomi aplikację na telefonie — zobaczysz to
   na ekranie telefonu.

**Gotowe — aplikacja jest zainstalowana i uruchomiona.**

---

## SPOSÓB D2 — bez kabla, przez plik

### D2.1 Prześlij plik APK na telefon
💻 Wybierz jeden sposób:
- **Dysk Google:** wejdź na drive.google.com → **Nowy** → **Prześlij plik** →
  wskaż `app-debug.apk` z folderu opisanego w kroku C3.
- **E-mail do siebie:** wyślij maila do własnej skrzynki z załącznikiem `app-debug.apk`.
- **Kabel + zwykłe kopiowanie:** podłącz telefon (tryb „Przesyłanie plików" jak w D1.3),
  w Eksploratorze skopiuj `app-debug.apk` do folderu **Pobrane** telefonu.

### D2.2 Pobierz plik na telefonie
📱 Telefon:
1. Otwórz aplikację, przez którą wysłałeś plik (Dysk / Gmail), albo folder **Pliki**
   → **Pobrane**, jeśli kopiowałeś kablem.
2. Dotknij plik **app-debug.apk**, aby go pobrać/otworzyć.

### D2.3 Zainstaluj
📱 Telefon:
1. Po dotknięciu pliku system zapyta o zgodę na **instalację z tego źródła**
   (Chrome / Pliki / Gmail — zależnie skąd otwierasz) → dotknij **Ustawienia**
   w tym komunikacie.
2. Włącz przełącznik **„Zezwól z tego źródła"** → wróć (strzałka wstecz).
3. Teraz dotknij **Zainstaluj**.
4. Poczekaj kilka sekund → **Otwórz**.

**Koniec części D.** Aplikacja LinguaForge jest zainstalowana na telefonie.

---

# CZĘŚĆ E — Pierwsze uruchomienie (📱 telefon)

1. Znajdź ikonę **LinguaForge** (pomarańczowa, litera A) na ekranie głównym albo
   w szufladzie aplikacji.
2. Dotknij ją.
3. Jeśli system zapyta o **zgodę na powiadomienia** → dotknij **Zezwól**
   (to dzięki temu serwer działa w tle).
4. Zobaczysz pomarańczowy ekran **„LinguaForge — Uruchamiam..."** — poczekaj
   10–20 sekund (pierwsze uruchomienie kopiuje materiały).
5. Pojawi się ekran logowania — załóż konto (login + hasło) albo zaloguj się.

### Jeśli masz już postępy na komputerze i chcesz je przenieść
📱 W aplikacji: **Więcej → Ustawienia → Kopia postępów → Wgraj kopię** →
wskaż plik pobrany wcześniej **na komputerze** (💻: Pulpit → Ustawienia →
Kopia postępów → Pobierz kopię → prześlij plik na telefon jak w kroku D2.1).

### Zalecane ustawienie baterii (żeby aplikacja nie gasła w tle)
📱 Telefon, **Ustawienia**:
1. **Aplikacje** → znajdź **LinguaForge** → dotknij.
2. **Bateria** (albo „Użycie baterii") → wybierz **Bez ograniczeń**
   (na niektórych telefonach: „Nieograniczone").

---

# AKTUALIZACJA PO ZMIANACH (kolejne razy)

💻 Za każdym razem, gdy masz nowszą wersję kodu:
1. `android\przygotuj_zrodla.bat` — dwuklik (jak w kroku B2).
2. Android Studio, plik **`android\app\build.gradle`**: znajdź linię
   `versionCode 1` → zmień na `versionCode 2` (przy kolejnej aktualizacji na 3, itd.).
3. Podwójny **Shift** → **Generate APKs** (jak w części C).
4. Zainstaluj nowy plik jak w części D.

Konta i postępy **zostają** — są zapisane w pamięci telefonu, nie w pliku APK.

---

# ROZWIĄZYWANIE PROBLEMÓW

## `Unable to load class 'org.gradle.util.VersionNumber'`
💻 Android Studio używa za nowej wersji Gradle.
1. Zamknij Android Studio całkowicie.
2. 💻 Eksplorator plików → pasek adresu wpisz: `%USERPROFILE%\.gradle` → Enter.
3. Skasuj cały ten folder (Shift+Delete).
4. Otwórz projekt ponownie (część B3) i poczekaj na sync — pobierze właściwą wersję.

## `Process 'command ...python.exe' finished with non-zero exit value 1`
💻 Nieudana instalacja bibliotek Pythona (masz już poprawiony zestaw w v1.0.2+).
1. Eksplorator plików → wejdź do: `...\LinguaForge\android\app\build\python`
2. Skasuj folder **`python`** w całości.
3. W Android Studio: menu **Build** (albo Shift+Shift → wpisz „Clean Project") →
   **Clean Project**.
4. Buduj ponownie (część C).

## `NDK not configured` / `No version of NDK matched`
💻 Wróć do kroku **A5** i upewnij się, że **NDK (Side by side)** i **CMake** są zainstalowane.

## `SDK location not found`
💻 Android Studio:
1. Menu **File** → **Project Structure**.
2. Po lewej: **SDK Location**.
3. Sprawdź, czy pole **Android SDK Location** wskazuje istniejący folder
   (zwykle `C:\Users\TwojaNazwa\AppData\Local\Android\Sdk`).
4. Jeśli puste — kliknij **...** i wskaż ten folder → **OK**.

## Menu „Build APK(s)" nie istnieje
💻 W nowszych wersjach programu nazywa się **„Generate APKs"** — użyj kroku C1
(podwójny Shift + wpisanie nazwy) zamiast szukać w menu.

## Telefon nie pojawia się w Android Studio (sposób D1)
📱 + 💻:
1. Sprawdź inny kabel USB (niektóre ładują, ale nie przesyłają danych).
2. 📱 Powiadomienie USB → upewnij się, że wybrano **Przesyłanie plików**, nie „Ładowanie".
3. 📱 Ustawienia → Opcje programisty → sprawdź, czy **Debugowanie USB** jest nadal włączone.
4. Odłącz i podłącz kabel ponownie, poczekaj 10 sekund.

## Aplikacja na telefonie pokazuje biały ekran dłużej niż minutę
📱 + 💻:
1. Zamknij aplikację całkowicie (przesuń z listy ostatnich aplikacji) i otwórz ponownie.
2. Jeśli nie pomoże: 💻 podłącz telefon, w Android Studio otwórz zakładkę
   **Logcat** (dolny pasek) → w polu filtra wpisz `python` → spróbuj otworzyć
   aplikację na telefonie jeszcze raz i przeczytaj, co pojawia się na czerwono.
   Wklej mi tę treść.

## Nie wiem, na czym stanęło budowanie
💻 Android Studio, dolny pasek → kliknij zakładkę **Build** (ikona młotka po lewej
krawędzi okna) → rozwinie się drzewo etapów budowania → czerwony znak ✕ pokazuje,
który etap zawiódł → kliknij go, żeby zobaczyć pełny komunikat.
