import pygame
import random
import cv2
import numpy as np
import time
import wave
import subprocess
import sys

# ================= CONFIG =================
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

VIDEO_FILE = "bubble_800x400.mp4"
AUDIO_FILE = "audio.wav"
FINAL_FILE = "bubble_with_audio.mp4"

# ============ INIT PYGAME (CORRECT ORDER) ============
pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 512)  # stereo-safe
pygame.init()

SOUND_ENABLED = True
try:
    pygame.mixer.init()
except pygame.error:
    SOUND_ENABLED = False
    print("⚠️ Sound disabled")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Sort")
clock = pygame.time.Clock()

# ============ VIDEO ============
video = cv2.VideoWriter(
    VIDEO_FILE,
    cv2.VideoWriter_fourcc(*"mp4v"),
    FPS,
    (WIDTH, HEIGHT)
)

if not video.isOpened():
    print("❌ VideoWriter failed")
    pygame.quit()
    sys.exit(1)

# ============ SOUND ENGINE ============
class SoundEngine:
    def __init__(self):
        self.events = []
        self.start_time = None
        self.cache = {}
        if SOUND_ENABLED:
            pygame.mixer.set_num_channels(MAX_POLYPHONY)
            self.channels = [pygame.mixer.Channel(i) for i in range(MAX_POLYPHONY)]
        else:
            self.channels = []

    def triangle_wave(self, freq, duration):
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        wave = 2 * np.abs(2 * (freq * t - np.floor(freq * t + 0.5))) - 1
        env = np.exp(-4 * t)
        return np.int16(wave * env * 32767 * 0.25)

    def get_sound(self, freq):
        key = int(freq)
        if key in self.cache:
            return self.cache[key]

        mono = self.triangle_wave(key, SOUND_DURATION)

        mixer_info = pygame.mixer.get_init()
        channels = mixer_info[2] if mixer_info else 1

        if channels == 2:
            data = np.column_stack((mono, mono))
        else:
            data = mono

        data = np.ascontiguousarray(data, dtype=np.int16)
        sound = pygame.sndarray.make_sound(data)
        self.cache[key] = sound
        return sound

    def play(self, freq, vol=0.3):
        if not SOUND_ENABLED:
            return

        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()

        now = pygame.time.get_ticks() - self.start_time
        self.events.append((now, freq, SOUND_DURATION, vol))

        ch = self.channels[now % MAX_POLYPHONY]
        ch.set_volume(vol)
        ch.play(self.get_sound(freq))

sound_engine = SoundEngine()

# ============ DRAW ============
def draw_frame(arr, highlight=None, done_upto=None):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            cleanup()

    screen.fill(BG_COLOR)
    bar_w = WIDTH / len(arr)

    for i, v in enumerate(arr):
        color = BAR_COLOR
        if done_upto is not None and i <= done_upto:
            color = DONE_COLOR
        elif highlight and i in highlight:
            color = PIVOT_COLOR

        x = int(i * bar_w)
        w = max(1, int(bar_w - 1))
        pygame.draw.rect(screen, color, (x, HEIGHT - v, w, v))

    pygame.display.flip()

    frame = pygame.surfarray.array3d(screen)
    frame = np.transpose(frame, (1, 0, 2))
    video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    clock.tick(FPS)

# ============ SORT ============
def freq_from_value(v, max_v):
    return int(MIN_FREQ + (v / max_v) * MAX_FREQ_SPAN)

def bubble_sort(arr):
    max_v = max(arr)
    n = len(arr)

    for i in range(n):
        for j in range(n - i - 1):
            sound_engine.play(freq_from_value(arr[j], max_v), 0.15)

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                sound_engine.play(freq_from_value(arr[j], max_v), 0.25)
                draw_frame(arr, highlight={j, j + 1})
        draw_frame(arr)

def finish(arr):
    max_v = max(arr)
    for i in range(len(arr)):
        sound_engine.play(freq_from_value(arr[i], max_v), 0.2)
        draw_frame(arr, done_upto=i)

# ============ AUDIO RENDER ============
def render_audio(events):
    if not events:
        return

    end_ms = max(s + int(d * 1000) for s, _, d, _ in events)
    samples = int(end_ms * SAMPLE_RATE / 1000)
    mix = np.zeros(samples)

    for start, freq, dur, vol in events:
        pos = int(start * SAMPLE_RATE / 1000)
        wave = sound_engine.triangle_wave(freq, dur).astype(np.float64) / 32767
        mix[pos:pos + len(wave)] += wave * vol

    mix /= np.max(np.abs(mix)) or 1
    pcm = np.int16(mix * 32767)

    with wave.open(AUDIO_FILE, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(pcm.tobytes())

# ============ CLEANUP ============
def cleanup():
    video.release()
    pygame.quit()
    sys.exit()

# ============ RUN ============
arr = [int((i + 1) * (HEIGHT - 60) / N) for i in range(N)]
random.shuffle(arr)

draw_frame(arr)
time.sleep(0.3)

bubble_sort(arr)
finish(arr)

video.release()
render_audio(sound_engine.events)

try:
    subprocess.run(
        ["ffmpeg", "-y", "-i", VIDEO_FILE, "-i", AUDIO_FILE,
         "-c:v", "copy", "-c:a", "aac", FINAL_FILE],
        check=True
    )
    print("✅ bubble_with_audio.mp4 created")
except Exception:
    print("⚠️ ffmpeg failed")

cleanup()
