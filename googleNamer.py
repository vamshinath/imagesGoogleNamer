from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
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
    searchUrl = 'http://www.google.hr/searchbyimage/upload'

    browser = webdriver.Firefox(options=options)
   
    filePath = fl
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']

    browser.get(fetchUrl)

    imgname=browser.find_element_by_xpath('//*[@title="Search"]').get_attribute("value")

    renameFile(fl,imgname.replace(" ",''))

    browser.close()




def main():

    os.chdir(sys.argv[1])

    files = scanFiles()

    files_count = len(files)
    ctr=0

    for img in files:
        print(str(ctr)+"/"+str(files_count),end=" ")
        ctr+=1
        threading.Thread(target=getName,args=(img,)).start()
        while  threading.active_count() > 10:
            time.sleep(0.75)

       



if __name__ == "__main__":
    main()