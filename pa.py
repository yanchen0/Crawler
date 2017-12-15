import requests ,re ,os,subprocess,MySQLdb,hashlib
from bs4 import BeautifulSoup 
import upload_package

down_path=os.path.join('down')
web_url='http://download.cnet.com/'


def down_file(name,url):
	print '************************************************'
	print url
	os.chdir(down_path)
	subprocess.call(["wget.exe",'-e','http_proxy=127.0.0.1:1080','-t','10','-c',url,'-O',name])
	os.chdir(os.path.abspath(os.path.dirname(os.getcwd())))

def make_md5(file):
	try:
		m=hashlib.md5()
		with open(file,'rb')as fp:
			while True:
				blk=fp.read(4096)
				if not blk:
					break
				m.update(blk)
		return m.hexdigest()
	except:
		return False


print 'start !!'

while True:
	n = 0
	for x in range(100):
		n = x + 1
		print "%ss/software/windows/?sort=most-popular&page=%d"%(web_url,n)
		res=requests.get("%ss/software/windows/?sort=most-popular&page=%d"%(web_url,n))



		re_p = re.compile(r'<a href ="%s(.*)class="item-anchor">'%web_url)
		sub_page = re_p.findall(res.content)
		if sub_page!=[]:
			for p in sub_page: 
				download_url=web_url+p.split(' ')[0][:-1]
				result=requests.get(download_url)
				soup = BeautifulSoup(result.content,'html.parser')
				try :
					
					size=soup.find('ul',{'class':'two'}).find_all('div')[1].string
					name=soup.find('div',{'class':'download-now flat-detail-button-dln'}).get('data-product-title')
					company=soup.find_all("table", attrs={"class":"specs-details"})[1].find('tr',attrs={"id": "specsPubName"}).find_all('td')[1].string

					ver=soup.find('ul',{'class':'one'}).find_all('div')[1].string
					
					conn=MySQLdb.Connect(host='127.0.0.1',user='root',passwd='',db='mysql',charset='utf8')
					cur=conn.cursor()
					
					cur.execute("select * from down_2017 where name='%s' and ver='%s' and size='%s'"%(name,ver,size))
					reslist=cur.fetchall()

					if reslist==():

						print 'size :',size
						print 'name :',name
						print 'company :',company
						print "ver: ",ver
						print 'download...'
						print '-----------------------------------------------------------------------------------'
		
						down_url=soup.find('div',{'class':'download-now flat-detail-button-dln'}).get('data-dl-url')
						file_name=down_url.split('&fileName=')[-1]


						down_file(file_name,down_url)

						downfile=os.path.join(down_path,file_name)
						if make_md5(downfile):
							md5=make_md5(downfile)
							upload_package.main(downfile)

							cur.execute("INSERT INTO down_2017 (name,ver,size,company,md5) VALUES('%s','%s','%s','%s','%s')" %(name,ver,size,company,md5)) 
							conn.commit()
							
			
					else:
						print name,' is found'

						print '-----------------------------------------------------------------------------------'
					cur.close()
					conn.close()

				except Exception as e:
					print e 
