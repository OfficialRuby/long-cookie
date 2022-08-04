from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from reward.models import Device, App, Reward, Parameter, Account


# This is not actually the best practice,
# Produc image URLs can can be made an independent model
# The below image url is hardcoded and meant for testing purpose only
device_image_urls = {
    'xiaomi': '/device/xiaomi.jpg',
    'scan_watch': '/device/scan-watch.jpg',
    'longevity': '/device/longevity.jpg',
    'steel_hr': '/device/steel-HR.png',
}


app_icon_urls = {
    'google_fit': '/app/google-fit.png',
    'samsung_health': '/app/samsung-health.png',
    'apple_health': '/app/apple-health.jpg',
    'xiaomi': '/app/xiaomi.webp',
    'garmin_connect': '/app/garmin-connect.png',
}


@receiver(post_save, sender=Account)
def signup_actions(sender, instance, created, ** kwargs):
    if created:
        # Create devices when user signs up
        Device.objects.create(account=instance, device_name="Xiaomi Mi Band", thumbnail=device_image_urls.get('xiaomi'))
        Device.objects.create(account=instance, device_name="Scan Watch", thumbnail=device_image_urls.get('scan_watch'))
        Device.objects.create(account=instance, device_name="Longevity BioContainer",
                              thumbnail=device_image_urls.get('longevity'))
        Device.objects.create(account=instance, device_name="Steel HR", thumbnail=device_image_urls.get('steel_hr'))
        # Create app when user signs up
        App.objects.create(account=instance, app_name='google', thumbnail=app_icon_urls.get('google_fit'))
        App.objects.create(account=instance, app_name='apple', thumbnail=app_icon_urls.get('apple_health'))
        App.objects.create(account=instance, app_name='garmin', thumbnail=app_icon_urls.get('garmin_connect'))
        App.objects.create(account=instance, app_name='samsung', thumbnail=app_icon_urls.get('samsung_health'))
        App.objects.create(account=instance, app_name='xiaomi', thumbnail=app_icon_urls.get('xiaomi'))
        # Reward user with initial 50 LONG token when they sign up
        Reward.objects.create(account=instance, title="Welcom reward",  reward_point=50)


@receiver(post_save, sender=Parameter)
def device_rewards(sender, instance, created, ** kwargs):
    if instance.awarded == True and instance.date_awarded != None:
        Reward.objects.create(account=instance.account, reward_point=instance.reward_point,
                              title=f'Reward for providing parameters')


@receiver(post_save, sender=Device)
def device_rewards(sender, instance, created, ** kwargs):
    if instance.awarded == True and instance.date_awarded != None:
        Reward.objects.create(account=instance.account, reward_point=instance.reward_point,
                              title=f'Reward for connecting {instance.device_name} ')


@receiver(post_save, sender=App)
def device_rewards(sender, instance, created, ** kwargs):
    if instance.awarded == True and instance.date_awarded != None:
        Reward.objects.create(account=instance.account, reward_point=instance.reward_point,
                              title=f'Reward for connecting {instance.app_name} ')
