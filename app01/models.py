from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator,MaxValueValidator


class BusinessInformation(models.Model):
# 基本信息
    business_submit_time = models.DateField(auto_now_add=True, verbose_name='申请日期')
    business_id= models.CharField(verbose_name='申请账号',max_length=50,null=False)
    business_name_photo = models.CharField(verbose_name='人像照片',max_length=200,null=False)
    business_shop_photo= models.CharField(verbose_name='店铺照片',max_length=200,null=False)
    business_name= models.CharField(verbose_name='店铺名称',max_length=50,null=False)
    business_type= models.CharField(verbose_name='商家类型',max_length=11,null=False)
    business_true_name= models.CharField(verbose_name='商家姓名',max_length=11,null=False)
    business_identification_number= models.CharField(verbose_name='商家身份证号码',unique=True,max_length=20,null=False)
    business_phone=models.CharField(verbose_name='商家联系方式',max_length=11,null=False)
    business_email = models.CharField(verbose_name='商家邮箱',max_length=40,null=False)
    business_address= models.CharField(verbose_name='商家地址',max_length=10,null=False)
    business_full_address= models.CharField(verbose_name='商家详细地址',max_length=100,null=True)
# 商户信息
    business_license_photo = models.CharField(verbose_name='营业执照照片',max_length=200,null=False)
    business_license = models.CharField(verbose_name='营业执照号',max_length=40,null=False)
    tax_registration_certificate = models.CharField(verbose_name='税务登记证号',max_length=40,null=False)
    business_organization = models.CharField(verbose_name='组织机构代码证号',max_length=40,null=False)
    business_unified_social_credit = models.CharField(verbose_name='统一社会信用代码',max_length=40,null=False)
    business_legal_representative = models.CharField(verbose_name='法人代表',max_length=10,null=False)
    business_date = models.CharField(verbose_name='成立日期',max_length=40,null=False)
    business_term = models.CharField(verbose_name='营业期限',max_length=10,null=False)
# 状态
    business_agree_choices = (
        (1,'未读'),
        (0,'已同意'),
    )
    business_agree = models.SmallIntegerField(verbose_name='状态',choices=business_agree_choices,default=1)
# class Login(models.Model):
#     phone = models.CharField(verbose_name='手机号',max_length=11)
#     price = models.IntegerField(verbose_name='价格',default=0)
#     level_choices = (
#         (1,'一级'),
#         (2,'二级'),
#         (3,'三级'),
#         (4,'四级'),
#     )
#     level = models.SmallIntegerField(verbose_name='级别',choices=level_choices,default=1)
#     status_choices = (
#         (1,'已占用'),
#         (2,'未占用'),
#     )
#     status = models.SmallIntegerField(verbose_name='状态',choices=status_choices,default=2)
class LoginInformation(models.Model):
    login_time = models.DateField(auto_now_add=True, verbose_name='创建日期')
    account = models.CharField(verbose_name='账号',max_length=11,unique=True,null=False)
    phone = models.CharField(verbose_name='手机号',max_length=11,unique=True,null=False)
    username = models.CharField(verbose_name='姓名',max_length=11,null=True,blank=True)
    password = models.CharField(max_length=20,verbose_name='密码',null=True,blank=True)
    username_type_choices = (
        (0,'管理员'),
        (1,'用户'),
        (2,'商家'),
        (3,'客服'),
    )
    username_type = models.SmallIntegerField(verbose_name='状态',choices=username_type_choices,default=1)
    status_choices = (
        (1,'在线'),
        (0,'离线'),
    )
    status = models.SmallIntegerField(verbose_name='状态',choices=status_choices,default=0)
    gender_choices = (
        (1,'男'),
        (0,'女'),
    )
    address = models.CharField(verbose_name='收货地址',max_length=20,blank=True,null=True)
    gender = models.SmallIntegerField(verbose_name='性别',choices=gender_choices,default=1)
    file_name = models.ImageField(upload_to='imgs_photo/',verbose_name='头像')
    detailed_address = models.CharField(verbose_name='详细收货地址',max_length=100,blank=True,null=True)
    

class LunBoTuInformation(models.Model):
    name = models.CharField(verbose_name='图片名称',max_length=100)
    image = models.ImageField(upload_to='imgs_lun_bos/',verbose_name='轮播图')
