# -*- coding: utf-8 -*-

import os
import os.path

import requests
import recruit,blog,app
from flask import Flask, session, request, redirect, render_template, url_for

requests = requests.session()

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object('conf.Config')


'''
This is the very first procedure executed by the system in any
page of the system. It checks the language of the current language
of user's browser and render the appropriate page
'''
@app.route('/main',methods=['GET'])
@app.route('/teaser',methods=['GET'])
@app.route('/blog',methods=['GET'])
@app.route('/app',methods=['GET'])
@app.route('/',methods=['GET'])
def set_language():
    hd_lang = request.headers["Accept-Language"]
    hd_lang = hd_lang.split(",")[0]; 

    path = request.path
    if len(path)==1:
        path = ""

    if hd_lang.find("pt")>=0:
        return redirect("pt" + path)
    else:
        return redirect("en" + path)

@app.route('/<lang>/blog', methods=['GET'])
@app.route('/<lang>/blog/<page>', methods=['GET'])
def blog_main(lang,page=None):
    return blog.main(request,lang,page)

@app.route('/<lang>/app', methods=['GET'])
@app.route('/<lang>/app/<page>', methods=['GET'])    
def app_main(lang,page=None):
    return app.main(request,lang,page)


@app.route('/<lang>', methods=['GET','POST'])
def recruit_main(lang):       
    return recruit.main(request,lang)

@app.route('/validate_code', methods=['POST'])
def recruit_validate_code():
    return recruit.validate_code(request)  

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)  
