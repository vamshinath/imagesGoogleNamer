from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
import base64

from multiprocessing.dummy import Pool


ua = UserAgent()
options = Options()
options.headless = True
files_count=0
counter=0

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
    if len(newName) == 0:
        pass

    path = os.path.dirname(fl)
    ext="."+os.path.basename(fl).split(".")[-1]
    shutil.move(fl,path+"/gsd"+newName+ext)
    print(fl,newName)

def getName(fl):
    global counter
    global gotError
    counter+=1


    print(str(counter)+"/"+str(files_count))

    try:
        searchUrl = 'https://www.google.com/imghp?sbi=1&gws_rd=ssl'
        rsearchUrl= "http://www.google.com/searchbyimage/upload"
        browser = webdriver.Firefox(options=options)
    
        userAgent = ua.random
        #browser = webdriver.Firefox()
    
        filePath = fl
        multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
        header = {'User-Agent':str(userAgent)}
        response = requests.post(rsearchUrl, files=multipart, allow_redirects=False,headers=header)
        fetchUrl = response.headers['Location']

        time.sleep(1)
        browser.get(searchUrl)
        time.sleep(1)
        browser.find_element_by_link_text("Upload an image").click()
        time.sleep(1.5)
        # image = "data:image/jpg;base64," + filePath
        
        # browser.execute_script('document.getElementById("qbui").value = "' + image + '"')

        # browser.find_element_by_id("qbf").submit()
        # time.sleep(2)

        browser.get(fetchUrl)

        time.sleep(1)

        imgname=browser.find_element_by_xpath('//*[@title="Search"]').get_attribute("value")

        if imgname == None or len(imgname) < 3:
            gotError = True
            pass

        renameFile(fl,imgname.replace(" ",''))
        browser.close()
    except Exception as e:
        print(e)
        gotError = True
        if not browser is None:
            browser.close()




def main():

    global gotError
    global files_count

    os.chdir(sys.argv[1])

    files = scanFiles()

    files_count = len(files)
    ctr=0

    mypool = Pool(10)

    mypool.map(getName,files)

    mypool.join()
    mypool.close()

    # for img in files:

        

        # if gotError:
        #     time.sleep(2.5)
        # print(str(ctr)+"/"+str(files_count),end=" ")
        # ctr+=1
        # threading.Thread(target=getName,args=(img,)).start()
        # time.sleep(5)
        # while  threading.active_count() > 15:
        #     time.sleep(1.5)

       



if __name__ == "__main__":
    main()
