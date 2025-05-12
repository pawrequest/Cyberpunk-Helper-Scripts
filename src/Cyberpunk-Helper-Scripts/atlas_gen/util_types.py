from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from typing_extensions import Literal
from pydantic import BaseModel, ConfigDict

ArchiveOrRaw = Literal["archive", "raw"]


class AtlasBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    # class Config:
    #     allow_population_by_field_name = True


def cp_path_str(p: Path):
    return str(f"\\{p}").replace("/", "\\")


# AtlasPath = Annotated[Path, PlainSerializer(cp_path_str)]


class CookingTypes(StrEnum):
    PC = "PLATFORM_PC"
    NONE = 'PLATFORM_None"'


@dataclass
class AtlasConstants:
    wolven_version: str = "8.16.0"
    json_version: str = "0.0.9"
    game_version: int = 2200
    data_type: str = "CR2W"
    single_texture_mode: int = 1
    ink_type: str = "inkTextureAtlas"
    static_texture_type: str = "StaticTexture"
    res_4k_ultra: str = "UltraHD_3840_2160"
    data_version: int = 195
    build_version: int = 0
    resource_path: str = "ResourcePath"


class AtlasFlags(StrEnum):
    SOFT = "Soft"
    DEFAULT = "Default"


class AtlasDTypes(StrEnum):
    STR = "string"
    UINT64 = "uint64"


@dataclass
class ResourcePaths:
    project_name: str
    rs_scripts: Path = None

    def __post_init__(self):
        self.rs_scripts = Path("resources") / self.project_name / "scripts"


@dataclass
class SubPaths:
    project_name: str
    arch_or_raw: ArchiveOrRaw
    images: Path = None

    def __post_init__(self):
        self.images = Path(self.arch_or_raw) / self.project_name / "images"


@dataclass
class WolvenPaths:
    wolven_root: Path
    project_name: str

    project_root: Path = None
    source: Path = None
    sounds: Path = None
    scripts: Path = None

    archive: SubPaths = None
    raw: SubPaths = None
    resource: ResourcePaths = None

    def build_path(self, arch_or_raw: ArchiveOrRaw, s: str):
        return self.source / arch_or_raw / self.project_name / s

    def __post_init__(self):
        self.project_root = self.wolven_root / self.project_name
        self.source = self.project_root / "source"
        self.sounds = self.source / "customSounds"

        self.archive = SubPaths(project_name=self.project_name, arch_or_raw="archive")
        self.raw = SubPaths(project_name=self.project_name, arch_or_raw="raw")
        self.resource = ResourcePaths(project_name=self.project_name)
        self.scripts = self.resource.rs_scripts

    def get_image_path(self, arch_or_raw: ArchiveOrRaw, s: str):
        return self.project_root / getattr(self, arch_or_raw).images / s


def empty_texture_str():
    return {"DepotPath": {"$type": "ResourcePath", "$storage": "string", "$value": ""}, "Flags": "Soft"}


def empty_texture_int():
    return {"DepotPath": {"$type": "ResourcePath", "$storage": AtlasDTypes.UINT64, "$value": 0}, "Flags": "Soft"}


def dynamic_texture_slot():
    return {
        "$type": "inkDynamicTextureSlot",
        "parts": [],
        "texture": empty_texture_int(),
    }
