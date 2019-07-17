import java.net.*;
import java.io.*;

public class AudioServer {
  public static void main(String[] args) {
    String file_location = "/var/www/html/input.wav";
    ServerSocket serverSocket = null;

    try {
      serverSocket = new ServerSocket(10002);
      System.out.println("socket 10002");
    } catch(IOException e) {
      System.out.println("Can't setup on this port number");
    }

    Socket socket = null;

    try {
      socket = serverSocket.accept();
      System.out.println("socket accept");

      //DataOutputStream out = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()));
      DataInputStream input = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
      FileOutputStream output = new FileOutputStream(file_location);
      byte[] bytes = new byte[16 * 1024];

      int count;
      while((count = input.read(bytes)) > 0) {
        output.write(bytes, 0, count);
      }

      output.close();
      input.close();
      socket.close();
      serverSocket.close();
    } catch(Exception e) {
      System.out.println("exception");
    }
  }
}

/*
public class AudioServer {

       public static void main(String[] args) throws IOException {
            if(args.length == 0)
              throw new IllegalArgumentException("expected sound file arg");

            File soundFile = AudioUtil.getSoundFile(args[0]);

            System.out.println("server: " + soundFile);

            try(ServerSocket serverSocket = new ServerSocket(10002);
            FileInputStream in = new FileInputStream(soundFile)) {

              if(serverSocket.isBound()) {
                Socket client = serverSocket.accept();
                OutputStream out = client.getOutputStream();

                byte buffer[]= new byte[2048];
                int count;
                while((count = in.read(buffer)) != -1)
                  out.write(buffer, 0, count);
              }
            }

            System.out.println("server: shutdown");
       }
}

class AudioUtil {
  public static File getSoundFile(String fileName) {
    File soundFile = new File(fileName);

    if(!soundFile.exists() || !soundFile.isFile())
      throw new IllegalArgumentException("not a file: " + soundFile);

    return soundFile;
  }
}
*/
