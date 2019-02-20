from flask import Flask, render_template, request, url_for, redirect
import os
import json
import urllib3, requests

cookies = requests.cookies.RequestsCookieJar()

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')
	
@app.route('/to_do', methods = ['GET','POST'])
def to_do():
	r = requests.get('https://hunter-todo-api.herokuapp.com/todo-item', cookies = cookies)
	return render_template('to-do.html', items = r.json())

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
			r = requests.post('https://hunter-todo-api.herokuapp.com/auth', data = json.dumps({'username':username}))
			global cookies
			cookies = r.cookies
			if (r.status_code == 200):
				return redirect(url_for('to_do'))
			else:
				return render_template('login.html', lstatus = r.text)
		elif (method == 'register'):
			r = requests.post('https://hunter-todo-api.herokuapp.com/user', data = json.dumps({'username':username}))
			if (r.status_code == 201):
				return render_template('login.html', rstatus = "Register successful. Please Login")
			else:
				return render_template('login.html', rstatus = r.text)
	else:
		return render_template('login.html')
		
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
	