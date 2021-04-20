# Generated by Django 2.2.10 on 2021-04-06 10:09

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0169_indicator_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='termsandcondition',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='faq',
            name='question',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='termsandcondition',
            name='sub_title',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='termsandcondition',
            name='title',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]