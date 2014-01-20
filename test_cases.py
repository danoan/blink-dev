#coding:utf-8

import unittest
import decimal
from util import Database as db
from models import *
from conf import Config

#ContactModel Test

class CMBaseTest(unittest.TestCase):
	def setUp(self):
		self.conn = db.connect_database(Config.DATABASE_URL)
		self.cur = self.conn.cursor()		
		self.cm = ContactModel('1234-5678',1,'B')

	def tearDown(self):
		try:
			if self.cm.id!=None:
				self.cm.delete(self.cur)				
				self.conn.commit()
		finally:
			self.conn.close()
			self.cur.close()

class ContactModelTestCase(CMBaseTest):
	def test_A_instantiation(self):
		assert self.cm.number=='1234-5678'
		assert self.cm.type==1
		assert self.cm.status=='B'

	def test_B_insert(self):
		self.cm.insert(self.cur)
		self.conn.commit()
		assert self.cm.id!=None

	def test_C_exist(self):
		self.cm.insert(self.cur)
		self.conn.commit()
		assert self.cm.exist(self.cur,self.cm.id)==True

	def test_D_get(self):
		self.cm.insert(self.cur)
		self.conn.commit()

		cm_get = ContactModel.get(self.cur,self.cm.id)

		assert cm_get.number==self.cm.number
		assert cm_get.type==self.cm.type
		assert cm_get.status==self.cm.status
		assert cm_get.id==self.cm.id

	def test_E_update(self):
		self.cm.insert(self.cur)
		self.conn.commit()

		self.cm = ContactModel.get(self.cur,self.cm.id)
		self.cm.number = "9876-5432"
		self.cm.type = 2
		self.cm.status = "D"

		self.cm.update(self.cur)

		cm_get = ContactModel.get(self.cur,self.cm.id)
		assert cm_get.number==self.cm.number
		assert cm_get.type==self.cm.type
		assert cm_get.status==self.cm.status
		assert cm_get.id==self.cm.id

def run_CM_test_suite():
	suite = unittest.makeSuite(ContactModelTestCase,'test')
	runner = unittest.TextTestRunner()
	runner.run(suite)


#DocumentModel Test

class DMBaseTest(unittest.TestCase):
	def setUp(self):
		self.conn = db.connect_database(Config.DATABASE_URL)
		self.cur = self.conn.cursor()		
		self.dm = DocumentModel('1234-5678',1,'Brazil')

	def tearDown(self):
		try:
			if self.dm.id!=None:
				self.dm.delete(self.cur)				
				self.conn.commit()
		finally:
			self.conn.close()
			self.cur.close()

class DocumentModelTestCase(DMBaseTest):
	def test_A_instantiation(self):
		assert self.dm.number=='1234-5678'
		assert self.dm.type==1
		assert self.dm.country=='Brazil'

	def test_B_insert(self):
		self.dm.insert(self.cur)
		self.conn.commit()
		assert self.dm.id!=None

	def test_C_exist(self):
		self.dm.insert(self.cur)
		self.conn.commit()
		assert self.dm.exist(self.cur,self.dm.id)==True

	def test_D_get(self):
		self.dm.insert(self.cur)
		self.conn.commit()

		dm_get = DocumentModel.get(self.cur,self.dm.id)

		assert dm_get.number==self.dm.number
		assert dm_get.type==self.dm.type
		assert dm_get.country==self.dm.country
		assert dm_get.id==self.dm.id

	def test_E_update(self):
		self.dm.insert(self.cur)
		self.conn.commit()

		self.dm = DocumentModel.get(self.cur,self.dm.id)
		self.dm.number = "9876-5432"
		self.dm.type = 2
		self.dm.country = "Argentina"

		self.dm.update(self.cur)

		dm_get = ContactModel.get(self.cur,self.dm.id)
		assert dm_get.number==self.dm.number
		assert dm_get.type==self.dm.type
		assert dm_get.country==self.dm.country
		assert dm_get.id==self.dm.id

def run_DM_test_suite():
	suite = unittest.makeSuite(ContactModelTestCase,'test')
	runner = unittest.TextTestRunner()
	runner.run(suite)	


#BlinkModel Test

