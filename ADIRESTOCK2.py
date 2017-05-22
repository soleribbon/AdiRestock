import requests, json, time, re
from bs4 import BeautifulSoup
import random
from slacker import Slacker
import tweepy
import requests
from requests.auth import HTTPProxyAuth

 
#------------------------
slackapikey = ('xoxb-168765462614-AF2fvGqqzsTorz0BTvzXaEYu')
slack = Slacker(slackapikey)

consumer_key = ("mTB5fHp7hQobiqiK3rD8YKn0j")
consumer_secret = ("gDg7PyRGtgnbv6hNhMIrLPd5vHqx3Ld7DsndZK3KZccenocADx")
access_token = ("865371714858885122-I4KeOb6QdiSeOToOGshLJwKF3s2Ye7i")
access_token_secret = ("xGLpgfIGTUiRrgdNcCmojbWPtuRGEvSyh3b9f9eLeC65E")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
#-------------------------

proxyuser = "zoz"
proxypass = "zoz"

skus = open('pids.txt').read().splitlines()
proxifile_us = open('usproxy.txt').read().splitlines()
proxifile_uk = open('ukproxy.txt').read().splitlines()
locales_file = open('locales.txt').read().splitlines()

headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                "Accept-Language" : "en-US,en;q=0.8"}




#r = requests.get("http://www.adidas.com/us/", proxies=proxies, auth=auth)
#print (r.text)






def parsingjson():
    while True:
        time.sleep(1)  
        
        locales = random.choice(locales_file)
        
        if locales == "US":

            basesiteurl = ("adidas.com")
            locale = ("US")
            proxiez_us = random.choice(proxifile_us)
            proxies = {"http": proxiez_us}
            sitemapurl = ('http://www.adidas.com/on/demandware.static/-/Sites-CustomerFileStore/default/adidas-US/en_US/sitemaps/product/adidas-US-en-us-product.xml')
            print ("US")
        
        elif locales == "UK":
            basesiteurl = ("adidas.co.uk")
            locale = ("GB")
            proxiez_uk = random.choice(proxifile_uk)
            proxies = {"http": proxiez_uk}
            sitemapurl = ("http://www.adidas.co.uk/on/demandware.static/-/Sites-CustomerFileStore/default/adidas-GB/en_GB/sitemaps/product/adidas-GB-en-gb-product.xml")
            print ("UK")
        
        
        #auth = HTTPProxyAuth(proxyuser, proxypass)
        
        print (proxies)

        req = requests.Session()
        #requests.GET.getlist('url')
        req.cookies.clear()

        sku = random.choice(skus)
        

        base = ("http://www.{}/on/demandware.store/Sites-adidas-{}-Site/MLT/Product-GetVariants?pid={}").format(basesiteurl, locale, sku) #improve
            
        print (sku)
        r = req.get(base, headers=headers, proxies=proxies)
        print (r.status_code)
        

        try:
            json_data = (json.loads(r.text))
            pid = json_data['variations']['variants'][0]['articleNo']
            price = json_data['variations']['variants'][0]['pricing']['standard']
        except:
            continue

        
        #PARSES SIZE STOCK
        #product_size_stocks = {}
        #product_size_ids = {}
        #for item in json_data['variations']['variants']:
                #product_size_stocks[str(item['attributes']['size'])] = int(item['ATS'])

        #PARSES TOTAL STOCK
        versions = json.loads(r.text)['variations']['variants']
                    
        stock = {}
        global total
        total = 0
        for version in versions:
            stockCount = version["ATS"]
            total += int(stockCount)
            stockSizes = version["attributes"]["size"]
            stock[stockSizes] = stockCount
            
        stock['total'] = total
        #print (total)
        
        if total > 0:
            
            print ("HURRAYYYY")


            headerz = {
                            'Connection': 'keep-alive',
                            'Host': 'www.adidas.com',
                            'Upgrade-Insecure-Requests': '1',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
                        }
                        
                        
                        


            
            searchword = (sku)
            response = req.get(sitemapurl, headers=headers, proxies=proxies)

            print (searchword)                       
        
            ya = (response.text)
            
            token = BeautifulSoup(ya, "lxml")
            
            
            for option in token.find_all('loc', text=re.compile(searchword)):
                    global link
                    link = (option.text)
                    #print (link)
                
                    
                    
               
                
            #time.sleep(10)
              



            try: 
                aco = req.get(link, headers=headerz, proxies=proxies)
            except:
                continue
            soup = BeautifulSoup(aco.text, 'lxml')
            
            
            titleofproduct = soup.title.string
            print (titleofproduct)

            brosd = str(titleofproduct)
            inttotal = str(total)





            slack.chat.post_message('#adimon', 

            "RESTOCK:\n" +
            (brosd) + "\n" +
            "Stock: " + (inttotal) + "\n" +
            #"PID: " + (sku) + "\n" +
            "Link:\n" + 
            (link) + "\n" +
            ("-------------------------")



            )

            #TWEETIINNG SSTUFFFFF
            
            try:
                api.update_status("RESTOCK:\n" +
                (brosd) + "\n" +
                "Stock: " + (inttotal) + "\n" +
                "Link:\n" + 
                (link) + "\n" +
                ("-------------------------")
                )
            except:
                continue
            
        else:
            
            continue
        #versions2 = json.loads(r.text)['variations']['variants']['avStatus']
    
parsingjson()

#find in general yes or no stock
#convert pids from file to url  - fixed but needs improving! (currently random)
#MAKE DIFF REGIONS







