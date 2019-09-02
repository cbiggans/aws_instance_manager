import sys
# This is needed, reason:
# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
sys.path.append('.')
from manager import EC2Manager

m = EC2Manager()
ids = m.terminate(types=['running'])

if ids and len(ids) > 0:
  print("Terminated ID's: %s" % ids )
else:
  print("No Running Instances")
