from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    bio = models.TextField(null=True, blank=True, verbose_name="بیوگرافی")
    job = models.CharField(max_length=250, null=True, blank=True, verbose_name="شغل", default="مدرس")
    photo = models.ImageField(upload_to="account_image/%Y/", null=True, blank=True, verbose_name="تصویر") 
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="شماره تلفن")
    following = models.ManyToManyField("self", related_name='followers', through="Contact", through_fields=('user_to', 'user_from'), symmetrical=False,  blank=True)

    def __str__(self):
        return self.username


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name="rel_from_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name="rel_to_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts", verbose_name="کاربر")
    description = models.TextField(verbose_name="توضیحات")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="user_likes", blank=True)
    saved_by = models.ManyToManyField(User, related_name="saved_posts", blank=True)
    total_likes = models.PositiveBigIntegerField(default=0)
    tags = TaggableManager()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.description
    
    def get_absolute_url(self):
        return reverse('social:post_detail', args=[self.id])
    
    def save(self, *args, **kwargs):
        self.slug = slugify('tags')
        super().save(*args, **kwargs)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="پست")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    body = models.TextField(verbose_name="متن")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return "f{self.author}: {self.post}"
    

class Ticket(models.Model):
    
    class Subject(models.TextChoices):
        OFFER = 'offer', 'پیشنهاد'
        CRITICISM = 'criticism', 'انتقاد'
        REPORT = 'report', 'گزارش'

    user = models.ForeignKey(User, related_name="tickets", on_delete=models.CASCADE, null=True)
    massage = models.TextField()
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=11)
    subject = models.CharField(max_length=250, choices=Subject.choices, default=Subject.OFFER)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.massage

    def get_absolute_url(self):
        return reverse("social:ticket_detail", kwargs={'pk': self.pk})


class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="ticket_reply")
    text = models.TextField()