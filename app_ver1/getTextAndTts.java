package com.example.eunsong.sndtoserver;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ContentValues;
import android.os.AsyncTask;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Locale;

import static android.speech.tts.TextToSpeech.ERROR;

public class getTextAndTts extends Activity {

    private TextView tv_outPut;
    private TextToSpeech tts;              // TTS 변수 선언
    private Button button;

    //String url = "http://ec2-13-209-47-170.ap-northeast-2.compute.amazonaws.com/test.php";

    @SuppressLint("MissingSuperCall")
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.get_text_and_tts);

        //Log.d("경로", url);

        // 위젯에 대한 참조.
        tv_outPut = (TextView) findViewById(R.id.tv_outPut);
        button = (Button) findViewById(R.id.tts);

        // 결과값 화면에 출력
       tv_outPut.setText(Network.output);

        // TTS를 생성하고 OnInitListener로 초기화 한다.
        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status != ERROR) {
                    // 언어를 선택한다.
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // editText에 있는 문장을 읽는다.
                tts.speak(tv_outPut.getText().toString(), TextToSpeech.QUEUE_FLUSH, null);
                Toast.makeText(getApplicationContext(), "TTS 실행", Toast.LENGTH_SHORT).show();
            }
        });
    }



    @Override
    protected void onDestroy() {
        super.onDestroy();
        // TTS 객체가 남아있다면 실행을 중지하고 메모리에서 제거한다.
        if (tts != null) {
            tts.stop();
            tts.shutdown();
            tts = null;
        }
    }


}
