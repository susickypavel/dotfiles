# Dotfiles

This repository is a single [chezmoi](https://www.chezmoi.io/) source of truth
for macOS, Linux, and Windows machines.

The managed home directory lives under `home/`. The `.chezmoiroot` file tells
chezmoi to use that directory as its source state, which keeps repository-only
files such as this README out of `$HOME`.

## Layout

```text
home/
  .chezmoiignore                  # platform-specific target exclusions
  .chezmoitemplates/agents/
    AGENTS.md                    # shared global instructions (initially empty)
  .chezmoitemplates/claude/
    settings.json                # shared Claude Code baseline
  dot_zsh_plugins.txt             # macOS and Linux ~/.zsh_plugins.txt
  private_dot_claude/
    empty_CLAUDE.md.tmpl          # shared instructions -> ~/.claude/CLAUDE.md
    modify_settings.json         # merges baseline into ~/.claude/settings.json
  private_dot_codex/
    empty_AGENTS.md.tmpl          # shared instructions -> ~/.codex/AGENTS.md
  private_dot_config/
    ghostty/config.tmpl           # macOS/Linux Ghostty config selector
    starship.toml                 # shared ~/.config/starship.toml
  AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/
    settings.json                # Windows-only Windows Terminal settings
  Documents/PowerShell/
    Microsoft.PowerShell_profile.ps1 # Windows-only PowerShell 7 profile
```

Chezmoi source names describe their destination paths. For example,
`private_dot_config/starship.toml` becomes `~/.config/starship.toml`.

## Platform rules

Use the simplest representation that fits each file:

- Put identical files directly under `home/`, as with `starship.toml`.
- Put files needed by only some operating systems under `home/`, then exclude
  them elsewhere in `home/.chezmoiignore`.

## Agent instructions

Edit `home/.chezmoitemplates/agents/AGENTS.md` to set shared global
instructions for Codex and Claude Code. It starts empty. Chezmoi copies its
literal contents into `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md` on
macOS, Linux, and Windows using the two include templates. On Windows,
`~` is your user profile directory.

The templates use the
[`empty_` attribute](https://www.chezmoi.io/reference/source-state-attributes/)
so chezmoi creates the destination files even while the shared source is
empty. Edit the shared source, then review and apply just these files:

```sh
chezmoi diff ~/.codex/AGENTS.md ~/.claude/CLAUDE.md
chezmoi apply ~/.codex/AGENTS.md ~/.claude/CLAUDE.md
```

These files hold standing instructions. Reusable skills are installed
separately; referencing a skill here does not install it.

## Claude Code

Edit `home/.chezmoitemplates/claude/settings.json` to change the shared
baseline. `home/private_dot_claude/modify_settings.json` uses chezmoi's
[modify template](https://www.chezmoi.io/user-guide/manage-different-types-of-file/#modify-an-existing-file)
support to merge it into `~/.claude/settings.json` on macOS and Linux, or
`%USERPROFILE%\.claude\settings.json` on Windows.

On each apply, nested objects are merged and shared values take precedence.
Keys absent from the baseline are preserved, including machine-specific
hooks and status lines. The `permissions.allow`, `ask`, `deny`, and
`additionalDirectories` lists combine local and shared entries without
duplicates; other lists use the shared value when present. A missing or
empty file starts with the baseline. Invalid JSON stops the apply.

Run `chezmoi diff` to review the merge, then `chezmoi apply`. Removing a key
or permission rule from the baseline does not remove it from an existing
local file; remove it locally too when needed. Avoid `chezmoi add` or
`chezmoi re-add` for this file, since that can replace the modifier with a
full copy containing machine-specific settings.

Project settings can override this user baseline; see the
[Claude Code settings documentation](https://code.claude.com/docs/en/settings).

## Windows Terminal

`home/AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json`
manages the settings for the stable Microsoft Store installation of
[Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/install#settings-json-file).
The `AppData` directory is excluded on macOS and Linux.

This is a full copy of the configuration, including profiles, keybindings,
fonts, and the PowerShell starting directory (`D:\repositories`). Edit it
in the repo and apply with chezmoi, or save changes made in Terminal's UI:

```powershell
chezmoi add "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
```

## Bootstrap a new machine

With chezmoi already installed:

```sh
chezmoi init --apply https://github.com/susickypavel/dotfiles.git
```

On macOS or Linux, install chezmoi and apply the repo in one command:

```sh
sh -c "$(curl -fsLS https://get.chezmoi.io)" -- init --apply susickypavel
```

On Windows, install it first and then apply the repo:

```powershell
winget install twpayne.chezmoi
chezmoi init --apply https://github.com/susickypavel/dotfiles.git
```

Use `chezmoi diff` before `chezmoi apply` when changing an existing machine.

## Use an existing checkout

Chezmoi uses its configured source directory, even when you run it from a
different Git checkout. Run `chezmoi source-path` to see the active source.
To use this checkout for one command, run these from the repository root:

```sh
chezmoi --source . diff
chezmoi --source . apply
```

To make it the default, run `chezmoi edit-config` and set `sourceDir` to the
absolute repository path. For example, in `chezmoi.toml` on Windows:

```toml
sourceDir = "D:/repositories/dotfiles"
```

Point to the repository root; `.chezmoiroot` selects the `home/` subdirectory.
This path is local to each machine and is not part of the shared dotfiles.

## Add files

Add a shared file normally:

```sh
chezmoi add ~/.config/starship.toml
```

For a file that should exist only on selected systems, add it normally and add
its target path to the appropriate branch in `home/.chezmoiignore`.

Useful daily commands:

```sh
chezmoi diff
chezmoi apply
chezmoi update
chezmoi cd
```
