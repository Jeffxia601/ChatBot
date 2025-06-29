# AI Dating Simulator
> GPT-4o-mini powered AI chat application that simulates dating conversations, deployed on Microsoft Azure.
> ​**Personal full-stack project**​ | Deployed May 2025 | ​**Python 3.12.7**

[![Azure Deployment](https://img.shields.io/badge/Deployed%20on-Microsoft%20Azure-0089D6?logo=microsoft-azure)](https://dpchatbot-b3d9f4bdbveadcgt.centralus-01.azurewebsites.net/) (Click this icon to view the app)
## Key Features
- GPT-4o-mini powered conversations
- English/Chinese language switching
- Context memory across conversations
- Automatic conversation summaries

## Technical Stack
- ​**Frontend**: HTML/CSS/JavaScript
- ​**Backend**: Flask + OpenAI API
- **Others**: Redis, Azure

## 🔧 Installation
```bash
# Clone with Python 3.12+ required
git clone https://github.com/Jeffxia601/ai-dating-simulator.git
cd ai-dating-simulator

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


