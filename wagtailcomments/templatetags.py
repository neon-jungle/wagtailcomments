from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template import Library

from wagtailcomments.utils import get_comment_form_class, get_comment_model

register = Library()


@register.simple_tag
def get_comments(object):
    return get_comment_model().objects.get_for_template(object)


@register.simple_tag
def get_comment_form(request, object):
    form_class = get_comment_form_class()
    return form_class(request=request, object=object)


@register.simple_tag
def get_comment_url(object):
    content_type = ContentType.objects.get_for_model(object)
    return reverse('wagtailcomments:add', kwargs={
        'content_type_pk': content_type.pk, 'object_pk': object.pk})
