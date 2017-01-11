# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource

from business import model as business_model
from db.account import models as account_models

class UserProfile(business_model.Model):
	"""
	用户详情
	"""
	__slots__ = (
		'id',
		'user_id',
		'webapp_id',
		'webapp_type',
		'app_display_name',
		'is_active',
		'note',
		'status',
		'is_mp_registered',
		'mp_token',
		'mp_url',
		'new_message_count',
		'webapp_template',
		'is_customed',
		'is_under_previewed',
		'expire_date_day',
		'force_logout_date',
		'host_name',
		'logout_redirect_to',
		'system_name',
		'system_version',
		'homepage_template_name',
		'backend_template_name',
		'homepage_workspace_id',
		'account_type',
		'is_oauth',
		'sub_account_count',
		'is_use_wepage',
		'store_name'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['webapp_ids'])
	def from_webapp_ids(args):
		user_profiles = []
		user_profiles_models = account_models.UserProfile.select().dj_where(webapp_id__in=args['webapp_ids'])

		for profile_model in user_profiles_models:
			user_profile = UserProfile(profile_model)
			user_profiles.append(user_profile)
		return user_profiles

	@staticmethod
	@param_required(['mall_type'])
	def from_mall_type(args):
		user_profiles = []
		user_profiles_models = account_models.UserProfile.select().dj_where(webapp_type=args['mall_type'])

		for profile_model in user_profiles_models:
			user_profile = UserProfile(profile_model)
			user_profiles.append(user_profile)
		return user_profiles

	@staticmethod
	@param_required(['webapp_id'])
	def from_webapp_id(args):
		profile_model= account_models.UserProfile.get(webapp_id=args['webapp_id'])
		user_profile = UserProfile(profile_model)
		return user_profile

	@staticmethod
	@param_required(['user_id'])
	def from_user_id(args):
		profile_model= account_models.UserProfile.get(user=args['user_id'])
		user_profile = UserProfile(profile_model)
		return user_profile

	@property
	def username(self):
		return self.context['db_model'].user.username

	@staticmethod
	@param_required(['user_ids'])
	def get_user_id_2_store_name(args):
		profile_models = account_models.UserProfile.select().dj_where(user_id__in=args['user_ids'])
		user_id2store_name = {}
		for model in profile_models:
			user_id2store_name[model.user_id] = model.store_name
		return user_id2store_name

	@staticmethod
	@param_required(['webapp_ids'])
	def get_webapp_id_2_store_name(args):
		profile_models = account_models.UserProfile.select().dj_where(webapp_id__in=args['webapp_ids'])
		user_id2store_name = []
		for model in profile_models:
			user_id2store_name.append({
					'webapp_id': model.webapp_id,
					'store_name': model.store_name
				})
		return user_id2store_name

	@staticmethod
	@param_required(['page', 'page_count'])
	def from_page(args):
		"""
		分页获取商户列表
		"""
		page = args['page']
		page_count = args['page_count']
		users = account_models.UserProfile.select().dj_where(is_active=True)
		counts = users.count()
		page_users = users.paginate(int(page), int(page_count))
		result = [UserProfile(user) for user in page_users]
		return {
			'users': result,
			'counts': counts
		}

	@staticmethod
	@param_required(['webapp_type'])
	def from_webapp_type(args):
		user_profiles = []
		user_profiles_models = account_models.UserProfile.select().dj_where(webapp_type=args['webapp_type'])

		for profile_model in user_profiles_models:
			user_profile = UserProfile(profile_model)
			user_profiles.append(user_profile)
		return user_profiles
