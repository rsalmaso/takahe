# Generated by Django 4.2.1 on 2023-07-15 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_remove_token_code_token_revoked_alter_token_token_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="token",
            name="push_subscription",
            field=models.JSONField(blank=True, null=True),
        ),
    ]