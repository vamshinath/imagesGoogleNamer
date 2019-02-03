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
        browser = webdriver.Firefox()
    
        filePath = fl
        browser.get(searchUrl)
        time.sleep(2.5)

        browser.find_element_by_id("imgFile").send_keys(filePath)
        browser.find_element_by_id("checkReverse").submit()

        time.sleep(1.5)
        link = getGoogleLink(browser)
        if link == False:
            return 
        browser.get(link)
        time.sleep(2.5)

        ul=browser.find_element_by_class_name("other-sites__container")

        imgname=ul.find_element_by_class_name("other-sites__desc").text

        print(imgname)

        # imgname=browser.find_element_by_xpath('//*[@title="Search"]').get_attribute("value")

        if imgname == None or len(imgname) < 3:
            print("Nothing")
            gotError = True
            pass

        renameFile(fl,imgname.replace(" ",''))
        browser.close()
    except Exception as e:
        print("hey "+str(e))
        gotError = True
        if not browser is None:
            browser.close()


def getGoogleLink(browser):
    link=''
    while len(link) <3:
        try:
            link=browser.find_elements_by_link_text("Check Images")[-1].get_attribute("href")
            print(link)
        except IndexError:
            time.sleep(2)
            return False
        except Exception as e:
            print(e)
            time.sleep(1)
    return link


def main():

    global gotError
    global files_count

    os.chdir(sys.argv[1])

    files = scanFiles()

    files_count = len(files)

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
