import json
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserProfileForm, LoginForm
from myapp.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from myapp.models import *
from decimal import Decimal
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from django.http import HttpResponse
import joblib

scatter = {}
models_list = []
num_of_epoches = 30


def register(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to a login page or dashboard
    else:
        form = UserProfileForm()
    return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or dashboard
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def bathroom_create(request):
    if request.method == 'POST':
        form = BathroomApplianceForm(request.POST)
        if form.is_valid():
            bathroom_appliance = form.save(commit=False)
            bathroom_appliance.user = request.user.profile.user
            print(bathroom_appliance.user)
            bathroom_appliance.save()
            return redirect('bathroom_list')
    else:
        form = BathroomApplianceForm()
    return render(request, 'bathroom_create.html', {'form': form})


def bathroom_delete(request, bathroom_id):
    bathroom = get_object_or_404(BathroomAppliance, id=bathroom_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('bathroom_list')  # Redirect to the list view after deletion
    return render(request, 'bathroom_list.html', {'bathroom': bathroom, 'bathroom_id': bathroom_id})


def bedroom_delete(request, bedroom_id):
    bathroom = get_object_or_404(BedroomAppliance, id=bedroom_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('bedroom_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'bedroom_list.html', {'bathroom': bathroom, 'bedroom_id': bedroom_id})


def dininghall_delete(request, dininghall_id):
    bathroom = get_object_or_404(DininghallAppliance, id=dininghall_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('dininghall_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'dininghall_list.html', {'bathroom': bathroom, 'dinignhall_id': dininghall_id})


def kitchen_delete(request, kitchen_id):
    bathroom = get_object_or_404(KitchenAppliance, id=kitchen_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('kitchen_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'kitchen_list.html', {'bathroom': bathroom, 'kitchen_id': kitchen_id})


def livingroom_delete(request, livingroom_id):
    bathroom = get_object_or_404(LivingroomAppliance, id=livingroom_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('livingroom_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'livingroom_list.html', {'bathroom': bathroom, 'livingroom_id': livingroom_id})


@login_required
def kitchen_appliance_create(request):
    if request.method == 'POST':
        form = KitchenApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kitchen_appliance_list')  # Redirect to a success URL
    else:
        form = KitchenApplianceForm()
    return render(request, 'kitchen_appliance_form.html', {'form': form})


@login_required
def kitchen_appliance_list(request):
    # Retrieve all kitchen appliances from the database
    kitchen_appliances = KitchenAppliance.objects.all()
    return render(request, 'kitchen_list.html', {'kitchen_appliances': kitchen_appliances})


@login_required
def bedroom_appliance_create(request):
    if request.method == 'POST':
        form = BedroomApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bedroom_appliance_list')  # Redirect to a success URL
    else:
        form = BedroomApplianceForm()
    return render(request, 'bedroom_appliance.html', {'form': form})


@login_required
def bedroom_appliance_list(request):
    # Retrieve all kitchen appliances from the database
    bedroom_appliances = BedroomAppliance.objects.all()
    return render(request, 'bedroom_list.html', {'bedroom_appliances': bedroom_appliances})


@login_required
def dininghall_appliance(request):
    if request.method == 'POST':
        form = DininghallApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dininghall_appliance_list')  # Redirect to a success URL
    else:
        form = DininghallApplianceForm()
    return render(request, 'dininghall_appliance.html', {'form': form})


@login_required
def dininghall_appliance_list(request):
    # Retrieve all kitchen appliances from the database
    dininghall_appliances = DininghallAppliance.objects.all()
    return render(request, 'dininghall_list.html', {'dininghall_appliances': dininghall_appliances})


@login_required
def livingroom_appliance(request):
    if request.method == 'POST':
        form = LivingroomApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('livingroom_appliance_list')  # Redirect to a success URL
    else:
        form = LivingroomApplianceForm()
    return render(request, 'livingroom_appliance.html', {'form': form})


@login_required
def livingroom_appliance_list(request):
    # Retrieve all kitchen appliances from the database
    livingroom_appliances = LivingroomAppliance.objects.all()
    return render(request, 'livingroom_list.html', {'livingroom_appliances': livingroom_appliances})


@login_required
def bathroom_list(request):
    appliances = BathroomAppliance.objects.all()
    return render(request, 'bathroom_list.html', {'appliances': appliances})


# def calculate_energy_consumption(request, appliance_id):
#     # Retrieve the BathroomAppliance object
#     appliance = get_object_or_404(BathroomAppliance, pk=appliance_id)
#     total_energy_consumption = 0

#     # Calculate energy consumption for each month
#     energy_consumption = {}
#     months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
#     for month in months:
#         # Get the usage hours for the current month
#         usage_hours = getattr(appliance, month)
#         # print(usage_hours)

#         # Calculate energy consumption using the formula
#         energy_consumption[month] = appliance.wattage * usage_hours / 1000
#         # print(energy_consumption[month])
#         total_energy_consumption += energy_consumption[month]

#         print(total_energy_consumption)

#     # Pass the appliance and energy consumption dictionary to the template
#     return render(request, 'energy_consumption_result.html', {'appliance': appliance, 'energy_consumption': energy_consumption,'total_energy_consumption': total_energy_consumption , ' usage_hours': usage_hours})

@login_required
def calculate_energy_consumption(request):
    appliances = BathroomAppliance.objects.all()
    energy_results = []
    total_energy_sum = Decimal('0')  # Initialize total energy sum as a Decimal
    total_carbon_footprint = Decimal('0')  # Initialize total carbon footprint
    rate_per_kwh = Decimal('2')
    carbon_emissions_per_kwh = Decimal('0.5')  # Assume carbon emissions factor of 0.5 kgCO2/kWh

    for appliance in appliances:
        total_energy_consumption = 0
        total_carbon_for_appliance = 0
        energy_consumption = {}
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            energy_consumption[month] = appliance.wattage * usage_hours / 1000
            total_energy_consumption += energy_consumption[month]

        # Calculate carbon footprint for the current appliance
        total_carbon_for_appliance = total_energy_consumption * carbon_emissions_per_kwh
        total_carbon_footprint += total_carbon_for_appliance

        # Add current appliance's energy consumption and carbon footprint details to energy_results list
        energy_results.append({
            'appliance': appliance,
            'energy_consumption': energy_consumption,
            'total_energy_consumption': total_energy_consumption,
            'total_carbon_footprint': total_carbon_for_appliance
        })

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    # Calculate payment amount
    payment_amount = total_energy_sum * rate_per_kwh

    return render(request, 'energy_consumption_result.html', {
        'energy_results': energy_results,
        'total_energy_sum': total_energy_sum,
        'payment_amount': payment_amount,
        'total_carbon_footprint': total_carbon_footprint
    })


@login_required
def calculate_energy_consumption1(request):
    appliances = KitchenAppliance.objects.all()
    energy_results = []
    total_energy_sum = Decimal('0')  # Initialize total energy sum as a Decimal
    rate_per_kwh = Decimal('2')
    carbon_footprint_per_kwh = Decimal('0.5')  # Carbon footprint per kWh

    total_carbon_footprint = Decimal('0')  # Initialize total carbon footprint

    for appliance in appliances:
        total_energy_consumption = 0
        energy_consumption = {}
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            energy_consumption[month] = appliance.wattage * usage_hours / 1000
            total_energy_consumption += energy_consumption[month]

        # Calculate carbon footprint for the current appliance
        appliance_carbon_footprint = total_energy_consumption * carbon_footprint_per_kwh

        # Add current appliance's carbon footprint to the total
        total_carbon_footprint += appliance_carbon_footprint

        energy_results.append({
            'appliance': appliance,
            'energy_consumption': energy_consumption,
            'total_energy_consumption': total_energy_consumption,
            'carbon_footprint': appliance_carbon_footprint  # Include carbon footprint for each appliance
        })

        total_energy_sum += total_energy_consumption  # Add current appliance's energy consumption to the total sum
        payment_amount = total_energy_sum * rate_per_kwh

    return render(request, 'energy_consumption_result1.html', {
        'energy_results': energy_results,
        'total_energy_sum': total_energy_sum,
        'payment_amount': payment_amount,
        'total_carbon_footprint': total_carbon_footprint  # Pass total carbon footprint to the template
    })


def model_manual_learning(scatter):
    for key in scatter:
        scatter[key] -= scatter[key] / num_of_epoches
    return scatter


@login_required
def calculate_energy_consumption2(request):
    appliances = BedroomAppliance.objects.all()
    energy_results = []
    total_energy_sum = Decimal('0')  # Initialize total energy sum as a Decimal
    rate_per_kwh = Decimal('2')
    carbon_footprint_per_kwh = Decimal('0.5')  # Carbon footprint per kWh

    total_carbon_footprint = Decimal('0')  # Initialize total carbon footprint

    for appliance in appliances:
        total_energy_consumption = 0
        energy_consumption = {}
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            energy_consumption[month] = appliance.wattage * usage_hours / 1000
            total_energy_consumption += energy_consumption[month]

        # Calculate carbon footprint for the current appliance
        appliance_carbon_footprint = total_energy_consumption * carbon_footprint_per_kwh

        # Add current appliance's carbon footprint to the total
        total_carbon_footprint += appliance_carbon_footprint

        energy_results.append({'appliance': appliance, 'energy_consumption': energy_consumption,
                               'total_energy_consumption': total_energy_consumption,
                               'carbon_footprint': appliance_carbon_footprint})
        total_energy_sum += total_energy_consumption  # Add current appliance's energy consumption to the total sum
        payment_amount = total_energy_sum * rate_per_kwh

    return render(request, 'energy_consumption_result2.html',
                  {'energy_results': energy_results, 'total_energy_sum': total_energy_sum,
                   'payment_amount': payment_amount, 'total_carbon_footprint': total_carbon_footprint})


@login_required
def calculate_energy_consumption3(request):
    appliances = DininghallAppliance.objects.all()
    energy_results = []
    total_energy_sum = Decimal('0')  # Initialize total energy sum as a Decimal
    rate_per_kwh = Decimal('2')
    carbon_footprint_per_kwh = Decimal('0.5')  # Carbon footprint per kWh

    total_carbon_footprint = Decimal('0')  # Initialize total carbon footprint

    for appliance in appliances:
        total_energy_consumption = 0
        energy_consumption = {}
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            energy_consumption[month] = appliance.wattage * usage_hours / 1000
            total_energy_consumption += energy_consumption[month]

        # Calculate carbon footprint for the current appliance
        appliance_carbon_footprint = total_energy_consumption * carbon_footprint_per_kwh

        # Add current appliance's carbon footprint to the total
        total_carbon_footprint += appliance_carbon_footprint

        energy_results.append({'appliance': appliance, 'energy_consumption': energy_consumption,
                               'total_energy_consumption': total_energy_consumption,
                               'carbon_footprint': appliance_carbon_footprint})
        total_energy_sum += total_energy_consumption  # Add current appliance's energy consumption to the total sum
        payment_amount = total_energy_sum * rate_per_kwh

    return render(request, 'energy_consumption_result3.html',
                  {'energy_results': energy_results, 'total_energy_sum': total_energy_sum,
                   'payment_amount': payment_amount, 'total_carbon_footprint': total_carbon_footprint})


@login_required
def calculate_energy_consumption4(request):
    appliances = LivingroomAppliance.objects.all()
    energy_results = []
    total_energy_sum = Decimal('0')  # Initialize total energy sum as a Decimal
    rate_per_kwh = Decimal('2')
    carbon_footprint_per_kwh = Decimal('0.5')  # Carbon footprint per kWh

    total_carbon_footprint = Decimal('0')  # Initialize total carbon footprint

    for appliance in appliances:
        total_energy_consumption = 0
        energy_consumption = {}
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            energy_consumption[month] = appliance.wattage * usage_hours / 1000
            total_energy_consumption += energy_consumption[month]

        # Calculate carbon footprint for the current appliance
        appliance_carbon_footprint = total_energy_consumption * carbon_footprint_per_kwh

        # Add current appliance's carbon footprint to the total
        total_carbon_footprint += appliance_carbon_footprint

        energy_results.append({'appliance': appliance, 'energy_consumption': energy_consumption,
                               'total_energy_consumption': total_energy_consumption,
                               'carbon_footprint': appliance_carbon_footprint})
        total_energy_sum += total_energy_consumption  # Add current appliance's energy consumption to the total sum
        payment_amount = total_energy_sum * rate_per_kwh

    return render(request, 'energy_consumption_result4.html',
                  {'energy_results': energy_results, 'total_energy_sum': total_energy_sum,
                   'payment_amount': payment_amount, 'total_carbon_footprint': total_carbon_footprint})


@login_required
def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def piechart(request):
    appliances = BathroomAppliance.objects.all()
    energy_results = []  # Changed variable name to energy_results
    total_energy_sum = Decimal('0')

    for appliance in appliances:
        total_energy_consumption = 0
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            total_energy_consumption += appliance.wattage * usage_hours / 1000

        energy_results.append({'appliance': appliance,
                               'total_energy_consumption': total_energy_consumption})  # Changed key name to 'appliance'

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    payment_amount = total_energy_sum * Decimal('2')  # Assuming a rate of $2 per kWh

    return render(request, 'bathroom_piechart.html', {'energy_results': energy_results,
                                                      'payment_amount': payment_amount})  # Corrected context variable name


def piechart1(request):
    appliances = BedroomAppliance.objects.all()
    energy_results = []  # Changed variable name to energy_results
    total_energy_sum = Decimal('0')

    for appliance in appliances:
        total_energy_consumption = 0
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            total_energy_consumption += appliance.wattage * usage_hours / 1000

        energy_results.append({'appliance': appliance,
                               'total_energy_consumption': total_energy_consumption})  # Changed key name to 'appliance'

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    payment_amount = total_energy_sum * Decimal('2')  # Assuming a rate of $2 per kWh

    return render(request, 'bedroom_piechart.html', {'energy_results': energy_results,
                                                     'payment_amount': payment_amount})  # Corrected context variable name\


def piechart2(request):
    appliances = KitchenAppliance.objects.all()
    energy_results = []  # Changed variable name to energy_results
    total_energy_sum = Decimal('0')

    for appliance in appliances:
        total_energy_consumption = 0
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            total_energy_consumption += appliance.wattage * usage_hours / 1000

        energy_results.append({'appliance': appliance,
                               'total_energy_consumption': total_energy_consumption})  # Changed key name to 'appliance'

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    payment_amount = total_energy_sum * Decimal('2')  # Assuming a rate of $2 per kWh

    return render(request, 'kitchen_piechart.html', {'energy_results': energy_results,
                                                     'payment_amount': payment_amount})  # Corrected context variable name


def piechart3(request):
    appliances = DininghallAppliance.objects.all()
    energy_results = []  # Changed variable name to energy_results
    total_energy_sum = Decimal('0')

    for appliance in appliances:
        total_energy_consumption = 0
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            total_energy_consumption += appliance.wattage * usage_hours / 1000

        energy_results.append({'appliance': appliance,
                               'total_energy_consumption': total_energy_consumption})  # Changed key name to 'appliance'

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    payment_amount = total_energy_sum * Decimal('2')  # Assuming a rate of $2 per kWh

    return render(request, 'dininghall_piechart.html', {'energy_results': energy_results,
                                                        'payment_amount': payment_amount})  # Corrected context variable name


def piechart4(request):
    appliances = LivingroomAppliance.objects.all()
    energy_results = []  # Changed variable name to energy_results
    total_energy_sum = Decimal('0')

    for appliance in appliances:
        total_energy_consumption = 0
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            total_energy_consumption += appliance.wattage * usage_hours / 1000

        energy_results.append({'appliance': appliance,
                               'total_energy_consumption': total_energy_consumption})  # Changed key name to 'appliance'

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    payment_amount = total_energy_sum * Decimal('2')  # Assuming a rate of $2 per kWh

    return render(request, 'livingroom_piechart.html', {'energy_results': energy_results,
                                                        'payment_amount': payment_amount})  # Corrected context variable name


def scatterplot(request):
    appliances = BathroomAppliance.objects.all()
    energy_results = []  # Changed variable name to energy_results
    total_energy_sum = Decimal('0')

    for appliance in appliances:
        total_energy_consumption = 0
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            total_energy_consumption += appliance.wattage * usage_hours / 1000

        energy_results.append({'appliance': appliance,
                               'total_energy_consumption': total_energy_consumption})  # Changed key name to 'appliance'

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    payment_amount = total_energy_sum * Decimal('2')  # Assuming a rate of $2 per kWh

    return render(request, 'scatterplot.html', {'energy_results': energy_results,
                                                'payment_amount': payment_amount})  # Corrected context variable name


def scatterplot1(request):
    appliances = BedroomAppliance.objects.all()
    energy_results = []  # Changed variable name to energy_results
    total_energy_sum = Decimal('0')

    for appliance in appliances:
        total_energy_consumption = 0
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            total_energy_consumption += appliance.wattage * usage_hours / 1000

        energy_results.append({'appliance': appliance,
                               'total_energy_consumption': total_energy_consumption})  # Changed key name to 'appliance'

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    payment_amount = total_energy_sum * Decimal('2')  # Assuming a rate of $2 per kWh

    return render(request, 'scatterplot1.html', {'energy_results': energy_results,
                                                 'payment_amount': payment_amount})  # Corrected context variable name


def scatterplot2(request):
    appliances = KitchenAppliance.objects.all()
    energy_results = []  # Changed variable name to energy_results
    total_energy_sum = Decimal('0')

    for appliance in appliances:
        total_energy_consumption = 0
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            total_energy_consumption += appliance.wattage * usage_hours / 1000

        energy_results.append({'appliance': appliance,
                               'total_energy_consumption': total_energy_consumption})  # Changed key name to 'appliance'

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    payment_amount = total_energy_sum * Decimal('2')  # Assuming a rate of $2 per kWh

    return render(request, 'scatterplot2.html', {'energy_results': energy_results,
                                                 'payment_amount': payment_amount})  # Corrected context variable name


def scatterplot3(request):
    appliances = DininghallAppliance.objects.all()
    energy_results = []  # Changed variable name to energy_results
    total_energy_sum = Decimal('0')

    for appliance in appliances:
        total_energy_consumption = 0
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            total_energy_consumption += appliance.wattage * usage_hours / 1000

        energy_results.append({'appliance': appliance,
                               'total_energy_consumption': total_energy_consumption})  # Changed key name to 'appliance'

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    payment_amount = total_energy_sum * Decimal('2')  # Assuming a rate of $2 per kWh

    return render(request, 'scatterplot3.html', {'energy_results': energy_results,
                                                 'payment_amount': payment_amount})  # Corrected context variable name


def scatterplot4(request):
    appliances = LivingroomAppliance.objects.all()
    energy_results = []  # Changed variable name to energy_results
    total_energy_sum = Decimal('0')

    for appliance in appliances:
        total_energy_consumption = 0
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            total_energy_consumption += appliance.wattage * usage_hours / 1000

        energy_results.append({'appliance': appliance,
                               'total_energy_consumption': total_energy_consumption})  # Changed key name to 'appliance'

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    payment_amount = total_energy_sum * Decimal('2')  # Assuming a rate of $2 per kWh

    return render(request, 'scatterplot4.html', {'energy_results': energy_results,
                                                 'payment_amount': payment_amount})  # Corrected context variable name


def Random_forest(request):
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split, RandomizedSearchCV
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error
    df = pd.DataFrame(data)
    optimized_data = df.sum(axis=1)
    features = df.drop(columns='Target')  # Features are all columns except the target column
    target = df['Target']  # Target variable
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    }
    rf_model = RandomForestRegressor(random_state=42)
    rf_random = RandomizedSearchCV(estimator=rf_model, param_distributions=param_grid, n_iter=100, cv=3, verbose=2,
                                   random_state=42, n_jobs=-1)
    rf_random.fit(X_train_scaled, y_train)
    best_params = rf_random.best_params_
    # Example: Train Random Forest model with optimized hyperparameters
    rf_model = RandomForestRegressor(**best_params)
    rf_model.fit(X_train_scaled, y_train)
    # Example: Predictions on test set
    predictions = rf_model.predict(X_test_scaled)
    # Example: Model evaluation
    mse = mean_squared_error(y_test, predictions)
    print("Mean Squared Error:", mse)
    print("Optimized data (total energy usage for each room):")
    print(optimized_data)
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    import os
    # Generate random monthly usage data for three appliances
    appliance_labels = ['Appliance 1', 'Appliance 2', 'Appliance 3']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_usage = {}
    for label in appliance_labels:
        monthly_usage[label] = [random.randint(1, 100) for _ in range(12)]
    return render(request, 'Scatter_plot.html')


def charts(request):
    return render(request, "charts.html")


def contact(request):
    return render(request, 'contact.html')


from datetime import datetime
from django.shortcuts import render


def billings(request):
    # Get current month name and its first three letters
    current_month_name = datetime.now().strftime('%B')
    current_month_abbreviation = datetime.now().strftime('%b').lower()

    print("Current month name:", current_month_name)

    # Initialize sums dictionary to store total values for each appliance model
    sums = {}

    # Define a function for extracting data from appliance models and calculating the sum
    def extract_and_sum(appliance_model):
        data = [int(getattr(appliance, current_month_abbreviation)) for appliance in appliance_model.objects.all()]
        total = sum(data)
        sums[appliance_model.__name__.lower()] = total

    # Call the function for each appliance model
    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)

    # Get total value for the current month by summing values from all appliance models
    total_value = sum(sums.values())
    final = total_value * 3.45

    print("Total value for the current month:", final)

    # Pass the month name and total value as context
    context = {
        'current_month_name': current_month_name,
        'total_value': final
    }

    return render(request, 'billings.html', context)


import json
import json
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
import json


def extract_and_sum(appliance_model):
    data = [int(appliance.jan) for appliance in appliance_model.objects.all()]
    append.extend(data)
    total = sum(data)
    sums.append(total)
    scatter[appliance_model.__name__.lower()] = total


def random_forest(request):
    data = {
        'Bathroom': [int(appliance.jan) for appliance in BathroomAppliance.objects.all()],
        'Kitchen': [int(appliance.jan) for appliance in KitchenAppliance.objects.all()],
        'Bedroom': [int(appliance.jan) for appliance in BedroomAppliance.objects.all()],
        'Dininghall': [int(appliance.jan) for appliance in DininghallAppliance.objects.all()],
        'Livingroom': [int(appliance.jan) for appliance in LivingroomAppliance.objects.all()],
        'Target': [int(appliance.jan) for appliance in BathroomAppliance.objects.all()]
    }
    max_length = max(len(values) for values in data.values())
    for key, values in data.items():
        if len(values) < max_length:
            data[key] += [0] * (max_length - len(values))
        elif len(values) > max_length:
            data[key] = values[:max_length]
    print(data)
    df = pd.DataFrame(data)
    optimized_data = df.sum(axis=1)
    features = df.drop(columns='Target')
    target = df['Target']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    }
    rf_model = RandomForestRegressor(random_state=42)
    rf_random = RandomizedSearchCV(estimator=rf_model, param_distributions=param_grid, n_iter=100, cv=3, verbose=2,
                                   random_state=42, n_jobs=-1)
    rf_random.fit(X_train_scaled, y_train)
    best_params = rf_random.best_params_
    rf_model = RandomForestRegressor(**best_params)
    rf_model.fit(X_train_scaled, y_train)
    predictions = rf_model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, predictions)
    print("Mean Squared Error:", mse)
    print("Optimized data (total energy usage for each room):")
    print(optimized_data)
    # also the code to save the model in a folder named models
    import joblib
    joblib.dump(rf_model, 'models/random_forest_model.pkl')
    return HttpResponse("Random Forest model trained successfully!")


def k_nearest_neighbours(request):
    data = {
        'Bathroom': [int(appliance.jan) for appliance in BathroomAppliance.objects.all()],
        'Kitchen': [int(appliance.jan) for appliance in KitchenAppliance.objects.all()],
        'Bedroom': [int(appliance.jan) for appliance in BedroomAppliance.objects.all()],
        'Dininghall': [int(appliance.jan) for appliance in DininghallAppliance.objects.all()],
        'Livingroom': [int(appliance.jan) for appliance in LivingroomAppliance.objects.all()],
        'Target': [int(appliance.jan) for appliance in BathroomAppliance.objects.all()]
    }
    max_length = max(len(values) for values in data.values())
    for key, values in data.items():
        if len(values) < max_length:
            data[key] += [0] * (max_length - len(values))
        elif len(values) > max_length:
            data[key] = values[:max_length]
    df = pd.DataFrame(data)
    optimized_data = df.sum(axis=1)
    features = df.drop(columns='Target')
    target = df['Target']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    param_grid = {
        'n_neighbors': [3, 5, 7, 9],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan']
    }
    knn_model = KNeighborsRegressor()
    knn_random = RandomizedSearchCV(estimator=knn_model, param_distributions=param_grid, n_iter=100, cv=3, verbose=2,
                                    random_state=42, n_jobs=-1)
    knn_random.fit(X_train_scaled, y_train)
    best_params = knn_random.best_params_
    knn_model = KNeighborsRegressor(**best_params)
    knn_model.fit(X_train_scaled, y_train)
    predictions = knn_model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, predictions)
    print("Mean Squared Error:", mse)
    print("Optimized data (total energy usage for each room):")
    print(optimized_data)
    joblib.dump(knn_model, 'models/knn_model.pkl')
    return HttpResponse("KNN model trained successfully!")


def linear_regression(request):
    data = {
        'Bathroom': [int(appliance.jan) for appliance in BathroomAppliance.objects.all()],
        'Kitchen': [int(appliance.jan) for appliance in KitchenAppliance.objects.all()],
        'Bedroom': [int(appliance.jan) for appliance in BedroomAppliance.objects.all()],
        'Dininghall': [int(appliance.jan) for appliance in DininghallAppliance.objects.all()],
        'Livingroom': [int(appliance.jan) for appliance in LivingroomAppliance.objects.all()],
        'Target': [int(appliance.jan) for appliance in BathroomAppliance.objects.all()]
    }
    max_length = max(len(values) for values in data.values())
    for key, values in data.items():
        if len(values) < max_length:
            data[key] += [0] * (max_length - len(values))
        elif len(values) > max_length:
            data[key] = values[:max_length]
    df = pd.DataFrame(data)
    optimized_data = df.sum(axis=1)
    features = df.drop(columns='Target')
    target = df['Target']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    param_grid = {
        'fit_intercept': [True, False],
        'copy_X': [True, False],
        'positive': [True, False],
        'n_jobs': [None, 1, -1]
    }
    lr_model = LinearRegression()
    lr_random = RandomizedSearchCV(estimator=lr_model, param_distributions=param_grid, n_iter=100, cv=3, verbose=2,
                                   random_state=42, n_jobs=-1)
    lr_random.fit(X_train_scaled, y_train)
    best_params = lr_random.best_params_
    lr_model = LinearRegression(**best_params)
    lr_model.fit(X_train_scaled, y_train)
    predictions = lr_model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, predictions)
    print("Mean Squared Error:", mse)
    print("Optimized data (total energy usage for each room):")
    print(optimized_data)
    joblib.dump(lr_model, 'models/linear_regression_model.pkl')
    return HttpResponse("Linear Regression model trained successfully!")


def svm(request):
    data = {
        'Bathroom': [int(appliance.jan) for appliance in BathroomAppliance.objects.all()],
        'Kitchen': [int(appliance.jan) for appliance in KitchenAppliance.objects.all()],
        'Bedroom': [int(appliance.jan) for appliance in BedroomAppliance.objects.all()],
        'Dininghall': [int(appliance.jan) for appliance in DininghallAppliance.objects.all()],
        'Livingroom': [int(appliance.jan) for appliance in LivingroomAppliance.objects.all()],
        'Target': [int(appliance.jan) for appliance in BathroomAppliance.objects.all()]
    }
    max_length = max(len(values) for values in data.values())
    for key, values in data.items():
        if len(values) < max_length:
            data[key] += [0] * (max_length - len(values))
        elif len(values) > max_length:
            data[key] = values[:max_length]
    df = pd.DataFrame(data)
    optimized_data = df.sum(axis=1)
    features = df.drop(columns='Target')
    target = df['Target']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    param_grid = {
        'C': [0.1, 1, 10],
        'gamma': [0.01, 0.1, 1],
        'epsilon': [0.01, 0.1, 1],
        'kernel': ['linear', 'rbf']
    }
    svm_model = SVR()
    svm_random = RandomizedSearchCV(estimator=svm_model, param_distributions=param_grid, n_iter=100, cv=3, verbose=2,
                                    random_state=42, n_jobs=-1)
    svm_random.fit(X_train_scaled, y_train)
    best_params = svm_random.best_params_
    svm_model = SVR(**best_params)
    svm_model.fit(X_train_scaled, y_train)
    predictions = svm_model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, predictions)
    print("Mean Squared Error:", mse)
    print("Optimized data (total energy usage for each room):")
    print(optimized_data)
    joblib.dump(svm_model, 'models/svm_model.pkl')
    return HttpResponse("SVM model trained successfully!")


def january(request):
    sums = []
    scatter = {}
    models_list = []
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.jan) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    jan_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'jan': jan_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "january.html", context)


def february(request):
    append = []
    models_lists = []
    sums = []
    scatter = {}
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.feb) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    feb_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'feb': feb_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "february.html", context)