class BMBaseTest(unittest.TestCase):
	def setUp(self):
		self.conn = db.connect_database(Config.DATABASE_URL)
		self.cur = self.conn.cursor()				
		self.bm = BlinkModel(2001,2002,2003,'A','Muito Bom',decimal.Decimal(9.5))

	def tearDown(self):
		try:
			if self.bm.id!=None:
				self.bm.delete(self.cur)				
				self.conn.commit()
		finally:
			self.conn.close()
			self.cur.close()

class BlinkModelTestCase(BMBaseTest):
	def test_A_instantiation(self):
		assert self.bm.user_1_id==2001
		assert self.bm.user_2_id==2002
		assert self.bm.activity_id==2003
		assert self.bm.status=='A'
		assert self.bm.comment=='Muito Bom'
		assert self.bm.rating==decimal.Decimal(9.5)

	def test_B_insert(self):
		self.bm.insert(self.cur)
		self.conn.commit()
		assert self.bm.id!=None

	def test_C_exist(self):
		self.bm.insert(self.cur)
		self.conn.commit()
		assert self.bm.exist(self.cur,self.bm.id)==True

	def test_D_get(self):
		self.bm.insert(self.cur)
		self.conn.commit()

		bm_get = BlinkModel.get(self.cur,self.bm.id)

		assert bm_get.user_1_id==self.bm.user_1_id
		assert bm_get.user_2_id==self.bm.user_2_id
		assert bm_get.activity_id==self.bm.activity_id
		assert bm_get.status==self.bm.status
		assert bm_get.comment==self.bm.comment
		assert bm_get.rating==self.bm.rating

	def test_E_update(self):
		self.bm.insert(self.cur)
		self.conn.commit()

		self.bm = BlinkModel.get(self.cur,self.bm.id)
		self.bm.user_1_id = 2002
		self.bm.user_2_id = 2001
		self.bm.activity_id = 2004
		self.bm.status = 'B'
		self.bm.comment = "Ruim Bacarai"
		self.bm.rating = decimal.Decimal(6.7)

		self.bm.update(self.cur)
		self.conn.commit()

		bm_get = BlinkModel.get(self.cur,self.bm.id)

		assert bm_get.user_1_id==self.bm.user_1_id
		assert bm_get.user_2_id==self.bm.user_2_id
		assert bm_get.activity_id==self.bm.activity_id
		assert bm_get.status==self.bm.status
		assert bm_get.comment==self.bm.comment
		assert bm_get.rating==self.bm.rating		

def run_BM_test_suite():
	try:
		conn = db.connect_database(Config.DATABASE_URL)
		cur = conn.cursor()		

		b1 = BlinkerModel("Testivaldo","2013/01/16","M", "Teste City","Testelandia","23 16 143","91846273",7.8,None)
		b2 = BlinkerModel("Testivaldo Junior","2013/01/26","F", "Testelopolis","Pais dos Testes","29 41 09","1763301",8.5,None)

		b1.insert(cur,2001)
		b2.insert(cur,2002)

		a1 = ActivityModel("Atividade Teste","Teste, Esporte, Educação")
		a2 = ActivityModel("Atividade Testeita","Divertido, Cinema, Social")

		a1.insert(cur,2003)
		a2.insert(cur,2004)

		conn.commit()

		suite = unittest.makeSuite(BlinkModelTestCase,'test')
		runner = unittest.TextTestRunner()
		runner.run(suite)
	except Exception as inst:
		raise inst
	finally:
		b1.delete(cur)
		b2.delete(cur)

		a1.delete(cur)
		a2.delete(cur)

		conn.commit()
		cur.close()
		conn.close()


#BlinkerModel

class BKRBaseTest(unittest.TestCase):
	def setUp(self):
		self.conn = db.connect_database(Config.DATABASE_URL)
		self.cur = self.conn.cursor()
		self.bkr = BlinkerModel("Mr. Capoeira",datetime.date(2013,12,31),"M","Rio de Janeiro","Brasil","GPS","9012389",decimal.Decimal(9.3),"9128472")

	def tearDown(self):
		try:
			if self.bkr.id!=None:
				self.bkr.delete(self.cur)
				self.conn.commit()
		finally:
			self.conn.close()
			self.cur.close()


