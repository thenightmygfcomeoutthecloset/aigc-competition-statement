#!/usr/bin/env python3
"""Vendor-neutral image-generation execution boundary."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from PIL import Image, UnidentifiedImageError


class GenerationBackendUnavailable(RuntimeError):
    status = "generation_backend_unavailable"


class GenerationExecutionError(RuntimeError):
    pass


class ImageGenerationBackend(Protocol):
    name: str
    mode: str
    model: str

    def execute(self, request: dict[str, Any], output_path: Path) -> dict[str, Any]: ...


@dataclass
class UnavailableBackend:
    name: str = "unavailable"
    mode: str = "delegated"
    model: str = "unavailable"

    def execute(self, request: dict[str, Any], output_path: Path) -> dict[str, Any]:
        raise GenerationBackendUnavailable(
            "generation_backend_unavailable: configure AIGC_IMAGE_GENERATION_COMMAND "
            "or pass an ImageGenerationBackend from the host Agent"
        )


@dataclass
class SubprocessBackend:
    """Adapter for a real provider wrapper that reads request JSON on stdin."""

    command: list[str]
    name: str = "external_generation_command"
    mode: str = "image_to_image"
    model: str = "provider-reported"

    def execute(self, request: dict[str, Any], output_path: Path) -> dict[str, Any]:
        environment = os.environ.copy()
        environment["AIGC_OUTPUT_PATH"] = str(output_path)
        process = subprocess.run(
            self.command,
            input=json.dumps(request, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            env=environment,
            check=False,
        )
        if process.returncode != 0:
            raise GenerationExecutionError(
                f"Generation backend exited with {process.returncode}: {process.stderr.strip()}"
            )
        metadata: dict[str, Any] = {}
        if process.stdout.strip():
            try:
                parsed = json.loads(process.stdout)
                if isinstance(parsed, dict):
                    metadata = parsed
            except json.JSONDecodeError as exc:
                raise GenerationExecutionError("Generation backend stdout must be a JSON object") from exc
        return metadata


def resolve_backend(backend: ImageGenerationBackend | None = None) -> ImageGenerationBackend:
    if backend is not None:
        return backend
    command = os.environ.get("AIGC_IMAGE_GENERATION_COMMAND", "").strip()
    if not command:
        return UnavailableBackend()
    try:
        parsed_command = json.loads(command) if command.startswith("[") else shlex.split(command, posix=os.name != "nt")
    except (json.JSONDecodeError, ValueError) as exc:
        raise GenerationBackendUnavailable("generation_backend_unavailable: invalid AIGC_IMAGE_GENERATION_COMMAND") from exc
    if not isinstance(parsed_command, list) or not parsed_command or not all(isinstance(item, str) and item for item in parsed_command):
        raise GenerationBackendUnavailable("generation_backend_unavailable: command must be a non-empty argv list")
    return SubprocessBackend(
        command=parsed_command,
        name=os.environ.get("AIGC_IMAGE_GENERATION_BACKEND", "external_generation_command"),
        mode=os.environ.get("AIGC_IMAGE_GENERATION_MODE", "image_to_image"),
        model=os.environ.get("AIGC_IMAGE_GENERATION_MODEL", "provider-reported"),
    )


def _verify_complete_image(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.stat().st_size == 0:
        raise GenerationExecutionError(f"Backend did not create an image: {path}")
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            width, height = image.size
            mode = image.mode
    except (OSError, UnidentifiedImageError) as exc:
        raise GenerationExecutionError(f"Backend output cannot be decoded: {path}") from exc
    if width < 64 or height < 64:
        raise GenerationExecutionError(f"Backend output is too small to be a complete artwork: {width}x{height}")
    return {"width": width, "height": height, "image_mode": mode, "complete_artwork": True}


def generate_image(
    prompt: str,
    input_images: list[str],
    parameters: dict[str, Any],
    output_path: str,
    stage_id: str,
    backend: ImageGenerationBackend | None,
) -> dict[str, Any]:
    """Execute one real generation request and verify its complete-image output."""
    resolved = resolve_backend(backend)
    if not prompt.strip():
        raise ValueError("Generation prompt must exist before execution")
    if resolved.name in {"opencv_filter", "deterministic_visual_study", "local_filter"}:
        raise GenerationExecutionError("Traditional image filters cannot be generation backends")
    missing = [path for path in input_images if not Path(path).is_file()]
    if missing:
        raise GenerationExecutionError(f"Generation input images are missing: {missing}")
    request = {
        "stage_id": stage_id,
        "backend": resolved.name,
        "mode": resolved.mode,
        "model": resolved.model,
        "prompt": prompt,
        "negative_prompt": str(parameters.get("negative_prompt", "")),
        "parameters": parameters,
        "input_images": input_images,
        "output_path": output_path,
        "output_contract": "complete_artwork_version",
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    backend_metadata = resolved.execute(request, output)
    image_metadata = _verify_complete_image(output)
    return {**request, **image_metadata, "backend_metadata": backend_metadata}
