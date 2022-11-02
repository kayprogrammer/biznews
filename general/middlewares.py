from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user
        tzname = request.COOKIES.get('localtimezone')
        if user.is_authenticated:
            tzname = user.timezone.name

        if tzname:
            timezone.activate(tzname)
        else:
            timezone.deactivate()
        
        response = self.get_response(request)
        return response
        