class BlinkerModelTestCase(BKRBaseTest):

	def test_A_instantiation(self):
		assert self.bkr.name=="Mr. Capoeira"
		assert self.bkr.birthday==datetime.date(2013,12,31)
		assert self.bkr.gender=="M"
		assert self.bkr.city=="Rio de Janeiro"
		assert self.bkr.country=="Brasil"
		assert self.bkr.location=="GPS"
		assert self.bkr.fbid=="9012389"
		assert self.bkr.rating==decimal.Decimal(9.3)
		assert self.bkr.trust_cloud_id=="9128472"	

	def test_B_insert(self):
		self.bkr.insert(self.cur)
		self.conn.commit()
		assert self.bkr.id!=None

	def test_C_exist(self):
		self.bkr.insert(self.cur)
		self.conn.commit()
		assert BlinkerModel.exist(self.cur,self.bkr.id)

	def test_D_get(self):
		self.bkr.insert(self.cur)
		bkr_get = BlinkerModel.get(self.cur,self.bkr.id)

		assert self.bkr.name==bkr_get.name
		assert self.bkr.birthday==bkr_get.birthday
		assert self.bkr.gender==bkr_get.gender
		assert self.bkr.city==bkr_get.city
		assert self.bkr.country==bkr_get.country
		assert self.bkr.location==bkr_get.location
		assert self.bkr.fbid==bkr_get.fbid
		assert self.bkr.rating==bkr_get.rating
		assert self.bkr.trust_cloud_id==bkr_get.trust_cloud_id

	def test_E_update(self):
		self.bkr.insert(self.cur)
		
		
		self.bkr.name = "Mr. Capoeira Boladao"
		self.bkr.birthday = datetime.date(2014,01,26)
		self.bkr.gender = "F"
		self.bkr.city = "Manaus"
		self.bkr.country = "Norway"
		self.bkr.location = "GPSSS"
		self.bkr.fbid = "123123213"
		self.bkr.rating = decimal.Decimal(8.1)
		self.bkr.trust_cloud_id = "u9r89303"

		self.bkr.update(self.cur)
		self.conn.commit()

		bkr_get = BlinkerModel.get(self.cur,self.bkr.id)
	
		assert self.bkr.name==bkr_get.name
		assert self.bkr.birthday==bkr_get.birthday
		assert self.bkr.gender==bkr_get.gender
		assert self.bkr.city==bkr_get.city
		assert self.bkr.country==bkr_get.country
		assert self.bkr.location==bkr_get.location
		assert self.bkr.fbid==bkr_get.fbid
		assert self.bkr.rating==bkr_get.rating
		assert self.bkr.trust_cloud_id==bkr_get.trust_cloud_id

	def test_F_check_fbid(self):
		self.bkr.insert(self.cur)
		self.conn.commit()

		assert BlinkerModel.check_fbid(self.cur,self.bkr.fbid)!=None

def run_BKR_test_suite():
	suite = unittest.makeSuite(BlinkerModelTestCase,"test")
	runner = unittest.TextTestRunner()
	runner.run(suite)

#InternationalBlinkerModel

class IBMBaseTest(unittest.TestCase):
	def setUp(self):
		self.conn = db.connect_database(Config.DATABASE_URL)
		self.cur = self.conn.cursor()		
		self.ibm = InternationalBlinkerModel(32,1,2,1,2,'A')

	def tearDown(self):
		try:
			if self.ibm.id!=None:
				self.ibm.delete(self.cur)				
				self.conn.commit()
		finally:
			self.conn.close()
			self.cur.close()

