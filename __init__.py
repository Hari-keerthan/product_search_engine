from flask import Flask
from flask import request
from flask import render_template
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from concurrent.futures import ThreadPoolExecutor
import re

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template("myform.html") # this should be the name of your html file




def flipkart(i):

    inp = i
    middle = i.replace(" ","%20")
    first ='https://www.flipkart.com/search?q='
    last = '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    url1 = str(first)+str(middle)+str(last)
    print(url1)
    r = requests.get(url1)
    print(r)
    content = r.content.decode(encoding='UTF-8')
    soup = BeautifulSoup(content, "lxml")
    regex = re.compile('.*_1vC4OE.*')
    reviews = soup.find_all('a', {"class": "_2cLu-l"})
    cost = soup.find_all("div", {"class" : regex})

    if len(reviews) == 0:
        reviews = soup.find_all('div', {"class": "_3wU53n"})
    if len(reviews) == 0:
        reviews = soup.find_all('a', {"class": "_2mylT6"})
    link = soup.find_all('a' ,{"class": "_31qSD5"})
    link_aftr = []
    if len(link) == 0:
        link = soup.find_all('a', {"class": "_2cLu-l"})
    if len(link) == 0:
        link = soup.find_all('a', {"class": "Zhf2z-"})
    if len(link) == 0:
        link = soup.find_all('a', {"class": "_3dqZjq"})
        #print('https://www.flipkart.com'+i['href'])
    price_aftr = []
    rev_aftr = []
    for i,j,k in zip(cost,reviews,link):
        str2 = str(j.text)
        Ratio = fuzz.partial_ratio(inp.lower(),str2.lower())
        if Ratio>80:
            price_aftr.append(i.text)
            rev_aftr.append(j.text)
            link_aftr.append('https://www.flipkart.com'+k['href'])
            
    if len(rev_aftr) < 3:
        price_aftr = []
        rev_aftr = []
        link_aftr = []
        for i,j,k in zip(cost,reviews,link):
            price_aftr.append(i.text)
            rev_aftr.append(j.text)
            link_aftr.append('https://www.flipkart.com'+k['href'])
        
    opt = dict(zip(rev_aftr,zip(price_aftr,link_aftr)))
    return opt
    #return render_template("index.html",message="flipkart123",contacts=opt)
 

def amazon(i):
    inp = i
    middle = i.replace(" ","+")
    first = 'https://www.amazon.in/s?k='
    last = '&ref=nb_sb_noss_2'
    url2 = str(first) + str(middle) + str(last)
    print(url2)
    headers = {'User-Agent': 'Chrome' }
    #session = requests.Session()
    #session.trust_env = True
    r = requests.get(url2,headers=headers)
    print(r)
    content = r.content.decode(encoding='UTF-8')
    soup = BeautifulSoup(content, "lxml")
    regex = re.compile('.*a-section a-spacing-medium.*')
    #reviews = soup.find_all("span", {"class": "a-size-medium a-color-base a-text-normal"})
    reviews = soup.find_all("span",{"class": regex})
    cost = soup.find_all('span', {"class": "a-price-whole"})
    image = soup.find_all('img' , {'class' : 's-image'})
    img_aftr = []
    rev_aftr = []
    price_aftr = []
    link = soup.find_all('a' ,{"class": "a-link-normal a-text-normal"})
    link_aftr = []
    '''
    for i in link:
        link_aftr.append('https://www.amazon.in'+i['href'])
        '''
    for i,j,k,l in zip(cost,reviews,link,image):
        str2 = str(j.text)
        Ratio = fuzz.partial_ratio(inp.lower(),str2.lower())
        if Ratio>80:
            price_aftr.append(i.text)
            rev_aftr.append(j.text)
            link_aftr.append('https://www.amazon.in'+k['href'])
            img_aftr.append(l['src'])
    if len(rev_aftr) < 3:
        price_aftr = []
        rev_aftr = []
        link_aftr = []
        for i,j,k in zip(cost,reviews,link):
            price_aftr.append(i.text)
            rev_aftr.append(j.text)
            link_aftr.append('https://www.flipkart.com'+k['href'])
    
    opt = dict(zip(rev_aftr,zip(price_aftr,link_aftr,img_aftr)))
    return opt


