function decrypt(stringData, passwd){
	// remove '\n' from message
	stringData = stringData.replace(/\r?\n|\r/g, "");
	// decrypt message
	var de = CryptoJS.AES.decrypt(stringData, passwd, {keySize: 256/32});
	// decode content into UTF-8
	var content = (de.toString(CryptoJS.enc.Utf8));
	return content;
}

function decrypt_file(filename, passwd){
	var stringData = $.ajax({
					url: filename + ".html.cyph.txt",
					async: false
				 }).responseText;
	// decode content into UTF-8
	var content = decrypt(stringData, passwd);
	return content;
}

function encrypt(stringData, passwd){
	// decrypt message
	var en = CryptoJS.AES.encrypt(stringData, passwd, {keySize: 256/32});
	var content = (en.toString());
	return content;
}

function encrypt_file(filename, passwd){
	var stringData = $.ajax({
					url: filename + ".html.cyph.txt",
					async: false
				 }).responseText;
	var content = encrypt(stringData, passwd);
	return content;
}