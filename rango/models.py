from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    # override the save() method of Category to update slug field
    # everythime the category name changes, the slug will also change.
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class UserProfile(models.Model):
    # links UserProfile to a User model instance
    user = models.OneToOneField(User)

    # additional attributes to include
    website = models.URLField(blank=True) # blank=True means they are allowed to be blank if ncessary
    picture = models.ImageField(upload_to='profile_images', blank=True) #upload_to folder will be joined with MEDIA ROOT

    # override __unicode__ method to return something meaningful
    def __unicode__(self):
        return self.user.username





