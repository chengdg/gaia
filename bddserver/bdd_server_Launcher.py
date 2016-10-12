#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bdd_server启动脚本
1. rebuild
2. start service
3. start_bdd_server
"""
import os
import platform

if platform.system() == 'Windows':
	is_windows = True
	CD_COMMAND = 'cd /d'
	EXT = 'bat'
else:
	is_windows = False
	CD_COMMAND = 'cd'
	EXT = 'sh'

ignored_dir = {'manage-system-base', 'python-service-base', 'h5'}
print('ignored_dir:{}'.format(list(ignored_dir)))

a = os.listdir(os.curdir)

print("**********bdd_server_Launcher:begin***********")

all_dirs = filter(lambda x: os.path.isdir(x), os.listdir(os.curdir))

print('ALL dir:{}'.format(all_dirs))

for dir in all_dirs:
	if os.path.isdir(dir) and dir not in ignored_dir:
		# rebuild

		if dir in ('weapp', 'Weapp'):
			dir = os.path.join(dir, 'weapp')

		if os.path.exists(os.path.join(dir, 'rebuild.bat')) or os.path.exists(os.path.join(dir, 'rebuild.sh')):
			print('rebuild:{}'.format(dir))
			os.system('{} {} && start rebuild'.format(CD_COMMAND, dir))

		# start service

		if os.path.exists(os.path.join(dir, 'start_service.bat')) or os.path.exists(
				os.path.join(dir, 'start_service.sh')):
			print('start_service:{}'.format(dir))
			os.system('{} {} && start start_service'.format(CD_COMMAND, os.path.abspath(dir)))

		# start_bdd_server
		bdd_server_path = os.path.abspath(os.path.join(os.curdir, dir, 'start_bdd_server.bat'))
		if os.path.exists(bdd_server_path) and dir not in ('manage-system-base', 'python-service-base'):
			print('start bdd server:{}'.format(dir))
			os.system('{} {} && start start_bdd_server'.format(CD_COMMAND, os.path.abspath(dir)))

print("**********bdd_server_Launcher:end***********")
