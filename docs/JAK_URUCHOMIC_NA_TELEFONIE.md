# Jak uruchomić LinguaForge na telefonie

## Sposób 1 (zalecany): komputer + telefon w tej samej sieci Wi-Fi

1. Na komputerze uruchom **`start_telefon.bat`** (zamiast zwykłego `start.bat`).
2. W czarnym oknie zobaczysz dwa adresy, np.:
   ```
   Na tym komputerze:  http://127.0.0.1:8177
   Na telefonie:       http://192.168.1.15:8177
   ```
3. Przy pierwszym uruchomieniu Windows zapyta o dostęp do sieci —
   zaznacz **„Sieci prywatne"** i kliknij **„Zezwól na dostęp"**.
4. W telefonie otwórz przeglądarkę i wpisz adres z linii **„Na telefonie"**
   (razem z `:8177`).
5. Zaloguj się swoim kontem — to ten sam profil i te same postępy co na komputerze.

**Ważne:** komputer musi być włączony z uruchomionym `start_telefon.bat`. Telefon jest
tylko ekranem — cała aplikacja działa na komputerze.

## Dodaj jak zwykłą aplikację (ikona na ekranie głównym)

- **Android (Chrome):** menu ⋮ → *Dodaj do ekranu głównego*.
- **iPhone (Safari):** przycisk udostępniania → *Do ekranu początkowego*.

Aplikacja otworzy się wtedy na pełnym ekranie, bez paska przeglądarki, z własną ikoną.

## Gdy strona się nie otwiera

| Objaw | Rozwiązanie |
|---|---|
| „Nie można połączyć" | Sprawdź, czy telefon jest na tym samym Wi-Fi (nie na danych komórkowych). |
| Nadal nie działa | Zapora Windows: Panel sterowania → Zapora → Zezwalaj aplikacji → zaznacz **Python** dla sieci prywatnych. |
| Adres się zmienił | Router przydziela adresy dynamicznie — po restarcie sprawdź adres w oknie `start_telefon.bat`. |
| Sieć „publiczna" | Ustawienia Windows → Sieć → Właściwości Wi-Fi → zmień profil na **Prywatna**. |

## Dźwięk i mikrofon na telefonie

Lektor (czytanie zdań) działa w przeglądarce telefonu, ale **pierwsze odtworzenie
wymaga dotknięcia ekranu** — taka jest zasada w telefonach. Wystarczy raz kliknąć
przycisk ▶ Odtwórz. Na Androidzie polski głos zwykle jest wbudowany; na iPhonie
sprawdź: Ustawienia → Dostępność → Treść mówiona → Głosy.

## Sposób 2: aplikacja bezpośrednio na telefonie (dla zaawansowanych)

Można uruchomić serwer na samym Androidzie przez aplikację **Termux**:
```
pkg install python
pip install fastapi uvicorn
cd /sdcard/LinguaForge
python main.py
```
Następnie w przeglądarce telefonu: `http://127.0.0.1:8177`.
Wtedy komputer nie jest potrzebny, ale aktualizacje trzeba kopiować ręcznie.
