from rest_framework import routers
from duck_recruitment import views
from .views import DeclareAgentView
from django.conf.urls import url, include

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'dsi-individus', views.CCOURS_IndividuViewSet)
# router.register(r'ied-individus', views.BaseIndividuViewSet)
router.register(r'agents', views.AgentViewSet)

urlpatterns = [
    url('^declare_agent/$',
        DeclareAgentView.as_view(),
        name='declare_agent'),
    url(r'^', include(router.urls)),
    url(r'^associate/$', views.AddAssociationView.as_view()),
    url(r'^add_agent/$', views.AddAgentView.as_view()),
    url(r'^delete_agent/$', views.DeleteAgentView.as_view()),
    url(r'^modify_agent/$', views.ModifyAgentView.as_view()),
]