class InternationalBlinkerModelTestCase(IBMBaseTest):
	def test_A_instantiation(self):
		assert self.ibm.blinker_id == 32
		assert self.ibm.document_1_id == 1
		assert self.ibm.document_2_id == 2
		assert self.ibm.contact_1_id == 1
		assert self.ibm.contact_2_id == 2
		assert self.ibm.status == 'A'

	def test_B_insert(self):
		self.ibm.insert(self.cur)
		assert self.ibm.id != None

	def test_C_exist(self):
		self.ibm.insert(self.cur)
		self.conn.commit()
		assert InternationalBlinkerModel.exist(self.cur,self.ibm.id)==True

	def test_D_exist_blinker_id(self):
		self.ibm.insert(self.cur)
		self.conn.commit()
		assert InternationalBlinkerModel.exist_blinker_id(self.cur,self.ibm.blinker_id)==True		

	def test_E_get(self):
		self.ibm.insert(self.cur)
		self.conn.commit()
		self.ibm_get = InternationalBlinkerModel.get(self.cur,self.ibm.id)

		assert self.ibm.blinker_id == self.ibm_get.blinker_id
		assert self.ibm.document_1_id == self.ibm_get.document_1_id
		assert self.ibm.document_2_id == self.ibm_get.document_2_id
		assert self.ibm.contact_1_id == self.ibm_get.contact_1_id
		assert self.ibm.contact_2_id == self.ibm_get.contact_2_id
		assert self.ibm.status == self.ibm_get.status
		assert self.ibm.id == self.ibm_get.id

	def test_F_update(self):
		self.ibm.insert(self.cur)
		self.conn.commit()

		self.ibm.contact_1_id = 40
		self.ibm.contact_2_id = 41
		self.ibm.document_1_id = 50
		self.ibm.document_2_id = 51		
		self.ibm.status = 'A'

		self.ibm.update(self.cur)
		self.conn.commit()

		self.ibm_get = InternationalBlinkerModel.get(self.cur,self.ibm.id)
		
		assert self.ibm.blinker_id == self.ibm_get.blinker_id
		assert self.ibm.document_1_id == self.ibm_get.document_1_id
		assert self.ibm.document_2_id == self.ibm_get.document_2_id
		assert self.ibm.contact_1_id == self.ibm_get.contact_1_id
		assert self.ibm.contact_2_id == self.ibm_get.contact_2_id
		assert self.ibm.status == self.ibm_get.status
		assert self.ibm.id == self.ibm_get.id		

def run_IBM_test_suite():
	try:
		conn = db.connect_database(Config.DATABASE_URL)
		cur = conn.cursor()		

		c1 = ContactModel("1234","1","A")
		c2 = ContactModel("5678","2","B")
		c40 = ContactModel("1234","1","A")
		c41 = ContactModel("5678","2","B")	

		d1 = DocumentModel("089","1","A")
		d2 = DocumentModel("112","2","B")
		d50 = DocumentModel("089","1","A")
		d51 = DocumentModel("112","2","B")

		c1.insert(cur,"1")
		c2.insert(cur,"2")
		c40.insert(cur,"40")
		c41.insert(cur,"41")

		d1.insert(cur,"1")
		d2.insert(cur,"2")
		d50.insert(cur,"50")
		d51.insert(cur,"51")

		conn.commit()

		suite = unittest.makeSuite(InternationalBlinkerModelTestCase,'test')
		runner = unittest.TextTestRunner()
		runner.run(suite)
	except Exception as inst:
		raise inst
	finally:
		c1.delete(cur)
		c2.delete(cur)
		c40.delete(cur)
		c41.delete(cur)

		d1.delete(cur)
		d2.delete(cur)
		d50.delete(cur)
		d51.delete(cur)

		conn.commit()


#RequestModel

class REQBaseTest(unittest.TestCase):
	def setUp(self):
		self.conn = db.connect_database(Config.DATABASE_URL)
		self.cur = self.conn.cursor()
		self.req = RequestModel(2000,0,"A",100)

	def tearDown(self):
		try:
			if self.req.id!=None:
				self.req.delete(self.cur)
				self.conn.commit()
		finally:
			self.conn.close()
			self.cur.close()

class RequestModelTestCase(REQBaseTest):

	def test_A_instantiation(self):
		assert self.req.activity_id==2000
		assert self.req.type==0
		assert self.req.status=="A"
		assert self.req.user_id==100

	def test_B_insert(self):
		self.req.insert(self.cur)
		self.conn.commit()
		assert self.req.id!=None

	def test_C_exist(self):
		self.req.insert(self.cur)
		self.conn.commit()
		assert RequestModel.exist(self.cur,self.req.id)

	def test_D_get(self):
		self.req.insert(self.cur)
		req_get = RequestModel.get(self.cur,self.req.id)

		assert self.req.activity_id==req_get.activity_id
		assert self.req.type==req_get.type
		assert self.req.status==req_get.status
		assert self.req.user_id==req_get.user_id

	def test_E_update(self):
		self.req.insert(self.cur)
		
		self.req.activity_id = 2001
		self.req.type = 1
		self.req.status = "B"
		self.req.user_id = 101

		self.req.update(self.cur)
		self.conn.commit()

		req_get = RequestModel.get(self.cur,self.req.id)
	
		assert self.req.activity_id==req_get.activity_id
		assert self.req.type==req_get.type
		assert self.req.status==req_get.status
		assert self.req.user_id==req_get.user_id

