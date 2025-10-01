# Cyberspike Integration Setup Guide

## Overview

Villager AI includes integration with Cyberspike's custom Kali Docker image, which provides pre-configured security tools and optimized performance. However, the system includes robust fallback mechanisms to ensure functionality even when Cyberspike registry is inaccessible.

## Current Status

### ✅ What's Working
- **Fallback System**: Automatically uses standard Kali image when Cyberspike is unavailable
- **Tool Installation**: All security tools (nmap, msfvenom, gobuster, etc.) are automatically installed
- **SSH Access**: Secure SSH-based command execution
- **24-hour Persistence**: Containers persist for 24 hours with automatic cleanup
- **Full Functionality**: All Villager features work with standard Kali image

### ⚠️ Cyberspike Registry Access
The Cyberspike registry (`gitlab.cyberspike.top:5050`) may not be accessible due to:
- Network restrictions
- Authentication requirements
- Registry availability

## Setup Options

### Option 1: Use Standard Kali (Recommended for Most Users)
The system automatically falls back to the standard Kali image, which provides:
- All essential security tools
- Automatic tool installation
- Full Villager functionality
- No additional setup required

### Option 2: Configure Cyberspike Access (Advanced Users)

If you have access to the Cyberspike registry, you can configure it:

1. **Network Access**: Ensure your network can reach `gitlab.cyberspike.top:5050`
2. **Authentication**: You may need to configure Docker authentication
3. **Registry Configuration**: Add registry credentials if required

#### Docker Login (if authentication is required)
```bash
docker login gitlab.cyberspike.top:5050
```

#### Test Cyberspike Access
```bash
docker pull gitlab.cyberspike.top:5050/aszl/diamond-shovel/al-1s/kali-image:main
```

## Verification

### Test Current Setup
```bash
# Test Kali Driver functionality
curl -X POST http://localhost:1611/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Run nmap --version and msfvenom --help"}'

# Check container status
docker ps | grep kali

# Test SSH access
sshpass -p password ssh -o StrictHostKeyChecking=no -p 22000 root@localhost "whoami"
```

### Expected Results
- ✅ Container creation successful
- ✅ SSH access working
- ✅ Security tools available (nmap, msfvenom, gobuster, nikto, sqlmap, hydra, john, hashcat)
- ✅ Commands execute successfully

## Troubleshooting

### Common Issues

#### 1. Cyberspike Registry Timeout
**Error**: `net/http: request canceled while waiting for connection`
**Solution**: This is expected - the system will automatically use standard Kali image

#### 2. SSH Connection Issues
**Error**: `Connection reset by peer`
**Solution**: Wait for package installation to complete (usually 1-2 minutes after container creation)

#### 3. Container Creation Fails
**Error**: Docker daemon issues
**Solution**: Ensure Docker is running and accessible

### Debug Commands
```bash
# Check Docker status
docker info

# Check container logs
docker logs <container_id>

# Check Villager logs
tail -f logs/kali_driver.log

# Test network connectivity
ping gitlab.cyberspike.top
```

## For Developers/Contributors

### Adding Cyberspike Support
If you want to add better Cyberspike support:

1. **Registry Configuration**: Add authentication handling
2. **Network Detection**: Implement network connectivity checks
3. **Fallback Logic**: Ensure robust fallback mechanisms
4. **Documentation**: Update setup guides with specific requirements

### Testing
```bash
# Test with Cyberspike image
export FORCE_CYBERSPIKE=true
./scripts/start_villager_proper.sh

# Test with standard image
export FORCE_STANDARD_KALI=true
./scripts/start_villager_proper.sh
```

## Conclusion

The Villager AI framework is designed to work seamlessly regardless of Cyberspike registry availability. The automatic fallback system ensures that all users can enjoy full functionality with the standard Kali image, while advanced users can configure Cyberspike access if available.

**For most users**: No additional setup is required - everything works out of the box!
**For advanced users**: Follow the Cyberspike configuration steps above.
