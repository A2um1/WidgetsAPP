"""

Widgets 工具包  Beta V 0.9.5
Author: Wayland
所需库 Tkinter, pillow

"""
import configparser
import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image, ImageTk

favicon = ''


class Window:
    @staticmethod
    def exit(win):
        win.destroy()

    @staticmethod
    def win(title=None, size=None, bg=None, fg=None, font=None, logo=None, resizable=True):
        """
        创建一个主窗口
        并且进行全局样式设定
        :param resizable:
        :param title: 窗口标题
        :param size: 窗口大小
        :param bg: 背景色
        :param fg: 文字颜色
        :param font: 字体样式元组
        :param logo: APP图标文件路径
        :return: 返回窗口对象
        """
        window = tk.Tk()
        window.title(title)
        Style.Window.bg = window['bg'] = bg
        global favicon
        favicon = tk.PhotoImage("photo", file=logo)
        if logo:
            window.iconphoto(True, favicon)

        if not resizable:
            window.resizable(False, False)

        if size:
            if not isinstance(size, str):
                size = f'{size[0]}x{size[1]}'

            window.geometry(size)
            Style.Window.size = size

        Style.Window.logo = logo
        Style.Button.bg = Style.Checkbox.bg = Style.Window.bg = Style.Label.bg = bg
        Style.Label.font = Style.Button.font = Style.Checkbox.font = Style.Window.font = font
        Style.Button.fg = Style.Checkbox.fg = Style.Label.fg = Style.Window.fg = fg

        window.loop = window.mainloop
        return window

    @staticmethod
    def top_win(title=None, size=None, bg=None, logo=None):
        """
        生成一个顶层窗口
        :param title: 窗口标题
        :param size: 窗口大小
        :param bg: 背景颜色
        :param logo: 顶层窗口路径
        :return: 返回一个顶层窗口对象
        """
        window = tk.Toplevel()
        window.title = title
        window['bg'] = bg
        if not logo:
            logo = Style.Window.logo
        window.iconbitmap(logo)

        if size:
            window.geometry(size)
        else:
            window.geometry(Style.Window.size)

        return window


