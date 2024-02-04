import boto3
import pandas as pd

def get_ec2_instances(regions, keywords):
    instances = []
    
    for region in regions:
        # Create Boto3 EC2 client for the current region
        ec2 = boto3.client('ec2', region_name=region)
        
        # Retrieve all EC2 instances
        response = ec2.describe_instances()
        
        # Iterate through reservations and instances to find instances matching the keywords
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_name = ''
                
                # Get the instance name by looking for the 'Name' tag
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                        break
                
                # Check if the instance name contains any of the specified keywords
                for keyword in keywords:
                    if keyword.lower() in instance_name.lower():
                        instance_id = instance['InstanceId']
                        instance_type = instance['InstanceType']
                        instances.append({'Region': region, 'Instance ID': instance_id, 'Instance Type': instance_type})
                        break
    
    return instances

def display_instances_table(instances):
    # Create a pandas DataFrame from the list of instances
    df = pd.DataFrame(instances)
    
    # Display the DataFrame
    print(df)

# Replace ['us-west-2', 'eu-west-1'] with your desired regions
regions = ['us-east-1', 'us-east-2']

# Replace ['keyword1', 'keyword2'] with your desired keywords
keywords = ['cassandra', 'spark', 'opcenter']

# Get the EC2 instances matching the specified keywords in the given regions
instances = get_ec2_instances(regions, keywords)

# Display the instances in a pandas table
display_instances_table(instances)
