# Google Cloud Workstations How To
id: chrome-remote-desktop-startup
title: Connecting to Google Cloud Remote Desktop
summary: Step-by-step guide to connect to cloud workstations with pre-installed Chrome Remote Desktop.
authors: Michael Akridge
categories: Cloud, Remote Desktop, Connection
environments: Web
status: Published
tags: cloud, remote-desktop, workstations, connection
feedback link: https://github.com/MichaelAkridge-NOAA/CorAI/issues

<meta name="codelabs-base" content="/CorAI/">
# Codelab: Connecting to Google Cloud Workstations Remote Desktop

> **Goal:** Connect to a cloud workstation machine with pre-installed Chrome Remote Desktop.

> **Prerequisites:** Your cloud workstation already has Chrome Remote Desktop installed and configured.

---

## Step 1: Set Up Remote Access Authorization

1. Open your web browser on your **local machine** (not the cloud workstation)
2. Navigate to [https://remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)
3. Sign in with your Google account if prompted
4. Click on "Set up via SSH" to get the authorization script

You'll receive a Debian Linux setup script that looks similar to this:
```bash
DISPLAY= /opt/google/chrome-remote-desktop/start-host --code="4/0AY0e-g7..." --redirect-url="https://remotedesktop.google.com/_/oauthredirect" --name=$(hostname)
```

> 💡 **Important:** Copy this entire command - you'll need it for the next step.

---

## Step 2: Execute Authorization Script on Cloud Workstation

1. **SSH into your cloud workstation** or use the existing terminal connection
2. **Paste and execute** the authorization script you copied from Step 7
3. The command will authorize your cloud workstation for remote access

Example execution:
```bash
# Paste your specific authorization script here
DISPLAY= /opt/google/chrome-remote-desktop/start-host --code="your-code-here" --redirect-url="https://remotedesktop.google.com/_/oauthredirect" --name=$(hostname)
```

---

## Step 3: Verify Chrome Remote Desktop Service

Ensure the Chrome Remote Desktop service is running:

```bash
sudo service chrome-remote-desktop status
```

If it's not running, start it:
```bash
sudo service chrome-remote-desktop start
```

---

## Step 4: Connect from Your Local Machine

1. **On your local machine**, go back to [https://remotedesktop.google.com/access](https://remotedesktop.google.com/access)
2. You should see your cloud workstation listed under "Remote devices"
3. Click on your workstation name to initiate the connection
4. Enter the PIN you set during authorization (if prompted)

---

## Step 5: Test Your Connection

Once connected, you should see the XFCE desktop environment. Test your setup by:

- **Opening the file manager** to explore the system
- **Launching Google Chrome** from the applications menu
- **Testing network connectivity** by browsing to a website
- **Checking available applications** in the menu

---

## Troubleshooting

If you encounter issues:

**Connection Problems:**
- Verify the Chrome Remote Desktop service is running: `sudo service chrome-remote-desktop status`
- Check firewall settings if connections fail
- Ensure you're signed into the same Google account on both machines

**Performance Issues:**
- Adjust display quality in the remote desktop settings
- Close unnecessary applications on the cloud workstation
- Check network connectivity between your local machine and cloud

**Authorization Issues:**
- Re-run the authorization script from Step 8
- Verify you have the correct permissions on the cloud workstation

---

🎉 **You're ready to use your Google Cloud Workstation with remote desktop access!**
