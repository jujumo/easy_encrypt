SET infile=%1
start openssl aes-256-cbc -d -base64 -in %infile% -out %infile:~0,-9%
