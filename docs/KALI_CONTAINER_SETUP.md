# Kali Container Setup Guide

## Overview

Villager AI uses Kali Linux Docker containers to provide a secure, isolated environment for security tool execution. The system uses the standard `kalilinux/kali-rolling` image with automatic tool installation and SSH-based command execution.

## Current Status

### ✅ What's Working
- **Standard Kali Image**: Uses `kalilinux/kali-rolling` as the primary image
- **Tool Installation**: All security tools (nmap, msfvenom, gobuster, etc.) are automatically installed
- **SSH Access**: Secure SSH-based command execution
- **24-hour Persistence**: Containers persist for 24 hours with automatic cleanup
- **Full Functionality**: All Villager features work perfectly with standard Kali

## Setup Options

### ✅ Standard Kali Image (Primary Method)
The system uses the standard Kali image by default, which provides:
- All essential security tools (nmap, msfvenom, gobuster, nikto, sqlmap, hydra, john, hashcat)
- Automatic tool installation during container startup
- Full Villager functionality
- No additional setup required
- Reliable and always accessible

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

#### 1. Docker Image Pull Timeout
**Error**: `net/http: request canceled while waiting for connection`
**Solution**: Check Docker daemon status and network connectivity

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

# Test Docker connectivity
docker pull hello-world
```

## For Developers/Contributors

### Customizing Kali Container Setup
If you want to customize the Kali container setup:

1. **Custom Images**: Modify the `ensure_kali_image()` function
2. **Tool Installation**: Update the container startup script
3. **SSH Configuration**: Modify SSH settings in container creation
4. **Documentation**: Update setup guides with specific requirements

### Testing
```bash
# Test Kali container functionality
./scripts/test_villager_setup.sh

# Test with custom image
export CUSTOM_KALI_IMAGE=your-custom-image
./scripts/start_villager_proper.sh
```

## Conclusion

The Villager AI framework is designed to work seamlessly with the standard Kali image, which provides all necessary functionality. The system is optimized for reliability and accessibility, ensuring that all users can enjoy full functionality without any additional setup.

**For all users**: No additional setup is required - everything works out of the box with the standard Kali image!
**For future Cyberspike access**: The system will automatically detect and use Cyberspike if it becomes available.
