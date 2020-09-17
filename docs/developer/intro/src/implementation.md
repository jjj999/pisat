# pisat を利用した実装について

このドキュメントは

- [pisat のサブパッケージについて](pkg_overview.md)
- [pisat システムについて](system.md)

を読んだことを前提としています．

## ミッション設計の流れ

pisat フレームワークを用いたミッションの設計に不可欠な要素は

- コンポーネント
- Node
- Context

の3つです．

コンポーネントとは Component クラスを継承したサブクラスの総称で，
言わばミッションで利用する部品のことであり，
代表的なものとしてはセンサーやモーターなどがあります．
コンポーネントを利用する際には，まずそのコンポーネントが pisat に
含まれているかどうかを確認してみましょう．
コンポーネントが含まれていれば，そのままそのコンポーネントを利用できます．
もしコンポーネントが pisat に含まれていなければ，他人が作ったコンポーネントを探すか，
自分自身でコンポーネントを作る必要があります．
コンポーネントを作る際は，基本的にはそのコンポーネントに該当する基底クラスを継承します
（その基底クラスは Component クラスを継承しています）．
該当する基底クラスがない場合は直接 Component クラスを継承し実装することで
コンポーネントとして機能します．

Node と Context の必要性は[前回のドキュメント](system.md)で述べた通りです．
まずは，設計するミッションに必要な Node をリストアップし，
それらの関係をグラフで表し，その内容を Context に反映させる必要があります．
その後，Node を実装することでミッションの中身を埋めていきます．

上記の内容を簡潔にまとめると，

1. コンポーネントを探す（見つからなければ実装）
2. Node の関係を決めて Context に渡す
3. Node を実装

となります．
これらは，

1. なにを使って（What）
2. どのタイミングで（When）
3. どのような処理を（How）

というミッションの3つの要素を反映させたものです．

以下では，利用するコンポーネントが全て揃っている状態を仮定します．
また，Context オブジェクトにミッションフローを設定する方法は
[前回のドキュメント](system.md)で説明しました．
したがって，以下では上述の3つの要素のうち，3番目の Node を実装することについて
説明します．
コンポーネントの独自実装については[次回のドキュメント](self_expansion.md)
を参照してください．


## Node 実装のポイント

Node の実装を行う際は，[前回のドキュメント](system.md)で述べた Node の
ライフサイクルを意識することが重要です．
ライフサイクルを意識しながら適切なコールバックを実装することで，
ミッションの状態としての Node を柔軟に表現できます．

ミッションが Node によって小分けされている最大の利点は，
その Node で記述すべき処理にフォーカス出来る点にあります．
ユーザーはその Node で考慮すべき事柄だけに集中すればよく，
それ以外のことは頭の中から排除できます．

また，実装した Node クラスは実行時に pisat システムによって
そのオブジェクトが生成され，その Node から抜け出すとそのオブジェクトは
破棄されるという点に注意が必要です．
つまり，ある Node のインスタンス変数やインスタンスメソッドを
他の Node から参照することは出来ません．
もし，複数の Node から参照可能なオブジェクトを作成したい場合は，
コンポーネントとして実装し，ComponentManager を介して 
Node 内でオブジェクトを取得する必要があります．


## Node 内でのコンポーネントの参照

Node 内でコンポーネントを使用する際には，ComponentManager を介して
コンポーネントを取得する方法が一般的です．
ComponentManager は Node.manager で参照可能です．
ComponentManager を用いてコンポーネントを取得する場合は，
ComponentManager.get_component メソッドを用います:

```python
from pisat.core.nav import Node

class TestNode(Node):

    def enter(self):
        self.motor = self.manager.get_component("motor")
```

上記の例では，ComponentManager を介して「motor」というコンポーネント名の
コンポーネントを取得しています．
コンポーネントを取得するのは基本的にはどのコールバックメソッド内でも可能ですが，
一番最初に実行される enter コールバック内で取得するのが一般的です．
上記の例のように，インスタンス変数として取得してしまえば，
judge, control といったコールバックメソッド内でも利用できるからです．

### Component クラス

Component クラスはコンポーネントの共通インターフェース定義するクラスです．
コンポーネントは全て Component クラスのサブクラスのオブジェクトです．

