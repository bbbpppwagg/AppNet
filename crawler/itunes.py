import scrapy
from tutorial.items import TutorialItem
from urllib.request import unquote
from selenium import webdriver
import re

class ItunesSpider(scrapy.Spider):
    name = "itunes"
    allowed_domains = ["itunes.apple.com"]
    start_urls = [
        "https://itunes.apple.com/cn/app/qq/id444934666?mt=8"
    ]

    def parse(self,response):
        
        app_name = response.xpath(
            '//h1/text()')[0].extract()
        app_name = app_name.replace('\n', '').replace(' ', '')
        print(app_name)

        app_category = response.xpath('//a[@href="https://itunes.apple.com/cn/genre/id6005"]/text()')[0].extract()
        app_category = app_category.replace('\n', '').replace(' ', '')
        print(app_category)
    
        app_developer = response.xpath(
            '//dd[@class="information-list__item__definition l-column medium-9 large-6"]/text()')[0].extract()
        app_developer = app_developer.replace('\n', '').replace(' ', '')
        print(app_developer)

        app_descrption = response.xpath('//div[@class="section__description"]//p/@aria-label')[0].extract()
        app_descrption = app_descrption.replace('\n', '').replace(' ', '')
        print(app_descrption)

        app_logo_url = response.xpath(
            '//picture[@class="product-hero__artwork we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view"]//img/@src')[0].extract()
        app_logo_url = app_logo_url.replace('\n', '').replace(' ', '')
        print(app_logo_url)

        app_min_os_version = response.xpath(
            '//div[@class="information-list__item l-row"]//dd/@aria-label')[1].extract()
        app_min_os_version = app_min_os_version.replace('\n', '').replace(' ', '')
        app_min_os_version = re.findall(r"\d+\.?\d*", app_min_os_version)
        app_min_os_version = ''.join(app_min_os_version)
        print(app_min_os_version)

        app_min_os_version_text = response.xpath(
            '//div[@class="information-list__item l-row"]//dd/@aria-label')[1].extract()
        app_min_os_version_text = app_min_os_version_text.replace(
            '\n', '').replace(' ', '')
        print(app_min_os_version_text)

        # 不是所有App都有
        app_purchases_text = response.xpath('//dd[@class="information-list__item__definition l-column medium-9 large-6"]//li//span').extract()
        # app_purchases_text = app_purchases_text.replace('\n', '').replace(' ', '')
        for i in app_purchases_text:
            print(i)
        print("OK")

        app_developer_url = response.xpath('//h2[@class="product-header__identity app-header__identity"]//a/@href')[0].extract()
        app_developer_url = app_developer_url.replace(
            '\n', '').replace(' ', '')
        print(app_developer_url)

        app_content_rating = response.xpath(
            '//h1[@class="product-header__title app-header__title"]//span/text()')[0].extract()
        app_content_rating = app_content_rating.replace(
            '\n', '').replace(' ', '')
        print(app_content_rating)

        # app_content_rating_reason = response.xpath()
        # app_content_rating_reason = app_content_rating_reason.replace(
        #     '\n', '').replace(' ', '')
        # print(app_content_rating_reason)

        # app_installation_size = response.xpath()
        # app_installation_size = app_installation_size.replace(
        #     '\n', '').replace(' ', '')
        # print(app_installation_size)

        # app_language = response.xpath()
        # app_language = app_language.replace('\n', '').replace(' ', '')
        # print(app_language)

        # app_update_text = response.xpath()
        # app_update_text = app_update_text.replace('\n', '').replace(' ', '')
        # print(app_update_text)

        # app_comments = response.xpath()
        # app_comments = app_comments.replace('\n', '').replace(' ', '')
        # print(app_comments)

        # app_deal_comments = response.xpath()
        # app_deal_comments = app_deal_comments.replace(
        #     '\n', '').replace(' ', '')
        # print(app_deal_comments)

        # app_and_other_apps = response.xpath()
        # app_and_other_apps = app_and_other_apps.replace(
        #     '\n', '').replace(' ', '')
        # print(app_and_other_apps)

        # app_download_number = response.xpath()
        # app_download_number = app_download_number.replace(
        #     '\n', '').replace(' ', '')
        # print(app_download_number)

        # app_all_version_rating = response.xpath()
        # app_all_version_rating = app_all_version_rating.replace(
        #     '\n', '').replace(' ', '')
        # print(app_all_version_rating)

        # app_all_version_rating_number = response.xpath()
        # app_all_version_rating_number = app_all_version_rating_number.replace(
        #     '\n', '').replace(' ', '')
        # print(app_all_version_rating_number)

        # app_current_version_rating = response.xpath()
        # app_current_version_rating = app_current_version_rating.replace(
        #     '\n', '').replace(' ', '')
        # print(app_current_version_rating)

        # app_current_version_rating_number = response.xpath()
        # app_current_version_rating_number = app_current_version_rating_number.replace(
        #     '\n', '').replace(' ', '')
        # print(app_current_version_rating_number)

        # app_version_name = response.xpath()
        # app_version_name = app_version_name.replace('\n', '').replace(' ', '')
        # print(app_version_name)

        # app_update_time = response.xpath()
        # app_update_time = app_update_time.replace('\n', '').replace(' ', '')
        # print(app_update_time)

        # app_copyright_text = response.xpath()
        # app_copyright_text = app_copyright_text.replace(
        #     '\n', '').replace(' ', '')
        # print(app_copyright_text)

        # app_url_id = response.xpath()
        # app_url_id = app_url_id.replace('\n', '').replace(' ', '')
        # print(app_url_id)
