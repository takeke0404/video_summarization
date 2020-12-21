# 使い方
docker-compose run コンテナ名

webのとき --service-ports オプション要

# bertの学習
dockerを起動
docker-compose run get_video : 学習用配信音声とコメントダウンロード
docker-compose run get_clip_position : youtubeの配信を切り抜いた動画の元の配信映像での区間を検出
docker-compose run speech_segmentation : 音声のセグメンテーション
docker-compose run make_bert_data : 切り抜きの範囲のコメントを1それ以外のコメントを0とする学習データを作成
./bert_train 以下のフォルダをgoogle driveに入れてgoogle colab(TPU)で学習

# comment countによる要約

# bertによる要約

# comment count + bert による要約

# summarization_all 任意のurlリストから要約映像を作成する

# web サーバー上から要約映像を配信する

# 各種コンテナ
## get_video
list.txt(切り抜き動画のurl　元動画のurl)から音声、チャットリプレイを取得
## get_clip_position
## analyze_comment
## speech_segmentation
## summarization_by_comment_count
## web
