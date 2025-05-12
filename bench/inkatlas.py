from datetime import datetime
from pathlib import Path

from pydantic import Field, model_validator

from inkatlas_slot import InkTextureSlot
from util_types import (
    AtlasBase,
    AtlasConstants,
    CookingTypes,
    WolvenPaths,
    dynamic_texture_slot,
    empty_texture_int,
)


class InkAtlasHeader(AtlasBase):
    wolven_v: str = Field(default=AtlasConstants.wolven_version, alias="WolvenKitVersion")
    json_v: str = Field(default=AtlasConstants.json_version, alias="WKitJsonVersion")
    game_version: int = Field(default=AtlasConstants.game_version, alias="GameVersion")
    exported_dt: str = Field(default_factory=datetime.now().isoformat, alias="ExportedDateTime")
    data_type: str = Field(default=AtlasConstants.data_type, alias="DataType")
    archive_name: Path = Field(..., alias="ArchiveFileName")
    # archive_name: AtlasPath = Field(..., alias="ArchiveFileName")


class ElementSlots(AtlasBase):
    elements: list[InkTextureSlot] = Field(..., alias="Elements")

    @model_validator(mode="after")
    def get_elements(self):
        for i in range(3 - len(self.elements)):
            self.elements.append(InkTextureSlot.empty())
        return self


class RootChunk(AtlasBase):
    type: str = Field(default=AtlasConstants.ink_type, alias="$type")
    active_texture: str = Field(default=AtlasConstants.static_texture_type, alias="activeTexture")
    cooking_platform: str = Field(default=CookingTypes.PC, alias="cookingPlatform")
    dynamic_texture: dict = Field(default_factory=empty_texture_int, alias="dynamicTexture")
    dynamic_texture_slot: dict = Field(default_factory=dynamic_texture_slot, alias="dynamicTextureSlot")
    is_single_texture_mode: int = Field(default=AtlasConstants.single_texture_mode, alias="isSingleTextureMode")
    parts: list = Field(default_factory=list)
    slices: list = Field(default_factory=list)
    slots: ElementSlots
    texture: dict = Field(default_factory=empty_texture_int)
    texture_res: str = Field(default=AtlasConstants.res_4k_ultra, alias="textureResolution")


class InkAtlasData(AtlasBase):
    version: int = Field(default=AtlasConstants.data_version, alias="Version")
    build_version: int = Field(default=AtlasConstants.build_version, alias="BuildVersion")
    root_chunk: RootChunk = Field(..., alias="RootChunk")
    embedded_files: list = Field(default_factory=list, alias="EmbeddedFiles")


class InkAtlas(AtlasBase):
    header: InkAtlasHeader = Field(alias="Header")
    data: InkAtlasData = Field(..., alias="Data")


# class AtlasImages(AtlasBase):
#     combined_image_name: str
#
#     atlas_json_name: str = None
#     atlas_filename: str = None
#     xbm_filename: str = None
#
#     @model_validator(mode="after")
#     def get_paths(self):
#         self.atlas_filename = f"{self.combined_image_name}.inkatlas"
#         self.atlas_json_name = f"{self.combined_image_name}.inkatlas.json"
#         self.xbm_filename = f"{self.combined_image_name}.xbm"
#
#         return self


class WolvenProject(AtlasBase):
    project_name: str = "testing"
    root_path: Path = Path(r"D:\prdev\repos\canada\tests\wolven")
    w_paths: WolvenPaths = None

    @model_validator(mode="after")
    def get_paths(self):
        self.w_paths = WolvenPaths(project_name=self.project_name, wolven_root=self.root_path)
        return self


# class ImageCombiner(AtlasBase):
#     project: WolvenProject
#     combined_image_name: str
#     pngs: list[Path]
#
#     atlas_images: AtlasImages = None
#
#     @model_validator(mode="after")
#     def get_atl_images(self):
#         self.atlas_images = AtlasImages(combined_image_name=self.combined_image_name)
#         return self
