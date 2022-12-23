from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    email = models.EmailField(blank=False, max_length=254)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", primary_key=True)
    comment = models.CharField("コメント", max_length=255, blank=True)

    class Meta:
        db_table = "Profile"

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def post_user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


class FriendShip(models.Model):
    following = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    follower = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["following", "follower"], name="follow_unique"
            ),
        ]

    def __str__(self):
        return f"{self.follower.username} : {self.following.username}"
