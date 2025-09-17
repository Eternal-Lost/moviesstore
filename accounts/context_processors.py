from django.db.models import Sum
from cart.models import Order

def subscription_tier(request):
    if request.user.is_authenticated:
        total_spent = Order.objects.filter(user=request.user).aggregate(total=Sum('total'))['total'] or 0

        if total_spent >= 30:
            tier = "Premium"
        elif total_spent >= 15:
            tier = "Medium"
        else:
            tier = "Basic"
    else:
        tier = None

    return {'subscription_tier': tier}
