import fractions
import math
import cmath
import numpy as np
from scipy.stats import binom
from scipy import fftpack
from scipy.fftpack import fft, fftshift, ifft
import time   
import matplotlib.pyplot as plt


def gcd(a, b):
	return fractions.gcd(a,b)


def wrapper(func, *args, **kwargs):
	def wrapped():
		return func(*args, **kwargs)
	return wrapped



def ExtendedEuclid(a,b):
	if(b==0):
		return a,1,0
	else:
		d_p, x_p, y_p = ExtendedEuclid(b, a % b)
		d = d_p
		x = y_p
		y = x_p - (a/b)*y_p
		return d, x, y


def mod_inverse(a, m):
	d, x, y = ExtendedEuclid(a, m)
	if d != 1:
		raise Exception('modular inverse does not exist')
	else:
		return x % m


def phase(x):
	return cmath.phase(x)



def binomial_cdf(x, n, p):
	x = np.array(x)
	if(p<0 or p>1.0):
		raise Exception('Probability range is not [0,1]')
	if(n<0):
		raise Exception('Number of trials cannot be negative')
	if( (x<0).any() or (x>n).any() ):
		raise Exception('Cannot evaluate x outside [0,n]')
	return binom.cdf(x, n, p)




def shift(x, r):
	# x - complex array
	# r = shift amount
	# x[i] <- x[i-r]
	x = np.array(x)
	r = r % len(x)
	if(r>=len(x)):
		raise Exception('Shift amount if greater than lenght of x')
	
	x = np.roll(x, r, axis = 0)
	return x



def left_shift(x, r):
	
	x = np.array(x)
	r = r % len(x)
	if(r>=len(x)):
		raise Exception('Shift amount if greater than lenght of x')
	
	x = np.roll(x, len(x) - r, axis = 0)
	
	return x



def floor_to_pow2(x):
	ans = 1
	
	while(ans<=x):
		ans <<= 1
	
	return (ans / 2)



def cabs2(x):
	# square of abs value
	
	return abs(x)**2




def nth_element_immutable(x, n):
	# get the nth smallest element of the array
	x = np.array(x)
	if(n >= len(x) or n<0):
		raise Exception('index outside bounds')
	
	idx = np.argpartition(x, n)
	srtd = x[idx]
	
	return srtd[n]


def nth_element(x, n):
	
	
	if(n >= len(x) or n<0):
		raise Exception('index outside bounds')
	
	
	idx = np.argpartition(x, n)
	x = x[idx]
	
	return x



def find_largest_indices(num, samples):
	ind = np.argpartition(samples, -num)[-num:]
	return ind

def find_largest_indices2(num, samples):
	n = len(samples)
	cutoff = nth_element_immutable(samples, n-num-1)
	output = np.zeros(num)
	
	count = 0
	for i in range(n):
		
		if (samples[i] > cutoff):
			
			output[count] = i
			count +=1
		
	
	if (count < num):
		
		for i in range(n):
			
			if (samples[i] == cutoff):
				
				output[count] = i
				count +=1
				
				
				if (count >= num):
					break
				
			
			
		
		output = np.sort(output)
		
	
	return output





