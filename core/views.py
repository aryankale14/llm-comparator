from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from collections import Counter

from . import ai_models
from .models import UserQuery


@login_required
def home(request):
    responses = {}
    comparison = None
    query = ""
    if request.method == "POST":
        query = request.POST.get("query")
        selected_models = request.POST.getlist("models")

        # Limit to 40 queries per 12 hours
        twelve_hours_ago = timezone.now() - timedelta(hours=12)
        recent_queries = UserQuery.objects.filter(user=request.user, timestamp__gte=twelve_hours_ago)
        if recent_queries.count() >= 40:
            messages.error(request, "Query limit reached. You can only ask 10 queries every 12 hours.")
            return render(request, "core/home.html")

        # Get responses
        if "gpt" in selected_models:
            responses["GPT-4o-mini"] = ai_models.gpt(query + " Answer clearly without extra formatting.")
        if "gemini" in selected_models:
            responses["Gemini 2.5"] = ai_models.gem(query)
        if "mistral" in selected_models:
            responses["Mistral 12B"] = ai_models.mist(query)
        if "llama" in selected_models:
            responses["LLaMA 3"] = ai_models.llama(query)

        # Perform comparison only if 2+ models were selected
        if len(responses) >= 2:
            comparison = ai_models.compare_responses(
                responses.get("GPT-4o-mini", ""),
                responses.get("Gemini 2.5", ""),
                responses.get("Mistral 12B", ""),
                responses.get("LLaMA 3", "")
            )
        else:
            comparison = "Please select at least two models for comparison."

        # Save to DB
        UserQuery.objects.create(
            user=request.user,
            query_text=query,
            model_used=", ".join(selected_models),
            gpt_response=responses.get("GPT-4o-mini", ""),
            gemini_response=responses.get("Gemini 2.5", ""),
            mistral_response=responses.get("Mistral 12B", ""),
            llama_response=responses.get("LLaMA 3", ""),
            gemini_comparison=comparison
        )

    return render(request, "core/home.html", {
        "result": responses,
        "comparison": comparison,
        "query": query
    })


@login_required
def dashboard(request):
    queries = UserQuery.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "core/dashboard.html", {"queries": queries})


@staff_member_required
def analytics(request):
    filter_option = request.GET.get("filter", "all")
    now = timezone.now()

    # Date range filtering
    if filter_option == "7d":
        start_date = now - timedelta(days=7)
    elif filter_option == "30d":
        start_date = now - timedelta(days=30)
    else:
        start_date = None

    # Apply filter to queries
    if start_date:
        filtered_queries = UserQuery.objects.filter(timestamp__gte=start_date)
    else:
        filtered_queries = UserQuery.objects.all()

    # Aggregates
    total_queries = filtered_queries.count()

    queries_per_user = (
        filtered_queries.values("user__username")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    model_stats = (
        filtered_queries.values("model_used")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    model_counter = Counter()
    for q in filtered_queries:
        for m in q.model_used.split(","):
            model_counter[m.strip().lower()] += 1

    daily_query_data = (
        filtered_queries.annotate(date=TruncDate("timestamp"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )
    daily_data = {entry["date"].strftime("%Y-%m-%d"): entry["count"] for entry in daily_query_data}

    return render(request, "core/analytics.html", {
        "total_queries": total_queries,
        "queries_per_user": queries_per_user,
        "model_stats": model_stats,
        "per_model_usage": dict(model_counter),
        "filter_option": filter_option,
        "daily_query_data": daily_data,
    })


@login_required
def query_detail(request, query_id):
    query_obj = get_object_or_404(UserQuery, id=query_id, user=request.user)
    return render(request, "core/query_detail.html", {"query": query_obj})
