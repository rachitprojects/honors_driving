
import gmplot
import boto3
import json

sqs_client = boto3.client("sqs", region_name="us-east-2")
s3 = boto3.resource('s3')

while True:
    response = sqs_client.receive_message(
        QueueUrl="https://sqs.us-east-2.amazonaws.com/743056030620/kinesisupload.fifo",
        MaxNumberOfMessages=1,
        WaitTimeSeconds=3,
    )
    print(f"Number of messages received: {len(response.get('Messages', []))}")

    message_body = ""
    for message in response.get("Messages", []):
        message_body = message["Body"]
        print(message_body)

        response = sqs_client.delete_message(
        QueueUrl='https://sqs.us-east-2.amazonaws.com/743056030620/kinesisupload.fifo',
        ReceiptHandle=message['ReceiptHandle']
        )
        # print(f"Message body: {json.loads(message_body)}")
        # print(f"Receipt Handle: {message['ReceiptHandle']}")

        if message_body:
            s3.Bucket("emotion-honors").download_file(message_body, 'emo.txt')
            with open("emo.txt") as test:
                # s3.download_fileobj('emotion-honors', message_body, test)
                x = test.read()
                p = x.split('""')
                p[0] = p[0][1:]
                p[-1] = p[-1][:-2]
                print()
                temp = p[0].split(";")[0].split(" ")
                gmap3 = gmplot.GoogleMapPlotter(float(temp[0]), float(temp[1]), 13)
                count = 0
                map_count = 0
                for l in range(len(p)):
                    entry = (p[l].split(";"))
                    for x in entry:
                        map_data = x.split(" ")
                        map_data[0], map_data[1] = float(map_data[0]), float(map_data[1])
                        # mark(gmap3, map_data)
                        if map_data[2] == "Happy":
                            gmap3.marker(map_data[0], map_data[1], color="pink")
                        elif map_data[2] == "Angry":
                            gmap3.marker(map_data[0],map_data[1], color="red")
                        elif map_data[2] == "Sad":
                            gmap3.marker(map_data[0],map_data[1], color="blue")
                        elif map_data[2] == "Neutral":
                            gmap3.marker(map_data[0],map_data[1], color="white")
                        elif map_data[2] == "Disgust":
                            gmap3.marker(map_data[0],map_data[1], color="green")
                        elif map_data[2] == "Fear":
                            gmap3.marker(map_data[0],map_data[1], color="yellow")
                        elif map_data[2] == "Surprise":
                            gmap3.marker(map_data[0],map_data[1], color="orange")
                        count += 1
                        if count == 100:
                            map_count += 1
                            map_name = "map" + str(map_count) + ".html"
                            gmap3.draw(map_name)
                            response = s3.Bucket("hons-test-buck-output").upload_file(map_name, map_name)
                            gmap3 = gmplot.GoogleMapPlotter(map_data[0], map_data[1], 13)
                            count = 0


# from ast import literal_eval

# def mark(gmap3, map_data):
#     if map_data[2] == "Happy":
#         gmap3.marker(map_data[0], map_data[1], color="pink")
#     elif map_data[2] == "Angry":
#         gmap3.marker(map_data[0],map_data[1], color="red")
#     elif map_data[2] == "Sad":
#         gmap3.marker(map_data[0],map_data[1], color="blue")
#     elif map_data[2] == "Neutral":
#         gmap3.marker(map_data[0],map_data[1], color="white")
#     elif map_data[2] == "Disgust":
#         gmap3.marker(map_data[0],map_data[1], color="green")
#     elif map_data[2] == "Fear":
#         gmap3.marker(map_data[0],map_data[1], color="yellow")
#     elif map_data[2] == "Surprise":
#         gmap3.marker(map_data[0],map_data[1], color="orange")
