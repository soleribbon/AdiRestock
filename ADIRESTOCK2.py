import requests, json, time, re
from bs4 import BeautifulSoup
import random
from slacker import Slacker
import tweepy
import requests
from requests.auth import HTTPProxyAuth
from slackclient import SlackClient
 
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
        time.sleep(4)
        open('sizes.txt', 'w').close()
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
            ayo = str(stockSizes)
                #print str(stockSizes)
            
            with open('sizes.txt', 'a') as f:
                f.write(ayo + "\n")
                f.close()
            
        stock['total'] = total
        strtotal = (str(total))
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
            



            
            soups = BeautifulSoup(aco.text, "lxml")


            #EXTRACTS PICTURE
            a = (soups.find('div', {'id': 'main-image'}))

            productDivs = (soups.findAll('div', attrs={'id' : 'main-image'}))
            for div in productDivs:
                picture = div.find('a')['href']
            #-----------------------------------


            #GETS SIZE LIST

            ending_size_list = open('sizes.txt').read().splitlines()
            endingsizes = (", ".join(ending_size_list))
            


           
                
    

            

            attachments = [{
                        "title": (titleofproduct),
                        "color": "#9C1A22",
                        "author_link": "https://twitter.com/soleadimon",
                        "mrkdwn_in": ["text"],
                        "fields": [{
                                "title": "Available Sizes:",
                                "value": "{}".format(endingsizes),
                                "short": True
                                
                
                            
                            },
                            {
                                "title": "Total Stock:\n",
                                "value": total,
                                "short": True
                                
                            },
                            
                            
                            {
                                "title": "Link:",
                                "value": (link),
                                "short": False
                            }
                        
                        ]
            }]





            token = ("xoxp-128291386865-129057774181-142276982917-782873c11f4a369e32629df537e4a96a")
                
            slack_client = SlackClient(token)
            slack_client.api_call("chat.postMessage", channel='adimon', text='', username="RESTOCK:", attachments=attachments, icon_url=picture)







        

            #TWEETIINNG SSTUFFFFF
            
            try:
                api.update_status("RESTOCK:\n" +
                (sku) + "\n" +
                "Stock: " + (strtotal) + "\n" +
                "Link:\n" + 
                (link) + "\n" +
                ("-------------------------")
                )
            except Exception as e:
                print (e)
                continue
            
        else:
            
            continue
        #versions2 = json.loads(r.text)['variations']['variants']['avStatus']
    
parsingjson()

#find in general yes or no stock
#convert pids from file to url  - fixed but needs improving! (currently random)
#MAKE DIFF REGIONS






