import base64
import datetime
from decimal import Decimal
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import LoginInformation,OrdersInformation,CartItem,LunBoTuInformation,CommodityInformation,suggestionInformation,BusinessInformation,ChatMessageInformation
from app01.serializers import LoginSerializers,OrdersSerializers,CommoditySerializers,CartItemSerializers,ChatMessageSerializers, PostCartItemSerializers,SuccessSerializers,suggestionSerializers,BusinessSerializers
from rest_framework.views import APIView
import random
from datetime import datetime, timedelta
from django.utils import timezone
from dateutil import parser
from django.db.models import Count
from django.db.models import Sum


# 删除购物车
class delCartView(APIView):
    # 根据id删除购物车商品
    def post(self,request):
        for i in request.data:
            CartItem.objects.filter(id__in=request.data).delete()
        return Response('serializer.errors')

# 购物车管理
class cartView(APIView):
    # 添加到购物车
    def post(self,request):
        serializer = PostCartItemSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":0})
        else:
            print(serializer.errors)
            return Response(serializer.errors)
        

class cartDetailView(APIView):
    # 获取某个人的购物车信息
    def put(self,request,id):
        cartPeople = CartItem.objects.filter(Q(cart_commodity__commodityName__icontains=request.data.get('searchContent')) | Q(cart_commodity__commodityShopName__icontains=request.data.get('searchContent')),cart_user_id=id)
        serializer = CartItemSerializers(cartPeople,many=True)
        commodityName = set()
        for key in serializer.data:
            commodityName.add(key['cart_commodity']['commodityShopName'])
        result = []
        data=[]
        for key in commodityName:
            for i in serializer.data:
                if key == i['cart_commodity']['commodityShopName']:
                    i['cart_commodity']['commodityPhoto'] = out_picture(str('local_file/commodity/'+i['cart_commodity']['commodityPhoto']))
                    i['cart_commodity']['quantity']=i['quantity']
                    i['cart_commodity']['cartId']=i['id']
                    data.append(i['cart_commodity'])
            result.append({"commodityName":key,"data":data})
            data=[]
        return Response(result)
        

# 获取入驻商家量，用户注册量，总订单量
class homeNumberView(APIView):
    # 获取入驻商家量，用户注册量，总订单量
    def get(self,request):
        shopCount = BusinessInformation.objects.filter(business_agree=0).count()
        userCount = LoginInformation.objects.all().count()
        orderCount = OrdersInformation.objects.all().count()
        # 计算总订单金额
        totalAmount = OrdersInformation.objects.aggregate(order_price=Sum('order_price'))['order_price'] or 0
        return Response({'0':shopCount,'1':userCount,'2':orderCount,'3':totalAmount})

# 热门商品总销量
class chart02View(APIView):
    # 查询热门商品总销量比例
    def get(self,request):
        # 获取订单量最多的前五个商品名称及对应的订单数量
        popular_products = (
            OrdersInformation.objects
            .values('order_commodity_name')  # 按商品名称分组
            .annotate(order_count=Count('id'))  # 计算每个商品的订单数量
            .order_by('-order_count')[:5]  # 按订单数量降序排序并限制为前五个
        )
        # 构建响应格式
        result = [
            { 'value': item['order_count'],'name': item['order_commodity_name']}
            for item in popular_products
        ]
        return Response(result)

# 后台获取每日订单数据表
class chart01View(APIView):
    # 后台获取每日订单数据表
    def get(self,request):
        # 获取当前本地时间并转换为日期
        now = datetime.now()
        today = now.date()  # 注意，这里将使用当前时间的本地日期
        start_date = today - timedelta(days=6)
        orders01 = OrdersInformation.objects.filter(order_time__range=[start_date, today + timedelta(days=1)],order_commodity_type='0')
        # 用于每天的订单数初始化为0的列表
        order_counts01 = [0] * 7  # 7天（今天和过去6天）
        # 统计每天的订单数量，从最久到最近
        for order in orders01:
            
            order_date_index = (today  - timezone.localtime(order.order_time).date()).days
            if 0 <= order_date_index < 7:  # 确保索引在范围内
                order_counts01[6 - order_date_index] += 1  # 反转索引，最久的在前

        orders02 = OrdersInformation.objects.filter(order_time__range=[start_date, today + timedelta(days=1)],order_commodity_type='1')
        # 用于每天的订单数初始化为0的列表
        order_counts02 = [0] * 7  # 7天（今天和过去6天）
        # 统计每天的订单数量，从最久到最近
        for order in orders02:
            
            order_date_index = (today  - timezone.localtime(order.order_time).date()).days
            if 0 <= order_date_index < 7:  # 确保索引在范围内
                order_counts02[6 - order_date_index] += 1  # 反转索引，最久的在前
        
        return Response({'0':order_counts01,'1':order_counts02})

