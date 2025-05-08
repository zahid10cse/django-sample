import requests
from django.core.management.base import BaseCommand

from core.models import Country


class Command(BaseCommand):
    help = "Seed countries from https://restcountries.com/v3.1/all"

    def handle(self, *args, **kwargs):
        url = "https://restcountries.com/v3.1/all"
        try:
            response = requests.get(url)
            response.raise_for_status()
            countries_data = response.json()

            created, skipped = 0, 0

            for country in countries_data:
                try:
                    name = country["name"]["common"]
                    cca2 = country.get("cca2")
                    capital = country.get("capital", [None])[0]  # List of capitals
                    population = country.get("population")
                    timezone = country.get("timezones", [None])[0]  # List of timezones
                    flag = country.get("flags", {}).get("png")  # or svg if you prefer

                    obj, created_flag = Country.objects.get_or_create(
                        name=name,
                        defaults={
                            "cca2": cca2,
                            "capital": capital,
                            "population": population,
                            "timezone": timezone,
                            "flag": flag
                        }
                    )

                    if created_flag:
                        created += 1
                    else:
                        skipped += 1

                except Exception as e:
                    self.stderr.write(f"Error processing {country.get('name', {}).get('common', 'Unknown')}: {e}")

            self.stdout.write(self.style.SUCCESS(
                f"🌍 Countries seed complete. Created: {created}, Skipped: {skipped}"
            ))

        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"❌ Failed to fetch data: {e}"))
