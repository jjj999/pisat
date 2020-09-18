# 独自の拡張について

このドキュメントは

- [pisat のサブパッケージについて](pkg_overview.md)
- [pisat システムについて](system.md)
- [pisat を利用した実装について](implementation.md)

を読んだことを前提としています．

## コンポーネントとは

コンポーネントとは，直感的には**pisat システムにおける部品**という理解されます．
つまり，コンポーネントとはミッション遂行のための道具と変わりありません．
道具と言われるとハードウェアを想像するかもしれませんが，
ハードウェアをソフトウェア的に実装したほとんどのクラスがコンポーネントであると同時に，
ハードウェア的な実体のないようなコンポーネントも存在します．

コンポーネントとは厳密には，pisat.base.Component クラスのサブクラスのオブジェクトのことを指します．
これがハードウェア的な実体のないコンポーネントが存在する理由です．
背景がどうであれ，Component クラスを継承すればコンポーネントを作成することは可能です．

pisat の様々なサブクラスでは Component クラスを継承した基底クラスが用意されています．
例えば，センサーを実装するための基底クラスとして pisat.sensor.SensorBase などがあります．
ユーザーはこのような派生した基底クラスを継承することで，
目的の性質を持つコンポーネントを実装することが出来ます．

### コンポーネントである恩恵

コンポーネントであることの最大の価値は ComponentManager を用いて呼び出し可能であるということです．
正直これは大した恩恵ではありませんが，今後 Component の機能が増えれば
その恩恵は大きなものになるかもしれません．

現時点では，ComponentManager に登録されたコンポーネントは CanSat オブジェクトによって
ミッション終了まで保持されるため，実行時に ComponentManager を用いて呼び出し可能です．
この性質を利用して，異なる Node 間でのオブジェクトの共有を行うことが出来ます．


## コンポーネントの実装について

ここでは Component クラスを継承し，複数の Node から参照可能なカウンターを実装してみましょう．

```python
from typing import Optional

from pisat.base import Component

class Counter(Component):

    def __init__(self, name:Optional[str] = None):
        # Component のコンストラクタを呼び出す
        # Component には name プロパティが定義されている
        super().__init__(name=name)

        self._count: int = 0

    @property
    def count(self):
        return self._count

    def increment(self):
        self._count += 1

    def reset(self):
        self._count = 0
```

上記のコードの概要は以下のとおりです：

- カウンターのためのインスタンス変数を持つ
- 1だけ増加させるメソッドを持つ
- 0にリセットするメソッドを持つ

そして，このコンポーネントを ComponentManager に登録します．

```python
# 名前は counter にする
counter = Counter(name="counter")

# 登録
manager = ComponentManager(counter)
```

次に，Context と Node クラスを定義します．
今回は TestNode1 クラスと TestNode2 クラスの2つの Node クラスを定義します．
Context は以下の通りです．

```python
context = Context({
    TestNode1: {True: TestNode2, False: TestNode1},
    TestNode2: {True: None, False: TestNode2}
})
```

まずは TestNode1 を定義します．

```python
from pisat.core.nav import Node

class TestNode1(Node):

    def enter(self):
        self.counter = self.manager.get_component("counter")

    def judge(self, data) -> bool:
        self.counter.increment()

        if self.counter.count > 5:
            return True
        else:
            return False
```

次に，TestNode2 を定義します．

```python
from pisat.core.nav import Node

class TestNode2(Node):

    def enter(self):
        self.counter = self.manager.ger_component("counter")

    def judge(self, data) -> bool:
        if self.counter.count > 5:
            print("Good")
            self.counter.reset()

        self.counter.increment()

        if self.counter.count > 2:
            return True
        else:
            return False
```

最後に，CanSat オブジェクトを生成しミッションを実行してみましょう．

```python
cansat = CanSat(context, manager)
cansat.run()
```

上記のコードを実行すると，コンソールには「Good」と表示されるはずです．
詳細は今回のサンプルの[ソースコード](../../../../sample/counter/)を参照してください．


## ハンドラ

### 概要

ハンドラは様々な GPIO などのハードウェアインターフェースを利用するための
ミドルウェアのインターフェースを揃えるための緩衝材です．

全てのハンドラの大元の基底クラスは HandlerBase であり，
HandlerBase は Component のサブクラスです．
各ハードウェアインターフェースには対応するサブクラスがあり，
それらは全て HandlerBase のサブクラスとなります．
現時点でハンドラが対応しているハードウェアインターフェースと
その基底クラスは以下の通りです．

- デジタル入力（DigitalInputHandlerBase）
- デジタル出力（DigitalOutputHandlerBase）
- PWM（PWMHandlerBase）
- I2C（I2CHandlerBase）
- SPI（SPIHandlerBase）
- USB・UART（SerialHandlerBase）

