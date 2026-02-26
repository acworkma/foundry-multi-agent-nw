#!/usr/bin/env python3
"""Provision (or update) the multi-expert-router agents in Azure AI Foundry.

Requires:
    pip install "azure-ai-projects>=2.0.0b1" --pre
    pip install azure-identity
"""

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential

from config import ENDPOINT, MODEL_DEPLOYMENT

AGENT_SPECS: dict[str, str] = {
    "orchestrator": (
        "You are a router. Classify the user question and return ONLY a strict JSON "
        "object with boolean keys: neuro, benefits, geography.\n"
        "Rules:\n"
        "- Set one or more keys true if relevant.\n"
        "- If uncertain, choose the most likely route(s).\n"
        "- No markdown, no explanation, no extra keys, no code fences.\n"
        "Valid output example: {\"neuro\":true,\"benefits\":false,\"geography\":true}"
    ),
    "neuro-expert": (
        "You are a neuroscience expert. Answer only the neuroscience/brain/behavior "
        "aspect of the user question. If the question is partially out of scope, "
        "clearly state that and still provide relevant neuroscience guidance."
    ),
    "benefits-expert": (
        "You are a benefits and policy expert. Answer only benefits/program/policy/"
        "coverage implications relevant to the user question. Be explicit about "
        "assumptions and eligibility caveats."
    ),
    "geography-expert": (
        "You are a geography and regional-context expert. Answer only location-specific "
        "considerations such as region, access, local constraints, and "
        "environment-related impacts."
    ),
    "synthesizer": (
        "You synthesize multiple expert responses into one final answer. Merge overlaps, "
        "resolve conflicts conservatively, note uncertainties, and provide a concise, "
        "actionable final response."
    ),
}


def main() -> None:
    client = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())

    for name, instructions in AGENT_SPECS.items():
        definition = PromptAgentDefinition(
            model=MODEL_DEPLOYMENT,
            instructions=instructions,
        )

        # Check whether the agent already exists by name.
        exists = False
        try:
            client.agents.get(agent_name=name)
            exists = True
        except ResourceNotFoundError:
            pass

        version = client.agents.create_version(
            agent_name=name,
            definition=definition,
            description=f"Configured for workflow multi-expert-router ({name})",
        )

        action = "UPDATED" if exists else "CREATED"
        print(f"{action}\t{name}\tv{version.version}")


if __name__ == "__main__":
    main()
