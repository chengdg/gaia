# -*- coding: utf-8 -*-

from business import model as business_model
from business.member.member import Member
from db.member import models as member_models
from eaglet.core import paginator


class MemberRepository(business_model.Service):
	def __split_filters(self, filters):
		"""
		分离会员搜索的条件，分为：
		1、会员搜索条件
		2、会员信息搜索条件
		3、会员分组搜索条件
		"""
		member_filter_values = {}
		member_info_filter_values = {}
		member_group_filter_values = {}

		filter_parse_result = FilterParser.get().parse(filters)
		should_add_default_status = True #是否添加默认的会员status条件
		for filter_field_op, filter_value in filter_parse_result.items():
			#获得过滤的field
			items = filter_field_op.split('__')
			filter_field = items[0]
			op = None
			if len(items) > 1:
				op = items[1]

			#按表将filter分散到不同的list中
			filter_category = None
			should_ignore_field = False #是否略过该field不处理
			if filter_field == 'name' or filter_field == 'grade_id' or filter_field == 'created_at':
				filter_category = member_filter_values
			elif filter_field == 'status':
				should_add_default_status = False
				filter_category = member_filter_values
			elif filter_field == 'group':
				filter_category = member_group_filter_values

			if not should_ignore_field:
				if op:
					filter_field_op = '%s__%s' % (filter_field, op)
				filter_category[filter_field_op] = filter_value

		#补充条件
		member_filter_values['webapp_id'] = CorporationFactory.get().webapp_id
		if should_add_default_status:
			member_filter_values['status'] = member_models.SUBSCRIBED

		return {
			'member': member_filter_values,
			'member_info': member_info_filter_values,
			'member_group': member_group_filter_values
		}

	def __get_member_order_fields(self, options):
		"""
		获得商品排序field集合
		"""
		options = {} if not options else options
		type2field = {
			'id': member_models.Member.id
		}

		fields = []
		for order_type in options.get('order_options', ['-id']): #默认以id的倒序排序
			is_desc = False
			if order_type[0] == '-':
				is_desc = True
				order_type = order_type[1:]

			field = type2field[order_type]
			if is_desc:
				field = field.desc()

			fields.append(field)

		return fields

	def get_members(self, page_info, fill_options=None, options=None, filters=None):
		"""
		根据条件在商品池搜索商品
		@return:
		"""
		type2filters = self.__split_filters(filters)

		#构建排序策略
		order_fields = self.__get_member_order_fields(options)

		#member_member表中进行过滤
		member_filters = type2filters['member']
		#进行查询
		if member_filters:
			# 补充首次上架时间搜索值null判断
			member_db_models = member_models.Member.select().dj_where(**member_filters)
		else:
			member_db_models = member_models.Member.select().dj_where(status=member_models.SUBSCRIBED)
		if len(order_fields) > 0:
			# 考虑可以使用内存排序,而不是mysql自己排序
			member_db_models = member_db_models.order_by(*order_fields)

		#获取查询结果	
		pageinfo, member_db_models = paginator.paginate(member_db_models, page_info.cur_page, page_info.count_per_page)
		members = [Member(member_db_model) for member_db_model in member_db_models]

		# products = [Product(model) for model in product_models]
		# fill_product_detail_service = FillProductDetailService.get(self.corp)
		# fill_product_detail_service.fill_detail(products, fill_options)

		return members, pageinfo

	def get_member_by_id(self, member_id):
		"""
		根据id获得member对象
		"""
		member_db_model = member_models.Member.get(webapp_id=self.corp.webapp_id, id=member_id)

		return Member(member_db_model)

	def get_member_by_name(self, member_name):
		"""
		根据name获得member对象
		"""
		from eaglet.utils.string_util import hex_to_byte, byte_to_hex
		username_hexstr = byte_to_hex(member_name)

		member_db_models = list(member_models.Member.select().dj_where(webapp_id=self.corp.webapp_id, username_hexstr=username_hexstr))

		if len(member_db_models) > 0:
			member_db_model = member_db_models[0]
			return Member(member_db_model)
		else:
			return None

	def get_member_by_token(self, member_id):
		"""
		根据token获得member对象
		"""
		member_db_model = member_models.Member.get(webapp_id=self.corp.webapp_id, token=token)

		return Member(member_db_model)

	def get_members_from_webapp_user_ids(self, webapp_user_ids):
		"""
		根据webapp_user_ids获得member集合
		"""
		webappuser_id2member = dict(
			[(u.id, u.member_id) for u in member_models.WebAppUser.select().dj_where(id__in=webapp_user_ids)])
		member_ids = webappuser_id2member.values()
		db_member_models = member_models.Member.select().dj_where(id__in=member_ids)

		members = [Member(db_member_model) for db_member_model in db_member_models]
		id2member = dict([(m.id, m) for m in members])

		for webapp_user_id, member_id in webappuser_id2member.items():
			webappuser_id2member[webapp_user_id] = id2member.get(member_id, None)

		return webappuser_id2member, members

	
