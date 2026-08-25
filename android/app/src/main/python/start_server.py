# -*- coding: utf-8 -*-
"""Punkt wejścia serwera LinguaForge wewnątrz aplikacji Android (Chaquopy).

Kod aplikacji (main.py, core/, data/, static/) jest dołączany do paczki jako
moduł `linguaforge`. Dane zapisywalne (konta, dodane treści) trzymamy w prywatnym
katalogu aplikacji przekazanym z Kotlina.
"""
import os
import shutil
import sys
import threading


def _prepare_home(files_dir):
    """Przygotowuje katalog zapisu i kopiuje tam materiały przy pierwszym starcie."""
    home = os.path.join(files_dir, "linguaforge")
    os.makedirs(os.path.join(home, "accounts"), exist_ok=True)
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    src_data = os.path.join(pkg_dir, "linguaforge", "data")
    dst_data = os.path.join(home, "data")
    if os.path.isdir(src_data) and not os.path.isdir(dst_data):
        shutil.copytree(src_data, dst_data)          # materiały edytowalne przez administratora
    return home


def main(files_dir):
    home = _prepare_home(files_dir)
    os.environ["LF_HOME"] = home
    os.environ["LF_ANDROID"] = "1"

    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(pkg_dir, "linguaforge")
    os.environ["LF_APP_DIR"] = app_dir      # jawna, pewna ścieżka — main.py jej nie zgaduje
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)

    import main as lf                                 # główny moduł aplikacji
    import uvicorn

    def run():
        uvicorn.run(lf.app, host="127.0.0.1", port=8177, log_level="warning")

    threading.Thread(target=run, daemon=False).start()
    return "started"
