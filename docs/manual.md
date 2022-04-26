# op_tools ver0.2.0 User Manual

date: "2022 04/01"
author: "Hideo Doi" (doi.hideo.chemistry@gmail.com)

\newpage

### What is this?

A python module for analyzing crystal structures in molecular and particle simulations.
The environment surrounding each particle or atom is evaluated and converted into a numerical value.
These values are also called [order parameters](https://en.wikipedia.org/wiki/Phase_transition#Order_parameters).
Particles in the similar environment will have the same numerical value, while particles in the different environment will not have it.
For body-centered cubic (BCC) and face-centered cubic (FCC) lattices, the order parameter is known to have a specific value, which can be used to determine.
For example, the location of the boundary between solid and liquid.
This type of analysis is used in simulations of melting solid metals and in the analysis of grain boundaries of crystals.

### How to install

```bash
git clone https://github.com/hdoi/op_tools.git
cd op_tools
pip install -e .
```

### data requirement

  1. coord                     : List of coordinates of each particles.  Such as [ [0,0,0], [0,0,1], ... ] like [[x1, y1, z1], [x2, y2, z2], ... ]
  2. direct (optional)         : Direction vector of each particle. It may be a three-dimensional unit vector or a quaternion. Such as [[1,0,0], ...] or [[1,0,0,0], ....]
    In the case of a three-dimensional unit vector, the order is [x, y, z]. In the case of quaternions, the order is [w, x, y, z].
    In the case of a mass point or spherical particle, It has no direction vector. There is no problem with direct = [].
  3. box_length                : The length of the simulation box. Such as [3, 3, 3]
  4. op_settings : Settings for calculating each order parameter

## Common settings for all order parameters

### Neibhorhood particle setting

The numerical value of the order parameter for each particle is calculated using the coordinates of nearby particles.
The particles near a particle $i$ are called the neighborhood particles.
There are three methods implemented in this program to determine the neighborhood particles.
The first method is to consider a particle to be an adjacent particle of particle $i$ if it is within a certain distance (adjacency radius) from particle $i$.
The advantage of this method is that it is relatively easy to implement and user-friendly.
The disadvantages are that the number of neighborhood particles may be different for each particle and that it is scale dependent.
For example, specifying an adjacency radius of 1 nm and 1 angstrom will give different results.
This is called scale-dependency.
The second method is to use $n$ particles close to particle $i$ as neighbors.
The advantage is that there is no scale-dependency and the adjacent particles do not change if the length unit changes, because the relationship of distance is unchanged.
The disadvantages are that it is not easy to implement, the computational cost is slightly higher, and it is not widely used.
The third method is Delaunay partitioning ([Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram)).
After performing the Voronoi partitioning, two particles sharing each Voronoi facet are considered as adjacent particles.

#### Setting for neighborhood radius

```python
  op_settings = {
    'radius' : [1.5, 1.75] ,
    ... ( other parameter settings ) }
```

User can specify in the list format, and it is also possible to specify multiple conditions at the same time.
In the above example, the radius setting is 1.5 and 1.75. ..

#### Setting for the number of neighborhood particles

```python
  op_settings = {
    'neighbor' : [8, 12] ,
    ... ( other parameter settings ) }
```

User can specify in the list format, and it is also possible to specify multiple conditions at the same time.
In the above example, the number of neighborhood particles setting is 8 and 12. ..

#### Setting for Delaunay partitioning

```python
  op_settings = {
    'Delaunay': ['standard']
    ... ( other parameter settings ) }
```

In the above example, Delauneay partitioning is used.

### Setting for the number of times for averaging

When the classification performance of the order parameter of each particle does not enough performance, to increase the performance, user can perform the averaging calculation.
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

```python
  op_settings = {
    'ave_times'      : 1,
    ... ( other parameter settings )
     }
```

## List of order parameters

### $A$ : neighborhood parameters

common neighborhood parameter $A$ [@Honeycutt1987], predominant common neighborhood parameter $P$ [@Radhi2017],  another predominant common neighborhood parameter $N$ [@Radhi2017] are calculated using very similar formulas.
Order paraemter $P$ and $N$ are implemented as a another type of order parameter $A$.

$$ A^{(a=0,type=A,m)}(i) = A^{(a=0,m)}(i) = \frac{1}{N} \sum_{j \in N_b(i)} | \sum_{k \in N_b(i,j)} ( {\boldsymbol r}_{ik} + {\boldsymbol r}_{jk}) |^2 $$
$$ A^{(a=0,type=P,m)}(i) = P^{(a=0,m)}(i) = \frac{1}{N} \sum_{j \in N_b(i)} | \sum_{k \in N_b(i,j)} ( {\boldsymbol r}_{ij} + {\boldsymbol r}_{kj}) |^2 $$
$$ A^{(a=0,type=N,m)}(i) = N^{(a=0,m)}(i) = \frac{1}{N}|\sum_{j \in N_b(i)}   \sum_{k \in N_b(i,j)} ( {\boldsymbol r}_{ij} + {\boldsymbol r}_{kj} ) |^2 $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The list $N_b(i,j)$ is the list of $m$ nearest neighborhood particles from particle $i$ and particle $j$.
The variable $type$ specifies the type of order parameter.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.

```python
op_param = {
  'neighbor': [12],
  'radius': [1.5],
  'ave_times': 1,
  'm_in_A': [2],
  'types_in_A': ['A', 'P', 'N'],
  'analysis_type': ['A']}
```

### $B$ : bond angle analysis (BAA)

Bond angle analysis $B$ is calculated as follows. [@Ackland2006]

$$ B^{(a=0,m,n,\phi)}(i) = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)  }f^{(m,n,\phi)}(\theta_{jik}) $$
$$ f^{(m,n,\phi)}(\theta_{jik}) = cos^{n} (m\theta_{jik} + \phi) $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $\theta_{jik}$ is the angle between vector ${\boldsymbol r}_{ij}$ and vector ${\boldsymbol r}_{ik}$.
The variable $m$ is the coefficient of the angle.
The variable $n$ is the exponent of the cos function.
The variable $\phi$ is the intercept of angle.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.

