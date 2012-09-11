from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import Document, DocumentType

#from .settings import (AVAILABLE_MODELS, AVAILABLE_FUNCTIONS)

#available_models_string = (_(u' Available models: %s') % u','.join([name for name, model in AVAILABLE_MODELS.items()])) if AVAILABLE_MODELS else u''
#available_functions_string = (_(u' Available functions: %s') % u','.join([u'%s()' % name for name, function in AVAILABLE_FUNCTIONS.items()])) if AVAILABLE_FUNCTIONS else u''


class MetadataType(models.Model):
    """
    Define a type of metadata
    """
    name = models.CharField(unique=True, max_length=48, verbose_name=_(u'name'), help_text=_(u'Do not use python reserved words, or spaces.'))
    title = models.CharField(max_length=48, verbose_name=_(u'title'), blank=True, null=True)
    default = models.CharField(max_length=128, blank=True, null=True,
        verbose_name=_(u'default'),
        #help_text=_(u'Enter a string to be evaluated.%s') % available_functions_string)
        help_text=_(u'Enter a string to be evaluated.'))
    lookup = models.CharField(max_length=128, blank=True, null=True,
        verbose_name=_(u'lookup'),
        #help_text=_(u'Enter a string to be evaluated.  Example: [user.get_full_name() for user in User.objects.all()].%s') % available_models_string)
        help_text=_(u'Enter a string to be evaluated.  Example: [user.get_full_name() for user in User.objects.all()].'))
    #TODO: datatype?

    def __unicode__(self):
        return self.title if self.title else self.name

    class Meta:
        ordering = ('title',)
        verbose_name = _(u'metadata type')
        verbose_name_plural = _(u'metadata types')


class MetadataSet(models.Model):
    """
    Define a group of metadata types
    """
    title = models.CharField(max_length=48, verbose_name=_(u'title'))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = _(u'metadata set')
        verbose_name_plural = _(u'metadata set')


class MetadataSetItem(models.Model):
    """
    Define the set of metadata that relates to a set or group of
    metadata fields
    """
    metadata_set = models.ForeignKey(MetadataSet, verbose_name=_(u'metadata set'))
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))
    #required = models.BooleanField(default=True, verbose_name=_(u'required'))

    def __unicode__(self):
        return unicode(self.metadata_type)

    class Meta:
        verbose_name = _(u'metadata set item')
        verbose_name_plural = _(u'metadata set items')


class DocumentMetadata(models.Model):
    """
    Link a document to a specific instance of a metadata type with it's
    current value
    """
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'type'))
    value = models.CharField(max_length=256, blank=True, verbose_name=_(u'value'), db_index=True)

    def __unicode__(self):
        return unicode(self.metadata_type)

    class Meta:
        verbose_name = _(u'document metadata')
        verbose_name_plural = _(u'document metadata')


class DocumentTypeDefaults(models.Model):
    """
    Default preselected metadata types and metadata set per document
    type
    """
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    default_metadata_sets = models.ManyToManyField(MetadataSet, blank=True, verbose_name=_(u'default metadata sets'))
    default_metadata = models.ManyToManyField(MetadataType, blank=True, verbose_name=_(u'default metadata'))

    def __unicode__(self):
        return unicode(self.document_type)

    class Meta:
        verbose_name = _(u'document type defaults')
        verbose_name_plural = _(u'document types defaults')
