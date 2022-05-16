
import gmplot
import boto3
import json
from datetime import datetime

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

        if message_body:
            s3.Bucket("emotion-honors").download_file(message_body, 'data.txt')
            with open("data.txt") as test:
                # s3.download_fileobj('emotion-honors', message_body, test)
                x = test.read()
                p = x.split('""')
                p[0] = p[0][1:]
                p[-1] = p[-1][:-2]
                emo_gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946, 13)
                emo_count = 0
                emo_map_count = 0

                gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946, 13)
                count = 0
                map_count = 0
                plot_count = 0
                prev_light_current = 4000
                prev_ultra_dist = 1200
                low_illum = False
                overtaking = False

                for l in range(len(p)):
                        data = (p[l].split(";"))
                        if data[0].split(" ")[0] == "Arduino":
                            try:
                                for entry in data:
                                    entry = entry.split(" ")
                                    light_current = int(entry[1][:-2])
                                    ultra_dist = int(entry[2][:-2])
                                    if not low_illum:
                                        if light_current - prev_light_current <= -1000:
                                            gmap3.marker(float(entry[3]), float(entry[4]), color="black")
                                            low_illum = True
                                            prev_light_current = light_current
                                            plot_count += 1
                                    else:
                                        if light_current - prev_light_current >= 1000:
                                            gmap3.marker(float(entry[3]), float(entry[4]), color="white")
                                            low_illum = False
                                            prev_light_current = light_current
                                            plot_count += 1
                                    prev_light_current = light_current

                                    if not overtaking:
                                        if ultra_dist - prev_ultra_dist < -100:
                                            gmap3.marker(float(entry[3]), float(entry[4]), color="red")
                                            overtaking = True
                                            prev_ultra_dist = ultra_dist
                                            plot_count += 1
                                    else:
                                        if ultra_dist - prev_ultra_dist > 100:
                                            gmap3.marker(float(entry[3]), float(entry[4]), color="green")
                                            overtaking = False
                                            prev_ultra_dist = ultra_dist
                                            plot_count += 1
                                    prev_ultra_dist = ultra_dist
                                    count += 1

                                    if count >= 100 and plot_count >= 3:
                                        dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
                                        map_count += 1
                                        map_name = "map_iot" + dt_string + str(map_count) + ".html"
                                        gmap3.draw(map_name)
                                        print(map_name)
                                        response = s3.Bucket("hons-test-buck-output").upload_file(map_name, map_name)
                                        gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946, 13)
                                        count = 0
                                        plot_count = 0
                            except:
                                continue
                        else:
                            try:
                                for x in data:
                                    map_data = x.split(" ")
                                    map_data[0], map_data[1] = float(map_data[0]), float(map_data[1])
                                    # mark(gmap3, map_data)
                                    if map_data[2] == "Happy":
                                        emo_gmap3.marker(map_data[0], map_data[1], color="pink")
                                    elif map_data[2] == "Angry":
                                        emo_gmap3.marker(map_data[0],map_data[1], color="red")
                                    elif map_data[2] == "Sad":
                                        emo_gmap3.marker(map_data[0],map_data[1], color="blue")
                                    elif map_data[2] == "Neutral":
                                        emo_gmap3.marker(map_data[0],map_data[1], color="white")
                                    elif map_data[2] == "Disgust":
                                        emo_gmap3.marker(map_data[0],map_data[1], color="green")
                                    elif map_data[2] == "Fear":
                                        emo_gmap3.marker(map_data[0],map_data[1], color="yellow")
                                    elif map_data[2] == "Surprise":
                                        emo_gmap3.marker(map_data[0],map_data[1], color="orange")
                                    emo_count += 1
                                    if emo_count == 100:
                                        dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
                                        emo_map_count += 1
                                        map_name = "map" + dt_string + str(emo_map_count) + ".html"
                                        emo_gmap3.draw(map_name)
                                        print(map_name)
                                        response = s3.Bucket("hons-test-buck-output").upload_file(map_name, map_name)
                                        emo_gmap3 = gmplot.GoogleMapPlotter(map_data[0], map_data[1], 13)
                                        emo_count = 0
                            except:
                                continue