```python
op_param = {
  'neighbor': [12],
  'radius': [1.5],
  'ave_times': 1,
  'm_in_B': [2],
  'phi_in_B': [0],
  'n_in_B': [1, 2],
  'analysis_type': ['B']}
```

### $C$ : centrosymmetry parameter analysis (CPA)

centrosymmetry parameter $C$ is calculated as follows.[@Kelchner1998]

$$ C^{(a=0,type='half',mode)}(i) = \sum_{j \in M_b(i)} | {\boldsymbol r}_{ij} + {\boldsymbol r}_{ik}|^2$$
$$ C^{(a=0,type='all',mode)}(i)  = \sum_{j \in N_b(i)} | {\boldsymbol r}_{ij} + {\boldsymbol r}_{ik}|^2$$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $M_b(i)$ is the list of $N/2$ nearest neighbors of particle $i$.
The variable $type$ is a variable that specifies the number of times to add vectors.
The variable $mode$ is indicating how to determine particle $K$.
When the variable $mode$ is 'dist'$, particle $k$ is the particle in the list $N_b(i)$ nearest from the coordinate $r'_j$, opposite side of particle $r_i$.
When the variable $mode$ is 'angle', particle $k$ is the particle in the list $N_b(i)$ whose angle $\theta_{jik}$ is closest to $\pi$.
Two methods were implemented for use with liquids as well as solids.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.

```python
op_param = {
    'neighbor': [12],
    'radius': [2.0],
    'ave_times': 1,
    'types_in_C' : ['half'],
    'modes_in_C' : ['dist'],
    'analysis_type': ['C']}
```

### $D$ : neighbor distance analysis (NDA)

neighbor distance analysis $D$ is calculated as follows. [@Stukowski2012]

$$ D^{(a=0,f_{ij},f_{ik},f_{jk})}_i = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)} f_{ij}(r_{ij}) f_{ik}( r_{ik}) f_{jk}( r_{jk}) $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The functions $f_{ij}(r_{ij}), f_{ik}(r_{ik}), f_{jk}(r_{jk})$ are some function with distance as argument and return value.
The variables $r_{ij},r_{ik},r_{jk}$ are the distances of the vectors ${\boldsymbol r}_{ij} ,{\boldsymbol r}_{ik} ,{\boldsymbol r}_{jk}$ respectively.
The distances also satisfy $ r_{ij} <= r_{ik}$.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.
The following example is for the function $\{f_{ij}(r), f_{ik}(r), f_{jk}(r) \} = r$.

```python
def f_1(r):
    return r

op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'function': [f1],
  'analysis_type': ['D'] }
```

