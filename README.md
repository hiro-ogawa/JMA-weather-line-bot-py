# JMA-weather-line-bot-py

気象庁の天気予報データを利用した現在地の天気予報を表示するLINEボット

## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## 基本的な流れ

1. ユーザからLINEで位置情報を受け取る
2. 位置情報から最寄りの `class20s` のポイントを選ぶ
3. ポイントの天気予報情報を取得してユーザに送信

## 気象庁の天気予報の主なデータ構造

### area.json

https://www.jma.go.jp/bosai/common/const/area.json

位置情報が階層的に記録されている

- centers
  - offices
    - class10s
      - class15s
        - class20s

### 情報へのアクセス

- 明後日までの詳細天気
  - https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json
- 天気予報概要
  - https://www.jma.go.jp/bosai/forecast/data/overview_forecast/130000.json
- 週間天気予報概要
  - https://www.jma.go.jp/bosai/forecast/data/overview_week/130000.json
- 上記の情報は `offices` レベルにしか無い
- `overview_week` は多くの場所で用意されていない

## 課題

`class20s` の `path_code` は `JIS X 0402:2020` に準じているようだが、さらに2桁のサブコードが付随していたり、 `class20s` でJISのすべてを網羅しているわけでもなさそうなので、位置情報から `path_code` を取ってくるのが難しい

LINEで得られる位置情報から、 `class20s` のポイントを出す

### 解決方法

[Yahoo!ジオコーダAPI](https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/geocoder.html) を利用して `class20s` の市区町村名から緯度経度を得る。

## おことわり

気象庁のデータを利用しています。
ご利用の際は[利用規約](https://www.jma.go.jp/jma/kishou/info/coment.html)に則ってご使用ください。
