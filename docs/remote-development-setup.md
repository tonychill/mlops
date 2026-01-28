# Remote Development Setup with VS Code

This guide explains how to set up VS Code to connect to our remote development server via SSH. This allows you to use the server's resources (CPU, GPU, memory) while working from your local machine with a native development experience.

## Why Remote Development?

Local machines may not have sufficient resources for:
- Fine-tuning ML models
- Running Docker containers
- Running the full application stack
- Processing large datasets

The remote server provides the necessary compute power while VS Code makes it feel like local development.

## Prerequisites

- VS Code installed on your local machine
- SSH client installed (included by default on macOS and Linux; Windows 10+ includes OpenSSH)
- SSH access credentials to the remote server (provided by your team lead)

## Part 1: VS Code Remote SSH Setup

### Step 1: Install the Remote SSH Extension

1. Open VS Code
2. Go to Extensions (Cmd+Shift+X on macOS, Ctrl+Shift+X on Windows/Linux)
3. Search for "Remote - SSH" by Microsoft
4. Click Install

Alternatively, install from the command line:
```bash
code --install-extension ms-vscode-remote.remote-ssh
```

### Step 2: Configure SSH Keys (Recommended)

Using SSH keys avoids entering your password repeatedly.

**Generate an SSH key pair (if you don't have one):**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Press Enter to accept the default file location (`~/.ssh/id_ed25519`).

**Copy your public key to the remote server:**
```bash
ssh-copy-id username@remote-server-address
```

Or manually append your public key to `~/.ssh/authorized_keys` on the server.

### Step 3: Configure SSH Config File

Create or edit `~/.ssh/config` on your local machine:

```
Host dev-server
    HostName remote-server-address
    User your-username
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**Configuration explained:**
- `Host dev-server` - A friendly alias you'll use to connect
- `HostName` - The actual server IP or hostname
- `User` - Your username on the remote server
- `IdentityFile` - Path to your SSH private key
- `ForwardAgent yes` - Allows using your local SSH keys on the server (for git, etc.)
- `ServerAliveInterval/CountMax` - Keeps the connection alive

### Step 4: Connect to the Remote Server

1. Open VS Code
2. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
3. Type "Remote-SSH: Connect to Host..."
4. Select your configured host (e.g., `dev-server`)
5. VS Code will open a new window connected to the remote server

**First connection:** VS Code will install its server component on the remote machine. This happens automatically and only needs to be done once.

### Step 5: Open Your Project

Once connected:
1. Click "Open Folder" in the Explorer sidebar
2. Navigate to your project directory on the remote server
3. Click OK

You can now edit files, use the integrated terminal, and run commands as if working locally.

## Part 2: SSH Tunneling for Local Application Access

SSH tunneling allows you to access services running on the remote server from your local machine. This is essential for:
- Testing web applications in your local browser
- Using Postman to test APIs
- Accessing databases with local GUI tools
- Viewing ML training dashboards (TensorBoard, MLflow, etc.)

### Method 1: VS Code Automatic Port Forwarding

VS Code automatically detects and forwards ports when services start on the remote server.

1. Start a service on the remote server (e.g., `python app.py` running on port 8000)
2. VS Code detects it and shows a notification
3. Click "Open in Browser" or access via `localhost:8000`

**View and manage forwarded ports:**
1. Open the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`)
2. Type "Forward a Port" or view the "PORTS" tab in the bottom panel

### Method 2: Manual Port Forwarding in VS Code

1. Open the "PORTS" tab in the bottom panel
2. Click "Forward a Port"
3. Enter the remote port number
4. Optionally set a local port (defaults to the same number)

### Method 3: SSH Command Line Tunneling

For tunneling without VS Code, or for persistent tunnels:

**Single port forward:**
```bash
ssh -L local_port:localhost:remote_port dev-server
```

**Example - Forward remote port 8000 to local port 8000:**
```bash
ssh -L 8000:localhost:8000 dev-server
```

**Multiple ports:**
```bash
ssh -L 8000:localhost:8000 -L 5432:localhost:5432 -L 6379:localhost:6379 dev-server
```

**Background tunnel (runs in background):**
```bash
ssh -fN -L 8000:localhost:8000 dev-server
```

### Method 4: Persistent SSH Config Tunnels

Add tunnels to your `~/.ssh/config` for automatic forwarding:

```
Host dev-server
    HostName remote-server-address
    User your-username
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
    ServerAliveInterval 60
    ServerAliveCountMax 3

    # Application server
    LocalForward 8000 localhost:8000

    # API server
    LocalForward 8080 localhost:8080

    # PostgreSQL
    LocalForward 5432 localhost:5432

    # Redis
    LocalForward 6379 localhost:6379

    # TensorBoard
    LocalForward 6006 localhost:6006

    # MLflow
    LocalForward 5000 localhost:5000

    # Jupyter
    LocalForward 8888 localhost:8888
```

