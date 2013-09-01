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
		call_obj = {"call_id":x["id"],"category":x["categoria"],"reference":u"Supermercados Guanabara","call_description":u"Cidadão solicita que seu time passe a vencer no campeonato brasileiro", "street_name":x["rua"],"state":state[x["id"] % 3],"x":x["x"],"y":x["y"]}
		data.append(call_obj)

	template_vars = {"data":data}

	return render_template('index.html',**template_vars)


@app.route('/call_object/<call_id>')
def call_object(call_id):
    template_vars = {"call_title":"Chamado " + call_id, "call_object_id":call_id}
    return render_template('call_object_template.html',**template_vars)

@app.route('/social_panel/<call_id>')
def social_panel(call_id):
	import time

	call_object_id = "http://blink-app.herokuapp.com/call_object/" + call_id


	j = _get_db()
	for x in j:
		if str(x["id"])== str(call_id):			
			r = x
			break

	aberto = time.strptime(r["dt_aberto"], "%Y-%m-%d %H:%M:%S")
	aberto = time.strftime("%d/%m/%Y",aberto)
	fechado = time.strptime(r["dt_fechado"], "%Y-%m-%d %H:%M:%S")
	fechado = time.strftime("%d/%m/%Y",fechado)
	
	bairro = r["bairro"].strip()
	if len(bairro) > 18:
		bairro = bairro[0:16] + "..."

	rua = r["rua"]
	rua_t = r["rua_i"]
	if rua_t:
		rua_t = rua_t.split(",")[-1]
		rua = rua.split(" ")[1:]
		rua = " ".join(rua)
		rua_t = rua_t.strip()
		if rua_t == "R.":
			rua_t = "Rua"
		if rua_t == "Av.":
			rua_t = "Avenida"
		if rua_t == "Trv.":
			rua_t = "Travessa"
		if rua_t == "Etr.":
			rua_t = "Estrada"
	else:
		rua_t = None

	categoria = r["categoria"]
	if len(categoria) > 18:
		categoria = categoria[0:16] + "..."

	stateIndex = int(call_id) % 3

	template_vars = {	"call_id":r["id"],
						"open_date":aberto,
						"due_date":fechado,
						"call_object_id":call_object_id,
						"category":categoria,
						"neighborhood":bairro,
						"street":rua,
						"street_type": rua_t,
						"number":r["num"],
						"state":state[stateIndex]
						}	
	
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
