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
  .chezmoitemplates/zshrc/
    darwin                        # macOS ~/.zshrc contents
    linux                         # Linux ~/.zshrc contents
  dot_zshrc.tmpl                  # selects the correct zshrc template by OS
  dot_zsh_plugins.txt             # macOS and Linux ~/.zsh_plugins.txt
  private_dot_config/
    ghostty/config                # macOS-only Ghostty config
    starship.toml                 # shared ~/.config/starship.toml
  Documents/PowerShell/
    Microsoft.PowerShell_profile.ps1 # Windows-only PowerShell 7 profile
```

Chezmoi source names describe their destination paths. For example,
`dot_zshrc.tmpl` becomes `~/.zshrc`, and
`private_dot_config/starship.toml` becomes `~/.config/starship.toml`.

## Platform rules

Use the simplest representation that fits each file:

- Put identical files directly under `home/`, as with `starship.toml`.
- Put files needed by only some operating systems under `home/`, then exclude
  them elsewhere in `home/.chezmoiignore`.
- For a path that exists on multiple systems but has different contents, use
  one `.tmpl` target file and select an OS-specific file from
  `home/.chezmoitemplates/`, as with `.zshrc`.

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

## Add files

Add a shared file normally:

```sh
chezmoi add ~/.config/starship.toml
```

For a file that should exist only on selected systems, add it normally and add
its target path to the appropriate branch in `home/.chezmoiignore`.

For a path whose full contents differ per OS, add or update the corresponding
file in `home/.chezmoitemplates/` and keep the small selector template under
`home/`.

Useful daily commands:

```sh
chezmoi diff
chezmoi apply
chezmoi update
chezmoi cd
```
