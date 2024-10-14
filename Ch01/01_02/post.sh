#!/bin/bash

nc httpbin.org 80 <<EOF
POST /events HTTP/1.1
Host: httpbin.org
Connection: close
Content-Type: application/json
Content-Length: 75

{
  "login": "elliot",
  "action": "read",
  "uri": "file:///etc/passwd"
}
EOF
