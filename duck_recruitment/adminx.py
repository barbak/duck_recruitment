# -*- coding: utf8 -*-
from xadmin import views
import xadmin

from django.http.response import HttpResponse
from django.views.decorators.cache import never_cache
from xadmin.views import filter_hook

# from .models import Recruit

# class RecruitmentDashboard(views.Dashboard):
#     @never_cache
#     def get(self, request, *args, **kwargs):
#         self.widgets = self.get_widgets()
#         return HttpResponse("HELLLO")
#
# xadmin.site.register_view(r'^duck_recruitment_main/$', RecruitmentDashboard, 'recruitment_dashboard')

# class RecruitmentDashboard(views.website.IndexView):
#     widgets = [[{"type": "qbutton", "title": "Gestion candidats",
#                  "btns": [{'title': 'Déclaration des agents', 'url': 'declare_agent'},
# #                          {'title': 'Recrues', 'model': Recruit},
#                             {'title': 'Affectation aux EC', 'url': 'assign_ec_agent'},
#                           ]},
#                ]]
#     site_title = 'Backoffice'
#     title = 'Accueil'
#     widget_customiz = False
# xadmin.site.register_view(r'^recruitment/$', RecruitmentDashboard, 'recruitment_dashboard')

class RecruitmentDashboard(views.Dashboard):
    base_template = "duck_recruitment/declare_agent.html"
    widget_customiz = False

    def get_context(self):
        context = super(RecruitmentDashboard, self).get_context()
        # context['personnes'] = Personnel.objects.root_nodes()
        return context

    @filter_hook
    def get_breadcrumb(self):
        return [{'url': self.get_admin_url('index'), 'title': 'Accueil'},]

    @never_cache
    def get(self, request, *args, **kwargs):
        self.widgets = self.get_widgets()
        return self.template_response(self.base_template, self.get_context())

xadmin.site.register_view(r'^recruitment/$', RecruitmentDashboard, 'recruitment_dashboard')



# xadmin.site.register(Recruit)
