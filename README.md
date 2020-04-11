# Open in VSCode

**Open in VSCode** is a [fman](https://fman.io) Plugin that allows you to:

- Switch Visual Studio Code to the directory of the currently selected fman pane
  - Command: `Open current pane in VSCode`
- Open a new instance of Visual Studio Code to the selected fman pane
  - Command: `Open current pane in VSCode (New Instance)`
- Open all selected files in Visual Studio Code without switching your active VSCode folder
  - Command: `Open files in VSCode`
- Open all selected files in a new Visual Studio Code window
  - Command: `Open files in VSCode (New Instance)`

This plugins provides example Key Bindings that you can change. The default key bindings are:

```json
[
    {
        "keys": [
            "Ctrl+G"
        ],
        "command": "open_folder_in_code"
    },
    {
        "keys": [
            "Ctrl+Alt+G"
        ],
        "command": "open_folder_in_code_new_window"
    },
    {
        "keys": [
            "Ctrl+E"
        ],
        "command": "open_files_in_code"
    },
    {
        "keys": [
            "   Ctrl+Alt+E"
        ],
        "command": "open_files_in_code_new_window"
    }
]
```

## How to install

Open fman and press `CTRL+P` and goto `Install plugin`.

From the List select `Open files in VSCode` and press Enter.

For more Information on how to install plugins see [here](https://fman.io/docs/installing-plugins)
