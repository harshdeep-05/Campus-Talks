from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from notifications.models import Notification

def upload_location(instance, filename):
    u = User.objects.get(id = instance.user_id)
    return "%s/%s" %(str(u.username), filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    bio = models.CharField(max_length = 160, blank=True)
    location = models.CharField(max_length=50, blank=True)
    dob = models.DateField(default="2016-03-03")
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    display_pic = models.ImageField(default='/media/admin/default_user_dp/dp.jpg', upload_to=upload_location, null=True, blank=True)

    def __str__(self):
        u = User.objects.get(id = self.user_id)
        return u.username

    def do_i_follow(self, query_profile):
        if query_profile in self.follows.all() or query_profile == self:
            return True
        else:
            return False

    def get_who_to_follow(self):
    	who_to_follow = []
    	users = User.objects.filter(~Q(username=self.user.username))
    	for user in users:
    		if not self.do_i_follow(user.profile):
    			who_to_follow.append(user)
    	return who_to_follow[:5]

    @property
    def notification_count(self):
        return Notification.objects.unread_count(self.user)


User.profile = property(lambda u : UserProfile.objects.get_or_create(user=u)[0])
