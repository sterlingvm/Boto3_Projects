########################
### LIBRARY  IMPORTS ###

import boto3            # For AWS SDK interaction
import pandas as pd     # For Dataframes & Data ETL

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

filters = [{
    'Name': 'tag:Name',
    'Values': ['instance_one', 'instance_two']
}]
reservations = client.describe_instances(Filters=filters)

print(reservations)
