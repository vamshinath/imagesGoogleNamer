from selenium import webdriver
import requests,os,re,sys

def scanFiles():

    ofiles = {}
    imgFiles=[]

    for root, directories, filenames in os.walk('.'):
        for filename in filenames:
            if "9351" in filename:
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
        

def getName(fl):
    searchUrl = 'http://www.google.hr/searchbyimage/upload'

    browser = webdriver.Firefox()
   
    filePath =  ""
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']

    browser.get(fetchUrl)

    imgname=browser.find_element_by_xpath('//*[@title="Search"]').get_attribute("value")

    print(imgname)



def main():

    os.chdir(sys.argv[1])

    files = scanFiles()

    for img in files:
        print(img)
    


if __name__ == "__main__":
    main()