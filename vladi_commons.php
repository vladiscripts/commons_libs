<?php // <head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head>

// вывод на экран форматированный
function showarray($t) {echo '<pre>'.print_r($t,1).'</pre>';}

// В верхний регистр 1-ю букву строки
function mb_firstToUpper($word, $encoding = 'UTF8') {
	return mb_strtoupper(mb_substr($word,0,1,$encoding),$encoding) . mb_substr($word,1,mb_strlen($word),$encoding);
}

// В верхний регистр 1-ю букву строки, остальные в строчные
function mb_firstToUpper_strToLow($word, $encoding = 'UTF8') {
	return mb_strtoupper(mb_substr($word, 0, 1, $encoding), $encoding) . mb_substr(mb_convert_case($word, MB_CASE_LOWER, $encoding), 1, mb_strlen($word), $encoding); 
}

// запись файла csv
function fsave_csv($fout, $text, $delimiter=',') {
	$fp = fopen($fout,'w'); if ($fp) {
	//fputcsv($fp, $titles);
	foreach ($text as $line) { 
		fputcsv($fp, $line, $delimiter); //explode($fields_separator, $line));
	}
	fclose($fp);}
}

// запись файла
function fsave($fname, $text) {
	$fs=fopen($fname,'wt');
	 if (fwrite($fs, $text) === FALSE) {echo "Не могу произвести запись в файл ($fname)";exit;}
	fclose($fs);
}

// mysql инициация
$mysql_init = "SET NAMES 'utf8'; SET CHARACTER SET 'utf8'; SET SESSION collation_connection = 'utf8_general_ci'; SET TIME_ZONE = '+03:00'";


?>