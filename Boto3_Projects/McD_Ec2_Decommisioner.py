import boto3
import csv

def decommission_ec2_instances(csv_file):
    # Read the CSV file
    instances = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            instances.append({'Region': row['Region'], 'Instance ID': row['Instance ID'], 'Instance Type': row['Instance Type']})
    
    if not instances:
        print("No instances found in the CSV file.")
        return
    
    # Iterate through the instances and terminate them
    for instance in instances:
        region = instance['Region']
        instance_id = instance['Instance ID']
        try:
            ec2 = boto3.client('ec2', region_name=region)
            ec2.terminate_instances(InstanceIds=[instance_id])
            print(f"Terminated EC2 instance: {instance_id} in {region}")
        except Exception as e:
            print(f"Error terminating EC2 instance {instance_id} in {region}: {str(e)}")

# Replace 'instances.csv' with the path to your CSV file
csv_file = 'instances_example.csv'

# Decommission EC2 instances based on the CSV file
decommission_ec2_instances(csv_file)