def get_expermient_vs_N_parameters(N, ALG_TYPE):
	
	params = {}
	
	if(N == 8192):
		if(ALG_TYPE == 2): # sFFT 2.0
			##Bcst_loc =  2; Bcst_est =  2; Comb_cst = 32; comb_loops =8; est_loops =16; loc_loops =7; threshold_loops =6; tolerance_loc =1e-8; tolerance_est =1e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 2
			params['Comb_cst'] = 32
			params['comb_loops'] = 8
			params['est_loops'] = 16
			params['loc_loops'] = 7
			params['threshold_loops'] = 6
			params['tolerance_loc'] = 1e-8
			params['tolerance_est'] = 1e-8
		else: # sFFT 1.0
			##Bcst_loc =2; Bcst_est =  2; Comb_cst =1; comb_loops =1; est_loops =16; loc_loops =7; threshold_loops =6; tolerance_loc =1e-8; tolerance_est =1e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 2
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 16
			params['loc_loops'] = 7
			params['threshold_loops'] = 6
			params['tolerance_loc'] = 1e-8
			params['tolerance_est'] = 1e-8
		
		
	elif(N == 16384):
		if(ALG_TYPE == 2):
			##Bcst_loc =  4; Bcst_est =  4; Comb_cst = 32; comb_loops =8; est_loops =10; loc_loops =6; threshold_loops =5; tolerance_loc =1e-8; tolerance_est =1e-8;
			params['Bcst_loc'] = 4
			params['Bcst_est'] = 4
			params['Comb_cst'] = 32
			params['comb_loops'] = 8
			params['est_loops'] = 10
			params['loc_loops'] = 6
			params['threshold_loops'] = 5
			params['tolerance_loc'] = 1e-8
			params['tolerance_est'] = 1e-8
		else:
			params['Bcst_loc'] = 4
			params['Bcst_est'] = 4
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 10
			params['loc_loops'] = 6
			params['threshold_loops'] = 5
			params['tolerance_loc'] = 1e-8
			params['tolerance_est'] = 1e-8
			##Bcst_loc =4; Bcst_est =  4; Comb_cst =1; comb_loops =1; est_loops =10; loc_loops =6; threshold_loops =5; tolerance_loc =1e-8; tolerance_est =1e-8;
		
	elif(N == 32768):
		if(ALG_TYPE == 2):
			##Bcst_loc =  4; Bcst_est =  2; Comb_cst = 64; comb_loops =4; est_loops = 8; loc_loops =5; threshold_loops =4; tolerance_loc =1e-8; tolerance_est =1e-8;
			params['Bcst_loc'] = 4
			params['Bcst_est'] = 2
			params['Comb_cst'] = 64
			params['comb_loops'] = 4
			params['est_loops'] = 8
			params['loc_loops'] = 5
			params['threshold_loops'] = 4
			params['tolerance_loc'] = 1e-8
			params['tolerance_est'] = 1e-8
			
		else:
			##Bcst_loc =4; Bcst_est =  2; Comb_cst =1; comb_loops =1; est_loops = 8; loc_loops =5; threshold_loops =4; tolerance_loc =1e-8; tolerance_est =1e-8;
			params['Bcst_loc'] = 4
			params['Bcst_est'] = 2
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 8
			params['loc_loops'] = 5
			params['threshold_loops'] = 4
			params['tolerance_loc'] = 1e-8
			params['tolerance_est'] = 1e-8
		
		
	elif(N == 65536):
		if(ALG_TYPE == 2):
			##Bcst_loc =  4; Bcst_est =  2; Comb_cst =128; comb_loops =6; est_loops =10; loc_loops =4; threshold_loops =2; tolerance_loc =1e-8; tolerance_est =1e-8;
			params['Bcst_loc'] = 4
			params['Bcst_est'] = 2
			params['Comb_cst'] = 128
			params['comb_loops'] = 6
			params['est_loops'] = 10
			params['loc_loops'] = 4
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-8
			params['tolerance_est'] = 1e-8
		else:
			##Bcst_loc =4; Bcst_est =  2; Comb_cst =1; comb_loops =1; est_loops = 8; loc_loops =5; threshold_loops =4; tolerance_loc =1e-8; tolerance_est =1e-8;
			params['Bcst_loc'] = 4
			params['Bcst_est'] = 2
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 8
			params['loc_loops'] = 5
			params['threshold_loops'] = 4
			params['tolerance_loc'] = 1e-8
			params['tolerance_est'] = 1e-8
		
	elif(N == 131072):
		if(ALG_TYPE == 2):
			params['Bcst_loc'] = 1
			params['Bcst_est'] = 1
			params['Comb_cst'] = 8
			params['comb_loops'] = 2
			params['est_loops'] = 12
			params['loc_loops'] = 4
			params['threshold_loops'] = 3
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			##Bcst_loc =  1; Bcst_est =  1; Comb_cst =  8; comb_loops =2; est_loops =12; loc_loops =4; threshold_loops =3; tolerance_loc =1e-6; tolerance_est =1e-8;
			
			
		else:
			##Bcst_loc =2; Bcst_est =  1; Comb_cst =1; comb_loops =1; est_loops =10; loc_loops =5; threshold_loops =4; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 1
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 10
			params['loc_loops'] = 5
			params['threshold_loops'] = 4
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
		
		
	elif(N == 262144):
		if(ALG_TYPE == 2):
			##Bcst_loc =  1; Bcst_est =  1; Comb_cst =  8; comb_loops =2; est_loops =14; loc_loops =5; threshold_loops =4; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 1
			params['Bcst_est'] = 1
			params['Comb_cst'] = 8
			params['comb_loops'] = 2
			params['est_loops'] = 14
			params['loc_loops'] = 5
			params['threshold_loops'] = 4
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
		else:
			##Bcst_loc =2; Bcst_est =0.5; Comb_cst =1; comb_loops =1; est_loops =14; loc_loops =4; threshold_loops =3; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 0.5
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 14
			params['loc_loops'] = 4
			params['threshold_loops'] = 3
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
		
		
	elif(N == 524288):
		
		if(ALG_TYPE == 2):
			##Bcst_loc =0.5; Bcst_est =0.5; Comb_cst =  8; comb_loops =1; est_loops =10; loc_loops =4; threshold_loops =3; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 0.5
			params['Bcst_est'] = 0.5
			params['Comb_cst'] = 8
			params['comb_loops'] = 1
			params['est_loops'] = 10
			params['loc_loops'] = 4
			params['threshold_loops'] = 3
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
			
		else:
			##Bcst_loc =1; Bcst_est =0.5; Comb_cst =1; comb_loops =1; est_loops =12; loc_loops =5; threshold_loops =4; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 1
			params['Bcst_est'] = 0.5
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 12
			params['loc_loops'] = 5
			params['threshold_loops'] = 4
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
		
		
	elif(N == 1048576):
		
		if(ALG_TYPE == 2):
			##Bcst_loc =0.5; Bcst_est =0.5; Comb_cst =  8; comb_loops =2; est_loops =12; loc_loops =4; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 0.5
			params['Bcst_est'] = 0.5
			params['Comb_cst'] = 8
			params['comb_loops'] = 2
			params['est_loops'] = 12
			params['loc_loops'] = 4
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
		else:
			##Bcst_loc =2; Bcst_est =0.5; Comb_cst =1; comb_loops =1; est_loops =12; loc_loops =4; threshold_loops =3; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 0.5
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 12
			params['loc_loops'] = 4
			params['threshold_loops'] = 3
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
		
		
	elif(N == 2097152):
		
		if(ALG_TYPE == 2):
			##Bcst_loc =0.5; Bcst_est =0.2; Comb_cst =  8; comb_loops =1; est_loops =10; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 0.5
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 8
			params['comb_loops'] = 1
			params['est_loops'] = 10
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
		else:
			##Bcst_loc =2; Bcst_est =0.2; Comb_cst =1; comb_loops =1; est_loops =15; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 15
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
		
	elif(N == 4194304):
		
		if(ALG_TYPE == 2):
			##Bcst_loc =0.5; Bcst_est =0.2; Comb_cst =  8; comb_loops =1; est_loops = 8; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 0.5
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 8
			params['comb_loops'] = 1
			params['est_loops'] = 8
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
			
		else:
			##Bcst_loc =4; Bcst_est =0.2; Comb_cst =1; comb_loops =1; est_loops =10; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 4
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 10
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
		
	elif(N == 8388608):
		
		if(ALG_TYPE == 2):
			##Bcst_loc =0.5; Bcst_est =0.2; Comb_cst =  8; comb_loops =1; est_loops = 8; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 0.5
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 8
			params['comb_loops'] = 1
			params['est_loops'] = 8
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
			
		else:
			##Bcst_loc =2; Bcst_est =0.2; Comb_cst =1; comb_loops =1; est_loops = 8; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 8
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
		
		
	elif(N == 16777216):
		
		if(ALG_TYPE == 2):
			##Bcst_loc =0.5; Bcst_est =0.2; Comb_cst = 16; comb_loops =1; est_loops = 8; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 0.5
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 16
			params['comb_loops'] = 1
			params['est_loops'] = 8
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
		else:
			##Bcst_loc =4; Bcst_est =0.2; Comb_cst =1; comb_loops =1; est_loops = 8; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1e-8;
			params['Bcst_loc'] = 4
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 8
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
		
		
	else:
		
		
		params['Bcst_loc'] = 1
		params['Bcst_est'] = 1
		params['Comb_cst'] = 2
		params['comb_loops'] = 1
		params['est_loops'] = 16
		params['loc_loops'] = 4
		params['threshold_loops'] = 3
		params['tolerance_loc'] = 1e-8
		params['tolerance_est'] = 1e-8
		
		
	
	return params



