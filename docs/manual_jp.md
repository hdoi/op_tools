---
title: "op_tools ver 0.1.5 ユーザーマニュアル"
date: "March 2022"
author: "土居　英男 (doi.hideo.chemistry@gmail.com)"
---

\newpage

# これは何？

分子シミュレーションや粒子のシミュレーションにおける結晶構造を解析するためのpythonモジュールである。  
個々の粒子や原子の周囲の環境を評価し、ある数値に変換する。
この数値はlオーダーパラメータ (秩序変数, order parameter) とも呼ばれる。
似通った並び方の粒子は同じ数値になり、違った並び方をしている粒子は違う数値になる。
例えば、体心立方格子 (body-centered cubic, BCC) や 面心立法格子 (face-centered cubic, FCC) は数値が知られており、
どこが結晶で、どこがそうでないかを見分ける事が可能です。
このような解析は、固体金属を融解させるようなシミュレーションや、結晶構造の粒界を調べるシミュレーションなどで使われる。
オーダーパラメータの性能は、低い計算コスト、分類能力など評価される。

# インストール

所定のサイトからパッケージをダウンロードし、次のコマンドを実行してください。
```
$ cd order_tools  
$ pip3 install -e .  
```

# 必要なデータ
  1. coord                     : 各粒子の座標のリスト。  次のような。[ [0,0,0], [0,0,1], ... ]  
    [[x1, y1, z1], [x2, y2, z2], ... ] というような順番になっている。
  2. direct                    : 各粒子の方向ベクトル。3次元の単位ベクトルでも、四元数でも良い。次のような。[ [1,0,0], ... ] か [ [1,0,0,0] ,.... ]
    3次元の単位ベクトルの場合は、[x, y, z] の順番になっている。四元数の場合は、 [w, x, y, z]の順番になっている。
    質点や球状粒子の場合、方向ベクトルが存在しない。その場合は、direct = [] として問題ない。
  3. box_length                : シミュレーションボックスの長さ。 [ 3, 3, 3] xyzの順番になっている。
  4. op_settings : 各order parameter を計算するための設定


# すべてのオーダーパラメータで共通の設定

## 隣接粒子の設定

各粒子のオーダーパラメータの数値は近くに存在する粒子の座標を使用して計算される。
このある粒子 $i$ の近くにある粒子のことを、ある粒子の隣接粒子と呼ぶ。
隣接粒子の決める方法は2つある。  

一つめの方法は、粒子$i$からの距離がある距離 (隣接半径) 以内にある粒子を、粒子$i$の隣接粒子とする方法である。
この方法の利点は、実装が比較的簡単でユーザーにとってもわかりやすいと思われるところである。
欠点としては、隣接粒子の個数が各粒子で違う場合がある事と、距離の単位によって隣接粒子数が変わる事である。
例えば、隣接半径を 1 nm と1 angstrom と指定するのでは結果が変わる事である。このことをスケール依存性という。
二つ目の方法は、粒子$i$から距離の近い$n$個の粒子を隣接粒子とする方法である。
利点としては、スケール依存性がなく、長さの単位が変わっても距離の大小関係が変わらないため、隣接粒子が変化しない。
欠点としては、実装が比較的難しい、計算コストが大きい（数割程度）、論文での使用実績が存在するが少ない、という点である。
三つ目の方法は Delaunay分割 (Voronoi分割)を使う方法です。

各方法の使用法は、以下の通りである。

###  隣接半径を指定する場合

オーダーパラメータの計算条件を指定する op_settings で次のように指定を行う。
```
  op_settings = {
    'radius' : [1.5, 1.75] ,  
    ... ( 各オーダーパラメータの設定 ) }
```
list形式で指定することが可能で、複数の条件を一度に指定する事も可能である。
上の例では、距離 1.5 と 距離 1.75 での指定を行っている。  

###  隣接粒子の数を指定する場合

