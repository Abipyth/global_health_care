from django import forms
from .models import DailyFoodLog, WeeklyUpdate, UserQuery

class DailyFoodLogForm(forms.ModelForm):
    class Meta:
        model = DailyFoodLog
        fields = ['time', 'food_description']

class WeeklyUpdateForm(forms.ModelForm):
    class Meta:
        model = WeeklyUpdate
        fields = ['height', 'weight']

class UserQueryForm(forms.ModelForm):
    class Meta:
        model = UserQuery
        fields = ['query_text']

class UserQueryResponseForm(forms.ModelForm):  # 🔥 NEW FORM for Wellness Coach
    class Meta:
        model = UserQuery
        fields = ['response']