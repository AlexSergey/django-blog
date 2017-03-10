from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from django.contrib.contenttypes.models import ContentType
from utils.word_count import get_read_time

from comments.models import Comment

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(title, filename):
    return '%s/%s' %(title, filename) # for make subfolder when image uploading

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field='width_field',
        height_field='height_field'
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)

    read_time = models.IntegerField(default=0)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    ## We need to set __unicode__ and __str__ what will be get in admin table
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    # for link name
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def get_api_url(self):
        return reverse('posts-api:detail', kwargs={'slug': self.slug})

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    class Meta:
        # for pagination we need to sort this
        ordering = ['-timestamp', '-updated']

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug

    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = create_slug(instance)
        instance.slug = slug

    if instance.content:
        html_string = instance.get_markdown()
        read_time = get_read_time(html_string)
        instance.read_time = read_time

pre_save.connect(pre_save_post_receiver, sender=Post)