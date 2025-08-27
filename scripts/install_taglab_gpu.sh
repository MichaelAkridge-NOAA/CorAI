#!/bin/bash

# TagLab GPU Installation Script for Ubuntu/Debian with CUDA Support
# Based on the TagLab Docker container setup with GPU acceleration
# Author: Michael Akridge

set -e  # Exit on any error

echo "🚀 Starting TagLab GPU installation..."
echo "This script will install TagLab with CUDA GPU support and its dependencies on Ubuntu/Debian systems."

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

# Check for NVIDIA GPU
echo "🔍 Checking for NVIDIA GPU..."
if ! command -v nvidia-smi &> /dev/null; then
    echo "⚠️  NVIDIA drivers not detected. GPU acceleration may not work."
    echo "Please install NVIDIA drivers before running this script for optimal performance."
    echo "Continue anyway? (y/N): "
    read -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled. Please install NVIDIA drivers first."
        exit 1
    fi
else
    echo "✅ NVIDIA GPU detected:"
    nvidia-smi --query-gpu=gpu_name,driver_version,memory.total --format=csv,noheader,nounits
fi

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install CUDA and cuDNN if not present
echo "🔧 Installing CUDA toolkit and dependencies..."
if ! command -v nvcc &> /dev/null; then
    echo "Installing CUDA toolkit..."
    
    # Add NVIDIA package repositories
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu$(lsb_release -rs | tr -d .)/x86_64/cuda-keyring_1.0-1_all.deb
    sudo dpkg -i cuda-keyring_1.0-1_all.deb
    sudo apt-get update
    
    # Install CUDA toolkit
    sudo apt-get install -y cuda-toolkit-12-2 libcudnn8 libcudnn8-dev
    
    # Add CUDA to PATH
    echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
    export PATH=/usr/local/cuda/bin:$PATH
    export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
else
    echo "✅ CUDA toolkit already installed"
    nvcc --version
fi

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
python3.11 -m venv taglab-gpu-env

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

# Install Python dependencies with CUDA support
echo "📦 Installing Python dependencies with GPU support..."
source "$HOME/taglab-gpu-env/bin/activate"
pip install --upgrade pip setuptools wheel

# Install PyTorch with CUDA support
echo "🔥 Installing PyTorch with CUDA support..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install other GPU-accelerated packages
pip install rasterio
pip install opencv-python-headless
pip install cupy-cuda12x  # CuPy for CUDA acceleration

# Install TagLab with GPU support
echo "🔧 Installing TagLab with GPU acceleration..."
cd "$INSTALL_DIR/TagLab"
python3.11 install.py gpu

# Create launcher script
echo "🚀 Creating TagLab GPU launcher script..."
cat > "$HOME/launch-taglab-gpu.sh" << 'EOF'
#!/bin/bash
# TagLab GPU Launcher Script

# Set Qt environment variables for better compatibility
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export QT_LOGGING_RULES='*.debug=false;qt.qpa.*=false'
export QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms
export QT_QPA_FONTDIR=/usr/share/fonts
export QT_ACCESSIBILITY=0

# Set CUDA environment variables
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_VISIBLE_DEVICES=0  # Use first GPU by default

# Ensure runtime directory exists
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/tmp/runtime-$(id -u)}
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"

# Check GPU availability
echo "🔍 Checking GPU availability..."
python3.11 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"

# Activate virtual environment and launch TagLab
cd ~/Desktop/data_stuff/TagLab
source ~/taglab-gpu-env/bin/activate
python3.11 TagLab.py "$@"
EOF

chmod +x "$HOME/launch-taglab-gpu.sh"

# Add aliases to .bashrc for convenience
echo "⚙️  Adding convenience aliases to .bashrc..."
if ! grep -q "# TagLab GPU Environment" "$HOME/.bashrc"; then
    cat >> "$HOME/.bashrc" << 'EOF'

# TagLab GPU Environment
alias taglab-gpu='source ~/taglab-gpu-env/bin/activate && cd ~/Desktop/data_stuff/TagLab && python3.11 TagLab.py'
alias activate-taglab-gpu='source ~/taglab-gpu-env/bin/activate && cd ~/Desktop/data_stuff/TagLab'
alias taglab-gpu-test='python3.11 -c "import torch; print(f\"CUDA available: {torch.cuda.is_available()}\"); print(f\"GPU device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}\"))"'
EOF
fi

# Test GPU setup
echo ""
echo "🧪 Testing GPU setup..."
source "$HOME/taglab-gpu-env/bin/activate"
python3.11 -c "
import torch
import sys
print('=== GPU Setup Test ===')
print(f'Python version: {sys.version}')
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA version: {torch.version.cuda}')
    print(f'GPU count: {torch.cuda.device_count()}')
    for i in range(torch.cuda.device_count()):
        print(f'GPU {i}: {torch.cuda.get_device_name(i)}')
        print(f'Memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.1f} GB')
else:
    print('❌ GPU support not available')
print('======================')
"

echo ""
echo "🎉 TagLab GPU installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. To launch TagLab with GPU support, run: ~/launch-taglab-gpu.sh"
echo "2. Or use the alias: taglab-gpu"
echo "3. To activate the TagLab GPU environment: activate-taglab-gpu"
echo "4. To test GPU functionality: taglab-gpu-test"
echo ""
echo "📂 TagLab is installed at: $INSTALL_DIR/TagLab"
echo "🐍 Virtual environment: $HOME/taglab-gpu-env"
echo ""
echo "💡 Tips:"
echo "- Restart your terminal or run 'source ~/.bashrc' to use the new aliases"
echo "- GPU acceleration will be automatically used for supported operations"
echo "- Monitor GPU usage with 'nvidia-smi' while running TagLab"
echo "- For troubleshooting, visit: https://github.com/cnr-isti-vclab/TagLab/wiki"
echo ""
echo "🚀 Happy annotating with GPU acceleration!"
