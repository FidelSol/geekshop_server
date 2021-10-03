from datetime import datetime
from baskets.models import Basket


def menu(request):
    current_year = datetime.now().strftime("%Y")

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    return {"current_year": current_year, "basket": basket}
