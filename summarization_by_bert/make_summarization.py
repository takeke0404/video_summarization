import csv
import wave
import sys
import numpy as np

clip_length=300

def taple_join(taple,n):
    result = [taple[0]]
    for typet,st,et in taple:
        typer,sr,er = result[-1]
        if(sr<=st and et<=er):
            result[-1]=(typer,sr,er)
        elif(er+n>=st):
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

if __name__ == "__main__":
    name=sys.argv[1]
    predict=[]
    with open('./predict_result/'+name+'.csv') as f:
        for t,s,e,a,b in csv.reader(f):
            predict.append([t,s,e,a,b])
    predict=sorted(predict, key=lambda x: x[3],reverse=True)
    n=0
    flag=True
    clip_segments=[]
    while flag:
        n+=1
        l=predict[0:n]
        segments = []
        detect=False
        with open("../speech_segmentation/segmentation/"+name+".csv") as f:
            prev = ("",0,0)
            for type,start,end in csv.reader(f):
                if(detect):
                    if(type=="noise"):# 誤検知の可能性があるので検出直後のnoise区間は追加
                        detect=False
                        segments.append((type,float(start),float(end)))
                        continue
                    detect=False
                    continue
                for t,s,e,a,b in l:
                    if(float(e)==float(end)):
                        # 検出された区間のひとつ前のnoEnergy,noise以外の区間を結合
                        segments.append(prev)
                        # 検出された区間の結合
                        segments.append((type,float(start),float(end)))
                        detect=True
                        break
                if (type != "noEnergy" and type != "noise"):
                    prev = (type,float(start),float(end))
            segments = list(dict.fromkeys(segments))
        # 前の区間と5秒以上空いていない区間同士を結合
        segments = taple_join(segments,5)
        length=0
        for t,s,e in segments:
            length+=e-s
        if (length>clip_length):
            flag=False
        else:
            clip_segments=segments

    output_wav(name,clip_segments)
    # urlを先頭につけてcsvで書き出し
    url=""
    with open('../get_video/name_list.txt') as f:
        for video_url,video_name in csv.reader(f):
            if(video_name==name):
                url=video_url
    with open('./result/'+name+".csv",mode='w') as f:
        print(*url, sep='',file=f)
        for type,start,end in clip_segments:
            print(*(round(start,2),round(end,2)), sep=',', file=f)
