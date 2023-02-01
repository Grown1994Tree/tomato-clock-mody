#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import time
import subprocess
from absl import app,flags

WORK_MINUTES = 25
BREAK_MINUTES = 5
CYCLES = 1
flags.DEFINE_integer("t",25,"设置工作时长")
flags.DEFINE_integer("b",5,"设置休息时长")
flags.DEFINE_integer("c",1,"设置循环次数")
FLAGS=flags.FLAGS
    
    
def main(argv):
    work_minutes = WORK_MINUTES
    break_minutes = BREAK_MINUTES
    cycles = CYCLES
    try:
        if FLAGS.t:
            work_minutes = FLAGS.t
        
        if FLAGS.b:
            break_minutes = FLAGS.b 
        
        if FLAGS.c:
            cycles = FLAGS.c
        
        for i in range(int(cycles)):
            print(f'🍅 工作 {work_minutes} 分钟. Ctrl+C to exit')
            tomato(work_minutes, '是时候去休息了')
            print(f'🛀 休息 {break_minutes} 分钟. Ctrl+C to exit')
            tomato(break_minutes, '是时候去工作了')
        print("恭喜你完成工作")
    except KeyboardInterrupt:
        print('\n👋 再见')
    except Exception as ex:
        print(ex)
        exit(1)


def tomato(minutes, notify_msg):
    start_time = time.perf_counter()
    while True:
        diff_seconds = int(round(time.perf_counter() - start_time))
        left_seconds = minutes * 60 - diff_seconds
        if left_seconds <= 0:
            print('')
            break

        countdown = '{}:{} ⏰'.format(int(left_seconds / 60), int(left_seconds % 60))
        duration = min(minutes, 25)
        progressbar(diff_seconds, minutes * 60, duration, countdown)
        time.sleep(1)

    notify_me(notify_msg)


def progressbar(curr, total, duration=10, extra=''):
    frac = curr / total
    filled = round(frac * duration)
    print('\r', '🍅' * filled + '--' * (duration - filled), '[{:.0%}]'.format(frac), extra, end='')


def notify_me(msg):
    '''
    # macos desktop notification
    terminal-notifier -> https://github.com/julienXX/terminal-notifier#download
    terminal-notifier -message <msg>

    # ubuntu desktop notification
    notify-send

    # voice notification
    say -v <lang> <msg>
    lang options:
    - Daniel:       British English
    - Ting-Ting:    Mandarin
    - Sin-ji:       Cantonese
    '''

    print(msg)
    try:
        if sys.platform == 'darwin':
            # macos desktop notification
            subprocess.run(['terminal-notifier', '-title', '🍅', '-message', msg])
            subprocess.run(['say', '-v', 'Daniel', msg])
        elif sys.platform.startswith('linux'):
            # ubuntu desktop notification
            subprocess.Popen(["notify-send", '🍅', msg])
        else:
            # windows?
            # TODO: windows notification
            pass

    except:
        # skip the notification error
        pass



if __name__ == "__main__":
    app.run(main)
