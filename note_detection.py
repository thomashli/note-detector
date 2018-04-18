import pyaudio
from scipy.io import wavfile as wf 
import scipy
from scipy.fftpack import fft
import matplotlib.pyplot as plt 
import numpy as np
"""
Sample code from stackexchange post:
https://stackoverflow.com/questions/23377665/python-scipy-fft-wav-files?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
credit to eusoubrasileiro, Shenghui
"""
fs, data = wf.read('output1.wav')
a = data.T[0] # this is a two channel soundtrack, I get the first track
b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
c = fft(b) # calculate fourier transform (complex numbers list)
d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)

k = scipy.arange(int(len(data)/2)-1)
T = len(data)/fs  # where fs is the sampling frequency
frqLabel = k/T
frequency_magnitude_spectrum = abs(c[:(d-1)])

plt.plot(frqLabel,frequency_magnitude_spectrum,'r') 
#plt.plot(frqLabel,abs(c),'r') 
plt.show()

notes = {

#octave 0 to octave 8
	'c' = 		[16.35,32.7,65.41,130.81,261.63,523.25,1046.5,2093.,4186.]
	'c_sharp' = [17.32,34.65,69.3,138.59,277.18,554.37,1109,2217.46.3,4434.92]
	'd' = 		[18.35,36.71,73.42,146.83,293.66,587.33,1174.66,2349.3,4698.6]
	'd_sharp' = [19.45,38.89,77.78,155.56,311.13,622.25,1244.5,2489.,4978.03]
	'e' = 		[20.60,41.2,82.41,164.81,329.63,659.25,1318.5,2637.,5274.04]
	'f' = 		[21.83,43.65,87.31,174.61,349.23,698.46,1396.9,2793.,5587.65]
	'f_sharp' = [23.12,46.25,92.5,185.,369.99,739.99,1479.98,2959.,5919.91]
	'g' = 		[24.5,49.0,98.,196.,392.,784.,1568.,3135.96,6271.93]
	'g_sharp' = [25.96,51.91,103.83,207.65,415.30,830.6,1661.2,3322.4,6644.88]
	'a' = 		[27.5,55.0,110.0,220.,440.,880.,1760.,3520.,7040.]
	'a_sharp' = [14.568,29.135,58.270,116.541,233.082,466.164,932.328,1864.655,3729.310,7458.620]
	'b' = 		[30.87,61.74,123.47,246.94,493.88,988.,1975.5,3951.07,7902.13]

}