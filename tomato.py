#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import time
import subprocess

WORK_MINUTES = 25
BREAK_MINUTES = 5
CYCLES = 1

def main():
    args_len = len(sys.argv)
    if args_len == 1 or args_len == 3 or args_len == 5 or args_len == 7:
        args_dict = {}
        for i in range(1,args_len,2):
            args_dict[sys.argv[i]] = sys.argv[i+1]
    
        Exec(args_dict)
    elif sys.argv[1] == '-h':
        help()
    else:
        print("参数输入不符合规范")

def Exec(args_dict):
    work_minutes = WORK_MINUTES
    break_minutes = BREAK_MINUTES
    cycles = CYCLES
    try:
        for key in args_dict.keys():
            if key == '-t':
                work_minutes = int(args_dict[key])
            
            if key ==  '-b':
                break_minutes = int(args_dict[key])

            if key == '-c':
                cycles = int(args_dict[key])

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


def help():
    appname = sys.argv[0]
    appname = appname if appname.endswith('.py') else 'tomato'  # tomato is pypi package
    print('====== 🍅 Tomato Clock =======')
    print(f'{appname}         # 工作 {WORK_MINUTES} 分钟 ，休息 {BREAK_MINUTES} 分钟')
    print(f'{appname} -t <n>  # 工作 <n> 分钟')
    print(f'{appname} -b <n>  # 休息 <n> 分钟')
    print(f'{appname} -h      # 帮助')
    print(f'{appname} -r <n>  # 循环 <n> 次番茄时间')


if __name__ == "__main__":
    main()
