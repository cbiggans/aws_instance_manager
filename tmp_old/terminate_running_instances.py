import boto3
from get_running_instances import get_running_instance_ids
# https://www.edureka.co/community/32011/how-to-delete-an-ec2-instance-using-python-boto3

ids = get_running_instance_ids()

ec2 = boto3.resource('ec2')
ec2.instances.filter(InstanceIds = ids).terminate()
