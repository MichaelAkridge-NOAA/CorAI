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
   - Create required folder (`./data`) with open permissions
   - Start Label Studio using Docker Compose

3. **Access Label Studio:**
   On GCP Cloud Workstation, open your browser and go to:
   `https://port-8080-<your-workstation-id>.<cluser-id>.cloudworkstations.dev/user/login/`


---

### Stopping and Restarting Label Studio

To stop Label Studio and shut down the Docker containers:
```sh
docker compose down
```

To start Label Studio again:
```sh
docker compose up
```

**Details:**
- `docker compose down` will stop and remove the running containers, but your data in `./data` will be preserved.
- `docker compose up` will start the service again, using the same persistent data.
- You can use `docker compose up -d` to run Label Studio in the background (detached mode).
- To view logs, use `docker compose logs`.
- If you need to rebuild the image after changes to the Dockerfile, use `docker compose build` before starting up.

### Manual Steps (if not using the script)
```sh
mkdir -p ./data
chmod -R 777 ./data
cd CorAI/docker/labelstudio
docker compose up
```

---

**Note:**
- Make sure Docker is installed and running on your workstation.
- The data folder is mounted for persistence.
- For custom configuration, edit the `docker-compose.yml` or `Dockerfile` as needed.
