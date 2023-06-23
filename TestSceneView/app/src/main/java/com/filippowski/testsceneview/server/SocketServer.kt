package com.filippowski.testsceneview.server

import com.filippowski.testsceneview.MainActivity
import java.io.IOException
import java.net.ServerSocket

class SocketServer(private val activity: MainActivity) : Thread() {
    private var serverSocket: ServerSocket? = null
    private var running = false

    override fun run() {
        running = true
        try {
            // Создаем серверный сокет
            serverSocket = ServerSocket(1234)

            // Принимаем новые подключения
            while (running) {
                val socket = serverSocket!!.accept()
                // Обрабатываем новое подключение в отдельном потоке
                ClientThread(activity, socket).start()
            }
        } catch (e: IOException) {
            e.printStackTrace()
        } finally {
            // Закрываем серверный сокет
            serverSocket?.close()
        }
    }

    fun stopServer() {
        running = false
        serverSocket?.close()
    }
}