from django.shortcuts import render, redirect
from app.models import User, TravelInfo
from django.http import HttpResponse
from app.utils import GetHomeData, GetPublicData, GetChangSelfIndoData, GetAddCommentsData, GetEchartsData
from .recommendation import getUser_rating, user_bases_collaborative_filtering


#登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        try:
            User.objects.get(username=username, password=password)
            request.session['username'] = username
            return redirect('/app/home')
        except:
            return HttpResponse('用户名或密码错误')


#退出登录
def logout(request):
    request.session.clear()
    return redirect('/app/login')


#用户注册
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        #检查该用户是否已经注册
        try:
            User.objects.get(username=username)
        except:
            if not username or not email or not password or not repassword:
                return HttpResponse('不允许为空')
            if password != repassword:
                return HttpResponse('两次密码不一致')
            User.objects.create(username=username, email=email, password=password)
            return redirect('/app/login')
        return HttpResponse('该账号已存在')


#首页
def home(request):
    username = request.session['username']
    userInfo = User.objects.get(username=username)
    highScoreNum, provinceDicSort, commentsMaxTitle, highfraction, commentsNumMax, provinceTANum = GetHomeData.getHomeTagData()
    #获取首页两个排行榜数据（高分景点推荐榜，销量前十景点榜）
    top10TA, saleCountTop10 = GetHomeData.getRankingData()
    year, month, day = GetHomeData.getTimeNow()
    #获取用户创建时间数据
    userBarCharData = GetHomeData.getUserCreateTimeData()

    return render(request, 'home.html', {
        'userInfo': userInfo,
        'highScoreNum': highScoreNum,
        'provinceDicSort': provinceDicSort,
        'commentsMaxTitle': commentsMaxTitle,
        'highfraction': highfraction,
        'commentsNumMax': commentsNumMax,
        'provinceTANum': provinceTANum,
        'top10TA': top10TA,
        'nowTime': {'year': year, 'month': month, 'day': day},
        'userBarCharData': userBarCharData,
        'saleCountTop10': saleCountTop10,
    })


#个人信息修改
def changeSelfInfo(request):
    username = request.session['username']
    userInfo = User.objects.get(username=username)
    year, month, day = GetHomeData.getTimeNow()
    if request.method == "POST":
        GetChangSelfIndoData.changeSelfIndoData(username, request.POST, request.FILES)
        userInfo = User.objects.get(username=username)
    return render(request, 'changeSelfInfo.html', {
        'userInfo': userInfo,
        'nowTime': {'year': year, 'month': month, 'day': day},
    })


#修改密码
def changePassword(request):
    username = request.session['username']
    userInfo = User.objects.get(username=username)
    year, month, day = GetHomeData.getTimeNow()
    if request.method == "POST":
        res = GetChangSelfIndoData.changePassword(userInfo, request.POST)
        #待写完errorResponse去掉注释
        #if res != None:
        #return errorResponse(request,res)
    return render(request, 'changePassword.html', {
        'userInfo': userInfo,
        'nowTime': {'year': year, 'month': month, 'day': day},
    })


#数据表格
def tableData(request):
    username = request.session['username']
    userInfo = User.objects.get(username=username)
    year, month, day = GetHomeData.getTimeNow()
    tableData = GetPublicData.getAllTravelInfoMapData()
    return render(request, 'tableData.html', {
        'userInfo': userInfo,
        'nowTime': {'year': year, 'month': month, 'day': day},
        'tableData': tableData,
    })


#添加评论
def addComments(request, id):
    username = request.session['username']
    userInfo = User.objects.get(username=username)
    year, month, day = GetHomeData.getTimeNow()
    travelInfo = GetAddCommentsData.getTravelInfoById(id)
    if request.method == "POST":
        GetAddCommentsData.addComents({
            'id': id,
            'rate': int(request.POST.get('rate')),
            'content': request.POST.get('content'),
            'userInfo': userInfo,
            'travelInfo': travelInfo,
        })
        return redirect('/app/tableData')
    return render(request, 'addComments.html', {
        'userInfo': userInfo,
        'nowTime': {'year': year, 'month': month, 'day': day},
        'travelInfo': travelInfo,
        'id': id,
    })


