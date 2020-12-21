import json
import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

def main(comment_file_name):
    print("LOAD", comment_file_name)
    comments_json = json.load(open("./comments/"+comment_file_name+".json", "r", encoding="UTF-8"))

    # 時刻と内容の抽出
    comments_list = []
    for comment in comments_json:
        if(time2sec(comment["time"])<0):
            continue
        comments_list.append((time2sec(comment["time"]), comment["text"]))

    # 時間当たりコメント数
    comment_begin = comments_list[0][0]
    comment_end = comments_list[-1][0]
    comments_per_sec = np.zeros(comment_end - comment_begin + 1)
    for comment in comments_list:
        comments_per_sec[comment[0] - comment_begin] += 1

    # clipの範囲plot
    fig = plt.figure(figsize=(20,3),dpi=100)
    plt.subplot(2, 1, 1)
    for i in range(- comment_begin, len(comments_per_sec), 3600):
        plt.vlines(i, 0, np.max(comments_per_sec), "grey", linestyles="dashed")
    plt.plot(comments_per_sec)
    with open("./clip_position/"+comment_file_name+".csv") as f:
        for row in csv.reader(f):
            a,b=row
            plt.axvspan(int(int(a)/48000),int(int(b)/48000),color="y", alpha=0.3)

    plt.subplot(2, 1, 2)
    a = 10
    plt.plot(np.convolve(comments_per_sec, np.full(10, 1 / a)))
    with open("./clip_position/"+comment_file_name+".csv") as f:
        for row in csv.reader(f):
            a,b=row
            plt.axvspan(int(int(a)/48000),int(int(b)/48000),color="y", alpha=0.3)

    os.makedirs("plot_by_clip/", exist_ok=True)
    fig.savefig("./plot_by_clip/"+comment_file_name+".png")

    #コメント数での要約映像
    fig = plt.figure(figsize=(20,3),dpi=100)
    plt.subplot(2, 1, 1)
    for i in range(- comment_begin, len(comments_per_sec), 3600):
        plt.vlines(i, 0, np.max(comments_per_sec), "grey", linestyles="dashed")
    plt.plot(comments_per_sec)
    with open("./result_by_comment_count/"+comment_file_name+".csv") as f:
        count=0
        for row in csv.reader(f):
            if(count==0):
                count+=1
                continue
            a,b=row
            plt.axvspan(float(a),float(b),color="r", alpha=0.3)

    plt.subplot(2, 1, 2)
    a = 10
    plt.plot(np.convolve(comments_per_sec, np.full(10, 1 / a)))
    with open("./result_by_comment_count/"+comment_file_name+".csv") as f:
        count=0
        for row in csv.reader(f):
            if(count==0):
                count+=1
                continue
            a,b=row
            plt.axvspan(float(a),float(b),color="r", alpha=0.3)

    os.makedirs("plot_by_comment_count/", exist_ok=True)
    fig.savefig("./plot_by_comment_count/"+comment_file_name+".png")

    #bertでの要約映像
    fig = plt.figure(figsize=(20,3),dpi=100)
    plt.subplot(2, 1, 1)
    for i in range(- comment_begin, len(comments_per_sec), 3600):
        plt.vlines(i, 0, np.max(comments_per_sec), "grey", linestyles="dashed")
    plt.plot(comments_per_sec)
    with open("./result_by_bert/"+comment_file_name+".csv") as f:
        count=0
        for row in csv.reader(f):
            if(count==0):
                count+=1
                continue
            a,b=row
            plt.axvspan(float(a),float(b),color="g", alpha=0.3)

    plt.subplot(2, 1, 2)
    a = 10
    plt.plot(np.convolve(comments_per_sec, np.full(10, 1 / a)))
    with open("./result_by_bert/"+comment_file_name+".csv") as f:
        count=0
        for row in csv.reader(f):
            if(count==0):
                count+=1
                continue
            a,b=row
            plt.axvspan(float(a),float(b),color="g", alpha=0.3)

    os.makedirs("plot_by_bert/", exist_ok=True)
    fig.savefig("./plot_by_bert/"+comment_file_name+".png")

    #bert+commentでの要約映像
    fig = plt.figure(figsize=(20,3),dpi=100)
    plt.subplot(2, 1, 1)
    for i in range(- comment_begin, len(comments_per_sec), 3600):
        plt.vlines(i, 0, np.max(comments_per_sec), "grey", linestyles="dashed")
    plt.plot(comments_per_sec)
    with open("./result_by_comment_count_and_bert/"+comment_file_name+".csv") as f:
        count=0
        for row in csv.reader(f):
            if(count==0):
                count+=1
                continue
            a,b=row
            plt.axvspan(float(a),float(b),color="b", alpha=0.3)

    plt.subplot(2, 1, 2)
    a = 10
    plt.plot(np.convolve(comments_per_sec, np.full(10, 1 / a)))
    with open("./result_by_comment_count_and_bert/"+comment_file_name+".csv") as f:
        count=0
        for row in csv.reader(f):
            if(count==0):
                count+=1
                continue
            a,b=row
            plt.axvspan(float(a),float(b),color="b", alpha=0.3)

    os.makedirs("plot_by_comment_count_and_bert/", exist_ok=True)
    fig.savefig("./plot_by_comment_count_and_bert/"+comment_file_name+".png")


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

if __name__ == "__main__":
    args = sys.argv
    main(args[1])
