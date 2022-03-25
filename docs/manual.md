---
title: "User manual for op_tools ver 0.1"
date: "Feb 2019"
author: "Hideo Doi"
---

\newpage

# What is this?

python module for order parameter analysis for molecular and particle simulation.
this module evaluete the particle environment as the value.
In molecular simulation, there are often cases where you want to mechanically determine the structure of a particle.
For example, when melting simulating of solid metal, you may want to visualize how it melts.
You can use such a module at such a time.

# How to install

$ cd order_tools  
$ pip install -e .  

# 必要なデータ
  1. coord                     : List of coordinates of each particles.  Such as [ [0,0,0], [0,0,1], ... ] like [[x1, y1, z1], [x2, y2, z2], ... ]  
  2. direct                    : Direction vector of each particle. It may be a three-dimensional unit vector or a quaternion. Such as [[1,0,0], ...] or [[1,0,0,0], ....]  
    In the case of a three-dimensional unit vector, the order is [x, y, z]. In the case of quaternions, the order is [w, x, y, z].
    In the case of a mass point or spherical particle, It has no direction vector. There is no problem with direct = [].
  3. box_length                : The length of the simulation box. Such as [3, 3, 3]
  4. op_settings : Settings for calculating each order parameter


# Common settings for all order parameters

## Neibhorhood particle setting

The first method is to set a particle whose distance from particle $i$ is within a certain distance (neighborhood radius) as a neighborhood particle of particle $i$.
The advantage of this method is that it is relatively easy to implement and easy for users to understand.
The disadvantage is that the number of nearby particles can be different for each particle, and the number of nearby particles can vary depending on the unit of distance.
For example, specifying the neighborhood radius as 1 nm, 1 angstrom will change the result. This is called scale dependency.
Another method is to set $n$ particles close to the particle $i$ as neighborhood particles.
The advantage is that neighborhood particles do not change because there is no scale dependency, and even if the unit of length changes, the magnitude relationship of distances does not change.
The disadvantages are that it is relatively difficult to implement, the computational cost is relatively high (> 10%), and there are few usage records in articles.


###  Setting for neighborhood radius

Specify calculation conditions for order parameters.
```
  op_settings = {
    'radius' : [1.5, 1.75] ,  
    ... ( other parameter settings ) }
```
User can specify in the list format, and it is also possible to specify multiple conditions at the same time.
In the above example, the radius setting is 1.5 and 1.75. ..

###  Setting for the number of neighborhood particles

Specify calculation conditions for order parameters.
```
  op_settings = {
    'neighbor' : [8, 12] ,  
    ... ( other parameter settings ) }
```
User can specify in the list format, and it is also possible to specify multiple conditions at the same time.
In the above example, the number of neighborhood particles setting is 8 and 12. ..

## Setting for the number of times for averaging

When the classification performance of the order parameter of each particle does not enough performance.
To increase the performance, user can perform the averaging calculation.
The average is calculated with the order parameter of particle $i$ and the order parameter of neighborhood particles of particle $i$.
$N_b(i)$ is a list of $N$ neighborhood particles of particle $i$.
$\tilde{N}_b(i)$ is a list of $N + 1$ particles that $i$ itself is added to $N_b(i)$.
The order parameter of the particles $i$ before averaging is $X(i)$ and the order parameter after averaging is $Y(i)$.
The following calculation is performed.
$$Y(i) = \frac{ \sum_{j \in \tilde{N}_b(i)}X(j)}{N+1}$$ 

This averaging calculation has the following advantages and disadvantages.
The advantage is that the calculation cost is low, and it is possible to improve the classification performance of the same order parameter,
Any numerical value can be used, and it can be averaged many times.
On the other hand, the disadvantage is that more information is used to calculate the order parameters, and the resolution of the order parameters is decreased.
The order parameters are calculated using the information of neighborhood particles, and the averaging calculation is calculated using the order parameters of the neighborhood particles.
Each time the averaging operation is performed, the information on neighborhood particles of neighborhood particles is used.
In other words, more particles are used to calculate order parameters, and information on far particles is used.
This is not a problem in homogeneous systems, but it is a problem in inhomogeneous systems (such as interfaces).
In inhomogeneous systems, it is likely to be used in many cases for the purpose of wanting to know the position where the abnormality is occurring or want to know the position of the interface, etc.
Using distant particle information leads the indistinctness of position.

