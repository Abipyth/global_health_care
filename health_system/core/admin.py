from django.contrib import admin
from .models import (
    UserProfile, DailyFoodLog, UserQuery, 
    WeeklyUpdate, WellnessCoach, CoachReview
)

admin.site.register(UserProfile)
admin.site.register(DailyFoodLog)
admin.site.register(UserQuery)
admin.site.register(WeeklyUpdate)
admin.site.register(WellnessCoach)
admin.site.register(CoachReview)
