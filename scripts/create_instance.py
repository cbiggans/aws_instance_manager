import sys
# This is needed, reason:
# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
sys.path.append('.')
from manager import EC2Manager

m = EC2Manager()
instance = m.create()
print('InstanceId: %s' % instance[0].id)
