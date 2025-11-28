import tkinter as tk
from PIL import Image, ImageTk
import sys
from pynput import keyboard
import threading

# 全局变量：记录Win键是否按下，用于识别组合键
win_pressed = False

def fun(n):
	import os
	import sys
	return os.path.join(getattr(sys, "_MEIPASS", os.path.abspath(".")))

def on_press(key):
    """全局按键按下事件：拦截Win键及相关组合键"""
    global win_pressed
    try:
        # 拦截Win键本身
        if key == keyboard.Key.cmd or key == keyboard.Key.cmd_r:
            win_pressed = True
            return False  # 阻止系统接收Win键事件
        
        # 拦截Win+Ctrl+D（新建桌面）、Win+D（显示桌面）等组合键
        if win_pressed:
            # 拦截Win+Ctrl+D
            if (key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r) and key.char == 'd':
                return False
            # 拦截Win+D
            elif key.char == 'd':
                return False
            # 拦截Win+Tab（任务视图）
            elif key == keyboard.Key.tab:
                return False
            # 可继续添加其他Win组合键（如Win+E、Win+R等）
        
    except AttributeError:
        # 处理特殊键（如Ctrl、Alt等）
        pass
    return False  # 阻止所有按键事件传递（可选：仅拦截Win相关则调整逻辑）

def on_release(key):
    """全局按键释放事件：重置Win键状态"""
    global win_pressed
    if key == keyboard.Key.cmd or key == keyboard.Key.cmd_r:
        win_pressed = False
    return False

def start_keyboard_listener():
    """启动全局键盘监听器（线程中运行）"""
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    # 创建tk主窗口
    root = tk.Tk()
    # 全屏+置顶+隐藏边框（防拖拽/关闭）
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.overrideredirect(True)  # 隐藏标题栏和边框
    
    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # 加载并缩放图片
    try:
        image = Image.open(fun("windows.png"))
        image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
    except FileNotFoundError:
        print("错误：未找到windows.png文件！")
        sys.exit(1)
    
    # 显示图片
    label = tk.Label(root, image=photo)
    label.pack(fill=tk.BOTH, expand=True)
    
    # 拦截窗口关闭事件
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # 启动全局键盘监听线程（避免阻塞tk主循环）
    listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
    listener_thread.start()
    
    # 启动tk主循环
    root.mainloop()

if __name__ == "__main__":
    # 依赖安装：pip install pillow pynput
    # 注意：需以【管理员身份】运行脚本，否则全局监听无效！
    main()
