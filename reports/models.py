from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


from users.models import BaseModel, User
from listings.models import Comment, Listing


class CommentReport(BaseModel):
    """
    A class that represents a reports of a comment
    """
    reporter = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='commentreports')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='commentreports')
    reason = models.TextField(_('Reason for reporting this comment'), blank=True, null=True)

    def __str__(self):
        return f"{self.comment} - {self.reporter}"

    def clean(self):
        if self.comment.user == self.reporter:
            raise ValidationError(_("You can not report your own comment"))


class ListingReport(BaseModel):
    """
    A class that represents a reports of a listings
    """
    reporter = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='listingreports')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listingreports')
    reason = models.TextField(_('Reason for reporting this listings'), blank=True, null=True)

    def __str__(self):
        return f"{self.listing} - {self.reporter}"

    def clean(self):
        if self.listing.user == self.reporter:
            raise ValidationError(_("You can not report your own listing"))
