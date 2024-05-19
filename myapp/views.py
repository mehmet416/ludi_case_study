from django.shortcuts import render
from datetime import datetime, timedelta
from collections import defaultdict
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def load_users():
    with open('users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def load_simulations():
    with open('simulations.json', encoding='utf-8') as f:
        return json.load(f)

def parse_date(excel_date):
    # Convert Excel date to datetime
    try:
        base_date = datetime(1899, 12, 30)  # Excel base date
        delta = timedelta(days=float(excel_date))
        return base_date + delta
    except (ValueError, TypeError) as e:
        logging.error(f"Failed to parse date: {excel_date} - {e}")
        return None

def calculate_daily_growth(data):
    daily_data = defaultdict(list)
    for user in data['users']:
        date = parse_date(user['signup_datetime'])
        if date:
            formatted_date = date.strftime('%Y-%m-%d')
            daily_data[formatted_date].append(user['progress_percent'])

    dates = sorted(daily_data.keys())
    averages = [sum(values) / len(values) for values in daily_data.values()]
    return {'dates': dates, 'averages': averages}

def index(request):
    data = load_users()
    simulation_data = load_simulations()
    growth_data = calculate_daily_growth(data)
    total_users = len(data['users'])
    current_date = datetime.now().strftime('%Y-%m-%d')
    total_companies = len(set(simulation['company_name'] for simulation in simulation_data['simulations']))

    return render(request, 'index.html', {
        'growth_data': growth_data,
        'total_users': total_users,
        'current_date': current_date,
        'total_companies': total_companies,
    })
def format_timedelta(td):
    years = td.days // 365
    months = (td.days % 365) // 30
    days = (td.days % 365) % 30

    return f"{years} years, {months} months, {days} days"

def users(request):
    data = load_users()  # Assuming you have a function to load the JSON data
    now = datetime.utcnow()  # Get current time in UTC

    for user in data['users']:
        signup_timestamp = user['signup_datetime']
        signup_datetime = datetime.utcfromtimestamp(signup_timestamp)
        time_elapsed = now - signup_datetime
        user['time_elapsed_formatted'] = format_timedelta(time_elapsed)

    context = {'data': data['users']}  # Assuming you want to pass users data to the template
    return render(request, 'users.html', context)

def get_users(request):
    data = load_users()
    return JsonResponse(data)

def simulations(request):
    simulations_data = load_simulations()
    users_data = load_users()

    # Create dictionaries to count users and sum progress per simulation
    simulation_user_count = {}
    simulation_progress_sum = {}

    for user in users_data['users']:
        simulation_id = user['simulation_id']
        progress = user['progress_percent']

        if simulation_id in simulation_user_count:
            simulation_user_count[simulation_id] += 1
            simulation_progress_sum[simulation_id] += progress
        else:
            simulation_user_count[simulation_id] = 1
            simulation_progress_sum[simulation_id] = progress

    # Add user count and average progress to each simulation
    for simulation in simulations_data['simulations']:
        simulation_id = simulation['simulation_id']
        user_count = simulation_user_count.get(simulation_id, 0)
        total_progress = simulation_progress_sum.get(simulation_id, 0)
        average_progress = total_progress / user_count if user_count > 0 else 0

        simulation['number_of_users'] = user_count
        simulation['average_progress'] = round(average_progress, 1)
    context = {
        'simulations': simulations_data['simulations'],
        'main_bar': 'Main Bar Content',  # Replace with your actual main bar content
    }

    return render(request, 'simulations.html', context)


def companies(request):
    simulations_data = load_simulations()
    users_data = load_users()

    # Create dictionaries to store aggregate data per company
    company_simulations = {}
    company_user_count = {}
    company_progress_sum = {}

    # Initialize dictionaries with company names from simulations
    for simulation in simulations_data['simulations']:
        company_id = simulation['company_id']
        company_name = simulation['company_name']

        if company_id not in company_simulations:
            company_simulations[company_id] = {
                'company_name': company_name,
                'simulations': [],
                'total_users': 0,
                'progress_sum': 0
            }

        company_simulations[company_id]['simulations'].append(simulation['simulation_name'])

    # Aggregate data from users
    for user in users_data['users']:
        simulation_id = user['simulation_id']

        # Find the company for this simulation
        company_id = None
        for simulation in simulations_data['simulations']:
            if simulation['simulation_id'] == simulation_id:
                company_id = simulation['company_id']
                break

        if company_id:
            company_simulations[company_id]['total_users'] += 1
            company_simulations[company_id]['progress_sum'] += user['progress_percent']

    # Calculate average progress and prepare the final data for the template
    companies_list = []
    for company_id, data in company_simulations.items():
        total_users = data['total_users']
        average_progress = (data['progress_sum'] / total_users) if total_users > 0 else 0

        companies_list.append({
            'company_name': data['company_name'],
            'simulations': ', '.join(data['simulations']),
            'total_users': total_users,
            'average_progress': round(average_progress, 1)
        })

    context = {
        'companies': companies_list,
        'main_bar': 'Main Bar Content',  # Replace with your actual main bar content
    }

    return render(request, 'companies.html', context)
