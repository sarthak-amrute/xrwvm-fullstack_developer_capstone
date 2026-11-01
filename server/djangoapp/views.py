import json
import logging
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """Login a user"""
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'userName': username, 'status': 'Authenticated'})
        return JsonResponse({'userName': username, 'status': 'Failed'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def logout_user(request):
    """Logout the current user"""
    logout(request)
    return JsonResponse({'userName': ''})


@csrf_exempt
def registration(request):
    """Register a new user"""
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'userName': username, 'error': 'Already Registered'})
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username, password=password,
                first_name=first_name, last_name=last_name, email=email
            )
            login(request, user)
            return JsonResponse({'userName': username, 'status': 'Authenticated'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_dealerships(request, state='All'):
    """Get all dealerships or filter by state"""
    if state == 'All':
        endpoint = '/fetchDealers'
    else:
        endpoint = f'/fetchDealers/{state}'
    
    try:
        dealerships = get_request(endpoint)
        return JsonResponse({'status': 200, 'dealers': dealerships})
    except Exception as e:
        return JsonResponse({'status': 500, 'message': str(e)})


def get_dealer_details(request, dealer_id):
    """Get details for a specific dealer"""
    try:
        endpoint = f'/fetchDealer/{dealer_id}'
        dealership = get_request(endpoint)
        return JsonResponse({'status': 200, 'dealer': dealership})
    except Exception as e:
        return JsonResponse({'status': 500, 'message': str(e)})


def get_dealer_reviews(request, dealer_id):
    """Get reviews for a specific dealer"""
    try:
        endpoint = f'/fetchReviews/dealer/{dealer_id}'
        reviews = get_request(endpoint)
        for review_detail in reviews:
            sentiment_endpoint = f'/analyze/{review_detail["review"]}'
            sentiment = analyze_review_sentiments(sentiment_endpoint)
            review_detail['sentiment'] = sentiment.get('sentiment', 'neutral')
        return JsonResponse({'status': 200, 'reviews': reviews})
    except Exception as e:
        return JsonResponse({'status': 500, 'message': str(e)})


@csrf_exempt
def add_review(request):
    """Add a review for a dealer"""
    if not request.user.is_anonymous:
        if request.method == 'POST':
            data = json.loads(request.body)
            try:
                post_review(data)
                return JsonResponse({'status': 200})
            except Exception as e:
                return JsonResponse({'status': 401, 'message': f'Error in posting review: {e}'})
    return JsonResponse({'status': 403, 'message': 'Unauthorized'})


def get_cars(request):
    """Get all car makes and models"""
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate_cars()
    car_models = CarModel.objects.select_related('car_make')
    cars = [{'CarModel': car.name, 'CarMake': car.car_make.name} for car in car_models]
    return JsonResponse({'CarModels': cars})


def get_request(endpoint, **kwargs):
    """Helper to make GET requests to the dealer microservice"""
    params = '&'.join([f'{key}={val}' for key, val in kwargs.items()])
    request_url = f'http://localhost:3000{endpoint}?{params}' if params else f'http://localhost:3000{endpoint}'
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        logger.error(f'Error getting from {request_url}: {e}')
        return []


def analyze_review_sentiments(text):
    """Call sentiment analysis microservice"""
    try:
        request_url = f'http://localhost:5000/analyze/{text}'
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        return {'sentiment': 'neutral'}


def post_review(data_dict):
    """Post a review to the dealer microservice"""
    request_url = 'http://localhost:3000/insertReview'
    try:
        response = requests.post(request_url, json=data_dict)
        return response.json()
    except Exception as e:
        logger.error(f'Error posting review: {e}')


def initiate_cars():
    """Populate initial car data"""
    cars = [
        ('Toyota', ['Prius', 'RAV4', 'Camry', 'Corolla', 'Highlander'], ['SEDAN', 'SUV', 'SEDAN', 'SEDAN', 'SUV']),
        ('Ford', ['Explorer', 'Mustang', 'F-150', 'Escape', 'Edge'], ['SUV', 'COUPE', 'TRUCK', 'SUV', 'SUV']),
        ('Honda', ['Civic', 'Accord', 'CR-V', 'Pilot', 'HR-V'], ['SEDAN', 'SEDAN', 'SUV', 'SUV', 'SUV']),
        ('Chevrolet', ['Silverado', 'Malibu', 'Equinox', 'Blazer', 'Traverse'], ['TRUCK', 'SEDAN', 'SUV', 'SUV', 'SUV']),
        ('BMW', ['3 Series', '5 Series', 'X3', 'X5', 'M3'], ['SEDAN', 'SEDAN', 'SUV', 'SUV', 'COUPE']),
    ]
    for make_name, models, types in cars:
        car_make = CarMake.objects.create(name=make_name, description=f'{make_name} vehicles')
        for i, model_name in enumerate(models):
            CarModel.objects.create(
                car_make=car_make, name=model_name,
                car_type=types[i], year=2023, dealer_id=1
            )
