# Lightweight Virtual Character Dialogue System (AI Dating Simulator)
> GPT-4o-mini powered AI chat application that simulates dating conversations, deployed on Microsoft Azure.
> ​**Personal full-stack project**​ | Deployed May 2025 | ​**Python 3.11**

[![Azure Deployment](https://img.shields.io/badge/Deployed%20on-Microsoft%20Azure-0089D6?logo=microsoft-azure)](https://dpchatbot-b3d9f4bdbveadcgt.centralus-01.azurewebsites.net/) (Click this icon to view the app)

## Core Engineering Innovations
| ​**Feature**​                | ​**Implementation**​                        | ​**Performance**​            |
| :------------------------- | :---------------------------------------- | :-------------------------- |
| ​**High-Frequency Dialog**​ | Flask + Redis async queue processing       | ​**~200ms avg response time**​ |
| ​**Long-Context Stability**​ | Round-triggered summarization (5 turns/summary)<br>Key entity preservation algorithm | Effective memory decay mitigation |
| ​**Production-Grade SLA**​   | Azure Container Deployment<br>Application Insights monitoring | ​>99% availability​<br>Millisecond-level response tracking |

## Getting Started (Quick Setup)
1.  ​**Install Dependencies:​**​
  ```bash
  pip install --user -r requirements.txt
  ```
2.  **Set your OpenAI API key as environment variable**
    *   **For Linux/macOS:**
        ```bash
        export OPENAI_API_KEY="your-api-key-here"
        ```
    *   **For Windows (Command Prompt):**
        ```bash
        set OPENAI_API_KEY=your-api-key-here
        ```
    *   **For Windows (PowerShell)**
        ```bash
        $env:OPENAI_API_KEY="your-api-key-here"
        ```
3.  **Run local dev server**
```bash
python app.py
```