オーダーパラメータの計算条件を指定する op_settings で次のように指定を行う。
```
  op_settings = {
    'neighbor' : [8, 12] ,  
    ... ( 各オーダーパラメータの設定 ) }
```
list形式で指定することが可能で、複数の条件を一度に指定する事も可能である。
上の例では、隣接粒子数8 と 12 の指定を行っている。  

### Defaunay分割を行う場合

オーダーパラメータの計算条件を指定する op_settings で次のように指定を行う。
```
  op_settings = {
    'Delaunay': ['standard']
    ... ( 各オーダーパラメータの設定 ) }
```


## 隣接粒子で平均化を行う回数の設定

各粒子のオーダーパラメータの分類性能が低い場合は、以下の様な平均の計算を行う。
粒子$i$のオーダーパラメータと粒子$i$の隣接粒子のオーダーパラメータで平均を計算する場合がある。
粒子$i$の$N$個の隣接粒子のlistを$N_b(i)$、
$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のlistを $\tilde{N}_b(i)$とすると、
粒子$i$の平均化を行う前のオーダーパラメータを$X(i)$,平均化した後のオーダーパラメータを$Y(i)$とすると、次の様な計算を行う。
$$Y(i) = \frac{ \sum_{j \in \tilde{N}_b(i)}X(j)}{N+1}$$ 

この平均化の操作は以下の利点と欠点を持っている。
利点としては、平均を計算するだけであるため計算負荷が軽い事、同じオーダーパラメータの分類性能を上げる事が可能である事、
何らかの数値であれば使用できる事、何回も平均化をする事が可能である事、である。
一方、欠点としては、オーダーパラメータの計算に使用する情報が多くなり、オーダーパラメータの解像度が下がる事である。
オーダーパラメータは隣接粒子の情報を使って計算され、さらに平均化の計算では隣接粒子のオーダーパラメータを使って計算される。
平均化操作を1回行うごとに、隣接粒子の隣接粒子の情報を使用することになる。
つまり、オーダーパラメータの計算に使用する粒子が多くなり、遠くの粒子の情報を使用することになる。
これは、均一な系ではあまり問題にはならないが、不均一な系（界面など）では問題になる。
不均一な系では、異常が起こっている位置が知りたいであるとか、界面の位置を知りたいなどと言った目的で使用される場合が多いと思われるが、
遠くの粒子の情報を使用すると、位置がはっきりとはわからなくなる。

この平均化を行う回数は、オーダーパラメータの計算条件を指定する op_settings で次のように指定を行う。
なお、この値は、0 から始まり、0の場合は、平均化を行わない。

```
  op_settings = {
    'ave_times'      : 1, 
    ... ( 各オーダーパラメータの設定 )
     }
```

# 各オーダーパラメータの説明

## $S$ : Onsager's parameter

Onsagerのオーダーパラメータ $S$ は次の式で計算される。[@Onsager1949][@Zannoni1979]

$$ S^{(a=0,n)}(i) = \frac{ \sum_{j \in N_b(i)} {P_n(\cos( \theta ))} }{N}, n even.$$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
関数$P_n$は[Legendre polynomial](https://en.wikipedia.org/wiki/Legendre_polynomials)である。変数$n$はDegree of the polynomialである。
変数$\theta$は、粒子$i$の持つ方向ベクトル${\boldsymbol u}(i)$と粒子$j$の持つ方向ベクトル${\boldsymbol u}(j)$との角度である。
変数$\cos(\theta)$は通常、${\boldsymbol u}(i) \cdot {\boldsymbol u}(j)$で計算される。

$n = 2, 4$の時、オーダーパラメータ $S$ はそれぞれ以下の式で計算される。
$$ S^{(a=0, n=2)}(i) = \frac{ \sum_{j \in N_b(i)} { [ 3 \cos^2(\theta) - 1]/2 } }{N} $$
$$ S^{(a=0, n=4)}(i) = \frac{ \sum_{j \in N_b(i)} { [ 35 \cos^4(\theta) -30 \cos^2(\theta) + 3  ]/8 } }{N} $$


隣接粒子数12、隣接半径2.0でのオーダーパラメータの設定として以下の例を示す。
尚、このオーダーパラメータは計算のために方向ベクトルが必須であるため、質点や球状粒子の解析に使う事はできない。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'n_in_S' : [2],
  'analysis_type' : ['S']
   }
