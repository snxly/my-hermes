"""Send a startup DM to the home channel when the gateway boots.

Uses the running gateway's adapter directly — no subprocess, no new
WebSocket connection (avoids conflicts with WeCom's ws-based transport).
"""

import logging
from pathlib import Path

import yaml

from hermes_cli.config import get_hermes_home

logger = logging.getLogger("hooks.say-hello")


def _profile_display_name(profile: str) -> str:
    """Read profile_meta.display_name from the profile's config.yaml.

    Falls back to the profile name when the field is missing or unreadable.
    """
    try:
        cfg_path = Path(str(get_hermes_home())) / "config.yaml"
        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
        meta = (cfg or {}).get("profile_meta") or {}
        return meta.get("display_name") or profile
    except Exception:
        return profile


async def handle(event_type: str, context: dict) -> None:
    # Get the running gateway instance via its module-level weakref
    from gateway.run import _gateway_runner_ref

    gateway = _gateway_runner_ref()
    if gateway is None:
        logger.warning("Gateway runner not available, skipping startup message")
        return

    hermes_home = str(get_hermes_home())
    if "/profiles/" in hermes_home:
        profile = hermes_home.rsplit("/profiles/", 1)[-1]
    else:
        profile = "default"

    display = _profile_display_name(profile)
    message = f"✨ {display} 已上线，随时听候差遣～"

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
