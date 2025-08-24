import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import wave
import librosa
import librosa.display
from scipy.ndimage import maximum_filter
import hashlib

songs_hash={}
def takingAudioInput(name,to_identify=False):
    FRAMES_PER_BUFFER=3200   #how many frames will be recorded per sec
    FORMAT=pyaudio.paInt16  #data type of Int16 as it is a mono if its a stero then Int32
    CHANNELS=1      #same for a mono channel==1 
    RATE=16000  #wave recording frequency

    pa=pyaudio.PyAudio()  #alias


    stream=pa.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    print("Start Recording")


    seconds=11
    frames=[]   # indivisually capturing audio frequency 
    second_tracking=0
    second_count=0

    for i in range(0,int(RATE/FRAMES_PER_BUFFER*seconds)):
        data=stream.read(FRAMES_PER_BUFFER)
        frames.append(data)
        second_tracking+=1
        if second_tracking==RATE/FRAMES_PER_BUFFER:
            second_count+=1
            second_tracking=0
            print(f'Time left :{seconds-second_count}')

    stream.stop_stream()
    stream.close()
    pa.terminate()



    obj=wave.open(f'{name}.wav','wb')
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(pa.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b''.join(frames))
    obj.close()
    #this above code will write an audio file of type wav

    """file=wave.open(f'{name}.wav','rb')
    sample_freq=file.getframerate()
    frames=file.getnframes()
    signal_wave=file.readframes(-1)
    file.close()
    #this above code reads the frame of the audio

    time=frames/sample_freq

    audio_array=np.frombuffer(signal_wave,dtype=np.int16)
    times=np.linspace(0,time,num=frames)

    #plotting
    plt.figure(figsize=(15,5))
    plt.plot(times,audio_array)
    plt.ylabel("signal")
    plt.xlabel('Time(s)')
    plt.xlim(0,time)
    plt.title('Recorded')
    plt.show()"""


    def extract_peaks(S_db,threshold=18):
        peaks = maximum_filter(S_db, size=10) == S_db
        rows,cols=np.where(peaks)
        peaks_db=[(col,row) for col,row in zip(cols,rows) if S_db[row,col]>threshold]
        return peaks_db

    #loading the audio file
    audio_path=f'{name}.wav'
    y,sr =librosa.load(audio_path)


    #generate the spectogram
    S=np.abs(librosa.stft(y))  #S represents magnitude of audio frequencies
    S_db=librosa.amplitude_to_db(S,ref=np.max)   #We then convert this magnitude to decibel scale S_db which is suitable


    #displaying the spectogram
    if not to_identify:
        plt.figure(figsize=(12,8))
        librosa.display.specshow(S_db,sr=sr,x_axis='time',y_axis='log')
        plt.colorbar(format="%+2.0f dB")
        plt.title('Spectogram')
        plt.show()
    peaks=extract_peaks(S_db)
    peaks_str=str(peaks).encode()
    fingerprint=hashlib.sha1(peaks_str).hexdigest()
    if to_identify:
        try:
            print(songs_hash[fingerprint])
        except Exception as e:
            print("Song match not found")
    else:
        songs_hash[fingerprint]=name
        print(f'Generated fingerprint:{fingerprint}')

takingAudioInput("My Voice-Ashwin")
takingAudioInput("Hardest-Part by Olivia_Dean")
takingAudioInput("test",True)
