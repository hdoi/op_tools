---
title: "User manual for op_tools ver 0.2.0"
date: "April 2022"
author: "Hideo Doi"
---

\newpage

# What is this?

A python module for analyzing crystal structures in molecular and particle simulations.
The environment surrounding each particle or atom is evaluated and converted into a numerical value.
These values are also called [order parameters](https://en.wikipedia.org/wiki/Phase_transition#Order_parameters).
Particles in the similar environment will have the same numerical value, while particles in the different environment will not have it.
For body-centered cubic (BCC) and face-centered cubic (FCC) lattices, the order parameter is known to have a specific value, which can be used to determine.
For example, the location of the boundary between solid and liquid.
This type of analysis is used in simulations of melting solid metals and in the analysis of grain boundaries of crystals.


# How to install

$ git clone https://github.com/hdoi/op_tools.git
$ cd op_tools  
$ pip install -e .  

# data requirement
  1. coord                     : List of coordinates of each particles.  Such as [ [0,0,0], [0,0,1], ... ] like [[x1, y1, z1], [x2, y2, z2], ... ]  
  2. direct (optional)         : Direction vector of each particle. It may be a three-dimensional unit vector or a quaternion. Such as [[1,0,0], ...] or [[1,0,0,0], ....]  
    In the case of a three-dimensional unit vector, the order is [x, y, z]. In the case of quaternions, the order is [w, x, y, z].
    In the case of a mass point or spherical particle, It has no direction vector. There is no problem with direct = [].
  3. box_length                : The length of the simulation box. Such as [3, 3, 3]
  4. op_settings : Settings for calculating each order parameter


# Common settings for all order parameters

## Neibhorhood particle setting

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

###  Setting for neighborhood radius

```
  op_settings = {
    'radius' : [1.5, 1.75] ,  
    ... ( other parameter settings ) }
```
User can specify in the list format, and it is also possible to specify multiple conditions at the same time.
In the above example, the radius setting is 1.5 and 1.75. ..

###  Setting for the number of neighborhood particles

```
  op_settings = {
    'neighbor' : [8, 12] ,  
    ... ( other parameter settings ) }
```
User can specify in the list format, and it is also possible to specify multiple conditions at the same time.
In the above example, the number of neighborhood particles setting is 8 and 12. ..

###  Setting for Delaunay partitioning

```
  op_settings = {
    'Delaunay': ['standard']
    ... ( other parameter settings ) }
```
In the above example, Delauneay partitioning is used.

## Setting for the number of times for averaging

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

```
  op_settings = {
    'ave_times'      : 1, 
    ... ( other parameter settings )
     }
```

# List of order parameters

## $A$ : neighborhood parameters

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

Bond angle analysis $B$ is calculated as follows. [@Ackland2006]

$$ B^{(a=0,m,n,\phi)}(i) = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)  }f^{(m,n,\phi)}(\theta_{jik}) $$
$$ f^{(m,n,\phi)}(\theta_{jik}) = cos^{n} (m\theta_{jik} + \phi) $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $\theta_{jik}$ is the angle between vector ${\boldsymbol r}_{ij}$ and vector ${\boldsymbol r}_{ik}$.
The variable $m$ is the coefficient of the angle.
The variable $n$ is the exponent of the cos function.
The variable $\phi$ is the angle for the function correction.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.

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

centrosymmetry parameter $C$ is calculated as follows.[@Kelchner1998]

$$ C^{(a=0,type='half',mode)}(i) = \sum_{j \in M_b(i)} | {\boldsymbol r}_{ij} + {\boldsymbol r}_{ik}|^2$$
$$ C^{(a=0,type='all',mode)}(i)  = \sum_{j \in N_b(i)} | {\boldsymbol r}_{ij} + {\boldsymbol r}_{ik}|^2$$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $M_b(i)$ is the list of $N/2$ nearest neighbors of particle $i$.
The variable $mode$ is indicating how to determine particle $K$.
When the variable $mode$ is 'dist'$, particle $k$ is the particle in the list $N_b(i)$ nearest from the coordinate $r'_j$, opposite side of particle $r_i$.
When the variable $mode$ is 'angle', particle $k$ is the particle in the list $N_b(i)$ whose angle $\theta_{jik}$ is closest to $\pi$.
Two methods were implemented for use with liquids as well as solids.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.

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

neighbor distance analysis $D$ is calculated as follows. [@Stukowski2012]

$$ D^{(a=0,f_{ij},f_{ik},f_{jk})}_i = \frac{1}{N(N-1)/2} \sum_{j > k \in N_b(i)} f_{ij}(r_{ij}) f_{ik}( r_{ik}) f_{jk}( r_{jk}) $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The functions $f_{ij}(r_{ij}), f_{ik}(r_{ik}), f_{jk}(r_{jk})$ are some function with distance as argument and return value.
The variables $r_{ij},r_{ik},r_{jk}$ are the distances of the vectors ${\boldsymbol r}_{ij} ,{\boldsymbol r}_{ik} ,{\boldsymbol r}_{jk}$ respectively.
The distances also satisfy $ r_{ij} <= r_{ik}$.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.
The following example is for the function $\{f_{ij}(r), f_{ik}(r), f_{jk}(r) \} = r$.

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

