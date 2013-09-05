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
from flask import Flask, session, request, redirect, render_template, url_for

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
app.secret_key = "d5X2=!T774/=$z#(c@K3"

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

TYPE_EXCEPTION = 0
TYPE_SUCCESS = 1
TYPE_INFORMATION = 2

class BlinkException(Exception):
    pass

def removeRowFromId(cur,table,id_field,id_value):
    sql = "DELETE FROM " + table + " WHERE " + id_field + "=%s"
    data = (id_value,)

    try:
        cur.execute(sql,data)
    except (psycopg2.ProgrammingError,IndexError,Exception) as ex:
        if type(ex) is psycopg2.ProgrammingError:
            raise BlinkException('removeRow','Table already exist or not found; SQL syntax error; Wrong number of parameter;',ex,{"1":table})
        elif type(ex) is IndexError:
            raise BlinkException('removeRow','Cursor out of bounds.',ex,{"1":table})
        else:
            raise BlinkException('removeRow','Not Identified. Mysterious Error',ex,{"1":table})

#Action response Package
def ARP(pk_type,ex,user_data):
    if pk_type==0:  #Exception        
        ex_obj = {"ex_type":ex.args[0],"ex_info":ex.args[1],"ex_obj":"","ex_extra":ex.args[3]}
        p = {"type":"exception","ex_obj":ex_obj,"user_data":user_data}
    elif pk_type==1:    #Success
        p = {"type":"success","ex_obj":None,"user_data":user_data}
    elif pk_type==2:    #Information
        p = {"type":"information","ex_obj":None,"user_data":user_data}    

    return json.dumps(p)

def insert_user(cur,**a):
    # conn = connect_database()
    # cur = conn.cursor();

    try:
        sql = "SELECT id FROM users WHERE fbid=%s"    
        cur.execute( sql,(a["fbid"],) )        

        if cur.rowcount==0:
            sql = "INSERT INTO users(name,age,city,country,location,gender,fbid,rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
            data = (a["name"],a["age"],a["city"],a["language"],a["gps_location"],a["gender"],a["fbid"],a["rating"])

            cur.execute(sql,data)
            user_id = cur.fetchone()[0]            
        else:
            user_id = cur.fetchone()[0]
    except (psycopg2.ProgrammingError,IndexError,Exception) as inst:
        if type(inst) is psycopg2.ProgrammingError:
            raise BlinkException('Insert_User','Table already exist or not found; SQL syntax error; Wrong number of parameter;',inst,{"1":sql % data})
        elif type(inst) is IndexError:
            raise BlinkException('Insert_User','Cursor is out of bounds',inst,{});
        else:
            raise BlinkException('Insert_User','Not Identified. Mysterious Error',inst,{})

    return user_id

def insert_question(cur,**a):
    # conn = connect_database()
    # cur = conn.cursor();

    try:
        sql = "INSERT INTO activities(name,keywords) VALUES(%s,%s) RETURNING id"
        data = (a["question"],a["keywords"])    

        cur.execute(sql,data)
        return cur.fetchone()[0]    
    except (psycopg2.ProgrammingError,IndexError,Exception) as inst:
        if type(inst) is psycopg2.ProgrammingError:
            raise BlinkException('Insert_Question','Table already exist or not found; SQL syntax error; Wrong number of parameter;',inst,{"1":sql % data})
        elif type(inst) is IndexError:
            raise BlinkException('Insert_Question','Cursor is out of bounds',inst,{});
        else:
            raise BlinkException('Insert_Question','Not Identified. Mysterious Error',inst,{})
    

def insert_request(cur,**a):
    try:
        sql = "INSERT INTO requests(activity_id,type,user_id,status) VALUES(%s,%s,%s,%s) RETURNING id"
        data = (a["activity_id"],a["request_type"],a["user_id"],a["status"])

        cur.execute(sql,data)
        return cur.fetchone()[0]
    except:
        if type(inst) is psycopg2.ProgrammingError:
            raise BlinkException('Insert_Request','Table already exist or not found; SQL syntax error; Wrong number of parameter;',inst,{"1":sql % data})
        elif type(inst) is IndexError:
            raise BlinkException('Insert_Request','Cursor is out of bounds',inst,{});
        else:
            raise BlinkException('Insert_Request','Not Identified. Mysterious Error',inst,{}) 

