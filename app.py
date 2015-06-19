from flask import Flask
from flask import request, render_template, redirect
from pymongo import MongoClient
from datetime import datetime

import random
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app)

app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'shortner'

mClient = MongoClient('localhost',27017)
collection = mClient['shortner']['shortner']


@app.route('/', methods=['GET','POST'])
def index():
	if request.method=='GET':
		return render_template('index.html')
	else:
		if request.method=='POST':
			long_url = request.form['long_url']
			date_time = datetime.utcnow()
			put=False
			short=''
			message=''
			while not put:
				short = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(5))
				doc_to_insert = {
				'_id': short,
				'longUrl': long_url,
				'date': date_time
				}
				try:
					collection.insert(doc_to_insert)
					message='200 OK'
					put=True
				except:
					continue
			
			try:
				return render_template('shorten.html', short=short)
			except:
				return ''''ret_msg = {
			'message': message, 
			'shorturl': short
			}'''


@app.route('/<theurl>', methods=['GET'])
def shorten(theurl):
	if request.method=="GET":
		if theurl:
			entry = collection.find_one({'_id': theurl})
			if entry:
				long_url = entry['longUrl']
				return redirect(long_url, 301)
			else:
				abort(404)
		else:
			return redirect('/')	

if __name__ == '__main__':
	app.run()