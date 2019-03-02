import time
import keyboard

before_time = time.perf_counter()

print(before_time)

while True:
    if keyboard.is_pressed("s"):
        before_time = time.perf_counter()
        break

while True:
    if keyboard.is_pressed("p"):
        new_time = time.perf_counter()
        break

print(new_time - before_time)