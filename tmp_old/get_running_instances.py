import boto3
ec2 = boto3.resource('ec2')

def get_running_instance_ids():
  result = []
  for i in ec2.instances.all():
    if i.state['Name'] == 'running':
      result.append(i.id)

  return result
