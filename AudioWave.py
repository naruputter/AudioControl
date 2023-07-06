import soundfile as sf
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time

class Audio: 

	def __init__(self, filePath=None, audioData=[], sampleRate=44100):

		self.audio_data = audioData
		self.file_path = filePath
		self.sample_rate = sampleRate

		if ( filePath is not None ) and type(filePath) is str :

			self.audio_data, self.sample_rate = sf.read(filePath)

	def data(self):

		return self.audio_data, self.sample_rate

	def audio_data(self):

		return self.audio_data

	def sample_rate(self):

		return self.sample_rate

	def normalize(self): # Transform Data to [ -1, 1 ]

		max_value = np.max(self.audio_data)
		min_value = np.max(self.audio_data)

		max_absolute = max(abs(max_value), abs(min_value))

		self.audio_data = self.audio_data / max_absolute

		return self.audio_data

	def change_volume(self, volume=0): # Range [ -1, 1 ]

		self.audio_data = self.audio_data + (self.audio_data*volume)

		return self.audio_data

	def pan(self, side, value): # Only Stereo

		if side == 'right' :

			self.audio_data[:, 0] = self.audio_data[:, 0]*(1-value)

		elif side == 'left' :

			self.audio_data[:, 1] = self.audio_data[:, 1]*(1-value)



	def graph(self):

		plt.plot(self.audio_data)
		plt.xlabel('Sample Rate')
		plt.ylabel('Frequency (HZ)')
		plt.show()

	def play_audio(self, channels=2):

		play_audio = pyaudio.PyAudio()

		stream = play_audio.open(

			format = pyaudio.paFloat32,
			channels = channels,
			rate = self.sample_rate,
			output = True

			)

		stream.write(self.audio_data.astype(np.float32).tobytes())

		stream.stop_stream()
		stream.close()
		play_audio.terminate()

	def save_audio_data_file(self, path): # Cannot save frequency more than [-1,1]

		sf.write(path, self.waveform, self.sample_rate)



class WaveForm:

	def __init__(self, Frequency=440, Duration=1, sampleRate=44100, Mono=False):

		self.sample_rate = sampleRate
		self.frequency = Frequency
		self.duration = Duration
		self.waveform = None
		self.mono = Mono

	def data(self):

		return self.waveform, self.sample_rate

	def sine(self):

		linear = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
		self.waveform =   np.sin(2 * np.pi * self.frequency * linear)

		if self.mono == False :
			self.waveform  = np.column_stack((self.waveform , self.waveform))

		return self.waveform

	def square(self):

		linear = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
		self.waveform =  np.sign(np.sin(2 * np.pi * self.frequency * linear))

		if self.mono == False :
			self.waveform  = np.column_stack((self.waveform , self.waveform))

		return self.waveform

	def saw(self):

		linear = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
		self.waveform = 2 * (linear * self.frequency - np.floor(linear * self.frequency + 0.5))

		if self.mono == False :
			self.waveform  = np.column_stack((self.waveform , self.waveform))

		return self.waveform

	def graph(self):

		plt.plot(self.audio_data)
		plt.xlabel('Sample Rate')
		plt.ylabel('Frequency (HZ)')
		plt.show()


	def save_waveform_file(self, path):

		sf.write(path, self.waveform, self.sample_rate)


if __name__ == '__main__':

	wave = WaveForm(440, 0.1)
	A = wave.sine()

	audio = Audio(audioData=A)
	audio.play_audio()