Component クラスのコンストラクタには name という引数があります．
この name 引数に文字列を渡すことでコンポーネントの名前を設定できます．
コンポーネントの名前はコンポーネントの識別子であり，
ComponentManager はこのコンポーネントの名前をもとにコンポーネントを検索します．
したがって，コンポーネント名は重複してはなりません．

name 引数はオプション引数でデフォルトは None です．
この場合，コンポーネント名はクラス名と同一になります．
これは，同一のコンポーネントのオブジェクトが複数存在する場合には重複するため，
明示的に name 引数を指定する必要があります．

コンポーネント名は Component.name プロパティで参照可能です．

### ComponentManager.append

ComponentManager にもセットアップ作業は必要です．
ComponentManager は Component のサブクラスである ComponentGroup というクラスの
サブクラスとして実装されており，内部にコンポーネントを保持できるコンポーネントです．
ComponentManager.get_component を用いたコンポーネントの取得は，
ComponentManager 内部のコンポーネントの中から検索し，その結果を返しています．
したがって，ComponentManager 内部にコンポーネントが存在しない場合は
コンポーネントの取得は出来ません．

上記のような理由から，ComponentManager を利用する際にはまず Component を
登録してあげる必要があります．
その際に用いるメソッドが ComponentMangager.append メソッドです．
このメソッドは任意個のコンポーネントを引数として受け付け，
ComponentManager 内部に登録します．

```python
from pisat.core.manager import ComponentManager

manager = ComponentManager()
manager.append(component1, component2, component3)
```

また，ComponentManager.append メソッドは recursive という bool 型の
オプション引数を持っており，デフォルトは False です．
この recursive を True にすると，ComponentManager に
コンポーネントグループが登録された場合に，そのコンポーネントグループ内部に
登録されているコンポーネントをくまなく探し登録するという動作をします．
コンポーネントグループを登録しない場合は意味はありません．

```python
# com_group には component1, component2, component3 が
# 登録されているとする．
manager = ComponentManager()
manager.append(com_group, recursive=True)

# 内部のコンポーネントの名前を列挙
print(manager.list())
# >> (com_group, component1, component2, component3)
```

### ComponentMangager を使う理由

Node 内でグローバルな変数を参照しても ComponentManager を利用する際と
あまり大差はありません．
ただし，今後のアップデートなどによりコンポーネントを Python スクリプト上で
明示的にインスタンス化しないアーキテクチャ（設定ファイル読み込みなど）も
想定されており，その場合はそもそもコンポーネントがグローバルな変数とはなりません．

また，グローバル変数を用いること自体が大規模なソフトウェアでは
アンチパターンになりえます．
名前空間については可能な限り小規模にすることがベストプラクティスとされており，
コンポーネントが main 関数内などで初期化された場合などは，グローバルに参照不可能です．

一方で ComponentManager は CanSat オブジェクトによって Node 初期化時に
Node に渡されるので，上記のような問題を回避できます．
その代わり，現時点ではコンポーネント名を識別子として利用するため，
コンポーネント名は参照可能な形で定義されている必要があります．


## Node.judge の実装

Node.judge は Node の知覚部です．
DataLogger が CanSat オブジェクトに設定されている場合，
Node.judge コールバックの引数には，このコールバックが呼び出される度に
DataLogger によって取得された最新のデータが渡されます：

```python
from typing import Dict, Any

from pisat.config.type import Logable
from pisat.core.nav import Node

class TestNode(Node):

    def judge(self, data: Dict[str, Logable]) -> Any:
        print(data)
        # >> {"data_name": (data_value), ...}
```

もし，DataLogger が設定されていない場合，または
Node.is_feed クラス変数が False の場合は空の辞書が渡されます：

```python
class TestNode(Node):
    is_feed = False

    def judge(self, data: Dict[str, Logable]) -> Any:
        print(data)
        # >> {}
```

DataLogger が設定されていない場合と Node.is_feed が False の場合の違いは，
DataLogger が設定されていない場合はミッションを通して全ての Node の
judge コールバックに空の辞書が渡されるのに対し，
ある Node で is_feed を False にした場合はその Node 内でしか
その設定が有効にならない点にあります．
また，is_feed が False の場合はそもそもデータのロギング自体を行いません．

