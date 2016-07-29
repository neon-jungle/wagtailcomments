from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.crypto import constant_time_compare, salted_hmac
from ipware.ip import get_ip

from wagtailcomments.conf import settings
from wagtailcomments.models import CommentStatus
from wagtailcomments.utils import get_comment_model


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = get_comment_model()
        fields = ['user_name', 'user_email']

    def __init__(self, *args, request, **kwargs):
        self.request = request

        super().__init__(*args, **kwargs)

        # If the user is authenticated, dont bother grabbing their details
        if self.request.user.is_authenticated():
            del self.fields['user_name']
            del self.fields['user_email']

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.object = self.object
        comment.status = self.get_comment_status()

        # If the user is authenticated, attribute the comment to them
        if self.request.user.is_authenticated():
            comment.user = self.request.user

        if commit:
            comment.save()

        return comment

    def get_comment_status(self):
        """
        Get the published status of the submitted comment.

        If the current user is a staff member, the comment is automatically
        published. Otherwise, the comment is placed in the moderation queue.
        """
        user = self.request.user
        if user.is_authenticated() and user.is_staff:
            return CommentStatus.published
        else:
            return CommentStatus.moderation


class SecureCommentForm(forms.ModelForm):
    class Meta:
        model = get_comment_model()
        fields = []

    nonce = forms.CharField(widget=forms.HiddenInput())
    datestamp = forms.DateTimeField(widget=forms.HiddenInput())

    def _make_nonce(self, datestamp):
        data = '{}-{}-{}'.format(
            int(datestamp.timestamp()), self.content_type.pk, self.object.pk)
        return salted_hmac('wagtailcomments-secure-form', data).hexdigest()

    def __init__(self, *args, initial=None, **kwargs):
        self.now = timezone.now()

        initial = initial or {}
        initial.update({
            'datestamp': self.now,
            'nonce': self._make_nonce(self.now),
        })

        super().__init__(*args, initial=initial, **kwargs)

    def clean_nonce(self):
        nonce = self.cleaned_data['nonce']
        datestamp = self.cleaned_data.get('datestamp', None)
        if datestamp is not None:
            expected_nonce = self._make_nonce(datestamp)
            if not constant_time_compare(nonce, expected_nonce):
                raise forms.ValidationError('Security check failed')
        return self._make_nonce(self.now)

    def clean_datestamp(self):
        datestamp = self.cleaned_data.get('datestamp', None)
        timeout = settings.WAGTAILCOMMENTS_TIMEOUT
        if datestamp and self.now - timeout > datestamp:
            raise forms.ValidationError('The comment for has timed out')
        return self.now


class BaseCommentForm(UserCommentForm, SecureCommentForm):
    class Meta:
        model = get_comment_model()
        fields = UserCommentForm.Meta.fields + SecureCommentForm.Meta.fields

    def __init__(self, *args, object, **kwargs):
        self.object = object
        self.content_type = ContentType.objects.get_for_model(object)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.object = self.object
        comment.ip_address = get_ip(self.request)
        if commit:
            comment.save()
        return comment

    def prefix_field(self):
        if self.prefix is None:
            return ''
        return forms.widgets.HiddenInput().render(
            name='comment_form_prefix', value=self.prefix)
