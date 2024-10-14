import requests
from lxml import etree
import csv
import os
import time
import re
import pandas as pd
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TARecommendation.settings")
django.setup()
from app.models import TravelInfo


class spider(object):
    def __init__(self):
        self.url = 'http://piao.qunar.com/ticket/list.json?keyword=%s&page=%s'
        self.detailUrl = 'http://piao.qunar.com/ticket/detail_%s.html'
        self.commentUrl = 'http://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=%s&pageSize=10&index=1'  #固定10条 后续可改
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/105',
            'Cookie': 'QN300=s%3Dbaidu; QN1=0000f00029c4652611c824ba; QN99=2841; QN205=s%3Dbaidu; QN277=s%3Dbaidu; QN601=4fa7d46f7b6a8053886f2dfbb596345b; QN269=E434BA0077C811EF843C82B5DD30308C; QN48=0000ef002f10652611c875f9; quinn=21b6a1583407697e2ee214a668a8b780280422b1023afee9735233657403ac58b2b437b0df1a2e21cbad321fc85aa0c9; fid=7c8c2a7a-d628-46fe-a9c1-45fe6ddc405d; QN57=17268890310330.755611692279061; QunarGlobal=10.71.97.255_-6e76fc24_191e4ff1e6c_-296|1726889033552; ariaDefaultTheme=null; ctt_june=1683616182042##iK3wVK2NaUPwawPwasjNWKohWSGGaSWTEDDAXKg%3DXSg8aKkRVK2%3DWPj%3DaDGDiK3siK3saKgwWStmVKvAVKPsawPwaUvt; ctf_june=1683616182042##iK3wWKgNaUPwawPwasGTasjmWRD%2BEPGGastNXSfGasjsVDD%3DWK3sXS0RXSgwiK3siK3saKgwWStmVKvAVKP%3DWwPwaUvt; cs_june=1e980219e0683d534a30d19cbf46069033ec941755a1278b2c0696ea7a53668e2512692f08bea83a1da7cd31dff483fad146cded5d4d064159924011d1d9a977b17c80df7eee7c02a9c1a6a5b97c11794515c5114843730e0aba172f94bd9f805a737ae180251ef5be23400b098dd8ca; QN271AC=register_pc; QN271SL=fb9aec5a66b5c5531a203d85a16534ca; QN271RC=fb9aec5a66b5c5531a203d85a16534ca; _q=U.evarmpz3421; csrfToken=dX2ytlcVImGbzitekMoOvgo5Hypiyz1l; _s=s_3EHRTP4D5IK7BZDF6LBKYNOPCI; _t=28890924; _v=IQmiWVBfaFXhGlv2j21rfEw3JHKIBEqcyZ8jLAgK7Oz26lPS_KfQLN6OdRfPzKmtyaCuaGou5Vj2zxNUl-oZbg-MrIFGPU1qkHAZpvRIyer3lLX2KoUqBcKxK3dBiQ8s1Ox-m3VeXWvwoDxZtARAFgyN7sWvJBsEfGkwiuuWLyDm; QN43=""; QN42=%E5%8E%BB%E5%93%AA%E5%84%BF%E7%94%A8%E6%88%B7; _i=ueHd8ZkXXXVXbTmyd0wZVtCf9zWX; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; QN44=evarmpz3421; _vi=PB-2LQUFja7COHfck1VOqN47Bn_SJEAdfij-j8NdJj24oWdXRBhskDqahl9U8lpydQ9-1Wx71cNcrT5sHDGD91h0s6-Yv0BrabgsQmOlp1fKpCwELPqJ-u56oU0IBgrvtHjZYc7ysiLdKW_fhctyZhCXYK8FPzyb441Sut9eV6OG; QN71="MjAyLjExMy4xMy4xNTc65bm/6KW/OjE="; QN267=019028129658044ea4e; QN58=1727085461798%7C1727088085604%7C5; JSESSIONID=0B53F65AC5E09CCF2C5B51853BFAD28C; QN271=7d74740d-cbcd-482e-8a77-cf842a90b855; __qt=v1%7CVTJGc2RHVmtYMTlFR3ZxQXpGZEtwMFV2UnFKNzkxTlBPbjQxL3crS25TT3A1NWtSTWcxZmp2eDNTdDlwci9CN2JDUU1yNzdmdHpGUlJUQ3RtMldCSzN0WE95VGJuYW16RWVrOXQ1ZFZ3YUN4N0V5b2I4bmhMWjBXbUJuZlFKakNyZHFMM3J6ZjI2NzV4czhaQVpTTk1Xc2Z6dTQxUmFCNS8wTjMvWWNVbXgwPQ%3D%3D%7C1727090822535%7CVTJGc2RHVmtYMStWKzFpRHBpT0djclRDaFUrT1FTK2ZHVGZab2F6bHlMaC93bzZBbWJGTEFFZHNrQ29uQlFISEhsU0ZRM2l0K3dDdVJzVGRRSU50NWc9PQ%3D%3D%7CVTJGc2RHVmtYMStpMHRSalVneThta0xvbEpqdW9FRXJ6YTBkd09XSVVyaEM3bzZISjZMaExQNGY4UlZaSHFBRm9kVW9XNmlISUl1TWt1VzlrSDE4N3gyeVpEbVNoYXJpQ2dMaWxkRThGK2ZzaDBvdmI3WDFLS0poaDFGSWNzUncwL3hza0hYb1V3SEFkYVUzUjVrUnRpY0xHdDN6dkMxMnpqNVpJVVRpazYzMm5teE4zVEpOK1hDeisrTVJkTDVGcU9DWmsyb1pVYnVOeDVtU0tvMldUVUwwbWJ0VC9aWlR4bit0T210eVRmcVFnSzVWaXpsVVRxbURXSG13Tm9pNHJrMzlUdmRMQlljUEF4Z1VUNTNVV1RZRXRiZWNLOTEzVnhsNFZVekdvNVFiQVdDVHdmMEdNaXdkcWJDaHFUb3BTNGs1OFVJLzhwcVBiKzJ0Z1Zrc1JzcXBoWCt6T2dNeDRnQ1JVTW00V21Oa3Y5d3ZkcHZxUk5xMGdWcWNJeDdIRi9Ed3d4MllHZW1kUFhKcEtLRDhlNzY3S1lMVDlSZzA1OVNBanBYRDJ4ZTFoTExIaUE2OUJlR0xIMlNqNXJQcVpIanFydnM0M2dmYzdjejMyeHB4clR1anptVVYra0NmTVY5ekJETFZ2YVA0YWhIV044SHhaMC9tNVFpVkR4VkI3UElvN1drTThxZHVBbUV4UkMyQzNKYmhmVG1qUFZKK2dKWW9sVlNXWFRPSnJiSzF0a2hXZDRhYkwvaHVhaU9RREtySnllakdXNFhlZkFUWElYSjFlK2U4UFc3ZkxMNWJLUENnZC9hR3d6Zy9JWVVNdjRvQWpQNDgzeTRpMEpYaTdhVDdiemF5aG9mSVVSZmY0M0VHU2JRUi9HODBWNWRTS1BxZCtHN3ZJVWM9'
        }

    def init(self):
        if not os.path.exists('tempData.csv'):
            with open('tempData.csv', 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'title',
                    #'level',
                    'province',
                    'star',
                    'detailAddress',
                    'shortIntro',
                    'detailUrl',
                    'score',
                    'price',
                    'commentsTotal',
                    'detailIntro',
                    'img_list',
                    'comments',
                    'cover',
                    'discount',
                    'saleCount'
                ])

    def send_request(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response
        else:
            return None

    def save(self, row):
        with open('tempData.csv', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)

    def spiderMain(self, resp, province):
        respJason = resp.json()['data']['sightList']
        for index, travel in enumerate(respJason):
            print('正在爬取该页第%s条' % str(index + 1))
            time.sleep(1)
            detailAddress = travel['address']
            discount = travel['discount']
            shortIntro = travel['intro']
            price = travel['qunarPrice']
            saleCount = travel['saleCount']
            title = travel['sightName']
            cover = travel['sightImgURL']
            #if travel['star']:
            #level = travel['star'] + '景区'
            #else:
            #level = '未评级'
            sightId = travel['sightId']

            #详情页面相关爬取
            detailUrl = self.detailUrl % sightId
            respDetailXpath = etree.HTML(self.send_request(detailUrl).text)
            score = respDetailXpath.xpath('//span[@id="mp-description-commentscore"]/span/text()')
            if not score:
                score = 0
                star = 0
            else:
                score = score[0]
                star = int(float(score) * 10)
            commentsTotal = respDetailXpath.xpath('//span[@class="mp-description-commentCount"]/a/text()')[0].replace(
                '条评论', '')
            detailIntro = respDetailXpath.xpath('//div[@class="mp-charact-intro"]//p/text()')[0]
            img_list = respDetailXpath.xpath('//div[@class="mp-description-image"]/img/@src')[:5]  #取前5张图片

            #评论爬取
            commentSightId = respDetailXpath.xpath('//div[@class="mp-tickets-new"]/@data-sightid')[0]
            commentUrl = self.commentUrl % commentSightId

            comments = []
            try:
                commentList = self.send_request(commentUrl).json()['data']['commentList']
                for i in commentList:
                    if i['content'] != '用户未点评，系统默认好评。':
                        author = i['author']
                        content = i['content']
                        date = i['date']
                        score = i['score']
                        comments.append({
                            'author': author,
                            'content': content,
                            'date': date,
                            'score': score,
                        })
            except:
                comments = []

            resultData = []
            resultData.append(title)
            resultData.append(province)
            resultData.append(star)
            resultData.append(detailAddress)
            resultData.append(shortIntro)
            resultData.append(detailUrl)
            resultData.append(score)
            resultData.append(price)
            resultData.append(commentsTotal)
            resultData.append(detailIntro)
            resultData.append(img_list)
            resultData.append(json.dumps(comments))
            resultData.append(cover)
            resultData.append(discount)
            resultData.append(saleCount)

            self.save(resultData)

    def start(self):
        with open('./new_city.csv', 'r', encoding='utf-8') as readerfile:
            reader = csv.reader(readerfile)
            next(reader)
            for cityData in reader:
                for page in range(1, 10):
                    try:
                        url = self.url % (cityData[0], page)
                        print('正在爬取%s 该城市的旅游数据正在%s页 路径为%s' % (
                            cityData[0],
                            page,
                            url
                        ))

                        response = self.send_request(url)
                        self.spiderMain(response, cityData[0])
                        time.sleep(3)
                    except:
                        continue

    # 将所爬取的数据存入数据库
    def save_to_sql(self):
        with open('tempData.csv', 'r', encoding='utf-8') as csvfile:
            redercsv = csv.reader(csvfile)
            next(redercsv)
            for travel in redercsv:
                TravelInfo.objects.create(
                    title=travel[0],
                    province=travel[1],
                    star=travel[2],
                    detailAddress=travel[3],
                    shortInfo=travel[4],
                    detailUrl=travel[5],
                    score=travel[6],
                    price=travel[7],
                    commentsLen=travel[8],
                    detailIntro=travel[9],
                    img_list=travel[10],
                    comments=travel[11],
                    cover=travel[12],
                    discount=travel[13],
                    saleCount=travel[14]

                )


if __name__ == '__main__':
    spiderObj = spider()
    # spiderObj.init()
    # spiderObj.start()
    spiderObj.save_to_sql()
