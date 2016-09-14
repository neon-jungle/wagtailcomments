from jinja2.ext import Extension

from .templatetags import get_comment_form, get_comment_url, get_comments


class CommentExtension(Extension):

    def __init__(self, environment):
        super().__init__(environment)

        self.environment.globals.update({
            'get_comments': get_comments,
            'get_comment_form': get_comment_form,
            'get_comment_url': get_comment_url,
        })

        self.environment.filters.update({})
