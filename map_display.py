

from flask import *
import boto3
import os

markers = []

app = Flask(__name__, template_folder="." )
s3 = boto3.resource('s3')
buck = s3.Bucket("hons-test-buck-output")
s3_item = []

def check_s3():
    global s3_item
    s3_item = [x.key[:-5] for x in buck.objects.all()]

@app.route('/map<id>', methods=["GET"])
def render_maps(id):
    print(id)
    maps_down = os.listdir("maps")
    name = "map" + id + ".html"
    if name not in maps_down:
        buck.download_file(name, "maps/" + name)
    return render_template("maps/" + name)

@app.route('/')
def map_links():
    check_s3()
    return render_template("index.html", maps=s3_item)

if __name__ == '__main__':
    app.run()