def run_REQ_test_suite():
	try:
		conn = db.connect_database(Config.DATABASE_URL)
		cur = conn.cursor()		

		b1 = BlinkerModel("Testivaldo","2013/01/16","M", "Teste City","Testelandia","23 16 143","91846273",7.8,None)
		b2 = BlinkerModel("Testivaldo Junior","2013/01/26","F", "Testelopolis","Pais dos Testes","29 41 09","1763301",8.5,None)

		b1.insert(cur,100)
		b2.insert(cur,101)

		a1 = ActivityModel("Atividade Teste","Teste, Esporte, Educação")
		a2 = ActivityModel("Atividade Testeita","Divertido, Cinema, Social")

		a1.insert(cur,2000)
		a2.insert(cur,2001)

		conn.commit()		

		suite = unittest.makeSuite(RequestModelTestCase,"test")
		runner = unittest.TextTestRunner()
		runner.run(suite)
	except Exception as inst:
		raise inst
	finally:
		b1.delete(cur)
		b2.delete(cur)

		a1.delete(cur)
		a2.delete(cur)

		conn.commit()

		conn.close()
		cur.close()


#ActivityModel

class ACTBaseTest(unittest.TestCase):
	def setUp(self):
		self.conn = db.connect_database(Config.DATABASE_URL)
		self.cur = self.conn.cursor()
		self.act = ActivityModel("Dancar Cuduro","Reggaeton, Cuduro, Angolano")

	def tearDown(self):
		try:
			if self.act.id!=None:
				self.act.delete(self.cur)
				self.conn.commit()
		finally:
			self.conn.close()
			self.cur.close()

class ActivityModelTestCase(ACTBaseTest):

	def test_A_instantiation(self):
		assert self.act.name=="Dancar Cuduro"
		assert self.act.keywords=="Reggaeton, Cuduro, Angolano"

	def test_B_insert(self):
		self.act.insert(self.cur)
		self.conn.commit()
		assert self.act.id!=None

	def test_C_exist(self):
		self.act.insert(self.cur)
		self.conn.commit()
		assert ActivityModel.exist(self.cur,self.act.id)

	def test_D_get(self):
		self.act.insert(self.cur)
		act_get = ActivityModel.get(self.cur,self.act.id)

		assert self.act.name==act_get.name
		assert self.act.keywords==act_get.keywords

	def test_E_update(self):
		self.act.insert(self.cur)
		
		self.act.name = "Counting Stars"
		self.act.keywords = "Ruby, OneRepublic"

		self.act.update(self.cur)
		self.conn.commit()

		act_get = ActivityModel.get(self.cur,self.act.id)
	
		assert self.act.name==act_get.name
		assert self.act.keywords==act_get.keywords

def run_ACT_test_suite():
	suite = unittest.makeSuite(ActivityModelTestCase,"test")
	runner = unittest.TextTestRunner()
	runner.run(suite)


#AccessCodeModel

class ACMBaseTest(unittest.TestCase):
	def setUp(self):
		self.conn = db.connect_database(Config.DATABASE_URL)
		self.cur = self.conn.cursor()
		self.acm = AccessCodeModel("aljas023DKD","I","N", "TEST CASE",100)

	def tearDown(self):
		try:
			if self.acm.id!=None:
				self.acm.delete(self.cur)
				self.conn.commit()
		finally:
			self.conn.close()
			self.cur.close()

