
import gmplot


with open("arduinoiot.txt") as test:
    iot = test.read()
    p = iot.split('""')
    p[0] = p[0][1:]
    p[-1] = p[-1][:-2]
    prev_light_current = 4000
    prev_ultra_dist = 1200
    low_illum = False
    overtaking = False
    gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946, 13)
    map_count = 0
    count = 0
    plot_count = 0
    for x in p:
        items = (x.split(";"))
        for entry in items:
            entry = entry.split(" ")
            if entry[0] == "Arduino":
                light_current = int(entry[1][:-2])
                ultra_dist = int(entry[2][:-2])
                if not low_illum:
                    if light_current - prev_light_current <= -1000:
                        print(prev_light_current)
                        print(light_current)
                        gmap3.marker(float(entry[3]), float(entry[4]), color="black")
                        print("plot light on map")
                        print(float(entry[3]), float(entry[4]))
                        low_illum = True
                        prev_light_current = light_current
                        plot_count += 1
                else:
                    if light_current - prev_light_current >= 1000:
                        print("plot light on map 2")
                        gmap3.marker(float(entry[3]), float(entry[4]), color="white")
                        print(float(entry[3]), float(entry[4]))
                        low_illum = False
                        prev_light_current = light_current
                        plot_count += 1
                prev_light_current = light_current

                if not overtaking:
                    if ultra_dist - prev_ultra_dist < -100:
                        print("plot overtake on map")
                        gmap3.marker(float(entry[3]), float(entry[4]), color="red")
                        overtaking = True
                        print(float(entry[3]), float(entry[4]))
                        prev_ultra_dist = ultra_dist
                        plot_count += 1
                else:
                    if ultra_dist - prev_ultra_dist > 100:
                        print("plot overtake on map 2")
                        gmap3.marker(float(entry[3]), float(entry[4]), color="green")
                        overtaking = False
                        print(float(entry[3]), float(entry[4]))
                        prev_ultra_dist = ultra_dist
                        plot_count += 1
                prev_ultra_dist = ultra_dist
                count += 1
        if count >= 100 and plot_count >= 3:
            map_count += 1
            print(map_count)
            map_name = "map_iot" + str(map_count) + ".html"
            gmap3.draw(map_name)
            gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946, 13)
            count = 0
            plot_count = 0
