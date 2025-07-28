id: labelstudio-docker-install
title: Install Label Studio with Docker
summary: Step-by-step guide to install Label Studio using Docker Compose.
authors: Michael Akridge
categories: Docker, LabelStudio, Setup
environments: Web
status: Published
tags: annotation, object-detection
feedback link: https://github.com/MichaelAkridge-NOAA/CorAI/issues

<meta name="codelabs-base" content="/CorAI/">

# Install Label Studio with Docker

## Introduction

This codelab will walk you through installing Label Studio using Docker Compose in your workspace.

## Prerequisites
- Docker and Docker Compose installed
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