# 多重查询订单页面页数
class ordersSystemCountView(APIView):
    # 查询订单页面页数
    def post(self,request):
        if request.data['order_people_address']!='':
            request.data['order_people_address']=request.data['order_people_address'][2]
        orders_information_count = OrdersInformation.objects.filter(Q(order_id__icontains=request.data.get('order_id')) & Q(order_commodity_name__icontains=request.data.get('order_commodity_name')) & Q(order_shop_name__icontains=request.data.get('order_shop_name')) & Q(order_commodity_type__icontains=request.data.get('order_commodity_type')) & Q(order_people_account__icontains=request.data.get('order_people_account')) & Q(order_people_phone__icontains=request.data.get('order_people_phone')) & Q(order_people_name__icontains=request.data.get('order_people_name')) & Q(order_people_address__icontains=request.data.get('order_people_address')) & Q(order_commodity_type__icontains=request.data.get('order_commodity_type'))).count()
        # commodity_information_count = CommodityInformation.objects.filter(Q(commodityName__icontains=request.data.get('commodityName')) & Q(commodityType__icontains=request.data.get('commodityType')) & Q(commodityShopName__icontains=request.data.get('commodityShopName'))).count()
        return Response(orders_information_count)

# 后台管理订单
class ordersSystemView(APIView):
    # 后台获取订单
    def post(self,request):
        if request.data['order_people_address']!='':
            request.data['order_people_address']=request.data['order_people_address'][2]
        orders_information = OrdersInformation.objects.filter(Q(order_id__icontains=request.data.get('order_id')) & Q(order_commodity_name__icontains=request.data.get('order_commodity_name')) & Q(order_shop_name__icontains=request.data.get('order_shop_name')) & Q(order_commodity_type__icontains=request.data.get('order_commodity_type')) & Q(order_people_account__icontains=request.data.get('order_people_account')) & Q(order_people_phone__icontains=request.data.get('order_people_phone')) & Q(order_people_name__icontains=request.data.get('order_people_name')) & Q(order_people_address__icontains=request.data.get('order_people_address')) & Q(order_commodity_type__icontains=request.data.get('order_commodity_type')))[(request.data.get('commodityPage')-1)*10:request.data.get('commodityPage')*10]
        serializer = OrdersSerializers(instance=orders_information,many=True)
        res = [dict(item) for item in serializer.data]
        for key in res:
            key['order_commodity_photo'] = out_picture(str('local_file/orders/'+key['order_commodity_photo']))
            # 解析字符串为 datetime 对象
            dt = parser.isoparse(key['order_time'])
            # 格式化为所需的字符串格式
            key['order_time'] = dt.strftime("%Y-%m-%d %H:%M:%S")
        return Response(res)
    
# 后台管理订单
class ordersSystemDetailView(APIView):
    # 后台修改某个订单
    def put(self,request,id):
        updateData = OrdersInformation.objects.get(order_id=request.data.get('order_id'))
        updateData.order_people_name=request.data.get('order_people_name')
        updateData.order_people_address=request.data.get('order_people_address')
        updateData.order_people_detailed_address=request.data.get('order_people_detailed_address')
        updateData.order_people_phone=request.data.get('order_people_phone')
        updateData.save()
        return Response('res')
        
    # 后台删除某个订单
    def delete(self,request,id):
        file_model=OrdersInformation.objects.get(id=id)
        default_storage.delete('local_file/order/'+str(file_model.order_commodity_photo))
        OrdersInformation.objects.get(id=id).delete()
        return Response('删除成功！')   

# 用户管理订单
class ordersView(APIView):
    # 用户提交订单
    def post(self,request):
        isNumber = 0
        while isNumber==0:
            orders_id = 'NSF'+str(random.randint(10000000000, 99999999999))  # 11位的范围
            allOrders = OrdersInformation.objects.all()
            for key in allOrders:
                if orders_id==key.order_id:
                    continue
            isNumber=1
        request.data['order_id']=orders_id
        file_name = orders_id+'.jpg'
        orderImg = request.data.get('order_commodity_photo')
        request.data['order_commodity_photo']=file_name
        if request.data['order_commodity_type']=='竹编家具':
            request.data['order_commodity_type']=0
        else:
            request.data['order_commodity_type']=1
        request.data['order_price']=round(float(request.data['order_price'])*request.data['order_number'],2)
        serializer = OrdersSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            save_picture('local_file/orders/' ,file_name,orderImg)
            return Response({'success':0})
        else:
            print(serializer.errors)
            return Response({ 'success':2,'errorType' :serializer.errors})



