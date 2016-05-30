#!/usr/bin/env python

import sys
from eaglet.command import manage as command_manager

print sys.path

if __name__ == '__main__':
    command = sys.argv[1]
    command_manager.run_command(command)

# if __name__ == "__main__":
#     command = sys.argv[1]
#     target_py = '%s.py' % command
#     commands_dir = './commands'
#     found_command = False
#     import os
#     for f in os.listdir(commands_dir):
#         if os.path.isfile(os.path.join(commands_dir, f)):
#             if f == target_py:
#                 found_command = True
#                 module_name = 'commands.%s' % command
#                 module = __import__(module_name, {}, {}, ['*',])
#                 instance = getattr(module, 'Command')()
#                 try:
#                     instance.handle(*sys.argv[2:])
#                 except TypeError, e:
#                     print '[ERROR]: wrong command arguments, usages:'
#                     print instance.help

#     if not found_command:
#         print 'no command named: ', command
