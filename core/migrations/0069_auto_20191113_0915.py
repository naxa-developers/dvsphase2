# Generated by Django 2.0.5 on 2019-11-13 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_auto_20191113_0829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fivew',
            old_name='rp_email',
            new_name='type_of_institution',
        ),
        migrations.RemoveField(
            model_name='fivew',
            name='rp_contact_name',
        ),
        migrations.RemoveField(
            model_name='fivew',
            name='rp_name',
        ),
        migrations.AddField(
            model_name='fivew',
            name='consortium_partner_first',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ConsortiumPartnerF', to='core.Partner'),
        ),
        migrations.AddField(
            model_name='fivew',
            name='consortium_partner_second',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ConsortiumPartnerS', to='core.Partner'),
        ),
        migrations.AddField(
            model_name='fivew',
            name='consortium_partner_third',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ConsortiumPartnerT', to='core.Partner'),
        ),
        migrations.AddField(
            model_name='fivew',
            name='local_partner_first',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LocalPartnerF', to='core.Partner'),
        ),
        migrations.AddField(
            model_name='fivew',
            name='local_partner_second',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LocalPartnerS', to='core.Partner'),
        ),
        migrations.AddField(
            model_name='fivew',
            name='local_partner_third',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LocalPartnerT', to='core.Partner'),
        ),
        migrations.AddField(
            model_name='fivew',
            name='rp_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PartnerContact', to='core.PartnerContact'),
        ),
    ]