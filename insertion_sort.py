import pygame
import random
import cv2
import numpy as np
import math
import time
import wave
import subprocess
import os

WIDTH, HEIGHT = 800, 400
FPS = 60
N = 200

BAR_COLOR = (84, 227, 70)
DONE_COLOR = (255, 255, 255)
PIVOT_COLOR = (255, 0, 0)
BG_COLOR = (0, 0, 0)

SAMPLE_RATE = 44100
SOUND_DURATION = 0.09
MIN_FREQ = 132
MAX_FREQ_SPAN = 1100
MAX_POLYPHONY = 16
WAVEFORM = "triangle"

pygame.init()
pygame.mixer.pre_init(SAMPLE_RATE, -16, 1, 512)
try:
    pygame.mixer.init()
except Exception:
    print("Warning: pygame.mixer failed to init; sound will be disabled.")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Insertion Sort")
clock = pygame.time.Clock()

video_filename = "insertion_800x400.mp4"
video = cv2.VideoWriter(
    video_filename,
    cv2.VideoWriter_fourcc(*"mp4v"),
    FPS,
    (WIDTH, HEIGHT)
)

class SoundEngine:
    def __init__(self, sample_rate=44100, duration=0.09, waveform="triangle", max_poly=16):
        self.sample_rate = sample_rate
        self.duration = duration
        self.waveform = waveform
        self.cache = {}
        self.max_poly = max_poly
        try:
            pygame.mixer.set_num_channels(max_poly)
            self.channels = [pygame.mixer.Channel(i) for i in range(max_poly)]
        except Exception:
            self.channels = []
        self.next_chan = 0
        self.events = []
        self.start_time = None

    def _generate_wave(self, freq, duration=None):
        if duration is None:
            duration = self.duration
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        if self.waveform == "sine":
            wave_arr = np.sin(2 * np.pi * freq * t)
        elif self.waveform == "square":
            wave_arr = np.sign(np.sin(2 * np.pi * freq * t))
        else:
            wave_arr = 2 * np.abs(2 * (freq * t - np.floor(freq * t + 0.5))) - 1
        attack_len = int(0.005 * self.sample_rate)
        decay_len = len(wave_arr) - attack_len
        env = np.ones_like(wave_arr)
        if attack_len > 0:
            env[:attack_len] = np.linspace(0, 1.0, attack_len)
        if decay_len > 0:
            env[attack_len:] = np.exp(-3.5 * (np.arange(decay_len) / decay_len))
        wave_arr = wave_arr * env
        return np.int16(wave_arr * 32767 * 0.25)

    def get_sound(self, freq):
        try:
            init_info = pygame.mixer.get_init()
        except Exception:
            init_info = None
        if init_info is None:
            class _Dummy():
                def play(self): pass
            return _Dummy()
        _, _, channels = init_info
        key = int(round(freq / 5.0) * 5)
        cache_key = (key, channels)
        if cache_key in self.cache:
            return self.cache[cache_key]
        mono = self._generate_wave(key)
        if channels == 2:
            arr = np.column_stack((mono, mono))
        else:
            arr = mono.copy()
        arr = np.ascontiguousarray(arr, dtype=np.int16)
        try:
            sound = pygame.sndarray.make_sound(arr)
        except Exception:
            class _Dummy():
                def play(self): pass
            sound = _Dummy()
        self.cache[cache_key] = sound
        return sound

    def play_freq(self, freq, volume=0.4, duration=None):
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()
        if duration is None:
            duration = self.duration
        start_ms = pygame.time.get_ticks() - self.start_time
        self.events.append((start_ms, float(freq), float(duration), float(volume)))
        sound = self.get_sound(freq)
        if not self.channels:
            try: sound.play()
            except: pass
            return
        ch = self.channels[self.next_chan]
        self.next_chan = (self.next_chan + 1) % self.max_poly
        try:
            ch.set_volume(volume)
            ch.play(sound)
        except:
            try: sound.play()
            except: pass

sound_engine = SoundEngine(sample_rate=SAMPLE_RATE, duration=SOUND_DURATION, waveform=WAVEFORM, max_poly=MAX_POLYPHONY)