def get_expermient_vs_K_parameters(K, ALG_TYPE):
	
	params= {}
	
	if(K == 50):
		
		if(ALG_TYPE == 2):
			#Bcst_loc =0.5; Bcst_est =0.2; Comb_cst = 16; comb_loops =1; est_loops =10; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1.0e-8;
			params['Bcst_loc'] = 0.5
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 16
			params['comb_loops'] = 1
			params['est_loops'] = 10
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
		else:
			
			##Bcst_loc =4; Bcst_est =0.2; Comb_cst =1; comb_loops =1; est_loops =10; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1.0e-8;
			params['Bcst_loc'] = 4
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 10
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
		
		
		
	elif(K == 100):
		
		
		if(ALG_TYPE == 2):
			##Bcst_loc =0.5; Bcst_est =0.2; Comb_cst = 16; comb_loops =1; est_loops =12; loc_loops =4; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1.0e-8;
			params['Bcst_loc'] = 0.5
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 16
			params['comb_loops'] = 1
			params['est_loops'] = 12
			params['loc_loops'] = 4
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
		else:
			##Bcst_loc =2; Bcst_est =0.2; Comb_cst =1; comb_loops =1; est_loops =12; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =1.0e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 0.2
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 12
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
		
		
		
	elif(K == 200):
		
		
		if(ALG_TYPE == 2):
			##Bcst_loc =  0.5; Bcst_est =  0.5; Comb_cst = 32; comb_loops =1; est_loops = 8; loc_loops =4; threshold_loops =3; tolerance_loc =1e-6; tolerance_est =0.5e-8;
			params['Bcst_loc'] = 0.5
			params['Bcst_est'] = 0.5
			params['Comb_cst'] = 32
			params['comb_loops'] = 1
			params['est_loops'] = 8
			params['loc_loops'] = 4
			params['threshold_loops'] = 3
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 0.5e-8
		else:
			##Bcst_loc =4; Bcst_est =0.5; Comb_cst =1; comb_loops =1; est_loops =10; loc_loops =3; threshold_loops =2; tolerance_loc =1e-6; tolerance_est =0.5e-8;
			params['Bcst_loc'] = 4
			params['Bcst_est'] = 0.5
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 10
			params['loc_loops'] = 3
			params['threshold_loops'] = 2
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 0.5e-8
			
		
		
		
	elif(K == 500):
		
		
		if(ALG_TYPE == 2):
			##Bcst_loc =0.5; Bcst_est =0.5; Comb_cst = 64; comb_loops =1; est_loops =10; loc_loops =4; threshold_loops =3; tolerance_loc =1e-6; tolerance_est =0.5e-8;
			params['Bcst_loc'] = 0.5
			params['Bcst_est'] = 0.5
			params['Comb_cst'] = 64
			params['comb_loops'] = 1
			params['est_loops'] = 10
			params['loc_loops'] = 4
			params['threshold_loops'] = 3
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 0.5e-8
		else:
			###Bcst_loc =2; Bcst_est =  1; Comb_cst =1; comb_loops =1; est_loops =12; loc_loops =4; threshold_loops =3; tolerance_loc =1e-6; tolerance_est =0.5e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 1
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 12
			params['loc_loops'] = 4
			params['threshold_loops'] = 3
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 0.5e-8
			
		
		
		
	elif(K == 1000):
		
		if(ALG_TYPE == 2):
			##Bcst_loc =  1; Bcst_est =  1; Comb_cst =128; comb_loops =3; est_loops =12; loc_loops =4; threshold_loops =3; tolerance_loc =1e-6; tolerance_est =0.5e-8;
			params['Bcst_loc'] = 1
			params['Bcst_est'] = 1
			params['Comb_cst'] = 128
			params['comb_loops'] = 3
			params['est_loops'] = 12
			params['loc_loops'] = 4
			params['threshold_loops'] = 3
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 0.5e-8
		else:
			##Bcst_loc =2; Bcst_est =  1; Comb_cst =1; comb_loops =1; est_loops =12; loc_loops =5; threshold_loops =4; tolerance_loc =1e-6; tolerance_est =1.0e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 1
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 12
			params['loc_loops'] = 5
			params['threshold_loops'] = 4
			params['tolerance_loc'] = 1e-6
			params['tolerance_est'] = 1e-8
			
		
		
		
		
	elif(K == 2000):
		
		
		if(ALG_TYPE == 2):
			
			##Bcst_loc =  1; Bcst_est =  1; Comb_cst =512; comb_loops =3; est_loops =16; loc_loops =4; threshold_loops =3; tolerance_loc =1e-7; tolerance_est =0.2e-8;
			params['Bcst_loc'] = 1
			params['Bcst_est'] = 1
			params['Comb_cst'] = 512
			params['comb_loops'] = 3
			params['est_loops'] = 16
			params['loc_loops'] = 4
			params['threshold_loops'] = 3
			params['tolerance_loc'] = 1e-7
			params['tolerance_est'] = 0.2e-8
		else:
			
			#Bcst_loc =2; Bcst_est =  1; Comb_cst =1; comb_loops =1; est_loops =16; loc_loops =5; threshold_loops =4; tolerance_loc =1e-7; tolerance_est =0.5e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 1
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 16
			params['loc_loops'] = 5
			params['threshold_loops'] = 4
			params['tolerance_loc'] = 1e-7
			params['tolerance_est'] = 0.5e-8
			
		
		
	elif(K == 2500):
		
		if(ALG_TYPE == 2):
			
			##Bcst_loc =  1; Bcst_est =  1; Comb_cst =512; comb_loops =3; est_loops =16; loc_loops =4; threshold_loops =3; tolerance_loc =1e-7; tolerance_est =0.2e-8;
			params['Bcst_loc'] = 1
			params['Bcst_est'] = 1
			params['Comb_cst'] = 512
			params['comb_loops'] = 3
			params['est_loops'] = 16
			params['loc_loops'] = 4
			params['threshold_loops'] = 3
			params['tolerance_loc'] = 1e-7
			params['tolerance_est'] = 0.2e-8
		else:
			
			##Bcst_loc =2; Bcst_est =  1; Comb_cst =1; comb_loops =1; est_loops =16; loc_loops =5; threshold_loops =4; tolerance_loc =1e-7; tolerance_est =0.5e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 1
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 16
			params['loc_loops'] = 5
			params['threshold_loops'] = 4
			params['tolerance_loc'] = 1e-7
			params['tolerance_est'] = 0.5e-8
			
		
		
		
	elif(K == 4000):
		
		if(ALG_TYPE == 2):
			##Bcst_loc =  1; Bcst_est =  2; Comb_cst =512; comb_loops =3; est_loops =14; loc_loops =8; threshold_loops =7; tolerance_loc =1e-8; tolerance_est =0.5e-8;
			params['Bcst_loc'] = 1
			params['Bcst_est'] = 2
			params['Comb_cst'] = 512
			params['comb_loops'] = 3
			params['est_loops'] = 14
			params['loc_loops'] = 8
			params['threshold_loops'] = 7
			params['tolerance_loc'] = 1e-8
			params['tolerance_est'] = 0.5e-8
		else:
			##Bcst_loc =2; Bcst_est =  2; Comb_cst =1; comb_loops =1; est_loops =14; loc_loops =6; threshold_loops =5; tolerance_loc =1e-8; tolerance_est =1.0e-8;
			params['Bcst_loc'] = 2
			params['Bcst_est'] = 2
			params['Comb_cst'] = 1
			params['comb_loops'] = 1
			params['est_loops'] = 14
			params['loc_loops'] = 6
			params['threshold_loops'] = 5
			params['tolerance_loc'] = 1e-8
			params['tolerance_est'] = 1e-8
			
		
		
		
	else:
		
		
		params['Bcst_loc'] = 1
		params['Bcst_est'] = 1
		params['Comb_cst'] = 2
		params['comb_loops'] = 1
		params['est_loops'] = 16
		params['loc_loops'] = 4
		params['threshold_loops'] = 3
		params['tolerance_loc'] = 1e-8
		params['tolerance_est'] = 1e-8
		
	
	
	return params














