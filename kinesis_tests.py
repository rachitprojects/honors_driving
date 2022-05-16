import boto3
import json
from sys import argv, getsizeof
import time

my_stream_name = "emotion-honors"
client = boto3.client("kinesis")
# response = client.describe_stream(StreamName=my_stream_name)
# response = client.get_records()
# print(json.dumps(str(shard_iterator[""]), indent=5))

# record_response = client.get_records(ShardIterator=shard_iterator,
#                                               Limit=2)
# payload = "['{"latitude": 12.9, "longitude": 77.4833, "emotion": "Neutral"}', '{"latitude": 13.0585, "longitude": 77.6407, "emotion": "Neutral"}', '{"latitude": 13.0006, "longitude": 77.6746, "emotion": "Neutral"}', '{"latitude": 12.9716, "longitude": 77.5946, "emotion": "Neutral"}', '{"latitude": 12.9317, "longitude": 77.6227, "emotion": "Neutral"}', '{"latitude": 12.9382, "longitude": 77.6228, "emotion": "Fear"}', '{"latitude": 12.9211, "longitude": 77.6134, "emotion": "Sad"}', '{"latitude": 12.9709, "longitude": 77.5658, "emotion": "Sad"}', '{"latitude": 12.9904, "longitude": 77.6842, "emotion": "Sad"}']"

print(getsizeof(argv[1]))
start = time.time()
put_response = client.put_record(
                    StreamName=my_stream_name,
                    Data=json.dumps(argv[1]),
                    PartitionKey="aa-bb")
end = time.time()
print(end - start)
print(put_response)


# my_shard_id = response['StreamDescription']['Shards'][2]['ShardId']
# my_shard_id = put_response["ShardId"]
# shard_iterator = client.get_shard_iterator(StreamName=my_stream_name,
#                                                       ShardId=my_shard_id,
#                                                       ShardIteratorType='LATEST')["ShardIterator"]
#
# record_response = client.get_records(ShardIterator=shard_iterator, Limit=2)
# while 'NextShardIterator' in record_response:
#     record_response = client.get_records(ShardIterator=record_response['NextShardIterator'],
#                                                   Limit=2)
#
#     print(record_response)
#
    # wait for 5 seconds
    # time.sleep(3)

# print(record_response)
