from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from wagtailcomments import registry
from wagtailcomments.models import CommentStatus
from wagtailcomments.utils import get_comment_form_class, get_return_url


def add_comment(request, content_type_pk, object_pk):
    content_type = get_object_or_404(ContentType, pk=content_type_pk)
    if content_type.model_class() not in registry:
        raise Http404
    object = get_object_or_404(content_type.model_class(), pk=object_pk)

    return_url = get_return_url(request, object)

    # Only POSTs allowed, but be nice to people instead of a HTTP 405 error
    if request.method != 'POST':
        return HttpResponseRedirect(return_url)

    # For comment systems that allow replies, etc, there might be multiple
    # forms on the page. These forms are disambiguated using a form prefix,
    # 'comment_form_prefix' should be included in the post data so we know what
    # fields to look for.
    form_prefix = request.POST.get('comment_form_prefix')
    CommentForm = get_comment_form_class()
    form = CommentForm(data=request.POST, files=request.FILES, request=request,
                       object=object, prefix=form_prefix)

    if form.is_valid():
        comment = form.save()
        if comment.status is CommentStatus.published:
            message = 'Your comment has been posted'
        else:
            # Every other type gets the same 'awaiting moderation' message,
            # regardless of whether the comment is awaiting moderation or has
            # automatically been marked as deleted
            message = 'Your comment has been added, and is awaiting moderation'
        messages.success(request, message)
        return HttpResponseRedirect(return_url)
    return TemplateResponse(request, 'wagtailcomments/add_comment.html', {
        'object': object,
        'object_type': content_type,
        'form': form,
    })
