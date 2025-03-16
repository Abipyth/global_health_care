from django.db import models
from django.contrib.auth.models import User

# User Profile for End Users
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    wellness_coach = models.ForeignKey('WellnessCoach', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

# Wellness Coach Model
class WellnessCoach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

# Daily Food Log
class DailyFoodLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.CharField(max_length=20)  # Morning, Afternoon, Evening, Dinner
    food_description = models.TextField()

    def __str__(self):
        return f"{self.user.user.username} - {self.date} - {self.time}"

class WeeklyUpdate(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    height = models.FloatField()  # in cm
    weight = models.FloatField()  # in kg
    bmi = models.FloatField(blank=True, null=True)  # Auto-calculated
    bmi_category = models.CharField(max_length=20, blank=True, null=True)  # BMI Category

    def save(self, *args, **kwargs):
        if self.height and self.weight:
            self.bmi = round(self.weight / ((self.height / 100) ** 2), 2)
            self.bmi_category = self.get_bmi_category()
        super().save(*args, **kwargs)

    def get_bmi_category(self):
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def __str__(self):
        return f"{self.user.user.username} - {self.date} - BMI: {self.bmi} ({self.bmi_category})"

# User Queries
class UserQuery(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    query_text = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query by {self.user.user.username} on {self.created_at}"

# Coach Reviews
class CoachReview(models.Model):
    coach = models.ForeignKey(WellnessCoach, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.coach.user.username} for {self.user.user.username}"
