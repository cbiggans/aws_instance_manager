import boto3
import os

UBUNTU_AMI = 'ami-07d0cf3af28718ef8'

"""
# Commands found from: https://blog.ipswitch.com/how-to-create-an-ec2-instance-with-python
# * Great guide for getting started

# Configure the AWS secret & region settings
aws configure

# Get all variables associated with all instances
aws ec2 describe-instances

# SSH into instance
ssh -i /etc/aws/ec2-keypair.pem ubuntu@ec2-54-210-156-211.compute-1.amazonaws.com

# If get an error with sshing into the new instance, look at these articles
# * https://stackoverflow.com/questions/21981796/cannot-ping-aws-ec2-instance
# ** Had timeout issues because my requests weren't going all the way through,
#     tried pinging and that didn't even work
# *
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html#TroubleshootingInstancesConnectingSSH
# ** Overall Troubleshooting guide
# ** Also provides usernames to use for the different instances
# * https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html
"""


class EC2Manager(object):
  def __init__(self):
    self.ec2 = boto3.resource('ec2')

  def index(self):
    """
    List all ec2 instances on account
    """
    result = {'running': [], 'pending': [], 'terminated': [], 'other': []}
    for i in self.ec2.instances.all():
      if i.state['Name'] == 'running':
        result['running'].append(i)
      if i.state['Name'] == 'pending':
        result['pending'].append(i)
      elif i.state['Name'] == 'terminated':
        result['terminated'].append(i)
      else:
        result['other'].append(i)

    return result

  def create(self):
    """
    Create an ec2 instance
    """
    instances = self.ec2.create_instances(
      ImageId=UBUNTU_AMI,
      MinCount=1,
      MaxCount=1,
      InstanceType='t2.micro',
      KeyName='ec2-keypair2'
    )

    return instances

  def destroy(self, ids=[], types=[]):
    """This is just an alias for terminate to follow the CRUD pattern"""
    return self.terminate(ids=ids, types=types)

  def terminate(self, ids=[], types=[]):
    """
    Can terminate based off of types
    * types: 'running', 'stopped'
    * https://www.edureka.co/community/32011/how-to-delete-an-ec2-instance-using-python-boto3
    """
    if types and 'running' in types:
      ids = [i.id for i in self.index()['running']]

    if len(ids) > 0:
      self.ec2.instances.filter(InstanceIds = ids).terminate()

    return ids

  def create_key_pair(self):
    # create a file to store the key locally
    path = 'ec2-keypair2.pem'
    outfile = open(path,'w')

    # call the boto ec2 function to create a key pair
    key_pair = self.ec2.create_key_pair(KeyName='ec2-keypair2')

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    outfile.write(KeyPairOut)

    # Set file to read only
    # https://stackoverflow.com/questions/16249440/changing-file-permission-in-python
    os.chmod(path, 0o400)