# 用户端产品数据
class commoditySearchPeopleTableView(APIView):
    # 查询产品类型
    def post(self,request):
        # 假设 request.data.get('commodityOther') 返回 ['灯罩', '装饰物品']
        selected_values = request.data.get('commodityOther', [])
        commodity_type = request.data.get('commodityType')
        commodity_name = request.data.get('commodityName')
        # 构造查询
        q_objects = Q()
        for value in selected_values: 
            q_objects |= Q(commodityOther__icontains=value)
        if commodity_type:
            q_objects &= Q(commodityType=commodity_type)
        if request.data.get('commodityPriceBefore')  or  request.data.get('commodityPriceAfter'):
            price_q_objects = Q(commodityPriceBefore__gt = Decimal(request.data.get('commodityPriceBefore')) ) & Q(commodityPriceAfter__lt= Decimal(request.data.get('commodityPriceAfter')) )
            q_objects &= price_q_objects
        if commodity_name:
            name_q_object = Q(commodityName__icontains = request.data.get('commodityName')) | Q(commodityShopName__icontains = request.data.get('commodityName'))
            q_objects &= name_q_object
        commodity_information = CommodityInformation.objects.filter(q_objects)
        serializer = CommoditySerializers(instance=commodity_information,many=True)
        res = [dict(item) for item in serializer.data]
        for key in res:
            key['commodityPhoto'] = out_picture(str('local_file/commodity/'+key['commodityPhoto']))
        return Response(res)


# 用户端产品风格
class commoditySearchTypeView(APIView):
    # 查询产品类型
    def post(self,request):
        commodity =  CommodityInformation.objects.filter(commodityType=request.data.get('commodityType'))
        commodityOther = []
        for key in commodity:
            commodityOther.append(key.commodityOther)
        commodityOtherResult = list(set(commodityOther))
        if len(commodityOtherResult)<10:
            return Response(commodityOtherResult)
        else:
            return random.sample(commodityOtherResult,10)

# 多重查询商品页面页数
class commoditySearchCountView(APIView):
    # 查询商品页面页数
    def post(self,request):
        commodity_information_count = CommodityInformation.objects.filter(Q(commodityName__icontains=request.data.get('commodityName')) & Q(commodityType__icontains=request.data.get('commodityType')) & Q(commodityShopName__icontains=request.data.get('commodityShopName'))).count()
        return Response(commodity_information_count)

# 多重查询商品
class commoditySearchView(APIView):
    # 多重查询商品数据
    def post(self,request):
        commodity_information = CommodityInformation.objects.filter(Q(commodityName__icontains=request.data.get('commodityName')) & Q(commodityType__icontains=request.data.get('commodityType')) & Q(commodityShopName__icontains=request.data.get('commodityShopName')) )[(request.data.get('commodityPage')-1)*10:request.data.get('commodityPage')*10]
        serializer = CommoditySerializers(instance=commodity_information,many=True)
        res = [dict(item) for item in serializer.data]
        for key in res:
            key['commodityPhoto'] = out_picture(str('local_file/commodity/'+key['commodityPhoto']))
        return Response(res)

#   后台商品管理
class CommodityView(APIView):
    # 后台添加商品信息
    def post(self,request):
        if BusinessInformation.objects.filter(business_name = request.data.get('commodityShopName')).first() == None:
            return Response({'success':1})
        else:
            business = BusinessInformation.objects.get(business_name = request.data.get('commodityShopName'))
            request.data['businessId']=business.id
            commodityImg = request.data.get('commodityPhoto')
            file_name = request.data.get('commodityName')+request.data.get('commodityShopName')+'.jpg' 
            allFile = CommodityInformation.objects.all()
            for key in allFile:
                if key.commodityPhoto==file_name:
                    return Response({'success':3})
            request.data['commodityPhoto']=file_name
            serializer = CommoditySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            save_picture('local_file/commodity/' ,file_name,commodityImg)
            return Response({'success':0})
        else:
            print(serializer.errors)
            return Response({ 'success':2,'errorType' :serializer.errors})
        
# 根据id管理某个商品
class CommodityDetailView(APIView): 
    # 根据id修改商品
    def put(self,request,id):
      
        file_model = CommodityInformation.objects.get(id=id)
        default_storage.delete('local_file/commodity/'+str(file_model.commodityPhoto))
        commodityImg = request.data.get('commodityPhoto')
        file_name = request.data.get('commodityName')+request.data.get('commodityShopName')+'.jpg' 
        request.data['commodityPhoto']=file_name
        serializer = CommoditySerializers(file_model,data=request.data)
        if serializer.is_valid():
            serializer.save()
            save_picture('local_file/commodity/' ,file_name,commodityImg)
            return Response({'success':0})
        else:
            print(serializer.errors)
            return Response({ 'success':2,'errorType' :serializer.errors})
        
    # 根据id删除商品
    def delete(self,request,id):
        file_model=CommodityInformation.objects.get(id=id)
        default_storage.delete('local_file/commodity/'+str(file_model.commodityPhoto))
        CommodityInformation.objects.get(id=id).delete()
        return Response('删除成功！')   

#   后台获取消息推送页数
class ChatSearchCountView(APIView):
    # 后台管理消息推送页数
    def post(self,request):
        messageCount = ChatMessageInformation.objects.filter(Q(chatContent__icontains=request.data.get('chatContent')) & Q(chatId__icontains=request.data.get('chatId')) & Q(chatType__icontains=request.data.get('chatType')) & Q(chatTime__icontains=request.data.get('chatTime')) & Q(chatTitle__icontains=request.data.get('chatTitle')) ).count()
        return Response(messageCount)

