from .models import *


def AdminCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype == '4':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)
