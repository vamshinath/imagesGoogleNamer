from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from multiprocessing.dummy import Pool

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
    if len(newName) <2:
        return

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
        searchUrl = 'https://smallseotools.com/reverse-image-search/'
        browser = webdriver.Firefox(options=options)
    
        filePath = fl
        browser.get(searchUrl)
        time.sleep(2.5)

        browser.find_element_by_id("imgFile").send_keys(filePath)
        browser.find_element_by_id("checkReverse").submit()

        time.sleep(1.5)
        link = getYandexLink(browser)
        if link == False:
            return 
        browser.get(link)
        time.sleep(2.5)

        ul=getOtherContainerLink(browser)
        if ul == False:
            return

        imgname=ul.find_element_by_class_name("other-sites__desc").text

        print(imgname)

        if imgname == None or len(imgname) < 3:
            print("Nothing")
            gotError = True
            return

        renameFile(fl,imgname.replace(" ",''))
        browser.close()
    except Exception as e:
        print("hey "+str(e))
        gotError = True
        browser.close()


def getYandexLink(browser):
    link=''
    counter = 0
    while len(link) <3 and counter < 4:
        counter+=1
        try:
            link=browser.find_elements_by_link_text("Check Images")[-1].get_attribute("href")
        except Exception as e:
            print(e)
            time.sleep(2.5)

    if len(link) < 3:
        return False

    return link

def getOtherContainerLink(browser):
    link=''
    counter = 0
    while len(link) <3 and counter < 4:
        counter+=1
        try:
            link=browser.find_element_by_class_name("other-sites__container")
        except Exception as e:
            print(e)
            time.sleep(2.5)

    if len(link) < 3:
        return False

    return link


def main():

    global gotError
    global files_count

    os.chdir(sys.argv[1])

    files = scanFiles()

    files_count = len(files)

    # mypool = Pool(10)

    # mypool.map(getName,files)

    # mypool.join()
    # mypool.close()



    for img in files:

        

        if gotError:
            time.sleep(2.5)
        threading.Thread(target=getName,args=(img,)).start()
        time.sleep(3)
        while  threading.active_count() > 8:
            time.sleep(1.5)

       



if __name__ == "__main__":
    main()
