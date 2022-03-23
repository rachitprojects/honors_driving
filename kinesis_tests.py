import boto3
import json

my_stream_name = "emotion-driving"
client = boto3.client("kinesis")
response = client.describe_stream(StreamName=my_stream_name)
# response = client.get_records()
# print(json.dumps(str(shard_iterator[""]), indent=5))

# record_response = client.get_records(ShardIterator=shard_iterator,
#                                               Limit=2)
payload = {
                'timestamp': "Monday 10:19pm 2022",
                'thing_id': "macintosh"
          }


put_response = client.put_record(
                    StreamName=my_stream_name,
                    Data=json.dumps(payload),
                    PartitionKey="aa-bb")

print(put_response)


# my_shard_id = response['StreamDescription']['Shards'][2]['ShardId']
my_shard_id = put_response["ShardId"]
shard_iterator = client.get_shard_iterator(StreamName=my_stream_name,
                                                      ShardId=my_shard_id,
                                                      ShardIteratorType='LATEST')["ShardIterator"]

record_response = client.get_records(ShardIterator=shard_iterator, Limit=2)
while 'NextShardIterator' in record_response:
    record_response = client.get_records(ShardIterator=record_response['NextShardIterator'],
                                                  Limit=2)

    print(record_response)
#
    # wait for 5 seconds
    # time.sleep(3)

# print(record_response)
