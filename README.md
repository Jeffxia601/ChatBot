# Lightweight Virtual Character Dialogue System (An AI Dating Simulator)
> GPT-4o-mini powered AI chat application that simulates dating conversations, deployed on Microsoft Azure.
> ​**Personal full-stack project**​ | Deployed May 2025 | ​**Python 3.11**

[![Azure Deployment](https://img.shields.io/badge/Deployed%20on-Microsoft%20Azure-0089D6?logo=microsoft-azure)](https://dpchatbot-b3d9f4bdbveadcgt.centralus-01.azurewebsites.net/) (Click this icon to view the app)

## Core Engineering Innovations
| ​**Feature**​                | ​**Implementation**​                        | ​**Performance**​            |
| :------------------------- | :---------------------------------------- | :-------------------------- |
| ​**High-Frequency Dialog**​ | Flask + Redis async queue processing       | ​**~200ms avg response time**​ |
| ​**Long-Context Stability**​ | Round-triggered summarization (5 turns/summary)<br>Key entity preservation algorithm | Effective memory decay mitigation |
| ​**Production-Grade SLA**​   | Azure Container Deployment<br>Application Insights monitoring | ​**>99% availability**​<br>Millisecond-level response tracking |

## 🔧 Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key as environment variable
# For Linux/macOS:
export OPENAI_API_KEY="your-api-key-here"

# For Windows (Command Prompt):
set OPENAI_API_KEY=your-api-key-here

# For Windows (PowerShell):
$env:OPENAI_API_KEY="your-api-key-here"

# Run local dev server
python app.py


