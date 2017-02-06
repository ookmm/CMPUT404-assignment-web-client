#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #socket.AF_INLET indicates that we want an IPv4 
        #socket.SOCK_STREAM indicates that we want a TCP socket
        clientSocket.connect((host, port))
        return clientSocket

    def get_code(self, data):
        statusCode = data.split(' ')[1]
        return int(statusCode)

    def get_headers(self,data):
        header = data.split('\r\n\r\n')[0]
        return header

    def get_body(self, data):
        body = data.split('\r\n\r\n')[1]
        return body



    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    
    def GET(self, url, args=None):
        # code = 500
        # body = ""

        parsedUrl = urlparse(url)
        host = parsedUrl.hostname
        path = parsedUrl.path
        port = parsedUrl.port

        header = 'GET {} HTTP/1.1\r\n'\
                'Host: {}\r\n'\
                'Accept: */*\r\n'\
                'Connection: Close\r\n\r\n'.format(path, host)

        if port == None:
            port = 80
        conn = self.connect(host,port)
        conn.sendall(header)

        data = self.recvall(conn)
        code = self.get_code(data)
        body = self.get_body(data)
        print data


        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # code = 500
        # body = ""

        parsedUrl = urlparse(url)
        host = parsedUrl.hostname
        path = parsedUrl.path
        port = parsedUrl.port

        contents = ''
        if args: #it has contents!!
            contents =  urllib.urlencode(args) #encoding these contents
        contentLength = str(len(contents))

        header = 'POST {} HTTP/1.1\r\n'\
                'Host: {}\r\n'\
                'Content-Type: application/x-www-form-urlencoded\r\n'\
                'Content-Length: {}\r\n'\
                'Accept: */*\r\n\r\n'\
                '{}\r\n'.format(path,host,contentLength,contents)


        if port== None:
            port = 80
        conn = self.connect(host,port)
        conn.sendall(header)

        data = self.recvall(conn)
        code = self.get_code(data)
        body = self.get_body(data)

        print data
        return HTTPResponse(code, body)
    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"

    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )    
