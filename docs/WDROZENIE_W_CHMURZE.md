# LinguaForge w chmurze — dostęp z iPhone'a i Androida przez link

Ta sama aplikacja, uruchomiona na serwerze zamiast na telefonie. Testerzy dostają
jeden adres, otwierają w przeglądarce i mogą dodać ikonę na ekran główny.
Działa identycznie na iPhonie i Androidzie.

## Co się zmienia względem wersji telefonowej

| | APK (Android) | Chmura (iPhone + Android) |
|---|---|---|
| Instalacja u testera | Firebase App Tester + APK | otwarcie linku |
| Aktualizacja | budujesz APK, wgrywasz, oni instalują | wgrywasz kod — gotowe u wszystkich |
| Postępy | osobno na każdym telefonie | wspólny serwer, widzisz wszystkich |
| Internet | niepotrzebny | wymagany |
| iPhone | ❌ | ✅ |

## Przygotowanie kodu (już zrobione)

- `PORT` i host czytane ze zmiennych środowiskowych (hosting sam przydziela port)
- `LF_ADMIN_PASSWORD` — hasło administratora ze zmiennej (**koniecznie ustaw własne!**)
- `LF_HOME` — katalog danych (konta, postępy) do podpięcia trwałego dysku
- `Procfile` i `runtime.txt` — pliki, których oczekuje hosting

## Wdrożenie krok po kroku (Railway — darmowy start)

1. Załóż konto na **railway.app** (logowanie przez GitHub).
2. Wrzuć projekt na GitHub jako **prywatne** repozytorium.
3. Railway → **New Project** → **Deploy from GitHub repo** → wskaż repozytorium.
4. Zakładka **Variables** → dodaj:
   - `LF_ADMIN_PASSWORD` = własne, mocne hasło
   - `LF_HOME` = `/data`
5. Zakładka **Volumes** → **New Volume** → punkt montowania: `/data`
   ⚠️ **Bez tego kroku konta i postępy skasują się przy każdej aktualizacji.**
6. Zakładka **Settings** → **Generate Domain** → dostajesz adres typu
   `linguaforge-production.up.railway.app`
7. Wyślij ten adres testerom.

## Co robią testerzy

1. Otwierają link w przeglądarce telefonu.
2. Zakładają konto (login + hasło).
3. **iPhone (Safari):** przycisk udostępniania → *Do ekranu początkowego*
   **Android (Chrome):** ⋮ → *Dodaj do ekranu głównego*

Aplikacja otwiera się wtedy pełnoekranowo, z własną ikoną — wygląda jak zwykła apka.

## Aktualizacja aplikacji

Wgrywasz zmiany na GitHub → Railway sam przebudowuje i uruchamia nową wersję.
Testerzy odświeżają stronę i mają nowe funkcje. Bez instalowania czegokolwiek.

## Ograniczenia, o których trzeba wiedzieć

- **Lektor na iPhonie** działa przez mechanizm przeglądarki (Safari go obsługuje),
  ale głosy zależą od ustawień telefonu. Most natywny z wersji APK działa tylko
  w aplikacji na Androida.
- **Bez internetu aplikacja nie działa.** Wersja APK zostaje jako wariant offline.
- **Darmowy plan** hostingu zwykle usypia serwer przy braku ruchu — pierwsze wejście
  po przerwie może potrwać kilkanaście sekund.
- **Hasła** są hashowane z solą (SHA-256). Dla trzech znajomych to wystarczy;
  przy szerszym udostępnieniu warto przejść na bcrypt i włączyć HTTPS
  (Railway daje HTTPS automatycznie).
