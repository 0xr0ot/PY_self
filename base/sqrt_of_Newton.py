#!usr/bin/env python3

def sqrt(n):
	max_error = 0.0001
	k = float(n)
	while True:
		v = k - k/2 + n / 2 / k
		if abs(v - k) < max_error:
			break
	return v
