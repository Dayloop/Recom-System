from app.models import User, TravelInfo
import json


#获取景点信息
def getAllTravelInfoMapData(province=None):
    def map_fn(item):
        #item.img_list = json.loads(item.img_list)
        item.comments = json.loads(item.comments)
        return item

    if province:
        travelList = TravelInfo.objects.filter(province=province)
    else:
        travelList = TravelInfo.objects.all()
    travelListMap = list(map(map_fn, travelList))
    return travelListMap


#获取用户信息
def getAllUserInfoData():
    return User.objects.all()


#获取城市列表
def getCityList():
    travelList = getAllTravelInfoMapData()
    return list(set([x.province for x in travelList]))


#获取评论数据
def getAllCommentsData():
    travelList = getAllTravelInfoMapData()
    commentsList = []
    for travel in travelList:
        for comment in travel.comments:
            commentsList.append(comment)

    return commentsList
