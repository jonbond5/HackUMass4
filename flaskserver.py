#!/usr/bin/env python2
from flask import Flask, render_template, Response, url_for
import socket
import struct
from twilio.rest import TwilioRestClient
from twilio import twiml

account_sid = "AC3b2a8665742df65778decd8ed7957942"
auth_token = "37bffc94c2a8b01f368c8649c9949d98"

client = TwilioRestClient(account_sid,auth_token)

jon_number = "+15085582233"
jon_prov_number = "+17743570805"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(connection):
    while True:
        img = readImg(connection)
        if img == "":
       	    break
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
    return

def readImg(connection):
    fp = connection.makefile('rb')
    image_len = struct.unpack('<L', fp.read(struct.calcsize('<L')))[0]

    if image_len <= 0:
        return ""
    else:
        return fp.read(image_len)
    
@app.route('/video_feed')
def video_feed():
    global server_socket, connection
    if server_socket == None:
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', 8003))
        server_socket.listen(0)
        connection, _ = server_socket.accept()
        send_call(jon_number,jon_prov_number)
    return Response(gen(connection),
            mimetype='multipart/x-mixed-replace; boundary=frame')

def send_text():
    client.messages.create(
        to="+19786607877",
        from_="+17743570805",
        body="Hi there")
    return

@app.route('/outbound',methods=['POST'])
def outbound():
    response = twiml.Response()
    response.say("          Officer in danger, allocating and dispatching backup to their location.  I repeat: officer in danger, allocating and dispatching backup to their location.",voice='alice')
    return str(response)

def send_call(to_number,from_number):
    call = client.calls.create(
        to=to_number,
        from_=from_number,
        url="http://52.90.176.100/outbound")
    print call.sid

print 'Attempting call'
print 'Done'
server_socket = None
connection = None

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
    #try:
    #    app.run(host='0.0.0.0')
    #except IOError:
    #    pass
