# Foundry Multi-Agent NW

Multi-agent workflow project for Azure AI Foundry using a router + specialist agents pattern.

## Project Structure

- `workflow.yaml`: Workflow definition (`multi-expert-router`) that routes a user question to one or more specialist agents and synthesizes the final answer.
- `scripts/provision_foundry_workflow_agents.py`: Python provisioning script to create or update required Azure AI Foundry agents.

## Workflow Overview

The workflow includes these agents:

- `orchestrator`
- `neuro-expert`
- `benefits-expert`
- `geography-expert`
- `synthesizer`

At runtime, the orchestrator returns route booleans and the workflow conditionally invokes experts, then combines outputs for the synthesizer.

## Prerequisites

- Python 3.10+
- Azure CLI authenticated to the correct tenant/subscription (`az login`)
- Access to an Azure AI Foundry project endpoint
- Python packages (see `requirements.txt`):
  - `azure-ai-projects>=2.0.0b1` (new Foundry Agent Service SDK)
  - `azure-identity`

## Provision Agents

1. Install dependencies:

   ```bash
   pip install -r requirements.txt --pre
   ```

2. (Optional) Override the default endpoint/model via environment variables:

   ```bash
   export AZURE_AI_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
   export AZURE_AI_MODEL="chat-main"
   ```

   If unset, the script falls back to the values hard-coded for `proj-nw`.

3. Run provisioning script:

   ```bash
   python scripts/provision_foundry_workflow_agents.py
   ```

   The script uses `DefaultAzureCredential`, which picks up credentials from
   `az login`, managed identity, environment variables, etc.

## Notes

- This project targets **new** Azure AI Foundry agents (not classic). The
  `azure-ai-projects` v2 SDK is required per the
  [migration guide](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/migrate?view=foundry).
- Each agent is defined as a `PromptAgentDefinition` and deployed via
  `client.agents.create_version()`, which creates a new version if the agent
  already exists.
- Keep environment-specific values out of source control where possible.