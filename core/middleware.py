from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

class CheckLoginCookiesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            username = request.COOKIES.get('username')
            password = request.COOKIES.get('password')

            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('task_list')  # Certifique-se de que 'task_list' é o nome correto da URL

        response = self.get_response(request)
        return response
