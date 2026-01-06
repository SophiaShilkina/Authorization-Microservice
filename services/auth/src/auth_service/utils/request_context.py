from typing import Dict, Any

from fastapi import Request


def get_request_context(request: Request) -> dict:
    """Все нужные данные из запроса"""
    context = {
        "headers": dict(request.headers),
        "method": request.method,
        "url": str(request.url),
        "path": request.url.path,
        "ip": request.client.host if request.client else None,
        "port": request.client.port if request.client else None,
    }

    return context


def extract_device_info(context: Dict[str, Any]) -> dict | None:
    """Извлечение информации об устройстве из заголовков"""
    headers = context.get("headers", {})

    user_agent = headers.get("user-agent")
    if not user_agent:
        return None

    device_info = {
        "user_agent": user_agent,
        "accept_language": headers.get("accept-language"),
        "accept_encoding": headers.get("accept-encoding"),
        "accept": headers.get("accept"),
        "connection": headers.get("connection"),
        "cache_control": headers.get("cache-control"),
    }

    return {k: v for k, v in device_info.items() if v is not None}


def extract_ip_address(context: Dict[str, Any]) -> str | None:
    """Извлечение IP адреса"""
    headers = context.get("headers", {})

    forwarded_headers = [
        "x-forwarded-for",
        "x-real-ip",
        "cf-connecting-ip",
        "true-client-ip",
        "forwarded",
    ]

    for header in forwarded_headers:
        value = headers.get(header)
        if value:
            ips = [ip.strip() for ip in value.split(",")]
            if ips:
                return ips[0].split(":")[0]

    return context.get("ip")
