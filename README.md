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

- Python 3.7+
- Azure CLI authenticated to the correct tenant/subscription
- Access to an Azure AI Foundry project endpoint
- Python packages:
  - `azure-ai-agents`
  - `azure-identity`

## Provision Agents

1. Update endpoint/model values in `scripts/provision_foundry_workflow_agents.py` if needed:
   - `ENDPOINT`
   - `MODEL_DEPLOYMENT`
2. Install dependencies:

   ```bash
   pip install azure-ai-agents azure-identity
   ```

3. Run provisioning script:

   ```bash
   python scripts/provision_foundry_workflow_agents.py
   ```

## Notes

- Keep environment-specific values out of source control where possible.
- Consider moving endpoint/model configuration to environment variables in a follow-up change.