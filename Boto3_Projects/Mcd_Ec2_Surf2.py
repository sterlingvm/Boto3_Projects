import boto3
import pandas as pd

def get_ec2_instances(region):
    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.all()
    return instances

def create_instances_table(instances):
    instance_data = []
    for instance in instances:
        instance_data.append({
            'Instance ID': instance.id,
            'Instance Type': instance.instance_type
        })
    df = pd.DataFrame(instance_data)
    return df

def main():
    region = 'us-east-1'  # Update with your desired region
    instances = get_ec2_instances(region)
    table = create_instances_table(instances)
    print(table)

if __name__ == '__main__':
    main()
