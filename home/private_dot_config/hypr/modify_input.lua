{{- /* chezmoi:modify-template */ -}}
{{- $current := .chezmoi.stdin -}}
{{- $load := `require("hypr.mouse")` -}}
{{- $loaded := regexMatch `(?m)^[\t ]*require\(["']hypr\.mouse["']\)[\t ]*;?[\t ]*(--[^\r\n]*)?\r?$` $current -}}
{{- if $loaded -}}
  {{- $current -}}
{{- else -}}
  {{- if $current -}}
    {{- $current | trimSuffix "\n" -}}
    {{- "\n\n" -}}
  {{- end -}}
  {{- $load -}}
  {{- "\n" -}}
{{- end -}}