Tetrahedron order parameter $I$ is calculated as follows. [@CHAU1998][@Duboue-Dijon2015]

$$ I^{(a=0)}(i) = 1 - \frac{3}{8} \sum_{ j > k \in N_b(i) }\{ \cos( \theta_{jik})+ 1/3 \}^2  $$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $\theta_{jik}$ is the angle between the vector ${\boldsymbol r}_{ij}$ and the vector ${\boldsymbol r}_{ik}$.

The following example shows the conditions for calculating the order parameter with 4 neighborhood particles and 2.0 adjacency radius.

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

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
The variable $\tilde{N}_b(i)$ is a list of $N+1$ particles with particle $i$ itself added to $N_b(i)$.
The variable $b$ is the number of times the spherical harmonic function is averaged over adjacent particles.
The function $Y$ is the spherical harmonic function.
The variables $\theta_{ij}, \phi_{ij}$ are angles in the spherical coordinate system representation of vector ${\boldsymbol r}_{ij}$, where $\theta$ is the angle from the $z$ axis and $\phi$ is the angle from the $x$ axis.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'l_in_Q': [4],
  'b_in_Q': 1,
  'analysis_type': ['Q'] }
```

Steinhardt's order parameter [@Steinhardt1983] can be calculated with the following setting.

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q' : [4,6],
  'b_in_Q' : 0,
  'analysis_type' : ['Q'] }
```

Lechner's order parameter [@Lechner2008] can be calculated with the following setting.

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
The matrix $\left( \begin{array}{ccc} l & l & l \{m_1 & m_2 & m_3 \end{array} \right)$ is a Wigner 3-$j$ symbol.

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 1,
  'l_in_Q': [4],
  'b_in_Q': 1,
  'analysis_type': ['W'] }
```

Steinhardt's order parameter [@Steinhardt1983] can be calculated with the following setting.

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q': [4,6],
  'b_in_Q': 0,
  'analysis_type': ['W'] }
```

Lechner's order parameter [@Lechner2008] can be calculated with the following setting.

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q': [4,6],
  'b_in_Q': 1,
  'analysis_type': ['W'] }
```

## $Q2, W2$ : function weighting Bond order parameter

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

```
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

```
op_settings = {
  'neighbor': [12],
  'radius': [2.0],
  'ave_times': 0,
  'l_in_Q': [4,6],
  'b_in_Q': 0,
  'analysis_type': ['LQ', 'LW'] }
```



## $S$ : Onsager's parameter

Onsager's order parameter $S$ is calculated as follows. [@Onsager1949][@Zannoni1979]

$$ S^{(a=1,n)}(i) = \frac{ \sum_{j \in N_b(i)} {P_n(\cos( \theta ))} }{N}$$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
関数$P_n$は[Legendre polynomial](https://en.wikipedia.org/wiki/Legendre_polynomials)である。
変数$n$はDegree of the polynomialで偶数である。
変数$\theta$は、粒子$i$の持つ方向ベクトル${\boldsymbol u}(i)$と粒子$j$の持つ方向ベクトル${\boldsymbol u}(j)$との角度である。
変数$\cos(\theta)$は通常、${\boldsymbol u}(i) \cdot {\boldsymbol u}(j)$で計算される。

$n = 2, 4$の時、オーダーパラメータ $S$ はそれぞれ以下の式で計算される。
$$ S^{(a=1, n=2)}(i) = \frac{ \sum_{j \in N_b(i)} { [ 3 \cos^2(\theta) - 1]/2 } }{N} $$
$$ S^{(a=1, n=4)}(i) = \frac{ \sum_{j \in N_b(i)} { [ 35 \cos^4(\theta) -30 \cos^2(\theta) + 3  ]/8 } }{N} $$


The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.
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

$$ T^{(a=0,n)}(i) = \frac{ \sum_{j \in N_b(i)}{ \cos( 2 \pi z(i,j) / d ) P_n(\cos( \theta )) }   }{N}$$

The variable $a$ is the number of times to perform averaging the value amoung neighborhood particles.
The list $N_b(i)$ is the list of $N$ neighborhood particles of particle $i$.
関数$P_n$は[Legendre polynomial](https://en.wikipedia.org/wiki/Legendre_polynomials)です。変数$n$はDegree of the polynomialです。
変数$\theta$は、粒子$i$の持つ方向ベクトル${\boldsymbol u}_i$と粒子$j$の持つ方向ベクトル${\boldsymbol u}_j$との角度です。
変数$z(i,j)$は、粒子$i$を通過し、ベクトル${\boldsymbol u}_i$と垂直な平面$P$から、粒子$j$$までの距離です。
変数$d$は、液晶のsmectic相の層から層までの距離です。

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

## $Z$ : user define order parameter

ユーザーが定義するためのオーダーパラメータ $Z$ を用意している。

The following example shows the conditions for calculating the order parameter with 12 neighborhood particles and 2.0 adjacency radius.
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
  order_param_data['Q_N6_a=1_b_1']
```

- Q : オーダーパラメータの種類
- N6 : 隣接粒子の条件
- 'a=1_b=1' : オーダーパラメータの計算に使用したパラメータ



# Reference

