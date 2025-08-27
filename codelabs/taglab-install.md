# Install Taglab
id: taglab-install
title: Install TagLab
summary: Step-by-step guide to install TagLab for coral annotation.
authors: Michael Akridge
categories: TagLab, Annotation, Setup
environments: Web
status: Published
tags: annotation, vital-rates
feedback link: https://github.com/MichaelAkridge-NOAA/CorAI/issues

<meta name="codelabs-base" content="/CorAI/">
# Codelab: Installing TagLab for Coral Annotation

> **Goal:** Install TagLab on your computer and launch it for the first time using multiple installation methods.

---

## Choosing Between CPU and GPU Installation

**Use CPU Installation if:**
- You don't have an NVIDIA GPU
- You're new to TagLab and want a simpler setup
- You primarily work with smaller image datasets
- You want the most stable and compatible installation

**Use GPU Installation if:**
- You have an NVIDIA GPU with CUDA support
- You work with large, high-resolution coral images
- You want to use AI-assisted annotation features
- You need faster processing for batch operations

---

## Installation Methods

Choose the method that best fits your system and preferences:

1. **🐧 Linux (Ubuntu/Debian) - Automated Script** (Recommended)
   - **CPU Version**: Standard installation for most users
   - **GPU Version**: CUDA-accelerated for enhanced performance
2. **🐳 Docker Container** (Cross-platform)
3. **📦 Manual Installation** (All platforms)

---

## Method 1: Linux Automated Installation Script

For Ubuntu/Debian systems, choose between CPU or GPU installation:

### Option 1A: CPU Installation (Recommended for most users)

#### Prerequisites
- Ubuntu 20.04+ or Debian 11+ (with apt-get)
- Regular user account with sudo privileges
- At least 2GB free disk space

#### Installation Steps

1. **Download the CPU installation script:**
   ```bash
   wget https://raw.githubusercontent.com/MichaelAkridge-NOAA/CorAI/main/scripts/install_taglab_cpu.sh
   chmod +x install_taglab_cpu.sh
   ```

2. **Run the installation:**
   ```bash
   ./install_taglab_cpu.sh
   ```

3. **Launch TagLab:**
   ```bash
   ~/launch-taglab-cpu.sh
   # OR use the alias (after restarting terminal)
   taglab-cpu
   ```

### Option 1B: GPU Installation (For CUDA-enabled systems)

#### Prerequisites
- Ubuntu 20.04+ or Debian 11+ (with apt-get)
- NVIDIA GPU with CUDA support
- NVIDIA drivers installed (recommended)
- Regular user account with sudo privileges
- At least 4GB free disk space

#### Installation Steps

1. **Download the GPU installation script:**
   ```bash
   wget https://raw.githubusercontent.com/MichaelAkridge-NOAA/CorAI/main/scripts/install_taglab_gpu.sh
   chmod +x install_taglab_gpu.sh
   ```

2. **Run the installation:**
   ```bash
   ./install_taglab_gpu.sh
   ```

3. **Launch TagLab with GPU acceleration:**
   ```bash
   ~/launch-taglab-gpu.sh
   # OR use the alias (after restarting terminal)
   taglab-gpu
   ```

4. **Test GPU functionality:**
   ```bash
   taglab-gpu-test
   ```

> ✅ **What the scripts do:**
> - **CPU Script**: Installs all system dependencies (Qt5, GDAL, Python 3.11, etc.), creates a Python virtual environment, clones and installs TagLab from source, sets up convenient launcher scripts and aliases
> - **GPU Script**: Everything in CPU script PLUS CUDA toolkit installation, PyTorch with CUDA support, GPU-optimized libraries, and GPU availability testing

---

## Method 2: Docker Container

Perfect for development environments or if you want an isolated installation:

