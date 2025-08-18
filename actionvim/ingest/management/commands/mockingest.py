import httpx
import time
import random
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.utils import timezone
from django.conf import settings
from urllib.parse import urlparse, urlencode

from actionvim.applications.models import Application


def sample_pageview_properties():
    base_origin = "https://example.com"
    paths = [
        ("/", "Home Page"),
        ("/about", "About Us"),
        ("/contact", "Contact Us"),
        ("/products", "Products"),
        ("/services", "Services"),
        ("/blog", "Blog"),
        ("/faq", "FAQ"),
        ("/terms", "Terms of Service"),
        ("/privacy", "Privacy Policy"),
        ("/login", "Login Page"),
        ("/signup", "Sign Up Page"),
        ("/dashboard", "User Dashboard"),
        ("/profile", "User Profile"),
        ("/settings", "Settings Page"),
        ("/help", "Help Center"),
        ("/support", "Support Page"),
        ("/search", "Search Results"),
    ]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 7.0; Nexus 5X Build/NBD90Z) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    ]
    referrers = [
        "https://google.com",
        "https://facebook.com",
        "https://twitter.com",
        "https://linkedin.com",
    ]
    path, title = random.choice(paths)
    query = {}
    if random.random() < 0.5:
        query.update(
            {
                "utm_source": random.choice(["google", "facebook", "twitter"]),
                "utm_medium": random.choice(["cpc", "social", "email"]),
                "utm_campaign": random.choice(
                    ["spring_sale", "summer_promo", "fall_discount"]
                ),
            }
        )
    url = f"{base_origin}{path}"
    if query:
        url += f"?{urlencode(query)}"
    ref = random.choice(referrers)
    ref_domain = urlparse(ref).netloc if ref else ""
    # fake perf metrics (sane ranges)
    lcp_ms = int(random.uniform(450, 2500))  # Largest Contentful Paint
    cls = round(random.uniform(0.0, 0.15), 3)  # Cumulative Layout Shift
    fid_ms = int(random.uniform(50, 300))  # First Input Delay
    return {
        "url": url,
        "title": title,
        "referrer": ref,
        "referrer_domain": ref_domain,
        "user_agent": random.choice(user_agents),
        "lcp_ms": lcp_ms,
        "cls": cls,
        "fid_ms": fid_ms,
    }


def random_past_time():
    # Define maximum range: let's say up to 3 years
    max_days = 365 * 3
    # Pick a random number of seconds within that range
    random_seconds = random.randint(0, max_days * 24 * 60 * 60)
    return timezone.now() - timezone.timedelta(seconds=random_seconds)


class Command(BaseCommand):
    help = "Mockingest command to simulate data ingestion via capture_id (API Key)"

    def add_arguments(self, parser):
        parser.add_argument(
            "capture_id",
            type=str,
            help="The capture_id (API Key) to use for mocking ingestion.",
        )

    def handle(self, *args, **options):
        capture_id = options.get("capture_id")
        application = Application.objects.filter(capture_id=capture_id).first()
        if not application:
            raise CommandError(f"No application found with capture_id: {capture_id}")

        BASE_URL = settings.BASE_URL
        injestion_url = f"{BASE_URL}/ingest/{capture_id}"
        while True:
            payload = {
                "name": "pagevisit",
                "properties": sample_pageview_properties(),
                "captured_at": random_past_time().isoformat(),
            }
            response = httpx.post(
                injestion_url,
                json=payload,
            )
            if response.status_code == 200:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully ingested event: {timezone.now()}")
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed to ingest event: {timezone.now()}. Status code: {response.status_code}"
                    )
                )
            # time.sleep(1)
