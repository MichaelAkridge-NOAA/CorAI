#!/usr/bin/env bash
# install_meshroom.sh
# Meshroom installer (default 2025.1.0) with desktop libs and a /usr/local/bin/meshroom launcher
# Examples:
#   sudo bash install_meshroom.sh
#   sudo bash install_meshroom.sh --version 2025.1.0

set -Eeuo pipefail

# -------- Defaults / Config --------
MESHROOM_VERSION="2025.1.0"
MESHROOM_URL="https://zenodo.org/records/16887472/files/Meshroom-${MESHROOM_VERSION}-Linux.tar.gz"
MESHROOM_DIR="/opt/Meshroom-${MESHROOM_VERSION}"
MESHROOM_BIN_LINK="/usr/local/bin/meshroom"

log()  { printf "\n\033[1;36m[MSHRM]\033[0m %s\n" "$*"; }
warn() { printf "\n\033[1;33m[WARN]\033[0m %s\n" "$*"; }
err()  { printf "\n\033[1;31m[ERROR]\033[0m %s\n" "$*"; }
need_root() { [[ $EUID -eq 0 ]] || { err "Run as root: sudo bash $0 ..."; exit 1; } }

# -------- CLI --------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --version) MESHROOM_VERSION="${2:?--version requires a value}"; shift 2 ;;
    --url)     MESHROOM_URL="${2:?--url requires a value}"; shift 2 ;;
    -h|--help)
      cat <<EOF
Usage: sudo bash $0 [options]
  --version <v>  Meshroom version (default: ${MESHROOM_VERSION})
  --url <url>    Override tarball URL (default: ${MESHROOM_URL})

Installs to /opt/Meshroom-<version> and creates /usr/local/bin/meshroom.
EOF
      exit 0 ;;
    *) err "Unknown option: $1"; exit 1 ;;
  esac
done

# Recompute DIR if user overrode version after defaults
MESHROOM_DIR="/opt/Meshroom-${MESHROOM_VERSION}"
need_root
export DEBIAN_FRONTEND=noninteractive
APT_GET="apt-get -y -o Dpkg::Options::=--force-confnew"

log "Updating APT and installing required desktop libraries..."
$APT_GET update
$APT_GET install \
  curl ca-certificates \
  libxcb-cursor0 \
  libxcb-xinerama0 \
  libxkbcommon-x11-0 \
  libxcb-icccm4 \
  libxcb-image0 \
  libxcb-keysyms1 \
  libxcb-render-util0 \
  libgl1 \
  libglib2.0-0 \
  libdbus-1-3

log "Installing Meshroom ${MESHROOM_VERSION} to ${MESHROOM_DIR}..."
mkdir -p /opt
curl -fL "$MESHROOM_URL" | tar -xz -C /opt

# Ensure expected path exists; try to detect if archive named folder differently
if [[ ! -d "$MESHROOM_DIR" ]]; then
  DETECTED_DIR=$(tar -tzf <(curl -fsL "$MESHROOM_URL") 2>/dev/null | head -n1 | cut -d/ -f1)
  if [[ -n "${DETECTED_DIR:-}" && -d "/opt/$DETECTED_DIR" ]]; then
    log "Detected Meshroom dir: /opt/$DETECTED_DIR (linking to $MESHROOM_DIR)"
    ln -snf "/opt/$DETECTED_DIR" "$MESHROOM_DIR"
  else
    warn "Could not confirm Meshroom directory; listing /opt for reference:"
    ls -la /opt | sed 's/^/[opt] /'
  fi
fi

# Create global launcher if possible
if [[ -f "$MESHROOM_DIR/Meshroom" ]]; then
  chmod +x "$MESHROOM_DIR/Meshroom" || true
  log "Creating global 'meshroom' command -> $MESHROOM_DIR/Meshroom"
  ln -sf "$MESHROOM_DIR/Meshroom" "$MESHROOM_BIN_LINK"
else
  warn "Expected '$MESHROOM_DIR/Meshroom' not found. Searching for a 'Meshroom' binary under /opt..."
  TARGET="$(find /opt -maxdepth 3 -type f -iname 'Meshroom' | head -n1 || true)"
  if [[ -n "$TARGET" ]]; then
    log "Linking fallback '$TARGET' -> $MESHROOM_BIN_LINK"
    ln -sf "$TARGET" "$MESHROOM_BIN_LINK"
    chmod +x "$TARGET" || true
  else
    warn "No 'Meshroom' binary found; CLI tools (e.g., meshroom_batch) may still be available in $MESHROOM_DIR."
  fi
fi

log "Meshroom install complete."
echo -e "\nTry:"
echo "  meshroom"
echo "  $MESHROOM_DIR/Meshroom"
