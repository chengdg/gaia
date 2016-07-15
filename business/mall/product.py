# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business import model as business_model
from settings import PRODUCT_POOL_USER_ID


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
        panda_product = mall_models.PandaProductToProduct.select()\
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

    def save(self, panda_product_id):
        owner_id = PRODUCT_POOL_USER_ID
        product = mall_models.Product.create(
            owner=owner_id,
            name=self.name,
            supplier=self.supplier,
            detail=self.detail,
            pic_url='',
            introduction='',
            thumbnails_url=self.thumbnails_url,
            price=self.price,
            weight=self.weight,
            stock_type=self.stock_type,
            purchase_price=self.purchase_price

        )
        mall_models.PandaProductToProduct.create(
            panda_product_id=int(panda_product_id),
            weapp_product=product.id,
        )
        new_product = Product(product)

        return new_product

    def update(self):
        """

        """
        change_rows = mall_models.Product.update(name=self.name,
                                                 stock_type=self.stock_type,
                                                 purchase_price=self.purchase_price,
                                                 detail=self.detail,
                                                 price=self.price,
                                                 weight=self.weight,
                                                 thumbnails_url=self.thumbnails_url
                                                 ).dj_where(id=self.id).execute()
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
        'weight'
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
            name='standard',
            is_standard=self.is_standard,
            price=self.price,
            stock_type=self.stock_type,
            stocks=self.stocks,
            weight=self.weight
        )
        return ProductModel(product_model)

    @staticmethod
    @param_required(['product_id', 'model_type'])
    def from_product_id(args):
        if args['model_type']:
            product_model = mall_models.ProductModel.select().dj_where(product_id=args['product_id'],
                                                                       name='standard',
                                                                       is_deleted=False).first()
            return ProductModel(product_model)

    def update(self):
        mall_models.ProductModel.update(price=self.price,
                                        stock_type=self.stock_type,
                                        stocks=self.stocks,
                                        weight=self.weight).dj_where(id=self.id,).execute()


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
        images = [dict(product=args['product_id'],
                       url=image.get('url'),
                       width=100,
                       height=100) for image in args['swipe_images']]

        # for image in self.swipe_images:

        ProductSwipeImage.save_many({'images': images})


class ProductPool(business_model.Model):
    """
    新商品池业务逻辑对象
    """
    __slots__ = (
        # user_id
        'woid',
        'product_id',
        'status'
    )

    def __init__(self):
        super(ProductPool, self).__init__()

    @staticmethod
    def save_many(pool):
        """

        """
        mall_models.ProductPool.insert_many(pool).execute()

    @staticmethod
    @param_required(['product_id', 'accounts'])
    def update_many(args):
        """
        accounts 需要显示的用户id列表(user_id)
        """
        product_pool = mall_models.ProductPool.select().dj_where(product_id=args.get('product_id'))
        # account_ids = [account.id for account in product_pool]
        woids = [str(account.woid) for account in product_pool]
        # 需要某个商户更新成不可件的
        off_woids = list(set(woids) - set(args.get('accounts')))
        # 需要某个商户下架的数据
        need_add = list(set(args.get('accounts')) - set(woids))

        # 需要新增到某个商户的
        pool = [dict(woid=account,
                     product_id=args.get('product_id'),
                     status=mall_models.PP_STATUS_ON_POOL) for account in need_add]

        if pool:
            ProductPool.save_many(pool)
        need_delete_ids = [p.id for p in product_pool if str(p.woid) in off_woids]
        mall_models.ProductPool.update(status=mall_models.PP_STATUS_DELETE)\
            .dj_where(id__in=need_delete_ids).execute()
        # 将不可见的因该更新成可见的进行更新
        mall_models.ProductPool.update(status=mall_models.PP_STATUS_ON_POOL) \
            .dj_where(product_id=args.get('product_id'),
                      status=mall_models.PP_STATUS_DELETE,
                      woid__in=args.get('accounts')).execute()

    @staticmethod
    @param_required(['product_id'])
    def delete_from_product(args):
        """
        因为同步商品删除，此处需要更新
        """
        mall_models.ProductPool.update(status=mall_models.PP_STATUS_DELETE)\
            .dj_where(product_id=args['product_id']).execute()
