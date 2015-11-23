
from django.views.generic import TemplateView
from rest_framework import routers
from duck_recruitment import views
from django.conf.urls import url, include


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'v1/dsi-individus', views.CCOURS_IndividuViewSet, base_name='dsi')
router.register(r'v1/agents', views.AgentViewSet, base_name='agents')
router.register(r'v1/ecs', views.EcViewSet, base_name='ecs')
router.register(r'v1/etapes', views.EtapeViewSet, base_name='etapes')
router.register(r'v1/etat_heure', views.EtatHeureViewSet, base_name='etat_heure')
router.register(r'v1/all_ec_annuel', views.AllEcAnnuelViewSet, base_name='all_ec_annuel')
router.register(r'v1/titulaires', views.TitulaireViewSet, base_name='titulaire')
router.register(r'v1/invitations_ec', views.InvitationEcViewSet, base_name='invitaions_ec')
router.register(r'v1/invitations_ec', views.InvitationEcViewSet, base_name='invitaions_ec')
router.register(r'v1/users', views.UserViewSet, base_name='users')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^v1/confirme_invitation$', views.ConfirmeInvitation.as_view(), name='confirme_invitation'),
    url(r'^confirme_invitation/(?P<pk>\d+)/$', TemplateView.as_view(template_name='confirmation_invitation.html')),
    url(r'^v1/summary', views.SummaryView.as_view()),

]