Node.judge の役目は引数に渡される data 内のデータを適切に処理し，
状態遷移をするか否かを決定するフラグ値を戻り値として返すことにあります．
例えば Context が以下のように設定されているとします：

```python
from pisat.core.nav import Context

context = Context({
    TestNode1: {True: TestNode2, False: TestNode1},
    TestNode2: {True: None, False: TestNode2}
})
```

このとき，TestNode1 の簡単な例は以下のようになります：

```python
from typing import Dict

from pisat.config.type import Logable
import pisat.config.dname as dname
from pisat.core.nav import Node

class TestNode1(Node):

    def judge(self, data: Dict[str, Logable]) -> bool:
        press = data.get(dname.PRESSURE)

        if press is not None:
            if press > 1000.:
                return True

        return False
```

上記の例では TestNode1 の行き先が TestNode2 か自分自身しかなかったため，
bool 型の戻り値にしましたが，Node.judge の戻り値の型は特に定まっておらず，
必要ならばどのようなオブジェクトでも使用可能です．

上記の例は非常に簡単な例であり，一度でもしきい値（今回は1000）を超えてしまうと
TestNode2 へと遷移してしまいます．
そこで，よりロバストな実装に書き換えてみましょう．

```python
class TestNode1(Node):

    def enter(self):
        self.count = 0

    def judge(self, data: Dict[str, Logable]) -> bool:
        press = data.get(dname.PRESSURE)

        if press is not None:
            if press > 1000.:
                self.count += 1
            else:
                self.count = 0

        if self.count >= 5:
            return True
        else:
            return False
```

これで5回連続で press の値が1000を超えなければ，状態遷移をしないようになりました．
このように Node.enter と連携して使用することで，様々な判定方法を実装できます．

### DataLogger

DataLogger クラスは pisat.core.logger で定義されているクラスの1つです．
このクラスはデータロガーを抽象化したクラスで，
DataLogger.read メソッドを実行すると，登録されているセンサーから
データを取得，登録されているアダプターのデータを渡し計算，
それらのデータをバッファに格納，バッファがたまったらファイルに書き込み，
というデータロガーとして機能を同時に引き受けます．
ただし，それらの機能は DataLogger で実装されているのではなく，
SensorController，LogQueue などで実装されているものです．
つまり，DataLogger はそれらのクラスの機能を複合したクラスです．

ユーザーはデータの読み込み処理などの設定をこの DataLogger クラスを
使用して設定できます（機能自体は SensorGroup，AdapterGroup に由来します）．
このデータ読み込み設定を **readability** と呼んでいます．
readability とは，例えば DataLogger.ignore にデータ名を渡せば，
そのデータ名のデータを取得しないようにしたり，
逆に DataLogger.reset_all を用いれば無視したデータを再度取得するように
設定することもできます．

このような readability の設定は Node.enter コールバック内で行うことが一般的です．
また，readability に関するバグを防ぐために，exit で全ての readability 
をリセットしておくと良いでしょう：

```python
import pisat.config.dname as dname
from pisat.core.nav import Node

class TestNode(Node):

    def enter(self):
        dlogger = self.manager.get_component("DataLogger")

        # ignore retreiving data named 'PRESSURE'
        dlogger.ignore(dname.PRESSURE)

    def judge(self, data):
        press = data.get(dname.PRESSURE)
        print(press)
        # >> None

    def exit(self):
        # reset all readabilities
        dlogger.reset_all()
```

DataLogger の詳細は [pisat.core のドキュメント](../core/)を参照してください．

### Logable

Logable は pisat.config.type モジュール内で定義されている型エイリアスです．
具体的な定義は以下のようになっています：

```python
from typing import Union

# Logable means this type of object can be logged by DataLogger.
# A subject to be logged and saved into a log file must be
# Logable type.
Logable = Union[int, float, str]
```

Logable 型はセンサーやアダプターでデータとして許容される型です．
Logable ではないデータ型をセンサーやアダプターで使用すると，
データロギング中のファイル書き込み操作などでエラーが発生する可能性があります．


## Node.control の実装

