from django.apps import apps
from django.utils.module_loading import import_string
from wagtail.wagtailcore.models import Page

from wagtailcomments.conf import settings
from wagtailcomments.models import COMMENT_MODEL_SETTING


def get_comment_model():
    model_string = getattr(settings, COMMENT_MODEL_SETTING)
    return apps.get_model(model_string)


def get_url_for_object(object):
    """
    """
    if isinstance(object, Page):
        return object.url
    else:
        return object.get_absolute_uri()


def get_return_url(request, object):
    suggested_url = request.POST.get('return_url')
    if suggested_url:
        # TODO Check this URL for an unsafe redirect off the site
        return suggested_url
    return get_url_for_object(object)


def get_comment_form_class():
    comment_model = get_comment_model()
    return import_string(comment_model.form_class)