これらのハンドラの基底クラスをミドルウェアを用いて実装することで，
共通のインターフェースを持つラッパークラスを実装しています．
現時点で実装に用いたミドルウェアとその具象クラスは以下の通りです．

- pigpio
  - PigpioDigitalInputHandler
  - PigpioDigitalOutputHandler
  - PigpioPWMHandler
  - PigpioI2CHandler
  - PigpioSPIHandler
  - PigpioSerialHandler
- RPi.GPIO
  - RpiGpioDigitalInputHandler
  - RpiGpioDigitalOutputHandler
  - RpiGpioPWMHandler
- pyserial
  - PyserialSerialHandler

### ハンドラの利用

ハンドラはコンポーネントなので，そのままでも利用可能です．
InputHandlerBase，OutputHandlerBase などはその具象クラスを
そのまま利用することもあるでしょう．
しかし，ハンドラの真の目的はハードウェアを実装した上位のコンポーネント内で
電気信号処理を行うためにあります．

例えば，多くのセンサーでは I2C，SPI，UART などの通信規格を備えています．
また，多くのモータードライバでは PWM 信号で制御できるように設計されています．
ハンドラはそれらの通信規格において電気信号を処理するために利用できます．
しかも，上述したハンドラの具象クラスは通信規格が同じであればインターフェースは同じなので，
いくつかのミドルウェアの中からユーザーが選択し利用することが出来ます．
例えば，あるセンサーが UART を通信規格として採用しているとしましょう．
このとき，ユーザーは UART を処理するハンドラとして PigpioSerialHandler か 
PyserialSerialHandler を選択することが出来ます．

ハンドラの操作は pisat において最も抽象度の低い操作の1つです．
つまり，最もハードウェアの知識が要求される操作の1つということです．
ハンドラを操作し電気信号を処理するためには，通信規格などに対する一定の知識を要します．
通信規格などにある程度習熟した状態で，ハンドラの操作を行うことをお勧めします．

ハンドラを用いて実装されているサブパッケージについては
[初回のドキュメント](pkg_overview.md)をサブパッケージ間の依存関係を参照してください．


## センサーの実装

pisat.sensor サブパッケージの多くのセンサークラスはハンドラを用いて実装されています．
ここでは，ハンドラを用いてセンサークラスを実装する方法と，
既に実装されているセンサークラスをラップする方法の2通りについて述べます．

### SensorBase について

pisat.sensor.SensorBase は全てのセンサークラスが継承すべき基底クラスです．
逆に pisat では SensorBase を継承し実装したクラスのオブジェクトをセンサーと呼んでいます．

SensorBase にはオーバーライドすべき変数，メソッドが以下の4つあります．

- SensorBase.DATA_NAMES
- SensorBase.DEFAULT_VALUES
- SensorBase.readf
- SensorBase.read

DATA_NAMES はデータ名を定義するためのクラス変数です．
型は Tuple[str] であり，データ名が1つであっても型は遵守する必要があります．

DEFAULT_VALUES はデバッグモード時の read メソッドの戻り値となるクラス変数です．
型は Dict[str, Logable] であり，read メソッドの戻り値と同一です．

readf メソッドはセンサーのデータ値のみをリストとして返すメソッドです．
戻り値の型は List[Logable] です．

read メソッドはセンサーのデータ名をキー，データ値を値とする辞書を返すメソッドです．
戻り値の方は Dict[str, Logable] です．

readf メソッドと read メソッドは引数として可変長のデータ名を受け付けます．
この引数に DATA_NAMES で定義されているデータ名を渡すと，取得するデータ名を制限できます．
ただし，必要な引数のみを指定したからと言って，データ取得速度が向上するとは限りません．
これは I2C 通信などでは Boost Read の機能により，一度に全てのデータを取得するほうが
高速になる場合があるからです．
この性質を利用して，引数を指定しデータ取得数を制限させた場合でも，
全てのデータを取得し必要なデータのみを戻り値として返すように実装されているセンサークラスもあります．

### ハンドラを用いて実装する方法

ハンドラは上述したようにある通信規格に則って電気信号処理を行うときに用いるコンポーネントです．
したがって，センサークラスを実装する際にハンドラを利用するタイミングは，
Raspberry Pi などのマスターデバイスからセンサーなどのスレーブデバイスに対して
何らかの通信を行う場合のみです．

ほとんどのセンサーは，内部のレジスタのビット情報を読み込むか書き込むかで機能します．
したがって，多くのハンドラは **read** メソッドと **write** メソッドを持っています，
ただし，どのような方式でビットの読み書きを行うかは通信規格に依るので，
センサーのデータシートを参照する必要があります．

今回は **I2C** と呼ばれる，比較的クロック周波数の低い通信規格を取り上げることにします．
I2C の欠点はシリアルクロック周波数が低く，それにより通信速度（bps）が低いことにありますが，
並列に100個以上のデバイスを接続することができる点が利点です．

