"""Send a startup DM to the home channel when the gateway boots.

Uses the running gateway's adapter directly — no subprocess, no new
WebSocket connection (avoids conflicts with WeCom's ws-based transport).
"""

import logging
import platform as platform_mod

from hermes_cli.config import get_hermes_home

logger = logging.getLogger("hooks.say-hello")


async def handle(event_type: str, context: dict) -> None:
    # Get the running gateway instance via its module-level weakref
    from gateway.run import _gateway_runner_ref

    gateway = _gateway_runner_ref()
    if gateway is None:
        logger.warning("Gateway runner not available, skipping startup message")
        return

    hostname = platform_mod.node()
    hermes_home = str(get_hermes_home())
    if "/profiles/" in hermes_home:
        profile = hermes_home.rsplit("/profiles/", 1)[-1]
    else:
        profile = "default"

    message = f"{hostname} / {profile} 已上线"

    # Send to each platform's home channel using the gateway's own adapters
    for platform, adapter in gateway.adapters.items():
        home = gateway.config.get_home_channel(platform)
        if not home or not home.chat_id:
            continue
        try:
            await adapter.send(str(home.chat_id), message)
            logger.info("Startup message sent to %s: %s", platform.value, message)
        except Exception as e:
            logger.warning("Failed to send startup message to %s: %s", platform.value, e)
