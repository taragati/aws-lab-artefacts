import boto3


# Initialize the EC2 client
ec2 = boto3.client('ec2')


def lambda_handler(event, context):
   print("Received event:", event)
  
   # 1. CHECK IF TRIGGERED BY EC2 STATE CHANGE (Manual Stop Protection)
   if event.get("source") == "aws.ec2" and event.get("detail-type") == "EC2 Instance State-change Notification":
       instance_id = event.get("detail", {}).get("instance-id")
       state = event.get("detail", {}).get("state")
      
       if state == "stopped":
           print(f"Alert: Instance {instance_id} was stopped manually. Overriding and restarting...")
           ec2.start_instances(InstanceIds=[instance_id])
           return f"Override triggered: Started instance {instance_id}"
       else:
           return "No action required for this state change."


   # 2. FALLBACK TO SCHEDULED TOGGLE (15-Minute Rule)
   instance_id = event.get('instance_id')
  
   if not instance_id:
       print("Error: No 'instance_id' found in the event payload.")
       return "Error: Missing instance_id"


   # Describe the instance
   response = ec2.describe_instances(InstanceIds=[instance_id])
  
   # FIX: Safely check if the lists contain elements before accessing index 0
   if not response['Reservations'] or not response['Reservations'][0]['Instances']:
       error_msg = f"Error: Instance ID '{instance_id}' was not found. Please double-check your Instance ID and ensure your Lambda function is deployed in the same AWS Region as your EC2 instance."
       print(error_msg)
       return error_msg
      
   instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
   print(f"Scheduled Event: Instance {instance_id} current state is '{instance_state}'")
  
   if instance_state == 'stopped':
       print(f"Starting instance: {instance_id}")
       ec2.start_instances(InstanceIds=[instance_id])
       return f"Successfully sent start command to {instance_id}"
      
   elif instance_state == 'running':
       print(f"Stopping instance: {instance_id}")
       ec2.stop_instances(InstanceIds=[instance_id])
       return f"Successfully sent stop command to {instance_id}"
      
   else:
       print(f"Instance {instance_id} is in '{instance_state}' state. Toggling skipped.")
       return f"Instance is currently {instance_state}. Toggling skipped."
