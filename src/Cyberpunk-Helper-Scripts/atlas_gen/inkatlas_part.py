from pydantic import Field

from util_types import AtlasBase


class InkAtlasClippingRect(AtlasBase):
    type: str = Field(default="Rect", alias="$type")
    bottom: int = Field(...)
    left: int = Field(...)
    right: int = Field(...)
    top: int = Field(...)

    @classmethod
    def empty(cls):
        return cls(bottom=0, left=0, right=0, top=0) # noqa pydanitc populate_by_name false positive


class InkAtlasClippingRectUV(AtlasBase):
    type: str = Field(default="RectF", alias="$type")
    bottom: float = Field(..., alias="Bottom")
    left: float = Field(..., alias="Left")
    right: float = Field(..., alias="Right")
    top: float = Field(..., alias="Top")


class PartName(AtlasBase):
    type: str = Field(default="CName", alias="$type")
    storage: str = Field(default="string", alias="$storage")
    value: str = Field(..., alias="$value")


class InkAtlasPart(AtlasBase):
    type: str = Field(default="inkTextureAtlasMapper", alias="$type")
    clipping_rect: InkAtlasClippingRect = Field(..., alias="clippingRectInPixels")
    clipping_rect_uv: InkAtlasClippingRectUV = Field(..., alias="clippingRectInUVCoords")
    pname: PartName = Field(alias="partName")
