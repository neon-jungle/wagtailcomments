from django.core.urlresolvers import reverse
from django.utils.functional import cached_property
from wagtail.wagtailadmin.site_summary import SummaryItem
from wagtail.wagtailcore import hooks

from .models import CommentStatus
from .utils import get_comment_model


class UnmoderatedCommentSummaryItem(SummaryItem):
    order = 400
    template = 'wagtailcomments/comments_summary.html'

    def get_context(self):
        url = '{url}?status__exact={status}'.format(
            url=reverse('wagtailcomments_index'),
            status=CommentStatus.moderation.name)
        return {
            'total_unmoderated_comments': self.count,
            'url': url,
        }

    def should_display(self):
        return self.count != 0

    @cached_property
    def count(self):
        return get_comment_model().objects\
            .filter(status=CommentStatus.moderation)\
            .count()


@hooks.register('construct_homepage_summary_items')
def add_documents_summary_item(request, items):
    item = UnmoderatedCommentSummaryItem(request)
    if item.should_display():
        items.append(item)
