#coding:utf-8

import os
from flask import Flask, session, request, redirect, render_template, url_for
from flaskext.mysql import MySQL
	
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object('conf.Config')

mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def hello():
	return render_template('index.html')


@app.route('/call_object/<call_id>')
def call_object(call_id):
	call_id = "http://blink-app.heroku/blog"
	template_vars = {"call_title":"Chamado Maneiro", "call_object_id":call_id}

	return render_template('call_object_template.html',**template_vars)


@app.route('/social_panel/<call_id>')
def social_panel(call_id):
	call_object_id = "http://blink-app.heroku/blog"
	template_vars = {"call_id":call_id,"call_object_id":call_object_id,"category":u"Iluminação","state":"Aguardando"}
	
	return render_template('social_panel_template.html',**template_vars)

@app.route('/db')
def db():
	cursor = mysql.get_db().cursor()
	query = ("SELECT * FROM tb_bairro limit 10;")
	cursor.execute(query)
	print(cursor);	
	for (id_bairro, no_bairro, fl_ativo) in cursor:
  		print(id_bairro, fl_ativo)
	cursor.close()
	return "PORRA"
