import datetime
import decimal
import psycopg2
from util import BlinkException,BlinkCodeNotExist

'''Classes
ContactModel
DocumentoModel
BlinkModel
BlinkerModel
InternationalBlinkerModel
RequestModel
ActivityModel
AccessCodeModel
CategoryModel
RelatedActivityModel
RelatedCategoryModel
'''

class ContactModel():
    def __init__(self,_number,_type,_status,_id=None):
        data = (_number,_type,_status,_id)
        self.__fill__(data)        

    def __fill__(self,_row):        
        self.number = _row[0]
        self.type = _row[1]
        self.status = _row[2]                
        self.id = _row[3]

    @staticmethod
    def get(cur,_id):
        try:
            sql = "SELECT number,type,status,id FROM contact WHERE id=%s"
            data = (_id,)
            cur.execute(sql,data)
            if cur.rowcount==0:
                return None
            else:
                return ContactModel(*cur.fetchone())
        except psycopg2.Error as inst:
            raise BlinkException('get_contact','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('get_contact','Not Identified.',inst.args,{})    

    @staticmethod
    def exist(cur,_id):
        try:
            sql = "SELECT * FROM contact WHERE id=%s"
            data = (_id,)
            cur.execute(sql,data)
            return cur.rowcount>0            
        except psycopg2.Error as inst:
            raise BlinkException('get_contact','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('get_contact','Not Identified.',inst.args,{})    


    def insert(self,cur,_id=None):
        try:
            if _id==None:
                sql = "INSERT INTO contact(number,type,status) VALUES(%s,%s,%s) RETURNING id"
                data = (self.number,self.type,self.status)
            else:
                sql = "INSERT INTO contact(id,number,type,status) VALUES(%s,%s,%s,%s) RETURNING id"
                data = (_id,self.number,self.type,self.status)                

            cur.execute(sql,data)
            self.id = cur.fetchone()[0]
        except psycopg2.Error as inst:
            raise BlinkException('insert_contact','Database Error',inst.args,{"1":sql % data})
        except IndexError as inst:
            raise BlinkException('insert_contact','Cursor is out of bounds',inst.args,{});
        except Exception as inst:
            raise BlinkException('insert_contact','Not Identified.',inst.args,{})                   

    def update(self,cur):
        try:
            sql = "UPDATE contact SET number=%s,type=%s,status=%s WHERE id=%s"
            data = (self.number,self.type,self.status,self.id)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('update_contact','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('update_contact','Not Identified. Mysterious Error',inst.args,{})       


    def delete(self,cur):
        if self.id==None:
            raise BlinkException('delete_contact','Row not inserted',None,{})        

        try:
            sql = "DELETE FROM contact WHERE id=%s"
            data = (self.id,)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('delete_contact','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('delete_contact','Not Identified. Mysterious Error',inst.args,{})       

class DocumentModel():
    def __init__(self,_number,_type,_country,_id=None):
        data = (_number,_type,_country,_id)
        self.__fill__(data)

    def __fill__(self,row):
        self.number = row[0]
        self.type = row[1]
        self.country = row[2]
        self.id = row[3] 

    @staticmethod
    def get(cur,_id):
        try:
            sql = "SELECT number,type,country,id FROM document WHERE id=%s"
            data = (_id,)
            cur.execute(sql,data)
            if cur.rowcount==0:
                return None
            else:
                return DocumentModel(*cur.fetchone())
        except psycopg2.Error as inst:
            raise BlinkException('get_document','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('get_document','Not Identified. Mysterious Error',inst.args,{})                   

    @staticmethod
    def exist(cur,_id):
        try:
            sql = "SELECT * FROM document WHERE id=%s"
            data = (_id,)
            cur.execute(sql,data)
            return cur.rowcount>0            
        except psycopg2.Error as inst:
            raise BlinkException('get_document','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('get_document','Not Identified.',inst.args,{})   


    def insert(self,cur,_id=None):
        try:
            if _id==None:
                sql = "INSERT INTO document(number,type,country) VALUES(%s,%s,%s) RETURNING id"
                data = (self.number,self.type,self.country)
            else:
                sql = "INSERT INTO document(id,number,type,country) VALUES(%s,%s,%s,%s) RETURNING id"
                data = (_id,self.number,self.type,self.country)

            cur.execute(sql,data)
            self.id = cur.fetchone()[0]
        except psycopg2.Error as inst:
            raise BlinkException('insert_document','Database Error',inst.pgerror,{"1":sql % data})
        except IndexError as inst:
            raise BlinkException('insert_document','Cursor is out of bounds',inst.args,{});
        except Exception as inst:
            raise BlinkException('insert_document','Not Identified. Mysterious Error',inst.args,{})                           

    def update(self,cur):
        try:
            sql = "UPDATE document SET number=%s,type=%s,country=%s WHERE id=%s"
            data = (self.number,self.type,self.country,self.id)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('update_document','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('update_document','Not Identified. Mysterious Error',inst.args,{})       


    def delete(self,cur):
        if self.id==None:
            raise BlinkException('delete_document','Row not inserted',None,{})        
            
        try:
            sql = "DELETE FROM document WHERE id=%s"
            data = (self.id,)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('delete_document','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('delete_document','Not Identified. Mysterious Error',inst.args,{})           

class BlinkModel():
    def __init__(self,_user_1_id,_user_2_id,_activity_id,_status,_comment,_rating,_id=None):
        data = (_user_1_id,_user_2_id,_activity_id,_status,_comment,_rating,_id)
        self.__fill__(data)

    def __fill__(self,_row):
        self.user_1_id = _row[0]
        self.user_2_id = _row[1]
        self.activity_id = _row[2]
        self.status = _row[3]
        self.comment = _row[4]
        self.rating = decimal.Decimal(_row[5])
        self.id = _row[6]

    @staticmethod
    def get(cur,_id):
        try:
            sql = "SELECT user_1_id,user_2_id,activity_id,status,comment,rating,id FROM blink WHERE id=%s"
            data = (_id,)
            cur.execute(sql,data)

            if cur.rowcount==0:
                return None
            else:
                return BlinkModel(*cur.fetchone())
        except psycopg2.Error as inst:
            raise BlinkException('get_blink','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('get_blink','Not Identified. Mysterious Error',inst.args,{})            

    @staticmethod
    def exist(cur,_id):
        try:
            sql = "SELECT * FROM blink WHERE id=%s"
            data = (_id,)
            cur.execute(sql,data)

            return cur.rowcount>0
        except psycopg2.Error as inst:
            raise BlinkException('exist_blink','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('exist_blink','Not Identified. Mysterious Error',inst.args,{})            

    def insert(self,cur,_id=None):
        try:
            if _id==None:
                sql = "INSERT INTO blink(user_1_id,user_2_id,activity_id,status,comment,rating) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id"
                data = (self.user_1_id,
                        self.user_2_id,
                        self.activity_id,
                        self.status,
                        self.comment,
                        self.rating)
            else:
                sql = "INSERT INTO blink(id,user_1_id,user_2_id,activity_id,status,comment,rating) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id"
                data = (_id,
                        self.user_1_id,
                        self.user_2_id,
                        self.activity_id,
                        self.status,
                        self.comment,
                        self.rating)                

            cur.execute(sql,data)
            self.id=cur.fetchone()[0]
        except psycopg2.Error as inst:
            raise BlinkException('insert_blink','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('insert_blink','Not Identified. Mysterious Error',inst.args,{})            

    def update(self,cur):
        try:
            sql = "UPDATE blink SET user_1_id=%s ,user_2_id=%s, activity_id=%s, status=%s, comment=%s, rating=%s WHERE id=%s"
            data = (self.user_1_id,
                    self.user_2_id,
                    self.activity_id,
                    self.status,
                    self.comment,
                    self.rating,
                    self.id)             

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('update_blink','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('update_blink','Not Identified. Mysterious Error',inst.args,{})     

    def delete(self,cur):
        if self.id==None:
            raise BlinkException('delete_blink','Row not inserted',None,{})        
            
        try:
            sql = "DELETE FROM blink where id=%s"
            data = (self.id,)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('delete_blink','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('delete_blink','Not Identified. Mysterious Error',inst.args,{})              

class BlinkerModel():

    def __init__(self,_name,_birthday,_gender,_city,_country,_location,_fbid,_rating,_tcid,_id=None):
        data = (_name,_birthday,_gender,_city,_country,_location,_fbid,_rating,_tcid,_id)      
        self.__fill__(data)   

    def __fill__(self,_row):
        self.name = _row[0]
        self.birthday = _row[1]
        self.gender = _row[2]
        self.city = _row[3]
        self.country = _row[4]
        self.location = _row[5]        
        self.fbid = _row[6]
        self.rating = _row[7]
        self.trust_cloud_id = _row[8]
        self.id = _row[9]

    @staticmethod
    def get(cur,_id):
        try:
            sql = "SELECT name,birthday,gender,city,country,location,fbid,rating,trust_cloud_id,id FROM blinker WHERE id=%s"
            data = (_id,)

            cur.execute(sql,data)
            if cur.rowcount==0:
                return None
            else:
                return BlinkerModel(*cur.fetchone())
        except psycopg2.Error as inst:
            raise BlinkException('get_blinker','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('get_blinker','Not Identified. Mysterious Error',inst.args,{})   

    @staticmethod
    def exist(cur,_id):
        try:
            sql = "SELECT * FROM blinker WHERE id=%s"
            data = (_id,)
            cur.execute(sql,data)

            return cur.rowcount>0
        except psycopg2.Error as inst:
            raise BlinkException('exist_blinker','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('exist_blinket','Not Identified. Mysterious Error',inst.args,{})                

    @staticmethod
    def check_fbid(cur,_fbid):
        try:
            sql = "SELECT id FROM blinker WHERE fbid=%s"    
            data = (_fbid,)

            cur.execute( sql,data )   

            return cur.rowcount==0
        except psycopg2.Error as inst:
            raise BlinkException('Blinker_check_fbid','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('Blinker_check_fbid','Not Identified. Mysterious Error',inst.args,{})			 	

    def insert(self,cur,_id=None):
        try:
            if BlinkerModel.check_fbid(cur,self.fbid):
                if _id==None:
                    sql = "INSERT INTO blinker(name,birthday,gender,city,country,location,fbid,rating,trust_cloud_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
                    data = (self.name,
                            self.birthday,
                            self.gender,
                            self.city,
                            self.country,
                            self.location,
                            self.fbid,
                            self.rating,
                            self.trust_cloud_id)
                else:
                    sql = "INSERT INTO blinker(name,birthday,gender,city,country,location,fbid,rating,trust_cloud_id,id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
                    data = (self.name,
                            self.birthday,
                            self.gender,
                            self.city,
                            self.country,
                            self.location,
                            self.fbid,
                            self.rating,
                            self.trust_cloud_id,
                            _id)                    

                cur.execute(sql,data)            
                self.id = cur.fetchone()[0]            
            else:
                self.id = cur.fetchone()[0]
        except psycopg2.Error as inst:
            raise BlinkException('insert_blinker','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('insert_blinker','Not Identified. Mysterious Error',inst.args,{})     

    def update(self,cur): 
        try:
            sql = "UPDATE blinker SET name=%s,birthday=%s,gender=%s,city=%s,country=%s,location=%s,fbid=%s,rating=%s,trust_cloud_id=%s WHERE id=%s"

            data = (self.name,
                    self.birthday,
                    self.gender,
                    self.city,
                    self.country,
                    self.location,
                    self.fbid,
                    self.rating,
                    self.trust_cloud_id,
                    self.id)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('update_blinker','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('update_blinker','Not Identified. Mysterious Error',inst.args,{})

    def delete(self,cur):
        if self.id==None:
            raise BlinkException('delete_blinker','Row not inserted',None,{})        
            
        try:
            sql = "DELETE FROM blinker WHERE id=%s"
            data = (self.id,)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('delete_blinker','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('delete_blinker','Not Identified. Mysterious Error',inst.args,{})                 
  
class InternationalBlinkerModel():
    def __init__(self,_blinker_id,_document_1_id,_document_2_id,_contact_1_id,_contact_2_id,_status,_id=None):
        data = (_blinker_id,_document_1_id,_document_2_id,_contact_1_id,_contact_2_id,_status,_id)
        self.__fill__( data )

    def __fill__(self,row):
        self.blinker_id = row[0]
        self.document_1_id = row[1]
        self.document_2_id = row[2]
        self.contact_1_id = row[3]
        self.contact_2_id = row[4]
        self.status = row[5]

        self.id = row[6]

    @staticmethod
    def get(cur,_id): 
        try:
            sql = "SELECT * FROM international_blinker WHERE id=%s"
            data = (_id,)

            cur.execute(sql,data)
            if cur.rowcount==0:
                return None
            else:
                return InternationalBlinkerModel(*cur.fetchone())
        except psycopg2.Error as inst:
            raise BlinkException('get_International','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('get_International','Not Identified. Mysterious Error',inst.args,{})


    @staticmethod
    def exist(cur,_id):
        try:
            sql = "SELECT id FROM international_blinker WHERE id=%s"
            data = (_id,)

            cur.execute(sql,data)
            return cur.rowcount>0

        except psycopg2.Error as inst:
            raise BlinkException('exist_International','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('exist_International','Not Identified. Mysterious Error',inst.args,{})

    @staticmethod
    def exist_blinker_id(cur,_blinker_id):
        try:
            sql = "SELECT id FROM international_blinker WHERE blinker_id=%s"
            data = (_blinker_id,)

            cur.execute(sql,data)
            return cur.rowcount>0

        except psycopg2.Error as inst:
            raise BlinkException('exist_blinker_International','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('exist_blinker_International','Not Identified. Mysterious Error',inst.args,{})            

    def delete(self,cur):
        if self.id==None:
            raise BlinkException('delete_international','Row not inserted',None,{})        
            
        try:
            sql = "DELETE FROM international_blinker WHERE id=%s"
            data = (self.id,)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('delete_international','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('delete_international','Not Identified. Mysterious Error',inst.args,{})         

    def update(self,cur): 
        try:
            sql = "UPDATE international_blinker SET document_1_id=%s,document_2_id=%s,contact_1_id=%s,contact_2_id=%s,status=%s WHERE id=%s"

            data = (self.document_1_id,
                    self.document_2_id,
                    self.contact_1_id,
                    self.contact_2_id,
                    self.status,
                    self.id)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('update_International','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('update_International','Not Identified. Mysterious Error',inst.args,{})

    def insert(self,cur):
        try:
            sql = "INSERT INTO international_blinker (blinker_id,document_1_id,document_2_id,contact_1_id,contact_2_id,status) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id"
            data = (self.blinker_id,
                    self.document_1_id,
                    self.document_2_id,
                    self.contact_1_id,
                    self.contact_2_id,
                    self.status)

            cur.execute(sql,data)

            self.id = cur.fetchone()[0]
        except psycopg2.Error as inst:
            raise BlinkException('Insert_International','Database Error',inst.pgerror,{"1":sql % data})
        except IndexError as inst:
            raise BlinkException('Insert_International','Cursor is out of bounds',inst.args,{});
        except Exception as inst:
            raise BlinkException('Insert_International','Not Identified. Mysterious Error',inst.args,{})     	

class RequestModel():
    def __init__(self,_activity_id,_request_type,_status,_user_id,_id=None):
        data = (_activity_id,_request_type,_status,_user_1_id,_id)
        self.__fill__(data)

    def __fill__(self,_row):
        self.activity_id = _row[0]
        self.request_type = _row[1]
        self.status = _row[2]
        self.user_id = _row[3]
        self.id = _row[4] 

    @staticmethod
    def get(cur,_id):
        try:
            sql = "SELECT activity_id,request_type,status,user_id,id FROM request WHERE id=%s"
            data = (_id,)
            cur.execute(sql,data)

            if cur.rowcount==0:
                return None
            else:
                return RequestModel(*cur.fetchone())
        except psycopg2.Error as inst:
            raise BlinkException('get_request','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('get_request','Not Identified. Mysterious Error',inst.args,{})            

    @staticmethod
    def exist(cur,_id):
        try:
            sql = "SELECT * FROM request WHERE id=%s"
            data = (_id,)
            cur.execute(sql,data)

            return cur.rowcount>0
        except psycopg2.Error as inst:
            raise BlinkException('get_request','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('get_request','Not Identified. Mysterious Error',inst.args,{})        


    def update(self,cur): 
        try:
            sql = "UPDATE request SET activity_id=%s, request_type=%s, status=%s, user_id=%s WHERE id=%s"
            data = (self.activity_id,
                    self.request_type,
                    self.status,
                    self.user_id,
                    self.id)             

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('update_request','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('update_request','Not Identified. Mysterious Error',inst.args,{})     


    def insert(self,cur,_id=None):
        try:
            if _id==None:
                sql = "INSERT INTO request(activity_id,type,user_id,status) VALUES(%s,%s,%s,%s) RETURNING id"
                data = (self.activity_id,
                        self.request_type,
                        self.user_id,
                        self.status)
            else:
                sql = "INSERT INTO request(id,activity_id,type,user_id,status) VALUES(%s,%s,%s,%s,%s) RETURNING id"
                data = (_id,
                        self.activity_id,
                        self.request_type,
                        self.user_id,
                        self.status)                

            cur.execute(sql,data)
            self.id = cur.fetchone()[0]
        except psycopg2.Error as inst:
            raise BlinkException('Insert_Request','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('Insert_Request','Not Identified. Mysterious Error',inst.args,{})

    def delete(self,cur):
        if self.id==None:
            raise BlinkException('delete_request','Row not inserted',None,{})        
            
        try:
            sql = "DELETE FROM request where id=%s"
            data = (self.id,)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('delete_request','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('delete_request','Not Identified. Mysterious Error',inst.args,{})          

class ActivityModel():
    def __init__(self,_name,_keyword,_id=None):
        data = (_name,_keyword,_id)
        self.__fill__(data)

    def __fill__(self,_row):
        self.name = _row[0]
        self.keywords = _row[1]
        self.id = _row[2]

    @staticmethod
    def get(cur,_id):
        try:
            sql = "SELECT name,keywords,id FROM activity WHERE id=%s"
            data = (_id,)
            cur.execute(sql,data)

            if cur.rowcount==0:
                return None
            else:
                return ActivityModel(*cur.fetchone())
        except psycopg2.Error as inst:
            raise BlinkException('get_activity','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('get_activity','Not Identified. Mysterious Error',inst.args,{})            

    @staticmethod
    def exist(cur,_id):
        try:
            sql = "SELECT * FROM activity WHERE id=%s"
            data = (_id,)
            cur.execute(sql,data)

            return cur.rowcount>0
        except psycopg2.Error as inst:
            raise BlinkException('get_activity','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('get_activity','Not Identified. Mysterious Error',inst.args,{})        


    def update(self,cur): 
        try:
            sql = "UPDATE activity SET name=%s, keywords=%s WHERE id=%s"
            data = (self.name,
                    self.keywords,
                    self.id)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('update_activity','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('update_activity','Not Identified. Mysterious Error',inst.args,{})    

    def insert(self,cur,_id=None):
        try:
            if _id==None:
                sql = "INSERT INTO activity(name,keywords) VALUES(%s,%s) RETURNING id"
                data = (self.name,
                        self.keywords)    
            else:
                sql = "INSERT INTO activity(name,keywords,id) VALUES(%s,%s,%s) RETURNING id"
                data = (self.name,
                        self.keywords,
                        _id)                    

            cur.execute(sql,data)
            self.id = cur.fetchone()[0]    
        except psycopg2.Error as inst:
            raise BlinkException('Insert_Activity','Database Error',inst.pgerror,{"1":sql % data})
        except IndexError as inst:
            raise BlinkException('Insert_Activity','Cursor is out of bounds',inst.args,{});
        except Exception as inst:
            raise BlinkException('Insert_Activity','Not Identified. Mysterious Error',inst.args,{})

    def delete(self,cur):
        if self.id==None:
            raise BlinkException('delete_activity','Row not inserted',None,{})        
            
        try:
            sql = "DELETE FROM activity WHERE id=%s"
            data = (self.id,)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('delete_activity','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('delete_activity','Not Identified. Mysterious Error',inst.args,{})             

class AccessCodeModel():

    def __init__(self,_access_code,_type,_status,_extra_field,_used_by,_id=None):
        data = (_access_code,_type,_status,_extra_field,_used_by,_id)
        self.__fill__(data)

    def __fill__(self,_row):
        self.access_code = _row[0]
        self.type = _row[1]
        self.status = _row[2]
        self.extra_field = _row[3]
        self.used_by = _row[4]
        self.id = _row[5]

    @staticmethod
    def get(cur,_id): 
        try:
            sql = "SELECT access_code,type,status,extra_field,used_by,id FROM access_code WHERE id=%s"
            data = (_id,)

            cur.execute(sql,data)
            if cur.rowcount==0:
                return None
            else:
                return AccessCodeModel(*cur.fetchone())

        except psycopg2.Error as inst:
            raise BlinkException('get_access','Database Error',inst.pgerror,{"1":sql % data})                               
        except Exception as inst:
            raise BlinkException('get_access','Not Identified. Mysterious Error',inst.args,{}) 


    @staticmethod
    def is_valid(cur,_access_code):
        try:
            sql = "SELECT extra_field,status FROM access_code WHERE access_code like %s"
            data = (_access_code,)

            cur.execute(query,data)
            if cur.rowcount>0:
                row = cur.fetchone()
                if row[1]!='N':
                    return False
                else:
                    return True
            else:
                raise BlinkCodeNotExist(access_code)
        except psycopg2.Error as inst:
            raise BlinkException('is_valid','Database Error',inst.pgerror,{"1":sql % data})
        except BlinkCodeNotExist as inst:
            raise BlinkCodeNotExist('is_valid','Given code doesn`t exist in database',inst.args,{})
        except Exception as inst:
            raise BlinkException('is_valid','Not Identified. Mysterious Error',inst.args,{})

    def insert(self,cur): pass

    def update(self,cur): pass

    def check_code(self,cur):
        try:
            sql = "UPDATE access_code SET used_by=%s, status='U' WHERE access_code=%s"
            data = (self.blinker_id,
                    self.user_code)

            cur.execute(sql,data)
        except psycopg2.Error as inst:
            raise BlinkException('check_code','Database Error',inst.pgerror,{"1":sql % data})
        except Exception as inst:
            raise BlinkException('check_code','Not Identified. Mysterious Error',inst.args,{})

# class CategoryModel():
#     def __init__(self,):        

# class RelatedActivityModel():
#     def __init__(self,):

# class RelatedCategoryModel():
#     def __init__(self,):