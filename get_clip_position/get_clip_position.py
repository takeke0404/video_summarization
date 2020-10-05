#!/usr/bin/env python3
import wave
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import signal
import os

SKIP=1

def get_wave(file):

    print("LOAD", file)
    wf = wave.open(file, mode = "rb")
    framerate = wf.getframerate()
    frame = wf.getnframes() # 異なる場合があります
    sampwidth = wf.getsampwidth()
    channel = wf.getnchannels()
    print(" framerate:", framerate)
    print(" frame:", frame)

    if frame < 1000000000:
        buffer = wf.readframes(-1)
    else:
        print("RELOAD")
        wf.close()
        wf2 = open(file, "rb")
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

    if sampwidth == 2:
        # 2 byte -> 16 bit -> int16
        w = np.frombuffer(buffer, dtype = "int16")
    else:
        w = np.empty(0)

    if channel == 1:
        # モノラル
        mw = w[ : : SKIP]
    elif channel == 2:
        # ステレオ
        lw = w[ : : 2*SKIP]
        rw = w[1 : : 2*SKIP]
        mw = (lw >> 1) + (rw >> 1)
    else:
        mw = np.empty(0)

    print(mw.shape)
    del w
    print()
    return mw, int(framerate/SKIP)

def write_wave(file,parts):

    wf = wave.open(file, mode="rb")
    channel = wf.getnchannels()
    framerate = wf.getframerate()
    sampwidth = wf.getsampwidth()

    if wf.getnframes() < 1000000000:
        buffer = wf.readframes(-1)
    else:
        wf.close()
        print("RELOAD")
        wf2 = open(file, "rb")
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
    for a,b in parts:
        ww = np.append(ww,mw[a:b])

    of = wave.open("clips/"+os.path.basename(file),"wb")
    of.setparams((channel,sampwidth,framerate,len(ww),"NONE", "not compressed"))
    of.writeframes(ww)
    of.close()

    return

