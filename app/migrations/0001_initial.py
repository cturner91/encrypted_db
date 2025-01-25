# Generated by Django 5.1.4 on 2025-01-25 21:15

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EncryptedMixin',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MessageEncrypted',
            fields=[
                ('encryptedmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.encryptedmixin')),
                ('created_at', models.TextField()),
                ('sequence_number', models.TextField()),
                ('user_from', models.TextField()),
                ('user_to', models.TextField()),
                ('content', models.TextField()),
            ],
            bases=('app.encryptedmixin',),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('encrypted', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.messageencrypted')),
            ],
        ),
    ]
