# pisat (Alpha)

## Overview

pisat は[東北大学 From The Earth](https://www.fte-tohoku.org/) のCanSatチームが開発している CanSat フレームワークです．
詳細は[開発者用ドキュメント](./docs/developer/)を参照してください．

## Examples

応用例は [sample](./sample/) を参照してください．

## Installation

### pip

```
$ pip insatll git+https://github.com/jjj999/pisat.git
```

### pipenv

```
$ pipenv install git+https://github.com/jjj999/pisat.git#egg=pisat
```

### 開発環境をデプロイ

開発環境をデプロイする場合は，リポジトリをクローン後にリポジトリのルート上で

```
$ pipenv install
```

を実行してください．
環境の詳細は[開発者用ドキュメント](./docs/developer/)を参照してください．

## Documentation

pisat に関するドキュメントや API は [docs](./docs/) を参照してください．
ただし，サブパッケージによってはドキュメントの整備が追いついていない可能性があります．
