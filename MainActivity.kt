package com.eksa.vpn

import android.app.Activity
import android.content.Intent
import android.net.VpnService
import android.os.Bundle
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView

class MainActivity : Activity() {
    private val requestCode = 701
    private lateinit var status: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(40, 80, 40, 40)
        }
        status = TextView(this).apply { text = "EKSA VPN — Disconnected"; textSize = 20f }
        val connect = Button(this).apply {
            text = "Connect"
            setOnClickListener {
                val permission = VpnService.prepare(this@MainActivity)
                if (permission != null) startActivityForResult(permission, requestCode)
                else startVpnService()
            }
        }
        val disconnect = Button(this).apply {
            text = "Disconnect"
            setOnClickListener { stopService(Intent(this@MainActivity, EksaVpnService::class.java)); status.text = "Disconnected" }
        }
        layout.addView(status); layout.addView(connect); layout.addView(disconnect)
        setContentView(layout)
    }

    @Deprecated("Use Activity Result API in production")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == this.requestCode && resultCode == RESULT_OK) startVpnService()
    }

    private fun startVpnService() {
        startForegroundService(Intent(this, EksaVpnService::class.java))
        status.text = "VPN service started — tunnel engine not yet integrated"
    }
}