### $F$ : angular Fourier series (AFS) like parameter

angular Fourier series parameter $F$ is calculated as follows. [@Bartok2013][@Seko2018]

$$ F^{(a=0,f_{1},f_{2},m) }_i  = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)} f_{1}( r_{ij} ) f_{2}( r_{ik} ) cos(l\theta_{jik}) $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The function $f^1(r), f^2(r)$ is some function with distance as argument and value as return value.
The variable $l$ is the coefficient of the angle.
The variable $\theta_{jik}$ is the angle between vector ${\boldsymbol r}_{ij}$ and vector ${\boldsymbol r}_{ik}$.
The distance satisfies $r_{ij} <= r_{ik}$.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.
The following example is for the function $\{f_{ij}(r), f_{ik}(r) \} = r$.

```python
def f_1(r):
    return r

op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'l_in_F': [1],
  'function': [f1],
  'analysis_type': ['F']}
```

### $H$ : angle histogram analysis (AHA)

angle histogram analysis $H$は次の式で計算される。

$$ h^{(b=0, bin)}(i) = \frac{1}{N(N-1)/2} \sum_{j>k \in N_b(i)} histogram^{(bin)}(\theta_{jik} ) $$
$$ h^{(b, bin)}(i)  = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}h^{(b-1, bin)}(j) $$
$$ H^{(a=0, b, bin, \nu)}(i) = FFT_{ amplitude }( h^{(b, bin)}(i)) \delta(X - \nu) $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $\tilde{N}_b(i)$ is a list of $N+1$ particles with particle $i$ itself added to the variable $N_b(i)$.
The variable $b$ is the number of times the histogram of each particle is averaged with the histograms of its neighboring particles.
The variable $\theta_{jik}$ is the angle between the vector ${\boldsymbol r}_{ij}$ and the vector ${\boldsymbol r}_{ik}$.
The function $histogram$ creates a histogram of the number of bins $bin$.
The function $FFT_{amplitude}$ computes amplitude by Fourier transforming the histogram.
The function $\delta$ is the Dirac delta function.
The variable $\nu$ is the frequency component of the histogram after the Fourier transform.
This is because the delta function $\delta$ becomes 1 only when the frequency component $X$ is the same as $\nu$.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.

```python
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'b_in_H': 1,
  'bin_in_H': [24],
  'nu_in_H': [3],
  'analysis_type': ['H'] }
```

### $I$ : tetrahedron order parameter (TOP)

Tetrahedron order parameter $I$ is calculated as follows. [@CHAU1998][@Duboue-Dijon2015]

$$ I^{(a=0)}(i) = 1 - \frac{3}{8} \sum_{ j > k \in N_b(i) }\{ \cos( \theta_{jik})+ 1/3 \}^2  $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $\theta_{jik}$ is the angle between the vector ${\boldsymbol r}_{ij}$ and the vector ${\boldsymbol r}_{ik}$.

The following example shows the conditions for calculating the order parameter with 4 neighborhood particles and 2.0 adjacency radius.

```python
op_settings = {
  'neighbor': [4],
  'radius': [2.0],
  'ave_times': 1,
  'analysis_type': ['I'] }
```

### $Q$ : Bond order parameter

Bond order parameter $Q$ is calculated as follows. [@Steinhardt1983][@Lechner2008]

$$ Q^{(l,a=0,b)}_i = \sqrt{\frac{4\pi}{2l+1}\sum_{m=-l}^{l}|q^{(l,a=0,b)}_{lm}(i)|^2}$$
$$ q^{(l,a=0,b)}_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q^{(l,a=0,b-1)}_{lm}(j) $$
$$ q^{(l,a=0,b=1)}_{lm}(i) = \frac{1}{N} \sum_{j \in N_b(i)} Y_{lm}(\theta_{ij}, \phi_{ij}) $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $\tilde{N}_b(i)$ is a list of $N+1$ particles with particle $i$ itself added to $N_b(i)$.
The variable $b$ is the number of times the spherical harmonic function is averaged over adjacent particles.
The function $Y$ is the spherical harmonic function.
The variables $\theta_{ij}, \phi_{ij}$ are angles in the spherical coordinate system representation of vector ${\boldsymbol r}_{ij}$, where $\theta$ is the angle from the $z$ axis and $\phi$ is the angle from the $x$ axis.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.

```python
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'l_in_Q': [4],
  'b_in_Q': 1,
  'analysis_type': ['Q'] }
```

