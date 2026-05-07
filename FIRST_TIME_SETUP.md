# First-time setup on a computer without Git

This tutorial explains how to get this signature repository onto a computer that does not have Git yet. The key idea is:

- The first time you get the repository, you **clone** it.
- Later, when the repository already exists on your computer, you **pull** updates.

## 1. Check whether Git is installed

Open a terminal:

- **Windows:** open **PowerShell**.
- **macOS:** open **Terminal**.
- **Linux:** open your terminal application.

Run:

```bash
git --version
```

If you see a version number, Git is already installed and you can skip to [step 3](#3-clone-the-repository-for-the-first-time).

If the command is not recognized, install Git in step 2.

## 2. Install Git

### Windows

1. Go to <https://git-scm.com/download/win>.
2. Download and run the installer.
3. You can keep the default installer choices.
4. Close and reopen PowerShell.
5. Confirm the installation:

```bash
git --version
```

### macOS

The simplest method is to install Apple's command line developer tools. In Terminal, run:

```bash
git --version
```

If macOS asks you to install developer tools, accept the prompt. After installation, run the command again:

```bash
git --version
```

You can also install Git from <https://git-scm.com/download/mac>.


## 3. Clone the repository for the first time

Ask the repository owner for the repository URL. It will usually look like one of these:

https://github.com/TvanGorcum/Dynamic_signature

Choose where you want to store the repository, then run `git clone`.
cd 
Example:

```bash
cd Documents
git clone https://github.com/TvanGorcum/Dynamic_signature.git
cd repository-name
```

After cloning, you now have a local copy of the repository.

## 4. Configure the signature

Open `config.ini` in a text editor and change these values:

```ini
[signature]
name = Your Name
function = Your EIRES Function
```

Also set the final signature copy location:

```ini
[paths]
copy_to_path = path/to/your/outlook/signature.html
```

On Windows, Outlook signatures are often stored in a folder like:

```ini
copy_to_path = C:\Users\YourUser\AppData\Roaming\Microsoft\Signatures\eires_signature.html
```

Replace `YourUser` with your Windows username.

## 5. Generate the personalized signature

From inside the repository folder, run:

```bash
python generate_signature.py
```

If your system uses `python3` instead of `python`, run:

```bash
python3 generate_signature.py
```

The script will:

1. Run `git pull --ff-only` to update the local template.
2. Read your name, function, and paths from `config.ini`.
3. Generate a personalized HTML signature file.
4. Copy the signature to the configured destination path.

## 6. Pull updates later

After the first clone, you do not need to clone again. To retrieve future template updates, go into the repository folder and pull:

```bash
cd path/to/repository-name
git pull --ff-only
```

Then regenerate the signature:

```bash
python generate_signature.py
```

## Troubleshooting

### `git` is not recognized

Git is not installed or your terminal was opened before Git was installed. Install Git, then close and reopen the terminal.

### `python` is not recognized

Install Python from <https://www.python.org/downloads/>. On Windows, enable **Add python.exe to PATH** during installation. Then close and reopen PowerShell.

### `git pull` says there is no tracking information

This usually means the repository was not cloned from a remote, or the local branch is not connected to a remote branch. If you cloned the repository normally, this should not happen. You can still test generation without pulling by running:

```bash
python generate_signature.py --skip-pull
```

### I downloaded a ZIP instead of cloning

A ZIP download is fine for viewing files, but it is not connected to Git. You cannot use `git pull` inside a ZIP download. Install Git and use `git clone` if you want updates through Git.
