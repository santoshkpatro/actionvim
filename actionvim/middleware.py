from django.conf import settings
from django.shortcuts import HttpResponse
from mimetypes import guess_type

class ViteStaticMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if "/assets/" in request.path:
            # remaining_path = request.path.split("/frontend/", 1)[1]
            content_type, _ = guess_type(request.path)
            file_path = settings.BASE_DIR / "dist" / request.path[1:]
            
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type=content_type)
                return response

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response