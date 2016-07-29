from django.apps import apps
from django.contrib.admin.filters import RelatedFieldListFilter
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.html import format_html
from enumchoicefield.admin import EnumListFilter
from wagtail.contrib.modeladmin.helpers import AdminURLHelper, PermissionHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from wagtailcomments import registry
from wagtailcomments.utils import get_comment_model


class ContentTypeFilter(RelatedFieldListFilter):
    """An admin list filter that shows all models that can be commented on"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_models = apps.get_models()
        comment_models = [model for model in all_models if model in registry]
        content_types = ContentType.objects.get_for_models(*comment_models)
        self.lookup_choices = sorted(
            [(ct.pk, ct) for ct in content_types.values()],
            key=lambda x: x[1].model_class()._meta.verbose_name)


class NoAddPermissionHelper(PermissionHelper):
    """Comments can not be created through the admin"""
    def user_can_create(self, user):
        return False


class CommentUrlHelper(AdminURLHelper):
    def get_action_url_name(self, action):
        return 'wagtailcomments_%s' % (action)


class CommentAdmin(ModelAdmin):
    model = get_comment_model()
    menu_label = 'Comments'
    menu_icon = 'openquote'
    list_display = ['who', 'datetime', 'status']
    list_filter = [
        ('status', EnumListFilter),
        ('object_type', ContentTypeFilter),
    ]
    search_fields = ['user_name', 'user_email', 'status']

    url_helper_class = CommentUrlHelper

    permission_helper_class = NoAddPermissionHelper

    def who(self, comment):
        """
        Who made this comment. If it is a user, link to their profile in the
        admin; otherwise show their name and email address.
        """
        if comment.user:
            user = comment.user
            user_display = user.get_full_name() \
                or getattr(user, user.USERNAME_FIELD)
            try:
                # Just incase someone is running a minimal install without
                # wagtailusers installed.
                return format_html('<a href="{url}">{name}</a>'.format(
                    url=reverse('wagtailusers_users:edit', args=[user.pk]),
                    name=user_display))
            except NoReverseMatch:
                return user_display
        else:
            return '{name} ({email})'.format(name=comment.user_name,
                                             email=comment.user_email)
