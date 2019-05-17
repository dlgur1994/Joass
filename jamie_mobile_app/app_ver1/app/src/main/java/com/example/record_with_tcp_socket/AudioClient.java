package com.example.record_with_tcp_socket;

import android.os.AsyncTask;
import android.widget.Toast;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class AudioClient {
    public static void connect(final String server_IP, final int server_port, final String input_file) {
        //Socket socket;

        final File file = new File(input_file);

        try {
            AsyncTask<Void, Void, Void> asyncTask = new AsyncTask<Void, Void, Void>() {
                @Override
                protected Void doInBackground(Void... voids) {

                    Socket socket;
                    byte[] bytes = new byte[16 * 1024];

                    try {
                        socket = new Socket(server_IP, server_port);

                        InputStream input = new FileInputStream(file);
                        OutputStream output = socket.getOutputStream();

                        int count;
                        while((count = input.read(bytes)) > 0) {
                            output.write(bytes, 0, count);
                        }

                        output.close();
                        input.close();
                        socket.close();

                    } catch(IOException e) {
                        e.printStackTrace();
                    }

                    return null;
                }
            };

            asyncTask.execute();

        } catch(Exception e) {
            e.printStackTrace();
        }
    }
}