```

## $T$ : McMillan's Sigma

McMillanのパラメータ$T$は次の式で計算される。[@McMillan1971]

$$ T^{(a=0,n)}(i) = \frac{ \sum_{j \in N_b(i)}{ \cos( 2 \pi z(i,j) / d ) P_n(\cos( \theta )) }   }{N}$$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
関数$P_n$は[Legendre polynomial](https://en.wikipedia.org/wiki/Legendre_polynomials)である。変数$n$はDegree of the polynomialである。
変数$\theta$は、粒子$i$の持つ方向ベクトル${\boldsymbol u}(i)$と粒子$j$の持つ方向ベクトル${\boldsymbol u}(j)$との角度である。
変数$\cos(\theta)$は、${\boldsymbol u}(i) \cdot {\boldsymbol u}(j)$で計算される。
変数$z(i,j)$は、ベクトル${\boldsymbol r}(i)$を通過し、ベクトル${\boldsymbol u}(i)$と垂直な平面$P$から、
ベクトル${\boldsymbol r}(j)$までの距離である。
変数$d$は、液晶のsmectic相の層から層までの距離である。

$n = 2$の時、オーダーパラメータ $T$ は以下の式で計算される。
$$ T^{(a=0,n=2)}(i) = \frac{ \sum_{j \in N_b(i)}{ \cos( 2 \pi z(i,j) / d ) [ 3 \cos^2(\theta) - 1 ]/2 }   }{N}$$

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。
尚、このオーダーパラメータは計算のために方向ベクトルが必須であるため、質点や球状粒子の解析に使う事はできない。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'n_in_T': [2],
  'd_in_T': [1.0],
  'analysis_type' : ['T']
   }
```

## $A$ : neighborhood parameters

common neighborhood parameter $A$ [@Honeycutt1987]、predominant common neighborhood parameter $P$ [@Radhi2017]、 another predominant common neighborhood parameter $N$ [@Radhi2017] は非常に似ている式で計算される。

$$ A^{(a=0,type=A,m)}(i) = A^{(a=0,m)}(i) = \frac{1}{N} \sum_{j \in N_b(i)} | \sum_{k \in N_b(i,j)} ( {\boldsymbol r}_{ik} + {\boldsymbol r}_{jk}) |^2 $$
$$ A^{(a=0,type=P,m)}(i) = P^{(a=0,m)}(i) = \frac{1}{N} \sum_{j \in N_b(i)} | \sum_{k \in N_b(i,j)} ( {\boldsymbol r}_{ij} + {\boldsymbol r}_{kj}) |^2 $$
$$ A^{(a=0,type=N,m)}(i) = N^{(a=0,m)}(i) = \frac{1}{N}|\sum_{j \in N_b(i)}   \sum_{k \in N_b(i,j)} ( {\boldsymbol r}_{ij} + {\boldsymbol r}_{kj} ) |^2 $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$N_b(i,j)$は粒子$i$,粒子$j$から近い$m$個の粒子のリストである。
変数$type$で計算を行うオーダーパラメータの種類を指定する変数である。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_param = {
  'neighbor': [12],
  'radius': [1.5],
  'ave_times': 1,
  'm_in_A': [2],
  'types_in_A': ['A', 'P', 'N'],
  'analysis_type': ['A']}
```

## $B$ : bond angle analysis (BAA)

bond angle analysis $B$は次の式で計算される。 [@Ackland2006]

$$ B^{(a=0,m,n,\phi)}(i) = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)  }f^{(m,n,\phi)}(\theta_{jik}) $$
$$ f^{(m,n,\phi)}(\theta_{jik}) = cos^{n} (m\theta_{jik} + \phi) $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\theta_{jik}$ベクトル${\boldsymbol r}_{ij}$とベクトル${\boldsymbol r}_{ik}$との角度である。
変数$m$は、角度の係数である。
変数$n$は、cos関数に使用する指数である。
変数$\phi$は、関数の補正のために角度である。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_param = {
  'neighbor': [12],
  'radius': [1.5],
  'ave_times': 1,
  'm_in_B': [2],
  'phi_in_B': [0],
  'n_in_B': [1, 2],
  'analysis_type': ['B']}
```

