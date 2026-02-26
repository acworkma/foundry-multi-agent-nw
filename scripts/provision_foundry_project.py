#!/usr/bin/env python3
"""
Provision the Azure AI Foundry project that underpins the multi-expert-router
workflow.  This script creates, in order:

    1. Resource Group
    2. AI Services Account  (Microsoft.CognitiveServices/accounts, kind=AIServices)
    3. Foundry Project      (Microsoft.CognitiveServices/accounts/projects)

Run this *before* provision_foundry_model_deployment.py and
provision_foundry_workflow_agents.py.

Requires:
    pip install azure-identity azure-mgmt-resource azure-mgmt-subscription azure-mgmt-cognitiveservices
"""

from azure.identity import AzureCliCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import (
    Account,
    AccountProperties,
    Project,
    ProjectProperties,
    Sku,
)
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.subscription import SubscriptionClient

# ── Configuration ─────────────────────────────────────────────────────────────
# These names must match the values used by the downstream provisioning scripts.
RESOURCE_GROUP_NAME = "rg-proj-nw"
LOCATION            = "eastus2"

ACCOUNT_NAME        = "proj-nw-resource"     # AI Services account
ACCOUNT_SKU         = "S0"
ACCOUNT_KIND        = "AIServices"

PROJECT_NAME        = "proj-nw"              # Foundry project (child of account)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_subscription_id(credential: AzureCliCredential) -> str:
    """Return the ID of the currently-active Azure subscription."""
    sub_client = SubscriptionClient(credential)
    sub = next(sub_client.subscriptions.list())
    return sub.subscription_id


def _ensure_resource_group(
    credential: AzureCliCredential,
    subscription_id: str,
) -> None:
    """Create the resource group if it does not already exist."""
    rm = ResourceManagementClient(credential, subscription_id)
    result = rm.resource_groups.create_or_update(
        RESOURCE_GROUP_NAME,
        {"location": LOCATION},
    )
    print(f"RESOURCE GROUP\t{result.name}\t{result.location}")


def _ensure_ai_services_account(
    client: CognitiveServicesManagementClient,
) -> None:
    """Create or update the AI Services account."""
    account = Account(
        location=LOCATION,
        kind=ACCOUNT_KIND,
        sku=Sku(name=ACCOUNT_SKU),
        properties=AccountProperties(),
    )
    poller = client.accounts.begin_create(
        resource_group_name=RESOURCE_GROUP_NAME,
        account_name=ACCOUNT_NAME,
        account=account,
    )
    result = poller.result()
    print(f"AI SERVICES\t{result.name}\t{result.properties.endpoint}")


def _ensure_project(
    client: CognitiveServicesManagementClient,
) -> None:
    """Create or update the Foundry project under the AI Services account."""
    project = Project(
        location=LOCATION,
        properties=ProjectProperties(
            display_name=PROJECT_NAME,
            description="Multi-expert-router workflow project",
        ),
    )
    poller = client.projects.begin_create(
        resource_group_name=RESOURCE_GROUP_NAME,
        account_name=ACCOUNT_NAME,
        project_name=PROJECT_NAME,
        project=project,
    )
    result = poller.result()
    endpoint = f"https://{ACCOUNT_NAME}.services.ai.azure.com/api/projects/{PROJECT_NAME}"
    print(f"PROJECT\t\t{result.name}\t{endpoint}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    credential = AzureCliCredential()
    subscription_id = _get_subscription_id(credential)
    print(f"Subscription: {subscription_id}\n")

    # 1. Resource Group
    _ensure_resource_group(credential, subscription_id)

    # 2. AI Services Account
    cs_client = CognitiveServicesManagementClient(credential, subscription_id)
    _ensure_ai_services_account(cs_client)

    # 3. Foundry Project
    _ensure_project(cs_client)

    print(f"\nDone. Project endpoint:\n"
          f"  https://{ACCOUNT_NAME}.services.ai.azure.com/api/projects/{PROJECT_NAME}")


if __name__ == "__main__":
    main()
