---
title: "論文に使用したパラメータなど"
date: "Feb 2019"
--

# $A$ : neighborhood parameters

common neighborhood parameter $A$ [@Honeycutt1987]、predominant common neighborhood parameter $P$ [@Radhi2017]、 another predominant common neighborhood parameter $N$ [@Radhi2017] は非常に似ている式で計算される。
$P$と$N$に関しては、$A$の一種として実装されている。

$$ A^{(type,m)}(i) = \frac{1}{N+1} \sum_{j \in \tilde{N}_b(i)} A'^{(type,m)}(j) $$

$$ A'^{(type=A,m)}( i ) = \frac{1}{N} \sum_{j \in N_b(i)} | \sum_{k \in N_b(i,j)} \{ {\boldsymbol r}(i,k) + {\boldsymbol r}(j,k)\} |^2 $$
$$ A'^{(type=P,m)}( i ) = \frac{1}{N} \sum_{j \in N_b(i)} | \sum_{k \in N_b(i,j)} \{ {\boldsymbol r}(i,j) + {\boldsymbol r}(k,j)\} |^2 $$
$$ A'^{(type=N,m)}( i ) = \frac{1}{N}|\sum_{j \in N_b(i)}   \sum_{k \in N_b(i,j)} \{ {\boldsymbol r}(i,j) + {\boldsymbol r}(k,j)\} |^2 $$

変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は粒子$i$を含む$N+1$個の隣接粒子のリストである。
変数$N_b(i,j)$は粒子$i$,粒子$j$から最も近い$m$個の粒子のリストである。
変数$type$で計算を行うオーダーパラメータの種類を指定する変数である。

本研究では、変数$m$として、$\{1,2,3\}$ を使用した。


# $B$ : bond angle analysis (BAA)

bond angle analysis $B$は次の式で計算される。 [@Ackland2006]

$$ B^{(m,n,\phi)}(i) = \frac{1}{N+1} \sum_{j \in \tilde{N}_b(i)} B'^{(m,n,\phi)}(i) $$
$$ B'^{(m,n,\phi)}(i) = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)} f^{(m,n,\phi)}(\theta(j,i,k)) $$
$$ f^{(m,n,\phi)}(\theta(j,i,k)) = cos^{n} (m\theta(j,i,k) + \phi) $$

変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は粒子$i$を含む$N+1$個の隣接粒子のリストである。
変数$\theta(j,i,k)$はベクトル${\boldsymbol r}(i,j)$とベクトル${\boldsymbol r}(i,k)$との角度である。
変数$m$は、角度の係数である。
変数$n$は、cos関数に使用する指数である。
変数$\phi$は、関数の補正のために角度である。

本研究では、変数$m$として、$\{1,2,3\}$、
変数$n$として、$\{1,2\}$
変数$\phi$として、$\{ 0, 2/3 \pi, \pi/2, \pi/3, \pi/4, \pi/5, \pi/6 \}$を使用した。


# $C$ : centrosymmetry parameter analysis (CPA)

centrosymmetry parameter $C$は次の式で計算される。[@Kelchner1998]

$$ C(i) = \frac{1}{N+1} \sum_{j \in \tilde{N}_b(i)} C'(i) $$
$$ C'(i) = \sum_{j \in M_b(i)} | {\boldsymbol r}(i,j) + {\boldsymbol r}(i,k)|^2$$

