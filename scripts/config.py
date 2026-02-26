"""Shared configuration for provisioning scripts.

On first import, generates a random 4-character suffix and persists it to
``scripts/.suffix``.  Subsequent imports (and runs of other scripts) reuse
the same suffix so that resource names stay consistent across all three
provisioning steps.

Delete ``scripts/.suffix`` to generate a new suffix on the next run.
"""

import os
import random
import string

_SUFFIX_PATH = os.path.join(os.path.dirname(__file__), ".suffix")


def _load_or_create_suffix() -> str:
    if os.path.exists(_SUFFIX_PATH):
        with open(_SUFFIX_PATH) as f:
            value = f.read().strip()
            if value:
                return value
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    with open(_SUFFIX_PATH, "w") as f:
        f.write(suffix)
    print(f"Generated new resource suffix: {suffix}  (stored in scripts/.suffix)")
    return suffix


SUFFIX = _load_or_create_suffix()

# ── Derived resource names ────────────────────────────────────────────────────
RESOURCE_GROUP_NAME = f"rg-proj-nw-{SUFFIX}"
LOCATION            = "eastus2"

ACCOUNT_NAME = f"proj-nw-resource-{SUFFIX}"
ACCOUNT_SKU  = "S0"
ACCOUNT_KIND = "AIServices"

PROJECT_NAME = f"proj-nw-{SUFFIX}"

DEPLOYMENT_NAME  = "chat-main"
MODEL_FORMAT     = "OpenAI"
MODEL_NAME       = "gpt-4o"
MODEL_VERSION    = "2024-11-20"
SKU_NAME         = "GlobalStandard"
SKU_CAPACITY     = 10

ENDPOINT = os.environ.get(
    "AZURE_AI_ENDPOINT",
    f"https://{ACCOUNT_NAME}.services.ai.azure.com/api/projects/{PROJECT_NAME}",
)
MODEL_DEPLOYMENT = os.environ.get("AZURE_AI_MODEL", DEPLOYMENT_NAME)