def draw_frame(arr, highlight=None, finish=False, end_index=None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            video.release()
            pygame.quit()
            exit()
    screen.fill(BG_COLOR)
    bar_w = WIDTH // len(arr)
    for i, v in enumerate(arr):
        if finish and i <= end_index:
            color = DONE_COLOR
        elif highlight and i in highlight:
            color = PIVOT_COLOR
        else:
            color = BAR_COLOR
        pygame.draw.rect(screen, color, (i * bar_w, HEIGHT - v, bar_w - 1, v))
    pygame.display.update()
    frame = pygame.surfarray.array3d(screen)
    frame = np.transpose(frame, (1, 0, 2))
    video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    clock.tick(FPS)

def value_to_freq(value, max_value):
    if max_value <= 0:
        return MIN_FREQ
    norm = float(value) / float(max_value)
    freq = MIN_FREQ + norm * MAX_FREQ_SPAN
    return max(40, int(freq))

def insertion_sort(arr, play_sound=True):
    n = len(arr)
    max_val = max(arr) if arr else 1
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        if play_sound:
            sound_engine.play_freq(value_to_freq(key, max_val), volume=0.22)
        while j >= 0 and arr[j] > key:
            if play_sound:
                sound_engine.play_freq(value_to_freq(arr[j], max_val), volume=0.16)
                sound_engine.play_freq(value_to_freq(arr[j+1], max_val), volume=0.28)
            arr[j+1] = arr[j]
            draw_frame(arr, highlight={j, j+1})
            j -= 1
        arr[j+1] = key
        if play_sound:
            sound_engine.play_freq(value_to_freq(arr[j+1], max_val), volume=0.28)
        draw_frame(arr, highlight={j+1})

def finish_white(arr, per_bar_delay_ms=18):
    max_val = max(arr) if arr else 1
    base = MIN_FREQ
    span = MAX_FREQ_SPAN
    arpeggio_notes = [base + span * (i / 8) for i in (2, 3, 4, 5, 7)]
    for f in arpeggio_notes:
        sound_engine.play_freq(int(f), volume=0.28)
        pygame.time.delay(30)
    for i in range(len(arr)):
        draw_frame(arr, finish=True, end_index=i)
        freq = value_to_freq(arr[i], max_val)
        sound_engine.play_freq(freq, volume=0.22)
        pygame.time.delay(per_bar_delay_ms)
    final_freqs = [
        value_to_freq(max_val, max_val),
        value_to_freq(int(max_val * 0.66), max_val),
        value_to_freq(int(max_val * 0.33), max_val)
    ]
    for f in final_freqs:
        sound_engine.play_freq(int(f), volume=0.34)
    pygame.time.delay(200)
    tail_notes = [final_freqs[0], final_freqs[1], final_freqs[2]]
    for f in tail_notes:
        sound_engine.play_freq(int(f * 0.85), volume=0.22)
        pygame.time.delay(80)
    pygame.time.delay(120)

def synthesize_events_to_wav(events, sample_rate=44100, filename="audio.wav", waveform="triangle"):
    if not events:
        return
    start_ms = min(e[0] for e in events)
    end_ms = max(e[0] + int(e[2]*1000) for e in events)
    total_samples = int((end_ms - start_ms) * sample_rate / 1000) + 1
    master = np.zeros(total_samples, dtype=np.float64)
    def make_wave(freq, duration_s):
        t = np.linspace(0, duration_s, int(sample_rate*duration_s), endpoint=False)
        if waveform == "sine":
            w = np.sin(2*np.pi*freq*t)
        elif waveform == "square":
            w = np.sign(np.sin(2*np.pi*freq*t))
        else:
            w = 2*np.abs(2*(freq*t - np.floor(freq*t + 0.5))) - 1
        attack = int(0.005*sample_rate)
        if attack > 0 and len(w) > attack:
            env = np.ones_like(w)
            env[:attack] = np.linspace(0, 1.0, attack)
            env[attack:] = np.exp(-3.5 * (np.arange(len(w)-attack) / max(1, len(w)-attack)))
            w *= env
        return w
    for evt in events:
        evt_start_ms, freq, duration_s, volume = evt
        pos = int((evt_start_ms - start_ms) * sample_rate / 1000)
        seg = make_wave(freq, duration_s)
        end_pos = pos + len(seg)
        if end_pos > len(master):
            master = np.pad(master, (0, end_pos - len(master)))
        master[pos:end_pos] += (seg * volume)
    max_amp = np.max(np.abs(master)) or 1.0
    master = master / max_amp * 0.95
    int16 = np.int16(master * 32767)
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int16.tobytes())

arr = [int((i + 1) * (HEIGHT - 60) / N) for i in range(N)]
random.shuffle(arr)
draw_frame(arr)
pygame.time.delay(300)
sound_engine.start_time = pygame.time.get_ticks()
insertion_sort(arr, play_sound=True)
finish_white(arr, per_bar_delay_ms=18)
pygame.time.delay(200)
video.release()

audio_filename = "audio.wav"
synthesize_events_to_wav(sound_engine.events, sample_rate=SAMPLE_RATE, filename=audio_filename, waveform=WAVEFORM)

output_with_audio = "insertion_with_audio.mp4"
ffmpeg_cmd = ["ffmpeg", "-y", "-i", video_filename, "-i", audio_filename, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", output_with_audio]
try:
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ {output_with_audio} created successfully!")
except Exception:
    print("⚠️ ffmpeg mux failed or ffmpeg not found. Video and audio files saved separately:")
    print(f" - video: {video_filename}")
    print(f" - audio: {audio_filename}")
    print("Install ffmpeg and run:")
    print(f"ffmpeg -y -i {video_filename} -i {audio_filename} -c:v copy -c:a aac -b:a 192k insertion_with_audio.mp4")

pygame.quit()
print("Done.")
