from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

class Question(models.Model):
    # owner of question
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="questions")
    #gets parent question to record a series of questions
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL, blank=True)
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True,null=True)
    content = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.title}, Content: {self.content}"
    
    #return user's answer for question. If not answered, return False

    def find_user_answer(self, user_id):
        option_set = self.options.all()
        for option in option_set:
            user_answer = option.choosers.filter(id = user_id)
            if user_answer:
                return user_answer
            else:
                continue
        return False

    def add_option(self, content):
        new_option = Option(content=content)
        self.options.add(new_option, bulk=False)
        


class Option(models.Model):
    date = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True,null=True)
    image = models.FileField(upload_to='images/', blank = True, null =True)
    score = models.FloatField(blank=True, null=True, default=0.0)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name="options")
    # find out what option the user chose
    choosers = models.ManyToManyField(User, related_name="answers", null=True, blank=True)
    def __str__(self):
        return f"{self.content}, Score: {self.score}"

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE, related_name = 'information')
    location = models.CharField(max_length=20)
    bio = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank = True, null =True)
    score = models.FloatField(blank=True, null=True, default=0.0)
    followers = models.ManyToManyField(User, related_name='following', blank=True, null=True)
    def __str__(self):
        return f"On {self.location}"

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    try:
        instance.information.save()
    except ObjectDoesNotExist:
        return f"Admin logging in"