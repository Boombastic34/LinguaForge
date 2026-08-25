package pl.linguaforge.app

import android.Manifest
import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.view.View
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.TextView
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

/**
 * Jedyny ekran aplikacji: pełnoekranowy widok internetowy pokazujący LinguaForge,
 * która działa na lokalnym serwerze uruchomionym w usłudze ServerService.
 */
class MainActivity : AppCompatActivity() {

    private lateinit var web: WebView
    private lateinit var splash: TextView
    private var ttsBridge: NativeTtsBridge? = null

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // powiadomienie usługi (Android 13+)
        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
            != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.POST_NOTIFICATIONS), 1)
        }

        // start serwera jako usługa pierwszoplanowa — przeżywa wyjście z aplikacji
        ContextCompat.startForegroundService(this, Intent(this, ServerService::class.java))

        splash = TextView(this).apply {
            text = "LinguaForge\n\nUruchamiam…"
            textSize = 22f
            setTextColor(0xFFFFFFFF.toInt())
            setBackgroundColor(0xFFE8590C.toInt())
            gravity = android.view.Gravity.CENTER
        }
        web = WebView(this).apply {
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            settings.databaseEnabled = true
            settings.mediaPlaybackRequiresUserGesture = false   // lektor bez dodatkowego dotknięcia
            isVerticalScrollBarEnabled = false
            overScrollMode = View.OVER_SCROLL_NEVER              // brak "gumowego" efektu strony
            setBackgroundColor(0xFFFFFFFF.toInt())
            settings.cacheMode = android.webkit.WebSettings.LOAD_DEFAULT
            visibility = View.GONE
            addJavascriptInterface(NativeTtsBridge(this@MainActivity, this).also { ttsBridge = it }, "NativeTTS")
            webViewClient = object : WebViewClient() {
                override fun shouldOverrideUrlLoading(v: WebView?, r: WebResourceRequest?): Boolean {
                    val url = r?.url?.toString() ?: return false
                    // linki zewnętrzne otwieramy w przeglądarce, resztę w aplikacji
                    return if (url.startsWith("http://127.0.0.1")) false
                    else { startActivity(Intent(Intent.ACTION_VIEW, r.url)); true }
                }
                override fun onPageFinished(view: WebView?, url: String?) {
                    splash.visibility = View.GONE
                    web.visibility = View.VISIBLE
                }
            }
        }
        val root = android.widget.FrameLayout(this)
        root.addView(web)
        root.addView(splash)
        setContentView(root)

        // cofnięcie w aplikacji zamiast zamykania
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (web.canGoBack()) web.goBack() else moveTaskToBack(true)
            }
        })

        waitForServerThenLoad()
    }

    /** Serwer potrzebuje chwili na start — próbujemy, aż odpowie. */
    private fun waitForServerThenLoad(attempt: Int = 0) {
        Thread {
            var ready = false
            for (i in 0 until 60) {
                try {
                    val c = java.net.URL("http://127.0.0.1:8177/api/ping").openConnection()
                            as java.net.HttpURLConnection
                    c.connectTimeout = 800; c.readTimeout = 800
                    if (c.responseCode == 200) { ready = true; c.disconnect(); break }
                    c.disconnect()
                } catch (e: Exception) { /* jeszcze nie wstał */ }
                Thread.sleep(500)
            }
            runOnUiThread {
                if (ready) web.loadUrl("http://127.0.0.1:8177/")
                else splash.text = "Nie udało się uruchomić aplikacji.\n" +
                        "Zamknij ją całkowicie i otwórz ponownie."
            }
        }.start()
    }

    override fun onResume() {
        super.onResume()
        // po powrocie do aplikacji odświeżamy tylko, gdy strona się nie wczytała
        if (web.url == null) waitForServerThenLoad()
    }

    override fun onDestroy() {
        ttsBridge?.shutdown()
        super.onDestroy()
    }
}
