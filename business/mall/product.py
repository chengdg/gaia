# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business.account.user_profile import UserProfile
from business import model as business_model
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from settings import PANDA_IMAGE_DOMAIN


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
        'model'
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

    def save(self, panda_product_id):

        user_profile = UserProfile.from_webapp_type({'webapp_type': 2})
        if not user_profile:
            return None
        owner_id = user_profile[0].user_id
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
            purchase_price=self.purchase_price,
            stocks=0,
            promotion_title=self.promotion_title if self.promotion_title else ''

        )
        mall_models.PandaHasProductRelation.create(
            panda_product_id=int(panda_product_id),
            weapp_product_id=product.id,
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
                                                 promotion_title=self.promotion_title,
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
    @param_required(['product_id', 'model_type'])
    def from_product_id(args):
        if args['model_type']:
            product_model = mall_models.ProductModel.select().dj_where(product_id=args['product_id'],
                                                                       name='standard',
                                                                       is_deleted=False).first()
            return ProductModel(product_model)

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
        accounts = [str(account) for account in args.get('accounts')]
        woids = list(set([str(account.woid) for account in product_pool]))
        # 需要某个商户更新成不可件的
        off_woids = list(set(woids) - set(accounts))
        # 需要添加的映射
        need_add = list(set(accounts) - set(woids))

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
