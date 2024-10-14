from app.models import TravelInfo
from app.utils.GetHomeData import getTimeNow
import json

#通过景点id获取景点全部数据
def getTravelInfoById(id):
    travel = TravelInfo.objects.get(id=id)
    #travel.img_list = json.loads(travel.img_list)
    travel.comments = json.loads(travel.comments)

    return travel

#增添评论
def addComents(commentData):

   year, month, day = getTimeNow()
   travelInfo = commentData['travelInfo']
   travelInfo.comments.append({
       'author': commentData['userInfo'].username,
       'score': commentData['rate'],
       'comment': commentData['content'],
       'date': str(year) + '-' + str(month) + '-' + str(day),
       'userId': commentData['userInfo'].id,
   })
   travelInfo.comments = json.dumps(travelInfo.comments)
   travelInfo.save()
