<?php
    //Headers
    header('Access-Control-Allow-Origin: *');
    header('Content-Type: application/json');

    $random = rand(0000000000, 9999999999); //Gera uma variavel aleatória

    $target_dir = "/home/marcos/uploads/"; //Diretório onde serão salvos os arquivos
    $target_base = $target_dir . basename($_FILES["fileToUpload"]["name"]); //Define o nome padrão do arquivo
    $uploadOk = 1; //Essa variavel verifica se o upload ocorreu corretamente, isso evita colocar ifs um dentro do outro
    $FileType = strtolower(pathinfo($target_base,PATHINFO_EXTENSION)); //Pega a extensão do arquivo passado, isso em minúculo
    $target_file = $target_dir . $random . "." . $FileType; //Define o caminho que será salvo o arquivo

    // Allow certain file for http://www.labvirtual.ileel.ufu.br/labileelhttp://www.labvirtual.ileel.ufu.br/labileelmats
    if($FileType != "jpg" && $FileType != "wav") { //Verifica se a extensão é compátivel
        $output = "Sorry, only JPG or WAV files are allowed."; //Grava uma sáida
 	$uploadOk = 0; //Avisa que ocorreu erro de upload
    }

    // Check if $uploadOk is set to 0 by an error
    if ($uploadOk == 0) {
        echo json_encode($output); //Mostra a saída salva
        // if everything is ok, try to upload file
    } else {
        if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) { //Salva o arquivo no servidor
            //Variavel contendo o comando que será executado
            $request = "cd /var/www/service/; java -cp /var/www/service/lib/weka.jar:/var/www/service/lib/gson-2.6.2.jar:/var/www/service/Analyzer.jar lab.EmotionAnalyzer $target_file 2>/dev/null";
            $output = shell_exec($request); //Executa o comando e salva sua saida
            exec("rm $target_file"); //Remove o arquivo passado do servidor
            echo $output; //Mostra a saída na tela
        } else { //Caso não consiga salvar o arquivo no servidor
            $output = "Sorry, there was an error uploading your file."; //Grava uma sáida
            echo json_encode($output); //Mostra a saída salva
        }
    }
?>
