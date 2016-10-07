# -*- coding: utf-8 -*-

import scrapy

from kt_scraper.items import KtScraperItem

class KTSpider(scrapy.Spider):
    name = "KoreaTextile"
    allowed_domains = ["www.koreatextile.org"]
    start_urls = ["https://www.koreatextile.org/hki/hki3010.do;jsessionid=c2qrX31QnghQcKxvT3ZC8hnylDqzPnJhhvk4LX67bCcvcL8Xvp2G!1479840388?checkboxCode=11&kindRemark=%ED%99%94%EC%9D%B4%EB%B2%84&isTabItemFlag=&isMoreOpen=&searchCndResult=&searchCndResultTarget=&_searchCndSubCode=on&lang=ko_KR&pageIndex=" + str(i) for i in range(1, 8)]  # FIXME: Last page_no

    def parse(self, response):
        div_list = response.xpath('/html/body/div/form[2]/div/div/div[@class="list_wrap"]')
        for div in div_list:
            item = KtScraperItem()
            item["name"] = div.xpath('.//li[@class="com_name pg_highlight"]/a/text()')[0].extract().strip()
            bullets = div.xpath('.//div[@class="com_con pg_highlight"]//text()').extract()
            bullets = [bullet.strip() for bullet in bullets]
            for idx, bullet in enumerate(bullets):
                if u"주소" in bullet:
                    item["address"] = bullet.split(':')[-1].strip().replace('\t', '').replace('\r', '').replace('\n', ' ')
                elif u"연락처" in bullet:
                    item["contact"] = bullet.split(':')[-1].strip()
                elif u"홈페이지" in bullet:
                    item["homepage"] = bullets[idx+1]
                elif u"제품정보" in bullet:
                    item["product"] = bullet.split(':')[-1].strip()
                elif u"검색키워드" in bullet:
                    item["keyword"] = bullet.split(':')[-1].strip()
                elif u"인증현황" in bullet:
                    item["cert_status"] = bullet.split(':')[-1].strip().replace('\t', '').replace('\r', '').replace('\n', ' ')

            yield item