def march(request):
    append = []
    models_lists = []
    sums = []
    scatter = {}
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.mar) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    mar_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'mar': mar_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "march.html", context)


def may(request):
    append = []
    models_lists = []
    sums = []
    scatter = {}
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.may) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    may_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'may': may_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "may.html", context)


def april(request):
    append = []
    models_lists = []
    sums = []
    scatter = {}
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.apr) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    apr_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'apr': apr_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "april.html", context)


def june(request):
    append = []
    models_lists = []
    sums = []
    scatter = {}
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.jun) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    jun_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'jun': jun_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "june.html", context)


def july(request):
    append = []
    models_lists = []
    sums = []
    scatter = {}
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.jul) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    jul_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'jul': jul_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "july.html", context)


def august(request):
    append = []
    models_lists = []
    sums = []
    scatter = {}
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.aug) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    aug_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'aug': aug_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "august.html", context)


def september(request):
    append = []
    models_lists = []
    sums = []
    scatter = {}
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.sep) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    sep_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'sep': sep_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "september.html", context)


def october(request):
    append = []
    models_lists = []
    sums = []
    scatter = {}
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.oct) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    oct_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'oct': oct_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "october.html", context)


def november(request):
    append = []
    models_lists = []
    sums = []
    scatter = {}
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.nov) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    nov_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'nov': nov_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "november.html", context)


