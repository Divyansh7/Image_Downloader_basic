import requests
import os
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen

#The part where download occurs.
#The location of the user local directory is given in this part.
def download_img(URL):
    local_filename=URL.split('/')[-1]
    print("Downloading {} ---> {}".format(URL, local_filename))
    response=requests.get(URL, stream=True)
    with open(local_filename,"wb") as fd:
        for chunk in response.iter_content(chunk_size=5024):
            if chunk:
                fd.write(chunk)

#The main part start from here.
#First the link is asked from the user.
#The link is searched for other links.
#All the link which have signs of pictures are stored.

'''
The links which were used are :
1.https://www.pexels.com/
2.https://pixabay.com/en/photos/wallpaper/
3.https://wallpaperscraft.com/catalog/3d/1366x768
4.https://wallpapercave.com/laptop-wallpapers-hd-free

NOTE:
Any website would work which has images in it.
'''

print("The links which were used are :\n1.https://www.pexels.com/\n2.https://pixabay.com/en/photos/wallpaper/\n3.https://wallpaperscraft.com/catalog/3d/1366x768\n4.https://wallpapercave.com/laptop-wallpapers-hd-free")
print("\nUse the above links as example.\nThe user can input any of his url to check.\nUser has to type the link from above example to check\n")
url=str(input("Url :"))
r=requests.get(url)
html=r.text
name=list(url.split("/"))
first_name=name[0]+"//"+name[2]
soup=BeautifulSoup(html,"lxml")
links=soup.find_all('a')

Urls=list()
newlink=list()
Max_page=100
page_count=0

#This is used to separate the empty and none link.
#Just to separate the links which are useful.
for link in links:
    href1=link.get("href")
    Urls.append(href1)
    if href1 is None:
        href1
    elif(href1.startswith("#")):
        href1
    elif(href1.startswith("https:")):
        newlink.append(href1)
    else:
        newlink.append(first_name+href1)

    
#All the links are check for their unique link.
newlink_set=set()
for i in newlink:
    if(page_count<Max_page):
        a=i.find("photos")
        b=i.find("photo")
        c=i.find("en")
        if(a>0 or b>0 or c>0):
            page_count+=1
            newlink_set.add(i)



img_name=set()
Max_img=100
img_count=0

#The second part is to check if the link has other links for pictures.
#All the picture containing link are transfered to the download area.
#Every link is checked.
#The slicing of link is done to separate the name and link for further process.
for newUrl in newlink_set:
    url_1=newUrl
    try:
        r_1=requests.get(url_1)
        html_1=r_1.text
        soup_1=BeautifulSoup(html_1,"lxml")
        imgData=soup_1.find_all("img")
        for img in imgData:
            temp=img.get("src")
            if(temp is None):
                img
            elif(temp.startswith("https")):
                question_mark = temp.find("?")
                if(question_mark>0):
                    temp = temp[:question_mark]
                os.path.split(temp)
                unique_img=os.path.split(temp)[1]
                if unique_img not in img_name:
                    img_name.add(unique_img)
                    if(img_count<Max_img):
                        img_count+=1
                        download_img(temp)
    except Exception:
        print("Blank")

print(page_count)
print(img_count)
print("Process Complete")


