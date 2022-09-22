## 概要
最新の歯科ニュースをSlackに連携することで調査コストを下げ、全体に歯科情報の共有を促す

## 対象
情報調達する際の対象は下記の通り
- WHITE CROSS
- 1D
- Doctorbook academy

## 処理概要
- scrapingによりそれぞ:qれのHPより情報を収集する。
- 取り纏め情報も欲しいことからCSVにて保管する。
- 追加情報があった場合は、Slackに連携、またコミットしmaster情報としても保管する。
- 情報の区分としては、情報、セミナーと2つに大きくは分ける。
- 不必要なカテゴリー対応ができるようにする。

## python library 追加時
pip freeze > requirements.txt

## 変更反映、リリース方法
herokuに反映
```
git init
git remote add heroku https://git.heroku.com/dental-scraping.git
git add . 
git commit -m "aap commit"
git push heroku master
```
## 実行スケジュール
世界標準時間(-9時間)のため確認の際は注意
https://dashboard.heroku.com/apps/dental-scraping/scheduler
