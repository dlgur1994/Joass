package com.example.eunsong.sndtoserver;
import android.os.Environment;
import android.util.Log;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.EventListener;

class Network {
    public static String output = "";

    //서버통신
    public static String IP_ADDRESS = "http://13.125.251.29/upload"; //서버주소입력

    //request header
    public String attachmentName = "sound";
    public String lineEnd = "\r\n";
    public String twoHyphens = "--";
    public String boundary = "*****";


    private static final int BUFFER_SIZE = 1 * 1024 * 1024;
    static final String FILE_PATH = Environment.getExternalStorageDirectory().getAbsolutePath();
    private static String TAG = "joassprac";

    //처음 url, 통신 instance
    public URL url;
    public HttpURLConnection httpURLConnection;

    //서버에서 보내는 responsecode
    int serverResponseCode = 0;

    //서버에서 받는 response
    InputStream responseInput;
    InputStreamReader responseInputStream;
    BufferedReader bufferedReader;
    StringBuilder stringBuilder;
    String line;
    String resultMessage;


    //서버와 통신 함수
    public void setHttpURLConnection(){
        System.out.println("ㅗㅗ2");
        try {
            url = new URL(IP_ADDRESS);
            httpURLConnection = (HttpURLConnection)url.openConnection();
            Log.d("connect", "connect " + url);


            //연결 준비 & 연결
            httpURLConnection.setDoInput(true);
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setChunkedStreamingMode(0);
            httpURLConnection.setUseCaches(false);
            httpURLConnection.setRequestMethod("POST");
            //httpURLConnection.setReadTimeout(TIMEOUT);
            //httpURLConnection.setConnectTimeout(TIMEOUT);
            httpURLConnection.setRequestProperty("Connection", "Keep-Alive");
            httpURLConnection.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);
            httpURLConnection.setRequestProperty("sun.net.http.allowRestrictedHeaders", "true");
            httpURLConnection.connect();

          Thread workThread = new Thread(new Runnable() {
                @Override
                public void run() {
                    while(true){
                        // 서버에서 넘겨주는 메세지 받는 스레
                        receiveFromServer();
                    }
                }
            });
            workThread.start();

        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    protected void sendToServer(String... param) {
        try {
            String filename = param[0];
            Log.d("Filename: ",filename);

            String fullFilename = FILE_PATH + "/" +filename;
            Log.d("full Filename: ",filename);


            File sourcefile = new File(fullFilename);
            FileInputStream wavfile = new FileInputStream(sourcefile);

            int available = wavfile.available();
            Log.d("size: ", Integer.toString(available));


            //녹음 파일 서버에 보내기
            //write data
            DataOutputStream outputStream = new DataOutputStream(httpURLConnection.getOutputStream());
            outputStream.writeBytes(twoHyphens + boundary + lineEnd);
            outputStream.writeBytes("Content-Disposition: form-data; name=\"uploaded_file\";filename=\"" + filename+lineEnd);
            outputStream.writeBytes(lineEnd);

            // Log.d("outputStream size: ", Integer.toString(outputStream.));

            int bytesAvailable = wavfile.available();
            int maxBufferSize = 1024;
            int bufferSize = Math.min(bytesAvailable, maxBufferSize);

            byte[] buffer = new byte[bufferSize];
            int length;
            while((length = wavfile.read(buffer)) != -1){
                outputStream.write(buffer, 0, length);
            }

            Log.d("outputStream", "sendToServer");
            outputStream.writeBytes(lineEnd);
            outputStream.writeBytes(twoHyphens+boundary+twoHyphens+lineEnd);


            outputStream.flush();
            outputStream.close();
            wavfile.close();


        } catch (IOException e) {
            e.printStackTrace();
            Log.d(TAG, "InputStream: Error!!!! ", e);
        } catch (Exception e) {
            Log.d(TAG, "InsertData: Error!!!! ", e);
        }
    }


    private void receiveFromServer(){
        String result = "";
        StringBuilder sb = null;
        receiveHandler eventHandler = new receiveHandler();

        int responseStatusCode = 0;
        try {
            responseStatusCode = httpURLConnection.getResponseCode();
           // Log.d(TAG, "POST response code - " + responseStatusCode);

            InputStream rinputStream;
            if(responseStatusCode == HttpURLConnection.HTTP_OK) {
                rinputStream = httpURLConnection.getInputStream();
              //  Log.d(TAG, "POST response code - inputstream");
            }
            else{
                rinputStream = httpURLConnection.getErrorStream();
            }

            InputStreamReader inputStreamReader = new InputStreamReader(rinputStream, "UTF-8");
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            sb = new StringBuilder();
            String line = null;


            while((line = bufferedReader.readLine()) != null){
                sb.append(line);
            }
            result = sb.toString();
            //System.out.println("result,"+result);
            if(result == null){
            //    System.out.println("result is NULL");
            }
            else {
                System.out.println("Hello," + result);
                eventHandler.messageHandle(result);
            }

            //inputStreamReader.close();
            //bufferedReader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        //이벤트로 호출해서 sb를 string형식으로 넘겨준다.
    }

}


class receiveHandler implements EventListener{
    void messageHandle(String message){
        System.out.println("access to eventhandler");
        System.out.println("message"+message);

        String[] splitMessage = message.split(",");
        System.out.println(splitMessage[0]);

        switch(splitMessage[0]){
            case "output":
                Network.output = splitMessage[2];
                System.out.println(splitMessage[2]);
                break;

            default:
                System.out.println(splitMessage[0]);
                break;

        }

    }

}
