package pl.linguaforge.app

import android.app.*
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.os.PowerManager
import androidx.core.app.NotificationCompat
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

/**
 * Serwer LinguaForge (FastAPI/uvicorn) uruchomiony w Pythonie wewnątrz aplikacji.
 * Działa jako usługa pierwszoplanowa, dzięki czemu Android jej nie zamyka,
 * gdy użytkownik wyjdzie z aplikacji.
 */
class ServerService : Service() {

    private var wakeLock: PowerManager.WakeLock? = null
    private var started = false

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        startForeground(1, buildNotification())
        wakeLock = (getSystemService(POWER_SERVICE) as PowerManager)
            .newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "LinguaForge::server")
            .apply { setReferenceCounted(false); acquire() }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (!started) {
            started = true
            Thread {
                if (!Python.isStarted()) Python.start(AndroidPlatform(this))
                val py = Python.getInstance()
                // katalog zapisu: prywatna pamięć aplikacji
                py.getModule("start_server").callAttr("main", filesDir.absolutePath)
            }.start()
        }
        return START_STICKY          // system wznowi usługę, gdyby ją ubił
    }

    private fun buildNotification(): Notification {
        val id = "linguaforge"
        if (Build.VERSION.SDK_INT >= 26) {
            val ch = NotificationChannel(id, "LinguaForge", NotificationManager.IMPORTANCE_LOW)
            ch.setShowBadge(false)
            (getSystemService(NotificationManager::class.java)).createNotificationChannel(ch)
        }
        val pi = PendingIntent.getActivity(
            this, 0, Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)
        return NotificationCompat.Builder(this, id)
            .setContentTitle(getString(R.string.service_title))
            .setContentText(getString(R.string.service_text))
            .setSmallIcon(R.mipmap.ic_launcher)
            .setOngoing(true)
            .setContentIntent(pi)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }

    override fun onDestroy() {
        wakeLock?.let { if (it.isHeld) it.release() }
        super.onDestroy()
    }
}