## $C$ : centrosymmetry parameter analysis (CPA)

centrosymmetry parameter $C$は次の式で計算される。[@Kelchner1998]

$$ C^{(a=0)}(i) = \sum_{j \in M_b(i)} | {\boldsymbol r}_{ij} + {\boldsymbol r}_{ik}|^2$$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$M_b(i)$は粒子$i$の最近接の$N/2$個の隣接粒子のリストである。

粒子$r_k$は、座標$r_j$を、座標$r_i$に関して反対側に移動した座標$r'_j$から一番近い位置にある$N_b(i)$リストにある粒子である。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_param = {
    'neighbor': [12],
    'radius': [2.0],
    'ave_times': 1,
    'analysis_type': ['C'] }
```

## $D$ : neighbor distance analysis (NDA)

neighbor distance analysis $D$のような秩序変数として以下のような秩序変数を実装した。[@Stukowski2012]
我々はovitoを使用してNDA解析を行うことを強く推奨する。
なぜなら、全く別物になってしまったため。

$$ D^{(a=0,f_{ij},f_{ik},f_{jk})}_i = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)} f_{ij}(r_{ij}) f_{ik}( r_{ik}) f_{jk}( r_{jk}) $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
関数$f_{ij}(r_{ij}), f_{ik}(r_{ik}), f_{jk}(r_{jk})$は、距離を引数とし、返り値として持つ何かの関数である。
変数$r_{ij},r_{ik},r_{jk}$は、それぞれベクトル${\boldsymbol r}_{ij} ,{\boldsymbol r}^{(o_i,o_k)}(i,k) ,{\boldsymbol r}^{(o_j,o_k)}(j,k)$の距離である。
また、距離は、$ r_{ij} \le r_{ik}$ を満たす。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。
尚、下記の例は、関数$\{f_{ij}(r), f_{ik}(r), f_{jk}(r) \} = r$の設定での例である。

```
def f_1(r):
    judge = 0
    if 0.8 < r and r < 1.21:
      judge =1
    return judge

op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'function': [f_1],
  'analysis_type': ['D'] }
```

## $F$ : angular Fourier series (AFS) like parameter

angular Fourier series parameter $F$は次の式で計算される。[@Bartok2013][@Seko2018]

$$ F^{(a=0,f_{1},f_{2},m) }_i  = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)} 
f_{1}( r_{ij} ) 
f_{2}( r_{ik} ) cos(l\theta_{jik}) $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
関数$f^1(r), f^2(r)$は、距離を引数として値を返り値として持つ何かの関数である。
変数$l$は、角度の係数である。
変数$\theta_{jik}$はベクトル${\boldsymbol r}_{ij}$とベクトル${\boldsymbol r}_{ik}$との角度である。
距離は、$r_{ij} \le r_{ik}$ を満たす。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。
尚、下記の例は、関数$\{f_{ij}(r), f_{ik}(r) \} = r$の設定での例である。

```
def f_1(r):
    return r

op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'l_in_F': [1],
  'function': [f_1],
  'analysis_type': ['F']}
