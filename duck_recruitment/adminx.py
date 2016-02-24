# -*- coding: utf8 -*-
from django.db import models
from xadmin import views
import xadmin

from django.views.decorators.cache import never_cache
from xadmin.filters import RelatedFieldListFilter
from xadmin.views import filter_hook

from duck_recruitment.models import Titulaire, TypeActe, EtapeVet, TypeEc, HeureForfait, Ec


class RecruitmentDashboard(views.Dashboard):
    base_template = "duck_recruitment/declare_agent.html"
    widget_customiz = False

    def get_context(self):
        context = super(RecruitmentDashboard, self).get_context()
        return context

    @filter_hook
    def get_breadcrumb(self):
        return [{'url': self.get_admin_url('index'), 'title': 'Accueil'},]

    @never_cache
    def get(self, request, *args, **kwargs):
        self.widgets = self.get_widgets()
        return self.template_response(self.base_template, self.get_context())

xadmin.site.register_view(r'^recruitment/$', RecruitmentDashboard, 'recruitment_dashboard')

xadmin.site.register(Titulaire)
xadmin.site.register(TypeActe)


class TypeEcsAdmin(object):
    model = TypeEc
    style = 'table'
    extra = 1

# class HeureForfaitAdmin(object):
#     model = HeureForfait
#     style = 'table'
#     extra = 1
#
#     @filter_hook
#     def formfield_for_dbfield(self, db_field, **kwargs):
#         # If it uses an intermediary model that isn't auto created, don't show
#         # a field in admin.
#         if isinstance(db_field, models.ManyToManyField) and not db_field.rel.through._meta.auto_created:
#             return None
#         attrs = self.get_field_attrs(db_field, **kwargs)
#         if db_field.name == 'type_ec':
#             kwargs['queryset'] = self.model_instance.typeec_set.all()
#         return db_field.formfield(**dict(attrs, **kwargs))
#
# class EtapeVetAdmin(object):
#     fields = ('cod_etp',)
#     readonly_fields = ('cod_etp',)
#     inlines = [TypeEcsAdmin, HeureForfaitAdmin]
#
#     def queryset(self):
#         queryset = super(EtapeVetAdmin, self).queryset()
#         return queryset.filter(cod_vrs_vet__in=[510,520])
#
#     # def
#
# class EtapeFilter(RelatedFieldListFilter):
#     def choices(self):
#         self.lookup_choices = [(x.pk, x.cod_etp.lib_etp) for x
#                                in EtapeVet.objects.filter(cod_vrs_vet__in=[510, 520]).order_by('cod_etp__lib_etp')]
#         return super(EtapeFilter, self).choices()
#
# class EcAdmin(object):
#     list_filter = [('etape', EtapeFilter)]
#     fields = ('type',)
#
#     @filter_hook
#     def formfield_for_dbfield(self, db_field, **kwargs):
#         # If it uses an intermediary model that isn't auto created, don't show
#         # a field in admin.
#         if isinstance(db_field, models.ManyToManyField) and not db_field.rel.through._meta.auto_created:
#             return None
#         attrs = self.get_field_attrs(db_field, **kwargs)
#         if db_field.name == 'type':
#             kwargs['queryset'] = self.org_obj.etape.filter(cod_vrs_vet__in=[510,520]).first().typeec_set.all()
#                 # kwargs['queryset'] = TypeEc.objects.filter(etape__pk=pk)
#                 # print kwargs['queryset']
#         return db_field.formfield(**dict(attrs, **kwargs))
#
#     def queryset(self):
#         queryset = super(EcAdmin, self).queryset()
#         return queryset.filter(etape__cod_vrs_vet__in=[510, 520])
#
# xadmin.site.register(EtapeVet, EtapeVetAdmin)
# xadmin.site.register(Ec, EcAdmin)
