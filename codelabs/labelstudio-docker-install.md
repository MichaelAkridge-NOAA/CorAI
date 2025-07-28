---
id: labelstudio-docker-install
summary: Install Label Studio with Docker
categories: docker, labelstudio, setup
status: Published
authors: Michael Akridge
feedback link: https://github.com/MichaelAkridge-NOAA/CorAI/issues
---
# Install Label Studio with Docker

- Docker and Docker Compose installed
summary: Step-by-step guide to install Label Studio using Docker Compose.
authors: Michael Akridge
categories: Docker, LabelStudio, Setup
environments: Web
status: Published
feedback link: https://github.com/MichaelAkridge-NOAA/CorAI/issues

- Basic command line knowledge

## Step 1: Clone the Repository

```bash
git clone https://github.com/MichaelAkridge-NOAA/CorAI.git
cd CorAI/docker/labelstudio
```

## Step 2: Start Label Studio

```bash
docker-compose up -d
```

## Step 3: Access Label Studio

Open your browser and go to [http://localhost:8080](http://localhost:8080)

## Step 4: Stop Label Studio

```bash
docker-compose down
```

## Next Steps
- Explore Label Studio features
- Try annotating your own data

## Resources
- [Label Studio Documentation](https://labelstud.io/guide/)
- [CorAI GitHub](https://github.com/MichaelAkridge-NOAA/CorAI)
