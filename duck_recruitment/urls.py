from rest_framework import routers
from duck_recruitment import views
from .views import DeclareAgentView
from django.conf.urls import url, include

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'v1/dsi-individus', views.CCOURS_IndividuViewSet, base_name='dsi')
# router.register(r'ied-individus', views.BaseIndividuViewSet)
router.register(r'v1/agents', views.AgentViewSet, base_name='agents')
router.register(r'v1/ecs', views.EcViewSet, base_name='ecs')
router.register(r'v1/etapes', views.EtapeViewSet, base_name='etapes')
router.register(r'v1/etat_heure', views.EtatHeureViewSet, base_name='etat_heure')
router.register(r'v1/all_ec_annuel', views.AllEcAnnuel, base_name='all_ec_annuel')

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