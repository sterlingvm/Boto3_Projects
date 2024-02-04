########################
### LIBRARY  IMPORTS ###

import boto3            # For AWS SDK interaction
import pandas as pd     # For Dataframes & Data ETL


########################
### DATA LOADING ###

# Load csv file
# tasks = "../Directory/Directory/target_file.csv"         # Insert filepath to csv here
tasks = input("What csv file would you like to read?: ") + ".csv"
# Read csv file
tasks_df = pd.read_csv(tasks)                               # The csv file is read into the program
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

# Connect Configuration Sheet
config_sheet = pd.read_csv("keyword-assignment-config.csv")
print('\n Keyword config file:')
print(config_sheet)

keywords = config_sheet['Keyword']
team_assignment = config_sheet['Team Assignment']

pairs = dict()
def make_dict(key, value):
    pairs[key] = value
    return pairs

x = 0
for i in config_sheet['Keyword']:
    key = config_sheet['Keyword'][x]
    value = config_sheet['Team Assignment'][x]
    make_dict(key,value)
    x += 1
print(pairs)

# Connect to AWS EC2 Resources using IP Addresses
# Retrieve AWS Resource Tag information / JSON object
tag_data = []
for item in ip:
    ec2 = boto3.client('ec2')
    filters = [{
        'Name': 'private-ip-address',
        'Values': [item],
    }]
    result_list = ec2.describe_instances(Filters=filters)
    print(result_list['Reservations'][0]['Instances'][0]['Tags'][0])
    if result_list['Reservations'][0]['Instances'][0]['Tags'][0]['Key'].lower() == key in pairs:
        tag_value = result_list['Reservations'][0]['Instances'][0]['Tags'][0]['Key']
    else:
        tag_value = result_list['Reservations'][0]['Instances'][0]['Tags'][0]['Value']
    tag_value = tag_value.lower()
    tag_data.append(tag_value)

# Team Delegation Logic based on AWS Resource Tag information & Log
team_delegation = []
for tag in tag_data:
    for key in pairs:
        if key in tag:
            team_delegation.append(pairs[key])
            break
        else:
            pass
    else:
        print("Tag with no assigned delegation: '" + tag + "'")
        team_delegation.append("Unknown")

# Input all mapped & Delegated Data into a new dataframe
final_data = {  'IP_Address': ip,
                'AWS_Account': aws_account,
                'Assigned_Department': team_delegation,
                'Associated Tag': tag_data
                }

final_df = pd.DataFrame(final_data)
print(final_df)


########################
### DATA  OUTPUTTING ###

# Output the final dataframe as a CSV
file_name = input("What would you like to name this file?: ")

final_df.to_csv(file_name + ".csv")
print("Delegation exported as '" + file_name + ".csv' within the current folder")