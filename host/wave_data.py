import numpy as np

sample_period_us = 1024 # sample period in usec
peaks_treshold = 2

def read_data(path):
	a, l = [], []
	with open(path) as f:
		while True:
			line = f.readline()
			vals = line.split()
			if len(vals) >= 2:
				a.append(int(vals[0]))
				l.append(int(vals[1]))
			else:
				break
	return np.array(a), np.array(l)

def plot_line(v):
	import matplotlib.pylab as pl
	pl.xlabel('seconds')
	t = np.arange(len(v)) * sample_period_us / 1e6
	pl.plot(t, v)
	pl.show()

def plot_xy(x, y):
	import matplotlib.pylab as pl
	pl.plot(x, y)
	pl.show()

def plot_map(data):
	import matplotlib.pyplot as plt
	from matplotlib import cm
	range = min(data.max(), -data.min())
	fig, ax = plt.subplots()
	cax = ax.imshow(data, interpolation='bicubic', cmap=cm.bwr, vmin=-range, vmax=range)
	# Add colorbar, make sure to specify tick locations to match desired ticklabels
	cbar = fig.colorbar(cax)

	plt.show()

def centers(a, t):
	c = []
	sum_iv, sum_v = 0., 0.
	for i, v in enumerate(a):
		if v > t:
			v_ =  v - t
			sum_iv += i * v_  
			sum_v += v_ 
		else:
			if sum_v > 0: c.append(sum_iv / sum_v)
			sum_iv, sum_v = 0., 0.
	return c

def align_centers(c):
	n = len(c) 
	if n < 3:
		return
	for i in range(n-2):
		d = (c[i+1] - (c[i] + c[i+2])/2.)/2.
		c[i] += d
	c[i+1] -= d
	c[i+2] += d

def data_trace(A, L, r, v, decay = 0):
	C = centers(L, L.mean() * peaks_treshold)
	align_centers(C)
	if len(C) < 2:
		return None
	C = np.array(C)
	first = int(C[0])
	A, L = A[first:], L[first:]
	C -= first
	n = len(A)
	I = np.arange(n)
	T = I * sample_period_us / 1e6
	X = T * v
	Y = np.empty(n)
	D = np.exp(-decay*T)
	c_, s = C[0], 1
	for c in C[1:]:
		p = c - c_
		i, j = int(c_), int(c)
		Y[i:j] = r * s * np.sin(np.pi * (I[i:j] - c_) / p) * D[i:j]
		c_, s = c, -s
	Y[j:] = r * s * np.sin(np.pi * (I[j:] - c_) / p) * D[j:]
	return X, Y, A

def data_map2grid(X, Y, A, cell, r):
	r2 = r * r
	xn, yn = X[-1] / cell, Y.max() / cell
	x_ = cell * np.arange(xn + 1)
	y_ = cell * np.arange(-yn, yn + 1)
	XG, YG = np.meshgrid(x_, y_)
	V, W = np.zeros(XG.shape), np.zeros(XG.shape)
	for i, a in enumerate(A):
		x, y = X[i], Y[i]
		F = r2 / (r2 + (XG - x)**2 + (YG - y)**2)
		V += a * F
		W += F
	return V/W

def data_compand(data, law):
	return np.where(data >= 0, data**law, -((-data)**law))

if __name__ == '__main__':
	import sys
	if len(sys.argv) < 2:
		print 'data filename required'
		sys.exit(1)
	a, l = read_data(sys.argv[1])
	if len(sys.argv) >= 3:
		n = int(sys.argv[2])
		a, l = a[:n], l[:n]
	print '%d data samples loaded' % len(a)
	l = np.array(l)
	p = centers(l, 2*l.mean())
	align_centers(p)
	X, Y, A = data_trace(a, l, 100, 50./60, 0)
	G = data_map2grid(X, Y, A, 2, 2)
	plot_map(data_compand(G, .2))

