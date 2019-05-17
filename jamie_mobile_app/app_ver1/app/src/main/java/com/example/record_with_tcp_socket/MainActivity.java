package com.example.record_with_tcp_socket;

import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.Environment;
import android.speech.tts.TextToSpeech;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.*;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import static android.speech.tts.TextToSpeech.ERROR;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {

    private MediaPlayer player;
    private MediaRecorder recorder;

    private Button record;
    private Button send;
    private Button receive;
    private TextView text;

    private TextToSpeech tts;
    //
    private Button all;
    int count = 0;

    private RequestQueue queue;
    private static final String TAG = "MAIN";

    String File_name = "record.wav";
    String input = Environment.getExternalStorageDirectory().getAbsolutePath() + "/" + File_name;
    String server_address = "http://ec2-13-209-87-151.ap-northeast-2.compute.amazonaws.com";
    String server_IP = "13.209.87.151";
    int server_port = 10002;

    int state = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        recorder = new MediaRecorder();
        player = new MediaPlayer();

        record = findViewById(R.id.record);
        send = findViewById(R.id.send);
        receive = findViewById(R.id.receive);
        text = findViewById(R.id.textView);

        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != ERROR) {
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });

        //
        all = findViewById(R.id.all);

        queue = Volley.newRequestQueue(this);

        //
        all.setOnClickListener(new View.OnClickListener() {
            AudioClient client = new AudioClient();
            String url = server_address + "/test.php";

            StringRequest stringRequest = new StringRequest(Request.Method.POST, url, new Response.Listener<String>() {
                @Override
                public void onResponse(String response) {
                    //nothing
                    Toast.makeText(getApplicationContext(), "execute server", Toast.LENGTH_SHORT).show();

                    client.connect(server_IP, server_port, input);
                    onStop();
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError e) {
                    e.printStackTrace();
                }
            });

            @Override
            public void onClick(View v) {
                if(count == 0) {
                    initAudioRecorder();
                    Toast.makeText(getApplicationContext(), "녹음을 시작합니다.", Toast.LENGTH_LONG).show();
                    recorder.start();

                    all.setText("stop recording");
                    count = 1;
                } else if(count == 1) {
                    Toast.makeText(getApplicationContext(), "녹음이 중지되었습니다.", Toast.LENGTH_LONG).show();
                    recorder.stop();

                    all.setText("button");
                    count = 0;

                    stringRequest.setTag(TAG);
                    queue.add(stringRequest);

                    Toast.makeText(getApplicationContext(), "uploaded the audio", Toast.LENGTH_SHORT).show();



                }
            }
        });
        //

        record.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                if(state == 0) {
                    //녹음시작
                    initAudioRecorder();
                    Toast.makeText(getApplicationContext(), "녹음을 시작합니다.", Toast.LENGTH_LONG).show();
                    recorder.start();

                    record.setText("stop recording");
                    state = 1;
                } else {
                    //녹음중지
                    Toast.makeText(getApplicationContext(), "녹음이 중지되었습니다.", Toast.LENGTH_LONG).show();
                    recorder.stop();

                    record.setText("start recording");
                    state = 0;
                }
            }
        });

        send.setOnClickListener(new View.OnClickListener() {
            AudioClient client = new AudioClient();
            String url = server_address + "/test.php";

            StringRequest stringRequest = new StringRequest(Request.Method.POST, url, new Response.Listener<String>() {
                @Override
                public void onResponse(String response) {
                    //nothing
                    Toast.makeText(getApplicationContext(), "execute server", Toast.LENGTH_SHORT).show();

                    client.connect(server_IP, server_port, input);
                    onStop();
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError e) {
                    e.printStackTrace();
                }
            });

            @Override
            public void onClick(View v) {
                stringRequest.setTag(TAG);
                queue.add(stringRequest);

                Toast.makeText(getApplicationContext(), "uploaded the audio", Toast.LENGTH_SHORT).show();
            }
        });

        receive.setOnClickListener(new View.OnClickListener() {
            String url = server_address + "/new.php";

            StringRequest stringRequest = new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {
                @Override
                public void onResponse(String response) {
                    text.setText(response);
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError e) {
                    e.printStackTrace();
                }
            });

            @Override
            public void onClick(View v) {
                stringRequest.setTag(TAG);
                queue.add(stringRequest);

                tts.speak(text.getText().toString(), TextToSpeech.QUEUE_FLUSH, null);
            }

        });

    }

    @Override
    protected void onStop() {
        super.onStop();
        if(queue != null) {
            queue.cancelAll(TAG);
        }
    }

    private void initAudioRecorder() {
        recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        recorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

        recorder.setOutputFile(input);

        try{
            recorder.prepare();
        } catch(Exception e) {
            e.printStackTrace();
        }
    }

    protected void onDestroy() {
        super.onDestroy();

        if(tts != null) {
            tts.stop();
            tts.shutdown();
            tts = null;
        }
    }
}
