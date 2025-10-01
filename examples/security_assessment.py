#!/usr/bin/env python3
"""
Villager AI Framework - Security Assessment Example

This example demonstrates how to use Villager for comprehensive
security assessments using AI-driven task decomposition.
"""

import sys
import os

# Add Villager to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def security_assessment_workflow():
    """Demonstrate a complete security assessment workflow."""
    
    print("🔍 Villager AI - Security Assessment Workflow")
    print("=" * 50)
    
    # Step 1: Target reconnaissance
    print("\n📡 Step 1: Target Reconnaissance")
    print("-" * 35)
    
    reconnaissance_tasks = [
        {
            "task": "Subdomain Enumeration",
            "tools": ["subfinder", "amass", "assetfinder"],
            "description": "Discover all subdomains of target.com"
        },
        {
            "task": "Port Scanning",
            "tools": ["nmap", "rustscan", "masscan"],
            "description": "Identify open ports and services"
        },
        {
            "task": "Technology Detection",
            "tools": ["whatweb", "wappalyzer", "httpx"],
            "description": "Identify web technologies and frameworks"
        }
    ]
    
    for task in reconnaissance_tasks:
        print(f"\n🎯 {task['task']}:")
        print(f"   Tools: {', '.join(task['tools'])}")
        print(f"   Purpose: {task['description']}")
    
    # Step 2: Vulnerability scanning
    print("\n🔍 Step 2: Vulnerability Scanning")
    print("-" * 40)
    
    vulnerability_tasks = [
        {
            "category": "Web Application",
            "tools": ["nikto", "dirb", "gobuster", "sqlmap"],
            "vulnerabilities": ["SQL Injection", "XSS", "Directory Traversal", "Authentication Bypass"]
        },
        {
            "category": "Network Services",
            "tools": ["nmap", "nessus", "openvas"],
            "vulnerabilities": ["Buffer Overflows", "Privilege Escalation", "Service Misconfigurations"]
        },
        {
            "category": "Infrastructure",
            "tools": ["nuclei", "zap", "burpsuite"],
            "vulnerabilities": ["SSL/TLS Issues", "CORS Misconfigurations", "Security Headers"]
        }
    ]
    
    for vuln_task in vulnerability_tasks:
        print(f"\n🔧 {vuln_task['category']} Testing:")
        print(f"   Tools: {', '.join(vuln_task['tools'])}")
        print(f"   Targets: {', '.join(vuln_task['vulnerabilities'])}")
    
    # Step 3: Exploitation attempts
    print("\n💥 Step 3: Exploitation Attempts")
    print("-" * 40)
    
    exploitation_tasks = [
        {
            "vulnerability": "SQL Injection",
            "tools": ["sqlmap", "custom_payloads"],
            "payloads": ["' OR '1'='1", "UNION SELECT", "Time-based blind"]
        },
        {
            "vulnerability": "Command Injection",
            "tools": ["burpsuite", "custom_scripts"],
            "payloads": ["; ls", "| whoami", "` id`"]
        },
        {
            "vulnerability": "File Upload",
            "tools": ["webshells", "reverse_shells"],
            "payloads": ["PHP webshell", "JSP backdoor", "ASPX shell"]
        }
    ]
    
    for exploit_task in exploitation_tasks:
        print(f"\n⚡ {exploit_task['vulnerability']}:")
        print(f"   Tools: {', '.join(exploit_task['tools'])}")
        print(f"   Payloads: {', '.join(exploit_task['payloads'])}")
    
    # Step 4: Post-exploitation
    print("\n🎯 Step 4: Post-Exploitation")
    print("-" * 35)
    
    post_exploit_tasks = [
        {
            "phase": "Initial Access",
            "activities": ["System enumeration", "User privilege escalation", "Persistence establishment"]
        },
        {
            "phase": "Lateral Movement",
            "activities": ["Network discovery", "Credential harvesting", "Service exploitation"]
        },
        {
            "phase": "Data Exfiltration",
            "activities": ["Sensitive data identification", "Data collection", "Exfiltration channels"]
        }
    ]
    
    for phase in post_exploit_tasks:
        print(f"\n🔄 {phase['phase']}:")
        for activity in phase['activities']:
            print(f"   • {activity}")
    
    # Step 5: Reporting
    print("\n📊 Step 5: AI-Generated Reporting")
    print("-" * 40)
    
    report_sections = [
        "Executive Summary with risk assessment",
        "Detailed vulnerability findings with CVSS scores",
        "Exploitation proof-of-concepts",
        "Remediation recommendations",
        "Compliance mapping (OWASP, NIST, ISO 27001)",
        "Risk prioritization matrix"
    ]
    
    for section in report_sections:
        print(f"   • {section}")
    
    print("\n✅ Security Assessment Workflow Complete!")
    print("\n📋 This workflow demonstrates how Villager AI can:")
    print("   • Automatically decompose complex security assessments")
    print("   • Coordinate multiple security tools and agents")
    print("   • Execute tasks in isolated, secure environments")
    print("   • Generate comprehensive, AI-powered reports")

def mcp_integration_example():
    """Show how to use MCP tools for security assessment."""
    
    print("\n🔗 MCP Integration Example")
    print("=" * 30)
    
    # Example MCP calls for security assessment
    mcp_calls = [
        {
            "tool": "mcp_villager-proper_create_task",
            "parameters": {
                "abstract": "Comprehensive Security Assessment",
                "description": "Perform full security assessment of target.com including reconnaissance, vulnerability scanning, and exploitation attempts",
                "verification": "Provide detailed report with all findings and recommendations"
            }
        },
        {
            "tool": "mcp_villager-proper_schedule_agent",
            "parameters": {
                "agent_name": "Security Analyst",
                "task_input": "Analyze the reconnaissance results and identify high-value targets for further testing"
            }
        },
        {
            "tool": "mcp_villager-proper_execute_tool",
            "parameters": {
                "tool_name": "os_execute_cmd",
                "parameters": {
                    "system_command": "nmap -sV -sC -A target.com"
                }
            }
        }
    ]
    
    for i, call in enumerate(mcp_calls, 1):
        print(f"\n{i}. {call['tool']}:")
        print(f"   Parameters: {call['parameters']}")

if __name__ == "__main__":
    security_assessment_workflow()
    mcp_integration_example()
