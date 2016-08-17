# -*- coding: utf-8 -*-
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business.mall.product_pool import ProductPool
from db.mall import models as mall_models
from business.account.user_profile import UserProfile
from business import model as business_model
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from settings import PANDA_IMAGE_DOMAIN
from services.product_service.task import clear_sync_product_cache


class Product(business_model.Model):
    __slots__ = (
        'id',
        'owner_id',
        'name',
        'physical_unit',
        'price',
        'introduction',
        'weight',
        'thumbnails_url',
        'pic_url',
        'detail',
        'remark',
        'display_index',
        'created_at',
        'shelve_type',
        'shelve_start_time',
        'shelve_end_time',
        'min_limit',
        'stock_type',
        'stocks',
        'is_deleted',
        'is_support_make_thanks_card',
        'type',
        'update_time',
        'postage_id',
        'is_use_online_pay_interface',
        'is_use_cod_pay_interface',
        'promotion_title',
        'user_code',
        'bar_code',
        'unified_postage_money',
        'postage_type',
        'is_member_product',
        'supplier',
        'supplier_user_id',
        'supplier_name',
        'purchase_price',
        'is_enable_bill',
        'is_delivery',
        'buy_in_supplier',

        'is_model_deleted',
        'custom_model_properties',
        'model_type',
        'swipe_images',
        'model_name',
        'model',
        'categories',
        'properties',

        'group_buy_info'
    )

    def __init__(self, model):
        super(Product, self).__init__()

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    def empty_product():
        product = Product(None)
        return product

    @staticmethod
    @param_required(['db_model'])
    def from_model(args):
        model = args['db_model']
        product = Product(model)
        return product

    @staticmethod
    @param_required(['product_id'])
    def from_id(args):
        product_db_model = mall_models.Product.get(id=args['product_id'])
        return Product(product_db_model)

    @staticmethod
    @param_required(['product_id'])
    def from_panda_product_id(args):
        panda_product = mall_models.PandaHasProductRelation.select()\
            .dj_where(panda_product_id=args['product_id']).first()
        if panda_product:
            product_db_model = mall_models.Product.get(id=panda_product.weapp_product_id)
            return Product(product_db_model)

    @staticmethod
    @param_required(['product_ids'])
    def from_ids(args):
        product_models = mall_models.Product.select().dj_where(id__in=args['product_ids'])
        products = []
        for model in product_models:
            products.append(Product(model))
        return products

    def fill_specific_model(self, model_name):
        product_model = mall_models.ProductModel.select().dj_where(product_id=self.id, name=model_name).first()
        product = self
        product.price = product_model.price
        product.weight = product_model.weight
        product.stock_type = product_model.stock_type
        product.stocks = product_model.stocks
        product.model_name = model_name
        product.model = product_model
        product.is_model_deleted = False
        product.user_code = product_model.user_code
        if product_model.is_deleted:
            product.is_model_deleted = True

        property_ids = []
        property_value_ids = []
        name = product.model_name
        if product.model_name != 'standard':
            for model_property_info in product.model_name.split('_'):
                property_id, property_value_id = model_property_info.split(':')
                property_ids.append(property_id)
                property_value_ids.append(property_value_id)

                id2property = dict(
                    [
                        (property.id, {"id": property.id, "name": property.name})
                        for property in mall_models.ProductModelProperty.select().dj_where(id__in=property_ids)
                    ])
                for property_value in mall_models.ProductModelPropertyValue.select().dj_where(id__in=property_value_ids):
                    id2property[property_value.property_id]['property_value'] = property_value.name
                    id2property[property_value.property_id]['property_pic_url'] = property_value.pic_url
            product.custom_model_properties = id2property.values()
            product.custom_model_properties.sort(lambda x, y: cmp(x['id'], y['id']))
        else:
            product.custom_model_properties = None

    @property
    def models(self):
        """

        """
        models = self.context.get('models', None)
        if not models and self.id:
            # return ProductTemplateProperty.from_template_id({"template_id": self.id})
            pass
        return models

    @models.setter
    def models(self, models):
        """

        """
        self.context['models'] = models

    # def save(self, panda_product_id):
    #
    #     user_profile = UserProfile.from_webapp_type({'webapp_type': 2})
    #     if not user_profile:
    #         return None
    #     owner_id = user_profile[0].user_id
    #     product = mall_models.Product.create(
    #         owner=owner_id,
    #         name=self.name,
    #         supplier=self.supplier,
    #         detail=self.detail,
    #         pic_url='',
    #         introduction='',
    #         thumbnails_url=self.thumbnails_url,
    #         price=self.price,
    #         weight=self.weight,
    #         stock_type=self.stock_type,
    #         purchase_price=self.purchase_price,
    #         stocks=0,
    #         promotion_title=self.promotion_title if self.promotion_title else ''
    #
    #     )
    #     mall_models.PandaHasProductRelation.create(
    #         panda_product_id=int(panda_product_id),
    #         weapp_product_id=product.id,
    #     )
    #     new_product = Product(product)
    #
    #     return new_product

    def update(self):
        """

        """
        change_rows = mall_models.Product.update(name=self.name,
                                                 stock_type=self.stock_type,
                                                 purchase_price=self.purchase_price,
                                                 detail=self.detail,
                                                 price=self.price,
                                                 weight=self.weight,
                                                 promotion_title=self.promotion_title,
                                                 thumbnails_url=self.thumbnails_url
                                                 ).dj_where(id=self.id).execute()
        # 清理缓存
        try:

            clear_sync_product_cache.delay(product_id=self.id)
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            # print msg
        return change_rows

    def delete(self):
        """
        主要更新商品为已删除，然后关联关系需要更新不可见
        """
        #
        change_rows = mall_models.Product.update(is_deleted=True).dj_where(id=self.id).execute()
        if change_rows > 0:
            ProductPool.delete_from_product({'product_id': self.id})
        return change_rows

    @staticmethod
    @param_required(['product_ids'])
    def check_product_shelve_on(args):
        """
        获取已经上架的产品
        """
        product_ids = args.get('product_ids')
        pools = mall_models.ProductPool.select().dj_where(product_id__in=product_ids,
                                                          status=mall_models.PP_STATUS_ON)
        on_product_ids = [pool.product_id for pool in pools]
        return list(set(on_product_ids))

    @staticmethod
    @param_required(['product_id', 'owner_id'])
    def get_from_id(args):
        product_id = args['product_id']
        owner_id = args['owner_id']

        is_in_owner_pool = ProductPool.get({'owner_id': owner_id})
        # todo 临时关闭
        # if not is_in_owner_pool:
        #     return None
        db_model = mall_models.Product.select().dj_where(id=product_id).first()
        product = Product(db_model)
        return product

    @staticmethod
    def fill_details(owner_id, products, options):
        """填充各种细节信息

		此方法会根据options中的各种填充选项，填充相应的细节信息

        @param owner_id: owner_id
		@param[in] products: Product业务对象集合
		@param[in] options: 填充选项
			with_price: 填充价格信息
			with_product_model: 填充所有商品规格信息
			with_product_promotion: 填充商品促销信息
			with_image: 填充商品轮播图信息
			with_property: 填充商品属性信息
			with_selected_category: 填充选中的分类信息
			with_all_category: 填充所有商品分类详情
			with_sales: 填充商品销售详情
			with_group_buy_info: 填充团购信息
		"""

        if options.get('with_selected_category', False):
            Product.__fill_category_detail(
                owner_id,
                products,
                True)

        if options.get('with_all_category', False):
            Product.__fill_category_detail(
                owner_id,
                products,
                False)

        if options.get('with_image', False):
            Product.__fill_image_detail(products)

        if options.get('with_property', False):
            Product.__fill_property_detail(owner_id, products)

        if options.get('with_group_buy_info', False):
            Product.__fill_group_buy_info(owner_id, products)



    @staticmethod
    def __fill_group_buy_info(owner_id, products):

        product_ids = [str(p.id) for p in products]

        params = {
            'woid': owner_id,
            'pids': "_".join(product_ids)
        }

        resp = Resource.use('marketapp_apiserver').get({
            'resource': 'group.group_buy_products',
            'data': params
        })

        product2group_info = {}
        if resp and resp['code'] == 200:
            product_group_infos = resp['data']['pid2is_in_group_buy']

            for product_group in product_group_infos:
                product2group_info[product_group["pid"]] = product_group["is_in_group_buy"]

        for product in products:
            product.group_buy_info = {
                'is_in_group_buy': product2group_info.get(product.id, False)
            }


    @staticmethod
    def __fill_image_detail(products):
        for product in products:
            product.swipe_images = [
                {'id': img.id, 'url': img.url, 'linkUrl': img.link_url, 'width':
                    img.width, 'height': img.height,}
                for img in mall_models.ProductSwipeImage.select().dj_where(
                    product_id=product.id)]

    @staticmethod
    def __fill_category_detail(owner_id, products, only_selected_category):
        categories = mall_models.ProductCategory.select().dj_where(owner=owner_id).order_by('id')
        product_ids = [p.id for p in products]

        # 获取product关联的category集合
        id2product = dict([(product.id, product) for product in products])
        for product in products:
            product.categories = []
            product.context['id2category'] = {}
            id2product[product.id] = product
            if not only_selected_category:
                for category in categories:
                    category_data = {
                        'id': category.id,
                        'name': category.name,
                        'is_selected': False
                    }
                    product.categories.append(category_data)
                    product.context['id2category'][category.id] = category_data

        id2category = dict([(category.id, category) for category in categories])
        for relation in mall_models.CategoryHasProduct.select().dj_where(product_id__in=product_ids).order_by('id'):
            category_id = relation.category_id
            product_id = relation.product_id
            if not category_id in id2category:
                # 微众商城分类，在商户中没有
                continue
            category = id2category[category_id]
            if not only_selected_category:
                id2product[product_id].context['id2category'][
                    category.id]['is_selected'] = True
            else:
                id2product[product_id].categories.append({
                    'id': category.id,
                    'name': category.name,
                    'is_selected': True
                })

    @staticmethod
    def __fill_property_detail(owner_id, products):
        for product in products:
            product.properties = [
                {"id": property.id, "name": property.name,
                 "value": property.value}
                for property in mall_models.ProductProperty.
                    select().dj_where(product_id=product.id)]


