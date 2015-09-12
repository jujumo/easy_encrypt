function read_file_from_url(filename) {
	var content = $.ajax({
					url: filename,
					async: false
				 }).responseText;
	return content;
}

function read_file_from_user(file_selector_id) {
	input = document.getElementById(file_selector_id);
	if (!input) {
		alert("Um, couldn't find the fileinput element.");
	}
	else if (!input.files) {
		alert("This browser doesn't seem to support the `files` property of file inputs.");
	}
	else if (!input.files[0]) {
		alert("Please select a file before clicking 'Load'");               
	}
	else {
		file = input.files[0];
			fr = new FileReader();
			fr.onload = function(e) {
				content = e.target.result;
				return content;
			};
		  //fr.readAsText(file);
		  fr.readAsDataURL(file);
	}
}

function write_file_to_user(filename, content) {
	var element = document.createElement('a');
	element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
	//element.setAttribute('href', 'data:text/plain;charset=utf-8,' + content);
	element.setAttribute('download', filename);
	element.style.display = 'none';
	document.body.appendChild(element);
	element.click();
	document.body.removeChild(element);
}
