[WIP] SuicaRecorder
===================

Suicaの履歴をテキストファイルに保存するためのユーティリティです。

インストール
----------

1. `$ brew install libusb`

2. `$ pip install suicarecorder`


使い方
-----

1. USB接続のNFC読み取り端末をマシンに接続し、カードを設置します。

2. 次のコマンドを実行します（重複する履歴は記録されません）。

```shell
$ record-suica
```

3. `~/.suicarecorder` ディレクトリ下のファイルに履歴が記録されます


動作確認済み端末
-------------

* RC-S380(Sory)
