#coding:utf-8

from conf import Config
from util import Util
from util import Database as db
from models import *

from flask import session, redirect, render_template, url_for

def main(request,lang):
    if request.method == 'GET':
        Util.PATHS_DICT["portuguese"] = (lang=="pt")
        Util.PATHS_DICT["DEBUG"] = Config.DEBUG

        page = "teaser_%s.html" % (lang,)

        return render_template(page,**Util.PATHS_DICT)         
    else:

        try:
            conn = db.connect_database(Config.DATABASE_URL)
            cur = conn.cursor()

            birthday = Util.get_db_date_format( request.form["field-birthday"] )

            country = request.form["field-locale"]
            if country!=None:
                country = Util.LOCALE_DICT[country];


            bm = BlinkerModel( _name=request.form["field-name"],
                            _birthday=birthday,
                            _gender=request.form["field-gender"],
                            _city=request.form["field-location"],
                            _country=country,
                            _location="GPS-Coordinates",
                            _fbid=request.form["field-fbid"],
                            _rating=decimal.Decimal(0.00),
                            _tcid=None)
            bm.insert(cur)  

            if "user_code" in session:
                ibm = InternationalBlinkerModel(_blinker_id=bm.id,
                                                _document_1_id=None,
                                                _document_2_id=None,
                                                _contact_1_id=None,
                                                _contact_2_id=None,
                                                _status='A')

                if InternationalBlinkerModel.exist_blinker_id(cur,ibm.blinker_id):
                    raise BlinkException("exception","nothing","This user is already an International Blinker",None)

                acm = AccessCodeModel.get_w_access_code(cur,session["user_code"])
                acm.check_code(cur,ibm.blinker_id)

                ibm.insert(cur)
                session.pop("user_code",None)

            am = ActivityModel( _name=request.form["field-question"],
                                _keywords="")
            am.insert(cur)

            rm = RequestModel(  _activity_id=am.id,
                                _type=request.form["field-request-type"],
                                _status="A",
                                _user_id=bm.id)

            rm.insert(cur)
            conn.commit()
            
            return Util.ARP(Util.TYPE_SUCCESS,None,None)

        except BlinkException as inst:
            return Util.ARP(Util.TYPE_EXCEPTION,inst,None)  
        except Exception as inst:
            return Util.ARP(Util.TYPE_EXCEPTION,
                            BlinkException('main','Not Identified',inst.args,{}),
                            None)	

def validate_code(request):
    try:
        conn = db.connect_database(Config.DATABASE_URL)
        cur = conn.cursor();

        if AccessCodeModel.is_valid(cur,_access_code=request.form["code"]):
            session["user_code"] = request.form["code"]
            return Util.ARP(Util.TYPE_SUCCESS,None,None)            
        else:
            return Util.ARP(Util.TYPE_INFORMATION,None,{"info":"USED"})

    except BlinkCodeNotExist as inst:
        return Util.ARP(Util.TYPE_EXCEPTION,inst,{"info":"INVALID"})
    except BlinkException as inst:
        return Util.ARP(Util.TYPE_EXCEPTION,inst,None)  
    finally:
        cur.close();
        conn.close();      