```

## $H$ : angle histogram analysis (AHA)

angle histogram analysis $H$は次の式で計算される。

$$ h^{(b=1, bin)}(i) = \frac{1}{N(N-1)/2} \sum_{j>k \in N_b(i)} histogram^{(bin)}(\theta_{jik} ) $$
$$ h^{(b, bin)}(i)  = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}h^{(b-1, bin)}(j) $$
$$ H^{(a=0, b, bin, \nu)}(i) = FFT_{ amplitude }( h^{(b, bin)}(i)) \delta(X - \nu) $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は変数$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のlistである。
変数$b$は、各粒子のヒストグラムを隣接粒子のヒストグラムで平均化をを行う回数である。
変数$\theta_{jik}$はベクトル${\boldsymbol r}_{ij}$とベクトル${\boldsymbol r}_{ik}$との角度である。
関数$histogram$はビンの数$bin$のヒストグラムを作成する関数である。
関数$FFT_{amplitude}$はヒストグラムをフーリエ変換し amplitude を計算する関数である。
関数$\delta$はディラックのデルタ関数である。
変数$\nu$はフーリエ変換された後のヒストグラムの周波数成分である。
周波数成分$X$が$\nu$と同じであった場合のみ、デルタ関数$\delta$は1になるためである。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'b_in_H': 1,
  'bin_in_H': [24],
  'nu_in_H': [3],
  'analysis_type': ['H'] }
```

## $I$ : tetrahedron order parameter (TOP)

Tetrahedron order parameter $I$ は以下の式で計算される。[@CHAU1998][@Duboue-Dijon2015]

$$ I^{(a=0)}(i) = 1 - \frac{3}{8} \sum_{ j > k \in N_b(i) }\{ \cos( \theta_{jik})+ 1/3 \}^2  $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\theta^{(o_j,o_i,o_k)}(j,i,k)$はベクトル${\boldsymbol r}^{(o_i,o_j)}(i,j)$とベクトル${\boldsymbol r}^{(o_i,o_k)}(i,k)$との角度である。

隣接粒子数4、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_settings = {
  'neighbor': [4],
  'radius': [2.0],
  'ave_times': 1,
  'analysis_type': ['I'] }
```



## $Q$ : Bond order parameter

Bond order parameter $Q$ は以下の式で計算される。[@Steinhardt1983][@Lechner2008]

$$ Q^{(l,a=0,b)}_i = \sqrt{\frac{4\pi}{2l+1}\sum_{m=-l}^{l}|q^{(l,a=0,b)}_{lm}(i)|^2}$$
$$ q^{(l,a=0,b)}_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q^{(l,a=0,b-1)}_{lm}(j) $$
$$ q^{(l,a=0,b=1)}_{lm}(i) = \frac{1}{N} \sum_{j \in N_b(i)} Y_{lm}(\theta_{ij}, \phi_{ij}) $$

変数$a$は、オーダーパラメータの値を隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のリストである。
変数$b$は、球面調和関数を隣接粒子で平均化を行う回数である。
関数$Y$は、球面調和関数である。
変数$\theta_{ij}, \phi_{ij}$はベクトル${\boldsymbol r}_{ij}$の球面座標系での表現における角度で、$\theta$は$z$軸からの角度、$\phi$は$x$軸からの角度である。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'l_in_Q': [4],
  'b_in_Q': 1,
  'analysis_type': ['Q'] }
```

Steinhardtのオーダーパラメータ[@Steinhardt1983]は以下のオプションで計算できる。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q' : [4,6],
  'b_in_Q' : 0,
  'analysis_type' : ['Q'] }
```

Lechnerのオーダーパラメータ[@Lechner2008]は以下のオプションで計算できる。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q' : [4,6],
  'b_in_Q' : 1,
  'analysis_type' : ['Q'] }
```


## $W$ : Bond order parameter

Bond order parameter $W$ は以下の式で計算される。[@Steinhardt1983][@Lechner2008]

$$ W^{(l,a=0,b)}_i = \frac{\sum_{m_1+m_2+m_3=0}
\left( \begin{array}{ccc}
  l & l & l \\
  m_1 & m_2 & m_3
\end{array} \right) 
q^{(l,a=0,b)}_{lm_1}(i) q^{(l,a=0,b)}_{lm_2}(i) q^{(l,a=0,b)}_{lm_3}(i) }{ \left( \sum_{m=-l}^{l} |q^{(l,a=0,b)}_{lm}(i)|^2  \right)^{3/2}  }$$
$$ q^{(l,a=0,b)}_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q^{(l,a=0,b-1)}_{lm}(j) $$
$$ q^{(l,a=0,b=0)}_{lm}(i) = \frac{1}{N} \sum_{j \in N_b(i)} Y_{lm}(\theta_{ij}, \phi_{ij}) $$

