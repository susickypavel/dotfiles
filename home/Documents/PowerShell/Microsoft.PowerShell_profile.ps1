# activations
(&starship init powershell) | Out-String | Invoke-Expression
(&mise activate pwsh) | Out-String | Invoke-Expression

# zsh-autosuggestions-like inline suggestions
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle InlineView

# Accept next word of suggestion, similar to fish/zsh-style partial accept
Set-PSReadLineKeyHandler -Chord "Ctrl+f" -Function ForwardWord
