from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from fake_useragent import UserAgent
ua = UserAgent()

options = Options()
#options.headless = False
browser = ''
gotError=False

import requests,os,re,sys,shutil
import threading,time

def scanFiles():

    ofiles = {}
    imgFiles=[]

    for root, directories, filenames in os.walk('.'):
        for filename in filenames:
            if "9351" in filename or filename.startswith("gsd"):
                continue
            try:
                    f=os.path.abspath(os.path.join(root,filename))
                    fsz=os.stat(f).st_size
                    if fsz < 10240:
                        continue
                    ofiles[f]=fsz
            except Exception as e:
                print(e)

    files = sorted(ofiles.items(),key=lambda x:x[1],reverse=True)

    for fl,_ in files:
        flnm_lower=os.path.basename(fl.lower())
        if ".jpg" in flnm_lower or ".png" in flnm_lower or ".jpeg" in flnm_lower:
            imgFiles.append(fl)

    return imgFiles
 
def renameFile(fl,newName):
    path = os.path.dirname(fl)
    ext="."+os.path.basename(fl).split(".")[-1]
    shutil.move(fl,path+"/gsd"+newName+ext)
    print(fl,newName)

def getName(fl):
    print("in getName")
    global gotError
    global ua
    global browser
    global options

    try:
        searchUrl = 'http://www.google.hr/searchbyimage/upload'
        #
        userAgent = ua.random
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", userAgent)

        options.add_argument(f'user-agent={userAgent}')
        browser = webdriver.Firefox(firefox_profile=profile,options=options)
    
        filePath = fl
        multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
        header = {'User-Agent':str(userAgent)}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False,headers=header)
        fetchUrl = response.headers['Location']

        print("request sent")

        browser.get(fetchUrl)

        imgname=browser.find_element_by_xpath('//*[@title="Search"]').get_attribute("value")

        if imgname == None or len(imgname) < 3:
            gotError = True
            pass

        renameFile(fl,imgname.replace(" ",''))
    except Exception as e:
        print(e)
        gotError = True
        if not browser:
            browser.close()




def main():

    global gotError

    os.chdir(sys.argv[1])

    files = scanFiles()

    files_count = len(files)
    ctr=0

    for img in files:
        # if gotError:
        #     time.sleep(1.5)
        if gotError and ctr > 30:
            os.system("python3 ~/googleNamer.py "+sys.argv[1])
            break


        print(str(ctr)+"/"+str(files_count),end=" ")
        ctr+=1
        #getName(img)
        #time.sleep(2)
        threading.Thread(target=getName,args=(img,)).start()
        time.sleep(1.3)
        while  threading.active_count() > 4:
            time.sleep(1.5)

       



if __name__ == "__main__":
    main()
