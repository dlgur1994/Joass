<?php 
// 변수 내용 출력 
$command = "sudo rm /var/www/html/new.php ; touch /var/www/html/new.php ; . /home/ubuntu/tf/tensorflow-dev/bin/activate ; python3 /home/ubuntu/code/server.py";
#$command = 'python3 /home/ubuntu/code/server_.py';
#$command = "python3 test.py && python3 test1.py";

#$output =  shell_exec($command);
#$output = exec($command);

##
exec($command,$out);
foreach($out as $key => $value) {
	echo $key." ".$value."<br>";
}

##

#sleep(3);

$result = fopen('/var/www/html/new.php', 'r');

echo($output);
echo fread($result, filesize('/var/www/html/new.php'));
?>
