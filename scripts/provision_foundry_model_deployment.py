#!/usr/bin/env python3
"""
Provision the 'chat-main' model deployment used by the multi-expert-router
workflow agents.

Mirrors the pattern in provision_foundry_workflow_agents.py so every
infrastructure component is scripted and repeatable.

Requires:
    pip install azure-identity azure-mgmt-cognitiveservices azure-mgmt-resource
"""

from azure.identity import AzureCliCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import (
    Deployment,
    DeploymentModel,
    DeploymentProperties,
    Sku,
)
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.subscriptions import SubscriptionClient

# ── Azure resource identifiers ───────────────────────────────────────────────
# The ACCOUNT_NAME is derived from the project endpoint in
# provision_foundry_workflow_agents.py:
#   https://proj-nw-resource.services.ai.azure.com/api/projects/proj-nw
ACCOUNT_NAME = "proj-nw-resource"  # AI Services account name

# ── Model deployment configuration ───────────────────────────────────────────
DEPLOYMENT_NAME  = "chat-main"
MODEL_FORMAT     = "OpenAI"
MODEL_NAME       = "gpt-4o"                     # catalog model name
MODEL_VERSION    = "2024-11-20"                  # model version to deploy
SKU_NAME         = "GlobalStandard"              # SKU tier (GlobalStandard, Standard, etc.)
SKU_CAPACITY     = 10                            # thousands of tokens-per-minute (TPM)


def _get_subscription_id(credential: AzureCliCredential) -> str:
    """Return the ID of the currently-active Azure subscription."""
    sub_client = SubscriptionClient(credential)
    # The first subscription returned is the one selected via `az account set`
    sub = next(sub_client.subscriptions.list())
    return sub.subscription_id


def _get_resource_group(credential: AzureCliCredential, subscription_id: str,
                        account_name: str) -> str:
    """Find the resource group that contains *account_name*."""
    rm_client = ResourceManagementClient(credential, subscription_id)
    for resource in rm_client.resources.list(
        filter=f"name eq '{account_name}'"
    ):
        return resource.id.split("/resourceGroups/")[1].split("/")[0]
    raise SystemExit(
        f"ERROR: Could not find a resource named '{account_name}' "
        f"in subscription {subscription_id}."
    )


def main() -> None:
    credential = AzureCliCredential()

    # ── Resolve subscription & resource group dynamically ─────────────────────
    subscription_id = _get_subscription_id(credential)
    resource_group = _get_resource_group(credential, subscription_id, ACCOUNT_NAME)
    print(f"Subscription : {subscription_id}")
    print(f"Resource group: {resource_group}")

    client = CognitiveServicesManagementClient(credential, subscription_id)

    # ── Discover existing deployments ─────────────────────────────────────────
    existing = {
        d.name: d
        for d in client.deployments.list(resource_group, ACCOUNT_NAME)
    }

    # ── Build desired deployment spec ─────────────────────────────────────────
    deployment = Deployment(
        sku=Sku(name=SKU_NAME, capacity=SKU_CAPACITY),
        properties=DeploymentProperties(
            model=DeploymentModel(
                format=MODEL_FORMAT,
                name=MODEL_NAME,
                version=MODEL_VERSION,
            ),
        ),
    )

    verb = "UPDATED" if DEPLOYMENT_NAME in existing else "CREATED"
    print(f"{'Updating' if verb == 'UPDATED' else 'Creating'} deployment "
          f"'{DEPLOYMENT_NAME}' ({MODEL_NAME}@{MODEL_VERSION}) …")

    # begin_create_or_update is idempotent — safe for both create and update
    poller = client.deployments.begin_create_or_update(
        resource_group_name=resource_group,
        account_name=ACCOUNT_NAME,
        deployment_name=DEPLOYMENT_NAME,
        deployment=deployment,
    )
    result = poller.result()  # blocks until provisioning completes

    print(f"{verb}\t{result.name}\t"
          f"{result.properties.model.name}@{result.properties.model.version}\t"
          f"sku={result.sku.name}/{result.sku.capacity}")


if __name__ == "__main__":
    main()