The number of times of this averaging is specified by op_settings specifying the calculation condition of the order parameter as follows.
Note that this value starts from 0, and in the case of 0, averaging is not performed.

```
  op_settings = {
    'ave_times'      : 1, 
    ... ( other parameter settings )
     }
```

## Coordinates

This software was developed to analyze particles (eg, ellipsoids, rods, arrows, disks, etc.) that have direction information, not mass points or spherical particles.
Of course, analysis of mass points and spherical particles is also possible.
If it is not a mass point or spherical particle, the coordinates you want to use for analysis may change.
For example, in the case of rod-like particles, it may be considered that analysis is desired to be performed at the coordinates of the center of the particle, or analysis is desired to be performed at the coordinates of the tip.
Also, the coordinates of one particle $i$ may be considered to be the center, and the coordinates of the neighborhood particle $j$ may be the tip.
Therefore, op_tools uses the following formula for particle coordinates.

$$ {\boldsymbol r}^{(o_i)}(i) = {\boldsymbol r}(i) + o_f o_i {\boldsymbol u}(i) $$


The vector ${\boldsymbol r}^{(o_i)}(i)$ is the coordinate vector of the particle $i$ for analysis,
The vector ${\boldsymbol r}(i)$ is a coordinate vector of the particle $i$ given as an argument to the python module.
The variable $o_f$ is a coefficient for the direction vector, the variable ${\boldsymbol o}_i$ is a variable indicating the position at the particle $i$, and the vector ${\boldsymbol u}(i)$ is unit direct vector of the particle $i$.
The variable $o_f$ represents the strength of the direction vector used throughout the analysis.
The variable $o_i$ is used to represent the position of the coordinate vector of the particle $i$.
Usually, it looks like $o_i \in \{1,0, -1\}$, and when $o_f = 1, o_i = 1$, the vector ${\boldsymbol r}^{(o_i)}(i)$ is the coordinates of the tip of the direction vector.
Also, when $o_f = 1, o_i = -1$, the vector ${\boldsymbol r}^{(o_i)}(i)$ is the coordinate of the end of the direction vector.
In this way, it is possible to switch which coordinate of the direction vector to use.
In the case of a mass point or a spherical particle, it may be set as $o_f = 0$ and $o_i = 0$.

In the case of an ellipsoid, specify the calculation condition of order parameter in op_settings as follows.


ベクトル ${\boldsymbol r}^{(o_i)}(i)$は、解析に使用する粒子$i$の座標ベクトル、
ベクトル${\boldsymbol r}(i)$は、pythonモジュールに引数として与えられた粒子$i$の座標ベクトルである。
変数$o_f$は方向ベクトルの係数で、変数${\boldsymbol o}_i$は粒子$i$での位置を示す変数、ベクトル${\boldsymbol u}(i)$は粒子$i$の持つ方向ベクトルである。
変数$o_f$は解析全体で用いる方向ベクトルの強さを表現している。
変数$o_i$は、粒子$i$の座標ベクトルの位置を表現するために用いている。
通常、$o_i \in \{1,0,-1\}$ のようになっており、$o_f=1, o_i=1$の時は、ベクトル${\boldsymbol r}^{(o_i)}(i)$は方向ベクトルの先端の座標になる。
また、$o_f=1, o_i=-1$の時は、ベクトル${\boldsymbol r}^{(o_i)}(i)$は方向ベクトルの後端の座標になる。
このように、方向ベクトルのどの座標を使うか切り替える事ができる。
尚、質点や球状粒子の場合は、$o_f=0, o_i=0$とすれば良い。

楕円体の場合は、オーダーパラメータの計算条件を指定する op_settings で次のように指定を行う。
```
  op_settings = {
    ... ( 各オーダーパラメータの設定 ) ...
    'o_factor'       : [1.0 ],
    'oi_oj'          : [1, 0, -1],
     }
```
この例では、座標として粒子の中心座標を入力とした場合、楕円体の先端、中心、後端の3通りを座標として使用したい場合の設定である。