class ProductModel(business_model.Model):

    __slots__ = (
        'id',
        'owner_id',
        'product_id',
        'name',
        'is_standard',
        'price',
        'stock_type',
        'stocks',
        'weight',
        'is_deleted',
        'purchase_price'
    )

    def __init__(self, model):
        super(ProductModel, self).__init__()
        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    def save(self):
        # 标准规格
        product_model = mall_models.ProductModel.create(
            owner=self.owner_id,
            product=self.product_id,
            name=self.name,
            is_standard=self.is_standard,
            price=self.price,
            stock_type=self.stock_type,
            stocks=self.stocks,
            purchase_price=self.purchase_price,
            is_deleted=self.is_deleted,
            weight=self.weight
        )
        return ProductModel(product_model)

    @staticmethod
    @param_required(['product_id'])
    def from_product_id(args):
        product_models = mall_models.ProductModel.select().dj_where(product_id=args['product_id'],
                                                                    is_deleted=False)

        return [ProductModel(product_model) for product_model in product_models]

    @staticmethod
    @param_required(['product_id', 'name'])
    def from_product_id_name(args):
        product_model = mall_models.ProductModel.select().dj_where(product_id=args['product_id'],
                                                                    is_deleted=False,
                                                                    name=args.get('name')).first()

        return ProductModel(product_model)

    def update(self):

        change_rows = mall_models.ProductModel.update(stock_type=self.stock_type,
                                        stocks=self.stocks).dj_where(id=self.id).execute()
        return  change_rows

    @staticmethod
    @param_required(['models'])
    def save_many(args):
        """
        保存多个
        """
        bulk_create = []
        models = args.get('models')
        bulk_create = [dict(owner=temp_model.owner_id,
                            product=temp_model.product_id,
                            name=temp_model.name,
                            is_standard=temp_model.is_standard,
                            price=temp_model.price,
                            stock_type=temp_model.stock_type,
                            stocks=temp_model.stocks,
                            is_deleted=temp_model.is_deleted,
                            weight=temp_model.weight,
                            purchase_price=temp_model.purchase_price) for temp_model in models]

        mall_models.ProductModel.insert_many(bulk_create).execute()

    @staticmethod
    @param_required(['models', 'product_id'])
    def update_many_models(args):
        """
        更新成多规格
        """
        models = args.get('models')
        if not models:
            return None

        # 已经有的规格,直接更新,否则添加
        # model_names = mall_models.ProductModel.select().dj_where(product_id=args.get('product_id'))
        # names = [model_name.name for model_name in model_names]
        # 需要新增的规格
        need_add = []
        try:
            # 如果是true说明是多规格商品,否则是单规格商品
            need_update_stand = True
            # 先暂时将所有的规格更新成已经删除
            mall_models.ProductModel.update(is_deleted=True).dj_where(product_id=args.get('product_id')).execute()
            for temp_model in models:
                if mall_models.ProductModel.select().dj_where(name=temp_model.name,
                                                              product_id=temp_model.product_id).count() > 0:
                    mall_models.ProductModel.update(price=temp_model.price,
                                                    stock_type=temp_model.stock_type,
                                                    stocks=temp_model.stocks,
                                                    weight=temp_model.weight,
                                                    purchase_price=temp_model.purchase_price,
                                                    is_deleted=temp_model.is_deleted)\
                        .dj_where(name=temp_model.name,
                                  product_id=temp_model.product_id).execute()
                    if temp_model.name == 'standard':
                        need_update_stand = False
                else:
                    need_add.append(temp_model)


            if need_add:
                ProductModel.save_many({'models': need_add})
            if need_update_stand:
                mall_models.ProductModel.update(is_deleted=True).dj_where(product_id=args.get('product_id'),
                                                                          name='standard').execute()
            return 'SUCCESS'
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return None


class ProductSwipeImage(business_model.Model):
    __slots__ = ()

    def __init__(self, model):
        super(ProductSwipeImage, self).__init__()
        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)
        # mall_models.ProductSwipeImage
        #     product = product,
        #     url = swipe_image['url'],
        #     width = swipe_image['width'],
        #     height = swipe_image['height']

    @staticmethod
    @param_required(['images'])
    def save_many(args):
        """

        """
        mall_models.ProductSwipeImage.insert_many(args.get('images')).execute()

    @staticmethod
    @param_required(['swipe_images', 'product_id'])
    def update_product_many(args):
        """
        更新用户的多个信息
        """
        mall_models.ProductSwipeImage.delete().dj_where(product=args['product_id']).execute()
        images = []
        for image in args['swipe_images']:
            url = image.get('url')
            if not url.startswith('http'):
                url = PANDA_IMAGE_DOMAIN + url
            images.append(dict(product=args['product_id'],
                               url=url,
                               width=100,
                               height=100))
        # images = [dict(product=args['product_id'],
        #                url=image.get('url'),
        #                width=100,
        #                height=100) for image in args['swipe_images']]

        # for image in self.swipe_images:

        ProductSwipeImage.save_many({'images': images})



