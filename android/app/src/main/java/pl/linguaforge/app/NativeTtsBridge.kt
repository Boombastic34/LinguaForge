package pl.linguaforge.app

import android.content.Context
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.webkit.JavascriptInterface
import android.webkit.WebView
import java.util.Locale

/**
 * Natywny lektor Androida (android.speech.tts.TextToSpeech) udostępniony do JavaScriptu
 * w stronie WebView. WebView na Androidzie NIE obsługuje przeglądarkowego
 * window.speechSynthesis — dlatego strona wywołuje ten most zamiast tego,
 * gdy wykryje, że działa wewnątrz naszej aplikacji (window.NativeTTS istnieje).
 *
 * Strona JS wywołuje: NativeTTS.speak(tekst, "en"|"pl", szybkość)
 * Most wywołuje z powrotem: window.onNativeTtsEnd() po zakończeniu (dla ewentualnych animacji).
 */
class NativeTtsBridge(private val context: Context, private val webView: WebView) {

    private var tts: TextToSpeech? = null
    private var ready = false
    private val pending = mutableListOf<() -> Unit>()

    init {
        tts = TextToSpeech(context) { status ->
            ready = (status == TextToSpeech.SUCCESS)
            if (ready) {
                tts?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                    override fun onStart(id: String?) {}
                    override fun onDone(id: String?) {
                        webView.post { webView.evaluateJavascript(
                            "window.onNativeTtsEnd && window.onNativeTtsEnd()", null) }
                    }
                    @Deprecated("Deprecated in Java")
                    override fun onError(id: String?) {}
                })
                synchronized(pending) {
                    pending.forEach { it() }
                    pending.clear()
                }
            }
        }
    }

    @JavascriptInterface
    fun isAvailable(): Boolean = true

    @JavascriptInterface
    fun speak(text: String, lang: String, rate: Float) {
        val run: () -> Unit = {
            val locale = if (lang == "pl") Locale("pl", "PL") else Locale.US
            val result = tts?.setLanguage(locale)
<<<<<<< HEAD
            // brak danych głosowych dla danego języka -> spróbuj wariantu ogólnego
            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                tts?.setLanguage(if (lang == "pl") Locale("pl") else Locale.ENGLISH)
            }
            tts?.setSpeechRate(rate.coerceIn(0.5f, 1.5f))
            tts?.stop()
            tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "lf_" + System.currentTimeMillis())
=======
            val missing = result == TextToSpeech.LANG_MISSING_DATA ||
                          result == TextToSpeech.LANG_NOT_SUPPORTED
            if (missing && lang == "pl") {
                // Bez polskich danych głosowych silnik przeczytałby polski tekst
                // angielską wymową (bełkot). Zamiast tego informujemy stronę.
                webView.post {
                    webView.evaluateJavascript(
                        "window.onNativeTtsMissing && window.onNativeTtsMissing('pl')", null)
                }
            } else {
                if (missing) tts?.setLanguage(Locale.ENGLISH)
                tts?.setSpeechRate(rate.coerceIn(0.5f, 1.5f))
                tts?.stop()
                tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "lf_" + System.currentTimeMillis())
            }
>>>>>>> 8f567b6 (LinguaForge v1.6.0 update)
            Unit
        }
        if (ready) run() else synchronized(pending) { pending.add(run) }
    }

<<<<<<< HEAD
=======
    /** Czy telefon ma dane głosowe dla danego języka. */
    @JavascriptInterface
    fun canSpeak(lang: String): Boolean {
        val locale = if (lang == "pl") Locale("pl", "PL") else Locale.US
        val r = tts?.isLanguageAvailable(locale) ?: return false
        return r == TextToSpeech.LANG_AVAILABLE ||
               r == TextToSpeech.LANG_COUNTRY_AVAILABLE ||
               r == TextToSpeech.LANG_COUNTRY_VAR_AVAILABLE
    }

>>>>>>> 8f567b6 (LinguaForge v1.6.0 update)
    @JavascriptInterface
    fun stop() {
        tts?.stop()
    }

    @JavascriptInterface
    fun hasPolishVoice(): Boolean {
        val voices = tts?.voices ?: return false
        return voices.any { it.locale.language == "pl" }
    }

    fun shutdown() {
        tts?.stop()
        tts?.shutdown()
    }
}