変数$a$は、オーダーパラメータの値を隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のリストである。
変数$b$は、球面調和関数を隣接粒子で平均化を行う回数。
関数$Y$は、球面調和関数である。
変数$\theta_{ij}, \phi_{ij}$はベクトル${\boldsymbol r}_{ij}$の球面座標系での表現における角度で、$\theta$は$z$軸からの角度、$\phi$は$x$軸からの角度である。
変数$o$は、粒子の位置を表現する数値の集合$O$かつ、$o_i \neq O$であるような$b$個の数値の集合である。
変数$m_1,m_2,m_3$は$-l$から$l$までの値をとるが、$m_1+m_2+m_3=0$の時だけ計算される。
行列$\left( \begin{array}{ccc} l & l & l \\ m_1 & m_2 & m_3 \end{array} \right)$はWigner 3-$j$ symbolである。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'l_in_Q': [4],
  'b_in_Q': 1,
  'p_in_Q': [0],
  'analysis_type': ['W'] }
```

Steinhardtのオーダーパラメータ[@Steinhardt1983]は以下のオプションで計算できる。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q': [4,6],
  'b_in_Q': 0,
  'analysis_type': ['W'] }
```

Lechnerのオーダーパラメータ[@Lechner2008]は以下のオプションで計算できる。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q': [4,6],
  'b_in_Q': 1,
  'analysis_type': ['W'] }
```

## $Q1, W1$ : facet weighting Bond order parameter

MickelのBond order parameter $Q1$ は以下のような式で計算される。[@Mickel2013]

$$ Q1^{(l,a=0,b)}_i = \sqrt{\frac{4\pi}{2l+1}\sum_{m=-l}^{l}|q^{(l,a=0,b)}_{lm}(i)|^2}$$
$$ q^{(l,a=0,b)}_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q^{(l,a=0,b-1)}_{lm}(j) $$
$$ q^{(l,a=0,b=0)}_{lm}(i) =   \sum_{j \in N_b(i)} 
    F(i,j) Y_{lm}(\theta_{ij}, \phi_{ij}) $$

Mickel の方法では、Voronoi分割した後のfacetの面積$A$を使う。
粒子$i$と粒子$j$の間の面積を$A(i,j)$とすると、
$$ F(i,j) =  \frac{ A(i,j) }{ \sum_{ k \in N_b(i)} A(i,k)}  $$

変数$a$は、オーダーパラメータの値を隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のリストである。
変数$b$は、球面調和関数を隣接粒子で平均化を行う回数である。
関数$Y$は、球面調和関数である。
変数$\theta_{ij}, \phi_{ij}$はベクトル${\boldsymbol r}_{ij}$の球面座標系での表現における角度で、$\theta$は$z$軸からの角度、$\phi$は$x$軸からの角度である。

また、オーダーパラメータ$W1$に関しては以下のように、計算する。

$$ W1^{(l,a=0,b)}_i = \frac{\sum_{m_1+m_2+m_3=0}
\left( \begin{array}{ccc}
  l & l & l \\
  m_1 & m_2 & m_3
\end{array} \right) 
q^{(l,a=0,b)}_{lm_1}(i) q^{(l,a=0,b)}_{lm_2}(i) q^{(l,a=0,b)}_{lm_3}(i) }{ \left( \sum_{m=-l}^{l} |q^{(l,a=0,b)}_{lm}(i)|^2  \right)^{3/2}  }$$

このorder parameterは隣接粒子をDelaunay分割で計算することが必要であるため、隣接条件はDelaunayのみで使用する。

隣接条件 Delaunay分割、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。
```
op_settings = {
  'Delaunay': ['standard'],
  'radius': [2.0],
  'ave_times': 1,
  'l_in_Q': [4],
  'analysis_type': ['Q1', 'W1'] }
