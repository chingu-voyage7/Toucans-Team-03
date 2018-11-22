from flask import Flask, render_template,redirect,url_for,request,make_response,send_from_directory
from flask_socketio import SocketIO
from IPython import embed
import json
import os
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def get_saved_data():
	try:
		data = json.loads(request.cookies.get('character'))
	except TypeError:
		data = {}
	return data

@app.route('/',methods=['GET', 'POST'])
def index():
	return render_template('index.html', saves=get_saved_data())

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@app.route('/save', methods=['POST'])
def save():
	response = make_response(redirect(url_for('chatroom')))
	data = get_saved_data()
	data.update(dict(request.form.items()))
	response.set_cookie('character', json.dumps(data))
	return response

@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
	return render_template('session.html', saves=get_saved_data())
	

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)