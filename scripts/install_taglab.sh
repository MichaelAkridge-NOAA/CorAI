#!/bin/bash

# TagLab Installation Script for Ubuntu/Debian
# Based on the TagLab Docker container setup
# Author: Michael Akridge

set -e  # Exit on any error

echo "🚀 Starting TagLab installation..."
echo "This script will install TagLab and its dependencies on Ubuntu/Debian systems."

# Check if running on Ubuntu/Debian
if ! command -v apt-get &> /dev/null; then
    echo "❌ This script is designed for Ubuntu/Debian systems with apt-get."
    echo "Please install TagLab manually or use the Docker container."
    exit 1
fi

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root for security reasons."
   echo "Please run as a regular user with sudo privileges."
   exit 1
fi

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt-get install -y \
    curl \
    wget \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    vim \
    git \
    libgdal-dev \
    gdal-bin \
    python3-gdal \
    cmake \
    build-essential \
    pkg-config \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxkbcommon-x11-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libxss1 \
    libglib2.0-0 \
    libsm6 \
    libice6 \
    qtbase5-dev \
    qttools5-dev-tools \
    libqt5gui5 \
    libqt5core5a \
    libqt5widgets5 \
    libqt5x11extras5 \
    qt5-style-plugins \
    libqt5svg5-dev \
    qt5-qmake \
    qtchooser \
    libxcb1 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    x11-utils \
    fonts-liberation \
    fonts-dejavu-core \
    qt5-gtk-platformtheme \
    qttranslations5-l10n

echo "✅ System dependencies installed successfully!"

# Create installation directory
INSTALL_DIR="$HOME/Desktop/data_stuff"
echo "📁 Creating installation directory at $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

# Create and activate virtual environment
echo "🐍 Creating Python virtual environment..."
cd "$HOME"
python3.11 -m venv taglab-env

echo "📥 Cloning TagLab repository..."
cd "$INSTALL_DIR"
if [ -d "TagLab" ]; then
    echo "⚠️  TagLab directory already exists. Updating..."
    cd TagLab
    git pull
    cd ..
else
    git clone https://github.com/MichaelAkridge-NOAA/TagLab.git
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
source "$HOME/taglab-env/bin/activate"
pip install --upgrade pip setuptools wheel
pip install rasterio

# Install TagLab
echo "🔧 Installing TagLab..."
cd "$INSTALL_DIR/TagLab"
python3.11 install.py cpu

# Create launcher script
echo "🚀 Creating TagLab launcher script..."
cat > "$HOME/launch-taglab.sh" << 'EOF'
#!/bin/bash
# TagLab Launcher Script

# Set Qt environment variables for better compatibility
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export QT_LOGGING_RULES='*.debug=false;qt.qpa.*=false'
export QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms
export QT_QPA_FONTDIR=/usr/share/fonts
export QT_ACCESSIBILITY=0

# Ensure runtime directory exists
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/tmp/runtime-$(id -u)}
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"

# Activate virtual environment and launch TagLab
cd ~/Desktop/data_stuff/TagLab
source ~/taglab-env/bin/activate
python3.11 TagLab.py "$@"
EOF

chmod +x "$HOME/launch-taglab.sh"

# Add aliases to .bashrc for convenience
echo "⚙️  Adding convenience aliases to .bashrc..."
if ! grep -q "# TagLab Environment" "$HOME/.bashrc"; then
    cat >> "$HOME/.bashrc" << 'EOF'

# TagLab Environment
alias taglab='source ~/taglab-env/bin/activate && cd ~/Desktop/data_stuff/TagLab && python3.11 TagLab.py'
alias activate-taglab='source ~/taglab-env/bin/activate && cd ~/Desktop/data_stuff/TagLab'
EOF
fi

echo ""
echo "🎉 TagLab installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. To launch TagLab, run: ~/launch-taglab.sh"
echo "2. Or use the alias: taglab"
echo "3. To activate the TagLab environment: activate-taglab"
echo ""
echo "📂 TagLab is installed at: $INSTALL_DIR/TagLab"
echo "🐍 Virtual environment: $HOME/taglab-env"
echo ""
echo "💡 Tips:"
echo "- Restart your terminal or run 'source ~/.bashrc' to use the new aliases"
echo "- TagLab works best with a modern graphics card and up-to-date drivers"
echo "- For troubleshooting, visit: https://github.com/cnr-isti-vclab/TagLab/wiki"
echo ""
echo "✨ Happy annotating!"
