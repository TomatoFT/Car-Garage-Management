# Generated by Django 3.0.5 on 2022-05-30 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gara', '0023_auto_20220531_0022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='baocaoton',
            old_name='mabaocaoton',
            new_name='MaBCT',
        ),
        migrations.RemoveField(
            model_name='baocaoton',
            name='mavattuphutung',
        ),
        migrations.RemoveField(
            model_name='baocaoton',
            name='phatsinh',
        ),
        migrations.RemoveField(
            model_name='baocaoton',
            name='toncuoi',
        ),
        migrations.RemoveField(
            model_name='baocaoton',
            name='tondau',
        ),
        migrations.AddField(
            model_name='baocaoton',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ct_phieunhapvtpt',
            name='mavattuphutung',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gara.VatTuPhuTung'),
        ),
        migrations.AlterField(
            model_name='ct_vattuphutung',
            name='mavattuphutung',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gara.VatTuPhuTung'),
        ),
        migrations.CreateModel(
            name='ct_baocaoton',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TonDau', models.PositiveIntegerField()),
                ('PhatSinh', models.PositiveIntegerField()),
                ('TonCuoi', models.PositiveIntegerField()),
                ('MaBCT', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gara.BaoCaoTon')),
                ('MaVTPT', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gara.VatTuPhuTung')),
            ],
        ),
    ]
