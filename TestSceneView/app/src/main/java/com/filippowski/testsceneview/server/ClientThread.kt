package com.filippowski.testsceneview.server


import com.filippowski.testsceneview.MainActivity
import java.io.BufferedReader
import java.io.IOException
import java.io.InputStreamReader
import java.io.PrintWriter
import java.net.Socket

class ClientThread(private val activity: MainActivity, private val socket: Socket) : Thread() {
    private var running = false

    override fun run() {
        running = true
        try {
            // Получаем потоки для чтения и записи
            val inputStream = BufferedReader(InputStreamReader(socket.getInputStream()))
            val outputStream = PrintWriter(socket.getOutputStream(), true)

            // Читаем и отображаем сообщения от клиента
            while (running) {
                val message = inputStream.readLine()
                if (message != null) {
                    activity.runOnUiThread {
                        activity.getMessage(message)
                    }
                }
            }
        } catch (e: IOException) {
            e.printStackTrace()
        } finally {
            // Закрываем соединение
            socket.close()
        }
    }

    fun stopClient() {
        running = false
        socket.close()
    }



}