class AccessCodeModelTestCase(ACMBaseTest):

	def test_A_instantiation(self):
		assert self.acm.access_code=="aljas023DKD"
		assert self.acm.type=="I"
		assert self.acm.status=="N"
		assert self.acm.extra_field=="TEST CASE"
		assert self.acm.used_by==100

	def test_B_insert(self):
		self.acm.insert(self.cur)
		self.conn.commit()
		assert self.acm.id!=None

	def test_C_exist(self):
		self.acm.insert(self.cur)
		self.conn.commit()
		assert AccessCodeModel.exist(self.cur,self.acm.id)

	def test_D_get(self):
		self.acm.insert(self.cur)
		acm_get = AccessCodeModel.get(self.cur,self.acm.id)

		assert self.acm.access_code==acm_get.access_code
		assert self.acm.type==acm_get.type
		assert self.acm.status==acm_get.status
		assert self.acm.extra_field==acm_get.extra_field
		assert self.acm.used_by==acm_get.used_by

	def test_E_update(self):
		self.acm.insert(self.cur)
		
		self.acm.access_code = "kasjdoiahdlka"
		self.acm.type = "S"
		self.acm.status = "U"
		self.acm.extra_field = "Jason Derulo"
		self.acm.used_by = 101

		self.acm.update(self.cur)
		self.conn.commit()

		acm_get = AccessCodeModel.get(self.cur,self.acm.id)
	
		assert self.acm.access_code==acm_get.access_code
		assert self.acm.type==acm_get.type
		assert self.acm.status==acm_get.status
		assert self.acm.extra_field==acm_get.extra_field
		assert self.acm.used_by==acm_get.used_by

	def test_G_is_valid(self):
		self.acm.insert(self.cur)
		assert AccessCodeModel.is_valid(self.cur,self.acm.access_code)

	def test_H_check_code(self):
		self.acm.insert(self.cur)		
		self.acm.check_code(self.cur,100)

		assert self.acm.status=="U"
		assert self.acm.used_by!=None

	def test_I_get_w_access_code(self):
		self.acm.insert(self.cur)
		self.conn.commit()

		assert AccessCodeModel.get_w_access_code(self.cur,self.acm.access_code)!=None

def run_ACM_test_suite():
	try:
		conn = db.connect_database(Config.DATABASE_URL)
		cur = conn.cursor()		

		b1 = BlinkerModel("Testivaldo","2013/01/16","M", "Teste City","Testelandia","23 16 143","91846273",7.8,None)
		b2 = BlinkerModel("Testivaldo Junior","2013/01/26","F", "Testelopolis","Pais dos Testes","29 41 09","1763301",8.5,None)

		b1.insert(cur,100)
		b2.insert(cur,101)

		conn.commit()		

		suite = unittest.makeSuite(AccessCodeModelTestCase,"test")
		runner = unittest.TextTestRunner()
		runner.run(suite)
	except Exception as inst:
		raise inst
	finally:
		b1.delete(cur)
		b2.delete(cur)

		conn.commit()

		conn.close()
		cur.close()	


#CategoryModel

class CATBaseTest(unittest.TestCase):
	def setUp(self):
		self.conn = db.connect_database(Config.DATABASE_URL)
		self.cur = self.conn.cursor()
		self.cat = CategoryModel("Outside Activity")

	def tearDown(self):
		try:
			if self.cat.id!=None:
				self.cat.delete(self.cur)
				self.conn.commit()
		finally:
			self.conn.close()
			self.cur.close()

class CategoryModelTestCase(CATBaseTest):

	def test_A_instantiation(self):
		assert self.cat.name=="Outside Activity"

	def test_B_insert(self):
		self.cat.insert(self.cur)
		self.conn.commit()
		assert self.cat.id!=None

	def test_C_exist(self):
		self.cat.insert(self.cur)
		self.conn.commit()
		assert CategoryModel.exist(self.cur,self.cat.id)

	def test_D_get(self):
		self.cat.insert(self.cur)
		cat_get = CategoryModel.get(self.cur,self.cat.id)

		assert self.cat.name==cat_get.name

	def test_E_update(self):
		self.cat.insert(self.cur)
		
		self.cat.name = "Dance and Sing"

		self.cat.update(self.cur)
		self.conn.commit()

		cat_get = CategoryModel.get(self.cur,self.cat.id)
	
		assert self.cat.name==cat_get.name

def run_CAT_test_suite():
	suite = unittest.makeSuite(CategoryModelTestCase,"test")
	runner = unittest.TextTestRunner()
	runner.run(suite)


def main():
	print "InternationalBlinkerModel Test Suite"
	run_IBM_test_suite()

	print "ContactModel Test Suite"	
	run_CM_test_suite()

	print "DocumentModel Test Suite"	
	run_DM_test_suite()

	print "Blink Model Test Suite"
	run_BM_test_suite()

	print "Blinker Model Test Suite"
	run_BKR_test_suite()	

	print "Request Model Test Suite"
	run_REQ_test_suite()		

	print "Activity Model Test Suite"
	run_ACT_test_suite()		

	print "Access Code Model Test Suite"
	run_ACM_test_suite()	

	print "Category Model Test Suite"
	run_CAT_test_suite()		

if __name__=='__main__':
	main()