def generate_random_signal(n, k):
	
	x_f = np.zeros(n)
	large_freq = np.random.randint(0, n, k)
	# generate k random indecies for the sparce k frequencies
	x_f[large_freq] = 1.0
	
	#plt.stem(x_f)
	#plt.show()
	
	
	
	x = n*fftpack.ifft(x_f, n)
	
	return x, x_f, large_freq


def generate_noisy_random_signal(n,k,noise_power):
	
	noise = (math.sqrt(2*noise_power)/2.0) * (np.random.rand(n, ) +  1j*np.random.rand(n,) )
	
	
	x_f = np.zeros(n)
	large_freq = np.random.randint(0, n, k)
	# generate k random indecies for the sparce k frequencies
	x_f[large_freq] = 1.0
	
	x = n*fftpack.ifft(x_f, n)
	
	x= x + noise
	
	return x, x_f, large_freq


def generate_offgrid_random_signal(n,k, noise_power):
	
	noise = (math.sqrt(2*noise_power)/2.0) * (np.random.rand(n, ) +  1j*np.random.rand(n,) )
	
	x_f = np.zeros(n)
	large_freq = np.random.randint(0, n, k)
	
	
	
	
	
	


def AWGN(x, n, std_noise):
	
	if(std_noise==0):
		return 1000000000
	
	gn = complex(0,0)
	
	sig_power =0
	noise_power =0
	snr=0.0
	u = 0.0
	v = 0.0
	
	for h in range(n):
		
		sig_power += abs(x[h])*abs(x[h])
		
		u = np.random.rand()
		v = np.random.rand()
		gn = std_noise * math.sqrt(-2*math.log(u)) * cmath.exp(2.0*math.pi * 1j * v)
		noise_power += -2.0*math.log(u)
		x[h] += gn
		
		
	
	
	noise_power = noise_power * std_noise * std_noise
	snr = sig_power/noise_power
	
	return snr






























