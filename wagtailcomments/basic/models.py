from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from wagtailcomments.models import COMMENT_MODEL_SETTING, BaseComment


class Comment(BaseComment):
    body = models.TextField()

    form_class = 'wagtailcomments.basic.forms.CommentForm'

    panels = BaseComment.panels + [
        FieldPanel('body'),
    ]

    class Meta:
        swappable = COMMENT_MODEL_SETTING
