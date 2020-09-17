# 独自の拡張について

## コンポーネントの実装について

残念なことに，コンポーネントを実装することは極めて面倒な作業です．
特にハードウェア (デバイス) の実装の場合はデバイスドライバの実装と似ています．
デバイスの実装の場合は，そのデバイスのデータシートを熟読して，基本的にはそのデータシートを再現することを目指す必要があります
(これがコンポーネントの実装が面倒である最大の理由です)．
一方，pisat にはハードウェアが実在していないようなソフトウェア的な部品もコンポーネントに分類されている場合があります．
代表例は pisat.calculate サブパッケージに含まれる Adapter と呼ばれるコンポーネントです．
Adapter はデータを受け取り，特定の計算をしてその結果を返すというコンポーネントです．
感覚的には「計算」という操作を担当する部品です．
このようなハードウェアの実体が存在しないコンポーネントはデータシートなどを参照する必要はありません．

デバイスの実装としてのコンポーネントは，デバイス自体が多種多様であるためコンポーネントも多種多様にならざるを得ません．
Adapter などの仮想的なコンポーネントも，やはり用途は様々であるためコンポーネントの種類も多くなります．
その一方で，pisat システムではコンポーネントの依存性を極めて小さなものにすることを目指しています．
この解決策の一つとして，コンポーネントに基底クラスを作り，全ての利用可能なコンポーネントは
その基底クラスを継承したものであるという規則が作られています ([最初のドキュメント](./pkg_overview.md)を参照) ．
したがって，コンポーネントを実装する際は必ずこの規則を守って実装する必要があります．

具体例を1つ示しましょう．
以下のコードは pisat.sensor.sensor.SensorBase の実装です．
SensorBase クラスは全てのセンサークラスの基底クラスです
(詳細は [pisat.sensor のドキュメント](../../sensor/)を参照してください)．

```Python
class SensorBase(SensorInterface):

    SENSOR_NAME: str = ""
    DATA_NAMES: tuple = ()
    DEFAULT_VALUES: Dict[str, Logable] = {}

    def __init__(self, handler: Optional[HandlerBase] = None, debug: bool = False) -> None:
        self._handler: Optional[HandlerBase] = handler
        self._debug: bool = debug

        if not (self._handler or self._debug):
            raise HandlerMismatchError(
                "Not set a Handler object. Set one unless you meant to debug.")

    def __str__(self) -> str:
        return self.SENSOR_NAME

    def __add__(self, sensor):
        return SensorGroup(self, sensor)

    def __iadd__(self, sensor):
        return self.__add__(self, sensor)

    @property
    def dnames(self) -> Tuple[str]:
        return self.DATA_NAMES

    def readf(self, *dnames) -> List[Logable]:
        if self._debug:
            if len(dnames) == 0:
                return [val for val in self.DEFAULT_VALUES.values()]
            else:
                return [self.DEFAULT_VALUES[dname] for dname in dnames]
        else:
            pass

    def read(self, *dnames) -> Dict[str, Logable]:
        if self._debug:
            if len(dnames) == 0:
                return self.DEFAULT_VALUES
            else:
                return {dname: self.DEFAULT_VALUES[dname] for dname in dnames}
        else:
            pass
```

この基底クラスでオーバーライドすべきメソッドや変数は

* \_\_init\_\_()
* readf()
* read()
* SENSOR_NAME
* DATA_NAMES
* DEFAULT_VALUES

の6つです (これは今後変更されるかもしれません) ．
各メソッドはインターフェースは統一されており，各変数も型が具体的に決まっています．
pisat システムを潤滑に動かすためには，このような規則は遵守する必要があります．
ちなみに上記の6つのメソッドと変数以外の属性はオーバーライドしてはなりません．
また，メソッドや変数を新たに追加することは全く問題ありません．

この SensorBase を継承して実際のコンポーネントであるセンサークラスを作成する方法は難しくはありません
(ただし，ハードウェアの知識とデータシートを読み解く力は必要です)．
まず3つのオーバーライドすべき変数はすぐに実装できるはずです．
これらはクラス変数として実装されることになっています．
残りの3つのメソッドはデバイスによって多少実装が異なるかもしれません．
ですが，インターフェースさえ正しければどの方法で実装しようと pisat システム的には OK です．
この3つのメソッドの実装は記述するべき処理が膨大になる可能性もあるので，
新たにメソッドや変数を追加するなどして，手順を小分けにすると見通しが立ちやすいです．

コンポーネントを実装する際には，必ず各コンポーネントのドキュメントを参照するようにしてください．
コンポーネントはサブパッケージごとに分類されているため，
pisat パッケージに実装したいコンポーネントの種類に該当するサブパッケージがあるはずです
(なければ pisat システムがサポートしていないコンポーネントということになります)．
それらのサブパッケージは独自のサブシステムを形成していることもあり，
その場合はそのサブシステムに則ったコンポーネントを作る必要があります．
このような理由から，コンポーネントを実装する際には，まず該当するサブパッケージのドキュメントを参照し，
サブシステムの理解を深める必要があります．
また，サブパッケージのドキュメントにはコンポーネントの実装のヒントなどもあるため，
そちらを参考にすると実装の見通しが立つでしょう．