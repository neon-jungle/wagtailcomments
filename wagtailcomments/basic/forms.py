from django import forms

from wagtailcomments.forms import BaseCommentForm


class CommentForm(BaseCommentForm):
    class Meta(BaseCommentForm.Meta):
        fields = BaseCommentForm.Meta.fields + ['body']

    body = forms.CharField(
        widget=forms.Textarea, max_length=3000, label='Comment')
