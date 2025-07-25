# Label Studio Docker Setup

This folder contains everything needed to run Label Studio in Docker, including a custom Dockerfile and a docker-compose configuration.

## Quick Start (GCP Cloud Workstation or Linux)

1. **Clone the repository:**
   ```sh
   git clone https://github.com/MichaelAkridge-NOAA/CorAI.git
   cd CorAI/docker/labelstudio
   ```

2. **Run the setup script:**
   ```sh
   bash start_labelstudio.sh
   ```
   This will:
   - Create required folders (`~/labelstudio/data`, `~/docker`) with open permissions
   - Start Label Studio using Docker Compose

3. **Access Label Studio:**
   Open your browser and go to `http://<your-workstation-ip>:8080`

---

### Manual Steps (if not using the script)
```sh
mkdir -p ~/labelstudio/data
chmod -R 777 ~/labelstudio/data
mkdir -p ~/docker
chmod -R 777 ~/docker
cd CorAI/docker/labelstudio
docker compose up
```

---

**Note:**
- Make sure Docker is installed and running on your workstation.
- The data folder is mounted for persistence.
- For custom configuration, edit the `docker-compose.yml` or `Dockerfile` as needed.