Node.control は Node の制御部です．
このコールバックは Main スレッドが起動した別のスレッド
（Control スレッドと呼んでいます）で実行されます．
このコールバックは judge コールバックで状態を監視している傍らで，
ブロッキングを受けず実行されるサブルーチンです．

このコールバックの実装で最も注意すべき点は，
マルチスレッド由来のバグが発生しないように実装を行わなければならないという点です．
最もやってはいけないことは，DataLogger オブジェクトなどの
Main スレッド内で常時利用されているオブジェクトを利用することです．
この対策として，以下のようなロック機構を備えたクラスが定義されています：

- pisat.core.logger.RefQueue
- pisat.core.nav.PostEvent

### RefQueue

RefQueue はロック機構を備えた小さなコンテナです．
DataLogger が取得したデータの最新の少量のデータを内部に保持しています．
RefQueue は DataLogger に結び付いているため，RefQueue の取得は 
DataLogger を経由して行います．
DataLogger に結び付いた RefQueue から取得できるデータは常に
最新であることが保証されます．

RefQueue を用いてデータを取得する方法を以下に示します．

```python
from typing import Deque, Dict

from pisat.config.type import Logable
from pisat.core.nav import Node

class TestNode(Node):

    def enter(self):
        dlogger = self.manager.get_component("DataLogger")
        self.refque = dlogger.refqueue

    def control(self):
        # ロックして内部のデータの deep copy を返す
        data: Deque[Dict[str, Logable]] = self.ref.get()
```

### PostEvent

PostEvent は [threading.Event](https://docs.python.org/ja/3/library/threading.html) 
クラスを継承したサブクラスで，基本的には Event オブジェクトのように振舞います．
したがって，基本的な利用目的は Event オブジェクトと同一ですが，
PostEvent は package プロパティを持つ点が異なります．
package プロパティは初期化時には None ですが，
set メソッドの第1引数にオブジェクトを渡すと，そのオブジェクトを返します．
これは Event の set メソッドに複数スレッドから参照可能なオブジェクトを渡せるように
しただけです．
pisat システムはこの set メソッドを用いて，PostEvent オブジェクトの
package にフラグ値を渡します．
これにより，Control スレッドではイベントの発生とともに，
どのようなフラグ値が judge によって返されたかを知ることが出来ます．
PostEvent オブジェクトは Node.event インスタンス変数から参照可能です．

PostEvent の使用例を以下に示します．

```python
from typing import Deque, Dict
from time import sleep

from pisat.config.type import Logable
import pisat.config.dname as dname
from pisat.core.nav import Node

class TestNode(Node):

    def enter(self):
        self.motor = self.manager.get_component("motor")

    # 0 --> more        --> judge will be called again
    # 1 --> good        --> set event
    # 2 --> too close   --> set event
    def judge(self, data: Dict[str, Logable]) -> int:
        distance = data.get(dname.DISTANCE)
        if distance is None:
            return 0

        if distance < 10.:
            return 2
        elif distance < 50.:
            return 1
        else:
            return 0

    def control(self):
        while self.event.is_set():
            # move forward
            self.motor.cw(100)
            sleep(0.5)

        flag = self.event.package
        # flag will not be 0.
        if flag == 1:
            pass
        elif flag == 2:
            # step back
            self.motor.ccw(50)
            sleep(1)
            
        self.motor.brake()
```


## まとめ

今回のドキュメントでは Node のサブクラスの具体的な実装の方針を述べました．
Node の各コールバックがどのタイミングで呼び出されるかは，
pisat.core.cansat.CanSat クラスで定義されているので，
興味がある場合は参照してみるとより理解が深まるでしょう．

今回のドキュメントでは上記の内容とともに pisat システムでよく利用される
いくつかのコンポーネントについても説明しました．
まずはどのようなコンポーネントがあるのか，そしてそのコンポーネントが
どのような役割を持つのかを理解することで，そのコンポーネントの適切な使い方を
理解できることでしょう．

Node の実装はミッション実装の大部分を占める作業であり，
Node の実装の完成度がミッションの完成度とも言えます．
特にマルチスレッドで動作する judge，control コールバックの実装に
気を配りながら，自分の手で Node を実装してみると良いでしょう．

[次回のドキュメント](self_expansion.md)ではコンポーネントの独自定義に
焦点を当て説明します．
