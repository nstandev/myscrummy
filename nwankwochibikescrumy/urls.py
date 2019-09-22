from django.conf.urls import url
from django.contrib.auth.models import User
from django.urls import path, include
from rest_framework.authtoken.models import Token
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from nwankwochibikescrumy import views
from nwankwochibikescrumy.views import MyTokenObtainPairView

app_name = 'nwankwochibikescrumy'

# router = DefaultRouter(trailing_slash=False)

router = DefaultRouter()

router.register(r'users', views.UserSerializerViewSet)
router.register(r'scrumgoals', views.ScrumyGoalsSerializerViewSet)
router.register(r'history', views.ScrumyHistorySerializerViewSet)
router.register(r'scrumusers', views.ScrumUserSerializerViewSet)
router.register(r'status', views.GoalStatusSerializerViewSet)
router.register(r'projects', views.ProjectSerializerViewSet)
router.register(r'scrumprojects', views.ProjectSerializerAuthViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('movegoal/<int:goal_id>', views.move_goal, name='movegoal'),
    path('addgoal', views.add_goal, name='addgoal'),
    path('home', views.home, name='home'),
    path('updategroup', views.update_group, name='update_group'),
    path('success', views.success, name='response'),
    path('accounts/', include('django.contrib.auth.urls')),


    # path('api', views.api_get),
    path('api/', include(router.urls)),

    # jwt paths
    url(r'^api-token-auth/$', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api-token-auth/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]

# print(include(router.urls))
# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)
# urlpatterns = format_suffix_patterns(urlpatterns)
