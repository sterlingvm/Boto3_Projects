########################
### LIBRARY  IMPORTS ###

import boto3            # For AWS SDK interaction
import pandas as pd     # For Dataframes & Data ETL


########################
### DATA LOADING ###

# Load csv file
# Connect Input Sheet --- INSERT BUCKET OBJECT INFO FOR INPUT SHEET HERE ---
input_file_bucket = '[insert-bucket-name-here]'
input_file_bucket_object = '[insert-input-file.csv-here]'

tasks = boto3.client('ec2').get_object(
                                                    Bucket=input_file_bucket,
                                                    Key=input_file_bucket_object
                                                )
# Read csv file
tasks_df = pd.read_csv(tasks['Body'])                               # The csv file is read into the program
# Print & Confirm Loaded csv file
print('\n Read input file:')
print(tasks_df)                                             # The program will represent and verify that the csv file has been correctly read


########################
### PROCESSING LOGIC ###

# Generate IP & AWS Teams List
ip_addresses = tasks_df['IP']
aws_teams = tasks_df['AWS Account']
# Generate all Unique IP Adresses & Associated AWS Teams
ip = []
aws_account = []
x = 0
for i in ip_addresses:
    if i not in ip:
        ip.append(i)
        aws_account.append(aws_teams.iat[x])
        x += 1
        continue
    if i in ip:
        x += 1
        continue

# Connect Configuration Sheet --- INSERT BUCKET OBJECT INFO FOR CONFIGURATION SHEET HERE ---
config_file_bucket = '[insert-bucket-name-here]'
config_file_bucket_object = 'keyword-assignment-config.csv'

s3_config_file_object_path = boto3.client('s3').get_object(
                                                    Bucket=config_file_bucket,
                                                    Key=config_file_bucket_object
                                                )                    # insert path to s3 bucket configuration file object in this line


config_sheet = pd.read_csv(s3_config_file_object_path['Body'])
print('\nKeyword configuration:')
print(config_sheet)

key = config_sheet['Key']
value = config_sheet['KeyValue']
team_assignment = config_sheet['Team Assignment']

pairs = dict()
def make_dict(key,value):
    pairs[key] = [value]
    return pairs

delegate = dict()
def make_dict2(item,team):
    delegate[item] = [team]
    return delegate

x = 0
for i in config_sheet['Key']:
    key = config_sheet['Key'][x]
    value = config_sheet['KeyValue'][x]
    team = config_sheet['Team Assignment'][x]
    if key in pairs:
        pairs[key].append(value)
    else:      
        make_dict(key,value)
    for key in pairs:
        if key == 'Name':
            for w in pairs['Name']:
                if w == value:
                    make_dict2(value,team)
                else:
                    continue
        if key != 'Name':
                make_dict2(key,team)
        else:
            pass
    x += 1
#     print(pairs)
#     print(delegate)
# print(pairs)
# print(delegate)


# Connect to AWS EC2 Resources using IP Addresses
# Retrieve AWS Resource Tag information / JSON object
tag_data = []
print(f'\n--- Tag registration log: ---')
print(f'--- First Instance ---')
for item in ip:
    ec2 = boto3.client('ec2')
    filters = [{
        'Name': 'private-ip-address',
        'Values': [item],
    }]
    result_list = ec2.describe_instances(Filters=filters)
    
    y = 0
    for value in result_list['Reservations'][0]['Instances'][0]['Tags']:
        y += 1

    for j in range(y):
        if result_list['Reservations'][0]['Instances'][0]['Tags'][j]['Key'] != "Name":
            if result_list['Reservations'][0]['Instances'][0]['Tags'][j]['Key'].lower() in pairs:
                tag_value = result_list['Reservations'][0]['Instances'][0]['Tags'][j]['Key'].lower()
                print(tag_value)
                tag_data.append(tag_value)
                break
            else:
                continue
        if result_list['Reservations'][0]['Instances'][0]['Tags'][j]['Key'] == "Name":
            for w in pairs['Name']:
                if w in result_list['Reservations'][0]['Instances'][0]['Tags'][j]['Value'].lower():
                    tag_value = result_list['Reservations'][0]['Instances'][0]['Tags'][j]['Value'].lower()
                    print(tag_value)
                    tag_data.append(tag_value)
                    break
            else:
                tag_value = result_list['Reservations'][0]['Instances'][0]['Tags'][j]['Value'].lower()
                tag_data.append(tag_value)
    print("--- Next Instance ---")
print(f'\n Here is the tag data from the instances: \n {tag_data}')

# Team Delegation Logic based on AWS Resource Tag information & Log
team_delegation = []
print(f'\n Here are the tag identification factors: \n {pairs}')
print(f'\n Here are the team delegation factors: \n {delegate}')
for tag in tag_data:
    if tag in delegate:
        team_delegation.append(delegate[tag])
        continue
    if tag not in delegate:
        for key in delegate:
            if key in tag:
                team_delegation.append(delegate[key])
                break
            else:
                continue
        else:
            print("Tag with no assigned delegation: '" + tag + "'")
            team_delegation.append("Unknown")
# print(team_delegation)

# Input all mapped & Delegated Data into a new dataframe
final_data = {  'IP_Address': ip,
                'AWS_Account': aws_account,
                'Assigned_Department': team_delegation,
                'Associated Tag': tag_data
                }

final_df = pd.DataFrame(final_data)
print(f'--- Delegation Results: ---')
print(f'\n {final_df}')


########################
### DATA  OUTPUTTING ###

# Output the final dataframe as a CSV
file_name = input('\nWhat would you like to name this output file?: ')

final_df.to_csv(file_name + ".csv")
print("Delegation exported as '" + file_name + ".csv' within the current folder")


#### To send this output file to S3, kindly uncomment the below section
# Upload file to S3
# boto3.client('s3').upload_file(Bucket=input_file_bucket, Key=f'{file_name}.csv', Filename=f'{file_name}.csv')

# Print confirmation of successful S3 object upload
# print("\nDelegation exported as '" + file_name + ".csv' within s3 bucket")