質点または球状粒子の場合は、オーダーパラメータの計算条件を指定する op_settings で次のように指定を行う。
```
  op_settings = {
    ... ( 各オーダーパラメータの設定 ) ...
    'o_factor'       : [0],
    'oi_oj'          : [0],
     }
```

また、粒子$i$の座標ベクトル${\boldsymbol r}^{(o_i)}(i)$から粒子$j$の座標ベクトル${\boldsymbol r}^{(o_j)}(j)$は以下のように計算する。

$$ {\boldsymbol r}^{(o_i,o_j)}(i,j) = {\boldsymbol r}^{(o_j)}(j) - {\boldsymbol r}^{(o_i)}(i)$$


# 各オーダーパラメータの説明

## $S$ : Onsager's parameter

Onsagerのオーダーパラメータ $S$ は次の式で計算される。[@Onsager1949][@Zannoni1979]

$$ S^{(a=1,n)}(i) = \frac{ \sum_{j \in N_b(i)} {P_n(\cos( \theta ))} }{N}, n even.$$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
関数$P_n$は[Legendre polynomial](https://en.wikipedia.org/wiki/Legendre_polynomials)である。変数$n$はDegree of the polynomialである。
変数$\theta$は、粒子$i$の持つ方向ベクトル${\boldsymbol u}(i)$と粒子$j$の持つ方向ベクトル${\boldsymbol u}(j)$との角度である。
変数$\cos(\theta)$は通常、${\boldsymbol u}(i) \cdot {\boldsymbol u}(j)$で計算される。

$n = 2, 4$の時、オーダーパラメータ $S$ はそれぞれ以下の式で計算される。
$$ S^{(a=1, n=2)}(i) = \frac{ \sum_{j \in N_b(i)} { [ 3 \cos^2(\theta) - 1]/2 } }{N} $$
$$ S^{(a=1, n=4)}(i) = \frac{ \sum_{j \in N_b(i)} { [ 35 \cos^4(\theta) -30 \cos^2(\theta) + 3  ]/8 } }{N} $$


隣接粒子数12、隣接半径2.0でのオーダーパラメータの設定として以下の例を示す。
尚、このオーダーパラメータは計算のために方向ベクトルが必須であるため、質点や球状粒子の解析に使う事はできない。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'oi_oj': [0],
  'o_factor': [0.00],
  'n_in_S' : [2],
  'analysis_type' : ['S']
   }
```

## $T$ : McMillan's Sigma

McMillanのパラメータ$T$は次の式で計算される。[@McMillan1971]

$$ T^{(a=1,n,o_i,o_j)} = \frac{ \sum_{j \in N_b(i)}{ \cos( 2 \pi z^{(o_i,o_j)}(i,j) / d ) P_n(\cos( \theta )) }   }{N}$$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
関数$P_n$は[Legendre polynomial](https://en.wikipedia.org/wiki/Legendre_polynomials)である。変数$n$はDegree of the polynomialである。
変数$\theta$は、粒子$i$の持つ方向ベクトル${\boldsymbol u}(i)$と粒子$j$の持つ方向ベクトル${\boldsymbol u}(j)$との角度である。
変数$\cos(\theta)$は通常、${\boldsymbol u}(i) \cdot {\boldsymbol u}(j)$で計算される。
変数$z^{(o_i,o_j)}(i,j)$は、ベクトル${\boldsymbol r}^{(o_i)}(i)$を通過し、ベクトル${\boldsymbol u}(i)$と垂直な平面$P$から、
ベクトル${\boldsymbol r}^{(o_j)}(j)$までの距離である。
変数$d$は、層から層までの距離である。


$n = 2$の時、オーダーパラメータ $T$ は以下の式で計算される。
$$ T^{(a=1,n=2,o_i,o_j)} = \frac{ \sum_{j \in N_b(i)}{ \cos( 2 \pi z^{(o_i,o_j)}(i,j) / d ) [ 3 \cos^2(\theta) - 1 ]/2 }   }{N}$$

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。
尚、このオーダーパラメータは計算のために方向ベクトルが必須であるため、質点や球状粒子の解析に使う事はできない。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'oi_oj': [0],
  'o_factor': [0.00],
  'n_in_T': [2],
  'd_in_T': [1.0],
  'analysis_type' : ['T']
   }
```

## $A$ : neighborhood parameters

