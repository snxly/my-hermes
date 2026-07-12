"""Send a startup DM to the home channel when the gateway boots."""

import logging
import os
import platform
import subprocess

from hermes_cli.config import get_hermes_home

logger = logging.getLogger("hooks.say-hello")


async def handle(event_type: str, context: dict) -> None:
    hostname = platform.node()

    # Infer profile name from HERMES_HOME path
    hermes_home = str(get_hermes_home())
    if "/profiles/" in hermes_home:
        profile = hermes_home.rsplit("/profiles/", 1)[-1]
    else:
        profile = "default"

    message = f"{hostname} / {profile} 已上线"

    try:
        subprocess.run(
            ["hermes", "--profile", profile, "send", message],
            capture_output=True,
            timeout=30,
        )
        logger.info("Startup message sent: %s", message)
    except Exception as e:
        logger.warning("Failed to send startup message: %s", e)
