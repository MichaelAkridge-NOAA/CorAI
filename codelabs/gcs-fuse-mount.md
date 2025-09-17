# Install GCS FUSE Mount
id: gcs-fuse-mount
title: Install GCS FUSE Mount
summary: Step-by-step guide to mount Google Cloud Storage buckets as local filesystems using gcsfuse.
authors: Michael Akridge
categories: Cloud Storage, FUSE, Setup
environments: Web
status: Published
tags: gcs, fuse, cloud-storage, mount
feedback link: https://github.com/MichaelAkridge-NOAA/CorAI/issues

# Google Cloud Storage FUSE Mount Tutorial

This tutorial provides step-by-step instructions for mounting a Google Cloud Storage bucket as a local filesystem using gcsfuse.

## Overview

Google Cloud Storage FUSE (gcsfuse) allows you to mount Cloud Storage buckets as file systems on Linux or macOS systems. This enables applications to access objects in Cloud Storage through standard file system operations.

## Prerequisites

- A Google Cloud Platform account with access to the target bucket
- Linux system with sudo privileges
- Google Cloud SDK (gcloud) installed

## Installation Steps

### 1. Create Local Mount Directory

Create a directory where the bucket will be mounted(example):

```bash
mkdir -p ~/gcs/genomics
```

### 2. Authenticate with Google Cloud

Login and set up application default credentials:

```bash
gcloud auth application-default login
```

This will open a browser window for authentication. Follow the prompts to complete the login process.

### 3. Install gcsfuse

Update package manager and install required dependencies:

```bash
sudo apt-get update
sudo apt-get install -y curl lsb-release
```

Configure the gcsfuse repository:

```bash
export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.asc
```

Update package list and install gcsfuse:

```bash
sudo apt-get update
sudo apt-get install gcsfuse
```
As one step:
```bash
sudo apt-get update
sudo apt-get install -y curl lsb-release
export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.asc
sudo apt-get update
sudo apt-get install gcsfuse
```

### 4. Mount the Bucket

Mount the specific directory from the bucket to your local filesystem:

```bash
gcsfuse --only-dir PIFSC/ESD/ARP/genomics nmfs_odp_pifsc ~/gcs/genomics
```

**Command breakdown:**
- `--only-dir PIFSC/ESD/ARP/genomics`: Only mount specific directory from the bucket
- `nmfs_odp_pifsc`: The name of the Google Cloud Storage bucket
- `~/gcs/genomics`: Local/cloud machine mount point directory

## Usage

Once mounted, you can access the bucket contents through standard file operations.

## Unmounting

When you're finished working with the mounted bucket, unmount it using:

```bash
fusermount -u ~/gcs/genomics
```

## Important Notes

- **Performance**: gcsfuse provides file system semantics but may not offer the same performance as native Cloud Storage operations
- **Permissions**: Ensure your Google Cloud credentials have appropriate permissions for the target bucket
- **Network Dependency**: The mount requires an active internet connection to access Cloud Storage
- **Caching**: gcsfuse uses local caching to improve performance, but changes may not be immediately visible across different mount points

## Troubleshooting

### Common Issues

1. **Permission Denied**: Verify your Google Cloud credentials and bucket permissions
2. **Mount Point Busy**: Ensure the directory is not already mounted or in use
3. **Network Issues**: Check internet connectivity and firewall settings

## Additional Resources

- [Google Cloud Storage FUSE Documentation](https://cloud.google.com/storage/docs/gcs-fuse)
- [gcsfuse GitHub Repository](https://github.com/GoogleCloudPlatform/gcsfuse)
- [Google Cloud SDK Documentation](https://cloud.google.com/sdk/docs)


---
