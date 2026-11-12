# Preview hook for .github/scripts/render-previews.sh: micro runs in a headless
# tmux pane with each color scheme and opens this port's own generator, so the
# syntax colors, line numbers, cursor line and statusline show.
# Requires: micro, tmux.
# shellcheck shell=bash
name=micro

setup() {
  mkdir -p "$work/micro/colorschemes"
  cp "$root"/themes/*.micro "$work/micro/colorschemes/"
}

cleanup() {
  tmux -L kanagawa-preview kill-server 2>/dev/null || true
}

capture() {
  cleanup
  printf '{"colorscheme": "kanagawa-%s", "colorcolumn": 80}\n' "$1" >"$work/micro/settings.json"
  sleep 0.5
  tmux -L kanagawa-preview new-session -d -s s -x 100 -y 30 -c "$root" \
    -e COLORTERM=truecolor -e TERM=xterm-256color -e LC_ALL=C.UTF-8 \
    "micro -config-dir $work/micro +20 scripts/generate.py"
  sleep 1.5
  tmux -L kanagawa-preview capture-pane -p -e -t s >"$2"
}
