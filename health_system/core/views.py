from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import json
from django.utils.timezone import localtime
from django.contrib.auth.models import User, Group
from .models import UserProfile, WellnessCoach, DailyFoodLog, WeeklyUpdate, UserQuery,WellnessCoachFeedback
from django.contrib.auth.decorators import login_required
from .forms import DailyFoodLogForm, WeeklyUpdateForm, UserQueryForm
# User Registration (End User)
def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']

        user = User.objects.create_user(username=username, password=password, email=email)
        user_profile = UserProfile.objects.create(user=user, phone_number=phone)

        # Assign End User Group
        user_group = Group.objects.get(name='End User')
        user.groups.add(user_group)

        return redirect('login')

    return render(request, 'register.html')

# Wellness Coach Registration
def register_coach(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']

        user = User.objects.create_user(username=username, password=password, email=email)
        coach_profile = WellnessCoach.objects.create(user=user, phone_number=phone, email=email)

        # Assign Wellness Coach Group
        coach_group = Group.objects.get(name='Wellness Coach')
        user.groups.add(coach_group)

        return redirect('login')

    return render(request, 'register_coach.html')

# User Login
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.groups.filter(name="Wellness Coach").exists():
                return redirect('review_queries')  # 🔥 Redirect wellness coach to their review
            return redirect('dashboard')  # Default redirect

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')


#  user_dashboard
# Role-based Dashboard
@login_required
def dashboard(request):
    if request.user.groups.filter(name="Admin").exists():
        return render(request, 'admin_dashboard.html')
    elif request.user.groups.filter(name="Wellness Coach").exists():
        # users = UserProfile.objects.all()
        # queries = UserQuery.objects.filter(response__isnull=True)  # Unanswered queries
        # return render(request, 'coach_dashboard.html', {'users': users, 'queries': queries})
        pass   ###  we currently redirecting wellness coach to review_queries
    # elif request.user.groups.filter(name="End User").exists():
    #     food_logs = DailyFoodLog.objects.filter(user__user=request.user)
    #     bmi_updates = WeeklyUpdate.objects.filter(user__user=request.user)
    #     queries = UserQuery.objects.filter(user__user=request.user)
    #     return render(request, 'user_dashboard.html', {'food_logs': food_logs, 'bmi_updates': bmi_updates, 'queries': queries})
    
    elif request.user.groups.filter(name="End User").exists():
        food_logs = DailyFoodLog.objects.filter(user__user=request.user)
        bmi_updates = WeeklyUpdate.objects.filter(user__user=request.user).order_by('-date', '-id')  # 🔥 Ensure latest entry

        # Fetch all queries related to the logged-in user
        queries = UserQuery.objects.filter(user__user=request.user).order_by('-id')
        # Prepare data for BMI chart
        dates = [update.date.strftime("%Y-%m-%d") for update in bmi_updates]
        bmi_values = [update.bmi for update in bmi_updates]
        
        # Prepare data for Food Log Chart
        food_log_dates = [log.date.strftime("%Y-%m-%d") for log in food_logs]
        food_log_times = [log.time for log in food_logs]
        food_log_counts = {}  # Count of logs for each time (morning, afternoon, etc.)
        
        for log in food_logs:
            if log.time not in food_log_counts:
                food_log_counts[log.time] = 0
            food_log_counts[log.time] += 1
        
        food_log_times_list = list(food_log_counts.keys())
        food_log_counts_list = list(food_log_counts.values())
        
        # 🔥 Get the most recent BMI update
        latest_bmi = bmi_updates.first()  # Fetch latest BMI correctly
        bmi_status = None
        bmi_alert = None

        if latest_bmi:
            bmi_status = f"Your latest BMI is {latest_bmi.bmi} ({latest_bmi.bmi_category})"

            # Set alerts for unhealthy BMI
            if latest_bmi.bmi_category in ["Underweight", "Overweight", "Obese"]:
                bmi_alert = "⚠️ Your BMI is in the " + latest_bmi.bmi_category + " range. Please consult a wellness coach!"


        # ✅ Fetch wellness coach feedback
        coach_feedbacks = request.user.user_feedbacks.all()
        coach_ratings = [feedback.rating for feedback in coach_feedbacks]
        feedback_dates = [feedback.bmi_update.date.strftime("%Y-%m-%d") for feedback in coach_feedbacks]

        return render(request, 'user_dashboard.html', {
            'food_logs': food_logs,
            'bmi_updates': bmi_updates,
            'dates': json.dumps(dates),
            'bmi_values': json.dumps(bmi_values),
            'food_log_dates': json.dumps(food_log_dates),
            'food_log_times': json.dumps(food_log_times_list),
            'food_log_counts': json.dumps(food_log_counts_list),
            'bmi_status': bmi_status,
            'bmi_alert': bmi_alert,
             'queries': queries,  # ✅ Pass queries to user_dashboard.html
             
             "coach_feedbacks": coach_feedbacks,
            "coach_ratings": coach_ratings,
           "feedback_dates": json.dumps(feedback_dates),
        })

    return render(request, 'login.html')


@login_required
def add_food_log(request):
    if request.method == "POST":
        form = DailyFoodLogForm(request.POST)
        if form.is_valid():
            food_log = form.save(commit=False)
            food_log.user = UserProfile.objects.get(user=request.user)
            food_log.save()
            return redirect('dashboard')
    else:
        form = DailyFoodLogForm()
    return render(request, 'add_food_log.html', {'form': form})

@login_required
def update_bmi(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = WeeklyUpdateForm(request.POST)
        if form.is_valid():
            bmi_update = form.save(commit=False)
            bmi_update.user = user_profile
            bmi_update.save()  # `save()` will auto-calculate BMI
            return redirect('dashboard')

    else:
        form = WeeklyUpdateForm()

    return render(request, 'update_bmi.html', {'form': form})


@login_required
def ask_query(request):
    if request.method == "POST":
        form = UserQueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.user = UserProfile.objects.get(user=request.user)
            query.save()
            return redirect('dashboard')
    else:
        form = UserQueryForm()
    return render(request, 'ask_query.html', {'form': form})


@login_required
def review_queries(request):
    if request.user.groups.filter(name="Wellness Coach").exists():  
        if request.method == "POST":
            ###  Handling User Queries
            query_id = request.POST.get('query_id')
            response_text = request.POST.get('response')
            
            if query_id and response_text:
                try:
                    query = UserQuery.objects.get(id=query_id)
                    query.response = response_text
                    query.save()
                except UserQuery.DoesNotExist:
                    pass

        # Fetch user queries
        unanswered_queries = UserQuery.objects.filter(response__isnull=True)
        answered_queries = UserQuery.objects.filter(response__isnull=False)

        return render(request, 'review_queries.html', {
            'unanswered_queries': unanswered_queries,
            'answered_queries': answered_queries,
        })

    return redirect('dashboard')

@login_required
def review_bmi_feedback(request):
    if request.user.groups.filter(name="Wellness Coach").exists():  
        if request.method == "POST":
            ###  Handling BMI and Food Log Feedback
            bmi_update_id = request.POST.get("bmi_update_id")
            rating = request.POST.get("rating")
            recommendation = request.POST.get("recommendation")
            
            if bmi_update_id and rating and recommendation:
                update = WeeklyUpdate.objects.get(id=bmi_update_id)
                WellnessCoachFeedback.objects.create(
                    coach=request.user,
                    user=update.user.user,  # ✅ Fix: Access correct user
                    bmi_update=update,
                    rating=rating,
                    recommendation=recommendation
                )

        # Fetch user data for BMI and Food Log Feedback
        bmi_updates = WeeklyUpdate.objects.all().order_by("-date")
        coach_feedbacks = WellnessCoachFeedback.objects.filter(coach=request.user)

        # Extract unique users from BMI updates
        unique_users = set(bmi_updates.values_list('user__user', flat=True))
        users = User.objects.filter(id__in=unique_users)

        return render(request, 'review_bmi_feedback.html', {
            "bmi_updates": bmi_updates,
            "coach_feedbacks": coach_feedbacks,
            "users": users,
        })

    return redirect('dashboard')