from __future__ import annotations

import asyncio
import ipaddress
import socket
from urllib.parse import urlparse

from app.core.config import get_settings
from app.core.errors import bad_request


def _allow_localhost() -> bool:
    env = get_settings().app_env.lower()
    return env in {"development", "dev", "local"}


async def ensure_public_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise bad_request("Only http and https URLs are allowed.")
    if not parsed.hostname:
        raise bad_request("Invalid URL.")

    host = parsed.hostname.lower()
    allow_localhost = _allow_localhost()
    if host in {"localhost"}:
        if allow_localhost:
            return
        raise bad_request("Localhost targets are not allowed.")

    await _ensure_public_host(host, allow_localhost)


def _is_private_ip(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    return (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_reserved
        or address.is_multicast
        or address.is_unspecified
    )


def _ensure_ip_is_public(ip: str, allow_localhost: bool) -> None:
    address = ipaddress.ip_address(ip)
    if address.is_loopback and allow_localhost:
        return
    if _is_private_ip(address):
        raise bad_request("Private network targets are not allowed.")


def _resolve_host(host: str, allow_localhost: bool) -> set[str]:
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return set()
    _ensure_ip_is_public(str(address), allow_localhost)
    return {str(address)}


async def _ensure_public_host(host: str, allow_localhost: bool) -> None:
    addresses = _resolve_host(host, allow_localhost)
    if not addresses:
        try:
            loop = asyncio.get_running_loop()
            infos = await asyncio.wait_for(
                loop.getaddrinfo(host, None, proto=socket.IPPROTO_TCP),
                timeout=3.0,
            )
        except Exception as exc:
            raise bad_request("Unable to resolve host.") from exc

        addresses = {info[4][0] for info in infos if info[4]}

    if not addresses:
        raise bad_request("Unable to resolve host.")

    for address in addresses:
        _ensure_ip_is_public(address, allow_localhost)
