#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# made by githubuser qurn
#
# Permission to use, copy, modify, distribute, and sell this software and its
# documentation for any purpose is hereby granted without fee, provided that
# the above copyright notice appear in all copies and that both that copyright
# notice and this permission notice appear in supporting documentation, and
# that the name of the copyright holders not be used in advertising or
# publicity pertaining to distribution of the software without specific,
# written prior permission.  The copyright holders make no representations
# about the suitability of this software for any purpose.  It is provided "as
# is" without express or implied warranty.
#
# THE COPYRIGHT HOLDERS DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
# EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.

# Contains ported code from Xkeystone made by Keith Packard
# Copyright © 2008 Keith Packard

# Change this values to your configuration:
# mon
# B pixel width
# C pixel height

from subprocess import call
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import time
import sys

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35, top=0.76)

#  *  q0    q1 D = 0
#  *
#  *  q3    q2 C = 768
#     A=0   B=1366

global mon
mon = sys.argv
global A
global B
global C
global D
# x
A = 0
B = 1366
w = B-A

# y
C = 768
D = 0
H = C-D

q0x = A  # top left
q0y = D
q1x = B  # top right
q1y = D
q2x = B  # bottom right
q2y = C
q3x = A  # bottom left
q3y = C

x = np.array([q0x, q1x, q2x, q3x, q0x])
y = np.array([q0y, q1y, q2y, q3y, q0y])

x1 = np.array([q0x, q1x, q2x, q3x, q0x])
y1 = np.array([q0y, q1y, q2y, q3y, q0y])

l, = plt.plot(x1, y1, lw=2, color='red')
lm, = plt.plot(x, y, lw=1, color='green')
plt.axis([A-w/2, B+w/2, (C+H/2), (D-H/2)])

axcolor = 'lightgoldenrodyellow'

ax0x = plt.axes([0.05, 0.90, 0.25, 0.03], facecolor=axcolor)
ax0y = plt.axes([0.05, 0.86, 0.25, 0.03], facecolor=axcolor)
ax1x = plt.axes([0.65, 0.90, 0.25, 0.03], facecolor=axcolor)
ax1y = plt.axes([0.65, 0.86, 0.25, 0.03], facecolor=axcolor)
ax2x = plt.axes([0.65, 0.18, 0.25, 0.03], facecolor=axcolor)
ax2y = plt.axes([0.65, 0.14, 0.25, 0.03], facecolor=axcolor)
ax3x = plt.axes([0.05, 0.18, 0.25, 0.03], facecolor=axcolor)
ax3y = plt.axes([0.05, 0.14, 0.25, 0.03], facecolor=axcolor)

s0x = Slider(ax0x, 'q0x', -2000,  2000, valinit=q0x)
s0y = Slider(ax0y, 'q0y', -2000,  2000, valinit=q0y)
s1x = Slider(ax1x, 'q1x', -2000,  2000, valinit=q1x)
s1y = Slider(ax1y, 'q1y', -2000,  2000, valinit=q1y)
s2x = Slider(ax2x, 'q2x', -2000,  2000, valinit=q2x)
s2y = Slider(ax2y, 'q2y', -2000,  2000, valinit=q2y)
s3x = Slider(ax3x, 'q3x', -2000,  2000, valinit=q3x)
s3y = Slider(ax3y, 'q3y', -2000,  2000, valinit=q3y)