class Widgets:

    @staticmethod
    def label(x, y, text=None, width=None, height=None, bg=None, fg=None, font: (int, str) = (0, ''),
              multiline: bool = False, justify: str = "",
              window=None):
        """
        添加一个标签
        :param justify: 对齐 可选 left center right
        :param multiline:
        :param x: 起始X
        :param y: 起始Y
        :param text: 文字
        :param width: 宽
        :param height: 高
        :param bg: 背景色
        :param fg: 文字颜色
        :param font: 字体样式元组 大小 特征
        :param window: 窗口对象
        :return: 标签对象
        """
        if not bg:
            bg = Style.Label.bg

        if not fg:
            fg = Style.Label.fg

        if font[0]:
            keys = font[1]
            keyword = []
            if 'b' in keys:
                keyword.append('bold')
            if '/' in font:
                keyword.append('italic')

            if '_' in keys:
                keyword.append('underline')
            if '-' in keys:
                keyword.append('overstrike')

            keyword = ' '.join(keyword)

            font = ('microsoft yahei', font[0], keyword)
        else:
            font = None

        if not height:
            height = Style.Label.height

        if not width:
            width = Style.Label.width
        if not justify:
            justify = tk.CENTER
        else:
            justify = tk.RIGHT if justify.upper() == "RIGHT" else tk.LEFT

        if multiline:
            widget = tk.Message(window, text=text, bg=bg, fg=fg, font=font,justify=justify)
        else:
            widget = tk.Label(window, text=text, bg=bg, fg=fg, font=font, justify=justify)


        widget.show = lambda: widget.place(x=x, y=y, width=width, height=height)
        widget.hide = widget.place_forget
        widget.show()
        return widget

    @staticmethod
    def image(x, y, src, width=None, height=None, bg=None, window=None):
        """
        绘制一个图片
        :param x: 起始X
        :param y: 起始Y
        :param src: 图片路径
        :param width: 图片宽
        :param height: 图片高
        :param bg: 背景色
        :param window: 窗口对象
        :return: 标签对象
        """

        if not bg:
            bg = Style.Window.bg

        img = Image.open(src, 'r')
        if width and height:
            img = img.resize((width, height))
        img = ImageTk.PhotoImage(img)
        Label = tk.Label(window, image=img, bg=bg)
        Label.image = img
        Label.show = lambda: Label.place(x=x, y=y)
        Label.hide = Label.place_forget
        Label.show()
        return Label

    @staticmethod
    def button(x, y, text, func, *args, width=None, height=None, bg=None, fg=None, mouse_enter_bg=None,
               mouse_leave_bg=None, active_bg=None, active_fg=None,
               font=None, window=None):
        """
        部署一个按钮
        :param x: 起始X
        :param y: 起始Y
        :param text: 文字
        :param func: 绑定函数
        :param args: 函数参数
        :param width: 宽度
        :param height: 高度
        :param bg: 背景颜色
        :param fg: 文字颜色
        :param mouse_enter_bg: 鼠标移入颜色
        :param mouse_leave_bg: 鼠标移出颜色
        :param active_bg: 鼠标按下背景颜色
        :param active_fg: 鼠标按下文字颜色
        :param font: 字体样式元组
        :param window: 窗口对象
        :return: 按钮对象
        """
        if not bg:
            bg = Style.Button.bg

        if not fg:
            fg = Style.Button.fg

        if not font:
            font = Style.Button.font

        if not active_bg:
            active_bg = Style.Button.active_bg

        if not active_fg:
            active_fg = Style.Button.active_fg

        Button = tk.Button(window, text=text, bg=bg, font=font, fg=fg, command=lambda: func(*args),
                           activeforeground=active_fg, activebackground=active_bg)

        if not mouse_enter_bg:
            mouse_enter_bg = Style.Button.mouse_enter_bg

        if not mouse_leave_bg:
            mouse_leave_bg = Style.Button.mouse_leave_bg

        def mouse_enter(self):
            Button['bg'] = mouse_enter_bg

        def mouse_leave(self):
            Button['background'] = mouse_leave_bg

        Button.bind("<Enter>", mouse_enter)
        Button.bind("<Leave>", mouse_leave)

        if not height:
            height = Style.Button.height

        if not width:
            width = Style.Button.width

        Button.show = lambda: Button.place(x=x, y=y, width=width, height=height)
        Button.hide = Button.place_forget
        Button.show()
        return Button

    @staticmethod
    def buttons(x, y, text_list, func_list, param_list, width=None, height=None, column=1, x_interval=None,
                y_interval=None, bg=None,
                fg=None, mouse_enter_bg=None,
                mouse_enter_fg=None, mouse_leave_fg=None,
                mouse_leave_bg=None,
                font=None, window=None, active_bg=None, active_fg=None):
        """
        快速部署集群按钮
        函数, 文字, 参数 按照下标相对应
        :param x: 起始X
        :param y: 起始Y
        :param text_list: 文字列表
        :param func_list: 函数列表, 也可为一个函数
        :param param_list: 函数对应的参数列表
        :param width: 宽度
        :param height: 高度
        :param column: 集群中最大列数
        :param x_interval: 集群按钮间横向距离
        :param y_interval: 集群按钮间纵向距离
        :param bg: 背景颜色
        :param fg: 文字颜色
        :param mouse_enter_bg: 鼠标移入颜色
        :param mouse_leave_bg: 鼠标移出颜色
        :param font: 字体样式元组
        :param window: 窗口对象
        :return: 无
        """

        if not bg:
            bg = Style.Button.bg

        if not fg:
            fg = Style.Button.fg

        if not font:
            font = Style.Button.font

        if not height:
            height = Style.Button.height

        if not width:
            width = Style.Button.width

        if not mouse_enter_bg:
            mouse_enter_bg = Style.Button.mouse_enter_bg

        if not mouse_leave_bg:
            mouse_leave_bg = Style.Button.mouse_leave_bg

        if not mouse_enter_fg:
            mouse_enter_fg = Style.Button.mouse_enter_fg

        if not mouse_leave_fg:
            mouse_leave_fg = Style.Button.mouse_leave_fg

        if not active_bg:
            active_bg = Style.Button.bg

        if not active_fg:
            active_fg = Style.Button.bg

        if not x_interval:
            x_interval = width

        if not y_interval:
            y_interval = height

        # 将参数可解包化
        param_args = list()
        for param in param_list:
            if isinstance(param, (tuple, list)):
                param_args.append(param)
            else:
                param_args.append([param])

        for i in range(len(text_list)):
            Button = tk.Button(window, text=text_list[i], bg=bg, font=font, fg=fg,
                               activebackground=active_bg, activeforeground=active_fg,
                               command=lambda param=param_args[i]: func_list[i](*param) if isinstance(func_list, (
                                   list, tuple)) else func_list(*param))

            def mouse_enter(self):
                Button['background'] = mouse_enter_bg
                Button['foreground'] = mouse_enter_fg

            def mouse_leave(self):
                Button['background'] = mouse_leave_bg
                Button['foreground'] = mouse_leave_fg

            Button.bind("<Enter>", mouse_enter)
            Button.bind("<Leave>", mouse_leave)

            Button.place(x=x + x_interval * ((i + 1) % column), y=y + y_interval * int((i + 1) / column),
                         width=width,
                         height=height)

    @staticmethod
    def checkbox(x, y, *args, width=None, height=None, column=1, x_interval=None, y_interval=None, bg=None,
                 fg=None,
                 select_bg=None, active_bg=None, active_fg=None, font=None, default_value=False, window=None):
        """
        快速部署选择器集群
        :param x: 起始X
        :param y: 起始Y
        :param args: 文字
        :param width: 宽度
        :param height: 高度
        :param column: 最大列数
        :param x_interval: 横向间距
        :param y_interval: 纵向间距
        :param bg: 背景色
        :param fg: 文字颜色
        :param select_bg: 选择器颜色
        :param active_bg: 按下背景色
        :param active_fg: 按下文字色
        :param font: 字体样式元组
        :param default_value: 默认选中 True/False
        :param window: 窗口对象
        :return: 返回选择器列表
        """
        binder_list = list()

        if not width:
            width = Style.Checkbox.width
        if not height:
            width = Style.Checkbox.width

        if not bg:
            bg = Style.Checkbox.bg

        if not fg:
            fg = Style.Checkbox.fg

        if not active_bg:
            active_bg = Style.Checkbox.active_bg

        if not select_bg:
            select_bg = Style.Checkbox.selector_bg

        if not x_interval:
            x_interval = width

        if not y_interval:
            y_interval = height

        for index, item in enumerate(args):
            val_binder = tk.IntVar()
            val_binder.set(default_value)
            choice_button = tk.Checkbutton(window, text=item, variable=val_binder,
                                           relief=tk.RAISED,
                                           selectcolor=select_bg, bg=bg, fg=fg,
                                           font=font,
                                           activeforeground=active_fg, activebackground=active_bg)
            choice_button.place(x=x + ((index + 1) % column) * x_interval, y=y + int((index + 1) / 3) * y_interval,
                                width=width, height=height)
            binder_list.append(val_binder)

        return binder_list

    @staticmethod
    def entry(x, y, *args, password=False, width=None, height=None, bg=None, fg=None, font=None, window=None):
        v = tk.StringVar()
        if not bg:
            bg = Style.Button.bg

        if not fg:
            fg = Style.Button.fg

        if not font:
            font = Style.Button.font

        Entry = tk.Entry(window, textvariable=v, bg=bg, font=font, fg=fg)

        if not height:
            height = Style.Entry.height

        if not width:
            width = Style.Entry.width

        if password:
            Entry['show'] = '*'

        Entry.show = lambda: Entry.place(x=x, y=y, width=width, height=height)
        Entry.hide = Entry.place_forget
        Entry.show()
        return Entry

    @staticmethod
    def ScrollBar(side='right', window=None):
        pass

    @staticmethod
    def List(window=None):
        tk.Listbox(window)


