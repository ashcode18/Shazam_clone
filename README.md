# Shazam_clone
Project Overview (Shazam Clone):

In this project, I'm building a simple audio recognition system — kind of like a mini Shazam. Here's how it works:

Audio Input (Recording):
I use the pyaudio library to record audio from the microphone. I open an audio stream with necessary parameters like buffer size, format (paInt16 for mono audio), sample rate (16,000 Hz), etc. This stream captures audio in real time for a fixed duration (e.g., 9 seconds).

Saving the Audio:
After recording, I write the captured audio frames into a .wav file using Python's wave module. The file is saved in binary write mode ('wb') because audio data is stored in bytes.

Feature Extraction (Librosa):
I use librosa to load the audio file and convert it into a spectrogram — which is a visual representation of the signal's frequency content over time.

Peak Detection & Fingerprinting:
From the spectrogram (in decibel scale), I extract the peaks using a local maximum filter. These peaks are the "signature" points in the audio. Then I hash the collection of these peaks using Python’s built-in hash() to generate a unique fingerprint.

Matching:
The fingerprints of known songs are stored in a dictionary. When a new audio sample is recorded, its fingerprint is compared to the existing ones to check for a match.
