#!/usr/bin/env python3
import wave
import numpy as np
import matplotlib.pyplot as plt
import time

def get_wave(file):
    print(file)
    wf = wave.open(file, mode="rb")
    print("channel: ", wf.getnchannels())
    print("width: ", wf.getsampwidth())
    print("framerate: ", wf.getframerate())
    print("frame: ", wf.getnframes())

    # if width=2
    w = np.frombuffer(wf.readframes(-1), dtype="int16")

    mw = w[ : : 2]
    del w
    print(len(mw))
    print(mw.dtype)
    return mw,wf.getframerate()

def get_crip_position(video_filename,crip_filename):
    ow,ow_framerate = get_wave(video_filename)
    cw,cw_framerate = get_wave(crip_filename)

    start = time.time()

    t_flag=0
    start_pos=0
    estimated_delay=[]
    #cripの1秒ごとに一致する区間を探す
    for n in range(0,len(cw),ow_framerate):
        print("平均:"+str(((np.abs(cw[n:n+ow_framerate])**0.1).mean())))
        print("切り抜き:"+str(int(n/ow_framerate))+"/"+str(int(len(cw)/ow_framerate))+" 経過時間:"+str(time.time()-start))
        if(t_flag==1):
            ow_part = (ow[start_pos-1:start_pos+ow_framerate+10]-ow[start_pos-1:start_pos+ow_framerate+10].mean())/(np.std(ow[start_pos-1:start_pos+ow_framerate+10])*len(ow[start_pos-1:start_pos+ow_framerate+10]))
            if(n>len(cw)-ow_framerate):
                ow_part = (ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10]-ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10].mean())/(np.std(ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10])*len(ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10]))
            cw_part = (cw[n:n+ow_framerate]-cw[n:n+ow_framerate].mean())/np.std(cw[n:n+ow_framerate])
            corr = np.correlate(ow_part,cw_part,"full")
            print("start_pos:"+str(start_pos)+" corr.argmax:"+str(corr.argmax())+" pos:"+str(start_pos)+" max:"+str(max(corr)))
            if(max(corr)>0.75):
                estimated_delay.append(start_pos)
                if(start_pos>len(ow)-ow_framerate):
                    start_pos=0
                start_pos=start_pos+ow_framerate
                continue
            else:
                t_flag=0
        #元動画5分ごとに一致度の最大値をとる
        for s in range(start_pos,len(ow)-len(cw)+1,ow_framerate*60*5):
            corr=0
            ow_part = (ow[s:s+ow_framerate*60*5]-ow[s:s+ow_framerate*60*5].mean())/(np.std(ow[s:s+ow_framerate*60*5])*len(cw[n:n+ow_framerate]))
            cw_part = (cw[n:n+ow_framerate]-cw[n:n+ow_framerate].mean())/np.std(cw[n:n+ow_framerate])
            corr = np.correlate(ow_part,cw_part,"full")
            print(str(int(s/(ow_framerate*60*5)))+"/"+str(int((len(ow)-len(cw)+1)/(ow_framerate*60*5)))+" start_pos:"+str(start_pos)+" corr.argmax:"+str(corr.argmax())+" pos:"+str(s+corr.argmax()-(len(cw[n:n+ow_framerate]) - 1))+" max:"+str(max(corr)))
            if(max(corr)>0.75):
                estimated_delay.append(s+corr.argmax()-(len(cw[n:n+ow_framerate]) - 1))
                start_pos=s+corr.argmax()+1
                t_flag=1
                break
        if(t_flag==1):
            continue
        for s in range(0,start_pos,ow_framerate*60*5):
            if(start_pos==0):
                break
            corr=0
            ow_part = (ow[s:s+ow_framerate*60*5]-ow[s:s+ow_framerate*60*5].mean())/(np.std(ow[s:s+ow_framerate*60*5])*len(cw[n:n+ow_framerate]))
            cw_part = (cw[n:n+ow_framerate]-cw[n:n+ow_framerate].mean())/np.std(cw[n:n+ow_framerate])
            corr = np.correlate(ow_part,cw_part,"full")
            print(str(int(s/(ow_framerate*60*5)))+"/"+str(int((len(ow)-len(cw)+1)/(ow_framerate*60*5)))+" start_pos:"+str(start_pos)+" corr.argmax:"+str(corr.argmax())+" pos:"+str(s+corr.argmax()-(len(cw[n:n+ow_framerate]) - 1))+" max:"+str(max(corr)))
            if(max(corr)>0.75):
                estimated_delay.append(s+corr.argmax()-(len(cw[n:n+ow_framerate]) - 1))
                start_pos=s+corr.argmax()+1
                t_flag=1
                break
        estimated_delay.append(None)

    end = time.time()
    print("実行時間:"+str(end-start)+"s")

    print(estimated_delay)

    fig = plt.figure()

    plt.subplot(4, 1, 1)
    plt.ylabel("original")
    plt.plot(ow[estimated_delay[0]:estimated_delay[0]+ow_framerate])

    plt.subplot(4, 1, 2)
    plt.ylabel("crip")
    plt.plot(cw[0:ow_framerate], color="g")

    fig.savefig("plot.png")

    return
