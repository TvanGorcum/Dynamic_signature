# First-time setup on a computer without Git

This guide explains how to set up the Dynamic Outlook Signature generator on a new computer. The normal workflow is:

- Clone the repository once with Git.
- Edit `config.ini` with your personal details.
- Run `generate_signature.exe` whenever you need to generate or refresh the Outlook signature.

You do **not** need to install Python for normal use. The included Windows executable is the supported way to run the generator.

## 1. Check whether Git is installed

Open **PowerShell** on Windows and run:

```powershell
git --version
```

If you see a version number, Git is already installed and you can skip to [step 3](#3-clone-the-repository-for-the-first-time).

If the command is not recognized, install Git in step 2.

## 2. Install Git

1. Go to <https://git-scm.com/download/win>.
2. Download and run the installer.
3. Keep the default installer choices unless your organization recommends different settings.
4. Close and reopen PowerShell.
5. Confirm the installation:

```powershell
git --version
```

## 3. Clone the repository for the first time

Ask the repository owner for the repository URL. It will usually be:

```text
https://github.com/TvanGorcum/Dynamic_signature.git
```

Choose where you want to store the repository, then clone it. For example:

```powershell
cd $HOME\Documents
git clone https://github.com/TvanGorcum/Dynamic_signature.git
cd Dynamic_signature
```

After cloning, you now have a local copy of the repository.

## 4. Configure the signature

Open `config.ini` in a text editor and change these values:

```ini
[signature]
name = Your Name
function = Your EIRES Function
```

Also set the final Outlook signature copy location:

```ini
[paths]
copy_to_path = C:\Users\YourUser\AppData\Roaming\Microsoft\Signatures\eires_signature.html
```

Replace `YourUser` with your Windows username. You may also choose a different file name, but keep the `.html` extension.

The default generated file is also written inside the repository at `output/personalized_signature.html`, which can be useful for checking the result before Outlook uses it.

## 5. Generate the personalized signature

From inside the repository folder, run:

```powershell
.\generate_signature.exe
```

Running from PowerShell is recommended because you can read the success or error messages. The executable will:

1. Update the local repository with `git pull --ff-only` so the latest shared template and executable are available.
2. Read your name, function, and paths from `config.ini`.
3. Generate a personalized HTML signature file.
4. Copy the signature to the configured Outlook destination path.

You can now open Outlook's signature settings and select the generated signature if Outlook does not select it automatically.

## 6. Refresh the signature later

After the first clone, you do not need to clone again. To retrieve future template updates and regenerate the signature, go into the repository folder and run the executable again:

```powershell
cd $HOME\Documents\Dynamic_signature
.\generate_signature.exe
```

If you want to update manually before generating, run:

```powershell
git pull --ff-only
.\generate_signature.exe
```

## Optional command-line flags

For local testing without the configurable pull step, run:

```powershell
.\generate_signature.exe --skip-pull
```

To use a different config file, run:

```powershell
.\generate_signature.exe --config path\to\config.ini
```

Most users do not need these options.

## Troubleshooting

### Windows blocks the executable

Windows SmartScreen or your browser may warn about downloaded executables. Only keep or run the file if you trust this repository and expected to download it.

### `git` is not recognized

Git is not installed, or PowerShell was opened before Git was installed. Install Git, then close and reopen PowerShell.

### `generate_signature.exe` is not recognized

Make sure you are inside the repository folder and include `./` or `.\` before the executable name:

```powershell
.\generate_signature.exe
```

### `git pull` says there is no tracking information

This usually means the repository was not cloned from a remote, or the local branch is not connected to a remote branch. If you cloned the repository normally, this should not happen. Re-clone the repository with Git if needed.

### I downloaded a ZIP instead of cloning

A ZIP download is fine for viewing files, but it is not connected to Git. The update step requires a real Git clone. Install Git and use `git clone` if you want automatic updates.

### The signature did not appear in Outlook

Confirm that `copy_to_path` points to your Outlook signatures folder and ends in `.html`. After generating, restart Outlook or open Outlook's signature settings to select the generated signature.
