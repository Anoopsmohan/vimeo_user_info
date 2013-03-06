from django.db import models


class UserDetails(models.Model):
    name = models.CharField(max_length=60)
    profile_url = models.URLField()
    paying = models.BooleanField()
    staff_pick = models.BooleanField()
    staff_pick_url = models.URLField(null=True)
    video_uploaded = models.BooleanField()

    class Meta:
        ordering = ('name', )
