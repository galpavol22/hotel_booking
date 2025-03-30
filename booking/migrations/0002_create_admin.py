from django.db import migrations

def create_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    username = "admin"
    password = "Admin123"  # Zvoľ bezpečné heslo!
    email = "admin@example.com"
    
    if not User.objects.filter(username=username).exists():
        print("Creating admin user...")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print("Admin user already exists.")

class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0001_initial'), # tu musíš mať tvoju aktuálnu migráciu
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
