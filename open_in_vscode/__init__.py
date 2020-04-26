
from os import environ, name as osname, path
from fman import DirectoryPaneCommand, show_alert, load_json, save_json
from fman.url import as_human_readable
from subprocess import Popen, SubprocessError, run, PIPE
from enum import IntFlag
from itertools import chain

CONFIG_FILE = "VSCodeLaunch.json"
ARG_NEWWND="-n"
ARG_REUSEWND="-r"

class LaunchOptions(IntFlag):
    NewWindow = 1,
    ReuseWindow = 2
    OpenFolder = 4


def launch_vscode(binPath: str, options: LaunchOptions, userargs: list, args: list):
    cmdline = []
    cmdline = list(chain(cmdline,args))
    cmdline = [str(binPath), ARG_NEWWND if LaunchOptions.NewWindow in options else ARG_REUSEWND] + userargs + cmdline
    try:
        Popen(cmdline, env=environ,
              restore_signals=True, start_new_session=True)
    except OSError as oserr:
        show_alert(f"OS Error: {oserr}")
    except ValueError as valerr:
        show_alert(f"Startup failure: {valerr}")
    except SubprocessError as procerr:
        show_alert(f"Unknown startup exception: {procerr}")


def find_code():
    if osname == "nt":
        result = run('powershell.exe -Command "Get-Command code | Select-Object -ExpandProperty Definition"', shell=True, stdout=PIPE)
        result.check_returncode()
        return str(result.stdout)
    else:
        return 'code'


def load_config() -> dict:
    config = load_json(CONFIG_FILE)
    if config is None:
        config = {
            "bin": find_code(),
            "additionalArgs": []
        }
        save_json(CONFIG_FILE, config)
    return config


class OpenFolderInCode(DirectoryPaneCommand):
    aliases = ('Open current pane in VSCode', 'Open current pane in Visual Studio Code')
    def __call__(self):
        config = load_config()

        folder =  as_human_readable(self.pane.get_path()).replace(path.sep, '/')
        launch_vscode(binPath=config["bin"],options=LaunchOptions.ReuseWindow | LaunchOptions.OpenFolder, userargs=config["additionalArgs"], args=[folder])


class OpenFolderInCodeNewWindow (DirectoryPaneCommand):
    aliases = ('Open current pane in VSCode (New Instance)', 'Open current pane in Visual Studio Code (New Instance)')
    def __call__(self):
        config = load_config()
        folder =  as_human_readable(self.pane.get_path()).replace(path.sep, '/')
        launch_vscode(binPath=config["bin"],options=LaunchOptions.NewWindow | LaunchOptions.OpenFolder, userargs=config["additionalArgs"], args=[folder])


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
        files = list(map(lambda p: p.replace(path.sep, '/'),map(as_human_readable,files)))
        launch_vscode(binPath=config["bin"],options=LaunchOptions.ReuseWindow, userargs=config["additionalArgs"], args=files)


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
        files = list(map(lambda p: p.replace(path.sep, '/'),map(as_human_readable,files)))
        launch_vscode(binPath=config["bin"],options=LaunchOptions.NewWindow, userargs=config["additionalArgs"], args=files)
