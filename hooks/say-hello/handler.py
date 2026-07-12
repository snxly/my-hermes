"""Send a startup DM to the home channel when the gateway boots.

Runs in a daemon thread to avoid blocking the gateway startup event loop.
"""

import logging
import platform as platform_mod
import subprocess
import threading

from hermes_cli.config import get_hermes_home

logger = logging.getLogger("hooks.say-hello")


def _send_message(profile: str, target_platform: str, message: str) -> None:
    """Fire-and-forget: run hermes send in a subprocess."""
    try:
        result = subprocess.run(
            ["hermes", "--profile", profile, "send", "--to", target_platform, message],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            logger.info("Startup message sent: %s", message)
        else:
            logger.warning(
                "hermes send failed (exit=%d): %s",
                result.returncode,
                result.stderr.strip(),
            )
    except Exception as e:
        logger.warning("Failed to send startup message: %s", e)


async def handle(event_type: str, context: dict) -> None:
    hostname = platform_mod.node()

    # Infer profile name from HERMES_HOME path
    hermes_home = str(get_hermes_home())
    if "/profiles/" in hermes_home:
        profile = hermes_home.rsplit("/profiles/", 1)[-1]
    else:
        profile = "default"

    # Pick the first active platform from the gateway:startup context
    platforms = context.get("platforms", [])
    if not platforms:
        logger.warning("No active platforms, cannot send startup message")
        return
    target_platform = platforms[0]

    message = f"{hostname} / {profile} 已上线"

    # Run in a daemon thread so the gateway event loop is not blocked
    thread = threading.Thread(
        target=_send_message,
        args=(profile, target_platform, message),
        name="say-hello",
        daemon=True,
    )
    thread.start()
