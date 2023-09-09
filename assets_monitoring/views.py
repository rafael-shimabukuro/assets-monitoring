from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import AssetRegistrationForm, CustomUserCreationForm
from .models import Asset, AssetOwnership
from django.db import models


@login_required
def ownership_register(request):
    if request.method == 'POST':
        form = AssetRegistrationForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            update_interval_minutes = form.cleaned_data['update_interval_minutes']
            now = timezone.now()

            asset, created = Asset.objects.get_or_create(ticker=ticker, defaults={
                'current_price': None,
                'update_interval_minutes': update_interval_minutes,
                'last_update': None,
                'next_update': now
            })
            if not created:
                asset.update_interval_minutes = min(update_interval_minutes, asset.update_interval_minutes)
                asset.save()

            asset_owner = form.save(commit=False)
            asset_owner.user = request.user
            asset_owner.asset = asset
            asset_owner.save()

            return redirect('ownership_list')
    else:
        form = AssetRegistrationForm()
    return render(request, 'asset_register.html', {'form': form})


@login_required
def ownership_list(request):
    assets_ownerships = AssetOwnership.objects.filter(user=request.user)
    return render(request, 'asset_list.html', {'assets_ownerships': assets_ownerships})


@login_required
def ownership_delete(request, ticker):
    try:
        asset = Asset.objects.get(ticker=ticker)
        ownership = AssetOwnership.objects.get(asset=asset, user=request.user)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Not found")

    if ownership.user != request.user:
        return HttpResponse(status=401)

    asset = ownership.asset
    ownership.delete()

    # If the asset has no ownerships left, delete the asset
    if not AssetOwnership.objects.filter(asset=asset).exists():
        asset.delete()
        return redirect('ownership_list')

    # Calculate the minimum update_interval_minutes among remaining ownerships
    min_update_interval = AssetOwnership.objects.filter(asset=asset).aggregate(models.Min('update_interval_minutes'))
    asset.update_interval_minutes = min_update_interval['update_interval_minutes__min']
    asset.save()

    return redirect('ownership_list')


def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            return redirect('/')  # Redirect to your desired URL after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
