#!/usr/bin/env python3
import wave
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import signal

def get_wave(file):
    print(file)
    wf = wave.open(file, mode="rb")
    print("channel: ", wf.getnchannels())
    print("width: ", wf.getsampwidth())
    print("framerate: ", wf.getframerate())
    print("frame: ", wf.getnframes())

    # if width=2
    w = np.frombuffer(wf.readframes(-1), dtype="int16")

    mw = np.empty(0,dtype="int16")
    mw = np.append(mw,w[ : : 2*10])
    del w
    print(len(mw))
    print(mw.dtype)
    print(int(wf.getframerate()/10))
    return mw,int(wf.getframerate()/10)

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
            ow_part = (ow[start_pos-1:start_pos+ow_framerate+10]-ow[start_pos-1:start_pos+ow_framerate+10].mean())/(np.std(ow[start_pos-1:start_pos+ow_framerate+10])*len(ow[start_pos-1:start_pos+ow_framerate+10]))
            if(n>len(cw)-ow_framerate):
                ow_part = (ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10]-ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10].mean())/(np.std(ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10])*len(ow[start_pos-1:start_pos+len(cw[n:n+ow_framerate])+10]))
            cw_part = (cw[n:n+ow_framerate]-cw[n:n+ow_framerate].mean())/np.std(cw[n:n+ow_framerate])
            corr = signal.correlate(ow_part,cw_part,"full")
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
        cut_len=5
        for s in range(start_pos,len(ow)-len(cw)+1,ow_framerate*60*cut_len):
            corr=0
            ow_part = (ow[s:s+ow_framerate*60*cut_len]-ow[s:s+ow_framerate*60*cut_len].mean())/(np.std(ow[s:s+ow_framerate*60*cut_len])*len(cw[n:n+ow_framerate]))
            cw_part = (cw[n:n+ow_framerate]-cw[n:n+ow_framerate].mean())/np.std(cw[n:n+ow_framerate])
            corr = signal.correlate(ow_part,cw_part,"full")
            print(str(int(s/(ow_framerate*60*cut_len)))+"/"+str(int((len(ow)-len(cw)+1)/(ow_framerate*60*cut_len)))+" start_pos:"+str(start_pos)+" corr.argmax:"+str(corr.argmax())+" pos:"+str(s+corr.argmax()-(len(cw[n:n+ow_framerate]) - 1))+" max:"+str(max(corr)))
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
            ow_part = (ow[s:s+ow_framerate*60*cut_len]-ow[s:s+ow_framerate*60*cut_len].mean())/(np.std(ow[s:s+ow_framerate*60*cut_len])*len(cw[n:n+ow_framerate]))
            cw_part = (cw[n:n+ow_framerate]-cw[n:n+ow_framerate].mean())/np.std(cw[n:n+ow_framerate])
            corr = signal.correlate(ow_part,cw_part,"full")
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
    clipping_part=[]
    pre_part=-1
    for s in estimated_delay:
        if(s==None):
            none_count+=count
            count=0
            none_count+=1
        else:
            if(pre_part!=-1):
                if(pre_part+ow_framerate+5>s and pre_part+ow_framerate-5<s):
                    if(s==estimated_delay[-1]):
                        clipping_part.append((pre_part-ow_framerate*(count+none_count),pre_part))
                    count+=1
                else:
                    if(count!=0):
                        clipping_part.append((pre_part-ow_framerate*(count+none_count),pre_part))
                        none_count=0
                        count=0
                    else:
                        none_count+=1
            pre_part=s

    print(clipping_part)
    return
