# Generated by Django 2.0.5 on 2019-09-02 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdatas', '0002_auto_20190901_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clickandback',
            name='case_counts',
            field=models.IntegerField(default='1', help_text='用例循环次数，请填写数字，例如：1、2、3', verbose_name='用例循环次数'),
        ),
        migrations.AlterField(
            model_name='clickandback',
            name='current_page_click_ele_find',
            field=models.CharField(blank=True, default='', help_text='元素查找风格：id、name、class_name、tag_name、link_text、partial_link_text、xpath', max_length=100, null=True, verbose_name='当前页面要点击元素查找风格'),
        ),
        migrations.AlterField(
            model_name='clickandback',
            name='current_page_click_ele_find_value',
            field=models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='当前页面要点击元素查找风格的确切值'),
        ),
        migrations.AlterField(
            model_name='clickandback',
            name='test_module',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='测试模块'),
        ),
    ]
