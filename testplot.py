import gmplot

gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946, 13)
gmap3.marker(12.9716, 77.5946, color="red")
gmap3.draw("map.html")

