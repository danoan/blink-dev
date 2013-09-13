import json
import psycopg2
import urlparse

class BlinkException(Exception):
    pass

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

def test_database(DB_URL):
    with connect_database(DB_URL) as conn:
        with conn.cursor() as cur:
            sql="Select name from activities where id = %s"
            cur.execute(sql,(12,))

            if cur.rowcount>0:
                row = cur.fetchone()
                return row[0]        

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
