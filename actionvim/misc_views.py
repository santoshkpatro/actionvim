from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from django.contrib.auth import logout


def index(request):
    index_path = settings.BASE_DIR / "frontend" / "index.html"
    if settings.DEBUG:
        return render(request, "index.html")

    return FileResponse(open(index_path, "rb"), content_type="text/html")


def sign_out(request):
    """
    Handle user logout.
    """
    logout(request)
    return render(request, "logged_out.html", status=200)


def health(request):
    """
    Simple health check endpoint with green OK text.
    """
    html = """
    <html>
        <body style="background-color:#f6ffed; margin:0; padding:0; display:flex; align-items:center; justify-content:center; height:100vh;">
            <h1 style="color:#52c41a; font-family:sans-serif; font-size:2rem;">OK</h1>
        </body>
    </html>
    """
    return HttpResponse(html, content_type="text/html", status=200)
