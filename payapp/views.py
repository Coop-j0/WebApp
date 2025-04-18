from django.shortcuts import render, redirect
from django.contrib import messages
from payapp.forms import PaymentForm, PaymentRequestForm, AdminRegistrationForm
from payapp.models import Transaction, UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q
from register.models import CustomUser
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from decimal import Decimal

EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.92,
    'GBP': 0.79,
}

@require_GET
def currency_conversion_api(request, from_currency, to_currency, amount):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    try:
        amount = float(amount)

        if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
            return JsonResponse(
                {'error': 'Unsupported currency code.'},
                status=400
            )

        gbp_amount = amount / EXCHANGE_RATES[from_currency]
        converted_amount = gbp_amount * EXCHANGE_RATES[to_currency]
        conversion_rate = EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency]

        return JsonResponse({
            'from': from_currency,
            'to': to_currency,
            'original_amount': amount,
            'conversion_rate': round(conversion_rate, 6),
            'converted_amount': round(converted_amount, 2),
        })

    except ValueError:
        return JsonResponse({'error': 'Invalid amount provided.'}, status=400)



def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
@user_passes_test(is_admin)
def admin_view_users(request):
    users = CustomUser.objects.all().select_related('userprofile')
    return render(request, 'admin_view_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def admin_view_transactions(request):
    transactions = Transaction.objects.all().order_by('-timestamp')
    return render(request, 'admin_view_transactions.html', {'transactions': transactions})

@login_required
@user_passes_test(is_admin)
def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            admin_user = form.save(commit=False)
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            return redirect('admin_dashboard')
    else:
        form = AdminRegistrationForm()
    return render(request, 'register_admin.html', {'form': form})

def dashboard_view(request):
    limit = 5

    print("=== DASHBOARD VIEW HAS BEEN CALLED ===")

    user_profile = UserProfile.objects.get(user=request.user)

    transactions = Transaction.objects.filter(
        Q(sender=user_profile) | Q(recipient=user_profile)
    ).order_by('-timestamp')[:5]


    context = {
        'user_profile': user_profile,
        'transactions': transactions,
        'limit':limit,
    }

    return render(request, 'register/dashboard.html', context)

@login_required
def make_payment(request):

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']


            recipient_profile = UserProfile.objects.get(user=recipient)
            sender_profile = UserProfile.objects.get(user=request.user)

            if sender_profile.balance < amount:
                messages.error(request, "Insufficient balance!")
                return redirect('make_payment')

            sender_profile.balance -= amount
            recipient_profile.balance += amount
            sender_profile.save()
            recipient_profile.save()

            Transaction.objects.create(
                sender=sender_profile,
                recipient=recipient_profile,
                amount=amount,
                type='payment',
            )



            messages.success(request, "Payment successful!")
            return redirect('dashboard')
    else:
        form = PaymentForm()

    return render(request, 'payapp/make_payment.html', {'form': form})

@login_required
def send_request(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            recipient_profile = UserProfile.objects.get(user=recipient)
            Transaction.objects.create(sender=user_profile, recipient=recipient_profile, amount=amount, type='request', is_request_accepted=False)

            messages.success(request, "Payment request sent successfully!")
            return redirect('dashboard')
    else:
        form = PaymentRequestForm()

    return render(request, 'payapp/send_request.html', {'form': form})
@login_required
def pending_requests(request):

    user_profile = UserProfile.objects.get(user=request.user)

    pending_requests = Transaction.objects.filter(recipient=user_profile,type = 'request', is_request_accepted=False)

    return render(request, 'payapp/pending_requests.html', {'pending_requests': pending_requests})

@login_required
@transaction.atomic
def accept_request(request, request_id):
    recipient_profile = request.user.userprofile

    payment_request = get_object_or_404(
        Transaction,
        id=request_id,
        recipient=recipient_profile,
        is_request_accepted=False,
        type='request'
    )

    sender_profile = payment_request.sender

    if recipient_profile.balance >= payment_request.amount:
        payment_request.is_request_accepted = True
        payment_request.save()

        recipient_profile.balance -=  Decimal(str(payment_request.amount))
        sender_profile.balance += Decimal(str(payment_request.amount))

        recipient_profile.save()
        sender_profile.save()

        messages.success(request, 'Payment request accepted successfully.')
    else:
        messages.error(request, 'Insufficient balance to accept this request.')

    return HttpResponseRedirect('/payments/pending_requests/')


@login_required
@transaction.atomic
def decline_request(request, request_id):
    recipient_profile = request.user.userprofile

    payment_request = get_object_or_404(
        Transaction,
        id=request_id,
        recipient=recipient_profile,
        is_request_accepted=False)

    payment_request.is_request_accepted = True
    payment_request.save()

    messages.success(request, 'Payment request declined.')

    return HttpResponseRedirect('/payments/pending_requests/')

def transaction_history(request):

    user_profile = UserProfile.objects.get(user=request.user)

    transactions = Transaction.objects.filter(
        Q(sender=user_profile) | Q(recipient=user_profile)
    ).order_by('-timestamp')

    context = {
        'user_profile': user_profile,
        'transactions': transactions,
    }

    return render(request, 'payapp/transaction_history.html', context)