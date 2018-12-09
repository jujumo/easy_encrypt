SET infile=%1
start openssl aes-256-cbc -e -base64 -md md5 -salt -in %infile% -out %infile%.enc