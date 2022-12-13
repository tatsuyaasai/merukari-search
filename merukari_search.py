# merukari_search.py
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
import io
from urllib import request
import os
import tkinter.filedialog


class MeruSearch:
    def __init__(self, url):
        self.driver_place = r'C:\Users\t_asai\AppData\Local\Programs\Python\Python311\Lib\selenium\chromedriver'
        self.site_url = url
        self.seller_name = ""
        self.seller_pro_num = 0
        self.seller_sell_num = 0
        self.pro_list = []

    def search(self):
        driver = webdriver.Chrome(self.driver_place)
        driver.get(self.site_url)
        sleep(5)

        seller_name_selector = "#main > div > div > section > div > div.layout__FlexWrapper-sc-1lyi7xi-9.gVXRLc > div:nth-child(1) > mer-heading"
        seller_info = driver.find_element_by_css_selector(seller_name_selector)
        self.seller_name = seller_info.get_attribute('title-label')

        seller_pro_num_selector = "#main > div > div > section > div > div.ProfileCard__UserInfo-sc-1ddjg8c-2.dYwgWT > div > a:nth-child(1) > div > mer-text.mer-spacing-r-4"
        self.seller_pro_num = driver.find_element_by_css_selector(seller_pro_num_selector).text

        seller_sell_num_selector = "#main > div > div > section > div > div.layout__FlexWrapper-sc-1lyi7xi-9.gVXRLc > div.avatar-info > div > div > a > mer-rating"
        seller_info = driver.find_element_by_css_selector(seller_sell_num_selector)
        self.seller_sell_num = seller_info.get_attribute('count')

        flag_load = True
        flag_max = 1
        while flag_load:
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            sleep(1)
            if driver.find_elements_by_class_name(
                    "LoadMoreButton__StyledButton-sc-ua1bnc-0"):
                flag_load = True
                load_button = driver.find_element_by_class_name(
                    "LoadMoreButton__StyledButton-sc-ua1bnc-0")
                load_button.click()
                flag_max += 1
                sleep(2)
                if flag_max * 30 > 1000:
                    flag_load = False
            else:
                flag_load = False

        class ProductData:
            def __init__(self, title, price, sold, pro_num, pic_src,
                         created_day, pro_url):
                self.title = title
                self.price = price
                self.flag_sold = sold
                self.pro_num = pro_num
                self.pic_src = pic_src
                self.created_day = created_day
                self.pro_url = pro_url

        def pic_save(i_url, i_num):
            if i_num < 300:
                f = io.BytesIO(request.urlopen(i_url).read())
                img = Image.open(f)
                img.save('for_img/img{}.jpg'.format(i_num))

        i = 1
        flag_pro = True
        css_selector = '#item-grid > ul > li:nth-child({}) > a > mer-item-thumbnail'
        url_css_selector = '#item-grid > ul > li:nth-child({}) > a'

        while flag_pro:
            if driver.find_elements_by_css_selector(css_selector.format(i)):

                url_element = driver.find_element_by_css_selector(
                    url_css_selector.format(i))
                element = driver.find_element_by_css_selector(
                    css_selector.format(i))

                if element.get_attribute('sticker'):
                    flag_sold = "売り切れ"
                else:
                    flag_sold = "販売中"

                pro = ProductData(element.get_attribute('alt')[:-6],
                                  element.get_attribute('price'),
                                  flag_sold,
                                  i,
                                  element.get_attribute('src'),
                                  element.get_attribute('src')[-10:],
                                  url_element.get_attribute('href')
                                  )
                self.pro_list.append(pro)
                pic_save(element.get_attribute('src'), i)
                i = i + 1
                flag_pro = True
                if i == 1000:
                    flag_pro = False
            else:
                flag_pro = False

        driver.quit()


if __name__ == "__main__":
    a = MeruSearch("https://jp.mercari.com/user/profile/134437721")
    a.search()
