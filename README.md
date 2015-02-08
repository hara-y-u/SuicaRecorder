[WIP] SuicaRecorder
===================

Suicaの履歴をテキストファイルに保存するためのユーティリティです（開発中）。

インストール
----------

1. [bazaar](http://bazaar.canonical.com/), [libusb](http://libusb.info)をインストール

2. `$ pip install suicarecorder`


使い方
-----

1. USB接続のNFC読み取り端末をマシンに接続します

2. 次のコマンドを実行します（重複する履歴は記録されません）

    ```shell
    $ recordsuica
    ```

3. Suicaなどのfelicaカードを読み取り端末にかざします

4. `~/.suicarecorder` ディレクトリ下のファイルに履歴が記録されます


動作確認済み端末
-------------

[nfcpyのドキュメントを参照してください](https://nfcpy.readthedocs.org/en/latest/overview.html#supported-hardware)


謝辞
---

* [nfcpyでお手軽NFC開発[1/2]](http://techblog.qoncept.jp/?p=165)

    nfcpyからRC-S380を扱えることを初めて知り、サンプルコードなども参考になりました。

* [SFCardFan](http://www.denno.net/SFCardFan/index.php)

    公開されている路線・駅コードのデータベースが役に立ちました。

* [FeliCa Library wiki](http://sourceforge.jp/projects/felicalib/wiki/suica)

    データのフォーマットや、コードの種別などのまとまった情報が役立ちました。
