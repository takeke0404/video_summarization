from inaSpeechSegmenter import Segmenter
import os
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def main(name):

    # 音声区間を抽出
    input_file='tmp/'+name+'.wav'
    print(input_file)
    seg = Segmenter(vad_engine='smn', detect_gender=False)
    segmentation = seg(input_file)

    with open('tmp/'+name+".csv",mode='w') as f:
        for type,start,end in segmentation:
            print(*(type,start,end), sep=',', file=f)

if __name__ == "__main__":
    args = sys.argv
    main(args[1])
