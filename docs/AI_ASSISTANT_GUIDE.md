# AI Assistant Guide - Villager AI + HexStrike Integration

## 🎯 Purpose of This Guide

This guide is specifically designed for AI assistants (like Cursor AI, Claude, etc.) to understand how to intelligently use both Villager AI and HexStrike tools in a hybrid approach. When both tools are available, the AI should make smart decisions about which tool to use based on task complexity and requirements.

## 🤖 How to Use This Guide

**For AI Assistants:** Read this guide to understand the hybrid approach and decision-making logic for using Villager AI and HexStrike tools effectively.

**For Users:** Share this guide with your AI assistant to ensure it understands how to use both tools optimally.

---

## 🏗️ Understanding the Hybrid Architecture

### **The Setup**
- **Villager AI**: Advanced AI orchestration framework with its own uncensored models (DeepSeek, etc.)
- **HexStrike**: 150+ direct security tools for immediate execution
- **Your AI Model**: Controls both tools and makes intelligent decisions about which to use

### **The Relationship**
- **NOT**: Villager controlling HexStrike
- **NOT**: HexStrike controlling Villager  
- **YES**: Your AI model intelligently choosing between both tools based on task needs

---

## 🎯 Decision-Making Framework

### **Use HexStrike When:**
- **Task is simple** - Single command or tool execution
- **Immediate results needed** - Quick scans, direct tool access
- **One-step operations** - No complex orchestration required
- **Fast reconnaissance** - Rapid information gathering

**Examples:**
- Quick port scan: `mcp_hexstrike-ai_nmap_scan()`
- Generate payload: `mcp_hexstrike-ai_msfvenom_generate()`
- Directory enumeration: `mcp_hexstrike-ai_gobuster_scan()`
- Hash cracking: `mcp_hexstrike-ai_hashcat_crack()`

### **Use Villager AI When:**
- **Task is complex** - Multi-phase operations required
- **AI reasoning needed** - Intelligent analysis and decision-making
- **Task decomposition** - Breaking down large objectives
- **Orchestrated workflows** - Coordinated multi-tool operations

**Examples:**
- Comprehensive security assessment: `mcp_villager-proper_create_task()`
- Complex penetration testing: `mcp_villager-proper_schedule_agent()`
- Multi-step vulnerability analysis: Villager's AI orchestration
- Advanced payload development: Villager's uncensored AI reasoning

---

## 🧠 AI Decision Logic

```
IF user asks for:
  - Quick scan/check → Use HexStrike
  - Single tool execution → Use HexStrike  
  - Immediate results → Use HexStrike
  - Simple reconnaissance → Use HexStrike

IF user asks for:
  - Comprehensive assessment → Use Villager AI
  - Complex analysis → Use Villager AI
  - Multi-step operation → Use Villager AI
  - AI-driven decision making → Use Villager AI

IF unsure:
  - Start with HexStrike for quick results
  - Escalate to Villager AI if complexity increases
```

---

## 💡 Practical Examples

### **Scenario 1: Quick Port Scan**
**User Request:** "Scan port 22 on 192.168.1.1"

**AI Decision:** Use HexStrike (simple, immediate result needed)
```python
result = mcp_hexstrike-ai_nmap_scan(
    target="192.168.1.1",
    ports="22",
    scan_type="-sV"
)
```

### **Scenario 2: Comprehensive Security Assessment**
**User Request:** "Perform a full security assessment of target.com"

**AI Decision:** Use Villager AI (complex, multi-phase operation)
```python
result = mcp_villager-proper_create_task(
    abstract="Comprehensive Security Assessment",
    description="Full security assessment of target.com including reconnaissance, vulnerability scanning, and analysis",
    verification="Detailed report with findings and recommendations"
)
```

### **Scenario 3: Progressive Approach**
**User Request:** "Check if target.com is vulnerable to SQL injection"

**AI Decision:** Start with HexStrike, escalate if needed
```python
# Step 1: Quick check with HexStrike
result = mcp_hexstrike-ai_sqlmap_scan(
    url="http://target.com/login.php"
)

# Step 2: If complex analysis needed, escalate to Villager
if complex_analysis_required:
    result = mcp_villager-proper_schedule_agent(
        agent_name="SQL Injection Analyst",
        task_input="Analyze SQL injection results and develop exploitation strategy"
    )
```

---

## 🛠️ Tool Capabilities Summary

### **HexStrike Capabilities (150+ Tools)**
- **Network Scanning**: Nmap, Masscan, Rustscan
- **Web Testing**: Gobuster, Dirb, Nikto, SQLMap
- **Password Attacks**: Hydra, John the Ripper, Hashcat
- **Payload Generation**: MSFVenom, custom exploits
- **Vulnerability Scanning**: Nuclei, custom scripts
- **Post-Exploitation**: Metasploit integration
- **And 150+ more specialized tools**

### **Villager AI Capabilities**
- **AI Orchestration**: Intelligent task decomposition
- **Agent Scheduling**: Multi-agent coordination
- **Uncensored AI**: Local DeepSeek and other models
- **Complex Workflows**: Multi-phase operations
- **Intelligent Analysis**: AI-driven decision making
- **Task Management**: Advanced task tracking and execution

---

## 🎯 Best Practices for AI Assistants

### **1. Always Consider Both Options**
- Don't default to one tool
- Evaluate task complexity first
- Choose the most appropriate tool

### **2. Progressive Escalation**
- Start simple with HexStrike
- Escalate to Villager AI if complexity increases
- Combine both tools when beneficial

### **3. Clear Communication**
- Explain why you chose a specific tool
- Offer alternatives when appropriate
- Suggest escalation paths

### **4. Efficiency Focus**
- Use HexStrike for quick wins
- Use Villager AI for complex operations
- Don't over-engineer simple tasks

---

## 🚨 Important Notes

### **Tool Independence**
- Villager AI and HexStrike are separate tools
- Your AI model controls both
- They work alongside each other, not hierarchically

### **AI Model Control**
- You (the AI assistant) make the decisions
- You choose which tool to use
- You orchestrate the hybrid approach

### **Uncensored Capabilities**
- Villager AI uses local, uncensored models
- HexStrike provides unrestricted tool access
- Both enable unrestricted cybersecurity operations

---

## 📋 Quick Reference

| Task Type | Tool Choice | Reason |
|-----------|-------------|---------|
| Quick port scan | HexStrike | Simple, immediate result |
| Generate payload | HexStrike | Direct tool execution |
| Directory enumeration | HexStrike | Single tool operation |
| Comprehensive assessment | Villager AI | Complex orchestration needed |
| Multi-phase testing | Villager AI | AI reasoning required |
| Vulnerability analysis | Villager AI | Intelligent decision making |
| Simple reconnaissance | HexStrike | Fast execution |
| Complex penetration test | Villager AI | Advanced orchestration |

---

## 🎯 Conclusion

The hybrid approach of Villager AI + HexStrike provides the best of both worlds:
- **HexStrike**: Fast, direct access to 150+ security tools
- **Villager AI**: Advanced AI orchestration and uncensored reasoning

As an AI assistant, your role is to intelligently choose between these tools based on task complexity, ensuring optimal results for the user while maintaining efficiency and effectiveness.

**Remember**: You control both tools. Choose wisely based on the task at hand.