def insert_international_by_code(cur,**a):

    try:
        sql_0 = "SELECT blinker_id FROM international_users WHERE blinker_id=%s"
        data_0 = (a["blinker_id"],)

        cur.execute(sql_0,data_0)
        if cur.rowcount>0:
            return "EXIST"

        sql_1 = "UPDATE access_code SET used_by=%s, status='U' WHERE access_code=%s"
        data_1 = (a["blinker_id"],a["user_code"])

        sql_2 = "INSERT INTO international_users (blinker_id,document_1_id,document_2_id,contact_1_id,contact_2_id,status) VALUES (%s,%s,%s,%s,%s,%s)"
        data_2 = (a["blinker_id"],a["document_1_id"],a["document_2_id"],a["contact_1_id"],a["contact_2_id"],a["status"])
        
        cur.execute(sql_1,data_1)
        cur.execute(sql_2,data_2)

        return "OK"
    except (psycopg2.ProgrammingError,IndexError,Exception) as inst:
        if type(inst) is psycopg2.ProgrammingError:
            raise BlinkException('Insert_Request','Table already exist or not found; SQL syntax error; Wrong number of parameter;',inst,{"1":sql % data})
        elif type(inst) is IndexError:
            raise BlinkException('Insert_Request','Cursor is out of bounds',inst,{});
        else:
            raise inst

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
        try:
            conn = connect_database()
            cur = conn.cursor()

            #User insert information processing
            locale = request.form["field-locale"]
            if locale!=None:
                language = locale_dict[locale];

            city = request.form["field-location"]        
            if city is None:
                city = "None";            

            birthday_list = request.form["field-birthday"].split("/")    
            birthday = datetime.datetime(int(birthday_list[2]),int(birthday_list[0]),int(birthday_list[1]))                       
            age = (datetime.datetime.now() - birthday).days/365

            user_id = insert_user(cur,name=request.form["field-name"],gender=request.form["field-gender"],fbid=request.form["field-fbid"],age=age,city=city,language=language,gps_location="GPS-Coordinates",rating=0.00)

            if "user_code" in session:
                ret = insert_international_by_code(cur,user_code=session["user_code"],blinker_id=user_id,document_1_id=None,document_2_id=None,contact_1_id=None,contact_2_id=None,status='A')
                session.pop("user_code",None)

            activity_id = insert_question(cur,question=request.form["field-question"],keywords="")
            request_id = insert_request(cur,activity_id=activity_id,request_type=request.form["field-request-type"],status="A",user_id=user_id)
        
            conn.commit()

            t1 = {"table":"requests","id_field":"id","id_value":request_id}
            t2 = {"table":"activities","id_field":"id","id_value":activity_id}
            # t3 = {"table":"users","id_field":"id","id_value":user_id}            
            t4 = {"table":"international_users","id_field":"blinker_id","id_value":user_id}
            l = [t1,t2,t4]
            user_data = {"test_data":l}
            
            return ARP(TYPE_SUCCESS,None,user_data)

        except (BlinkException,Exception) as inst:
            if type(inst) is BlinkException:
                return ARP(TYPE_EXCEPTION,inst,None)  
            else:
                ex = {}
                for i in range(0,len(inst.args)):
                    ex.update( {i:inst.args[i]} )

                return ARP(TYPE_EXCEPTION,BlinkException('Index','Not Identified. Mysterious Error',ex,{}),None)

@app.route('/validate_code', methods=['POST'])
def validate_code():
    try:
        code = request.form["code"]
        query = "SELECT extra_field,status FROM access_code WHERE access_code like %s"

        conn = connect_database()
        cur = conn.cursor();

        cur.execute(query,(code,))
        if cur.rowcount>0:
            row = cur.fetchone()
            if row[1]!='N':
                return ARP(TYPE_INFORMATION,None,{"info":"USED"})
            else:
                session["user_code"] = code
                return ARP(TYPE_SUCCESS,None,None)

        ex = Exception('Validate_Code','Code does not exist',None,{})    
        return ARP(TYPE_EXCEPTION,ex,{"info":"INVALID"})
    except (psycopg2.ProgrammingError,IndexError,Exception) as inst:
        if type(inst) is psycopg2.ProgrammingError:
            ex = Exception('Validate_Code','Table already exist or not found; SQL syntax error; Wrong number of parameter;',inst,{"1":sql % data})
        elif type(inst) is IndexError:
            ex = Exception('Validate_Code','Cursor is out of bounds',inst,{});
        else:
            ex = Exception('Validate_Code','Not Identified. Mysterious Error',inst,{})

        return ARP(TYPE_EXCEPTION,ex,None)

    finally:
        cur.close();
        conn.close();        

@app.route('/rollback', methods=['POST'])
def rollback():
    try:
        conn = connect_database()
        cur = conn.cursor()

        rb_obj = request.form["rollbackObj"]    #It is a list of dictionaries
        rb_obj = json.loads(rb_obj)

        for el in rb_obj:
            removeRowFromId(cur,el["table"],el["id_field"],el["id_value"])

        conn.commit()
    except Exception as ex:
        return ARP(TYPE_EXCEPTION,ex,None) 
    finally:    
        cur.close()
        conn.close()

    return "OK"

@app.route('/call_object/<call_id>')
def call_object(call_id):
    template_vars = {"call_title":"Chamado " + call_id, "call_object_id":call_id}
    return render_template('call_object_template.html',**template_vars)


@app.route('/blog', methods=['GET'])
def blog():
    return render_template("blog.html",CSS_PATH="static/css/", JS_PATH="static/js/", IMG_PATH="static/img/", MOV_PATH="static/mov/")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if app.config.get('FB_APP_ID') and app.config.get('FB_APP_SECRET'):
        app.run(host='0.0.0.0', port=port)
    else:
        print 'Cannot start application without Facebook App Id and Secret set'
