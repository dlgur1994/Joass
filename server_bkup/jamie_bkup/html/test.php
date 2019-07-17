<!DOCTYPE html>
<html>
<head>
	<meta charset='utf-8'/>
</head>
<body>
<?php 
// 변수 내용 출력 
$command = "java AudioServer";
$output = shell_exec($command);

echo($output);
?> 
</body>
</html>
