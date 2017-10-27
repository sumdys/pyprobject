
import requests

class cfda():
	"""docstring for cfda"""
	def __init__(self):
		self.session = requests.Session()
		self.url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList'
		
		self.head = {'Accept':'*/*',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
'Connection':'keep-alive',
'Content-Length':'75',
'Content-Type':'application/x-www-form-urlencoded;utf-8',
'Cookie':'JSESSIONID=8ED1167CDB4F426C8C2175A243B7C1B3; JSESSIONID=F4AF142591DC99037A55B623044D6BAC',
'Host':'125.35.6.84:81',
'Origin':'http://125.35.6.84:81',
'Referer':'http://125.35.6.84:81/xk/',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'X-Requested-With':'XMLHttpRequest'}

		self.f = open('dataCFDA.txt','w')

		self.jj = 269

		self.data = {
			'on':'true',
			'page':self.jj,
			'pageSize':'15',
			'productName':'',
			'conditionType':'1',
			'applyname':'',
			'applysn':''
		}



		def get_cfda(self):
			
			html = self.session.post(self.url, data = self.data, headers = self.head)

			while html.status_code == 200 and self.jj != 0:
				
				for ii in range(len(html.json()['list'])):
					cfda_data = html.json()['list'][ii]['EPS_NAME']+'--'+\
					html.json()['list'][ii]['PRODUCT_SN']+'--'+\
					html.json()['list'][ii]['XC_DATE']+'--'+\
					html.json()['list'][ii]['QF_MANAGER_NAME']+'--'+\
					html.json()['list'][ii]['XK_DATE']+'\n'

				self.f.write(cfda_data)

				self.jj = self.jj-1

		def close(self):
			self.f.close()


cfda = cfda()

cfda.get_cfda()

cfda.close()