#   后台获取消息推送
class ChatSearchView(APIView):
    # 后台管理消息推送
    def post(self,request):
        message = ChatMessageInformation.objects.filter(Q(chatContent__icontains=request.data.get('chatContent')) & Q(chatId__icontains=request.data.get('chatId')) & Q(chatType__icontains=request.data.get('chatType')) & Q(chatTime__icontains=request.data.get('chatTime')) & Q(chatTitle__icontains=request.data.get('chatTitle')) )[(request.data.get('message_page')-1)*10:request.data.get('message_page')*10]
        serializer = ChatMessageSerializers(instance=message,many=True)
        return Response(serializer.data)
        
#   用户接收消息推送
class ChatPeopleDetailView(APIView):
    # 用户获取消息推送
    def get(self,request,id):
        information = LoginInformation.objects.filter(id=id).first()
        chatPeople = ChatMessageInformation.objects.filter(Q(chatId=information.account) | Q(chatType='0') )
        serializer = ChatMessageSerializers(instance=chatPeople,many=True)
        return Response(serializer.data)

# 官方消息推送
class ChatMessageView(APIView):
    # 后台添加消息推送
    def post(self,request):
        if request.data.get('chatType')=='':
            return Response('类型不能为空！')
        else :
            if request.data.get('chatId')=='' and request.data.get('chatType')=='1':
                return Response({"success":1})
            elif request.data.get('chatId')=='' and request.data.get('chatType')=='0':
                request.data['loginId']=1
                serializer = ChatMessageSerializers(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"success":0})
                else:
                    return Response(serializer.errors)
            elif  request.data.get('chatType')=='1' and LoginInformation.objects.filter(account=request.data.get('chatId')).first()==None:
                return Response({"success":2})
            else:

                business  = LoginInformation.objects.get(account=request.data.get('chatId'))
                request.data['loginId']=business.id
                serializer = ChatMessageSerializers(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"success":0})
                else:
                    return Response(serializer.errors)
 #   官方消息推送管理
class ChatMessageDetailView(APIView):
    # 删除官方消息推送
    def delete(self,request,id):
        ChatMessageInformation.objects.get(id=id).delete()
        return Response('删除成功！')               


# 同意成为商家，改变状态
class agreeBusinessDetailView(APIView):
    # 同意成为商家
    def get(self,request,id):
        business  = BusinessInformation.objects.get(id=id)
        business.business_agree=0
        business.save()
        return Response('同意成功')
    
     # 不同意成为商家
    def delete(self,request,id):
        file_model=BusinessInformation.objects.get(id=id)
        default_storage.delete('local_file/business/imgs/business_name_photo/'+str(file_model.business_name_photo))
        default_storage.delete('local_file/business/imgs/business_shop_photo/'+str(file_model.business_shop_photo))
        default_storage.delete('local_file/business/imgs/business_license_photo/'+str(file_model.business_license_photo))
        BusinessInformation.objects.get(id=id).delete()
        return Response('删除成功！')

# 多重查询商家申请表
class businessSearchView(APIView):
    # 添加商家申请表数据
    def post(self,request):
        if request.data['business_address']!='':
            request.data['business_address']=request.data['business_address'][2]
        business_information = BusinessInformation.objects.filter(Q(business_submit_time__icontains=request.data.get('business_submit_time')) & Q(business_id__icontains=request.data.get('business_id')) & Q(business_name__icontains=request.data.get('business_name')) & Q(business_true_name__icontains=request.data.get('business_true_name')) & Q(business_identification_number__icontains=request.data.get('business_identification_number')) & Q(business_type__icontains=request.data.get('business_type')) & Q(business_phone__icontains=request.data.get('business_phone')) & Q(business_address__icontains=request.data.get('business_address')) & Q(business_agree=request.data.get('business_agree')))[(request.data.get('business_page')-1)*10:request.data.get('business_page')*10]
        serializer = BusinessSerializers(instance=business_information,many=True)
        res = [dict(item) for item in serializer.data]
        for key in res:
            key['business_name_photo'] = out_picture(str('local_file/business/imgs/business_name_photo/'+key['business_name_photo']))
            key['business_shop_photo'] = out_picture(str('local_file/business/imgs/business_shop_photo/'+key['business_shop_photo']))
            key['business_license_photo'] = out_picture(str('local_file/business/imgs/business_license_photo/'+key['business_license_photo']))
            if key['business_type']=='0':
                key['business_type']='竹编家具'
            else :
                key['business_type']='工艺品'
        return Response(res)

# 多重查询商家申请表页数
class businessSearchCountView(APIView):
    # 查询商家申请表页数
    def post(self,request):
        if request.data['business_address']!='':
            request.data['business_address']=request.data['business_address'][2]
        business_information_count = BusinessInformation.objects.filter(Q(business_submit_time__icontains=request.data.get('business_submit_time')) & Q(business_id__icontains=request.data.get('business_id')) & Q(business_name__icontains=request.data.get('business_name')) & Q(business_true_name__icontains=request.data.get('business_true_name')) & Q(business_identification_number__icontains=request.data.get('business_identification_number')) & Q(business_type__icontains=request.data.get('business_type')) & Q(business_phone__icontains=request.data.get('business_phone')) & Q(business_address__icontains=request.data.get('business_address')) & Q(business_agree=request.data.get('business_agree'))).count()
        return Response(business_information_count)

