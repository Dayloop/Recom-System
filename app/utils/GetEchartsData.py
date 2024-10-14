#GetEchartsData获取所有图表数据
from app.utils import GetPublicData
import datetime


travelInfoList = GetPublicData.getAllTravelInfoMapData()


#城市景点分析-柱状图-获取每一地点的Xdata和Ydata
def cityCharDataOne():
    cityDic = {}
    for travel in travelInfoList:
        if cityDic.get(travel.province,-1) == -1:
            cityDic[travel.province] = 1
        else:
            cityDic[travel.province] += 1
    return list(cityDic.keys()), list(cityDic.values())


#城市景点分析-饼状图-景点评分
def cityCharDataTwo():
    cityDic = {}
    for travel in travelInfoList:
        if cityDic.get(travel.score, -1) == -1:
            cityDic[travel.score] = 1
        else:
            cityDic[travel.score] += 1
    resultData = []
    for key,value in cityDic.items():
        resultData.append({
            'name':key,
            'value':value
        })
    return resultData

#评分情况分析—饼状图—star数据
def getRateCharDataOne(travelList):
    starDic = {}
    for travel in travelInfoList:
        if starDic.get(travel.star, -1) == -1:
            starDic[travel.star] = 1
        else:
            starDic[travel.star] += 1
    resultData = []
    for key, value in starDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData

#评分情况分析—饼状图—score数据
def getRateCharDataTwo(travelList):
    scoreDic = {}
    for travel in travelInfoList:
        if scoreDic.get(travel.score, -1) == -1:
            scoreDic[travel.score] = 1
        else:
            scoreDic[travel.score] += 1
    resultData = []
    for key, value in scoreDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData


#价格销量分析——折线图——景点价格
def  getPriceCharDataOne(travelList):
    xData = ['免费','100元以内','200元以内','300元以内','500元以内','500元以内','500元以外',]
    yData = [0 for x in range(len(xData))]
    for travel in travelList:
        price = float(travel.price)
        if price <= 10:
            yData[0] += 1
        elif price <= 100:
            yData[1] += 1
        elif price <= 200:
            yData[2] += 1
        elif price <= 300:
            yData[3] += 1
        elif price <= 400:
            yData[4] += 1
        elif price <= 500:
            yData[5] += 1
        elif price >= 500:
            yData[6] += 1

    return xData,yData

#价格销量分析——柱状图——销量
def getPriceCharDataTwo(travelList):
    xData = [str(x * 300) + '份以内' for x in range(1,15)]
    yData = [0 for x in range(len(xData))]
    for travel in travelList:
        saleCount = float(travel.saleCount)
        for x in range(1,15):
            count = x * 300
            if saleCount <= count:
                yData[x - 1] += 1
                break

    return xData, yData


#价格销量分析——饼图——折扣（discount）
def getPriceCharDataThree(travelList):
    discountDic = {}
    for travel in travelInfoList:
        if discountDic.get(travel.discount, -1) == -1:
            discountDic[travel.discount] = 1
        else:
            discountDic[travel.discount] += 1
    resultData = []
    for key, value in discountDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData


#评论分析——折线图——评论时间
def getCommentsCharDataOne():
    commentsList = GetPublicData.getAllCommentsData()
    xData = []
    #时间排序
    def get_list(date):
        return datetime.datetime.strptime(date, '%Y-%m-%d').timestamp()
    for comment in commentsList:
        xData.append(comment['date'])
    xData = list(set(xData))
    xData = list(sorted(xData,key=lambda x:get_list(x),reverse=True))
    yData = [0 for x in range(len(xData))]

    for comment in commentsList:
        for index,date in enumerate(xData):
            if comment['date'] == date:
                yData[index] += 1
    return xData,yData

#评论分析——饼图——评论评分
def getCommentsCharDataTwo():
    commentsList = GetPublicData.getAllCommentsData()
    scoreDic = {}
    for comment in commentsList:
        if scoreDic.get(comment['score'], -1) == -1:
            scoreDic[comment['score']] = 1
        else:
            scoreDic[comment['score']] += 1
    resultData = []
    for key, value in scoreDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData


#评论分析——柱状图——评论个数（commentsLen）
def getCommentsCharDataThree():
    travelList = GetPublicData.getAllTravelInfoMapData()
    xData = [str(x * 1000) + '条以内' for x in range(1, 30)]
    yData = [0 for x in range(len(xData))]
    for travel in travelList:
        commentsCount = float(travel.commentsLen)
        for x in range(1, 30):
            count = x * 1000
            if commentsCount <= count:
                yData[x - 1] += 1
                break

    return xData, yData