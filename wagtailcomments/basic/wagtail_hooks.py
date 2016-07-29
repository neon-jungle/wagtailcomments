from wagtail.contrib.modeladmin.options import modeladmin_register

from wagtailcomments.modeladmin import CommentAdmin


@modeladmin_register
class BasicCommentAdmin(CommentAdmin):
    pass
