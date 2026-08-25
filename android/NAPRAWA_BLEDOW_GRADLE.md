# Błędy przy pierwszym budowaniu — jak je naprawić

## Błąd: `Unable to load class 'org.gradle.util.VersionNumber'`

**Przyczyna:** Android Studio użyło najnowszej wersji Gradle (9.x), w której usunięto klasę
`VersionNumber`. Wtyczka osadzająca Pythona nadal jej potrzebuje, więc budowanie przerywa się
zanim cokolwiek się skompiluje. Wersja Gradle jest teraz **przypięta na sztywno** w pliku
`gradle/wrapper/gradle-wrapper.properties` (Gradle 8.7).

**Co zrobić po pobraniu poprawionej paczki:**

1. Zamknij projekt w Android Studio: **File → Close Project**.
2. Zatrzymaj tło Gradle'a: w oknie powitalnym **More Actions → Terminal**… albo prościej —
   zamknij całe Android Studio i w Menedżerze zadań (Ctrl+Shift+Esc) zakończ procesy
   **OpenJDK Platform binary** / **java.exe**, jeśli jakieś zostały.
3. Usuń zepsutą pamięć podręczną — skasuj folder:
   ```
   C:\Users\TWOJA_NAZWA\.gradle\caches
   ```
   (można skasować cały `.gradle`; zostanie pobrany od nowa)
4. W folderze `android` skasuj foldery `.gradle` i `build`, jeśli istnieją.
5. Uruchom Android Studio → **Open** → wskaż folder **`android`** z nowej paczki.
6. Gdy zapyta o zaufanie projektowi — **Trust Project**.
7. Poczekaj na **Gradle Sync**. Pobierze Gradle 8.7 (~130 MB) i biblioteki.

## Ustaw właściwą Javę (częsta druga przyczyna)

**File → Settings → Build, Execution, Deployment → Build Tools → Gradle**
→ pole **Gradle JDK** ustaw na **jbr-17** (albo dowolne **17**). Nie używaj 21 ani 8.
→ **OK** → **File → Sync Project with Gradle Files**.

## Jeśli Android Studio proponuje aktualizacje

Odrzucaj propozycje „Update Gradle plugin" i „Upgrade Gradle" — **wersje w tym projekcie są
dobrane tak, aby działały razem**:

| Element | Wersja |
|---|---|
| Gradle | 8.7 |
| Android Gradle Plugin | 8.4.0 |
| Kotlin | 1.9.24 |
| Chaquopy (Python) | 15.0.1 |
| Gradle JDK | 17 |
| compileSdk / targetSdk | 34 |

Podniesienie którejkolwiek pozycji osobno zwykle psuje budowanie.

## Gdy sync nadal nie przechodzi

1. **File → Invalidate Caches… → Invalidate and Restart** (zaznacz „Clear file system cache").
2. Sprawdź internet — pierwszy sync pobiera kilkaset MB.
3. Sprawdź, czy w **SDK Manager → SDK Tools** masz **NDK (Side by side)** i **CMake**.
4. Jeśli komunikat mówi o `SDK location not found`: **File → Project Structure → SDK Location**
   → wskaż `C:\Users\TY\AppData\Local\Android\Sdk`.

## Sprawdzian: czy wszystko gotowe

W dolnym pasku po synchronizacji powinno pojawić się **„BUILD SUCCESSFUL"** albo
**„Gradle sync finished"**. Dopiero wtedy: **Build → Build Bundle(s)/APK(s) → Build APK(s)**.
