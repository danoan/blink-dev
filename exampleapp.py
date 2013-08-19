# -*- coding: utf-8 -*-

import base64
import os
import os.path
import urllib
import hmac
import json
import hashlib
from base64 import urlsafe_b64decode, urlsafe_b64encode

import requests
from flask import Flask, request, redirect, render_template, url_for

FB_APP_ID = os.environ.get('FACEBOOK_APP_ID')
requests = requests.session()

app_url = 'https://graph.facebook.com/{0}'.format(FB_APP_ID)
FB_APP_NAME = json.loads(requests.get(app_url).content).get('name')
FB_APP_SECRET = os.environ.get('FACEBOOK_SECRET')

import psycopg2
import urlparse

def connect_database():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )    

def oauth_login_url(preserve_path=True, next_url=None):
    fb_login_uri = ("https://www.facebook.com/dialog/oauth"
                    "?client_id=%s&redirect_uri=%s" %
                    (app.config['FB_APP_ID'], get_home()))

    if app.config['FBAPI_SCOPE']:
        fb_login_uri += "&scope=%s" % ",".join(app.config['FBAPI_SCOPE'])
    return fb_login_uri


def simple_dict_serialisation(params):
    return "&".join(map(lambda k: "%s=%s" % (k, params[k]), params.keys()))


def base64_url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip('=')


def fbapi_get_string(path,
    domain=u'graph', params=None, access_token=None,
    encode_func=urllib.urlencode):
    """Make an API call"""

    if not params:
        params = {}
    params[u'method'] = u'GET'
    if access_token:
        params[u'access_token'] = access_token

    for k, v in params.iteritems():
        if hasattr(v, 'encode'):
            params[k] = v.encode('utf-8')

    url = u'https://' + domain + u'.facebook.com' + path
    params_encoded = encode_func(params)
    url = url + params_encoded
    result = requests.get(url).content

    return result


def fbapi_auth(code):
    params = {'client_id': app.config['FB_APP_ID'],
              'redirect_uri': get_home(),
              'client_secret': app.config['FB_APP_SECRET'],
              'code': code}

    result = fbapi_get_string(path=u"/oauth/access_token?", params=params,
                              encode_func=simple_dict_serialisation)
    pairs = result.split("&", 1)
    result_dict = {}
    for pair in pairs:
        (key, value) = pair.split("=")
        result_dict[key] = value
    return (result_dict["access_token"], result_dict["expires"])


def fbapi_get_application_access_token(id):
    token = fbapi_get_string(
        path=u"/oauth/access_token",
        params=dict(grant_type=u'client_credentials', client_id=id,
                    client_secret=app.config['FB_APP_SECRET']),
        domain=u'graph')

    token = token.split('=')[-1]
    if not str(id) in token:
        print 'Token mismatch: %s not in %s' % (id, token)
    return token


def fql(fql, token, args=None):
    if not args:
        args = {}

    args["query"], args["format"], args["access_token"] = fql, "json", token

    url = "https://api.facebook.com/method/fql.query"

    r = requests.get(url, params=args)
    return json.loads(r.content)


def fb_call(call, args=None):
    url = "https://graph.facebook.com/{0}".format(call)
    r = requests.get(url, params=args)
    return json.loads(r.content)



app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object('conf.Config')


def get_home():
    return 'https://' + request.host + '/'


def get_token():

    if request.args.get('code', None):
        return fbapi_auth(request.args.get('code'))[0]

    cookie_key = 'fbsr_{0}'.format(FB_APP_ID)

    if cookie_key in request.cookies:

        c = request.cookies.get(cookie_key)
        encoded_data = c.split('.', 2)

        sig = encoded_data[0]
        data = json.loads(urlsafe_b64decode(str(encoded_data[1]) +
            (64-len(encoded_data[1])%64)*"="))

        if not data['algorithm'].upper() == 'HMAC-SHA256':
            raise ValueError('unknown algorithm {0}'.format(data['algorithm']))

        h = hmac.new(FB_APP_SECRET, digestmod=hashlib.sha256)
        h.update(encoded_data[1])
        expected_sig = urlsafe_b64encode(h.digest()).replace('=', '')

        if sig != expected_sig:
            raise ValueError('bad signature')

        code =  data['code']

        params = {
            'client_id': FB_APP_ID,
            'client_secret': FB_APP_SECRET,
            'redirect_uri': '',
            'code': data['code']
        }

        from urlparse import parse_qs
        r = requests.get('https://graph.facebook.com/oauth/access_token', params=params)
        token = parse_qs(r.content).get('access_token')

        return token

