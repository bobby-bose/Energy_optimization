from django.shortcuts import redirect

class PreventLoginOrRegisterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ['/login/', '/register/'] and request.user.is_authenticated and request.session.get('logged_in'):
            return redirect('index')
        response = self.get_response(request)
        return response
