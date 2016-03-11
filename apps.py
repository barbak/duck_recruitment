# coding=utf-8
from django.apps import AppConfig


class DuckRecruitment(AppConfig):
    name = "duck_recruitment"
    label = "duck_recruitment"

    collapse_settings = [{
        "group_label": "Duck_Recruitment",
        "icon": 'fa-fw fa fa-circle-o',
        "entries": [{
            "label": 'Titulaires  ',
            "icon": 'fa-fw fa fa-circle-o',
            "url": '/duck_recruitment/titulaire/',  # name or url
            "groups_permissions": [],  # facultatif
            "permissions": [],  # facultatif
        }, {
            "label": 'Type actes ',
            "icon": 'fa-fw fa fa-circle-o',
            "url": '/duck_recruitment/typeacte/',  # name or url
            "groups_permissions": [],  # facultatif
            "permissions": [],  # facultatif
        }],

        "groups_permissions": [],  # facultatif
        "permissions": [],  # facultatif
    }, ]