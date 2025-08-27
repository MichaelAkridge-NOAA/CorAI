# Install Meshroom
id: mesh## Installation Methods

Choose the method that best fits your system:

1. **🐧 Linux Automated Script** (Recommended)
2. **📦 Manual Installation** (Advanced users)stall
title: Install Meshroom for 3D Reconstruction
summary: Step-by-step guide to install Meshroom for photogrammetry and 3D reconstruction.
authors: Michael Akridge
categories: Meshroom, 3D Reconstruction, Photogrammetry
environments: Web
status: Published
tags: photogrammetry, 3d-reconstruction, meshroom, computer-vision
feedback link: https://github.com/MichaelAkridge-NOAA/CorAI/issues

<meta name="codelabs-base" content="/CorAI/">
# Codelab: Installing Meshroom for 3D Reconstruction

> **Goal:** Install Meshroom on your Linux system using the automated installation script for photogrammetry and 3D reconstruction workflows.

---

## About Meshroom

Meshroom is a free and open-source 3D reconstruction software developed by AliceVision. It provides a complete photogrammetry pipeline for creating 3D models from photographs.

- **GitHub Repository:** [https://github.com/alicevision/Meshroom](https://github.com/alicevision/Meshroom)
- **Official Website:** [https://alicevision.org](https://alicevision.org)
- **Documentation:** [Meshroom Documentation](https://meshroom-manual.readthedocs.io)

---

## Installation Methods

Choose the method that best fits your system:

1. **🐧 Linux Automated Script** (Recommended)
2. **� Manual Installation** (Advanced users)
3. **� Docker Container** (Development/Testing)

---

## Method 1: Linux Automated Installation Script

Our automated script installs Meshroom with all required dependencies and desktop libraries.

### Prerequisites
- Ubuntu 20.04+ or Debian-based Linux distribution
- Root/sudo privileges
- At least 4GB free disk space
- Internet connection for downloading

### Installation Steps

1. **Download the installation script:**
   ```bash
   wget https://raw.githubusercontent.com/MichaelAkridge-NOAA/CorAI/main/scripts/install_meshroom.sh
   chmod +x install_meshroom.sh
   ```

2. **Run the installation with default settings:**
   ```bash
   sudo bash install_meshroom.sh
   ```

3. **Or specify a custom version:**
   ```bash
   sudo bash install_meshroom.sh --version 2025.1.0
   ```

4. **Launch Meshroom:**
   ```bash
   meshroom
   # OR directly
   /opt/Meshroom-2025.1.0/Meshroom
   ```

### What the Script Does

> ✅ **Automated Installation Process:**
> - Updates system packages and installs required dependencies
> - Installs essential desktop libraries (Qt, OpenGL, X11 components)
> - Downloads and extracts Meshroom from official Zenodo releases
> - Creates global `meshroom` command in `/usr/local/bin`
> - Sets up proper permissions and file structure

### Script Options

```bash
# Display help
sudo bash install_meshroom.sh --help

# Install specific version
sudo bash install_meshroom.sh --version 2024.1.0

# Use custom download URL
sudo bash install_meshroom.sh --url https://custom-url/Meshroom.tar.gz
```

### Installed Dependencies

The script automatically installs these required libraries:
- `libxcb-cursor0` - X11 cursor support
- `libxcb-xinerama0` - Multi-monitor support
- `libxkbcommon-x11-0` - Keyboard handling
- `libxcb-icccm4` - Window management
- `libxcb-image0` - Image handling
- `libxcb-keysyms1` - Key symbol mapping
- `libxcb-render-util0` - Rendering utilities
- `libgl1` - OpenGL support
- `libglib2.0-0` - Core libraries
- `libdbus-1-3` - Desktop bus communication

---

## Method 2: Manual Installation

For advanced users or custom setups:

### Download from Official Sources

1. **Visit the Meshroom releases:**
   - Go to [Meshroom Releases](https://github.com/alicevision/Meshroom/releases)
   - Or download from [Zenodo](https://zenodo.org/records/16887472)

2. **Download the Linux tarball:**
   ```bash
   wget https://zenodo.org/records/16887472/files/Meshroom-2025.1.0-Linux.tar.gz
   ```

3. **Extract and install:**
   ```bash
   sudo tar -xzf Meshroom-2025.1.0-Linux.tar.gz -C /opt
   sudo ln -sf /opt/Meshroom-2025.1.0/Meshroom /usr/local/bin/meshroom
   ```

4. **Install system dependencies manually:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y \
     libxcb-cursor0 libxcb-xinerama0 libxkbcommon-x11-0 \
     libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
     libxcb-render-util0 libgl1 libglib2.0-0 libdbus-1-3
   ```

---

## Launching Meshroom

### Command Line
```bash
# Global command (after script installation)
meshroom

# Direct path
/opt/Meshroom-2025.1.0/Meshroom

# Command line tools
meshroom_batch --input /path/to/images --output /path/to/output
```

### Desktop Integration
Create a desktop entry:
```bash
cat > ~/.local/share/applications/meshroom.desktop << EOF
[Desktop Entry]
Name=Meshroom
Comment=3D Reconstruction Software
Exec=/usr/local/bin/meshroom
Icon=/opt/Meshroom-2025.1.0/meshroom/ui/img/meshroom.png
Terminal=false
Type=Application
Categories=Graphics;3DGraphics;Photography;
EOF
```

---

## First Launch & Basic Workflow

### Getting Started

1. **Launch Meshroom** and you'll see the main interface with:
   - **Images panel:** Drag and drop your photos here
   - **Graph view:** Shows the processing pipeline
   - **3D viewer:** Displays reconstruction results

2. **Import Images:**
   - Drag photos into the Images panel
   - Or use File → Add Images/Folder

3. **Start Reconstruction:**
   - Click "Start" to begin the photogrammetry process
   - Monitor progress in the Graph view

4. **View Results:**
   - Use the 3D viewer to examine your model
   - Export results from File → Export

### Basic Requirements for Photos
- **Overlap:** 60-80% overlap between consecutive photos
- **Quality:** Sharp, well-lit images
- **Format:** JPEG, PNG, TIFF supported
- **Count:** Minimum 10-20 photos for simple objects

---

## Performance Optimization

### Hardware Recommendations
- **GPU:** NVIDIA GPU with CUDA support (highly recommended)
- **RAM:** 16GB+ for large datasets
- **Storage:** SSD for faster I/O operations
- **CPU:** Multi-core processor for CPU-only processing

### CUDA Setup (Optional but Recommended)
```bash
# Install NVIDIA drivers and CUDA toolkit
sudo apt-get install nvidia-driver-535
wget https://developer.download.nvidia.com/compute/cuda/12.0.0/local_installers/cuda_12.0.0_525.60.13_linux.run
sudo bash cuda_12.0.0_525.60.13_linux.run
```

---

## Troubleshooting

### Common Issues

**1. GUI Won't Start**
```bash
# Check display environment
echo $DISPLAY
export DISPLAY=:0

# Fix Qt platform issues
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
```

**2. Missing Dependencies**
```bash
# Re-run dependency installation
sudo apt-get install -y libxcb-cursor0 libxcb-xinerama0 libxkbcommon-x11-0
```

**3. Permission Issues**
```bash
# Fix binary permissions
sudo chmod +x /opt/Meshroom-2025.1.0/Meshroom
sudo chmod +x /usr/local/bin/meshroom
```

**4. CUDA Not Detected**
```bash
# Check CUDA installation
nvidia-smi
nvcc --version

# Verify Meshroom can see GPU
meshroom --help | grep -i cuda
```

### Getting Help

- **Documentation:** [Meshroom Manual](https://meshroom-manual.readthedocs.io)
- **Community:** [AliceVision Forum](https://github.com/alicevision/meshroom/discussions)
- **Issues:** [GitHub Issues](https://github.com/alicevision/meshroom/issues)
- **CorAI Support:** [CorAI Issues](https://github.com/MichaelAkridge-NOAA/CorAI/issues)

---

## Advanced Usage

### Command Line Processing
```bash
# Batch processing
meshroom_batch \
  --input /path/to/images \
  --output /path/to/output \
  --verbose

# Custom pipeline
meshroom_batch \
  --input /path/to/images \
  --pipeline /path/to/custom.mg \
  --output /path/to/output
```

### Custom Settings
- Edit processing nodes in the Graph view
- Save custom pipelines for reuse
- Adjust quality vs. speed trade-offs
- Configure output formats and resolution

---

🎉 **You're ready to start creating 3D models with Meshroom!**

### Next Steps
- Try reconstructing your first dataset
- Explore different pipeline configurations
- Learn about advanced photogrammetry techniques
- Check out the [Meshroom tutorials](https://meshroom-manual.readthedocs.io/en/latest/tutorials/sketchfab/sketchfab.html)