# 对商家申请表进行管理
class businessView(APIView):
    # 添加商家申请表
    def post(self,request):
        phone = LoginInformation.objects.filter(phone = request.data.get('business_phone')).first()
        phone_business = BusinessInformation.objects.filter(business_phone = request.data.get('business_phone')).first()
        if phone or phone_business:
            return Response({'success':1,'errorType' :1})
        if request.data['business_id']!='admin':
            information = LoginInformation.objects.get(id=request.data.get('business_id'))
            request.data['business_id']=information.account
        business_name_photo = request.data.get('business_name_photo')
        business_shop_photo = request.data.get('business_shop_photo')
        business_license_photo = request.data.get('business_license_photo')
        file_name =request.data.get('business_true_name')+request.data.get('business_identification_number')+'.jpg' 
        if request.data.get('business_name_photo')!='' and request.data.get('business_shop_photo')!='' and request.data.get('business_license_photo')!='' :
            request.data['business_name_photo']=file_name
            request.data['business_license_photo']=file_name
            request.data['business_shop_photo']=file_name
        else :
            return Response({'success':1,'errorType' :[]})
        serializer = BusinessSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            save_picture('local_file/business/imgs/business_name_photo/' ,file_name,business_name_photo)
            save_picture('local_file/business/imgs/business_shop_photo/',file_name,business_shop_photo)
            save_picture('local_file/business/imgs/business_license_photo/',file_name,business_license_photo)
            return Response({'success':0})
        else:
            return Response({ 'success':1,'errorType' :serializer.errors})
    # 获取首页的十个商家申请表
    def get(self,request):
        
        business_information = BusinessInformation.objects.filter(Q(business_agree=request.data.get('business_agree')))[:10]
        serializer = BusinessSerializers(instance=business_information,many=True)
        res = [dict(item) for item in serializer.data]
        for key in res:
            key['business_name_photo'] = out_picture(str('local_file/business/imgs/business_name_photo/'+key['business_name_photo']))
            key['business_shop_photo'] = out_picture(str('local_file/business/imgs/business_shop_photo/'+key['business_shop_photo']))
            key['business_license_photo'] = out_picture(str('local_file/business/imgs/business_license_photo/'+key['business_license_photo']))
            if key['business_type']=='0':
                key['business_type']='竹编家具'
            else :
                key['business_type']='工艺品'
        return Response(res)


# base64图片保存
def save_picture(file_path,file_name,file):
    encode_image = file.split(',')[1]
    binary_data = base64.b64decode(encode_image)
    photo_path=file_path+file_name
    default_storage.save( photo_path,ContentFile(binary_data))
    return 0
# 将图片转为base64给前端
def out_picture(file_name):
    file_content = default_storage.open(file_name).read()
    data_url = f"data:image/{file_name};base64," + base64.b64encode(file_content).decode('utf-8')
    return data_url

# 对上传的图片返回base64
class returnPhotoView(APIView):
    # 根据上传的照片进行解码返回base64
    def post(self,request):
        upload_file = request.FILES['file']
        upload_name = upload_file.name
        upload_content = upload_file.read()
        data_url = f"data:image/{upload_name};base64," + base64.b64encode(upload_content).decode('utf-8')
        return Response(data_url)
    def get(self,request):
        return Response('ok')
    
# 对反馈信息进行管理
class suggestionView(APIView):
    # 获取反馈信息的前十条
    def get(self,request):
        suggestion = suggestionInformation.objects.all()[:10]
        serializer = suggestionSerializers(instance=suggestion,many=True)
        return Response(serializer.data)
    # 添加反馈信息
    def post(self,request):
        serializer = suggestionSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':0})
        else:
            return Response(serializer.errors)
