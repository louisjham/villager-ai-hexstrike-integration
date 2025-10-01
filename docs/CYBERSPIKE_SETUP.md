# Cyberspike Integration Setup Guide

## Overview

Villager AI includes integration with Cyberspike's custom Kali Docker image, which provides pre-configured security tools and optimized performance. However, the system includes robust fallback mechanisms to ensure functionality even when Cyberspike registry is inaccessible.

## Current Status

### ✅ What's Working
- **Standard Kali Image**: Primary method using `kalilinux/kali-rolling`
- **Tool Installation**: All security tools (nmap, msfvenom, gobuster, etc.) are automatically installed
- **SSH Access**: Secure SSH-based command execution
- **24-hour Persistence**: Containers persist for 24 hours with automatic cleanup
- **Full Functionality**: All Villager features work perfectly with standard Kali

### ⚠️ Cyberspike Registry Status
The Cyberspike registry (`gitlab.cyberspike.top:5050`) is currently **not accessible** due to:
- Network restrictions/blocking
- Private registry access requirements
- Geographic or authentication limitations

## Setup Options

### ✅ Standard Kali Image (Primary Method)
The system uses the standard Kali image by default, which provides:
- All essential security tools (nmap, msfvenom, gobuster, nikto, sqlmap, hydra, john, hashcat)
- Automatic tool installation during container startup
- Full Villager functionality
- No additional setup required
- Reliable and always accessible

### ⚠️ Cyberspike Access (Currently Unavailable)
The Cyberspike registry is currently blocked/unreachable. If access becomes available in the future:

1. **Network Access**: Ensure your network can reach `gitlab.cyberspike.top:5050`
2. **Authentication**: Configure Docker authentication if required
3. **Registry Configuration**: Add registry credentials if needed

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

The Villager AI framework is designed to work seamlessly with the standard Kali image, which provides all necessary functionality. The system is optimized for reliability and accessibility, ensuring that all users can enjoy full functionality without any additional setup.

**For all users**: No additional setup is required - everything works out of the box with the standard Kali image!
**For future Cyberspike access**: The system will automatically detect and use Cyberspike if it becomes available.
