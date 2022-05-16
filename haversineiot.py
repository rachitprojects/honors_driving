
import gmplot
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import random

iot_points = []
emotion_points = []
plotted = []

def haversine(lon1, lat1, lon2, lat2):
     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
     dlon = lon2 - lon1
     dlat = lat2 - lat1
     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
     c = 2 * asin(sqrt(a))
     r = 6371
     return c * r

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def check_iot(test):
    split_str = test.split(" ")
    # print(split_str)
    # print(split_str[1][-2:])
    if len(split_str) == 5:
        if split_str[0] == "Arduino" and split_str[1][-2:] == "mV" and split_str[2][-2:] == "cm" and isfloat(split_str[3]) and isfloat(split_str[4]):
            return True
        else:
            return False
    else:
        return False


with open("arduinoiot.txt") as test:
    # s3.download_fileobj('emotion-honors', message_body, test)
    x = test.read()
    p = x.split('""')
    p[0] = p[0][1:]
    p[-1] = p[-1][:-2]
    gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946, 13)
    plot_count = 0
    prev_light_current = 4000
    prev_ultra_dist = 1200
    low_illum = False
    overtaking = False
    count = 0

    for l in range(len(p)):
            data = (p[l].split(";"))
            # print(data)
            # if data[0].split(" ")[0] != "Arduino":
            #     print(data)
            for entry in data:
                # print(check_iot(entry))
                if check_iot(entry):
                    entry = entry.split(" ")
                    light_current = int(entry[1][:-2])
                    ultra_dist = int(entry[2][:-2])
                    if not low_illum:
                        if light_current - prev_light_current <= -1000:
                            gmap3.marker(float(entry[3]), float(entry[4]), color="black")
                            low_illum = True
                            prev_light_current = light_current
                            plot_count += 1
                            if (float(entry[3]), float(entry[4])) not in iot_points:
                                iot_points.append((float(entry[3]), float(entry[4])))
                    else:
                        if light_current - prev_light_current >= 1000:
                            gmap3.marker(float(entry[3]), float(entry[4]), color="black")
                            low_illum = False
                            prev_light_current = light_current
                            plot_count += 1
                            if (float(entry[3]), float(entry[4])) not in iot_points:
                                iot_points.append((float(entry[3]), float(entry[4])))
                    prev_light_current = light_current

                    if not overtaking:
                        if ultra_dist - prev_ultra_dist < -100:
                            gmap3.marker(float(entry[3]), float(entry[4]), color="white")
                            overtaking = True
                            prev_ultra_dist = ultra_dist
                            plot_count += 1
                            if (float(entry[3]), float(entry[4])) not in iot_points:
                                iot_points.append((float(entry[3]), float(entry[4])))
                    else:
                        if ultra_dist - prev_ultra_dist > 100:
                            gmap3.marker(float(entry[3]), float(entry[4]), color="white")
                            overtaking = False
                            prev_ultra_dist = ultra_dist
                            plot_count += 1
                            if (float(entry[3]), float(entry[4])) not in iot_points:
                                iot_points.append((float(entry[3]), float(entry[4])))
                    prev_ultra_dist = ultra_dist
                    count += 1
                    # print(entry)

                    # if count >= 100 and plot_count >= 3:
                    #     # print("here")
                    #     dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
                    #     # map_count += 1
                    #     map_count = 1
                    #     map_name = "map_iotlolo" + dt_string + str(map_count) + ".html"
                    #     gmap3.draw(map_name)
                    #     print(map_name)
                    #     # response = s3.Bucket("hons-test-buck-output").upload_file(map_name, map_name)
                    #     gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946, 13)
                    #     count = 0
                    #     plot_count = 0
                elif isfloat(entry.split(" ")[0]):
                    # print("Emotion")
                    map_data = entry.split(" ")
                    map_data[0], map_data[1] = float(map_data[0]), float(map_data[1])
                    emotion_points.append(map_data)
                    # mark(gmap3, map_data)

                    # eligible = False
                    # for iotpt in iot_points:
                    #     if haversine(iotpt[0], iotpt[1], map_data[0], map_data[1]) <= 0.8:
                    #         # print()
                    #         eligible = True
                    #         # print("hogaya")
                    # if eligible:
                    #     count += 1
                    #     # print(map_data[2])
                    #     if map_data[2] == "Happy":
                    #         gmap3.marker(map_data[0], map_data[1], color="pink")
                    #     elif map_data[2] == "Angry":
                    #         gmap3.marker(map_data[0], map_data[1], color="red")
                    #     elif map_data[2] == "Sad":
                    #         gmap3.marker(map_data[0], map_data[1], color="blue")
                    #     elif map_data[2] == "Neutral":
                    #         gmap3.marker(map_data[0], map_data[1], color="white")
                    #     elif map_data[2] == "Disgust":
                    #         gmap3.marker(map_data[0], map_data[1], color="green")
                    #     elif map_data[2] == "Fear":
                    #         gmap3.marker(map_data[0], map_data[1], color="yellow")
                    #     elif map_data[2] == "Surprise":
                    #         gmap3.marker(map_data[0], map_data[1], color="orange")

                # if count >= 100:
                #     print(count, plot_count)
                #     dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
                #     # map_count += 1
                #     map_count = 1
                #     map_name = "map_iotlolo" + dt_string + str(map_count) + ".html"
                #     gmap3.draw(map_name)
                #     print(map_name)
                #     # response = s3.Bucket("hons-test-buck-output").upload_file(map_name, map_name)
                #     gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946, 13)
                #     count = 0
                #     plot_count = 0

count = 0
for emo_point in emotion_points:
    eligible = False
    for iotpt in iot_points:
        if (emo_point[0], emo_point[1]) not in plotted:
            if haversine(iotpt[0], iotpt[1], emo_point[0], emo_point[1]) <= 0.8:
                plotted.append((emo_point[0], emo_point[1]))
                print(emo_point)
                if emo_point[2] == "Happy":
                    print("here")
                    gmap3.marker(emo_point[0], emo_point[1], color="pink")
                elif emo_point[2] == "Angry":
                    gmap3.marker(emo_point[0], emo_point[1], color="red")
                elif emo_point[2] == "Sad":
                    gmap3.marker(emo_point[0], emo_point[1], color="blue")
                elif emo_point[2] == "Neutral":
                    gmap3.marker(emo_point[0], emo_point[1], color="white")
                elif emo_point[2] == "Disgust":
                    gmap3.marker(emo_point[0], emo_point[1], color="green")
                elif emo_point[2] == "Fear":
                    gmap3.marker(emo_point[0], emo_point[1], color="yellow")
                elif emo_point[2] == "Surprise":
                    gmap3.marker(emo_point[0], emo_point[1], color="orange")
                plot_count += 1
        if plot_count >= 3:
            print(count, plot_count)
            dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
            # map_count += 1
            map_count = 1
            map_name = "map_iotlolo" + dt_string + str(map_count) + ".html"
            gmap3.draw(map_name)
            print(map_name)
            # response = s3.Bucket("hons-test-buck-output").upload_file(map_name, map_name)
            # gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946, 13)
            count = 0
            plot_count = 0
            break

            # print("hogaya")



print(iot_points)
print(plot_count)