def paytm(i):
    inp = i
    middle = i.replace(" ","%20")
    first ='https://paytm.com/shop/search?q='
    last = '&from=organic&child_site_id=1&site_id=1'
    url4 = str(first)+str(middle)+str(last)
    print(url4)
    r = requests.get(url4)
    print(r)
    content = r.content.decode(encoding='UTF-8')
    soup = BeautifulSoup(content, "lxml")
    reviews = soup.find_all('div', {"class": "_2apC"})
    cost = soup.find_all('span', {"class": "_1kMS"})
    offer = soup.find_all('div',{"class":"_27VV"})
    link = soup.find_all('a',{'class': '_8vVO'})
    '''
    img_aftr = []
    image = soup.find_all('div' ,{'class' : '_3nWP'})
    for i in image:
        img_aftr.append((i.find_all('img'))['src'])
    
    img_aftr = []
    '''
    rev_aftr = []
    price_aftr = []
    offer_aftr = []
    link_aftr = []
    for i,j,k,l in zip(cost,reviews,offer,link):
        str2 = str(j.text)
        Ratio = fuzz.partial_ratio(inp.lower(),str2.lower())
        if Ratio>80:
            price_aftr.append(i.text)
            rev_aftr.append(j.text)
            offer_aftr.append(k.text)
            link_aftr.append(l['href'])
 
    opt = dict(zip(rev_aftr, zip(price_aftr,offer_aftr,link_aftr)))
    return opt


def croma(i):
    inp = i
    middle = i.replace(" ","+")
    first ='https://www.croma.com/search/?text='
    #last = '&from=organic&child_site_id=1&site_id=1'
    url5 = str(first)+str(middle)
    print(url5)
    headers = {'User-Agent': 'Chrome' }
    r = requests.get(url5,headers=headers)
    print(r)
    content = r.content.decode(encoding='UTF-8')
    soup = BeautifulSoup(content, "lxml")
    reviews = soup.find_all('h3')
    cost = soup.find_all('span', {"class": "pdpPrice"})
    link = soup.find_all('a' , {'class' : 'product__list--thumb'})
    image = soup.find_all('img', {'class' : '_primaryImg'})
    img_aftr = []
    price_aftr = []
    rev_aftr = []
    link_aftr = []
    for i,j,k,l in zip(cost,reviews,link,image):
        str2 = str(j.text)
        Ratio = fuzz.partial_ratio(inp.lower(),str2.lower())
        if Ratio>80:
            price_aftr.append(i.text)
            rev_aftr.append(j.text)
            link_aftr.append('http://croma.com'+k['href'])
            img_aftr.append(l['data-src'])
    opt = dict(zip(rev_aftr,zip(price_aftr,link_aftr,img_aftr)))
    return opt
    



        
@app.route('/', methods=['POST','GET'])
def my_form_post():
    text1 = request.form['text1']
    return text1

@app.route('/<product>', methods=['POST','GET'])
def hell(product):
    text1 = product 
    '''
    flip = flipkart(text1)
    amaz = amazon(text1)
    pytm = paytm(text1)
    chrm = croma(text1)
    '''
    executor = ThreadPoolExecutor(max_workers=20)
    flip = executor.submit(flipkart,text1)
    amaz = executor.submit(amazon,text1)
    pytm = executor.submit(paytm,text1)
    chrm = executor.submit(croma,text1)
    flip = flip.result()
    amaz = amaz.result()
    pytm = pytm.result()
    chrm = chrm.result()
    
    return render_template("index.html",flp="flipkart",product_flip=flip,amz="AMAZON",product_amaz=amaz,pay="PAYTM",product_pay=pytm,crm="CHROMA",product_crm=chrm)

@app.route('/test', methods=['POST','GET'])
def try2():
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
