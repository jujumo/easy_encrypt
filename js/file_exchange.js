function read_file_from_url(filename) {
	var content = $.ajax({
					url: filename,
					async: false
				 }).responseText;
	return content;
}

function encrypt_to_file(input_filename, text, passwd) {
	var encrypted = encrypt(text, passwd);
			a = $('<a>',{download: input_filename + '.aes',
				href: 'data:application/octet-stream,' + encrypted
			}).appendTo('body');
	a[0].click();
	a.remove();
	return true;
}

function decrypt_to_file(input_filename, text, passwd) {
	var decrypted = decrypt(text, passwd);
	if(decrypted === false || decrypted.substr(0,5) != 'data:'){
		//alert("Invalid pass phrase or file! Please try again.");
		return false;
	}
	a = $('<a>',{download: input_filename.replace('.aes', ''),
		href: decrypted
	}).appendTo('body');
	a[0].click();
	a.remove();
	return true;
}

function encrypt_from_file(file, passwd, callback) {
	reader = new FileReader();
	reader.onload = function(e) {
		var ok = encrypt_to_file(file.name, e.target.result, passwd);
		if (callback!==undefined) { callback(ok); } 
	};
	reader.readAsDataURL(file);
}

function decrypt_from_file(file, passwd, callback) {
	reader = new FileReader();
	reader.onload = function(e) {
		var ok = decrypt_to_file(file.name, e.target.result, passwd);
		if (callback!==undefined) { callback(ok); } 
	};
	reader.readAsText(file);
}