class Tools:

    @staticmethod
    def clean(window):
        """
        清空一个窗口
        :param window: 目标窗口
        :return: 无
        """
        for child in window.winfo_children():
            child.destroy()

    @staticmethod
    def tip(text, title=None):
        """
        弹窗提示信息
        :param text: 文字
        :param title: 题目
        :return: 无
        """
        if not title:
            title = Style.Msg.title
        msg.showinfo(title=title, message=text)

    @staticmethod
    def linked(*args):
        class Widget:
            def __init__(self, widgets):
                ws = []
                for i in widgets:
                    ws.append(i)
                self.ws = ws

            def show(self):
                for i in self.ws:
                    i.show()

            def hide(self):
                for i in self.ws:
                    i.hide()

            def destroy(self):
                for i in self.ws:
                    i.destroy()

        return Widget(args)


src = ''
db = configparser.ConfigParser()


class Static:
    def __init__(self, path: str):
        global db, src
        src = path
        db.read(path, encoding="utf-8")
        if not db.has_section("db"):
            db.add_section("db")
            db.write(open("ini", "w", encoding="utf-8"))

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        db.set('db', key, str(value))
        db.write(open(src, 'w', encoding="utf-8"))

    def __setitem__(self, key, value):
        db.set('db', key, str(value))
        db.write(open(src, 'w', encoding="utf-8"))

    def __getitem__(self, k):

        if not db.has_option('db', k):
            return None
        v = db.get("db", k)
        if v:
            if db.get('db', k).isdigit() or v[0] == "-":
                v = eval(v)
        return v

    @staticmethod
    def set(k: str, v):
        db.set('db', k, str(v))
        db.write(open(src, 'w', encoding="utf-8"))

    @staticmethod
    def get(k: str):
        return db.get('db', k)

    @staticmethod
    def data():
        return db.items('db')


class Style:
    class Window:
        bg = None
        size = None
        font = None
        fg = None
        logo = None

    class Label:
        bg = None
        font = None
        fg = None

        width = None
        height = None

    class Button:
        bg = None
        fg = None

        width = 100
        height = None

        active_fg = None
        active_bg = None

        mouse_enter_bg = None
        mouse_leave_bg = None

        mouse_enter_fg = None
        mouse_leave_fg = None

        font = None

    class Checkbox:
        bg = None
        fg = None

        width = None
        height = None

        selector_bg = None

        active_fg = None
        active_bg = None

        mouse_enter_bg = None
        mouse_leave_bg = None

        mouse_enter_fg = None
        mouse_leave_fg = None

        font = None

    class Msg:
        title = None

    class Entry:
        bg = None
        fg = None

        width = None
        height = None

        active_fg = None
        active_bg = None

        font = None


class Error:
    class WindowSizeError(Exception):
        def __str__(self):
            return 'Parameter "Window_size" should be an iterable object with two integer : width, height'

    class ColonyError(Exception):
        def __str__(self):
            return "Colony's row*column should equal to its amount of members."
