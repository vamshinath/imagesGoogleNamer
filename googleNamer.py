from selenium import webdriver
import requests

def main():

    searchUrl = 'http://www.google.hr/searchbyimage/upload'

    browser = webdriver.Firefox()
   
    filePath =  ""
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']

    browser.get(fetchUrl)

    imgname=browser.find_element_by_xpath('//*[@title="Search"]').get_attribute("value")

    print(imgname)


if __name__ == "__main__":
    main()