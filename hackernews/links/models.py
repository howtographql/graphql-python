# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Link(models.Model):
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
    posted_by = models.ForeignKey('users.User', null=True)


class Vote(models.Model):
    user = models.ForeignKey('users.User')
    link = models.ForeignKey('links.Link', related_name='votes')