import datetime
paths_dict = {"CSS_PATH":"static/css/", "JS_PATH":"static/js/", "IMG_PATH":"static/img/", "MOV_PATH":"static/mov/"}
locale_dict = {"af_ZA":"Afrikaans","ar_AR":"Arabic","az_AZ":"Azerbaijani","be_BY":"Belarusian","bg_BG":"Bulgarian","bn_IN":"Bengali","bs_BA":"Bosnian","ca_ES":"Catalan","cs_CZ":"Czech","cy_GB":"Welsh","da_DK":"Danish","de_DE":"German","el_GR":"Greek","en_GB":"English (UK)","en_PI":"English (Pirate)","en_UD":"English (Upside Down)","en_US":"English (US)","eo_EO":"Esperanto","es_ES":"Spanish (Spain)","es_LA":"Spanish","et_EE":"Estonian","eu_ES":"Basque","fa_IR":"Persian","fb_LT":"Leet Speak","fi_FI":"Finnish","fo_FO":"Faroese","fr_CA":"French (Canada)","fr_FR":"French (France)","fy_NL":"Frisian","ga_IE":"Irish","gl_ES":"Galician","he_IL":"Hebrew","hi_IN":"Hindi","hr_HR":"Croatian","hu_HU":"Hungarian","hy_AM":"Armenian","id_ID":"Indonesian","is_IS":"Icelandic","it_IT":"Italian","ja_JP":"Japanese","ka_GE":"Georgian","km_KH":"Khmer","ko_KR":"Korean","ku_TR":"Kurdish","la_VA":"Latin","lt_LT":"Lithuanian","lv_LV":"Latvian","mk_MK":"Macedonian","ml_IN":"Malayalam","ms_MY":"Malay","nb_NO":"Norwegian (bokmal)","ne_NP":"Nepali","nl_NL":"Dutch","nn_NO":"Norwegian (nynorsk)","pa_IN":"Punjabi","pl_PL":"Polish","ps_AF":"Pashto","pt_BR":"Portuguese (Brazil)","pt_PT":"Portuguese (Portugal)","ro_RO":"Romanian","ru_RU":"Russian","sk_SK":"Slovak","sl_SI":"Slovenian","sq_AL":"Albanian","sr_RS":"Serbian","sv_SE":"Swedish","sw_KE":"Swahili","ta_IN":"Tamil","te_IN":"Telugu","th_TH":"Thai","tl_PH":"Filipino","tr_TR":"Turkish","uk_UA":"Ukrainian","vi_VN":"Vietnamese","zh_CN":"Simplified Chinese (China)","zh_HK":"Traditional Chinese (Hong Kong)","zh_TW":"Traditional Chinese (Taiwan)"}


@app.route('/', methods=['GET', 'POST'])
def index():
    hd_lang = request.headers["Accept-Language"]
    hd_lang = hd_lang.split(",")[0];
    if request.method == 'GET':
        if hd_lang=="pt-BR":
            paths_dict["portuguese"] = True
            return render_template("teaser_pt_br.html",**paths_dict)
        else:
            return render_template("teaser_en_us.html",**paths_dict)
    else:
        name = request.form["field-name"]
        gender = request.form["field-gender"]
        fbid = request.form["field-fbid"]

        locale = request.form["field-locale"]
        if locale!=None:
            language = locale_dict[locale];
        
        city = request.form["field-location"]        
        if city is None:
            city = "None";            

        birthday_list = request.form["field-birthday"].split("/")    
        birthday = datetime.datetime(int(birthday_list[2]),int(birthday_list[0]),int(birthday_list[1]))                       
        age = (datetime.datetime.now() - birthday).days/365

        gps_location = "GPS-Coordinates"
        rating = 0.00

        conn = connect_database()
        cur = conn.cursor();

        sql_test_user_exist = "SELECT id FROM users WHERE fbid=%s"
        sql_test_user_exist_data = (fbid,)
        cur.execute(sql_test_user_exist,sql_test_user_exist_data)
        if cur.rowcount==0:

            sql_user = "INSERT INTO users(name,age,city,country,location,gender,fbid,rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
            sql_user_data = (name,age,city,language,gps_location,gender,fbid,rating)

            cur.execute(sql_user,sql_user_data)
            user_id = cur.fetchone()[0]            
        else:
            user_id = cur.fetchone()[0]

        question = request.form["field-question"]
        keywords = ""

        sql_activity = "INSERT INTO activities(name,keywords) VALUES(%s,%s) RETURNING id"
        sql_activity_data = (question,keywords)

        request_type = request.form["field-request-type"]
        status = "A" #Available,Waiting,Finished
        
        try:
            cur.execute(sql_activity,sql_activity_data)
            activity_id = cur.fetchone()[0]

            sql_request = "INSERT INTO requests(activity_id,type,user_id,status) VALUES(%s,%s,%s,%s) RETURNING id"
            sql_request_data = (activity_id,request_type,user_id,status)
            cur.execute(sql_request,sql_request_data)

            conn.commit()

            return "OK"
        except:
            return "ERRO"
        finally:
            cur.close()
            conn.close()



@app.route('/blog', methods=['GET'])
def blog():
    return render_template("blog.html",CSS_PATH="static/css/", JS_PATH="static/js/", IMG_PATH="static/img/", MOV_PATH="static/mov/")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if app.config.get('FB_APP_ID') and app.config.get('FB_APP_SECRET'):
        app.run(host='0.0.0.0', port=port)
    else:
        print 'Cannot start application without Facebook App Id and Secret set'
