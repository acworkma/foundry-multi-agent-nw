#!/usr/bin/env python3
from azure.ai.agents import AgentsClient
from azure.identity import AzureCliCredential

ENDPOINT = "https://proj-nw-resource.services.ai.azure.com/api/projects/proj-nw"
MODEL_DEPLOYMENT = "chat-main"

AGENT_SPECS = {
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
    client = AgentsClient(endpoint=ENDPOINT, credential=AzureCliCredential())
    existing = {agent.name: agent for agent in client.list_agents()}

    for name, instructions in AGENT_SPECS.items():
        if name in existing:
            agent = client.update_agent(
                agent_id=existing[name].id,
                name=name,
                model=MODEL_DEPLOYMENT,
                instructions=instructions,
                description=f"Configured for workflow multi-expert-router ({name})",
            )
            print(f"UPDATED\t{name}\t{agent.id}")
        else:
            agent = client.create_agent(
                name=name,
                model=MODEL_DEPLOYMENT,
                instructions=instructions,
                description=f"Configured for workflow multi-expert-router ({name})",
            )
            print(f"CREATED\t{name}\t{agent.id}")


if __name__ == "__main__":
    main()
