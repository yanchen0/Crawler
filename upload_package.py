#-*-coding:utf-8 -*-
import os
import shutil
import sys
import subprocess
import time

curdir,pyfile=os.path.split(sys.argv[0])

srckey='XA'  #可信来源

def main(src):
    #if len(sys.argv) < 2:
    #    print('invalid argv!')
    #    return
    #src=sys.argv[1]

    if not os.path.exists(src):
        print('not exists!', src)
        return
    #if os.path.isdir(src):
    #    if extract_package(src):
    #        upload(src)
    else:
        if extract_package(src):
            src2 =  src + '.extfiles'
            if os.path.isdir(src2):
                upload(src2)
                #shutil(src2)
            else:
                upload(src)
                #os.remove(src)
    try:
        shutil.rmtree(src2)
        os.remove(src)
    except Exception as e:
        print(e)

def extract_package(src):
    ext_tool=os.path.join(curdir,'engine13\\conscanx.exe')
    if not os.path.exists(ext_tool):
        print('not exists!',ext_tool)
        return False
    print('extracting...')
    p = subprocess.Popen([ext_tool, '-dumpemb', src])
    for i in range(3):
        try:
            output, err = p.communicate()
            if p.returncode == 0:
                print('{0} extract success!'.format(src))
                return True
                break
            print('extract failed!',err)
            time.sleep(3)
        except Exception as e:
            print(e)
    return False

def upload(src):
    up_tool=os.path.join(curdir,'GenericUploader\\GenericUploader.exe')
    
    if not os.path.exists(up_tool):
        print('not exists!',up_tool)
        return False
    print('uploading...')
    p = subprocess.Popen([up_tool, '-srckey='+srckey, src])

    print '\n------------------------------------'
    print 'cmd: ',up_tool, '-srckey='+srckey, src
    print '------------------------------------\n'
    for i in range(3):
        try:
            output, err = p.communicate()
            if p.returncode == 0:
                print('{0} upload success!'.format(src))
                return True
                break
            else:
                print('{0} upload failed![ret={1}]'.format(src, p.returncode))
            time.sleep(3)
        except Exception as e:
            print(e)
    return False

if __name__ == '__main__':
    main(test)
