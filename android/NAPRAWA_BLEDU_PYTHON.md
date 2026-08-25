# Błąd: `python.exe finished with non-zero exit value 1`

## Co się stało
Podczas budowania Chaquopy instaluje biblioteki Pythona do aplikacji. Zestaw użyty
wcześniej zawierał **pydantic 2**, którego część jest napisana w Ruście i kompilowana —
**dla Androida takiej wersji nie ma**, więc instalacja przerywała się błędem.

## Poprawka (już w projekcie od wersji 1.0.2)
W `app/build.gradle` jest teraz zestaw w całości napisany w Pythonie:

```
fastapi 0.99.1 · pydantic 1.10.13 · starlette 0.27.0 · uvicorn 0.22.0
anyio 3.7.1 · sniffio · h11 · click · idna · typing-extensions
```

Cała aplikacja została przetestowana na tym zestawie: logowanie, fiszki, ogniwa Ścieżki,
ocenianie odpowiedzi, eksport i pliki statyczne działają identycznie.
**Nie podnoś tych wersji** — nowsze wymagają pydantic 2.

## Co zrobić u siebie

1. Rozpakuj paczkę **v1.0.2** (albo podmień sam plik `android/app/build.gradle`).
2. W Android Studio: **File → Sync Project with Gradle Files**.
3. Wyczyść poprzednią, nieudaną instalację Pythona — skasuj folder:
   ```
   android\app\build\python
   ```
   (albo w Android Studio: **Build → Clean Project**)
4. Zbuduj ponownie: podwójny **Shift** → **Generate APKs**.

## Jak podejrzeć prawdziwy powód, gdyby błąd wrócił
Kliknij napis **„Build: failed"** po lewej stronie komunikatu, a potem przewiń wyżej.
Interesuje Cię linia zaczynająca się od `ERROR: Could not find a version…`
albo `Chaquopy: Failed to install…` — w niej jest nazwa problematycznego pakietu.
Prześlij mi tę linię, a dobiorę zamiennik.

## Dlaczego akurat te wersje
Chaquopy potrafi zainstalować:
- pakiety **czysto pythonowe** (pliki `py3-none-any.whl`) — bez ograniczeń,
- pakiety natywne **tylko wtedy**, gdy ktoś zbudował je wcześniej dla Androida.

pydantic 1.10 publikuje wersję czysto pythonową, pydantic 2 — nie. Stąd wybór.
FastAPI w wersji 0.99 to ostatnia gałąź współpracująca z pydantic 1, a ta aplikacja
nie korzysta z żadnej funkcji dodanej w nowszych wydaniach.