Now these ports are automatically forwarded whenever you connect.

## Part 3: Common Use Cases

### Running Docker on the Remote Server

Docker commands execute on the remote server when using the VS Code terminal:

```bash
# In VS Code terminal (connected to remote)
docker build -t myapp .
docker run -p 8000:8000 myapp
```

Access the container at `localhost:8000` on your local machine (via port forwarding).

**For Docker extension support:**
1. Install the "Docker" extension in VS Code
2. It will automatically use the remote Docker daemon

### Testing APIs with Postman

1. Ensure the API server is running on the remote server (e.g., port 8000)
2. Set up port forwarding for port 8000
3. In Postman, use `http://localhost:8000` as your base URL
4. Make requests as if the API were running locally

### ML Training with TensorBoard

1. Start TensorBoard on the remote server:
   ```bash
   tensorboard --logdir=./logs --port=6006
   ```
2. Forward port 6006 (automatic in VS Code or via SSH config)
3. Open `http://localhost:6006` in your local browser

### Jupyter Notebooks

1. Start Jupyter on the remote server:
   ```bash
   jupyter notebook --no-browser --port=8888
   ```
2. Copy the token from the terminal output
3. Open `http://localhost:8888` in your local browser
4. Enter the token when prompted

**Alternative:** Use VS Code's Jupyter extension to work with notebooks directly in VS Code.

## Part 4: Optimizing the Remote Development Experience

### VS Code Settings for Remote Development

Add to your VS Code settings (`settings.json`):

```json
{
    "remote.SSH.remotePlatform": {
        "dev-server": "linux"
    },
    "remote.SSH.connectTimeout": 60,
    "remote.SSH.showLoginTerminal": true,
    "remote.SSH.defaultExtensions": [
        "ms-python.python",
        "ms-toolsai.jupyter"
    ]
}
```

### Extensions to Install on Remote

Some extensions need to be installed on the remote server. When connected:

1. Go to Extensions
2. Look for extensions marked "Install in SSH: dev-server"
3. Install language-specific extensions (Python, Docker, etc.) on the remote

### Git Configuration

Your local SSH keys can be used on the remote server with SSH agent forwarding (configured with `ForwardAgent yes`).

Verify it works:
```bash
# On the remote server
ssh -T git@github.com
```

If you see your GitHub username, agent forwarding is working.

### File Syncing Considerations

- Files are stored on the remote server, not locally
- Use Git to sync code between developers
- Large datasets should remain on the server
- Consider using Git LFS for large files that need versioning

## Part 5: Troubleshooting

### Connection Issues

**"Connection refused" or timeout:**
- Verify the server is running and accessible
- Check if SSH port (usually 22) is open
- Test with plain SSH first: `ssh dev-server`

**"Permission denied":**
- Verify your SSH key is added to the server's `authorized_keys`
- Check file permissions: `chmod 700 ~/.ssh && chmod 600 ~/.ssh/*`

**VS Code stuck connecting:**
- Check `~/.vscode-server/` on the remote for corrupted installations
- Delete and let VS Code reinstall: `rm -rf ~/.vscode-server`

### Port Forwarding Issues

**"Address already in use":**
- Another process is using that local port
- Use a different local port: `-L 8001:localhost:8000`

**Can't access forwarded service:**
- Verify the service is running on the remote: `curl localhost:PORT`
- Check the service is binding to `localhost` or `0.0.0.0`

### Performance Optimization

**Slow file browsing:**
- Exclude large directories in VS Code settings:
  ```json
  {
      "files.watcherExclude": {
          "**/venv/**": true,
          "**/.git/objects/**": true,
          "**/node_modules/**": true
      }
  }
  ```

**High latency:**
- Use wired connection when possible
- Consider working closer to the server's geographic location
- Use VS Code's "workspace trust" to reduce security scanning

## Quick Reference

### Common Commands

| Action | Command |
|--------|---------|
| Connect to server | `Cmd/Ctrl+Shift+P` -> "Remote-SSH: Connect to Host" |
| Forward a port | `Cmd/Ctrl+Shift+P` -> "Forward a Port" |
| Open terminal | `` Ctrl+` `` |
| View forwarded ports | Click "PORTS" tab in bottom panel |

### Common Ports

| Service | Default Port |
|---------|--------------|
| Web application | 8000, 8080, 3000 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| TensorBoard | 6006 |
| MLflow | 5000 |
| Jupyter | 8888 |

## Additional Resources

- [VS Code Remote SSH Documentation](https://code.visualstudio.com/docs/remote/ssh)
- [SSH Tunneling Explained](https://www.ssh.com/academy/ssh/tunneling)
- [VS Code Remote Development Tips](https://code.visualstudio.com/docs/remote/troubleshooting)
