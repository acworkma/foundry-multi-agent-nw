# Foundry Multi-Agent NW

Provisions a multi-agent workflow on Azure AI Foundry using a router → specialist experts → synthesizer pattern.

## Prerequisites

- Python 3.10+
- Azure CLI authenticated to your tenant/subscription (`az login`)

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt --pre
```

The `--pre` flag is required for the `azure-ai-projects` beta package.

### 2. Provision the Foundry project

```bash
python scripts/provision_foundry_project.py
```

Creates the resource group `rg-proj-nw`, AI Services account `proj-nw-resource`, and Foundry project `proj-nw` in `eastus2`.

### 3. Deploy the model

```bash
python scripts/provision_foundry_model_deployment.py
```

Deploys `gpt-4o` as a `GlobalStandard` deployment named `chat-main` on the AI Services account.

### 4. Create the agents

```bash
python scripts/provision_foundry_workflow_agents.py
```

Creates or updates five agents in the project: `orchestrator`, `neuro-expert`, `benefits-expert`, `geography-expert`, and `synthesizer`.

To target a different project or model deployment, set these environment variables before running:

```bash
export AZURE_AI_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
export AZURE_AI_MODEL="<deployment-name>"
```

## Workflow

`workflow.yaml` defines the `multi-expert-router` workflow. To import it:

1. Open your Foundry project in the portal.
2. Go to **Build → Workflows → Create** (Blank workflow).
3. Switch to **YAML view** in the workflow editor.
4. Paste your YAML and **Save**.

## Project Structure

```
workflow.yaml                                  # Workflow definition
requirements.txt                               # Python dependencies
scripts/
  provision_foundry_project.py                 # Resource group, AI Services account, project
  provision_foundry_model_deployment.py        # gpt-4o model deployment
  provision_foundry_workflow_agents.py         # Five workflow agents
```