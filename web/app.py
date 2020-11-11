from flask import Flask, jsonify ,render_template ,request, Response
import os
import csv
import json
import urllib.parse
import glob
import subprocess
import requests

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    name_list=[]
    with open("./name_list.csv") as f:
        for videoId,videoName in csv.reader(f):
            name_list.append((videoId,videoName))
    return render_template("index.html",name_list=name_list)

@app.route('/post_url',methods=["POST"])
def post_url():
    url = request.form["youtube_url"]
    qs = urllib.parse.urlparse(url).query
    video_id = []
    try:
        video_id = urllib.parse.parse_qs(qs)["v"]
    except KeyError:
        url = requests.get(request.form["youtube_url"]).url
        qs = urllib.parse.urlparse(url).query
        video_id = urllib.parse.parse_qs(qs)["v"]
    response = Response()
    csvfile = ""
    with open("./error.txt") as f:
        for row in csv.reader(f):
            if(row[0] == video_id[0]):
                return Response(response=json.dumps(["error"]), status=200)
    with open("./making.txt") as f:
        for row in csv.reader(f):
            if(row[0] == video_id[0]):
                return Response(response=json.dumps(["making"]), status=200)
    with open("./name_list.csv") as f:
        for videoId,videoName in csv.reader(f):
            if(videoId=="https://www.youtube.com/watch?v="+video_id[0]):
                csvfile = "./summarization_by_comment_count/"+video_id[0]+".csv"
    if(csvfile!=""):
        json_list = []
        keys = ('start', 'end')
        with open(csvfile) as f:
            for row in csv.reader(f):
                json_list.append(row)
        return Response(response=json.dumps(json_list), status=200)

    tmp_files = glob.glob('./tmp/*')
    if(len(tmp_files)!=0):
        return Response(response=json.dumps(["crowd"]), status=200)

    subprocess.Popen( ["bash","make_summarization.sh","https://www.youtube.com/watch?v="+video_id[0],video_id[0]])

    return Response(response=json.dumps(["making"]), status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
