package com.eksa.vpn

import android.net.VpnService
import android.content.Intent
import android.os.IBinder
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build

class EksaVpnService : VpnService() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val channelId = "eksa_vpn_status"
        val manager = getSystemService(NotificationManager::class.java)
        if (Build.VERSION.SDK_INT >= 26) {
            manager.createNotificationChannel(NotificationChannel(channelId, "EKSA VPN", NotificationManager.IMPORTANCE_LOW))
        }
        val notification = if (Build.VERSION.SDK_INT >= 26) {
            Notification.Builder(this, channelId).setContentTitle("EKSA VPN")
                .setContentText("VPN service ready; tunnel core integration required")
                .setSmallIcon(android.R.drawable.stat_sys_warning).build()
        } else {
            @Suppress("DEPRECATION")
            Notification.Builder(this).setContentTitle("EKSA VPN").setContentText("Tunnel core integration required")
                .setSmallIcon(android.R.drawable.stat_sys_warning).build()
        }
        startForeground(1, notification)
        // TODO: integrate a licensed V2Ray/Xray Android core here.
        // Do not report CONNECTED until the core confirms the tunnel is established.
        return START_STICKY
    }
    override fun onBind(intent: Intent?): IBinder? = super.onBind(intent)
}