def update(val):

    global m00
    global m01
    global m02
    global m10
    global m11
    global m12
    global m20
    global m21
    global m22

    d0x = (A-s0x.val)
    d0y = (D-s0y.val)
    d1x = (B-s1x.val)
    d1y = (D-s1y.val)
    d2x = (B-s2x.val)
    d2y = (C-s2y.val)
    d3x = (A-s3x.val)
    d3y = (C-s3y.val)

    q0x = A+d0x  # top left
    q0y = D+d0y
    q1x = B+d1x  # top right
    q1y = D+d1y
    q2x = B+d2x  # bottom right
    q2y = C+d2y
    q3x = A+d3x  # bottom left
    q3y = C+d3y

    # preview rectangle
    Q0x = A-d0x  # top left
    Q0y = D-d0y
    Q1x = B-d1x  # top right
    Q1y = D-d1y
    Q2x = B-d2x  # bottom right
    Q2y = C-d2y
    Q3x = A-d3x  # bottom left
    Q3y = C-d3y

    xs = np.array([Q0x, Q1x, Q2x, Q3x, Q0x])
    ys = np.array([Q0y, Q1y, Q2y, Q3y, Q0y])

    l.set_xdata(xs)
    l.set_ydata(ys)
    fig.canvas.draw_idle()

    m02 = q0x
    m12 = q0y
    m22 = 1
    a = ((q2x - q3x)*(q1y - q2y) - (q2y - q3y)*(q1x - q2x)) * H
    b = (q2x - q1x - q3x + q0x) * (q1y - q2y) - (q2y - q1y - q3y + q0y) * (q1x - q2x)
    m21 = - b / a

    if (q1x != q2x):
        m20 = (m21 * (q2x - q3x) * H + q2x - q1x - q3x + q0x) / ((q1x - q2x) * w)
    else:
        m20 = (m21 * (q2y - q3y) * H + q2y - q1y - q3y + q0y) / ((q1y - q2y) * w)

    m00 = m20 * q1x + (q1x - q0x) / w
    m10 = m20 * q1y + (q1y - q0y) / w

    m01 = m21 * q3x + (q3x - q0x) / H
    m11 = m21 * q3y + (q3y - q0y) / H

    print(' ')
    print(' ', m00, ' ', m01, ' ', m02)
    print(' ', m10, ' ', m11, ' ', m12)
    print(' ', m20, ' ', m21, ' ', m22)
    print('xrandr --output {:s} --transform {:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}'.format(mon,m00, m01, m02, m10, m11, m12, m20, m21, m22))


s0x.on_changed(update)
s0y.on_changed(update)
s1x.on_changed(update)
s1y.on_changed(update)
s2x.on_changed(update)
s2y.on_changed(update)
s3x.on_changed(update)
s3y.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
resetbutton = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
applyax = plt.axes([0.2, 0.025, 0.1, 0.04])
applybutton = Button(applyax, 'Apply', color=axcolor, hovercolor='0.975')
testax = plt.axes([0.5-0.02, 0.025, 0.1, 0.04])
testbutton = Button(testax, 'Test', color=axcolor, hovercolor='0.975')


def reset(event):
    s0x.reset()
    s0y.reset()
    s1x.reset()
    s1y.reset()
    s2x.reset()
    s2y.reset()
    s3x.reset()
    s3y.reset()


def applyx(event):
    call(['xrandr', '--output', mon, '--transform', '%f,%f,%f,%f,%f,%f,%f,%f,%f' % (m00,m01,m02,m10,m11,m12,m20,m21,m22)])


def test(event):
    call(['xrandr', '--output', mon, '--transform', '%f,%f,%f,%f,%f,%f,%f,%f,%f' % (m00,m01,m02,m10,m11,m12,m20,m21,m22)])
    time.sleep(5)
    call(['xrandr', '--output', mon, '--transform', '1,0,0,0,1,0,0,0,1'])


resetbutton.on_clicked(reset)
applybutton.on_clicked(applyx)
testbutton.on_clicked(test)

plt.show()

