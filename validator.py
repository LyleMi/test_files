#!/usr/bin/env python3
"""Standard-library validator for AriadneBench submission v3."""
import argparse
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote, urljoin, urlsplit

MAX_APIS = 10_000
MAX_STRING = 16 * 1024
LOCATIONS = {"path", "query", "header", "cookie", "body", "form"}
EVIDENCE_TYPES = {"script-static", "source-map", "manifest", "runtime-config", "html-form", "worker"}


class ValidationError(ValueError):
    pass


def _object(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    if set(value) != fields:
        missing, unknown = fields - value.keys(), value.keys() - fields
        if missing:
            raise ValidationError(f"{label}.{sorted(missing)[0]} is required")
        raise ValidationError(f"{label}.{sorted(unknown)[0]} is not allowed")
    return value


def _string(value: Any, label: str, maximum: int = MAX_STRING) -> str:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label} must be a non-empty string")
    if len(value) > maximum:
        raise ValidationError(f"{label} exceeds {maximum} characters")
    return value


def normalize_url(value: str) -> str:
    try:
        parts = urlsplit(urljoin("https://ariadne.invalid/", value.replace("\\", "/")))
        port = parts.port
    except (ValueError, UnicodeError) as error:
        raise ValidationError("submission contains an invalid URL") from error
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        raise ValidationError("submission contains an invalid URL")
    try:
        host = parts.hostname.encode("idna").decode("ascii").lower()
    except UnicodeError as error:
        raise ValidationError("submission contains an invalid URL") from error
    default = (parts.scheme.lower(), port) in {("http", 80), ("https", 443)}
    authority = host + (f":{port}" if port is not None and not default else "")
    path = quote(parts.path or "/", safe="/%:@!$&'()*+,;=-._~{}")
    if parts.scheme.lower() == "https" and authority == "ariadne.invalid":
        return path
    return f"{parts.scheme.lower()}://{authority}{path}"


def validate(value: Any) -> dict[str, Any]:
    top = _object(value, {"schema_version", "apis"}, "$")
    if top["schema_version"] != "3.0":
        raise ValidationError('$.schema_version must equal "3.0"')
    if not isinstance(top["apis"], list):
        raise ValidationError("$.apis must be an array")
    if len(top["apis"]) > MAX_APIS:
        raise ValidationError(f"$.apis exceeds {MAX_APIS} items")
    for index, raw in enumerate(top["apis"]):
        label = f"$.apis[{index}]"
        api = _object(raw, {"url", "method", "parameters", "evidence"}, label)
        normalize_url(_string(api["url"], f"{label}.url"))
        method = _string(api["method"], f"{label}.method", 32)
        if not re.fullmatch(r"[A-Za-z]+", method):
            raise ValidationError(f"{label}.method must contain only ASCII letters")
        if not isinstance(api["parameters"], list) or not isinstance(api["evidence"], list):
            raise ValidationError(f"{label}.parameters and evidence must be arrays")
        for position, raw_parameter in enumerate(api["parameters"]):
            child = f"{label}.parameters[{position}]"
            item = _object(raw_parameter, {"name", "location"}, child)
            _string(item["name"], f"{child}.name", 1024)
            if item["location"] not in LOCATIONS:
                raise ValidationError(f"{child}.location has an unsupported value")
        for position, raw_evidence in enumerate(api["evidence"]):
            child = f"{label}.evidence[{position}]"
            item = _object(raw_evidence, {"type", "source"}, child)
            if item["type"] not in EVIDENCE_TYPES:
                raise ValidationError(f"{child}.type has an unsupported value")
            normalize_url(_string(item["source"], f"{child}.source"))
    return top


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("submission", type=Path)
    args = parser.parse_args()
    value = json.loads(args.submission.read_text(encoding="utf-8"), parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    validate(value)
    print("valid submission v3")


if __name__ == "__main__":
    main()
