# Dynamic Outlook Signature

This repository provides a Windows executable that generates a personalized Outlook HTML signature from the shared EIRES HTML template and your local `config.ini` settings.

## What is included

- `generate_signature.exe` is the normal app to run. It updates the local repository, renders the signature, and copies it to your configured Outlook signature location.
- `config.ini` stores your personal name, function, output paths, and workflow options.
- `templates/signature_template.html` is the shared EIRES Outlook signature template. The executable replaces the `{{NAME}}` and `{{FUNCTION}}` placeholders with your configured values.
- `generate_signature.py` is the Python source used to build the executable. End users should run the `.exe`, not the Python file.
- `FIRST_TIME_SETUP.md` contains a step-by-step setup guide for a new computer.

## First-time setup

If this is the first time using the signature generator on a computer, follow [`FIRST_TIME_SETUP.md`](FIRST_TIME_SETUP.md).

In short:

1. Install Git if it is not already installed.
2. Clone this repository.
3. Edit `config.ini` with your name, function, and Outlook signature destination.
4. Run `generate_signature.exe` from the repository folder.

The first download uses `git clone`. Later updates are handled by the executable through `git pull --ff-only`.

## Configure your signature

Edit the `[signature]` section in `config.ini`:

```ini
[signature]
name = Your Name
function = Your EIRES Function
```

Then choose where the final signature should be copied by editing `copy_to_path` in the `[paths]` section. Relative paths are resolved from the repository folder, and absolute paths are supported.

For Outlook on Windows, the destination is commonly similar to:

```ini
copy_to_path = C:\Users\YourUser\AppData\Roaming\Microsoft\Signatures\eires_signature.html
```

Replace `YourUser` with your Windows username.

## Generate and copy the signature

From the repository folder, run:

```powershell
.\generate_signature.exe
```

You can also double-click `generate_signature.exe` in File Explorer, but running it from PowerShell is recommended because you can see any success or error messages.

The executable performs this workflow:

1. Updates the local repository with `git pull --ff-only` so the shared template and executable are current.
2. Reads `config.ini` and `templates/signature_template.html`.
3. Replaces the name and function placeholders with your configured values.
4. Writes the personalized signature to `generated_output_path`.
5. Copies the generated HTML file to `copy_to_path`.

By default, the configuration allows generation to continue if the configurable pull step cannot complete, which keeps local/offline use possible. Set `allow_git_pull_failure = false` in `config.ini` if generation must stop whenever that pull step fails.

For local testing without the configurable pull step, run:

```powershell
.\generate_signature.exe --skip-pull
```

## Updating later

After the repository has been cloned once, you normally only need to run:

```powershell
.\generate_signature.exe
```

The executable checks for repository updates before generating the signature. If you prefer to update manually first, run:

```powershell
git pull --ff-only
.\generate_signature.exe
```

## Troubleshooting

### Windows blocks the executable

If Windows SmartScreen or your browser warns about the downloaded executable, choose the option to keep or run it only if you trust this repository and expected to download it.

### `git` is not recognized

Git is not installed, or PowerShell was opened before Git was installed. Install Git, then close and reopen PowerShell.

### The signature did not appear in Outlook

Confirm that `copy_to_path` points to your Outlook signatures folder and ends in `.html`. After generating, restart Outlook or open Outlook's signature settings to select the generated signature.

### I downloaded a ZIP instead of cloning

A ZIP download is fine for viewing files, but it is not connected to Git. The update step requires a real Git clone. Install Git and use `git clone` if you want automatic updates.
