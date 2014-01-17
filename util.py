#coding:utf-8

import json
import psycopg2
import urlparse

class BlinkException(Exception):
    pass

class BlinkCodeNotExist(Exception):	
    pass

class Util(object):
    PATHS_DICT = {"CSS_PATH":"/static/css/", "JS_PATH":"/static/js/", "IMG_PATH":"/static/img/", "MOV_PATH":"/static/mov/"}
    LOCALE_DICT = {"af_ZA":"Afrikaans","ar_AR":"Arabic","az_AZ":"Azerbaijani","be_BY":"Belarusian","bg_BG":"Bulgarian","bn_IN":"Bengali","bs_BA":"Bosnian","ca_ES":"Catalan","cs_CZ":"Czech","cy_GB":"Welsh","da_DK":"Danish","de_DE":"German","el_GR":"Greek","en_GB":"English (UK)","en_PI":"English (Pirate)","en_UD":"English (Upside Down)","en_US":"English (US)","eo_EO":"Esperanto","es_ES":"Spanish (Spain)","es_LA":"Spanish","et_EE":"Estonian","eu_ES":"Basque","fa_IR":"Persian","fb_LT":"Leet Speak","fi_FI":"Finnish","fo_FO":"Faroese","fr_CA":"French (Canada)","fr_FR":"French (France)","fy_NL":"Frisian","ga_IE":"Irish","gl_ES":"Galician","he_IL":"Hebrew","hi_IN":"Hindi","hr_HR":"Croatian","hu_HU":"Hungarian","hy_AM":"Armenian","id_ID":"Indonesian","is_IS":"Icelandic","it_IT":"Italian","ja_JP":"Japanese","ka_GE":"Georgian","km_KH":"Khmer","ko_KR":"Korean","ku_TR":"Kurdish","la_VA":"Latin","lt_LT":"Lithuanian","lv_LV":"Latvian","mk_MK":"Macedonian","ml_IN":"Malayalam","ms_MY":"Malay","nb_NO":"Norwegian (bokmal)","ne_NP":"Nepali","nl_NL":"Dutch","nn_NO":"Norwegian (nynorsk)","pa_IN":"Punjabi","pl_PL":"Polish","ps_AF":"Pashto","pt_BR":"Portuguese (Brazil)","pt_PT":"Portuguese (Portugal)","ro_RO":"Romanian","ru_RU":"Russian","sk_SK":"Slovak","sl_SI":"Slovenian","sq_AL":"Albanian","sr_RS":"Serbian","sv_SE":"Swedish","sw_KE":"Swahili","ta_IN":"Tamil","te_IN":"Telugu","th_TH":"Thai","tl_PH":"Filipino","tr_TR":"Turkish","uk_UA":"Ukrainian","vi_VN":"Vietnamese","zh_CN":"Simplified Chinese (China)","zh_HK":"Traditional Chinese (Hong Kong)","zh_TW":"Traditional Chinese (Taiwan)"}

    TYPE_EXCEPTION = 0
    TYPE_SUCCESS = 1
    TYPE_INFORMATION = 2

    #Action response Package
    def ARP(pk_type,ex,user_data):
        if pk_type==0:  #Exception        
            ex_obj = {"ex_type":ex.args[0],"ex_info":ex.args[1],"ex_msg":ex.args[2],"ex_extra":ex.args[3]}
            p = {"type":"exception","ex_obj":ex_obj,"user_data":user_data}
        elif pk_type==1:    #Success
            p = {"type":"success","ex_obj":None,"user_data":user_data}
        elif pk_type==2:    #Information
            p = {"type":"information","ex_obj":None,"user_data":user_data}    

        return json.dumps(p)       

    def get_age_from_facebook_date(birthday):
        try:
            birthday_list = birthday.split("/")    
            birthday = datetime.datetime(int(birthday_list[2]),int(birthday_list[0]),int(birthday_list[1]))                     
            today = datetime.datetime.now()
    
            age = (today.year - birthday.year)-1
            if today.month >= birthday.month:
                if today.day >= birthday.day:
                    age+=1

            return age
        except IndexError:
            try:
                return int(birthday)        
            except ValueError:
                return None

    def get_db_date_format(date):
        try:
            date = date.split("/")
            return "%s/%s/%s" % (date[2],date[0],date[1])
        except Exception:
            return None


class Database():
    @staticmethod
    def connect_database(DB_URL):
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(DB_URL)

        return psycopg2.connect(
            database=url.path[1:],
            user=url.username,
           password=url.password,
            host=url.hostname,
            port=url.port
        )          