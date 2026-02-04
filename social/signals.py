from .models import Post
from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail


@receiver(m2m_changed, sender=Post.likes.through)
def like_chenged(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()


@receiver(post_delete, sender=Post)
def send_email(sender, instance, **kwargs):
    subject = "post has deleted"
    message = f"your post {instance.description} has deleted!"
    send_mail(subject, message, 'samyartavakkoli87@gmail.com', [instance.author.email], fail_silently=False)