Steinhardt's order parameter [@Steinhardt1983] can be calculated with the following setting.

```python
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q' : [4,6],
  'b_in_Q' : 0,
  'analysis_type' : ['Q'] }
```

Lechner's order parameter [@Lechner2008] can be calculated with the following setting.

```python
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q' : [4,6],
  'b_in_Q' : 1,
  'analysis_type' : ['Q'] }
```

### $W$ : Bond order parameter

Bond order parameter $W$ is calculated as follows. [@Steinhardt1983][@Lechner2008]

$$ W^{(l,a=0,b)}_i = \frac{\sum_{m_1+m_2+m_3=0}
\left( \begin{array}{ccc}
  l & l & l \\
  m_1 & m_2 & m_3
\end{array} \right)
q^{(l,a=0,b)}_{lm_1}(i) q^{(l,a=0,b)}_{lm_2}(i) q^{(l,a=0,b)}_{lm_3}(i) }{ \left( \sum_{m=-l}^{l} |q^{(l,a=0,b)}_{lm}(i)|^2  \right)^{3/2}  }$$
$$ q^{(l,a=0,b)}_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q^{(l,a=0,b-1)}_{lm}(j) $$
$$ q^{(l,a=0,b=0)}_{lm}(i) = \frac{1}{N} \sum_{j \in N_b(i)} Y_{lm}(\theta_{ij}, \phi_{ij}) $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $\tilde{N}_b(i)$ is a list of $N+1$ particles with particle $i$ itself added to $N_b(i)$.
The variable $b$ is the number of times the spherical harmonic function is averaged over adjacent particles.
The function $Y$ is the spherical harmonic function.
Variables $\theta_{ij}, \phi_{ij}$ are angles in the spherical coordinate system representation of vector ${\boldsymbol r}_{ij}$, where $\theta$ is the angle from the $z$ axis and $\phi$ is the angle from the $x$ axis.
The variables $m_1,m_2,m_3$ take values from $-l$ to $l$, but are calculated only when $m_1+m_2+m_3=0$.
The matrix $\left( \begin{array}{ccc} l & l & l \\ m_1 & m_2 & m_3 \end{array} \right)$ is a Wigner 3-$j$ symbol.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.

```python
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'l_in_Q': [4],
  'b_in_Q': 1,
  'analysis_type': ['W'] }
```

Steinhardt's order parameter [@Steinhardt1983] can be calculated with the following setting.

```python
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q': [4,6],
  'b_in_Q': 0,
  'analysis_type': ['W'] }
```

Lechner's order parameter [@Lechner2008] can be calculated with the following setting.

```python
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q': [4,6],
  'b_in_Q': 1,
  'analysis_type': ['W'] }
```

### $Q2, W2$ : function weighting Bond order parameter

$$ Q2^{(l,a=0,b)}_i = \sqrt{\frac{4\pi}{2l+1}\sum_{m=-l}^{l}|q^{(l,a=0,b)}_{lm}(i)|^2}$$
$$ q^{(l,a=0,b)}_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q^{(l,a=0,b-1)}_{lm}(j) $$
$$ q^{(l,a=0,b=0)}_{lm}(i) = \sum_{j \in N_b(i)} F(i,j) Y_{lm}( \theta_{ij}, \phi_{ij}) $$

A function $F(i,j)$ can be used to weight between particles $i$ and $j$.

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $\tilde{N}_b(i)$ is a list of $N+1$ particles with particle $i$ itself added to $N_b(i)$.
The variable $b$ is the number of times the spherical harmonic function is averaged over adjacent particles.
The function $Y$ is the spherical harmonic function.
The variables $\theta_{ij}, \phi_{ij}$ are the angles in the spherical coordinate system representation of the vector ${\boldsymbol r}_{ij}$, where $\theta$ is the angle from the $z$ axis and $\phi$ is the angle from the $x$ axis.

The order parameter $W2$ is calculated as follows.

$$ W2^{(l,a=0,b)}_i = \frac{\sum_{m_1+m_2+m_3=0}
\left( \begin{array}{ccc}
  l & l & l \\
  m_1 & m_2 & m_3
\end{array} \right)
q^{(l,a=0,b)}_{lm_1}(i) q^{(l,a=0,b)}_{lm_2}(i) q^{(l,a=0,b)}_{lm_3}(i) }{ \left( \sum_{m=-l}^{l} |q^{(l,a=0,b)}_{lm}(i)|^2  \right)^{3/2}  }$$