I2C を扱うためのハンドラのインターフェースは **I2CHandlerBase** で定義されています．
主なメソッドは以下の通りです：

- close() -> None
- read(reg: int, count: int) -> Tuple[int, bytearray]
- write(reg: int, data: Union[bytes, bytearray]) -> None

**close** は I2C 通信を終了するためのメソッドです．

**read** はレジスタの状態を読み取るためのメソッドです．
引数 *reg* はデバイスのレジスタのアドレスを指します．
レジスタのアドレスはセンサーのデータシートに記載されているものを用いなければなりません．
引数 *count* は読み取る byte 数を受け付けます．
通常1つのレジスタには1 byte (8 bits) のデータが格納されているので，
本来は *count* の値は常に1になるはずなのですが，
1より大きな値を *count* に与えると *reg* に指定したレジスタから順番に
*count* バイト取得します．
例えば *reg* に 0x10 と指定し，*count* に8を指定すると，
0x10 ~ 0x17 のレジスタの値を取得することになります．
連番のレジスタの値を一気に取得する必要がある場合は，
*count* に1を指定し順に取得するより，このように一度に取得するほうが性能は良くなります．

**write** はレジスタの状態を書き換えるためのメソッドです．
引数 *reg* はデバイスのレジスタのアドレスを指します．
引数 *data* は書き込むビット列（通常1バイト）です．
レジスタへの書き込み処理は基本的にはセンサーの設定値を変更するために利用します．
指定したレジスタへの書き込みが禁止されている場合もありますので，
あらかじめデータシートを参照し書き込み可能なレジスタにのみ書き込み操作を行います．

後は，これらのメソッドを駆使してセンサーのデータシートを見ながらセンサークラスを実装するだけです．
通常はセンサーのレジスタから取得したデータに何らかの処理を施しセンサー値とするので，
どのような処理をするべきかもデータシートから探し出す必要があります．

### レートについての注意点

レートとは割合を意味する言葉ですが，もっぱら単位時間に対する割合を指す場合が多いです．
センサーに関連するレートとしては，

- シリアルクロック周波数
- ボーレート
- 転送速度
- サンプリングレート

などがあります．
これらはそれぞれ異なる意味を持つレートなので注意が必要です．

一方で，ユーザーの関心のほとんどはサンプリングレートにあることでしょう．
つまり，1秒間にどれほどセンサー値を取得できるかということです．
一般的に同じセンサーにおいて，上述したレートの中で最もレートが低いものはサンプリングレートです．
なぜなら，センサー値を取得するためには通信を行い，データを取得し，計算するという
手間があり，上述した3つのレートはそれらに大きく関わるレートであるからです．
計算するという操作を考えると，当然コンピューターの CPU のクロック周波数も依存してきます．
そして，一度に取得するデータが多いほど時間的なコストが大きくなるため
サンプリングレートは低下します．

サンプリングレートを向上させるには上記のような問題点を熟知しておく必要があります．
方法としては，根本的なレートの向上を図る方法とコストを分散する方法が考えられます．

根本的なレートとは，上述したレートのうちシリアルクロック周波数やボーレートのことを指します．
これらのレートを向上させることで多くの場合，転送速度（bps）は向上されることが期待されます．
bps が向上すればその分サンプリングレートも向上するわけです．
また，根本的なレートには CPU クロック周波数も含まれるでしょう．
bps が等しい場合，計算速度が速いことはセンサー値の算出速度が速いことを意味し，
結果的にサンプリングレートは向上することが期待できるからです．
この方法は垂直スケールによってサンプリングレート向上させようという方法と言えます．

コストを分散する方法とは，特に時間的なコストを計算リソースを最大限に活かす形で分散する方法です．
例えば，コア数の多い CPU を採用し複数のコアでデータの取得を行う方法などが考えられます．
そうすれば1つのコアに対するコストを分散できます．
あるいは，IO バウンドが大きいと判明した場合は，マルチスレッドで複数のセンサーを扱うなどの
手段も考えられます（この場合 asyncio を用いた非同期処理はお勧めしません）．
ただし，複数のセンサー値を同期的に扱い場合（つまり同一の時間変数を用いたい場合）などは，
これらの操作には注意が必要です．
なぜなら，基本的にこのような水平スケールは非同期的にタスクを処理するからです．

### 既存の具象クラスをラップする方法

センサークラスを最も簡単に作成する方法は，もともと誰かの手によって完成されている
クラスを用いて， SensorBase を継承する形でそのクラスをラップすることです．

