from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from real_estate_app.forms import LoginForm, TenantRegForm, PropertyForm, UnitForm
from real_estate_app.models import UserDetails, Property, Unit


def property_reg(request):
    """
    Api for register property
    """
    if request.method == 'GET':
        tenants = UserDetails.objects.filter(user_type='TNT').values('name', 'user_id')
        return render(request, "property_reg.html", {"tenants": tenants})
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with transaction.atomic():
                Property.objects.create(property_name=data.get('property_name'),
                                        address=data.get('address'),
                                        created_by=request.session.get('user_id'),
                                        location=data.get('location'), features=data.get('features'))
                messages.success(request, 'Property registration successful')
                return redirect('/property_reg')
        else:
            messages.error(request, form.errors)
    return render(request, 'property_reg.html')


def tenant_reg(request):
    if request.method == 'GET':
        return render(request, 'tenants.html')
    if request.method == 'POST':
        form = TenantRegForm(request.POST, request.FILES)
        if form.is_valid():
            if form.is_valid():
                form.instance.created_by = request.session.get('user_id')
                form.save()
                messages.success(request, 'Tenant created successfully')
                return redirect('/tenant_reg')
        else:
            messages.error(request, form.errors)
        return render(request, 'tenants.html')


def admin_user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Process the form data, e.g., save to the database
            email, password = form.cleaned_data.values()
            user_data = UserDetails.objects.filter(email=email, password=password).values('name', 'file', 'user_id')
            if user_data:
                property = Property.objects.all().values('property_name', 'address', 'location', 'features')
                user_data = user_data[0]
                request.session['user_id'] = user_data['user_id']
                user_data['host'] = f"http://{str(request.get_host())}/media/"
                return render(request, 'home.html', {"user_data": user_data, 'property': property})
            # Perform actions with the form data as needed
            else:
                messages.error(request, 'Invalid Credentials.')

                return render(request, 'login.html')


def unit_create(request):
    if request.method == 'GET':
        property = Property.objects.all().values('id', 'property_name')
        tenants = UserDetails.objects.filter(user_type='TNT').values('name', 'user_id')

        return render(request, 'unit.html', {"property": list(property), "tenants": list(tenants)})
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            if form.is_valid():
                data = form.cleaned_data
                Unit.objects.create(property_id=data.get('property'), rent_cost=data.get('rent_cost'),
                                    created_by=request.session.get('user_id'),
                                    unit_type=data.get('unit_type'),
                                    tenant_id=data.get('tenant'), agreement_end_date=data.get('agreement_end_date'))
                messages.success(request, 'Unit created successfully')
                return redirect('/unit_create')
        else:
            messages.error(request, form.errors)
        return render(request, 'unit.html')


def tenant_list(request):
    if request.method == 'GET':
        tenants = list(
            UserDetails.objects.filter(user_type='TNT').values('user_id', 'name', 'email', 'phone', 'address',
                                                               'file'))
        units = Unit.objects.all().values('rent_cost', 'unit_type', 'tenant', 'property__property_name',
                                          'agreement_end_date')
        for tenant in tenants:
            tenant['unit_data'] = [i for i in units if i['tenant'] == tenant['user_id']]
        return render(request, 'tenants_list.html',
                      {'tenants': tenants, 'host': f"http://{str(request.get_host())}/media/"})


def property_list(request):
    property = Property.objects.all().values('property_name', 'address', 'location', 'features')
    return render(request, 'home.html', {'property': property})
