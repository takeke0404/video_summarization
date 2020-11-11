import os
import sys
import numpy as np
import json
import csv
import wave

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
clip_length=300

def main(name):
    # 読み込み
    comments_json = json.load(open('../get_video/comments/'+name+'.json', "r", encoding="UTF-8"))

    # 時刻と内容の抽出
    comments_list = []
    for comment in comments_json:
        if(time2sec(comment["time"])<0):
            continue
        comments_list.append((time2sec(comment["time"]), comment["text"]))

    n=0
    flag=True
    clip_segments = []
    while flag:
        n+=1
        # 時間当たりコメント数(30秒までの畳み込み和,要約の長さまで上位n件)
        comment_begin = comments_list[0][0]
        comment_end = comments_list[-1][0]
        comments_per_sec = np.zeros(comment_end - comment_begin + 1)
        for comment in comments_list:
            comments_per_sec[comment[0] - comment_begin] += 1
        comment_count = np.convolve(comments_per_sec,[2]*20+[1]*10,)[30:]
        times = np.sort(np.argpartition(comment_count, -n)[-n:])

        # コメントが多かった部分を含む音声区間を抽出
        segments = []
        with open("../speech_segmentation/segmentation/"+name+".csv") as f:
            prev = ("",0,0)
            for type,start,end in csv.reader(f):
                for time in times:
                    if(float(start)<=time and time<=float(end)):
                        # 検出された区間のひとつ前のnoEnergy,noise以外の区間を結合
                        segments.append(prev)
                        # 検出された区間の結合
                        segments.append((type,float(start),float(end)))
                if (type != "noEnergy" and type != "noise"):
                    prev = (type,float(start),float(end))
            segments = list(dict.fromkeys(segments))
        # 前の区間と5秒以上空いていない区間同士を結合
        segments = taple_join(segments,5)
        len=0
        for t,s,e in segments:
            len+=e-s
        if (len>clip_length):
            flag=False
        else:
            clip_segments=segments

    print(clip_segments)
    output_comment(name,clip_segments,comments_list)
    output_wav(name,clip_segments)
    # urlを先頭につけてcsvで書き出し
    url=""
    with open('../get_video/name_list.txt') as f:
        for video_url,video_name in csv.reader(f):
            if(video_name==name):
                url=video_url
    with open('result/'+name+".csv",mode='w') as f:
        print(*url, sep='',file=f)
        for type,start,end in clip_segments:
            print(*(round(start,2),round(end,2)), sep=',', file=f)
    return

def time2sec(time_str):
    sec = 0
    if time_str.startswith("-"):
        ts = time_str[1 : ]
        mul = - 1
    else:
        ts = time_str
        mul = 1
    l = ts.split(":")
    for a in l[::-1]:
        sec += int(a) * mul
        mul *= 60
    return sec

def taple_join(taple,n):
    result = [taple[0]]
    for typet,st,et in taple:
        typer,sr,er = result[-1]
        if (er+n>=st):
            result[-1]=(typer,sr,et)
        else:
            result.append((typet,st,et))
    return result

def output_wav(name,clip_segments):
    # 音声clip出力
    wf = wave.open('../get_video/videos/'+name+'.wav', mode="rb")
    channel = wf.getnchannels()
    framerate = wf.getframerate()
    sampwidth = wf.getsampwidth()

    if wf.getnframes() < 1000000000:
        buffer = wf.readframes(-1)
        wf.close()
    else:
        wf.close()
        print("RELOAD")
        wf2 = open('../get_video/videos/'+name+'.wav', "rb")
        print("", wf2.read(4)) # RIFF
        wf2.read(4) # ファイルサイズ
        print("", wf2.read(4)) # WAVE
        while True:
            t = wf2.read(4) # チャンク名
            s = int.from_bytes(wf2.read(4), "little") # チャンクサイズ
            print("", t, s)
            if t == b"data":
                break
            wf2.read(s) # チャンク飛ばす
        buffer = wf2.read()

    w = np.frombuffer(buffer, dtype="int16")
    if channel == 1:
        # モノラル
        mw = w
    elif channel == 2:
        # ステレオ
        lw = w[ : : 2]
        rw = w[1 : : 2]
        mw = (lw >> 1) + (rw >> 1)
    else:
        mw = np.empty(0)
    ww = np.empty(0,dtype="int16")
    for type,start,end in clip_segments:
        ww = np.append(ww,mw[int(round(start,2)*framerate):int(round(end,2)*framerate)])

    of = wave.open("clips/"+name+".wav","wb")
    of.setparams((channel,sampwidth,framerate,len(ww),"NONE", "not compressed"))
    of.writeframes(ww)
    of.close()
    return

def output_comment(name,clip_segments,comments_list):
    #  範囲のコメントをファイル出力
    clip_comment = []
    for type,start,end in clip_segments:
        for comment in comments_list:
            time,text = comment
            if( start<time and time<end+10 ):
                clip_comment.append((time,text))
    clip_comment = list(dict.fromkeys(clip_comment))
    with open('comments/'+name+".txt",mode='w') as f:
        for row in clip_comment:
            print(*row, sep=',', file=f)
    return

if __name__ == "__main__":
    args = sys.argv
    main(args[1])
