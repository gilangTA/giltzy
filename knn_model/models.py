from django.db import models

# Create your models here.
class Knn(models.Model):
    performance = models.CharField(max_length=500)
    analysis = models.CharField(max_length=5000)

    def __str__(self):
        return self.performance

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username

class History(models.Model):
    id_history = models.AutoField(primary_key=True)
    hero_name = models.CharField(max_length=200)
    hero_damage = models.IntegerField(null=False)
    turret_damage = models.IntegerField(null=False)
    damage_taken = models.IntegerField(null=False)
    war_participation = models.IntegerField(null=False)
    result = models.CharField(max_length=200)

    def __str__(self):
        return self.hero_name

class Message(models.Model):
    id_message = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.message