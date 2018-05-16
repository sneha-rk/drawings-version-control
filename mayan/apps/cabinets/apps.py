from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from acls.permissions import permission_acl_edit, permission_acl_view
from common import (
    MayanAppConfig, menu_facet, menu_main, menu_multi_item, menu_object,
    menu_sidebar
)
from documents.search import document_page_search, document_search
from navigation import SourceColumn
from rest_api.classes import APIEndPoint

from .links import (
    link_cabinet_list, link_document_cabinet_list,
    link_document_cabinet_remove, link_cabinet_add_document,
    link_cabinet_add_multiple_documents, link_cabinet_child_add,
    link_cabinet_create, link_cabinet_delete, link_cabinet_edit,
    link_cabinet_view, link_custom_acl_list,
    link_multiple_document_cabinet_remove
)
from .menus import menu_cabinets
from .permissions import (
    permission_cabinet_add_document, permission_cabinet_delete,
    permission_cabinet_edit, permission_cabinet_remove_document,
    permission_cabinet_view
)
from .widgets import widget_document_cabinets


class CabinetsApp(MayanAppConfig):
    has_tests = True
    name = 'cabinets'
    verbose_name = _('Cabinets')

    def ready(self):
        super(CabinetsApp, self).ready()
        from actstream import registry

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentCabinet = self.get_model('DocumentCabinet')
        Cabinet = self.get_model('Cabinet')

        APIEndPoint(app=self, version_string='1')

        # Add explicit order_by as DocumentCabinet ordering Meta option has no
        # effect.
        Document.add_to_class(
            'document_cabinets',
            lambda document: DocumentCabinet.objects.filter(documents=document).order_by('parent__label', 'label')
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_cabinet_add_document,
                permission_cabinet_remove_document
            )
        )

        ModelPermission.register(
            model=Cabinet, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_cabinet_delete, permission_cabinet_edit,
                permission_cabinet_view, permission_cabinet_add_document,
                permission_cabinet_remove_document
            )
        )
        ModelPermission.register_inheritance(
            model=Cabinet, related='get_root',
        )

        registry.register(Cabinet)
