from app.utils import GetPublicData
import random
import time
#获取全部数据
travelMapData = GetPublicData.getAllTravelInfoMapData()
userData =     GetPublicData.getAllUserInfoData()
#获取首页三个card数据
def getHomeTagData():
    #高分景区个数
    highScoreNum = 0
    #景区总数
    TANum = 0
    #高分景区占比
    highfraction = 1
    #最大评论数
    commentsNumMax = 0
    #评论最多景区
    commentsMaxTitle = ''
    #地区景点数字典
    provinceDic = {}
    for travel in travelMapData:
        TANum += 1
        if float(travel.score) > 4.9:
            highScoreNum += 1
        if int(travel.commentsLen) >= commentsNumMax:
            commentsNumMax = int(travel.commentsLen)
            commentsMaxTitle = travel.title
        if provinceDic.get(travel.province,-1) == -1:
            provinceDic[travel.province] = 1
        else:
            provinceDic[travel.province] += 1

    provinceDicSort = list(sorted(provinceDic.items(), key=lambda x: x[1], reverse=True))[0][0]
    provinceTANum = list(sorted(provinceDic.items(), key=lambda x: x[1], reverse=True))[0][1]
    highfraction = round(highScoreNum/TANum * 100, 2)

    return highScoreNum,provinceDicSort, commentsMaxTitle,highfraction,commentsNumMax,provinceTANum


#获取首页两个排行榜数据（高分景点推荐榜，销量前十景点榜）
def getRankingData():
    #评分5.0的景区列表
    topTA = []
    for travel in travelMapData:
        if float(travel.score) == 5.0:
            topTA.append(travel)

    #top10列表
    top10TA = []
    for i in range(10):
        randomIndex = random.randint(0, len(topTA)-1)
        top10TA.append(topTA[randomIndex])

    #销量前十景点数据
    saleCountTop10 = list(sorted(travelMapData,key=lambda x:int(x.saleCount),reverse=True))[:10]

    return top10TA,saleCountTop10

#获取当前时间
def getTimeNow():
    timeFormat =time.localtime()
    year = timeFormat.tm_year
    month = timeFormat.tm_mon
    day = timeFormat.tm_mday
    return year,month,day

#获取地图数据
def getGeoData():
    pass

#获取用户创建时间数据
def getUserCreateTimeData():
    dataDic = {}
    for user in userData:
        if dataDic.get(str(user.createTime),-1) == -1:
            dataDic[str(user.createTime)] = 1
        else:
            dataDic[str(user.createTime)] += 1

    result =[]
    for key,value in dataDic.items():
        result.append({
            'name':key,
            'value':value
        })

    return result