def get_clip_position(video_filename,crip_filename):
    ow,ow_framerate = get_wave(video_filename)
    cw,cw_framerate = get_wave(crip_filename)

    start = time.time()

    t_flag=0
    not_match_flag=0
    start_pos=0
    estimated_delay=[]
    #cripの1秒ごとに一致する区間を探す
    for n in range(0,len(cw),ow_framerate):
        if(not_match_flag==1):
            not_match_flag=0
            estimated_delay.append(None)
            continue
        print("切り抜き:"+str(int(n/ow_framerate))+"/"+str(int(len(cw)/ow_framerate))+" 経過時間:"+str(time.time()-start))
        if(t_flag==1):
            ow_part = (ow[start_pos-1:start_pos+ow_framerate+10]-np.mean(ow[start_pos-1:start_pos+ow_framerate+10]))
            if(np.std(ow[start_pos-1:start_pos+ow_framerate+10])!=0):
                ow_part/=(np.std(ow[start_pos-1:start_pos+ow_framerate+10]))
            if(n>len(cw)-ow_framerate):
                ow_part = (ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10]-np.mean(ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10]))
                if(np.std(ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10])!=0):
                    ow_part/=np.std(ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10])
            cw_part = (cw[n:n+ow_framerate]-np.mean(cw[n:n+ow_framerate]))
            if(np.std(cw[n:n+ow_framerate])!=0):
                cw_part/=np.std(cw[n:n+ow_framerate])
            corr = signal.correlate(ow_part,cw_part,mode='full',method='auto')/len(cw_part)
            print("start_pos:"+str(start_pos)+" corr.argmax:"+str(corr.argmax())+" pos:"+str(start_pos+corr.argmax()-(len(cw[n:n+ow_framerate])-1))+" max:"+str(max(corr)))
            if(max(corr)>0.6):
                estimated_delay.append(start_pos+corr.argmax()-(len(cw[n:n+ow_framerate])-1))
                if(start_pos>len(ow)-ow_framerate):
                    start_pos=0
                start_pos=start_pos+ow_framerate+1
                continue
        #元動画5分ごとに一致度の最大値をとる
        cut_len=5
        for s in range(start_pos,len(ow)-len(cw)+1,ow_framerate*60*cut_len):
            corr=0
            ow_part = (ow[s:s+ow_framerate*60*cut_len]-np.mean(ow[s:s+ow_framerate*60*cut_len]))
            if(np.std(ow[s:s+ow_framerate*60*cut_len])!=0):
                ow_part/=(np.std(ow[s:s+ow_framerate*60*cut_len]))
            cw_part = (cw[n:n+ow_framerate]-np.mean(cw[n:n+ow_framerate]))
            if(np.std(cw[n:n+ow_framerate])!=0):
                cw_part/=np.std(cw[n:n+ow_framerate])
            corr = signal.correlate(ow_part,cw_part,mode='full',method='auto')/len(cw_part)
            print(str(int(s/(ow_framerate*60*cut_len)))+"/"+str(int((len(ow)-len(cw)+1)/(ow_framerate*60*cut_len)))+" start_pos:"+str(start_pos)+" corr.argmax:"+str(corr.argmax())+" pos:"+str(s+corr.argmax()-(len(cw[n:n+ow_framerate]) - 1))+" max:"+str(max(corr)))
            if(t_flag==1 and s==start_pos):
                if(ow_framerate-5<corr.argmax() and ow_framerate+5>corr.argmax()):
                    estimated_delay.append(s+corr.argmax()-(len(cw[n:n+ow_framerate]) - 1))
                    start_pos=s+corr.argmax()+1
                    continue
                t_flag=0
            if(max(corr)>0.75):
                estimated_delay.append(s+corr.argmax()-(len(cw[n:n+ow_framerate]) - 1))
                start_pos=s+corr.argmax()+1
                t_flag=1
                break
        if(t_flag==1):
            continue
        for s in range(0,start_pos,ow_framerate*60*cut_len):
            if(start_pos==0):
                break
            corr=0
            ow_part = (ow[s:s+ow_framerate*60*cut_len]-np.mean(ow[s:s+ow_framerate*60*cut_len]))
            if(np.std(ow[s:s+ow_framerate*60*cut_len])!=0):
                ow_part/=(np.std(ow[s:s+ow_framerate*60*cut_len]))
            cw_part = (cw[n:n+ow_framerate]-np.mean(cw[n:n+ow_framerate]))
            if(np.std(cw[n:n+ow_framerate])!=0):
                cw_part/=(np.std(cw[n:n+ow_framerate]))
            corr = signal.correlate(ow_part,cw_part,mode='full',method='auto')/len(cw_part)
            print(str(int(s/(ow_framerate*60*cut_len)))+"/"+str(int((len(ow)-len(cw)+1)/(ow_framerate*60*cut_len)))+" start_pos:"+str(start_pos)+" corr.argmax:"+str(corr.argmax())+" pos:"+str(s+corr.argmax()-(len(cw[n:n+ow_framerate]) - 1))+" max:"+str(max(corr)))
            if(max(corr)>0.75):
                estimated_delay.append(s+corr.argmax()-(len(cw[n:n+ow_framerate]) - 1))
                start_pos=s+corr.argmax()+1
                t_flag=1
                break
        estimated_delay.append(None)
        not_match_flag=1

    end = time.time()
    print("実行時間:"+str(end-start)+"s")

    print(estimated_delay)

    none_count=0
    count=0
    clipping_part=[(0,0)]
    pre_part=-1
    for i,s in enumerate(estimated_delay):
        if(s==None):
            none_count+=count
            count=0
            none_count+=1
        else:
            if(pre_part!=-1):
                if(pre_part+ow_framerate+5>s and pre_part+ow_framerate-5<s):
                    if(i==len(estimated_delay)-1):
                        a,b = clipping_part[-1]
                        if(b==s-ow_framerate*(count+none_count)):
                            clipping_part[-1] = (a,s+ow_framerate)
                        else:
                            clipping_part.append((s-ow_framerate*(count+none_count),s+ow_framerate))
                    elif(i!=len(estimated_delay)-1 and estimated_delay[i+1]==None):
                        a,b = clipping_part[-1]
                        if(b>=s-ow_framerate*(count+none_count) and a<s-ow_framerate*(count+none_count)):
                            clipping_part[-1] = (a,s+ow_framerate)
                        else:
                            clipping_part.append((s-ow_framerate*(count+none_count),s+ow_framerate))
                        none_count=0
                        count=0
                        continue
                    count+=1
                else:
                    if(count!=0):
                        a,b = clipping_part[-1]
                        if(b==pre_part-ow_framerate*(count+none_count-1)):
                            clipping_part[-1] = (a,pre_part+ow_framerate)
                        else:
                            clipping_part.append((pre_part-ow_framerate*(count+none_count-1),pre_part+ow_framerate))
                        none_count=1
                        count=0
                    else:
                        none_count+=1
            if(i==0):
                none_count+=1
            pre_part=s

    clipping_part.pop(0)
    del ow,cw
    for i in range(len(clipping_part)):
        a,b=clipping_part[i]
        clipping_part[i]=(a*SKIP,b*SKIP)
    write_wave(video_filename,clipping_part)
    print(clipping_part)

    with open('positions/'+os.path.splitext(os.path.basename(video_filename))[0]+".csv",mode='w') as f:
        for row in clipping_part:
            print(*row, sep=',', file=f)

    return
