import csv
import os
import random

def main():
    trains_dir="./train-comments"
    tests_dir="./test-comments"
    trains_file=os.listdir(trains_dir)
    tests_file=os.listdir(tests_dir)
    train_data=[]
    zero_count=0
    for file in trains_file:
        with open(trains_dir+"/"+file) as f:
            for t,s,e,a,b in csv.reader(f):
                if(int(b)==0 and zero_count%30==0 or int(b)==1):
                    train_data.append((a,b))
                if(int(b)==0):
                    zero_count+=1
    with open("trains/features.csv",mode='w') as f:
        print("feature", sep='', file=f)
        for text,label in train_data:
            print(*text, sep='', file=f)
    with open("trains/labels.csv",mode='w') as f:
        print("label", sep='', file=f)
        for text,label in train_data:
            print(*label, sep='', file=f)

    test_data=[]
    zero_count=0
    for file in tests_file:
        with open(tests_dir+"/"+file) as f:
            for t,s,e,a,b in csv.reader(f):
                if(int(b)==0 and zero_count%30==0 or int(b)==1):
                    test_data.append((a,b))
                if(int(b)==0):
                    zero_count+=1
    with open("tests/features.csv",mode='w') as f:
        print("feature", sep='', file=f)
        for text,label in test_data:
            print(*text, sep='', file=f)
    with open("tests/labels.csv",mode='w') as f:
        print("label", sep='', file=f)
        for text,label in test_data:
            print(*label, sep='', file=f)

if __name__ == "__main__":
    main()
