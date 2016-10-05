Feature: 更新图片分组

Background:
	Given jobs登录系统

@mall @mall.product @mall.image_group @hermes @wip
Scenario:1 删除图片分组
	Jobs添加图片分组后
	1. jobs能删除图片分组

	When jobs添加图片分组
		"""
		[{
			"name": "图片分组1",
			"images": [{
				"path": "/static/test_resource_img/hangzhou1.jpg"
			}, {
				"path": "/static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
			"name": "图片分组2",
			"images": [{
				"path": "/static/test_resource_img/hangzhou3.jpg"
			}]
		}]
		"""
	Then jobs能获取图片分组列表
		"""
		[{
			"name": "图片分组1",
			"images": [{
				"path": "/static/test_resource_img/hangzhou1.jpg"
			}, {
				"path": "/static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
			"name": "图片分组2",
			"images": [{
				"path": "/static/test_resource_img/hangzhou3.jpg"
			}]
		}]
		"""
	When jobs删除图片分组'图片分组1'
	Then jobs能获取图片分组列表
		"""
		[{
			"name": "图片分组2",
			"images": [{
				"path": "/static/test_resource_img/hangzhou3.jpg"
			}]
		}]
		"""