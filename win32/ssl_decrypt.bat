SET infile=%1
start openssl aes-256-cbc -d -base64 -md md5 -salt -in %infile% -out %infile:~0,-4%