# import boto3
#
# region = 'us-east-2'
# instances = ["i-0b6080090c7e3e984"]
# ec2 = boto3.client('ec2', region_name=region)
# ec2.start_instances(InstanceIds=instances)


import gmplot

gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946, 13)
gmap3.marker(12.8431, 77.4863, color="black")
gmap3.draw("map_fa.html")