common neighborhood parameter $A$ [@Honeycutt1987]、predominant common neighborhood parameter $P$ [@Radhi2017]、 another predominant common neighborhood parameter $N$ [@Radhi2017] は非常に似ている式で計算される。
$P$と$N$に関しては、$A$の一種として実装されている。

$$ A^{(a=1,type=A,m,o_i,o_j,o_k)}_i = A^{(a=1,m,o_i,o_j,o_k)}_i = \frac{1}{N} \sum_{j \in N_b(i)} | \sum_{k \in N_b(i,j)} \{ {\boldsymbol r}^{(o_i,o_k)}(i,k) + {\boldsymbol r}^{(o_j,o_k)}(j,k)\} |^2 $$
$$ A^{(a=1,type=P,m,o_i,o_j,o_k)}_i = P^{(a=1,m,o_i,o_j,o_k)}_i = \frac{1}{N} \sum_{j \in N_b(i)} | \sum_{k \in N_b(i,j)} \{ {\boldsymbol r}^{(o_i,o_k)}(i,j) + {\boldsymbol r}^{(o_j,o_k)}(k,j)\} |^2 $$
$$ A^{(a=1,type=N,m,o_i,o_j,o_k)}_i = N^{(a=1,m,o_i,o_j,o_k)}_i = \frac{1}{N}|\sum_{j \in N_b(i)}   \sum_{k \in N_b(i,j)} \{ {\boldsymbol r}^{(o_i,o_k)}(i,j) + {\boldsymbol r}^{(o_j,o_k)}(k,j)\} |^2 $$

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
  'oi_oj': [0],
  'o_factor': [0.00],
  'm_in_A': [2],
  'types_in_A': ['A', 'P', 'N'],
  'analysis_type': ['A']}
```

## $B$ : bond angle analysis (BAA)

bond angle analysis $B$は次の式で計算される。 [@Ackland2006]

$$ B^{(a=1,m,n,\phi,o_i,o_j,o_k)}_i = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)  }f^{(m,n,\phi,o_i,o_j,o_k)}(\theta^{(o_i,o_j,o_k)}(j,i,k)) $$
$$ f^{(m,n,\phi,o_i,o_j,o_k)}(\theta(j,i,k)) = cos^{n} (m\theta^{(o_i,o_j,o_k)}(j,i,k) + \phi) $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\theta^{(o_j,o_i,o_k)}(j,i,k)$はベクトル${\boldsymbol r}^{(o_i,o_j)}(i,j)$とベクトル${\boldsymbol r}^{(o_i,o_k)}(i,k)$との角度である。
変数$m$は、角度の係数である。
変数$n$は、cos関数に使用する指数である。
変数$\phi$は、関数の補正のために角度である。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_param = {
  'neighbor': [12],
  'radius': [1.5],
  'ave_times': 1,
  'oi_oj': [0],
  'o_factor': [0.00],
  'm_in_B': [2],
  'phi_in_B': [0],
  'n_in_B': [1, 2],
  'analysis_type': ['B']}
```

## $C$ : centrosymmetry parameter analysis (CPA)

centrosymmetry parameter $C$は次の式で計算される。[@Kelchner1998]

$$ C^{(a=1,o_i,o_j,o_k)}_i = \sum_{j \in M_b(i)} | {\boldsymbol r}^{(o_i,o_j)}(i,j) + {\boldsymbol r}^{(o_i,o_k)}(i,k)|^2$$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$M_b(i)$は粒子$i$の$N/2$個の隣接粒子のリストである。

粒子$k$の計算の方法は2通り実装している。
座標${\boldsymbol r}^{(o_j)}(j)$の、ベクトル${\boldsymbol r}^{(o_i)}(i)$に関して反対側に移動した${\boldsymbol r'}^{(o_j)}$(j)から一番近い位置にある$N_b(i)$リストにある粒子である。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_param = {
    'neighbor': [12],
    'radius': [2.0],
    'ave_times': 1,
    'oi_oj': [0],
    'o_factor': [0.00],
    'analysis_type': ['C'] }
