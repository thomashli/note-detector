
"""
Sample code from stackexchange post:
https://stackoverflow.com/questions/23377665/python-scipy-fft-wav-files?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
credit to eusoubrasileiro, Shenghui

Example Usage:
python3 note_detection.py input.wav
"""

import pyaudio
from scipy.io import wavfile as wf 
import scipy
from scipy.fftpack import fft
import matplotlib.pyplot as plt 
import numpy as np
import sys


notes = {
#from octave 0 to octave 8
	'C':		[16.35,32.7,65.41,130.81,261.63,523.25,1046.5,2093.,4186.],
	'C#':		[17.32,34.65,69.3,138.59,277.18,554.37,1109,2217.46,4434.92],
	'D' : 		[18.35,36.71,73.42,146.83,293.66,587.33,1174.66,2349.3,4698.6],
	'D#' : 		[19.45,38.89,77.78,155.56,311.13,622.25,1244.5,2489.,4978.03],
	'E' : 		[20.60,41.2,82.41,164.81,329.63,659.25,1318.5,2637.,5274.04],
	'F' : 		[21.83,43.65,87.31,174.61,349.23,698.46,1396.9,2793.,5587.65],
	'F#' : 		[23.12,46.25,92.5,185.,369.99,739.99,1479.98,2959.,5919.91],
	'G' : 		[24.5,49.0,98.,196.,392.,784.,1568.,3135.96,6271.93],
	'G#' : 		[25.96,51.91,103.83,207.65,415.30,830.6,1661.2,3322.4,6644.88],
	'A' : 		[27.5,55.0,110.0,220.,440.,880.,1760.,3520.,7040.],
	'A#' : 		[29.135,58.270,116.541,233.082,466.164,932.328,1864.655,3729.310,7458.620],
	'B' : 		[30.87,61.74,123.47,246.94,493.88,988.,1975.5,3951.07,7902.13]
}

note_names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

# finds closest note & octave & intonation 
def note_info(note):
	if note < 65:
		print('no note detected')
		return 
	elif note > 8500:
		print('above frequency range')
		return

	# Note and octave matching
	closestNote = 'C'
	closestFreq = 16.35
	closestOctave = 0
	minDiff = note - 16.35
	for i in notes:
		octave = 0
		for freq in notes[i]:
			if abs(note-freq) < abs(minDiff):
				closestNote = i
				closestFreq = freq
				minDiff = note-freq
				closestOctave = octave
			octave += 1

	#finding intonation
	nameInd = note_names.index(closestNote)
	nextFlatter = note_names[(nameInd - 1) % len(note_names)]
	nextSharper = note_names[(nameInd + 1) % len(note_names)]


	flat_tolerance = (closestFreq - notes[nextFlatter][closestOctave])/4
	sharp_tolerance = (notes[nextSharper][closestOctave] - closestFreq)/4
	tolerance = (notes[nextSharper][closestOctave]-notes[nextFlatter][closestOctave])/2

	tune_disp = list(str(' ') * 51)

	pos = int(round(minDiff/tolerance*50)+23)
	tune_disp[pos] = 'N'
	tune_disp[25] = closestNote


	if minDiff < 0:
		if (minDiff < flat_tolerance):
			intonation = 'flat'
		else:
			intonation = 'in tune'
	elif minDiff > 0:
		if (minDiff > sharp_tolerance):
			intonation = 'sharp'
		else:
			intonation = 'in tune'
	else:
		intonation = 'perfectly in tune'



	info = {'note': closestNote, 
			'octave' : closestOctave, 
			'intonation': intonation,
			'graph': '['+''.join(tune_disp)+']',
			'flow': round(closestFreq-(tolerance*2)),
			'fhigh': round(closestFreq+(tolerance*2))}

	return info

def tuner(wav):
	print("______")
	fs, data = wf.read("lala.wav")
	a = data.T[0] # this is a two channel soundtrack, I get the first track
	b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
	c = fft(b) # calculate fourier transform (complex numbers list)
	d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
	
	k = scipy.arange(int(len(data)/2)-1)
	T = len(data)/fs  # where fs is the sampling frequency
	frqLabel = k/T
	frqLabel = frqLabel[0:int(8000*T)]
	frequency_magnitude_spectrum = abs(c[:(d-1)])[:len(frqLabel)]
	frequency_magnitude_spectrum[0:10] = [0]*10

	#chord =  [i for i in range(len(frequency_magnitude_spectrum)) if frequency_magnitude_spectrum[i] > 20000]
	#print(chord)

	#plot spectrum 
	#plt.plot(frqLabel,frequency_magnitude_spectrum,'r')  
	#plt.show()
	
	#find the note
	max_mag = max(frequency_magnitude_spectrum)
	max_ind = np.argmax(frequency_magnitude_spectrum)
	num_iter = 0
	visited = []

	threshold = max_mag / 3
	if threshold < 10000:
		threshold = 10000
	while (max_mag > threshold):
		#plot spectrum 
		#plt.plot(frqLabel,frequency_magnitude_spectrum,'r')  
		#plt.show()
		if num_iter > 3:
			return; 
		note = frqLabel[max_ind]
		info = note_info(note)
		if info:
			if not np.any(visited == info['note']):
				print('Note: ', info['note'])
				print('Octave: ', info['octave'])
				print('Intonation: ', info['intonation'])
				print('Grapher:', info['graph'])
				visited.append(info['note']+str(info['octave']))

			#filtering it out
			flow = info['flow']*T 
			fhigh = info['fhigh']*T
			if flow > fhigh:
				flow, fhigh = fhigh, flow
			frequency_magnitude_spectrum[int(flow-20):int(fhigh+20)] = [0]*(int(fhigh+20)-int(flow-20))
			max_mag = max(frequency_magnitude_spectrum)
			max_ind = np.argmax(frequency_magnitude_spectrum)
		#plt.plot(frqLabel,frequency_magnitude_spectrum,'r')  
		#plt.show()
		num_iter += 1