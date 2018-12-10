import requests
import datetime
from lxml import etree
from selenium import webdriver

class Ubiq(object):

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B202'}
        self.s = requests.session()
        self.s.headers.update(self.headers)

        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome('./bin/chromedriver.exe', chrome_options=options)
        self.driver.get('https://www.ubiqlife.com/')

        for cookie in self.driver.get_cookies():
            c = {cookie['name']: cookie['value']}
            self.s.cookies.update(c)
        self.driver.quit()

        print(datetime.datetime.now().strftime('%X'), 'Getting form key.')
        r = self.s.get('https://www.ubiqlife.com/')
        tree = etree.HTML(r.content)
        self.formKey = tree.xpath('//*[@id="login_form"]/input/@value')[0]
        print(datetime.datetime.now().strftime('%X'), 'Finished getting form key.')

    def scrape(self, id):
        try:
            r = self.s.get('https://www.ubiqlife.com/checkout/cart/add/uenc/,/product/{}/form_key/{}/'.format(id, self.formKey))
            tree = etree.HTML(r.content)
            success = tree.xpath("//ul[@class='messages']/li/ul/li/span/text()")[0]
            if r.status_code == 200:
                if 'cart' in r.url:
                    return id, success
                else:
                    return id, r.url
            else:
                if 'catalog' in r.url:
                    return id, success
                else:
                    return id, r.url
        except Exception as e:
            return id, e

    def run(self, startId, endId):
        for id in range(startId, endId+1):
            x = self.scrape(id)
            if x:
                print(x[0], x[1])

if __name__ == '__main__':
    startId = 102698
    endId = 102800

    Ubiq().run(startId, endId)
