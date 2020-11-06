# pisat

## Overview

pisat はロボットや IoT 機器を製作するための Python フレームワークです．
現時点では Raspberry Pi の GPIO のみ対応しています．
詳細は[開発者用ドキュメント](./docs/developer/)を参照してください．

## Examples

応用例は [sample](./sample/) を参照してください．

## Installation

pip または pipenv を用いてインストール可能です．
ただし，Rapsberry Pi 以外のデバイスでインストールした場合には
Raspberry Pi でのみ動作可能なミドルウェアはインストールされないので注意してください．

```
$ pip insatll git+https://github.com/jjj999/pisat.git
```
```
$ pipenv install git+https://github.com/jjj999/pisat.git#egg=pisat
```

## Deploy Developing Environment

開発環境をデプロイする場合は，リポジトリをクローン後にリポジトリのルート上で

```
$ pipenv install
```

を実行してください．
環境の詳細は[開発者用ドキュメント](./docs/developer/)を参照してください．

## Documentation

pisat に関するドキュメントや API は [docs](./docs/) を参照してください．
ただし，サブパッケージによってはドキュメントの整備が追いついていない可能性があります．
