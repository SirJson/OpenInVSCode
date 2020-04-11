
from os import environ
from fman import DirectoryPaneCommand, show_alert, load_json, save_json
from fman.url import as_human_readable
from subprocess import Popen, SubprocessError
from enum import IntFlag
from itertools import chain
from typing import List

CONFIG_FILE = "VSCodeLaunch.json"
ARG_OPENFOLDER = "--folder-uri"
ARG_NEWWND="-n"
ARG_REUSEWND="-r"

class LaunchOptions(IntFlag):
    NewWindow = 1,
    ReuseWindow = 2
    OpenFolder = 4


def launch_vscode(binName: str, options: LaunchOptions, userargs: List[str], args: list):
    cmdline = []
    cmdline = list(chain(cmdline,args))
    cmdline = [binName, ARG_NEWWND if LaunchOptions.NewWindow in options else ARG_REUSEWND, ARG_OPENFOLDER if LaunchOptions.OpenFolder in options else ""] + userargs + cmdline
    try:
        Popen(cmdline, env=environ,
              restore_signals=True, start_new_session=True)
    except OSError as oserr:
        show_alert(f"OS Error: {oserr}")
    except ValueError as valerr:
        show_alert(f"Startup failure: {valerr}")
    except SubprocessError as procerr:
        show_alert(f"Unknown startup exception: {procerr}")


def load_config() -> dict:
    config = load_json(CONFIG_FILE)
    if config is None:
        config = {
            "bin": "code",
            "additionalArgs": []
        }
        save_json(CONFIG_FILE, config)
    return config


class OpenFolderInCode(DirectoryPaneCommand):
    aliases = ('Open current pane in VSCode', 'Open current pane in Visual Studio Code')
    def __call__(self):
        config = load_config()
        folder = as_human_readable(self.pane.get_path())
        launch_vscode(binName=config["bin"],options=LaunchOptions.ReuseWindow | LaunchOptions.OpenFolder, userargs=config["additionalArgs"], args=[folder])


class OpenFolderInCodeNewWindow (DirectoryPaneCommand):
    aliases = ('Open current pane in VSCode (New Instance)', 'Open current pane in Visual Studio Code (New Instance)')
    def __call__(self):
        config = load_config()
        folder = as_human_readable(self.pane.get_path())
        launch_vscode(binName=config["bin"],options=LaunchOptions.NewWindow | LaunchOptions.OpenFolder, userargs=config["additionalArgs"], args=[folder])


class OpenFilesInCode(DirectoryPaneCommand):
    aliases = ('Open files in VSCode', 'Open files in Visual Studio Code')
    def __call__(self):
        config = load_config()
        files = self.pane.get_selected_files()
        if len(files) == 0:
            cursorfile = self.pane.get_file_under_cursor()
            if cursorfile:
                files = [cursorfile]
            else:
                show_alert("Can't open files, no file selected")
                return
        files = list(map(as_human_readable,files))
        launch_vscode(binName=config["bin"],options=LaunchOptions.ReuseWindow, userargs=config["additionalArgs"], args=files)


class OpenFilesInCodeNewWindow(DirectoryPaneCommand):
    aliases = ('Open files in VSCode (New Instance)', 'Open files in Visual Studio Code (New Instance)')
    def __call__(self):
        config = load_config()
        files = self.pane.get_selected_files()
        if len(files) == 0:
            cursorfile = self.pane.get_file_under_cursor()
            if cursorfile:
                files = [cursorfile]
            else:
                show_alert("Can't open files, no file selected")
                return
        files = list(map(as_human_readable,files))
        launch_vscode(binName=config["bin"],options=LaunchOptions.NewWindow, userargs=config["additionalArgs"], args=files)
