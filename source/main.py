#coding:utf-8

import os
import json
import random,math
from flask import Flask, session, request, redirect, render_template, url_for
	
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object('conf.Config')

state = [u"aberto",u"fechado",u"atrasado"]

@app.route('/')
def hello():
	data = []

	j = _get_db()

	for x in j:
		x["category"] = x["id"] % 3:

	category = [u"Iluminação pública",u"Poda de árvore",u"Conservação de vias",u"Estacionamento irregular"]

	for x in j:
		cat_id = math.trunc(random.random()*len(category))

		call_obj = {"call_id":x["id"],"category":category[cat_id],"reference":u"Supermercados Guanabara","call_description":u"Cidadão solicita que seu time passe a vencer no campeonato brasileiro", "street_name":x["rua"],"state":state[x["id"] % 3],"x":x["x"],"y":x["y"]}
		data.append(call_obj)

	template_vars = {"data":data}

	return render_template('index.html',**template_vars)


@app.route('/social_panel/<call_id>')
def social_panel(call_id):
	call_object_id = "http://blink-app.herokuapp.com/call_object/" + call_id
	stateIndex = int(call_id) % 3
	template_vars = {"call_id":call_id,"open_date":"04/03/2013","due_date":"04/03/2013","call_object_id":call_object_id,"category":u"Iluminação","state":state[stateIndex]}	
	
	return render_template('social_panel_template.html',**template_vars)

@app.route('/ws/<call_id>')
def get_call(call_id):
	j = _get_db()


	for x in j:
		if str(x["id"])== str(call_id):			
			return json.dumps( x )

	return "Nao encontrei " + call_id

@app.route('/ws/')
def get_db():
	return json.dumps( _get_db() )

def _get_db():
	return json.load(open("static/data/data.js"),encoding="utf-8");