```

## $D$ : neighbor distance analysis (NDA)

neighbor distance analysis $D$は次の式で計算される。[@Stukowski2012]

$$ D^{(a=1,o_i,o_j,o_k,f_{ij},f_{ik},f_{jk})}_i = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)} f_{ij}( r^{(o_i,o_j)}(i,j)) f_{ik}( r^{(o_i,o_k)}(i,k)) f_{jk}( r^{(o_j,o_k)}(j,k) ) $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
関数$f_{ij}(r(i,j)), f_{ik}(r(i,k)), f_{jk}(r(j,k))$は、距離を引数とし、返り値として持つ何かの関数である。
変数$r(i,j),r(i,k),r(j,k)$は、 ベクトル${\boldsymbol r}^{(o_i,o_j)}(i,j) ,{\boldsymbol r}^{(o_i,o_k)}(i,k) ,{\boldsymbol r}^{(o_j,o_k)}(j,k)$の距離である。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。
尚、下記の例は、関数$\{f_{ij}(r), f_{ik}(r), f_{jk}(r) \} = r$の設定での例である。

```
def f_1(r):
    return r

op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'oi_oj': [0],
  'o_factor': [0.00],
  'function': [f_1],
  'analysis_type': ['D'] }
```

## $F$ : angular Fourier series (AFS) like parameter

angular Fourier series parameter $F$は次の式で計算される。[@Bartok2013][@Seko2018]

$$ F^{(a=1,o_i,o_j,o_k,f_{ij},f_{ik},m) }_i  = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)} f_{ij}( {\boldsymbol r}^{(o_i,o_j)}(i,j)) f_{ik}( {\boldsymbol r}^{(o_i,o_k)}(i,k)) cos(l\theta^{(o_j,o_i,o_k)}(j,i,k)) $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
関数$f_{ij}({\boldsymbol r}), f_{ik}({\boldsymbol r}), f_{jk}({\boldsymbol r})$は、ベクトルを引数として値を返り値として持つ何かの関数である。
変数$l$は、角度の係数である。
変数$\theta^{(o_j,o_i,o_k)}(j,i,k)$はベクトル${\boldsymbol r}^{(o_i,o_j)}(i,j)$とベクトル${\boldsymbol r}^{(o_i,o_k)}(i,k)$との角度である。
関数$f_{ij}(r(i,j)), f_{ik}(r(i,k))$は、距離を引数とし、返り値として持つ何かの関数である。
変数$r(i,j),r(i,k)$は、 ベクトル${\boldsymbol r}^{(o_i,o_j)}(i,j) ,{\boldsymbol r}^{(o_i,o_k)}(i,k)$の距離である。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。
尚、下記の例は、関数$\{f_{ij}(r), f_{ik}(r) \} = r$の設定での例である。

```
def f_1(r):
    return r

op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'oi_oj': [0],
  'o_factor': [0.00],
  'l_in_F': [1],
  'function': [f_1],
  'analysis_type': ['F']}
```

## $H$ : angle histogram analysis (AHA)

angle histogram analysis $H$は次の式で計算される。

$$ h^{(b=1, bin,o_i,o_j,o_k)}(i) = \frac{1}{N(N-1)/2} \sum_{j>k \in N_b(i)} histogram^{(bin)}(\theta^{(o_i,o_j,o_k)}(j,i,k) ) $$
$$ h^{(b, bin,o_i,o_j,o_k)}(i)  = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}h^{(b-1, bin, o_i, o_j,o_k)}(j) $$
$$ H^{(a=1, b, bin,o_i,o_j,o_k, \nu)}_i = FFT_{ amplitude }( h^{(b, bin,o_i,o_j,o_k)}(i)) \delta(X - \nu) $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は変数$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のlistである。
変数$b$は、各粒子のヒストグラムを隣接粒子のヒストグラムで平均化をを行う回数である。
変数$\theta^{(o_j,o_i,o_k)}(j,i,k)$はベクトル${\boldsymbol r}^{(o_i,o_j)}(i,j)$とベクトル${\boldsymbol r}^{(o_i,o_k)}(i,k)$との角度である。
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
  'oi_oj': [0],
  'o_factor': [0.00],
  'b_in_H': 1,
  'bin_in_H': [24],
  'nu_in_H': [3],
  'analysis_type': ['H'] }
```

## $I$ : tetrahedron order parameter (TOP)

