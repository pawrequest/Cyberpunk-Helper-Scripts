# many noqa for pydanitc populate_by_name false positive
import json
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from inkatlas import ElementSlots, InkAtlas, InkAtlasData, InkAtlasHeader, RootChunk, WolvenProject
from inkatlas_part import InkAtlasClippingRect, InkAtlasClippingRectUV, InkAtlasPart, PartName
from inkatlas_slot import DepotPath, InkTextureSlot, Texture
from util_types import AtlasDTypes, WolvenPaths

PROJECT_NAME = "canada"
PROJECT_ROOT = r"D:\prdev\repos\canada\src\canada"
IMPORT_IMGS_FROM: str = r'D:\prdev\repos\canada\src\jrme\jrme\source\raw\base\mrbill61\images'
COMBINED_IMAGE_NAME = "randy"
MAX_WIDTH = 2048
FILE_EXT = "png"

'''
NOTES

Working example: JRME

file structure:
jrme /source /  raw / base / mrbill61 / images
    / {image_name}.atlas
        /1080p
            / {image_part_name}.png
        / 2160p
            / {image_part_name}.png
    / {combined_image_name}.png
    / {combined_image_name}.inkatlas.json
'''

@dataclass
class ImageRow:
    images: list[Image.Image] = field(default_factory=list)
    width: int = 0
    height: int = 0

    def add_image(self, image: Image.Image):
        if self.width + image.width + len(self.images) - 1 > MAX_WIDTH - 1:  # -1 in case odd number
            return False
        elif image.width > MAX_WIDTH:
            raise ValueError(f"Image width ({image.width}) exceeds maximum width {MAX_WIDTH}")
        self.images.append(image)
        self.width += image.width
        if len(self.images) > 1:
            self.width += 1
        self.height = max(self.height, image.height)
        return True


# ImageCol = list[ImageRow]


def make_even(new_image):
    if new_image.width % 2 != 0:
        new_image = new_image.crop((0, 0, new_image.width - 1, new_image.height))
    if new_image.height % 2 != 0:
        new_image = new_image.crop((0, 0, new_image.width, new_image.height - 1))
    return new_image


@dataclass
class ImageGrid:
    images: list[Image.Image]
    rows: list[ImageRow] = field(default_factory=list[ImageRow])

    @property
    def width(self):
        return max(row.width for row in self.rows)

    @property
    def height(self):
        return sum(row.height for row in self.rows) + len(self.rows) - 1

    def __post_init__(self):
        self.rows.append(ImageRow())
        for image in self.images:
            self.add_image(image)

    def add_image(self, image: Image.Image):
        this_row = self.rows[-1]
        if not this_row.add_image(image):
            new_row = ImageRow()
            new_row.add_image(image)
            self.rows.append(new_row)

    def combined_image(self):
        y_offset = 0
        new_image = Image.new("RGBA", (self.width, self.height))
        for row in self.rows:
            x_offset = 0
            for image in row.images:
                new_image.paste(image, (x_offset, y_offset))
                x_offset += image.width +1
            y_offset += row.height +1
        new_image = make_even(new_image)
        return new_image


    def combined_json(self):
        y_offset = 0
        for row in self.rows:
            x_offset = 0
            for image in row.images:
                top_pixel = y_offset + (row.height - image.height) // 2
                left_pixel = x_offset
                bottom_pixel = top_pixel + image.height
                right_pixel = left_pixel + image.width

                rect_pc = InkAtlasClippingRect(
                    bottom=bottom_pixel,
                    left=left_pixel,
                    right=right_pixel,
                    top=top_pixel,
                )

                bottom_uv = (top_pixel + image.height) / self.height
                left_uv = left_pixel / self.width
                right_uv = (left_pixel + image.width) / self.width
                top_uv = top_pixel / self.height

                rect_uv = InkAtlasClippingRectUV(
                    Bottom=bottom_uv,
                    Left=left_uv,
                    Right=right_uv,
                    Top=top_uv,
                )

                x_offset += image.width +1
            y_offset += row.height +1
        return new_image



def get_rects(grid):
    rects = []
    on_image = 0
    csr: tuple[int, int] = (0, 0)  # w, h
    for row in grid.rows:
        for image in row.images:
            on_image += 1
            top_px = csr[1]
            left_px = csr[0]
            bot_px = csr[1] + image.height
            right_px = csr[0] + image.width
            rect = InkAtlasClippingRectUV(
                bottom=bot_px / grid.height,  # noqa
                left=left_px / grid.width,  # noqa
                right=right_px / grid.width,  # noqa
                top=top_px / grid.height,  # noqa
            )  # noqa

            rects.append(rect)
            csr = (csr[0] + image.width + 1, csr[1])
        csr = (csr[0], csr[1] + row.height + 1)
    return rects


