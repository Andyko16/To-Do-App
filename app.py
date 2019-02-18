from flask import Flask, render_template, request, url_for, redirect
import os
import json
import urllib3, requests

dict = []
cookies = requests.cookies.RequestsCookieJar()
	
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')
	
@app.route('/to_do', methods = ['GET','POST'])
def to_do():
	getAllToDOItems()
	return render_template('to-do.html', items = dict)

@app.route('/delete/<id>')
def delete(id):
	deleteToDoItem(id)
	return redirect(url_for('to_do'))
	
@app.route('/complete/<id>')
def complete(id):
	completeToDoItem(id)
	return redirect(url_for('to_do'))
		
@app.route('/add', methods = ['POST'])
def add():
	if request.method == 'POST':
		new_item = request.form['item']
		createToDoItem(new_item)
	return redirect(url_for('to_do'))


@app.route('/accounts')
def accounts():
	global cookies
	cookies = requests.cookies.RequestsCookieJar()
	return render_template('login.html')
	
@app.route('/account/<method>', methods = ['POST'])
def account(method):
	if request.method == 'POST':
		username = request.form['username']
		if (method == 'login'):
			login(username)
			return redirect(url_for('to_do'))
		elif (method == 'register'):
			register(username)
			return redirect(url_for('accounts'))
	else:
		return render_template('login.html')

def login(username):
	r = requests.post('https://hunter-todo-api.herokuapp.com/auth', data = json.dumps({'username':username}))
	global cookies
	cookies = r.cookies
	
def register(username):
	r = requests.post('https://hunter-todo-api.herokuapp.com/user', data = json.dumps({'username':username}))

def getAllToDOItems():
	r = requests.get('https://hunter-todo-api.herokuapp.com/todo-item', cookies = cookies)
	global dict
	dict = r.json()
		
def getToDoItem(id):
	url = 'https://hunter-todo-api.herokuapp.com/todo-item/' + id
	r = requests.get(url, cookies = cookies)
	
def createToDoItem(item):
	r = requests.post('https://hunter-todo-api.herokuapp.com/todo-item', data = json.dumps({'content' : item}), cookies = cookies)

def completeToDoItem(id):
	url = 'https://hunter-todo-api.herokuapp.com/todo-item/' + id
	r = requests.put(url, data = json.dumps({'completed' : True}), cookies = cookies)

def deleteToDoItem(id):
	url = 'https://hunter-todo-api.herokuapp.com/todo-item/' + id
	r = requests.delete(url, cookies = cookies)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True)
	