Tetrahedron order parameter $I$ は以下の式で計算される。[@CHAU1998][@Duboue-Dijon2015]

$$ I^{(a=1,o_i,o_j,o_k)}_i = 1 - \frac{3}{8} \sum_{ j > k \in N_b(i) }\{ \cos( \theta^{(o_i,o_j,o_k)}(j,i,k) + 1/3 \}^2  $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\theta^{(o_j,o_i,o_k)}(j,i,k)$はベクトル${\boldsymbol r}^{(o_i,o_j)}(i,j)$とベクトル${\boldsymbol r}^{(o_i,o_k)}(i,k)$との角度である。

隣接粒子数4、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_settings = {
  'neighbor': [4],
  'radius': [2.0],
  'ave_times': 1,
  'oi_oj': [0],
  'o_factor': [0.00],
  'analysis_type': ['I'] }
```



## $Q$ : Bond order parameter

Bond order parameter $Q$ は以下の式で計算される。[@Steinhardt1983][@Lechner2008]

$$ Q^{(l,a=1,b,o_i,o_j,p)}_i = \sqrt{\frac{4\pi}{2l+1}\sum_{m=-l}^{l}|q^{(l,a=1,b,o_i,o_j,p)}_{lm}(i)|^2}$$
$$ q^{(l,a=1,b,o_i,o_j,p)}_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q^{(l,a=1,b-1,o_i,o_j,p)}_{lm}(j) $$
$$ q^{(l,a=1,b=1,o_i,o_j,p)}_{lm}(i) = \frac{1}{N + c} [ \sum_{j \in N_b(i)} 
    Y_{lm}(\theta^{( o_i,o_j )}(i,j), \phi^{( o_i,o_j )}(i,j)) + 
    p \sum_{v \in o} Y_{lm}(\theta^{( o_i,v )}(i,i), \phi^{( o_i,v )}(i,i)) ] $$

変数$a$は、オーダーパラメータの値を隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のリストである。
変数$b$は、球面調和関数を隣接粒子で平均化を行う回数である。
関数$Y$は、球面調和関数である。
変数$\theta^{(o_i,o_j)}(i,j), \phi^{( o_i,o_j )}(i,j)$はベクトル${\boldsymbol r}^{(o_i,o_j)}(i,j)$の球面座標系での表現における角度で、$\theta$は$z$軸からの角度、$\phi$は$x$軸からの角度である。
変数$o$は、粒子の位置を表現する数値の集合$O$かつ、$o_i \neq O$であるような$b$個の数値の集合である。
例えば、$O=\{1,0,-1\}$かつ$o_i=0$であった、$o=\{1,-1\}$となる。
変数$p$は、粒子$i$自身の他の位置ベクトル重さである。
変数$c$は、規格化のための係数で、$c = bp$となるような数値である。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'oi_oj': [0],
  'o_factor': [0.00],
  'l_in_Q': [4],
  'b_in_Q': 1,
  'p_in_Q': [0],
  'analysis_type': ['Q'] }
```
尚、変数 p_in_Q では、変数として隣接粒子数$N$を使用することが可能であり、次のように指定する事も可能である。
```
op_settings = {
  'p_in_Q' : [0,'N', 'N/2', '2*N'],
    ... ( 各オーダーパラメータのパラメータ ) }
```

Steinhardtのオーダーパラメータ[@Steinhardt1983]は以下のオプションで計算できる。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'oi_oj': [0],
  'o_factor': [0.00],
  'l_in_Q' : [4,6],
  'b_in_Q' : 0,
  'p_in_Q' : [0],
  'analysis_type' : ['Q'] }
```

Lechnerのオーダーパラメータ[@Lechner2008]は以下のオプションで計算できる。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'oi_oj': [0],
  'o_factor': [0.00],
  'l_in_Q' : [4,6],
  'b_in_Q' : 1,
  'p_in_Q' : [0],
  'analysis_type' : ['Q'] }
```

## $W$ : Bond order parameter

Bond order parameter $W$ は以下の式で計算される。[@Steinhardt1983][@Lechner2008]