```

## $Q2, W2$ : function weighting Bond order parameter


$$ Q2^{(l,a=0,b)}_i = \sqrt{\frac{4\pi}{2l+1}\sum_{m=-l}^{l}|q^{(l,a=0,b)}_{lm}(i)|^2}$$
$$ q^{(l,a=0,b)}_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q^{(l,a=0,b-1)}_{lm}(j) $$
$$ q^{(l,a=0,b=0)}_{lm}(i) = \sum_{j \in N_b(i)} F(i,j) Y_{lm}( \theta_{ij}, \phi_{ij}) $$

粒子$i$と粒子$j$の間の重み付けを設定する関数$F(i,j)$を使用することができる。

変数$a$は、オーダーパラメータの値を隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のリストである。
変数$b$は、球面調和関数を隣接粒子で平均化を行う回数である。
関数$Y$は、球面調和関数である。
変数$\theta_{ij}, \phi_{ij}$はベクトル${\boldsymbol r}_{ij}$の球面座標系での表現における角度で、$\theta$は$z$軸からの角度、$\phi$は$x$軸からの角度である。


また、オーダーパラメータ$W2$に関しては以下のように、計算する。

$$ W2^{(l,a=0,b)}_i = \frac{\sum_{m_1+m_2+m_3=0}
\left( \begin{array}{ccc}
  l & l & l \\
  m_1 & m_2 & m_3
\end{array} \right) 
q^{(l,a=0,b)}_{lm_1}(i) q^{(l,a=0,b)}_{lm_2}(i) q^{(l,a=0,b)}_{lm_3}(i) }{ \left( \sum_{m=-l}^{l} |q^{(l,a=0,b)}_{lm}(i)|^2  \right)^{3/2}  }$$


隣接条件 Delaunay分割、隣接半径2.0でのMickelのオーダーパラメータの計算条件として以下の例を示す。

```
def f1(j, voronoi_area_list, distance_list):
    weight = voronoi_area_list[j] / np.sum(voronoi_area_list)
    return weight

op_settings = {
  'Delaunay': ['standard'],
  'radius': [2.0],
  'ave_times': 1,
  'l_in_Q': [4],
  'function_in_Q2': [f1],
  'analysis_type': ['Q2', 'W2'] }
```

他にも、距離に応じた重み付けなどができる。
以下の例は、粒子$i$と粒子$j$間の距離が近い場合はより重く、遠い場合はより軽くするような設定である。

```
def f1(j, voronoi_area_list, distance_list):
    sum_weight = 0
    for dist in distance_list:
      sum_weight += 1/dist
    weight = (1/distance_list[j]) / sum_weight
    return weight

op_settings = {
  'Delaunay': ['standard'],
  'radius': [2.0],
  'ave_times': 1,
  'l_in_Q': [4],
  'function_in_Q2': [f1],
  'analysis_type': ['Q2'] }
```


## $LQ, LW$ : local Bond order parameter

このオーダーパラメータは、[@Moore2010][@Fitzner2020][@Tribello2017]を模して実装したものである。

$$ LQ^{(l,a=0,b)}_i = \frac{1}{N} \sum_{j \in N_b(i)} \frac{ q^{(l,a,b)}_{lm}(i,j) }{ | q^{(l,a,b)}_{lm}(i) | | q^{(l,a,b)}_{lm}(j) |} $$
$$ q^{(l,a,b)}_{lm}(i,j) = \sum_{m=-l}^{l} q^{(l,a,b)}_{lm}(i) q^{\ast(l,a,b)}_{lm}(j)  $$
$$ q^{(l,a=0,b)}_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q^{(l,a=0,b-1)}_{lm}(j) $$
$$ q^{(l,a=0,b=0)}_{lm}(i) = \frac{1}{N} \sum_{j \in N_b(i)} Y_{lm}(\theta_{ij}, \phi_{ij}) $$

変数$a$は、オーダーパラメータの値を隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のリストである。
変数$b$は、球面調和関数を隣接粒子で平均化を行う回数である。
関数$Y$は、球面調和関数である。
変数$\theta_{ij}, \phi_{ij}$はベクトル${\boldsymbol r}_{ij}$の球面座標系での表現における角度で、$\theta$は$z$軸からの角度、$\phi$は$x$軸からの角度である。


$$ LW^{(l,a=0,b)}_i = \frac{\sum_{m_1+m_2+m_3=0}
\left( \begin{array}{ccc}
  l & l & l \\
  m_1 & m_2 & m_3
\end{array} \right) 
lq^{(l,a=0,b)}_{lm_1}(i) lq^{(l,a=0,b)}_{lm_2}(i) lq^{(l,a=0,b)}_{lm_3}(i) }{ \left( \sum_{m=-l}^{l} |lq^{(l,a=0,b)}_{lm}(i)|^2  \right)^{3/2}  }$$
$$ lq^{(l,a,b)}_{lm}(i) = \frac{1}{N}\sum_{j \in N_b(i)} \frac{q^{(l,a,b)}_{lm}(i) q^{\ast(l,a,b)}_{lm}(j)}{ | q^{(l,a,b)}_{lm}(i) | |  q^{(l,a,b)}_{lm}(j) | } $$


隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。
[@Moore2010]と同じようなオーダーパラメータは以下のオプションで計算できる。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q': [4,6],
  'b_in_Q': 0,
  'analysis_type': ['LQ', 'LW'] }
```


