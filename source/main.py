#coding:utf-8

import os
import json
import random,math
from flask import Flask, session, request, redirect, render_template, url_for
from flaskext.mysql import MySQL
	
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object('conf.Config')

mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def hello():
	data = []

	category = [u"Iluminação pública",u"Poda de árvore",u"Conservação de vias",u"Estacionamento irregular"]
	street_name = [u"Machado de Assis",u"Fábio Luz",u"Pinheiro Machado",u"Campos Sales",u"Meriti"]
	state = [u"aberto",u"fechado",u"atrasado"]

	for i in range(0,10):
		cat_id = math.trunc(random.random()*len(category))
		str_id = math.trunc(random.random()*len(street_name))
		st_id = math.trunc(random.random()*len(state))

		call_obj = {"call_id":i,"category":category[cat_id],"reference":u"Supermercados Guanabara","call_description":u"Cidadão solicita que seu time passe a vencer no campeonato brasileiro", "street_name":street_name[str_id],"state":state[st_id]}
		data.append(call_obj)

	template_vars = {"data":data}

	return render_template('index.html',**template_vars)


@app.route('/social_panel/<call_id>')
def social_panel(call_id):
	call_object_id = "http://blink-app.herokuapp.com/call_object/" + call_id
	template_vars = {"call_id":call_id,"open_date":"04/03/2013","due_date":"04/03/2013","call_object_id":call_object_id,"category":u"Iluminação","state":"Aguardando"}	
	
	return render_template('social_panel_template.html',**template_vars)

@app.route('/ws/<call_id>')
def get_call(call_id):
	j = json.load(open("static/data/data.js"),encoding="utf-8")


	for x in j:
		if str(x["id"])== str(call_id):			
			return json.dumps( x )

	return "Nao encontrei " + call_id

@app.route('/db')
def db():
	cursor = mysql.get_db().cursor()
	query = ("SELECT * FROM tb_bairro limit 10;")
	cursor.execute(query)	
	for (id_bairro, no_bairro, fl_ativo) in cursor:
  		print(id_bairro, fl_ativo)
	cursor.close()
	return "PORRA"
