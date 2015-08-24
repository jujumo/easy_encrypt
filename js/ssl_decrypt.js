
function decrypt(){
	name = $( "#loggin").val();
	passwd = $( "#password").val();
	// Load encrypted data file
	var stringData = $.ajax({
					url: name + ".html.cyph.txt",
					async: false
				 }).responseText;
	// remove '\n' from message
	stringData = stringData.replace(/\r?\n|\r/g, "");
	// decrypt message
	var de = CryptoJS.AES.decrypt(stringData, passwd, {keySize: 256/32});
	// decode content into UTF-8
	var content = (de.toString(CryptoJS.enc.Utf8));
	// display content
	var newDoc = document.open("text/html", "replace");
	newDoc.write(content);
	newDoc.close();
}

$(function(){
    $(this).find('input').keypress(function(e){
        if(e.which == 10 || e.which == 13) {
            decrypt();
        }
    });
});