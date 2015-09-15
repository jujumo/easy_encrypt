function decrypt(stringData, passwd){
	try {
		// remove '\n' from message
		stringData = stringData.replace(/\r?\n|\r/g, "");
		// decrypt message
		var de = CryptoJS.AES.decrypt(stringData, passwd, {keySize: 256/32});
		// decode content into UTF-8
		var content = (de.toString(CryptoJS.enc.Utf8));
		return content;
	} catch(err) {
		return false;
	}
}

function encrypt(content, passwd){
	try {
		var en = CryptoJS.AES.encrypt(content, passwd, {keySize: 256/32});
		content = (en.toString());
		return content;
	} catch(err) {
		return false;
	}
}
