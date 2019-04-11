#! -*- coding:utf-8 -*-

import wx
from cefpython3 import cefpython as cef
import platform
import sys
import os
import threading

import server

# reload(sys)
# sys.setdefaultencoding('utf-8')

WindowUtils = cef.WindowUtils()

WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

WIDTH = 1280
HEIGHT = 800

g_count_windows = 0

class Interaction(object):
    def __init__(self, frame):
        self.frame = frame

    def open_dir_dialog(self,callback):
        print('open_dir_dialog')

        dialog = wx.DirDialog(self.frame, u'请选择目录', '', style=(wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST))
        if dialog.ShowModal() != wx.ID_OK:
            return
        path = dialog.GetPath()
        dialog.Destroy()
        callback.Call(path)

    def open_multi_file_dialog(self,callback):
        print('open_dir_dialog')

        dialog = wx.FileDialog(self.frame, u'请选择文件', '', wildcard="JPG files (*.jpeg;*.jpg)|*.jpeg;*.jpg|PNG files (*.png)|*.png", style=(wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST))
        if dialog.ShowModal() != wx.ID_OK:
            return
        paths = dialog.GetPaths()
        dialog.Destroy()
        callback.Call(paths)

    def open_excel_file_dialog(self,callback):
        print('open_dir_dialog')

        dialog = wx.FileDialog(self.frame, u'请选择文件', '', wildcard="Excel files (*.xlsx)|*.xlsx", style=(wx.FD_OPEN | wx.FD_FILE_MUST_EXIST))
        if dialog.ShowModal() != wx.ID_OK:
            return
        path = dialog.GetPath()
        dialog.Destroy()
        callback.Call(path)

    def save_excel_file_dialog(self,callback):
        print('save_dir_dialog')

        dialog = wx.FileDialog(self.frame, u'请选择文件', '', wildcard="Excel files (*.xlsx)|*.xlsx", style=(wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT))
        if dialog.ShowModal() != wx.ID_OK:
            return
        path = dialog.GetPath()
        dialog.Destroy()
        callback.Call(path)

    def save_db_file_dialog(self,callback):
        print('save_db_dialog')

        dialog = wx.FileDialog(self.frame, u'请选择文件', '', wildcard="DB files (*.sqlite)|*.sqlite", style=(wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT))
        if dialog.ShowModal() != wx.ID_OK:
            return
        path = dialog.GetPath()
        dialog.Destroy()
        callback.Call(path)

    def open_db_file_dialog(self,callback):
        print('open_db_dialog')

        dialog = wx.FileDialog(self.frame, u'请选择文件', '', wildcard="DB files (*.sqlite)|*.sqlite", style=(wx.FD_OPEN | wx.FD_FILE_MUST_EXIST))
        if dialog.ShowModal() != wx.ID_OK:
            return
        path = dialog.GetPath()
        dialog.Destroy()
        callback.Call(path)

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title=u'', size=(WIDTH, HEIGHT))
        self.browser = None

        if LINUX:
            WindowUtils.InstallX11ErrorHandlers()

        global g_count_windows
        g_count_windows += 1

        self.setup_icon()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.browser_panel = wx.Panel(self, style=wx.WANTS_CHARS)
        self.browser_panel.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.browser_panel.Bind(wx.EVT_SIZE, self.OnSize)

        if LINUX:
            self.Show()
            if wx.version().startswith("3.") or wx.version().startswith("4."):
                wx.CallLater(20, self.embed_browser)
            else:
                self.embed_browser()
        else:
            self.embed_browser()
            self.Show()

    def setup_icon(self):
        icon_file = os.path.join(os.getcwd(),"ident.ico")
        if os.path.exists(icon_file) and hasattr(wx, "IconFromBitmap"):
            icon = wx.IconFromBitmap(wx.Bitmap(icon_file, wx.BITMAP_TYPE_PNG))
            self.SetIcon(icon)

    def embed_browser(self):
        window_info = cef.WindowInfo()
        (width, height) = self.browser_panel.GetClientSize().Get()
        window_info.SetAsChild(self.browser_panel.GetHandle(), [0, 0, width, height])

        self.browser = cef.CreateBrowserSync(window_info)
        self.browser.SetClientHandler(FocusHandler())

        bindings = cef.JavascriptBindings(bindToFrames=False, bindToPopups=False)
        bindings.SetObject("interaction", Interaction(self))

        self.browser.SetJavascriptBindings(bindings)
        self.browser.LoadUrl("http://127.0.0.1:5000")

    def OnSetFocus(self, _):
        if not self.browser:
            return
        if WINDOWS:
            WindowUtils.OnSetFocus(self.browser_panel.GetHandle(), 0, 0, 0)
        self.browser.SetFocus(True)

    def OnSize(self, _):
        if not self.browser:
            return
        if WINDOWS:
            WindowUtils.OnSize(self.browser_panel.GetHandle(), 0, 0, 0)
        elif LINUX:
            (x, y) = (0, 0)
            (width, height) = self.browser_panel.GetSize().Get()
            self.browser.SetBounds(x, y, width, height)
        # self.browser.NotifyMoveOrResizeStarted()

    def OnClose(self, event):
        if not self.browser:
            return

        if MAC:
            self.browser.CloseBrowser()
            self.clear_browser_references()
            self.Destroy()
            global g_count_windows
            g_count_windows -= 1
            if g_count_windows == 0:
                cef.Shutdown()
                wx.GetApp().ExitMainLoop()
                os._exit(0)
        else:
            self.browser.ParentWindowWillClose()
            event.Skip()
            self.clear_browser_references()

    def clear_browser_references(self):
        self.browser = None

class FocusHandler(object):
    def OnGotFocus(self, browser, **_):
        if LINUX:
            browser.SetFocus(True)

    def OnLoadStart(self, browser, frame):
        print("LoadStart")

    def OnLoadEnd(self, browser, frame, *args, **kwargs):
        print("LoadEnd")
        # frame.ExecuteJavascript("alert(1)")
        # frame.ExecuteJavascript("document.oncontextmenu = function() {return false;}")

class CefApp(wx.App):
    def __init__(self, redirect):
        self.timer = None
        self.timer_id = 1
        self.is_initialized = False
        super(CefApp, self).__init__(redirect=redirect)

    def OnPreInit(self):
        super(CefApp, self).OnPreInit()
        if MAC and wx.version().startswith("4."):
            self.initialize()

    def OnInit(self):
        self.initialize()
        return True

    def initialize(self):
        if self.is_initialized:
            return
        self.is_initialized = True
        self.create_timer()
        frame = MainFrame()
        self.SetTopWindow(frame)
        frame.Show()

    def create_timer(self):
        self.timer = wx.Timer(self, self.timer_id)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(5)

    def on_timer(self, _):
        cef.MessageLoopWork()

    def OnExit(self):
        self.timer.Stop()
        return 0

def run_browser():
    sys.excepthook = cef.ExceptHook
    settings = {}
    if WINDOWS:
        settings["auto_zooming"] = "system_dpi"
        cef.DpiAware.SetProcessDpiAware()
    cef.Initialize(settings)
    app = CefApp(False)
    app.MainLoop()
    del app
    if not MAC:
        cef.Shutdown()

def run_server():
    server.start()

def main():
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()

    run_browser()

if __name__ == '__main__':
    main()