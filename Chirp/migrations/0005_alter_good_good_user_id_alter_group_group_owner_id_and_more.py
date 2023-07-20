# Generated by Django 4.2 on 2023-07-20 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Chirp', '0004_alter_good_good_user_id_alter_group_group_owner_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='good_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='group',
            name='group_owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='contributor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_contributor', to=settings.AUTH_USER_MODEL),
        ),
    ]
