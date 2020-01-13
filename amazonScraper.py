import requests
from bs4 import BeautifulSoup
import json
from threading import Thread


class amazonScraper:


    """
        ===== How to use ? =====

    obj = amazonScraper(\"ram\", 2)
    obj.Start()

    
    """



    def __init__(self, keyword, pages):
        self.headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3865.120 Safari/537.36 OPR/64.0.3417.92"}
        self.p = pages
        self.keyword = "+".join(keyword.split(" "))

        self.result = []


    def MakeUrl(self):
        output = []
        for page in range(1, self.p):
            url = "https://www.amazon.in/s?k=%s&page=%d&ref=nb_sb_noss"%(self.keyword,page)
            output.append(url)
        return output


    def Scrape(self, url):
        
        """ This method will take data from GetData method and feed it to the ScrapeName method. """

        data = self.GetData(url)
        self.ScrapeName(data)


    def Start(self):

        """ This method will be called after declaring the object """

        for url in self.MakeUrl():
            t = Thread(target=self.Scrape, args=(url,))
            t.start()


    def GetData(self, url):

        """ Method for fetching the raw data of the searched item. """
        
        req = requests.get(url, headers=self.headers)
        return req.text
    
    def ScrapeName(self, data):

        """ Method for scraping the product name and its price. """

        data = data
        soup = BeautifulSoup(data, "lxml")

        out = []


        div = soup.find("div", {"class":"s-result-list s-search-results sg-row"})
        dataDivs = div.findAll("div", {"class":"a-section a-spacing-medium"})


        for x in dataDivs:
            try:

                """ 
                    Here I am looping through the divisions in the dataDivs list.
                    And then scraping the name and price of the top product.

                 """

                y = x.find("a", {"class":"a-link-normal a-text-normal"})
                name = y.find("span", {"class":"a-size-medium a-color-base a-text-normal"}).text
                
                
                """ Below two lines are for the price of the product. """

                n = x.find("a", {"class":"a-size-base a-link-normal s-no-hover a-text-normal"})
                price = n.find("span", {"class":"a-price-whole"}).text
            
                obj = {"name":name, "price":price}
                jsonObj = json.dumps(obj)
                out.append(jsonObj)
    

            except:
                pass
        self.result.append(out)
    #    print(out)
    

                

# key = str(input("Enter the name of product to search: "))
# pages = int(input("Enter the number of pages: "))

# am = amazonScraper(key, pages)
# am.Start()
