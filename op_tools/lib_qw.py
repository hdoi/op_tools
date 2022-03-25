# -*- coding: utf-8 -*-

import math
import numpy as np
from scipy.special import sph_harm as _sph_harm
from sympy.physics.wigner import wigner_3j


def gen_wigner3j(l_sph):
    l2 = 2*l_sph + 1
    wig = [[[0.0 for m1 in range(l2)] for m2 in range(l2)] for m3 in range(l2)]
    for m1 in range(-l_sph, l_sph+1):
        for m2 in range(-l_sph, l_sph+1):
            m3 = -m1 - m2
            if -l_sph <= m3 and m3 <= l_sph:
                wig[m1][m2][m3] = float(
                    wigner_3j(l_sph, l_sph, l_sph, m1, m2, m3))
    return wig


def func_to_value_wigner(l_sph, wigner3j, func):
    sum_vec = 0.0
    for m1 in range(-l_sph, l_sph+1):
        for m2 in range(-l_sph, l_sph+1):
            m3 = -m1 - m2
            if -l_sph <= m3 and m3 <= l_sph:
                wig = wigner3j[m1][m2][m3]
                sum_vec += wig * np.real(func[m1]*func[m2]*func[m3])

    sum_norm2 = 0.0
    for i_j in range(-l_sph, l_sph + 1):
        comp = func[i_j]
        sum_norm2 += np.real(comp*np.conjugate(comp))
    sum_norm = pow(sum_norm2, 3.0/2.0)

    if sum_norm != 0.0:
        w_value = np.real(sum_vec) / sum_norm
    else:
        w_value = 0.0
    return round(w_value, 14)


def sph_harm(l_sph, m_sph, theta, phi):
    return _sph_harm(m_sph, l_sph, phi, theta)


def calc_q(l_sph, theta, phi):
    q_l = [0 for i in range(2 * l_sph + 1)]
    for m_sph in range(l_sph + 1):
        q_l[m_sph] = sph_harm(l_sph, m_sph, theta, phi)
    for m_sph in range(-l_sph, 0):
        q_l[m_sph] = ((-1)**m_sph) * np.conjugate(sph_harm(l_sph, m_sph, theta, phi))
    return q_l

def calc_q_weighted(l_sph, theta, phi, weight):
    q_l = [0 for i in range(2 * l_sph + 1)]
    for m_sph in range(l_sph + 1):
        q_l[m_sph] = weight*sph_harm(l_sph, m_sph, theta, phi)
    for m_sph in range(-l_sph, 0):
        q_l[m_sph] = weight*((-1)**m_sph) * \
            np.conjugate(sph_harm(l_sph, m_sph, theta, phi))
    return q_l


def func_to_value(l_sph, func):
    sum_norm2 = 0.0
    for i_j in range(2 * l_sph + 1):
        comp = func[i_j]
        sum_norm2 += np.real(comp * np.conjugate(comp))
    q_value = math.sqrt(sum_norm2 * (4.0 * math.pi) / (2.0 * l_sph + 1.0))
    return round(q_value, 14)


