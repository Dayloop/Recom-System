import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TARecommendation.settings")
django.setup()
from app.models import TravelInfo


#获取用户评价评分


# 获取用户评价评分
def getUser_rating():
    user_rating = {}
    for travel in TravelInfo.objects.all():
        comments = json.loads(travel.comments)
        for com in comments:
            if isinstance(com, dict):  # 确保 com 是一个字典
                user_id = com.get('userId', -1)
                if user_id != -1:
                    if user_rating.get(user_id, -1) == -1:
                        user_rating[user_id] = {travel.title: com['score']}
                    else:
                        user_rating[user_id][travel.title] = com['score']
    return user_rating


#协同过滤
def user_bases_collaborative_filtering(user_id, user_rating, top_n=3):
    # 获取目标用户评分数据
    target_user_rating = user_rating[user_id]

    # 初始化字典，用于保存其他用户与目标用户的相似度得分
    user_similarity_scores = {}

    # 目标用户的评分项目（标题）转化为列表
    target_items = list(target_user_rating.keys())

    # 计算目标用户与其他用户之间的相似度得分
    for other_user_id, other_user_ratings in user_rating.items():
        if other_user_id == user_id:
            continue

            # 将其他用户的评分转化为numpy数组（对于目标项目）
        other_user_ratings_list = np.array([
            other_user_ratings.get(item, 0) for item in target_items
        ])

        # 计算余弦相似度
        similarity_score = \
            cosine_similarity([other_user_ratings_list], [np.array(list(target_user_rating.values()))])[0][0]
        user_similarity_scores[other_user_id] = similarity_score

        # 对用户相似度得分进行降序排序
    sorted_similar_user = sorted(user_similarity_scores.items(), key=lambda x: x[1], reverse=True)

    # 选择TOP N个相似用户喜欢的景点作为推荐结果
    recommended_items = set()
    for similar_user, _ in sorted_similar_user[:top_n]:
        recommended_items.update(user_rating[similar_user].keys())

        # 过滤目标用户已经评分的景点
    recommended_items -= set(target_items)

    return list(recommended_items)


if __name__ == '__main__':
    rating = getUser_rating()
    recommend = user_bases_collaborative_filtering(1, rating, top_n=3)
    print(recommend)
#print(recommend)
