from inaSpeechSegmenter import Segmenter
import os
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def main(name):

    # 音声区間を抽出
    input_file='./videos/'+name+'.wav'
    print(input_file)
    seg = Segmenter(vad_engine='smn', detect_gender=False)
    segmentation = seg(input_file)

    with open('segmentation/'+name+".csv",mode='w') as f:
        for type,start,end in segmentation:
            if (end-start>20 and type=="music"):
                t=start+10
                print(*(type,start,t), sep=',', file=f)
                while(end-t>20):
                    print(*(type,t,t+10), sep=',', file=f)
                    t+=10
                print(*(type,t,end), sep=',', file=f)
            else:
                print(*(type,start,end), sep=',', file=f)

if __name__ == "__main__":
    args = sys.argv
    main(args[1])
