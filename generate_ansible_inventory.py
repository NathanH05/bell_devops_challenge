import boto3
import json

# AWS setup (you can also set these up in your environment)
aws_region = 'eu-west-1'
aws_profile = 'bell-test'

# Initialize a session using your AWS credentials
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)

# Create EC2 resource client
ec2_client = session.client('ec2')

def get_ec2_instances():
    """Fetch all EC2 instances and return a list of their IP addresses."""
    instances = []
    response = ec2_client.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Collect instance details: instance ID, public IP
            instance_id = instance['InstanceId']
            public_ip = instance.get('PublicIpAddress')
            private_ip = instance['PrivateIpAddress']
            state = instance['State']['Name']
            if public_ip and state == 'running':
                instances.append({
                    'instance_id': instance_id,
                    'public_ip': public_ip,
                    'private_ip': private_ip,
                })
    return instances

def generate_inventory(instances):
    """Generate the Ansible inventory in INI format."""
    inventory = {}

    for instance in instances:
        # Assign instances to groups based on tags or other criteria
        group = 'ec2_instances'

        # Add instance IPs to inventory groups
        if group not in inventory:
            inventory[group] = []
        inventory[group].append(instance['public_ip'])

    # Convert inventory to Ansible-compatible format (INI)
    inventory_str = ""
    for group, ips in inventory.items():
        inventory_str
