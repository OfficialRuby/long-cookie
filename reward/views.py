from django.utils.crypto import get_random_string
import datetime
from django.views.generic import View
from random import randint
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from reward.models import Parameter, Device, App, Reward, Account
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class HomeView(View):
    def get(self, request, *args, **kwargs):
        response = render(request, 'home/index.html')
        if not '_longevity_anon_user' in self.request.COOKIES:
            today = datetime.datetime.today()
            a_year = datetime.timedelta(days=365)
            expires = today+a_year
            cookie_value = get_random_string(50)
            response.set_cookie('_longevity_anon_user', cookie_value, expires=expires)
            Account.objects.create(cookie=cookie_value)
        return response


class IndexView(View):
    def get(self, request, *args, **kwargs):
        try:
            cookie = request.COOKIES['_longevity_anon_user']
            if self.request.user.is_authenticated:
                reward = Reward.objects.filter(account__user=request.user).order_by('-date_awarded')
            else:
                reward = Reward.objects.filter(account__cookie=cookie).order_by('-date_awarded')

            reward_aggr = reward.aggregate(balance=Sum('reward_point'))
            context = {
                'rewards': reward,
                'reward_aggr': reward_aggr,

            }
            return render(self.request, 'dash/index.html', context)
        except KeyError:
            messages.warning(self.request, 'An error occured due to invalid or expired cookie item')
            return redirect('index')


class EarnRewardView(View):
    def get(self, request, *args, **kwargs):
        context = {

        }

        return render(self.request, 'dash/earn_reward.html', context)


class SupplyParameterView(View):
    def get(self, request, *args, **kwargs):
        context = {

        }

        return render(self.request, 'dash/supply_param.html', context)

    def post(self, request, *args, **kwargs):
        measure_instrument = request.POST.get('measure_instrument')
        height = request.POST.get('height')
        weight = request.POST.get('weight')

        form_valid = is_valid_form([measure_instrument, height, weight])
        if form_valid:
            try:

                cookie = request.COOKIES['_longevity_anon_user']
                if self.request.user.is_authenticated:
                    account = Account.objects.get(user=request.user)
                    param_obj, created = Parameter.objects.get_or_create(account=account)
                else:
                    account = Account.objects.get(cookie=cookie)
                    param_obj, created = Parameter.objects.get_or_create(account=account)
                param_obj.awarded = True
                param_obj.date_awarded = timezone.now()
                param_obj.measure_instrument = measure_instrument
                param_obj.weight = weight
                param_obj.height = height
                param_obj.save()
                messages.success(request, 'You have received 1 LONG token')
                return redirect('supply_param')
            except KeyError:
                # This will happen when cookie is missing or has expired
                messages.warning(request, 'Invalid or expired cookies, try again')
                return redirect('index')

        messages.error(request, 'Please fill out the required field(s)')
        return redirect('supply_param')


class ConnectDeviceView(View):
    def get(self, request, *args, **kwargs):
        try:
            cookie = request.COOKIES['_longevity_anon_user']
            if self.request.user.is_authenticated:
                account = Account.objects.get(user=request.user)
            else:
                account = Account.objects.get(cookie=cookie)

            device = Device.objects.filter(account=account)
            context = {
                'devices': device,
            }

            return render(self.request, 'dash/connect_device.html', context)
        except KeyError:
            # This will happen when cookie is missing or has expired
            messages.warning(request, 'Invalid or expired cookies, try again')
            return redirect('index')


def connect_device(request, id):
    if request.method == 'GET':
        device = get_object_or_404(Device, id=id)
        device.awarded = True
        device.date_awarded = timezone.now()
        device.battery_life = randint(1, 100)
        device.connection_status = 'success'
        device.save()
        messages.success(request, f'You have received 5 LONG token for connecting {device.device_name}')
        return redirect(request.META.get('HTTP_REFERER', 'connect_device'))
    return HttpResponseBadRequest('Request Not Implemented')


def disconnect_device(request, id):
    if request.method == 'GET':
        device = get_object_or_404(Device, id=id)
        device.awarded = False
        device.date_awarded = None
        device.battery_life = None
        device.connection_status = 'danger'
        device.save()
        messages.warning(request, f'You have disconnecte {device.device_name}')
        return redirect(request.META.get('HTTP_REFERER', 'connect_device'))
    return HttpResponseBadRequest('Request Not Implemented')


class ConnectAppView(View):
    def get(self, request, *args, **kwargs):
        try:
            cookie = request.COOKIES['_longevity_anon_user']
            if self.request.user.is_authenticated:
                account = Account.objects.get(user=request.user)
            else:
                account = Account.objects.get(cookie=cookie)

            app = App.objects.filter(account=account)
            context = {
                'apps': app,

            }

            return render(self.request, 'dash/connect_app.html', context)
        except KeyError:
            # This will happen when cookie is missing or has expired
            messages.warning(request, 'Invalid or expired cookies, try again')
            return redirect('index')


def connect_app(request, id):
    if request.method == 'GET':
        app = get_object_or_404(App, id=id)
        app.awarded = True
        app.date_awarded = timezone.now()
        app.connection_status = 'success'
        app.save()
        messages.success(request, f'You have received 5 LONG token for connecting {app.app_name}')
        return redirect(request.META.get('HTTP_REFERER', 'connect_device'))
    return HttpResponseBadRequest('Request Not Implemented')


def disconnect_app(request, id):
    if request.method == 'GET':
        app = get_object_or_404(App, id=id)
        app.awarded = False
        app.date_awarded = None
        app.connection_status = 'danger'
        app.save()
        messages.warning(request, f'You have disconnected {app.app_name.title()}')
        return redirect(request.META.get('HTTP_REFERER', 'connect_device'))
    return HttpResponseBadRequest('Request Not Implemented')


def verify_app_token(request):
    if request.method == 'GET':
        try:
            current_app = request.session['current_app']
            app = App.objects.filter(user=request.user, app_name=current_app)
            if app.exists():
                app = app.first()
                if 'error' in request.GET:
                    messages.warning(request, 'Connection cancelled by user')
                    return redirect('connect_app')
                else:
                    # This only uses google as testcase amd it can be modified to be in line with other health apps
                    app.api_key = request.GET.get('code')
                    app.awarded = True
                    app.date_awarded = timezone.now()
                    app.connection_status = 'success'
                    app.save()
                    del request.session['current_app']
                    messages.success(request, f'You have received 5 LONG token for connecting {app.app_name.title()}')
                    return redirect('connect_app')
            # messages.warning(request, 'Your browser is too old to browse this site')
        except KeyError:
            messages.error(request, 'Something went wrong please reload the page and try again')
            return redirect('connect_app')

    return HttpResponseBadRequest('Request Not Implemented')