$$ W^{(l,a=1,b,o_i,o_j,p)}_i = \frac{\sum_{m_1+m_2+m_3=0}
\left( \begin{array}{ccc}
  l & l & l \\
  m_1 & m_2 & m_3
\end{array} \right) 
q^{(l,a=1,b,o_i,o_j,p)}_{lm_1}(i) q^{(l,a=1,b,o_i,o_j,p)}_{lm_2}(i) q^{(l,a=1,b,o_i,o_j,p)}_{lm_3}(i) }{ \left( \sum_{m=-l}^{l} |q^{(l,a=1,b,o_i,o_j,p)}_{lm}(i)|^2  \right)^{3/2}  }$$
$$ q^{(l,a=1,b,o_i,o_j,p)}_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q^{(l,a=1,b-1,o_i,o_j,p)}_{lm}(j) $$
$$ q^{(l,a=1,b=1,o_i,o_j,p)}_{lm}(i) = \frac{1}{N+ c} [ \sum_{j \in N_b(i)} 
    Y_{lm}(\theta^{( o_i,o_j )}(i,j), \phi^{( o_i,o_j )}(i,j)) + 
    p \sum_{v \in o} Y_{lm}(\theta^{( o_i,v )}(i,i), \phi^{( o_i,v )}(i,i)) ] $$

変数$a$は、オーダーパラメータの値を隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のリストである。
変数$b$は、球面調和関数を隣接粒子で平均化を行う回数。
関数$Y$は、球面調和関数である。
変数$\theta^{(o_i,o_j)}(i,j), \phi^{( o_i,o_j )}(i,j)$はベクトル${\boldsymbol r}^{(o_i,o_j)}(i,j)$の球面座標系での表現における角度で、$\theta$は$z$軸からの角度、$\phi$は$x$軸からの角度である。
変数$o$は、粒子の位置を表現する数値の集合$O$かつ、$o_i \neq O$であるような$b$個の数値の集合である。
例えば、$O=\{1,0,-1\}$かつ$o_i=0$であった、$o=\{1,-1\}$となる。
変数$p$は、粒子$i$自身の他の位置ベクトル重さである。
変数$c$は、規格化のための係数で、$c = bp$となるような数値である。
変数$m_1,m_2,m_3$は$-l$から$l$までの値をとるが、$m_1+m_2+m_3=0$の時だけ計算される。
行列$\left( \begin{array}{ccc} l & l & l \\ m_1 & m_2 & m_3 \end{array} \right)$はWigner 3-$j$ symbolである。

隣接粒子数12、隣接半径2.0でのオーダーパラメータの計算条件として以下の例を示す。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'oi_oj': [0],
  'o_factor': [0.00],
  'l_in_Q': [4],
  'b_in_Q': 1,
  'p_in_Q': [0],
  'analysis_type': ['W'] }
```
尚、変数 p_in_Q では、変数として隣接粒子数$N$を使用することが可能であり、次のように指定する事も可能である。
```
op_settings = {
  'p_in_Q' : [0,'N', 'N/2', '2*N'],
    ... ( 各オーダーパラメータのパラメータ ) }
```

Steinhardtのオーダーパラメータ[@Steinhardt1983]は以下のオプションで計算できる。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'oi_oj': [0],
  'o_factor': [0.00],
  'l_in_Q': [4,6],
  'b_in_Q': 0,
  'p_in_Q': [0],
  'analysis_type': ['W'] }
```

Lechnerのオーダーパラメータ[@Lechner2008]は以下のオプションで計算できる。

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'oi_oj': [0],
  'o_factor': [0.00],
  'l_in_Q': [4,6],
  'b_in_Q': 1,
  'p_in_Q': [0],
  'analysis_type': ['W'] }
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
    'oi_oj'          : [1,0,-1],          # 粒子の座標をどの点にするかという設定 粒子 => [0], 直線 => [1,-1](先端、後端),  楕円体 => [0, 1, -1] (中心、先端、後端)  
    'o_factor'       : [0.5, 1.0, 1.5],   # 方向ベクトルの長さの設定
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
  order_param_data['Q_N6_a=1_b_1_of_1.00_oi=0_oj=0']
```

- Q : オーダーパラメータの種類
- N6 : 隣接粒子の条件
- 'a=1_b=1_of_1.00_oi=0_oj=0' : オーダーパラメータの計算に使用したパラメータ一覧
でアクセスできる。



# Reference