# Math from Xkeystone by Keith Packard:
#
#  * Ok, given an source quad and a dest rectangle, compute
#  * a transform that maps the rectangle to q. That's easier
#  * as the rectangle has some nice simple properties. Invert
#  * the matrix to find the opposite mapping
#  *
#  *  q0    q1
#  *
#  *  q3    q2
#  *
#  *  | m00 m01 m02 |
#  *  | m10 m11 m12 |
#  *  | m20 m21 m22 |
#  *
#  *  m [ 0 0 1 ] = q[0]
#  *
#  * Set m22 to 1, and solve:
#  *
#  *  |     m02       ,     m12       , 1 | = | q0x, q0y, 1 |
#  *
#  *  | m00 * w + q0x   m10 * w + q0y     |
#  *  | ------------- , ------------- , 1 | = | q1x, q1y, 1 |
#  *  |  m20 * w + 1     m20 * w + 1      |
# 
#  *   m00*w + q0x = q1x*(m20*w + 1)
#  *   m00 = m20*q1x + (q1x - q0x) / w;
#  *
#  *   m10*w + q0y = q1y*(m20*w + 1)
#  *   m10 = m20*q1y + (q1y - q0y) / w;
#  *
#  *   m01*h + q0x = q3x*(m21*h + 1)
#  *   m01 = m21*q3x + (q3x - q0x) / h;
#  *
#  *   m11*h + q0y = q3y*(m21*h + 1)
#  *   m11 = m21*q3y + (q3y - q0y) / h
#  *
#  *   m00*w +                 m01*h +                 q0x = q2x*(m20*w + m21*h + 1)
#  *
#  *   m20*q1x*w + q1x - q0x + m21*q3x*h + q3x - q0x + q0x = m20*q2x*w + m21*q2x*h + q2x
#  *
#  *   m20*q1x*w - m20*q2x*w = m21*q2x*h - m21*q3x*h + q2x - q1x + q0x - q3x + q0x - q0x
#  *
#  *   m20*(q1x - q2x)*w     = m21*(q2x - q3x)*h     + q2x - q1x - q3x + q0x
#  *
#  *
#  *   m10*w +                 m11*h +                 q0y = q2y*(m20*w + m21*h + 1)
#  *
#  *   m20*q1y*w + q1y - q0y + m21*q3y*h + q3y - q0y + q0y = m20*q2y*w + m21*q2y*h + q2y
#  *
#  *   m20*q1y*w - m20*q2y*w = m21*q2y*h - m21*q3y*h + q2y - q1y + q0y - q3y + q0y - q0y
#  *
#  *   m20*(q1y - q2y)*w     = m21*(q2y - q3y)*h     + q2y - q1y - q3y + q0y
#  *
#  *
#  *   m20*(q1x - q2x)*(q1y - q2y)*w     = m21*(q2x - q3x)*(q1y - q2y)*h     + (q2x - q1x - q3x + q0x)*(q1y - q2y)
#  *
#  *   m20*(q1y - q2y)*(q1x - q2x)*w     = m21*(q2y - q3y)*(q1x - q2x)*h     + (q2y - q1y - q3y + q0y)*(q1x - q2x)
#  *
#  *   0                                 = m21*((q2x - q3x)*(q1y - q2y) - (q2y - q3y)*(q1x - q2x))*h + (stuff)
#  *                                     = m21 * a + b;
#  *
#  *   m21 = -(stuff) / (other stuff)
#  *
#  *   m20 = f(m21)
#  *
#  *  m00 = f(m20)
#  *  m10 = f(m20)
#  *
#  *  m01 = f(m21)
#  *  m11 = f(m21)
#  *
#  * done.
#  */
# m_t solve (q_t q, real w, real h)
# {
#     real    q0x = q[0].x, q0y = q[0].y;
#     real    q1x = q[1].x, q1y = q[1].y;
#     real    q2x = q[2].x, q2y = q[2].y;
#     real    q3x = q[3].x, q3y = q[3].y;
#     real    m00, m01, m02;
#     real    m10, m11, m12;
#     real    m20, m21, m22;
# 
#     m02 = q0x;
#     m12 = q0y;
#     m22 = 1;
# 
#     real    a = ((q2x - q3x)*(q1y - q2y) - (q2y - q3y)*(q1x - q2x)) * h;
#     real    b = (q2x - q1x - q3x + q0x) * (q1y - q2y) - (q2y - q1y - q3y + q0y) * (q1x - q2x);
#     m21 = - b / a;
# 
#     if (q1x != q2x)
# 	m20 = (m21 * (q2x - q3x) * h + q2x - q1x - q3x + q0x) / ((q1x - q2x) * w);
#     else
# 	m20 = (m21 * (q2y - q3y) * h + q2y - q1y - q3y + q0y) / ((q1y - q2y) * w);
# 
#     m00 = m20 * q1x + (q1x - q0x) / w;
#     m10 = m20 * q1y + (q1y - q0y) / w;
# 
#     m01 = m21 * q3x + (q3x - q0x) / h;
#     m11 = m21 * q3y + (q3y - q0y) / h;
# 
#     return (m_t) {
# 	{ m00, m01, m02 },
# 	{ m10, m11, m12 },
# 	{ m20, m21, m22 } };
# }
