# pisat (Alpha)

pisat は[東北大学 From The Earth](https://www.fte-tohoku.org/) のCanSatチームが開発している
Raspberry Pi を用いた CanSat フレームワークです．
団体のリポジトリは[こちら](https://github.com/FROM-THE-EARTH)．

## 目的

* CanSat のコンポーネントの抽象化
* 各コンポーネントを統合するシステム開発
* Raspberry Pi を使った IoT デバイス開発の体系化

## Developer Documents
開発者用ドキュメントは[docs/developer](./docs/developer)にあります．全編日本語．

## リファレンス
APIやCanSatクラスの作成方法，その他デバイスへの応用などは[Wiki](./wiki)に掲載します．
掲載場所は変更になる可能性があります．

## プロジェクト
現在走っている開発プロジェクトは[Projects](./projects)を参照してください．

## 各ディレクトリの説明

### [docs](./docs/)
APIや開発者用のドキュメントを置きます．

### [data](./data/)
シミュレートやデータ分析に利用可能なデータを置きます．

### [pisat](./pisat/)
これが開発中のパッケージです．

### [sample](./sample/)
pisat を使ったサンプルプログラムが置かれています．

### [tests](./tests/)
デバッグ・検証用のスクリプトを置いてます．
内部のディレクトリ構造は pisat ディレクトリと同じです．
何かモジュールを作成した場合は検証用のスクリプトを作成し，このディレクトリ内に置きます．
