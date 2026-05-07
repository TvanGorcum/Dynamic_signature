# Dynamic Outlook Signature

This repository generates a personalized Outlook HTML signature from a shared HTML template and a local configuration file.

## Files

- `templates/signature_template.html` contains the shared EIRES Outlook signature template. The person's name and function are represented by `{{NAME}}` and `{{FUNCTION}}` placeholders.
- `config.ini` contains the editable personalization and deployment settings.
- `generate_signature.py` runs the workflow: update the local template with `git pull --ff-only`, generate a personalized HTML signature, and copy it to the configured destination path.

## First-time setup

If this is the first time using the repository on a computer that does not have Git installed yet, follow the step-by-step tutorial in [`FIRST_TIME_SETUP.md`](FIRST_TIME_SETUP.md). The first download uses `git clone`; later updates use `git pull --ff-only`.

## Configure your signature

Edit the `[signature]` section in `config.ini`:

```ini
[signature]
name = Your Name
function = Your EIRES Function
```

Then choose where the final signature should be copied by editing `copy_to_path` in the `[paths]` section. Relative paths are resolved from the repository root, and absolute paths are supported.

For Outlook on Windows, the destination is commonly similar to:

```ini
copy_to_path = C:\Users\YourUser\AppData\Roaming\Microsoft\Signatures\eires_signature.html
```

## Generate and copy the signature

Run:

```bash
python generate_signature.py
```

The script performs this workflow:

1. Runs `git pull --ff-only` to retrieve the latest repository content and update the HTML template locally.
2. Reads `config.ini` and `templates/signature_template.html`.
3. Writes the personalized signature to `generated_output_path`.
4. Copies the generated HTML file to `copy_to_path`.

If the current branch has no upstream remote configured, the default config allows the pull step to warn and continue so local generation still works. Set `allow_git_pull_failure = false` if generation must stop whenever the pull step fails.

For local testing without attempting a pull, run:

```bash
python generate_signature.py --skip-pull
```
