'''
# HHH_discrete.py
# author: mark r. yoder, ph.d.
#
# summary: discrete Hilbert-Huang transforms, basically a peak-fitting approach to HHH transforms.
'''
#
import numpy
import scipy
import math
import pylab as plt
import random
import operator
#
def get_peaks(X, uppers=True, col_index=-1):
	if uppers: op=operator.gt
	if not uppers: op = operator.lt
	#
	#return [[j,x] for x in X[1:-1] if op(x,X[j]) and op(x,X[j+2])]
	if not hasattr(X[0], '__len__'):
		return [x for x in X[1:-1] if op(x,X[j]) and op(x,X[j+2])]
	else:
		# we have a n n x m list.
		return [x for j,x in enumerate(X[1:-1]) if op(x[col_index],X[j][col_index]) and op(x[col_index],X[j+2][col_index])]
def get_upper_peaks(X):
	return get_peaks(X=X, uppers=True)
def get_lower_peaks(X):
	return get_peaks(X=X, uppers=False)

def get_h(XY):
	x_uppers = get_upper_peaks(XY)
	x_lowers = get_lower_peaks(XY)
	#
	return [[.5*(x_u+x_l), .5*(y_u+y_l)] for (x_u,y_u), (x_l,y_l) in zip(x_uppers, x_lowers)]
#
#def get_h_modes(XY, n_modes=-1):
def get_h_modes(XY):
	# @n_modes: positive integers will give just the number of modes to calculate.
	# ... but for now, just return everything.
	#
	modes = [XY]
	while len(modes[-1])>0:
		modes += [get_h(modes[-1])]
	#while  len(modes[-1])==0: modes.pop(-1)
	#
	return modes
#
def peaks_test_1(n_modes=5, r_factor_range=10., fignum=0):
	# some tests of peak fits. let's just use sin() functions.
	#
	X=numpy.linspace(0., 2.0*math.pi, 1000)
	Y = numpy.sin(X)
	Y_modes = [Y]
	R = random.Random()
	#
	for j in range(n_modes):
		x_r = R.random()
		Y_modes += numpy.sin(r_factor_range*x_r*X)
		Y += Y_modes[-1]
		#
	#
	h0=list(zip(X,Y))
	h1 = get_h(h0)
	#
	pks_upper = get_upper_peaks(h0)
	pks_lower = get_lower_peaks(h0)
	#
	modes = get_h_modes(h0)
	#return modes
	#
	plt.figure(fignum)
	plt.clf()
	plt.plot(X,Y, '.-')
	plt.plot(*zip(*pks_upper), color='g', ls='-', lw=2., marker='o')
	plt.plot(*zip(*pks_lower), color='g', ls='-', lw=2., marker='o')
	#plt.plot(*zip(*h1), color='r', ls='--', lw=2., marker='')
	for j,md in enumerate(modes[1:]):
		plt.plot(*zip(*md), ls='--', lw=2., marker='')
	
	return modes

if __name__=='__main__':
	pass
else:
	plt.ion()
#

		
	