class suggestionInformation(models.Model):
    feedback_time = models.DateField(auto_now_add=True, verbose_name='反馈日期')
    feedback_status_choices = (
        (1,'已读'),
        (0,'未读'),
    )
    feedback_status = models.SmallIntegerField(verbose_name='反馈状态',choices=feedback_status_choices,default=0)
    feedback_choices = (
        (0,'产品方向'),
        (1,'技术方向'),
    )
    feedback = models.SmallIntegerField(verbose_name='反馈状态',choices=feedback_choices,null=False)
    contact = models.CharField(verbose_name='联系方式',max_length=100,null=False)
    content = models.CharField(verbose_name='反馈内容',max_length=1000,blank=True,null=True)

class ChatMessageInformation(models.Model):
    loginId = models.ForeignKey(LoginInformation, related_name='用户id', on_delete=models.CASCADE)
    chatTime = models.DateField(auto_now_add=True, verbose_name='推送时间')
    chatId = models.CharField( verbose_name='推送账号', max_length=11 ,null=True,blank=True)
    chatTitle = models.CharField(verbose_name='推送主题',max_length=50,null=True,blank=True)
    chatContent = models.CharField(verbose_name='推送内容',max_length=443,null=True,blank=True)
    chatType_choices = (
        (0,'全部'),
        (1,'个人'),
    )
    chatType = models.SmallIntegerField(verbose_name='推送类型',choices=chatType_choices,default=0)
    # def __str__(self):
    #     return self.chatTime.strftime('%Y-%m-%d %H:%M')
class CommodityInformation(models.Model):
    businessId = models.ForeignKey(BusinessInformation, related_name='商家id', on_delete=models.CASCADE)
    commodityTime = models.DateField(auto_now_add=True, verbose_name='发布时间')
    commodityType_choices = (
        (0,'全部'),
        (1,'个人'),
    )
    commodityType = models.SmallIntegerField(verbose_name='商品类型',choices=commodityType_choices,default=0)
    commodityName = models.CharField( verbose_name='商品名称', max_length=11 ,null=False)
    commodityPhoto= models.CharField(verbose_name='店铺照片',max_length=200,null=False)
    commodityShopName= models.CharField(verbose_name='店铺名称',max_length=50,null=False)
    commodityShopNumber= models.IntegerField(verbose_name='商品库存量',null=False,validators=[
        MinValueValidator(Decimal(0))
    ])
    commodityOther= models.CharField(verbose_name='商品备注',max_length=11,null=False)
    commodityPriceBefore= models.DecimalField(verbose_name='优惠前价格',null=False,max_digits=10,decimal_places=2,validators=[
        MinValueValidator(Decimal('0.00'))
    ])
    commodityPriceAfter= models.DecimalField(verbose_name='优惠后价格',null=False,max_digits=10,decimal_places=2,validators=[
        MinValueValidator(Decimal('0.00'))
    ])
    commodityIntroduce= models.CharField(verbose_name='商品介绍',max_length=1000,blank=True,null=True)

class OrdersInformation(models.Model):
    order_id= models.CharField(verbose_name='订单id',max_length=20,null=False)
    order_time = models.DateTimeField(auto_now_add=True, verbose_name='下单时间')
    order_commodity_name = models.CharField( verbose_name='商品名称', max_length=11 ,null=False)
    order_shop_name= models.CharField(verbose_name='店铺名称',max_length=50,null=False)
    order_commodity_photo= models.CharField(verbose_name='商品照片',max_length=200,null=False)
    order_commodity_type_choices = (
        (0,'竹编家具'),
        (1,'工艺品'),
    )
    order_commodity_type = models.SmallIntegerField(verbose_name='商品类型',choices=order_commodity_type_choices,default=0)
    order_people_account = models.CharField(verbose_name='下单账号',max_length=11,null=False)
    order_people_phone = models.CharField(verbose_name='下单手机号',max_length=11,null=False)
    order_people_name = models.CharField(verbose_name='下单人姓名',max_length=11,null=True,blank=True)
    order_people_address = models.CharField(verbose_name='收货地址',max_length=20,blank=True,null=True)
    order_people_detailed_address = models.CharField(verbose_name='详细收货地址',max_length=65,blank=True,null=True)
    order_number= models.IntegerField(verbose_name='下单数量',null=False,validators=[
        MinValueValidator(Decimal(0))
    ])
    order_price= models.DecimalField(verbose_name='下单价格',null=False,max_digits=30,decimal_places=2,validators=[
        MinValueValidator(Decimal('0.00'))
    ])

class CartItem(models.Model):
    cart_user = models.ForeignKey(LoginInformation, on_delete=models.CASCADE, related_name='cart_items')  # 关联用户
    cart_commodity = models.ForeignKey(CommodityInformation, on_delete=models.CASCADE, related_name='cart_items')  # 关联商品
    quantity = models.PositiveIntegerField(default=1)  # 商品数量


    