変数$\tilde{N}_b(i)$は粒子$i$を含む$N+1$個の隣接粒子のリストである。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$M_b(i)$は粒子$i$の$N/2$個の隣接粒子のリストである。
粒子$k$は、座標${\boldsymbol r}(j)$の、ベクトル${\boldsymbol r}(i)$に関して反対側に移動した座標${\boldsymbol r'}(j)$から一番近い位置にある$N_b(i)$リストにある粒子である。


# $D$ : neighbor distance analysis (NDA)

neighbor distance analysis $D$は次の式で計算される。[@Stukowski2012]

$$ D(i) = \frac{1}{N+1} \sum_{j \in \tilde{N}_b(i)} D'(i) $$
$$ D'^{(f_{ij},f_{ik},f_{jk})}(i) = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)} f_{ij}( r(i,j)) f_{ik}( r(i,k)) f_{jk}( r(j,k) ) $$

変数$\tilde{N}_b(i)$は粒子$i$を含む$N+1$個の隣接粒子のリストである。
関数$f_{ij}(r(i,j)), f_{ik}(r(i,k)), f_{jk}(r(j,k))$は、距離を引数とし、返り値として何らかの値を持つ関数である。
変数$r(i,j),r(i,k),r(j,k)$は、 各々、粒子$i,j$, 粒子$i,k$, 粒子$j,k$間の距離である。

本研究では、関数$f$として、$\{ \sqrt{r}, r, r^2, [1 - \exp\{-(r-3.0)^2 / (2* 1.5^2)\}],  [0.5 + 0.5 * \exp\{-(r-3.0)^2 / (2 * (1.5)^2) \} ] \}$ を使用した。

# $F$ : angular Fourier series (AFS) like parameter

angular Fourier series parameter $F$は次の式で計算される。[@Bartok2013][@Seko2018]

$$ F(i) = \frac{1}{N+1} \sum_{j \in \tilde{N}_b(i)} F'(i) $$
$$ F'^{(f_a,f_b,m) }_i  = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)} 
f_a( min(  r(i,j), r(i,k) ) ) f_b ( max(  r(i,j), r(i,k) )) cos(l\theta(j,i,k)) $$

変数$a$は、隣接粒子で平均化を行う回数。
変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
関数$f_a, f_b$は、距離を引数とする何かの関数である。
変数$l$は、角度の係数である。
変数$\theta(j,i,k)$はベクトル${\boldsymbol r}(i,j)$とベクトル${\boldsymbol r}(i,k)$との角度である。

本研究では、関数$f_a, f_b$として、$\{ \sqrt{r}, r, r^2, [1 - \exp\{-(r-3.0)^2 / (2* 1.5^2)\}],  [0.5 + 0.5 * \exp\{-(r-3.0)^2 / (2 * (1.5)^2) \} ] \}$ を使用した。
変数$l$として、$\{ 1, 2, 3, 4, 6, 8, (180/109.5) , 2(180/109.5), 3(180/109.5), 4(180/109.5), 6(180/109.5)  \}$ を使用した。

# $I$ : tetrahedron order parameter (TOP)

Tetrahedron order parameter $I$ は以下の式で計算される。[@CHAU1998][@Duboue-Dijon2015]

$$ I(i) = \frac{1}{N+1} \sum_{j \in \tilde{N}_b(i)} I'(i) $$
$$ I'(i) = 1 - \frac{3}{8} \sum_{ j > k \in N_b(i) }\{ \cos( \theta(j,i,k)) + 1/3 \}^2  $$

変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は粒子$i$を含む$N+1$個の隣接粒子のリストである。
変数$\theta(j,i,k)$はベクトル${\boldsymbol r}(i,j)$とベクトル${\boldsymbol r}(i,k)$との角度である。


# $Q$ : Bond order parameter

Bond order parameter $Q$ は以下の式で計算される。[@Lechner2008]

$$ Q_l(i) = \sqrt{\frac{4\pi}{2l+1}\sum_{m=-l}^{l}|q'_{lm}(i)|^2}$$
$$ q'_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q_{lm}(j) $$
$$ q_{lm}(i) = \frac{1}{N}  \sum_{j \in N_b(i)} Y_{lm}(\theta(i,j), \phi(i,j)) $$

変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のリストである。
関数$Y$は、パラメータ$l$の球面調和関数である。
変数$\theta(i,j), \phi(i,j)$はベクトル${\boldsymbol r}(i,j)$の球面座標系での表現における角度で、$\theta$は$z$軸からの角度、$\phi$は$x$軸からの角度である。

本研究では、球面調和関数のパラメータ$l$として、$\{2, 3, 4, 5, 6, 8, 10, 12, 14, 16\}$を使用した。

# $W$ : Bond order parameter

Bond order parameter $W$ は以下の式で計算される。[@Lechner2008]

$$ W_l(i) = \frac{\sum_{m_1+m_2+m_3=0}
\left( \begin{array}{ccc}
  l & l & l \\
  m_1 & m_2 & m_3
\end{array} \right) 
q_{lm 1}(i) q_{lm_2}(i) q_{lm_3}(i) }{ \left( \sum_{m=-l}^{l} |q_{lm}(i)|^2  \right)^{3/2}  }$$
$$ q_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q'_{lm}(j) $$
$$ q'_{lm}(i) = \frac{1}{N} \sum_{j \in N_b(i)} Y_{lm}(\theta(i,j), \phi(i,j)) $$

変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
変数$\tilde{N}_b(i)$は$N_b(i)$に粒子$i$自身を追加した$N+1$個の粒子のリストである。
関数$Y$は、パラメータ$l$の球面調和関数である。
変数$\theta(i,j), \phi(i,j)$はベクトル${\boldsymbol r}(i,j)$の球面座標系での表現における角度で、$\theta$は$z$軸からの角度、$\phi$は$x$軸からの角度である。
変数$m_1,m_2,m_3$は$-l$から$l$までの値をとるが、$m_1+m_2+m_3=0$の時だけ計算される。
行列$\left( \begin{array}{ccc} l & l & l \\ m_1 & m_2 & m_3 \end{array} \right)$はWigner 3-$j$ symbolである。

本研究では、球面調和関数のパラメータ$l$として、$\{2,4,6,8,10,12,14,16\}$を使用した。

# $LQ$ : local Bond order parameter

local Bond order parameter $LQ$は以下の式で計算される。[@Moore2010][@Fitzner2020]

$$ LQ_l(i) = \frac{1}{N} \sum_{j \in N_b(i)}  \frac{ Re( \sum_{m=-l}^{l} q_{lm}(i) q^\ast_{lm}(j) ) }{ | q_{lm}(i) | | q_{lm}(j) | } $$
$$ q_{lm}(i) = \frac{1}{N} \sum_{j \in N_b(i)} Y_{lm}(\theta(i,j), \phi(i,j)) $$

変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
関数$Y$は、パラメータ$l$の球面調和関数である。
変数$\theta(i,j), \phi(i,j)$はベクトル${\boldsymbol r}(i,j)$の球面座標系での表現における角度で、$\theta$は$z$軸からの角度、$\phi$は$x$軸からの角度である。

本研究では、球面調和関数のパラメータ$l$として、$\{2,4,6,8,10,12,14,16\}$を使用した。

# $LW$ : local Bond order parameter

$$ LW_l(i) = \frac{\sum_{m_1+m_2+m_3=0}
\left( \begin{array}{ccc}
  l & l & l \\
  m_1 & m_2 & m_3
\end{array} \right) 
lq_{lm_1}(i) lq_{lm_2}(i) lq_{lm_3}(i) }{ \left( \sum_{m=-l}^{l} |lq_{lm}(i)|^2  \right)^{3/2}  }$$
$$ lq_{lm}(i) = \frac{1}{N}\sum_{j \in N_b(i)} \frac{q_{lm}(i) q^{\ast}_{lm}(j)}{ | q_{lm}(i) | |  q_{lm}(j) | } $$

変数$N_b(i)$は粒子$i$の$N$個の隣接粒子のリストである。
関数$Y$は、パラメータ$l$の球面調和関数である。
変数$\theta(i,j), \phi(i,j)$はベクトル${\boldsymbol r}(i,j)$の球面座標系での表現における角度で、$\theta$は$z$軸からの角度、$\phi$は$x$軸からの角度である。

本研究では、球面調和関数のパラメータ$l$として、$\{2,4,6,8,10,12,14,16\}$を使用した。

# Reference

