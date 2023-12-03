from django.views import View
from django.shortcuts import HttpResponse
from django.conf import settings
from django.shortcuts import redirect, render


class IndexView(View):
    def get(self, request, *args, **kwargs):
        if settings.DEBUG is True:
            return redirect("http://localhost:5173" + request.path)

        file_path = settings.BASE_DIR / "dist" / "index.html"
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type="text/html")
            return response