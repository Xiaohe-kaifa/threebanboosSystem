# Generated by Django 5.0.7 on 2024-09-18 15:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_submit_time', models.DateField(auto_now_add=True, verbose_name='申请日期')),
                ('business_id', models.CharField(max_length=50, verbose_name='申请账号')),
                ('business_name_photo', models.CharField(max_length=200, verbose_name='人像照片')),
                ('business_shop_photo', models.CharField(max_length=200, verbose_name='店铺照片')),
                ('business_name', models.CharField(max_length=50, verbose_name='店铺名称')),
                ('business_type', models.CharField(max_length=11, verbose_name='商家类型')),
                ('business_true_name', models.CharField(max_length=11, verbose_name='商家姓名')),
                ('business_identification_number', models.CharField(max_length=20, unique=True, verbose_name='商家身份证号码')),
                ('business_phone', models.CharField(max_length=11, verbose_name='商家联系方式')),
                ('business_email', models.CharField(max_length=40, verbose_name='商家邮箱')),
                ('business_address', models.CharField(max_length=10, verbose_name='商家地址')),
                ('business_full_address', models.CharField(max_length=100, null=True, verbose_name='商家详细地址')),
                ('business_license_photo', models.CharField(max_length=200, verbose_name='营业执照照片')),
                ('business_license', models.CharField(max_length=40, verbose_name='营业执照号')),
                ('tax_registration_certificate', models.CharField(max_length=40, verbose_name='税务登记证号')),
                ('business_organization', models.CharField(max_length=40, verbose_name='组织机构代码证号')),
                ('business_unified_social_credit', models.CharField(max_length=40, verbose_name='统一社会信用代码')),
                ('business_legal_representative', models.CharField(max_length=10, verbose_name='法人代表')),
                ('business_date', models.CharField(max_length=40, verbose_name='成立日期')),
                ('business_term', models.CharField(max_length=10, verbose_name='营业期限')),
                ('business_agree', models.SmallIntegerField(choices=[(1, '未读'), (0, '已同意')], default=1, verbose_name='状态')),
            ],
        ),
        migrations.CreateModel(
            name='LoginInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateField(auto_now_add=True, verbose_name='创建日期')),
                ('account', models.CharField(max_length=11, unique=True, verbose_name='账号')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='手机号')),
                ('username', models.CharField(blank=True, max_length=11, null=True, verbose_name='用户名')),
                ('password', models.CharField(blank=True, max_length=20, null=True, verbose_name='密码')),
                ('status', models.SmallIntegerField(choices=[(1, '在线'), (0, '离线')], default=0, verbose_name='状态')),
                ('address', models.CharField(blank=True, max_length=20, null=True, verbose_name='收货地址')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (0, '女')], default=1, verbose_name='性别')),
                ('file_name', models.ImageField(upload_to='imgs_photo/', verbose_name='头像')),
                ('detailed_address', models.CharField(blank=True, max_length=100, null=True, verbose_name='详细收货地址')),
            ],
        ),
        migrations.CreateModel(
            name='LunBoTuInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='图片名称')),
                ('image', models.ImageField(upload_to='imgs_lun_bos/', verbose_name='轮播图')),
            ],
        ),
        migrations.CreateModel(
            name='suggestionInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_time', models.DateField(auto_now_add=True, verbose_name='反馈日期')),
                ('feedback_status', models.SmallIntegerField(choices=[(1, '已读'), (0, '未读')], default=0, verbose_name='反馈状态')),
                ('feedback', models.SmallIntegerField(choices=[(0, '产品方向'), (1, '技术方向')], verbose_name='反馈状态')),
                ('contact', models.CharField(max_length=100, verbose_name='联系方式')),
                ('content', models.CharField(blank=True, max_length=1000, null=True, verbose_name='反馈内容')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessageInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatTime', models.DateField(auto_now_add=True, verbose_name='推送时间')),
                ('chatId', models.CharField(blank=True, max_length=11, null=True, verbose_name='推送账号')),
                ('chatTitle', models.CharField(blank=True, max_length=50, null=True, verbose_name='推送主题')),
                ('chatContent', models.CharField(blank=True, max_length=443, null=True, verbose_name='推送内容')),
                ('chatType', models.SmallIntegerField(choices=[(0, '全部'), (1, '个人')], default=0, verbose_name='推送类型')),
                ('loginId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='用户id', to='app01.logininformation')),
            ],
        ),
    ]