If you use Delaunay partitioning, you can calculate Mickel's order parameter as follows. [@Mickel2013]

```python
def f1(j, voronoi_area_list, distance_list):
    weight = voronoi_area_list[j] / np.sum(voronoi_area_list)
    return weight

op_settings = {
  'Delaunay': ['standard'],
  'ave_times': 1,
  'l_in_Q': [4],
  'function_in_Q2': [f1],
  'analysis_type': ['Q2', 'W2'] }
```

In addition, you can use other weighting function, such as weighting based on distance.
The following example is a setting weighting function based on the distance.
The more distance is the more less weight.

```python
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

### $LQ, LW$ : local Bond order parameter

These order parameters ware implemented in imitation of [@Moore2010][@Fitzner2020][@Tribello2017].

$$ LQ^{(l,a=0,b)}_i = \frac{1}{N} \sum_{j \in N_b(i)} \frac{ q^{(l,a,b)}_{lm}(i,j) }{ | q^{(l,a,b)}_{lm}(i) | | q^{(l,a,b)}_{lm}(j) |} $$
$$ q^{(l,a,b)}_{lm}(i,j) = \sum_{m=-l}^{l} q^{(l,a,b)}_{lm}(i) q^{\ast(l,a,b)}_{lm}(j)  $$
$$ q^{(l,a=0,b)}_{lm}(i) = \frac{1}{N+1}\sum_{j \in \tilde{N}_b(i)}q^{(l,a=0,b-1)}_{lm}(j) $$
$$ q^{(l,a=0,b=0)}_{lm}(i) = \frac{1}{N} \sum_{j \in N_b(i)} Y_{lm}(\theta_{ij}, \phi_{ij}) $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $\tilde{N}_b(i)$ is a list of $N+1$ particles with particle $i$ itself added to $N_b(i)$.
The variable $b$ is the number of times the spherical harmonic function is averaged over adjacent particles.
The function $Y$ is the spherical harmonic function.
The variables $\theta_{ij}, \phi_{ij}$ are the angles in the spherical coordinate system representation of the vector ${\boldsymbol r}_{ij}$, where $\theta$ is the angle from the $z$ axis and $\phi$ is the angle from the $x$ axis.

$$ LW^{(l,a=0,b)}_i = \frac{\sum_{m_1+m_2+m_3=0}
\left( \begin{array}{ccc}
  l & l & l \\
  m_1 & m_2 & m_3
\end{array} \right)
lq^{(l,a=0,b)}_{lm_1}(i) lq^{(l,a=0,b)}_{lm_2}(i) lq^{(l,a=0,b)}_{lm_3}(i) }{ \left( \sum_{m=-l}^{l} |lq^{(l,a=0,b)}_{lm}(i)|^2  \right)^{3/2}  }$$
$$ lq^{(l,a,b)}_{lm}(i) = \frac{1}{N}\sum_{j \in N_b(i)} \frac{q^{(l,a,b)}_{lm}(i) q^{\ast(l,a,b)}_{lm}(j)}{ | q^{(l,a,b)}_{lm}(i) | |  q^{(l,a,b)}_{lm}(j) | } $$

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.
That calculate the similar order parameters in [@Moore2010].

```python
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q': [4,6],
  'b_in_Q': 0,
  'analysis_type': ['LQ', 'LW'] }
```

### $S$ : Onsager's parameter

Onsager's order parameter $S$ is calculated as follows. [@Onsager1949][@Zannoni1979]

$$ S^{(a=0,n)}(i) = \frac{ \sum_{j \in N_b(i)} {P_n(\cos( \theta ))} }{N}$$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The function $P_n$ is [Legendre polynomial](https://en.wikipedia.org/wiki/Legendre_polynomials).
The variable $N$ is Degree of the polynomial and is even.
The variable $\theta$ is the angle between the direction vector ${\boldsymbol u}(i)$ of particle $i$ and the direction vector ${\boldsymbol u}(j)$ of particle $j$.
The variable $\cos(\theta)$ is usually calculated by ${\boldsymbol u}(i)\cdot {\boldsymbol u}(j)$.

When $n = 2, 4$, the order parameter $S$ is calculated by the following equations, respectively.
$$ S^{(a=0, n=2)}(i) = \frac{ \sum_{j \in N_b(i)} { [ 3 \cos^2(\theta) - 1]/2 } }{N} $$
$$ S^{(a=0, n=4)}(i) = \frac{ \sum_{j \in N_b(i)} { [ 35 \cos^4(\theta) -30 \cos^2(\theta) + 3  ]/8 } }{N} $$

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.
Note that this order parameter requires the direction vector.

```python
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'n_in_S' : [2],
  'analysis_type' : ['S']
   }
