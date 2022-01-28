from ssl import ALERT_DESCRIPTION_DECOMPRESSION_FAILURE
from django.urls import URLPattern, path

# path('주소',1의 인자로 갔을 때 호출할 뷰, 뷰에 전달할 키값, name=route의 이름)
from .import views
urlpatterns = [
    # 똥개훈련코드
    # # ex:/polls
    # path('', views.index, name='index'),
    # # ex:/polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),    
    # # ex:/polls/5/results
    # path('<int:question_id>/results/', views.results, name='results'),   
    # # ex:/polls/5/vote
    # path('<int:question_id>/vote/', views.vote , name='vote'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote , name='vote'),
    
]
app_name ='polls'