
import requests
from lxml import etree
import csv
import os
import pandas as pd

def init():
    if not os.path.exists('city.csv'):
        with open('city.csv', 'w', encoding='utf-8',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'city',
                'citylink'
            ])


def writerRow(row):
    with open('city.csv', 'a', encoding='utf-8',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def get_html(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/105',
        'Cookie':'QN300=s%3Dbaidu; QN1=0000f00029c4652611c824ba; QN99=2841; QN205=s%3Dbaidu; QN277=s%3Dbaidu; QN601=4fa7d46f7b6a8053886f2dfbb596345b; QN269=E434BA0077C811EF843C82B5DD30308C; QN48=0000ef002f10652611c875f9; quinn=21b6a1583407697e2ee214a668a8b780280422b1023afee9735233657403ac58b2b437b0df1a2e21cbad321fc85aa0c9; fid=7c8c2a7a-d628-46fe-a9c1-45fe6ddc405d; QN57=17268890310330.755611692279061; QunarGlobal=10.71.97.255_-6e76fc24_191e4ff1e6c_-296|1726889033552; ariaDefaultTheme=null; ctt_june=1683616182042##iK3wVK2NaUPwawPwasjNWKohWSGGaSWTEDDAXKg%3DXSg8aKkRVK2%3DWPj%3DaDGDiK3siK3saKgwWStmVKvAVKPsawPwaUvt; ctf_june=1683616182042##iK3wWKgNaUPwawPwasGTasjmWRD%2BEPGGastNXSfGasjsVDD%3DWK3sXS0RXSgwiK3siK3saKgwWStmVKvAVKP%3DWwPwaUvt; cs_june=1e980219e0683d534a30d19cbf46069033ec941755a1278b2c0696ea7a53668e2512692f08bea83a1da7cd31dff483fad146cded5d4d064159924011d1d9a977b17c80df7eee7c02a9c1a6a5b97c11794515c5114843730e0aba172f94bd9f805a737ae180251ef5be23400b098dd8ca; QN271AC=register_pc; QN271SL=fb9aec5a66b5c5531a203d85a16534ca; QN271RC=fb9aec5a66b5c5531a203d85a16534ca; _q=U.evarmpz3421; csrfToken=dX2ytlcVImGbzitekMoOvgo5Hypiyz1l; _s=s_3EHRTP4D5IK7BZDF6LBKYNOPCI; _t=28890924; _v=IQmiWVBfaFXhGlv2j21rfEw3JHKIBEqcyZ8jLAgK7Oz26lPS_KfQLN6OdRfPzKmtyaCuaGou5Vj2zxNUl-oZbg-MrIFGPU1qkHAZpvRIyer3lLX2KoUqBcKxK3dBiQ8s1Ox-m3VeXWvwoDxZtARAFgyN7sWvJBsEfGkwiuuWLyDm; QN43=""; QN42=%E5%8E%BB%E5%93%AA%E5%84%BF%E7%94%A8%E6%88%B7; _i=ueHd8ZkXXXVXbTmyd0wZVtCf9zWX; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; QN44=evarmpz3421; _vi=tpaqBxJrunb-xtgDo56QMU_X1rHBBSwutI7M-py7Zc_NLfW2Uii5egE8gtd-8qPcS9Tua3XxTCMxzXB4BZSY-F3iLJCzoJuGSR76GJ4P9MH_UoCNkNLPUEBv573s7y34d3TbrF8XcbvSGBfg04zViueOU_VDOdqM5w0gJpKcWQpq; QN71="MjAyLjExMy4xMy4xNTc65aSp5rSlOjE="; QN267=01902812965dcbfddd2; QN58=1727085461798%7C1727086215410%7C2; QN271=f2291005-4057-453c-8a4b-75fe68009507; JSESSIONID=4B7AD2C9663D12223C5CB54DC2A47312; __qt=v1%7CVTJGc2RHVmtYMS9Gd0p0cWw0d0VueEYvaEIxYTJZOWRyY2lNd2VBdjJpNmR3Qms3WVp1RW5JQ0dvZjVLZEpycjlZZ1l4TEhZeG81YXNKdlFzbE9ZWVlzSEVlRWRVTW1ubHpxUGZkdlhhb2VScDhUaTc3QVFMQXNEUlQ5b0VGcXhtMGhMTis1T0xhWGNhYndLT3I1bnF1bHpTRk5VMm02eitpaUxVNDJsQzNBPQ%3D%3D%7C1727086327262%7CVTJGc2RHVmtYMTg3SmtsenpMOUYrc0M5ZlliTnlRaXlXM3hld3ZHRGtsdGFDSEh1UEZPRjFKYnFQN01VRVBYUXh5K1o3b2lqM3lTbWVWOTZ3c3ZnVEE9PQ%3D%3D%7CVTJGc2RHVmtYMTlmUWR5anp4SGVZTEFqTUNKN21UL0xLSnlRMXJ6TE54dDljdzVzWGUxZmtObEJtbTByVlVIQlZhZlVEV1ZWcDZ1WjI1TkljblhTbG54ZFNjSmxrKzhhRXFabEYzTWtCNnBCcDBsMitieHlKTEVXZU1qTGZpemhJN2RmK1RmUVBONWp0UkRCcEUweUhiWC9xWFVTZEpFQkJLaDdUazJuNjhWSWRZYjd5UDFTNVliY3ZWWEpGcGEzMmZXMDg4Mi9MTjhuRTVQWjU2ZkZyZ21wOUNpTXZCZnJuWE1LRVBtMXdDWXI0MTI1NEdDYVhkdkpsNGJPOEgrcmVTMzcwUzVXWkN4czNHb0k0TENNZ01RZVYxTVFQQ3NzbmNHcW44YXRjZ2lTMGNoYXRPRlZMZCtiNUhSNno3ck1IRjdsYkRWNFpVZWNack9FR1ltY05iWnVEdklNcklaMUZvaU9uempTSWh3MURWOXFDT1Y3T2REUUE3N0x0NlBHVzFxa2lxa2hiS1N5NFhZbE1YY21ydzh3ZzBSZGlGdDdTbEhBdlZEWUhFbUZCb2pTWDFidHpNWXd2d0tySkdFZms5cW43NTFlYVRUNUVYMTdnYVYvSmtzN1cyTlR0YzlZV0JjMU5hay90YkNVZnVQbUNHdnJtRWJxMDAwQzZHWGQ5YUs0OFlYNG5LN3RZMkJ3RkwvOUlKSXJYWi9adi8rV0RpclA0cXNLaHFPeHhrNCtLZXBqS3BOcUVqWG1KcWJjRTVadFZHQ3lmUU9PRVFYb1ZFS2ExMXR4ZFdKdDdsL05uaHFJQk56ZlY4dWltdzFEWi9BYWtITXFiK1NlbFBLejJCWWU4VFNQZHN3MElrVjUzc1IxdGUvdkhtYTNZc01uRWtBQXVxOTRwNjg9',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response
    else:
        return None

def parse_html(response):
    route = etree.HTML(response.text)
    citylist = route.xpath('//div[@class="mp-city-content"]//li[@class="mp-city-item"]/a')
    for city in citylist:
        cityName = city.text
        cityLink = 'http://piao.qunar.com/ticket/list.htm?keyword=%s' %cityName
        writerRow([
            cityName,
            cityLink
        ])

if __name__ == '__main__':
    url = 'http://piao.qunar.com/daytrip/list.htm'
    init()
    response = get_html(url)
    parse_html(response)

# 读取CSV文件
df = pd.read_csv('city.csv')

# 去除重复数据（保留第一个出现的）
df_unique = df.drop_duplicates()



# 将处理后的数据写回CSV文件
df_unique.to_csv('city.csv', index=False)
