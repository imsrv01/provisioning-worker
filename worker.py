import boto3
import time
import json
import dynamodb


# Get the service resource
sqs = boto3.resource('sqs')
ec2 = boto3.resource('ec2')
#ec2.create_instances(ImageId='ami-09d95fab7fff3776c', MinCount=1, MaxCount=1, InstanceType='t2.micro')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='vra_createvm')

# Process messages by printing out body
while True:
    for message in queue.receive_messages():
        # Print out the body of the message
        print('Hello, {0}'.format(message.body))
        body = json.loads(message.body)
        print("imageid - ", body['imageid'])
        ec2.create_instances(
            ImageId=body['imageid'], 
            MinCount=1, 
            MaxCount=1, 
            InstanceType=body['instancetype'],
            TagSpecifications=[
                {   'ResourceType' : 'instance',
                    'Tags': [
                        {
                            'Key' : 'orderid',
                            'Value' : body['orderid']
                        }
                    ]
                }
            ]
         )

        # Let the queue know that the message is processed
        message.delete()
    print('waiting...')
    time.sleep(30)