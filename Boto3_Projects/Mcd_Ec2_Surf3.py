import boto3
import pandas as pd

def get_ec2_instances(region, keyword):
    # Create Boto3 EC2 client
    ec2 = boto3.client('ec2', region_name=region)
    
    # Retrieve all EC2 instances
    response = ec2.describe_instances()
    
    instances = []
    
    # Iterate through reservations and instances to find instances containing the specified keyword
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_name = ''
            
            # Get the instance name by looking for the 'Name' tag
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
                    break
            
            # Check if the instance name contains the specified keyword
            if keyword.lower() in instance_name.lower():
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                instances.append({'Instance ID': instance_id, 'Instance Type': instance_type})
    
    return instances

def display_instances_table(instances):
    # Create a pandas DataFrame from the list of instances
    df = pd.DataFrame(instances)
    
    # Display the DataFrame
    print(df)

# Replace 'us-west-2' with your desired region
region = 'us-east-1'

# Replace 'keyword' with your desired keyword
keyword = 'Cassandra'

# Get the EC2 instances containing the specified keyword
instances = get_ec2_instances(region, keyword)

# Display the instances in a pandas table
display_instances_table(instances)
