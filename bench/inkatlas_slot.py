from pathlib import Path
from typing import Literal

from pydantic import Field

from atlas_gen.inkatlas_part import InkAtlasPart
from atlas_gen.util_types import AtlasBase, AtlasConstants, AtlasDTypes, AtlasFlags


class DepotPath(AtlasBase):
    type: Literal["ResourcePath"] = Field(default=AtlasConstants.resource_path, alias="$type")
    storage_dtype: AtlasDTypes = Field(..., alias="$storage")
    value: Path | int = Field(..., alias="$value")

    # storage: AtlasDTypes = Field(default=AtlasDTypes.STR, alias='$storage')


class Texture(AtlasBase):
    depot: DepotPath = Field(..., alias="DepotPath")
    flags: str = Field(default=AtlasFlags.SOFT, alias='Flags')


class InkTextureSlot(AtlasBase):
    type: Literal["inkTextureSlot"] = Field(default="inkTextureSlot", alias="$type")
    parts: list[InkAtlasPart]
    texture: Texture
    slices: list = Field(default_factory=list)

    @classmethod
    def empty(cls):
        return cls(
            parts=[],
            texture=Texture(
                depot=DepotPath(
                    storage_dtype=AtlasDTypes.UINT64,
                    value=0
                )
        )
        )
