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

## Installation Methods

Choose the method that best fits your system and preferences:

1. **🐧 Linux (Ubuntu/Debian) - Automated Script** (Recommended)
2. **🐳 Docker Container** (Cross-platform)
3. **📦 Manual Installation** (All platforms)

---

## Method 1: Linux Automated Installation Script

For Ubuntu/Debian systems, use our automated installation script:

### Prerequisites
- Ubuntu 20.04+ or Debian 11+ (with apt-get)
- Regular user account with sudo privileges
- At least 2GB free disk space

### Installation Steps

1. **Download the installation script:**
   ```bash
   wget https://raw.githubusercontent.com/MichaelAkridge-NOAA/CorAI/main/scripts/install_taglab.sh
   chmod +x install_taglab.sh
   ```

2. **Run the installation:**
   ```bash
   ./install_taglab.sh
   ```

3. **Launch TagLab:**
   ```bash
   ~/launch-taglab.sh
   # OR use the alias (after restarting terminal)
   taglab
   ```

> ✅ **What the script does:**
> - Installs all system dependencies (Qt5, GDAL, Python 3.11, etc.)
> - Creates a Python virtual environment
> - Clones and installs TagLab from source
> - Sets up convenient launcher scripts and aliases

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
```bash
~/launch-taglab.sh
# OR
taglab  # (alias, restart terminal first)
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
> - TagLab works best with a modern graphics card and up-to-date drivers
> - For large images, ensure you have sufficient RAM (8GB+ recommended)
> - Use SSD storage for better performance with large datasets

---

## Troubleshooting & Support

### Common Issues

**Linux: Qt/Display Issues**
```bash
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
```

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