def get_parts(rects):
    parts = []
    for i, rect in enumerate(rects, start=1):
        part_name = PartName(value=f"{COMBINED_IMAGE_NAME}{i:02d}")
        part = InkAtlasPart(pname=part_name, clipping_rect=InkAtlasClippingRect.empty(), clipping_rect_uv=rect)
        parts.append(part)
    return parts


if __name__ == "__main__":
    w_path = WolvenPaths(roo)
    project = WolvenProject(
        project_name=PROJECT_NAME,
        root_path=Path(PROJECT_ROOT),
    )
    image_dir = project.w_paths.source / project.w_paths.raw.images
    image_dir.mkdir(parents=True, exist_ok=True)
    combined_stem = image_dir / f"{COMBINED_IMAGE_NAME}"
    combined_stem1080 = image_dir / f"{COMBINED_IMAGE_NAME}_1080"

    atlas_json = combined_stem.with_suffix(".inkatlas.json")
    combined_image_file = combined_stem.with_suffix("." + FILE_EXT)
    combined_image_file1080 = combined_stem1080.with_suffix("." + FILE_EXT)
    image_files = [f for f in Path(IMPORT_IMGS_FROM).iterdir() if f.is_file() and f.suffix == f".{FILE_EXT}"]
    arch_name = project.w_paths.build_path("archive", "images") / f"{COMBINED_IMAGE_NAME}.inkatlas"
    grid = ImageGrid(images=[Image.open(_) for _ in image_files])
    rects = get_rects(grid)
    parts = get_parts(rects)
    xbm_str = (project.w_paths.build_path("archive", "images") / COMBINED_IMAGE_NAME).with_suffix(".xbm")
    # xbm_str = project.w_paths.archive.images / f"{COMBINED_IMAGE_NAME}.xbm"
    depotpath = DepotPath(value=xbm_str, storage_dtype=AtlasDTypes.STR)

    headers = InkAtlasHeader(archive_name=arch_name)  # noqa
    texture = Texture(depot=depotpath)
    slot = InkTextureSlot(texture=texture, parts=parts)
    data = InkAtlasData(root_chunk=RootChunk(slots=ElementSlots(elements=[slot, slot])))
    atlas = InkAtlas(header=headers, data=data)

    combined = grid.combined_image()
    atl_data = atlas.model_dump(mode="json", by_alias=True)
    with open(atlas_json, "w") as f:
        json.dump(atl_data, f, indent=2)

    with open(combined_image_file, "wb") as f:
        combined.save(f, FILE_EXT.upper())

    resized_image = combined.resize(
        (combined.width // 2, combined.height // 2), resample=None, box=None, reducing_gap=None
    )
    resized_image = make_even(resized_image)

    with open(combined_image_file1080, "wb") as f:
        resized_image.save(f, FILE_EXT.upper())

    ...

"""
has slices:
elements/inktextureslot
rootchunk

"""

# from pathlib import Path
#
# from inkatlas import RootChunk, ElementSlots, InkAtlas, InkAtlasHeader, InkAtlasData
# from inkatlas_part import PartName, InkAtlasClippingRect, InkAtlasClippingRectUV, InkAtlasPart
# from inkatlas_slot import InkTextureSlot, Texture
#
# if __name__ == '__main__':
#     archivename = "randy"
#     location = Path()
#
#     pname = PartName(value=f'{archivename}01')
#
#     rect = InkAtlasClippingRect(bottom=1000, left=0, right=1000, top=0)
#     rect_uv = InkAtlasClippingRectUV(bottom=1.0, left=0, right=1.0, top=0)
#
#     part = InkAtlasPart(clipping_rect=rect, clipping_rect_uv=rect_uv, pname=pname)
#
#     pathstr = "\\prdev\\images\\randy.xbm"
#     slot = InkTextureSlot(
#         parts=[part],
#         texture= Texture.from_path_str(pathstr)
#     )
#     root_chunk = RootChunk(
#         slots=ElementSlots(elements=[slot])
#     )
#     atlas = InkAtlas(
#         header=InkAtlasHeader(archive_name="randy"),
#         data=InkAtlasData(
#             root_chunk=root_chunk
#         )
#     )
