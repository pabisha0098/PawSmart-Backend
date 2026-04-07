from django.db import migrations


def seed_services(apps, schema_editor):
    GroomingService = apps.get_model("grooming", "GroomingService")
    if GroomingService.objects.exists():
        return
    GroomingService.objects.bulk_create(
        [
            GroomingService(
                name="Bath & Brush",
                description="Wash, dry, and brush-out.",
                duration_minutes=60,
                price="35.00",
                is_active=True,
            ),
            GroomingService(
                name="Full Groom",
                description="Bath, haircut, nails, and ears.",
                duration_minutes=90,
                price="65.00",
                is_active=True,
            ),
            GroomingService(
                name="Nail Trim",
                description="Quick nail trim and file.",
                duration_minutes=20,
                price="15.00",
                is_active=True,
            ),
        ]
    )


def unseed_services(apps, schema_editor):
    GroomingService = apps.get_model("grooming", "GroomingService")
    GroomingService.objects.filter(
        name__in=["Bath & Brush", "Full Groom", "Nail Trim"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("grooming", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(seed_services, unseed_services),
    ]