例として，とある温度センサーを扱うための TempSensor というクラスが既に誰かの手によって
実装されているとしましょう．
ただし，この TempSensor は SensorBase を継承しておらず，pisat システムにおける
センサーとは呼べません．
pisat システムにおいてセンサーと呼べるようになるには，SensorBase を継承し，
上述した4つの変数・メソッドを実装する必要があります．
そこで，内部で TempSensor オブジェクトを使用する SensorBase を継承した 
TempSensorX というクラスを作成することにしましょう．

まず，TempSensor は以下のメソッドを持っているとします：

- read_temp() -> float

そして，この read_temp メソッドは float 型で温度のセンサー値を返すものとします．

さて，それでは TempSensorX を実装していきます．
上述した SensorBase の4つの変数・メソッドをどのように実装しているかに着目してください．

```python
from typing import Dict, Optional, Tuple, List

from pisat.config.type import Logable
import pisat.config.dname as dname
from pisat.sensor import SensorBase

from temp_sensor import TempSensor

class TempSensorX(SensorBase):

    DATA_NAMES: Tuple[str] = (dname.TEMPERATURE,)
    DEFAULT_VALUES: Dict[str, Logable] = {dname.TEMPERATURE: 20.}

    def __init__(self, debug: bool = True, name: Optional[str] = None):
        # 今回はハンドラは用いないから None を指定
        super().__init__(handler=None, debug=debug, name=name)

        self._sensor: TempSensor = TempSensor()

    def readf(self, *dnames: Tuple[str, ...]) -> List[Logable]:
        # debug 機能を使う場合は必要
        debugging = super().readf(*dnames)
        if debugging:
            return debugging

        # 内部で TempSensor.read_temp を使う
        if len(dnames) == 0:
            return [self._sensor.read_temp()]
        else:
            result = []
            for name in dnames:
                if name == dname.TEMPERATURE:
                    result.append(self._sensor.read_temp())

            return result

    def read(self, *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        # debug 機能を使う場合は必要
        debugging = super().readf(*dnames)
        if debugging:
            return debugging

        # 内部で TempSensor.read_temp を使う
        if len(dnames) == 0:
            return {dname.TEMPERATURE: self._sensor.read_temp()}
        else:
            result = {}
            for name in dnames:
                if name == dname.TEMPERATURE:
                    result[dname.TEMPERATURE] = self._sensor.read_temp()

            return result

```

このように実装することで pisat システムで動作可能なセンサークラスにすることができます．
また，今回の場合はハンドラを全く用いていません．
それは，TempSensor が既にセンサー値を出力する能力を持っているためです．

既存のクラスをラップする方法は，手頃にセンサークラスを作成できる反面，
パフォーマンスに問題が生じる場合があります．
まず，上記のようにラップしている時点でセンサー値の取得までにいくつかの
手間が加わってしまっています．
それに加え，利用するクラスそのものがセンサーのパフォーマンスを
十分に発揮できるように設計されていない可能性もあり，
その場合の修復は困難であることがあります．
もし pisat.sensor サブパッケージに利用したいセンサーが存在する場合は，
そちらの利用を検討することをお勧めします．


## その他のハードウェアのソフトウェア的な実装

ここまで，ハードウェアの代表例としてセンサーを取り扱っていましたが，
利用可能なハードウェアはまだまだあります．
よく使うハードウェアには以下のようなものがあります．

- DC モーター
- サーボモーター
- 無線モジュール
- スイッチ
- LED

これらのハードウェアは全てハンドラを用いて実装可能です．
pisat システムで利用したい場合は，いくつかの用意されている基底クラスを
継承し実装する必要があります．
その主な目的は，インターフェースを統一し，システムが共通の動作を行うことを
可能にするためです．
システムに操作を委ねることでユーザーの負担を大幅に減少させることができ，
再利用性も向上します．

例えば，DC モーターを実装したい場合は pisat.actuator に用意されている
MotorBase などを継承し実装することになります．
当然，利用したいコンポーネントが既に pisat に用意されているならば，
すぐにそれを利用することが出来ます．

### 今後の展望

現時点ではハードウェア実装を行っているサブパッケージは以下のとおりです：

- pisat.actuator
- pisat.comm
- pisat.sensor

今後はハードウェアの性質に合わせて追加のサブパッケージが登場する可能性があります．

pisat では様々なアイディアを受け付けています．
議論がある場合は Issue までお願いします．


## まとめ

今回のドキュメントではコンポーネントを独自に定義する方法を紹介しました．
特に，

- Component を直接継承する方法
- ハンドラを用いてハードウェアを実装する方法
- 既存のクラスをラップする方法

を取り上げ，ハードウェア実装についてはセンサーの実装を例として挙げました．

[次回のドキュメント](pisat_example.md)では，ここまで説明してきた内容を
復習しつつ，pisat を利用したミッションの構築を学びます．
簡単なミッションの例を通して，ミッションの構想を pisat フレームワークを用いて
いかに実装するかを学びます．