### Prerequisites
- Docker installed on your system
- Chrome Remote Desktop account (Google account)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MichaelAkridge-NOAA/CorAI.git
   cd CorAI/codelabs/taglab
   ```

2. **Build and run the container:**
   ```bash
   docker-compose up --build
   ```

3. **Set up Chrome Remote Desktop:**
   - Execute the setup script in the container:
     ```bash
     docker exec -it crd-desktop /start-crd.sh
     ```
   - Follow the prompts to connect your Google account
   - Access via [https://remotedesktop.google.com/access](https://remotedesktop.google.com/access)

> 🌐 **Docker Benefits:**
> - Complete desktop environment with TagLab pre-installed
> - Accessible from any device via web browser
> - No local installation required
> - Persistent data storage via Docker volumes

---

## Method 3: Manual Installation

For other operating systems or custom setups:

### Visit the TagLab Repository
- Open the [TagLab GitHub page](https://github.com/cnr-isti-vclab/TagLab) in your browser
- Review the README for platform-specific requirements

### Download Options

**Option A: Source Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/cnr-isti-vclab/TagLab.git
   cd TagLab
   ```
2. Follow the installation guide in the repository README

**Option B: Pre-built Releases**
1. Visit the [TagLab Releases page](https://github.com/cnr-isti-vclab/TagLab/releases)
2. Download the appropriate version for your operating system
3. Follow platform-specific installation instructions

### Platform-Specific Instructions

- **Windows:** Download the `.exe` installer and follow the setup wizard
- **macOS:** Download the `.dmg` file and drag to Applications folder
- **Linux:** Use the automated script (Method 1) or build from source

---

## Launching TagLab

### Linux (Script Installation)

**CPU Version:**
```bash
~/launch-taglab-cpu.sh
# OR
taglab-cpu  # (alias, restart terminal first)
```

**GPU Version:**
```bash
~/launch-taglab-gpu.sh
# OR
taglab-gpu  # (alias, restart terminal first)
```

### Docker Container
- Connect via Chrome Remote Desktop at [remotedesktop.google.com/access](https://remotedesktop.google.com/access)
- TagLab will auto-launch when you connect

### Manual Installation
- **Windows/macOS:** Launch from applications menu
- **Linux:** Run from terminal or create desktop shortcut

---

## First Launch & Configuration

When you first launch TagLab:

1. **Welcome Screen:** You may see a welcome dialog or project selection screen
2. **Create New Project:** Click "File" → "New Project" to start annotating
3. **Import Images:** Use "File" → "Import Images" to load your coral images
4. **Configure Tools:** Explore the annotation tools and settings

> 🖥️ **Performance Tips:**
> - **CPU Version**: Works well for standard annotation tasks and smaller datasets
> - **GPU Version**: Provides accelerated processing for AI-assisted features and large datasets
> - TagLab works best with a modern graphics card and up-to-date drivers
> - For large images, ensure you have sufficient RAM (8GB+ recommended)
> - Use SSD storage for better performance with large datasets

> 🚀 **GPU Benefits:**
> - Faster AI model inference for automated segmentation
> - Accelerated image processing operations
> - Better performance with large, high-resolution coral images
> - Enhanced real-time preview capabilities

---

## Troubleshooting & Support

### Common Issues

**Linux: Qt/Display Issues**
```bash
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
```

**GPU Installation: CUDA Not Found**
- Ensure NVIDIA drivers are installed: `nvidia-smi`
- Verify CUDA installation: `nvcc --version`
- Check PyTorch CUDA: `python3.11 -c "import torch; print(torch.cuda.is_available())"`
- Use GPU test alias: `taglab-gpu-test`

**GPU Performance: Not Using GPU**
- Check GPU memory usage: `nvidia-smi`
- Verify CUDA environment variables are set
- Restart terminal after installation to load new environment

**Docker: Can't Connect to Remote Desktop**
- Ensure you completed the `/start-crd.sh` setup process
- Check that port 8080 is accessible
- Verify your Google account has Chrome Remote Desktop enabled

**General: Installation Errors**
- Check system requirements in the [TagLab Wiki](https://github.com/cnr-isti-vclab/TagLab/wiki)
- Ensure all dependencies are installed
- Try running with verbose output for debugging

### Getting Help

- **Documentation:** [TagLab Wiki](https://github.com/cnr-isti-vclab/TagLab/wiki)
- **Issues:** [TagLab GitHub Issues](https://github.com/cnr-isti-vclab/TagLab/issues)
- **CorAI Support:** [CorAI Issues](https://github.com/MichaelAkridge-NOAA/CorAI/issues)

---

🎉 **You're ready to start annotating coral images with TagLab!**

### Next Steps
- Load your first coral image dataset
- Explore the annotation tools and workflows
- Check out the [TagLab documentation](https://github.com/cnr-isti-vclab/TagLab#installing-taglab) for advanced features