def december(request):
    append = []
    models_lists = []
    sums = []
    scatter = {}
    random_forest(request)
    a = joblib.load('models/random_forest_model.pkl')
    models_lists.append(a)
    k_nearest_neighbours(request)
    b = joblib.load('models/knn_model.pkl')
    models_lists.append(b)
    linear_regression(request)
    c = joblib.load('models/linear_regression_model.pkl')
    models_lists.append(c)
    svm(request)
    d = joblib.load('models/svm_model.pkl')
    models_lists.append(d)

    def extract_and_sum(appliance_model):
        data = [int(appliance.dec) for appliance in appliance_model.objects.all()]
        append.extend(data)
        total = sum(data)
        sums.append(total)
        scatter[appliance_model.__name__.lower()] = total

    extract_and_sum(BathroomAppliance)
    extract_and_sum(KitchenAppliance)
    extract_and_sum(BedroomAppliance)
    extract_and_sum(DininghallAppliance)
    extract_and_sum(LivingroomAppliance)
    dec_json = json.dumps(sums)
    scat_json = json.dumps(scatter)
    scatter = model_manual_learning(scatter)
    models_list.append(scatter)
    result_json = json.dumps(scatter)
    context = {'dec': dec_json, 'scat_json': scat_json, 'result': result_json}
    return render(request, "december.html", context)