# 对反馈信息进行操作
class suggestionDetailView(APIView):
    # 修改反馈信息的未读状态
    def put(self,request,id):
        suggestion  = suggestionInformation.objects.get(id=id)
        serializer = suggestionSerializers(instance=suggestion,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    # 根据id进行反馈建议信息的删除
    def delete(self,request,id):
        suggestionInformation.objects.get(id=id).delete()
        return Response({'success':'删除成功！'})
# 反馈建议的复合查找功能
class searchSuggestionView(APIView):
    def post(self,request):
        if request.data.get('searchSuggestionPage')=='':
            count = suggestionInformation.objects.filter(Q(feedback_status__icontains=request.data.get('searchSuggestionStatus')) & Q(feedback__icontains=request.data.get('searchSuggestionFeedback')) ).count()
            return Response(count)
        else:
            suggestion = suggestionInformation.objects.filter(Q(feedback_status__icontains=request.data.get('searchSuggestionStatus')) & Q(feedback__icontains=request.data.get('searchSuggestionFeedback')) )[(request.data.get('searchSuggestionPage')-1)*10:request.data.get('searchSuggestionPage')*10]
            serializer = suggestionSerializers(instance=suggestion,many=True)
        return Response(serializer.data)
    
# 成功登录，返回部分个人信息
class successView(APIView):
    def post(self,request):
        if request.data.get('phone')=='':
            return Response({'手机号不能为空!'})
        information = LoginInformation.objects.filter(phone=request.data.get('phone')).first()
        if information!=None :
            serializer = SuccessSerializers(instance=information,many=False)
            file_content = default_storage.open(str(information.file_name)).read() 
            data_url = f"data:image/{str(information.file_name)};base64," + base64.b64encode(file_content).decode('utf-8')
            res = dict(serializer.data)
            res['file_name'] = data_url
            return Response(res)
    
# 判断手机号是否为空或者已存在
class verifyView(APIView):
    def post(self,request):
        if request.data.get('phone')=='':
            return Response({'手机号不能为空!'})
        if LoginInformation.objects.filter(phone=request.data.get('phone')).first() :
            return Response({'手机号已存在!'})
        return Response('')
    
# 获取默认头像
class avatarView(APIView):
    # 获取默认头像
    def get(self,request):
        static_path = 'local_file/information_photo/default_img/toux.png'
        file_content = default_storage.open(static_path).read() 
        data_url = f"data:image/{static_path};base64," + base64.b64encode(file_content).decode('utf-8')
        return Response(data_url)
    # 头像上传的空链接
    def post(self,request):
        return Response('ok')
# 对轮播图进行管理
class LunBoTuView(APIView):
    # 获取全部的轮播图
    def get(self,request):
        upload_data = LunBoTuInformation.objects.all()
        image_data = []
        for img in upload_data:
            file_id = img.id
            file_name = img.name
            file_content = default_storage.open(file_name).read()
            data_url = f"data:image/{img.image};base64," + base64.b64encode(file_content).decode('utf-8')
            image_data.append({'id':file_id,'name':file_name,'file':data_url})
        return Response(image_data)
    # 添加轮播图
    def post(self,request):
        upload_file = request.FILES['file']
        upload_name = 'local_file/lun/'+upload_file.name
        upload_content = upload_file.read()
        file_path = default_storage.save(upload_name,ContentFile(upload_content))
        file_model = LunBoTuInformation(name=upload_name,image=file_path)
        file_model.save()
        return JsonResponse({'message':'文件上传成功'})
# 根据id轮播图的删除
class LunBoTuDetailView(APIView):
    def delete(self,request,id):
        delete_data = LunBoTuInformation.objects.get(id=id)
        delete_name = delete_data.name
        default_storage.delete(delete_name)
        LunBoTuInformation.objects.get(id=id).delete()
        upload_data = LunBoTuInformation.objects.all()
        image_data = []
        for img in upload_data:
            file_id = img.id
            file_name = img.name
            file_content = default_storage.open(file_name).read()
            data_url = f"data:image/{img.image};base64," + base64.b64encode(file_content).decode('utf-8')
            image_data.append({'id':file_id,'name':file_name,'file':data_url})
        return Response(image_data)
    
# 复合查询个人信息
class SearchDetailView(APIView):
    # 根据复合信息进行查找
    def post(self,request):
        if request.data.get('searchTime')==0:
            if request.data.get('searchPage')=='':
                if request.data.get('searchGender')!='':
                    count = LoginInformation.objects.filter( gender=request.data.get('searchGender') and  Q(phone__icontains=request.data.get('searchContent')) | Q(username__icontains=request.data.get('searchContent')) | Q(account__icontains=request.data.get('searchContent'))  ).count()
                    return Response(count)
                else :
                    count = LoginInformation.objects.filter( Q(phone__icontains=request.data.get('searchContent')) | Q(username__icontains=request.data.get('searchContent')) | Q(account__icontains=request.data.get('searchContent'))  ).count()
                    return Response(count)
            else :
                if request.data.get('searchContent')!='':
                    if request.data.get('searchGender')!='':
                        login = LoginInformation.objects.filter( gender=request.data.get('searchGender') and  Q(phone__icontains=request.data.get('searchContent')) | Q(username__icontains=request.data.get('searchContent')) | Q(account__icontains=request.data.get('searchContent'))  )
                    else:
                        login = LoginInformation.objects.filter( Q(phone__icontains=request.data.get('searchContent')) | Q(username__icontains=request.data.get('searchContent')) | Q(account__icontains=request.data.get('searchContent')))[(request.data.get('searchPage')-1)*10:request.data.get('searchPage')*10]
                else :
                    if request.data.get('searchGender')!='':
                        login = LoginInformation.objects.filter(gender=request.data.get('searchGender'))[(request.data.get('searchPage')-1)*10:request.data.get('searchPage')*10]
                    else:
                        login = LoginInformation.objects.all()[(request.data.get('searchPage')-1)*10:request.data.get('searchPage')*10]
        else :
            if request.data.get('searchPage')=='':
                if request.data.get('searchGender')!='':
                    count = LoginInformation.objects.filter( gender=request.data.get('searchGender') and  Q(phone__icontains=request.data.get('searchContent')) | Q(username__icontains=request.data.get('searchContent')) | Q(account__icontains=request.data.get('searchContent'))  ).count()
                    return Response(count)
                else :
                    count = LoginInformation.objects.filter( Q(phone__icontains=request.data.get('searchContent')) | Q(username__icontains=request.data.get('searchContent')) | Q(account__icontains=request.data.get('searchContent'))  ).count()
                    return Response(count)
            else :
                
                if request.data.get('searchContent')!='':
                    if request.data.get('searchGender')!='':
                        login = LoginInformation.objects.filter( gender=request.data.get('searchGender') and  Q(phone__icontains=request.data.get('searchContent')) | Q(username__icontains=request.data.get('searchContent')) | Q(account__icontains=request.data.get('searchContent'))  ).order_by('-login_time')
                    else:
                        login = LoginInformation.objects.filter( Q(phone__icontains=request.data.get('searchContent')) | Q(username__icontains=request.data.get('searchContent'))| Q(account__icontains=request.data.get('searchContent'))).order_by('-login_time')[(request.data.get('searchPage')-1)*10:request.data.get('searchPage')*10]
                else :
                    
                    if request.data.get('searchGender')!='':
                        login = LoginInformation.objects.filter(gender=request.data.get('searchGender')).order_by('-login_time')[(request.data.get('searchPage')-1)*10:request.data.get('searchPage')*10]
                    else:
                        
                        login = LoginInformation.objects.all().order_by('-login_time')[(request.data.get('searchPage')-1)*10:request.data.get('searchPage')*10]
        upload_data = []
        for i in login:
            file_content = default_storage.open(str(i.file_name)).read()
            data_url = f"data:image/{str(i.file_name)};base64," + base64.b64encode(file_content).decode('utf-8')
            i.file_name=data_url
            if i.gender == 0:
                i.gender = '女'
            else :
                i.gender='男'
            if i.status == 0 :
                i.status = '离线'
            else :
                i.status = '在线'
            if i.username_type==0:
                i.username_type='管理员'
            elif i.username_type==1:
                i.username_type='用户'
            elif i.username_type==2:
                i.username_type='商家'
            elif i.username_type==3:
                i.username_type='客服'
            upload_data.append({'id':i.id,'username':i.username,'phone':i.phone,'file_name':data_url,'password':i.password,'gender':i.gender,'login_time':i.login_time,'status':i.status,'account':i.account,'detailed_address':i.detailed_address,'address':i.address,'username_type':i.username_type})
        return Response(upload_data)

# 管理个人信息
class LoginView(APIView):
    # 获取全部个人信息
    def get(self,request):
        login = LoginInformation.objects.all()[:10]
        upload_data = []
        for i in login:
            file_content = default_storage.open(str(i.file_name)).read()
            data_url = f"data:image/{str(i.file_name)};base64," + base64.b64encode(file_content).decode('utf-8')
            i.file_name=data_url
            if i.gender == 0:
                i.gender = '女'
            else :
                i.gender='男'
            if i.status == 0 :
                i.status = '离线'
            else :
                i.status = '在线'
            if i.username_type==0:
                i.username_type='管理员'
            elif i.username_type==1:
                i.username_type='用户'
            elif i.username_type==2:
                i.username_type='商家'
            elif i.username_type==3:
                i.username_type='客服'
            upload_data.append({'id':i.id,'username':i.username,'phone':i.phone,'file_name':data_url,'password':i.password,'gender':i.gender,'login_time':i.login_time,'status':i.status,'account':i.account,'detailed_address':i.detailed_address,'address':i.address,'username_type':i.username_type})
        return Response(upload_data)
    # 添加个人信息
    def post(self,request):
        print(type(request.data.get('photo')))
        upload_path = request.data.get('photo')
        encode_image = upload_path.split(',')[1]
        binary_data = base64.b64decode(encode_image)
        file_name='local_file/information_photo/imgs/'+request.data.get('file_name')
        file_path = default_storage.save( file_name,ContentFile(binary_data))
        request.data['file_name']=file_path
        request.data.pop('photo')
        if request.data.get('gender') == '女':
            request.data['gender']=0
        else :
            request.data['gender']=1
        if request.data.get('status') == '离线': 
            request.data['status']=1
        else :
            request.data['status']=1
        file_model = LoginInformation(phone=request.data.get('phone'),file_name=file_path,username=request.data.get('username'),gender=request.data.get('gender'),password=request.data.get('password'),account=request.data.get('phone'),detailed_address=request.data.get('detailed_address'),address=request.data.get('address'),username_type=request.data.get('username_type'))
        file_model.save()
        login = LoginInformation.objects.all()[:10]
        for i in login:
            file_content = default_storage.open(str(i.file_name)).read()
            data_url = f"data:image/{str(i.file_name)};base64," + base64.b64encode(file_content).decode('utf-8')
            i.file_name=data_url
        serializer = LoginSerializers(instance=login,many=True)
        if request.data.get('username_type')=='1':
            return Response({'success':0})
        
        return Response(serializer.data)
    
# 根据id对个人信息进行操作
class LoginDetailView(APIView):
    # 获取某个用户的信息
    def get(self,request,id):
        login = LoginInformation.objects.get(id=id)
        serializer = LoginSerializers(instance=login,many=False)
        file_content = default_storage.open(str(login.file_name)).read() 
        data_url = f"data:image/{str(login.file_name)};base64," + base64.b64encode(file_content).decode('utf-8')
        res = dict(serializer.data)
        res['file_name'] = data_url
        
        return Response(res)
# 删除某个用户信息
    def delete(self,request,id):
        file_model = LoginInformation.objects.get(id=id)
        default_storage.delete(str(file_model.file_name))
        LoginInformation.objects.get(id=id).delete()
        return Response('删除成功！')
    # 修改某个用户信息
    def put(self,request,id):
        # 判断手机号是否存在
        is_phone = LoginInformation.objects.get(id=id)
        if is_phone.phone!=request.data.get('phone'):
            allInformation = LoginInformation.objects.all()
            for key in allInformation:
                if key.phone == request.data.get('phone'):
                    return Response({"success":'1'})
        file_model = LoginInformation.objects.get(id=id)
        default_storage.delete(str(file_model.file_name))
        upload_path = request.data.get('photo')
        encode_image = upload_path.split(',')[1]
        binary_data = base64.b64decode(encode_image)
        file_path = default_storage.save('local_file/information_photo/imgs/'+request.data.get('file_name'),ContentFile(binary_data))
        request.data['file_name']=file_path
        request.data.pop('photo')
        if request.data.get('gender') == '女':
            request.data['gender']=0
        else :
            request.data['gender']=1
        if request.data.get('status') == '离线': 
            request.data['status']=1
        else :
            request.data['status']=1
        if request.data['username_type']=='管理员':
                request.data['username_type']=0
        elif request.data['username_type']=='用户':
                request.data['username_type']=1
        elif request.data['username_type']=='商家':
                request.data['username_type']=2
        elif request.data['username_type']=='客服':
                request.data['username_type']=3
        LoginInformation.objects.filter(id=id).update(phone=request.data.get('phone'),file_name=file_path,username=request.data.get('username'),gender=request.data.get('gender'),password=request.data.get('password'),detailed_address=request.data.get('detailed_address'),address=request.data.get('address'),username_type=request.data.get('username_type'))
        return Response('修改成功！')

# 用户登录
class peopleLogin(APIView):
    # 存储session登录用户的信息
    def post(self,request):
        people = LoginInformation.objects.filter(account = request.data.get('account'),password = request.data.get('password'),username_type = '1').first()
        if people == None:
            return Response({'success':1})
        else:
            # request.session["people"] = {  }
            request.session["people"] = { 'id':people.id }
        return Response({'success':0})
    # 获取登录用户的信息
    def get(self,request):
        people = request.session.get('people')
        if not people:
            return Response({'success':1})
        else:
            people = LoginInformation.objects.filter(id=people['id']).first()
            serializer = LoginSerializers(instance=people,many=False)
            file_content = default_storage.open(str(people.file_name)).read() 
            data_url = f"data:image/{str(people.file_name)};base64," + base64.b64encode(file_content).decode('utf-8')
            res = dict(serializer.data)
            res['file_name'] = data_url
            return Response(res)
# 删除session信息
class peopleCloseLogin(APIView):
    def get(self,request):
        request.session.pop('people')
        return Response({'success':0})
    
# 后台登录
class manageLogin(APIView):
    # 存储session登录后台管理的信息
    def post(self,request):
        people = LoginInformation.objects.filter(account = request.data.get('account'),password = request.data.get('password'),username_type = request.data.get('username_type')).first()
        if people == None:
            return Response({'success':1})
        else:
            # request.session["people"] = {  }
            request.session["manage"] = { 'id':people.id }
        return Response({'success':0})
    # 获取登录后台的信息
    def get(self,request):
        people = request.session.get('manage')
        if people == None:
            return Response({'success':1})
        people = LoginInformation.objects.filter(id=people['id']).first()
        serializer = LoginSerializers(instance=people,many=False)
        return Response(serializer.data)
# 删除session后台管理信息
class manageCloseLogin(APIView):
    def get(self,request):
        request.session.pop('manage')
        return Response({'success':0})
    
# 删除session后台管理信息
class idBusinessLogin(APIView):
    def post(self,request):
        people = LoginInformation.objects.filter(account=request.data.get('business_id')).first()
        serializer = LoginSerializers(instance=people,many=False)
        return Response(serializer.data)

