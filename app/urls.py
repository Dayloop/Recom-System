from django.urls import path
from app import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register, name='register'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout,name='logout'),
    path('changeSelfInfo/',views.changeSelfInfo,name='changeSelfInfo'),
    path('changePassword/',views.changePassword, name='changePassword'),
    path('tableData/',views.tableData,name='tableData'),
    path('addComments/<int:id>',views.addComments,name='addComments'),
    path('cityChar/',views.cityChar,name='cityChar'),
    path('rateChar/',views.rateChar,name='rateChar'),
    path('priceChar',views.priceChar,name='priceChar'),
    path('commentsChar/',views.commentsChar,name='commentsChar'),
    path('recommendation/',views.recommendation,name='recommendation'),
]