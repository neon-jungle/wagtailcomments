from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from enumchoicefield import ChoiceEnum, EnumChoiceField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, MultiFieldPanel)

from . import allow_comments

COMMENT_MODEL_SETTING = 'WAGTAILCOMMENTS_MODEL'


class CommentStatus(ChoiceEnum):
    moderation = 'Awaiting moderation'
    published = 'Published'
    rejected = 'Rejected'
    deleted = 'Deleted'


class BaseCommentQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=CommentStatus.published)

    def for_object(self, object):
        return self.filter(
            object_type=ContentType.objects.get_for_model(object),
            object_id=object.pk)

    def get_for_template(self, object):
        """
        Get all the comments for an object, for use in a template.
        Subclasses can override this to provide more relevant data to the
        template, for example by returning a tree of nested comments rather
        than a queryset of flat comments.
        """
        return self.select_related('user').published().for_object(object)


class BaseComment(models.Model):
    object_id = models.TextField()
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object = GenericForeignKey('object_type', 'object_id')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.EmailField(blank=True, null=True)

    datetime = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()

    status = EnumChoiceField(CommentStatus)

    objects = BaseCommentQuerySet.as_manager()

    panels = [
        MultiFieldPanel([
            FieldPanel('user'),
            FieldRowPanel([
                FieldPanel('user_name', classname='col6'),
                FieldPanel('user_email', classname='col6'),
            ]),
        ], heading='Who'),
        FieldPanel('status'),
    ]

    class Meta:
        abstract = True
        ordering = ['datetime']

    def __str__(self):
        return '{} on {}'.format(
            self.get_name(), self.datetime.date().isoformat())

    def get_name(self):
        if self.user:
            return self.user.get_full_name() \
                or getattr(self.user, self.user.USERNAME_FIELD)
        else:
            return self.user_name


@allow_comments
class Commentable(models.Model):
    allow_comments = True
