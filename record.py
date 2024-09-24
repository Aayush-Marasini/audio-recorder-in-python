import tkinter as tk
import pyaudio
import wave
import datetime
import threading

# Global variables
RECORDING = False

def start_recording(duration):
    global RECORDING
    RECORDING = True
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []

    end_time = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    
    while RECORDING and datetime.datetime.now() < end_time:
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    if RECORDING:
        save_audio(frames)

def save_audio(frames):
    global RECORDING
    RECORDING = False
    file_name = "recorded_audio.wav"
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

def schedule_recording(duration, start_time):
    current_time = datetime.datetime.now()
    scheduled_time = datetime.datetime(current_time.year, current_time.month, current_time.day, start_time.hour, start_time.minute)
    if current_time > scheduled_time:
        scheduled_time += datetime.timedelta(days=1)
    
    delay = (scheduled_time - current_time).total_seconds()
    
    threading.Timer(delay, start_recording, args=[duration]).start()

def start_recording_button_clicked():
    duration = int(duration_entry.get())
    start_time = time_entry.get()
    start_time = datetime.datetime.strptime(start_time, "%H:%M")
    schedule_recording(duration, start_time)
    status_label.config(text="Recording scheduled.")

# Create the GUI
app = tk.Tk()
app.title("Scheduled Audio Recorder")

duration_label = tk.Label(app, text="Recording Duration (seconds):")
duration_label.pack()

duration_entry = tk.Entry(app)
duration_entry.pack()

time_label = tk.Label(app, text="Recording Time (HH:MM):")
time_label.pack()

time_entry = tk.Entry(app)
time_entry.pack()

start_button = tk.Button(app, text="Start Recording", command=start_recording_button_clicked)
start_button.pack()

status_label = tk.Label(app, text="")
status_label.pack()

app.mainloop()
