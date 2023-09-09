from datetime import timedelta

from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone

from assets import settings
from assets.settings import ALPHAVANTAGE_KEY
from .models import Asset, AssetOwnership
import requests


def update_asset_prices():
    now = timezone.now()
    assets = Asset.objects.filter(Q(next_update__isnull=True) | Q(next_update__lte=now))
    for asset in assets:
        print(asset.ticker, "trying to update price")
        response = requests.get(
            f'https://www.alphavantage.co/query',
            params={
                'function': 'GLOBAL_QUOTE',
                'symbol': asset.ticker + '.SA',
                'apikey': ALPHAVANTAGE_KEY
            }
        )
        if response.status_code == 200:
            data = response.json().get('Global Quote')
            now = timezone.now()
            if data:
                latest_price = data.get('05. price')
                asset.current_price = float(latest_price)
                asset.last_update = now
                asset.next_update = now + timezone.timedelta(minutes=asset.update_interval_minutes)
                asset.save()
                print(asset.ticker, "price updated")

                notify_ownerships(asset)


def notify_ownerships(asset):
    ownerships = asset.assetownership_set.all()
    for ownership in ownerships:
        # Check if already notified in the last 24h
        now = timezone.now()
        if ownership.notified_time and (now - ownership.notified_time) < timedelta(hours=24):
            continue

        if asset.current_price > ownership.max_price or asset.current_price < ownership.min_price:

            subject = f'Sell {asset.ticker} Exceeded Maximum Price' if asset.current_price > ownership.max_price \
                else f'Buy {asset.ticker} Fell Below Minimum Price'

            message = f'{asset.ticker} has exceeded the maximum price of {ownership.max_price}. ' \
                      f'Current price is {asset.current_price}.' if asset.current_price > ownership.max_price \
                else f'{asset.ticker} has fallen below the minimum price of {ownership.min_price}.' \
                      f'Current price is {asset.current_price}.'

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [ownership.user.email]
            send_mail(subject, message, from_email, recipient_list)
            print(ownership.user.email, "notified about", asset.ticker)
            ownership.notified_time = timezone.now()
            ownership.save()