## $Z$ : user define order parameter

ユーザーが定義するためのオーダーパラメータ $Z$ を用意している。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。
```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'analysis_type': ['Z'] }
```
オーダーパラメータの計算部分としては、 op_tools/op_z_user_define.py である。
このファイルを編集し、ユーザーの考えたオーダーパラメータを実装することが可能である。

# 大量の解析を行う設定

  現実的に実行するためには、非常に長い計算が必要だろう。

```
  def f_1(r):
      return r
  op_settings = {  
    # 隣接粒子半径の設定
    'neighbor'       : [8],               # 隣接粒子数
    'radius'         : [1.5],             # 隣接半径
    'ave_times'      : 1,                 # あるオーダーパラメータを周囲の粒子で平均を計算する回数  
    # A
    'op_types' : ['A','P','N'],           # オーダーパラメータ A での解析の種類の指定
    'm_in_A'         : [2, 4],            # 粒子i,粒子j からの距離の近い粒子jの粒子数
    # B
    'm_in_B' : [2],                       # 角度の係数
    'n_in_B': [1, 2],                     # cosine関数の指数
    'phi_in_B': [0],                      # 角度のoffset
    # C
    # D
    'function': [f_1]                     # 関数の種類
    # F
    'l_in_F' : [1],                       # 角度の係数
    # H
    'b_in_H' : 1,                         # 角度のヒストグラムを平均化する回数
    'bin_in_H' : [24],                    # ヒストグラムのビンの数
    'nu_in_H' : [3],                      # 抜き出す角度の周波数成分。この例では pi/3 の周波数の成分の指定になっている。
    # I
    # Q
    'b_in_Q'         : 1,                 # 球面調和関数を平均化する回数
    'l_in_Q'         : [2, 4, 6],         # 球面調和関数の次数を指定するパラメータl  
    'p_in_Q'         : [0],               # その粒子の方向ベクトルに関する重み
    # S
    'n_in_S'         : [2],               # Degree of Legendre_polynomials
    # T
    'n_in_T'         : [2],               # Degree of Legendre_polynomials
    'd_in_T': [1.0],
    'analysis_type': ['A', 'B', 'C', 'D', 'F', 'H', 'I', 'Q', 'W', 'S', 'T']} # 解析するオーダーパラメータの種類
```

# 出力のフォーマット

次のように使用する。
```
  import order_tools
  order_param_data = \
    op_analyze(coord, direct, box_length, op_settings)
```
出力として各粒子のオーダーパラメータが計算される。
各粒子のオーダーパラメータにアクセスするためには、
```
  order_param_data['Q_N6_a=1_b_1']
```

- Q : オーダーパラメータの種類
- N6 : 隣接粒子の条件
- 'a=1_b=1' : オーダーパラメータの計算に使用したパラメータ一覧
でアクセスできる。



# Reference