#数据可视化——城市景点等级分析
def cityChar(request):
    username = request.session['username']
    userInfo = User.objects.get(username=username)
    year, month, day = GetHomeData.getTimeNow()
    #柱状图X、Y数据
    Xdata, Ydata = GetEchartsData.cityCharDataOne()
    #饼状图数据
    resultData = GetEchartsData.cityCharDataTwo()
    return render(request, 'cityChar.html', {
        'userInfo': userInfo,
        'nowTime': {'year': year, 'month': month, 'day': day},
        'cityCharOneData': {
            'Xdata': Xdata,
            'Ydata': Ydata,
        },
        'cityCharTwoData': resultData,
    })


#数据可视化——评分分析
def rateChar(request):
    username = request.session['username']
    userInfo = User.objects.get(username=username)
    year, month, day = GetHomeData.getTimeNow()
    #城市列表,可用于做城市选择下拉框
    cityList = GetPublicData.getCityList()
    #未进行城市选择时默认展示第一个数据
    travelList = GetPublicData.getAllTravelInfoMapData(cityList[0])
    charOneData = GetEchartsData.getRateCharDataOne(travelList)
    charTwoData = GetEchartsData.getRateCharDataTwo(travelList)

    #判断是否进行城市选择请求
    if request.method == "POST":
        travelList = GetPublicData.getAllTravelInfoMapData(request.POST.get('province'))
        #star数据
        charOneData = GetEchartsData.getRateCharDataOne(travelList)
        charTwoData = GetEchartsData.getRateCharDataTwo(travelList)

    return render(request, 'rateChar.html', {
        'userInfo': userInfo,
        'nowTime': {'year': year, 'month': month, 'day': day},
        'cityList': cityList,
        'charOneData': charOneData,
        'charTwoData': charTwoData,
    })


#数据可视化——价格销量分析（价格、销量、折扣）
def priceChar(request):
    username = request.session['username']
    userInfo = User.objects.get(username=username)
    year, month, day = GetHomeData.getTimeNow()
    # 城市列表,可用于做城市选择下拉框
    cityList = GetPublicData.getCityList()
    # 未进行城市选择时默认展示全部城市总数据
    travelList = GetPublicData.getAllTravelInfoMapData()
    #价格折线图x、y数据
    x1data, y1data = GetEchartsData.getPriceCharDataOne(travelList)
    #销量柱状图x、y数据
    x2data, y2data = GetEchartsData.getPriceCharDataTwo(travelList)
    #折扣数据
    discountPieData = GetEchartsData.getPriceCharDataThree(travelList)

    # 判断是否进行城市选择请求
    if request.method == "POST":
        travelList = GetPublicData.getAllTravelInfoMapData(request.POST.get('province'))
        x1data, y1data = GetEchartsData.getPriceCharDataOne(travelList)
        x2data, y2data = GetEchartsData.getPriceCharDataTwo(travelList)
        discountPieData = GetEchartsData.getPriceCharDataThree(travelList)

    return render(request, 'priceChar.html', {
        'userInfo': userInfo,
        'nowTime': {'year': year, 'month': month, 'day': day},
        'cityList': cityList,
        'echartsData': {
            'x1data': x1data,
            'y1data': y1data,
            'x2data': x2data,
            'y2data': y2data,
            'discountPieData': discountPieData,
        }
    })


#数据可视化——评论分析（评论时间、评论评分、评论个数）
def commentsChar(request):
    username = request.session['username']
    userInfo = User.objects.get(username=username)
    year, month, day = GetHomeData.getTimeNow()
    #评论时间折线图x、y数据
    x1Data, y1Data = GetEchartsData.getCommentsCharDataOne()
    #评论评分数据
    commentsScorePieData = GetEchartsData.getCommentsCharDataTwo()
    #评论个数数据
    x2Data, y2Data = GetEchartsData.getCommentsCharDataThree()
    return render(request, 'commentsChar.html', {
        'userInfo': userInfo,
        'nowTime': {'year': year, 'month': month, 'day': day},
        'echartsData': {
            'x1data': x1Data,
            'y1data': y1Data,
            'commentsScorePieData': commentsScorePieData,
            'x2data': x2Data,
            'y2data': y2Data,
        }
    })


#景点推荐
def recommendation(request):
    username = request.session['username']
    userInfo = User.objects.get(username=username)
    year, month, day = GetHomeData.getTimeNow()

    user_rating = getUser_rating()
    recommended = user_bases_collaborative_filtering(userInfo.id, user_rating)
    return render(request, 'recommendation.html', {
        'userInfo': userInfo,
        'nowTime': {'year': year, 'month': month, 'day': day},
        'recommended': recommended,

    })
