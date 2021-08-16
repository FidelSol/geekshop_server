from datetime import datetime


def menu(request):
    current_year = datetime.now().strftime("%Y")
    return {"current_year": current_year}
