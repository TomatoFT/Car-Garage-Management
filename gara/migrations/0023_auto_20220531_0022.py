# Generated by Django 3.0.5 on 2022-05-30 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gara', '0022_auto_20220530_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phieusuachua',
            name='tinhtrangthutien',
        ),
        migrations.AlterField(
            model_name='baocaodoanhso',
            name='month',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='baocaodoanhso',
            name='tongdoanhso',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='baocaodoanhso',
            name='year',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='baocaoton',
            name='mavattuphutung',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gara.VatTuPhuTung'),
        ),
        migrations.AlterField(
            model_name='baocaoton',
            name='phatsinh',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='baocaoton',
            name='toncuoi',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='baocaoton',
            name='tondau',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='ct_baocaodoanhso',
            name='STT',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ct_baocaodoanhso',
            name='luotsua',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ct_baocaodoanhso',
            name='thanhtien',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ct_phieunhapvtpt',
            name='dongia',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='ct_phieunhapvtpt',
            name='mavattuphutung',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gara.VatTuPhuTung'),
        ),
        migrations.AlterField(
            model_name='ct_phieunhapvtpt',
            name='soluong',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='ct_phieusuachua',
            name='solan',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='ct_phieusuachua',
            name='tiencong',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='ct_phieusuachua',
            name='tongtien',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ct_phieusuachua',
            name='tongtienvattu',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ct_vattuphutung',
            name='dongia',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='ct_vattuphutung',
            name='mavattuphutung',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gara.VatTuPhuTung'),
        ),
        migrations.AlterField(
            model_name='ct_vattuphutung',
            name='soluong',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='ct_vattuphutung',
            name='tongthanhtien',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='khachhang',
            name='dienthoai',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='phieunhapvtpt',
            name='tongtien',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='phieusuachua',
            name='tongthanhtien',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='phieuthutien',
            name='sotienthu',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='quydinhhienhanh',
            name='GiaTri',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tiencong',
            name='tiencong',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vattuphutung',
            name='dongia',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='vattuphutung',
            name='soluong',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='xe',
            name='tienno',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
