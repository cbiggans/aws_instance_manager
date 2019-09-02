import sys
# This is needed, reason:
# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
sys.path.append('.')
from manager import EC2Manager

m = EC2Manager()
instances = m.index()
found = False
for instance in instances['running']:
  found = True
  print('------------------------------------------------------')
  print('ID: %s' % instance.id)
  print('Public IP Address: %s' % instance.public_ip_address)
  print('Public DNS: %s' % instance.public_dns_name)
  example_ssh_call = 'ssh -i /etc/aws/%s.pem ubuntu@%s' % (
    instance.key_name, instance.public_dns_name)
  print('Example SSH Call: %s' % example_ssh_call)
  print('------------------------------------------------------')

if found is False:
  print('No Running Instances Found')
