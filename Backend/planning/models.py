from django.db import models
from django.contrib.auth.models import User
from courses.models import Deck



# Create your models here.
class Availability(models.Model):
    DAYS=[
        ('Lundi','Monday'),
        ('Mardi','Tuesday'),
        ('Mercredi','Wednesday'),
        ('Jeudi','Thursday'),
        ('Vendredi','Friday'),
        ('Samedi','Saturday'),
        ('Dimanche','Sunday')

    ]
    day=models.CharField(max_length=20, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    def __str__(self):
        return f"{self.user.username} - {self.day}"


class RevisionPlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revision_plans')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title
    

    
class RevisionSession(models.Model):
        STATUS_CHOICES=[
            ('planned','programmé'),
            ('done','terminé'),
            ('cancelled','annulé')
        ]
        date=models.DateField()
        start_time = models.TimeField()
        end_time = models.TimeField()
        status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
        revisionPlan = models.ForeignKey(RevisionPlan, on_delete=models.CASCADE, related_name='sessions')
        deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='revision_sessions')

        def __str__(self):
            return f"{self.revisionPlan.user.username} - {self.date}"


