from django.db import models

# Create your models here.
class Link(models.Model):
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
    posted_by = models.ForeignKey('users.User', null=True, on_delete=models.deletion.CASCADE)


class Vote(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.deletion.CASCADE)
    link = models.ForeignKey('links.Link', related_name='votes', on_delete=models.deletion.CASCADE)
