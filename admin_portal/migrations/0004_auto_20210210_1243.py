# Generated by Django 3.1.5 on 2021-02-10 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0003_auto_20210210_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lifechoicesacademy',
            name='student_number',
            field=models.CharField(max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='lifechoicesmember',
            name='ID_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='lifechoicesmember',
            name='allergies',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='lifechoicesmember',
            name='chronic_condition',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='lifechoicesstuff',
            name='WorkPermit_number',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='lifechoicesstuff',
            name='account_holder_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='lifechoicesstuff',
            name='account_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='lifechoicesstuff',
            name='bank_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='lifechoicesstuff',
            name='branch_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='lifechoicesstuff',
            name='branch_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='lifechoicesstuff',
            name='tax_number',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