```

### $T$ : McMillan's Sigma

McMillan's order parameter $T$ is calculated as follows. [@McMillan1971]

$$ T^{(a=0,n)}(i) = \frac{ \sum_{j \in N_b(i)}{ \cos( 2 \pi z(i,j) / d ) P_n(\cos( \theta )) }   }{N}$$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The function $P_n$ is [Legendre polynomial](https://en.wikipedia.org/wiki/Legendre_polynomials).
The variable $N$ is Degree of the polynomial and is even.
The variable $\theta$ is the angle between the direction vector ${\boldsymbol u}_i$ of particle $i$ and the direction vector ${\boldsymbol u}_j$ of particle $j$.
The variable $Z(i,j)$ is the distance from the plane $P$, which passes through particle $i$ and is perpendicular to the direction vector ${\boldsymbol u}_i$$, to particle $j$$.
The variable $D$ is the distance from layer to layer of the smectic phase of the liquid crystal.

When $n = 2$, the order parameter $T$ is calculated as follows.
$$ T^{(a=0,n=2)}(i) = \frac{ \sum_{j \in N_b(i)}{ \cos( 2 \pi z(i,j) / d ) [ 3 \cos^2(\theta) - 1 ]/2 }   }{N}$$

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.
Note that this order parameter requires the direction vector.

```python
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'n_in_T': [2],
  'd_in_T': [1.0],
  'analysis_type' : ['T']
   }
```

### $Z$ : user define order parameter

An order parameter $Z$ is provided for the user to define.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.

```python
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'analysis_type': ['Z'] }
```

The calculation part of the order parameter is op_tools/op_z_user_define.py.
It is possible to edit this file and implement the order parameter that the user has thought of.

## Setting for many types analysis
uj
This takes much time.

```python
  def f_1(r):
      return r
  op_settings = {
    # neighborhood particles settings
    'neighbor'       : [8],               # number of neighborhood particles
    'radius'         : [1.5],             # adjacency radius
    'ave_times'      : 1,                 # average time
    # A
    'op_types' : ['A','P','N'],    # specify the type of analysis in order parameter A
    'm_in_A'         : [2, 4],     # number of neighborhood particles from particle i and j
    # B
    'm_in_B' : [2],                # factor of angle
    'n_in_B': [1, 2],              # exponent of cos function
    'phi_in_B': [0],               # intercept of angle
    # C
    'types_in_C' : ['half'],       # number of vector adding
    'modes_in_C' : ['dist'],       # search method for opposite side particle
    # D
    'function': [f1]               # function
    # F
    'l_in_F' : [1],                # factor of angle
    # H
    'b_in_H' : 1,                  # number of averaging of angle histogram
    'bin_in_H' : [24],             # bin of histogram
    'nu_in_H' : [3],               # frequency components of angle, (pi/3)
    # I
    # Q
    'b_in_Q'         : 1,          # number of averaging of spherical harmonic function
    'l_in_Q'         : [2, 4, 6],  # parameter for spherical harmonic
    # Q2 W2
    'function_in_Q2' : [f2],       # weighting functin
    # LQ LW
    # S
    'n_in_S'         : [2],        # degree of Legendre_polynomials
    # T
    'n_in_T'         : [2],        # degree of Legendre_polynomials
    'd_in_T'         : [1.0],      # distance between layers of smectic phase
    'analysis_type': ['A', 'B', 'C', 'D', 'F', 'H', 'I',
    'Q', 'W', 'Q2', 'W2', 'LQ', 'LW', 'S', 'T']} # Order parameter types
```

## Output format

User can use as follows.

```python
  import order_tools
  order_param_data = \
    op_analyze(coord, direct, box_length, op_settings)
```

To access the order parameters for each particle,

```python
  order_param_data['Q_N6_a=1_b_1']
```

- Q : Types of order parameter
- N6 : setting of neighborhood particles
- 'a=1_b=1' : parameter of order parameter calculation

## Reference
