#  -*- coding:utf-8 -*-
import urllib2, urllib
import os, sys
import time,datetime
import requests,re
import bs4
import urllib2
import subprocess,zipfile


#root_site='http://www.malware-traffic-analysis.net'
#s = requests.session()
#s.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
#s.get(root_site)
	
##########################################################################################
def decomp(file_path ,password):
	if os.path.exists(file_path):  
		#if file_path[-4:]=='.zip':
		#print file_path
		print '-----------------------------------'
		print file_path,' is Found~  Decomp!'
		print '-----------------------------------'
		zip = zipfile.ZipFile(file_path, "r",zipfile.zlib.DEFLATED)
		try:
			if os.path.isdir(file_path[:-4]):  
				pass  
			else:  
				os.mkdir(file_path[:-4])  
				zip.extractall(path=file_path[:-4],members=zip.namelist() , pwd=password)
				zip.close()
		except Exception as ex:
			print ex

	else:
		print file_path,'is not found!'
		sys.exit()

def compress(zip_file, input_dir):
	tmp_file=os.path.join('tmp',zip_file) 
	  	
	if not os.path.exists('tmp'):  
		os.mkdir('tmp')  


	#print '----------------------------------------'
	print 'Compress: ',input_dir,' -> ',tmp_file,
	print '\n----------------------------------------'
	f_zip = zipfile.ZipFile(tmp_file, 'w')
	for root, dirs, files in os.walk(input_dir):
		for f in files:
			abs_path = os.path.join(os.path.join(root, f))
			rel_path = os.path.relpath(abs_path, os.path.dirname(input_dir))
			f_zip.write(abs_path, rel_path, zipfile.ZIP_STORED)


	
	if os.path.exists(tmp_file):
		#print name
		#print file_path,'asfasfasf'
		#os.remove(os.path.join('download',zip_file))
		

			'''os.system('rd /S /Q %s'%(os.path.join('download',zip_file))[:-4]) 
			print 'del :' ,os.path.join('download',zip_file)[:-4]
			'''
	

		#os.system('copy %s %s'%(tmp_file,path))
		#shutil.copy(tmp_file, path) 

	else:
		print os.path.join('download',zip_file)[:-4],'is Del Error!!'
##########################################

def down_file(_path,url,filen):
	print _path,url,filen
	os.chdir(_path)
	subprocess.call(["wget.exe",'-t','3','-c',url,'-O',filen])	
	os.chdir(os.path.dirname(__file__))




def up_sample(_path,CS):
	#name=_path.split('\\')[-1]

	name2=os.path.join('download',_path.split('\\')[-1][:-4])
	decomp(_path,'infected')

	#compress(name,_path[:-4])

	'''tmp_file=os.path.join('tmp',name)
	print '---------------------------------------'
	print tmp_file,'is Upload!'
	'''
	#cmd = 'GenericUploader/GenericUploader.exe %s -srckey=%s' %(tmp_file,CS)
	cmd = 'GenericUploader/GenericUploader.exe %s -srckey=%s' %(name2,CS)

	#print 'cmd: ',cmd

	child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	streamdata = child.communicate()[0]
	rc = child.returncode
	#if rc == 0:
	#	os.remove('uploads\\' + md5  + '.malwr')
		#self.mydb.insert(t)
	print 'CMD:[',cmd,']'
	if rc == 0:
		print('{0} upload success!'.format(name2))
		print '---------------------------------------'
		#return True
		#break
	else:
		print('{0} upload failed![ret={1}]'.format(name2, child.returncode))
		print '---------------------------------------'
	
	os.system('rd /S /Q %s'%(name2) )
	print 'del :' ,name2


	#print 'CMD:[',cmd,']'
	#print streamdata, child.returncode

	'''
	os.system('del /q %s'%tmp_file)
	print 'del :' ,tmp_file
	'''


	'''print _path,'is Upload!'
	try:
		toolpath=os.path.join('GenericUploader','GenericUploader.exe')
		subprocess.call([toolpath,_path,CS])
		#print CS
		#os.remove(_path)
	except Exception, _ex:
		print 'ERROR: %s' % str(_ex)
		print _path,'is Wrong!'
	'''


Title='''class="list_header">(.*)</a> -- <a href="(.*)" class="main_menu">'''


def get_url(page):
	
	#res1 = s.get(page)
	res1 = requests.get(page) 
	#print res1.content
	#print res1

	data = re.compile(Title).findall(res1.content) 

	for i in range(len(data)):

		result=page.replace(page.split('/')[-1],'')+data[i][1]
		#print data1[i][0],page.replace('index.html','')+data1[i][1],data1[i][2]
		print result
		#print i

		try:
			#res2 = s.get(result)
			res2 = requests.get(result)
			_re=['li>ZIP file of the malware:&nbsp; <a class="menu_link" href="(.*).zip">(.*).zip</a></li>',
			     'li>ZIP archive of the malware:&nbsp; <a class="menu_link" href="(.*).zip">(.*).zip</a',
			     'li>ZIP archive of the malware and artifacts:&nbsp; <a class="menu_link" href="(.*).zip">(.*).zip</a']

			
			for index,item in enumerate(_re):
				data1 = re.compile(item,re.I).findall(res2.content) 

				if data1!=[]:

					url=result.replace(result.split('/')[-1],'')+data1[0][0]+'.zip'
					path=os.path.join('download',data1[0][0]+'.zip')
					if not os.path.exists(path):
						print url
						print "downloading file -%d!"%index

						down_file(_path,url,data1[0][0]+'.zip')
						up_sample(path,'LE')
					else:
						print url,'is found! '
				
		except requests.exceptions.ConnectionError:
			print 'ConnectionError'
			get_url(page)


if __name__ == '__main__':

	root_site='http://www.malware-traffic-analysis.net'
	_path=r'download'
	nian=time.strftime('%Y',time.localtime(time.time()))
	#for i in range(2017, 2018):
	page=root_site+'/'+nian+'/index.html'
	print('start get page ' + page)
	get_url(page)	


#########################################################

#db = py_mysql('spider','p',weihua_path)
#db.down_func(filename,weihua_path,weihua_log,'QE')

#	ok=Amain('spider')
#ok.down_func(filename,weihua_path,weihua_log,'QE')


