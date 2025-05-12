import math
import json
from pathlib import Path
from typing import List

from PIL import Image
from pydantic import BaseModel, Field

from generate_inkatlasConformImages import make_both_dims_power_of_two
from inkatlas_part import InkAtlasPart, InkAtlasClippingRectUV, PartName, InkAtlasClippingRect
from json_gnerators import empty_atlas_data2, empty_slot

OUTPUT_FOLDER = r"C:\prdev\mod\Cyberpunk-Helper-Scripts\data"
INPUT_FOLDER = r"D:\data\cp77\1024"
ATLAS_NAME = "randy"
OUTPUT_FOLDER = Path(OUTPUT_FOLDER)
INPUT_FOLDER = Path(INPUT_FOLDER)


class AtlasLayout:
    def __init__(self, images: List[Image.Image], spacing: int):
        self.images = images
        self.spacing = spacing
        self.num_images = len(images)
        self.grid_size = math.ceil(math.sqrt(self.num_images))
        self.max_width = max(image.width for image in images)
        self.max_height = max(image.height for image in images)
        self.orig_canvas_size = self.grid_size * max(self.max_width, self.max_height) + (self.grid_size - 1) * spacing
        self.final_canvas_size = None


def make_canvas_from_layout(layout: AtlasLayout) -> Image.Image:
    canvas = Image.new("RGBA", (layout.orig_canvas_size, layout.orig_canvas_size), (0, 0, 0, 0))
    x_offset, y_offset = 0, 0
    for i, image in enumerate(layout.images):
        canvas.paste(image, (x_offset, y_offset))
        x_offset += layout.max_width + layout.spacing
        if (i + 1) % layout.grid_size == 0:
            x_offset = 0
            y_offset += layout.max_height + layout.spacing
    return canvas


def make_parts_from_layout(layout: AtlasLayout, atlas_name:str) -> List[InkAtlasPart]:
    parts = []
    x_offset, y_offset = 0, 0
    for i, _ in enumerate(layout.images, start=1):
        left_uv = x_offset / layout.final_canvas_size
        top_uv = y_offset / layout.final_canvas_size
        right_uv = (x_offset + layout.max_width) / layout.final_canvas_size
        bottom_uv = (y_offset + layout.max_height) / layout.final_canvas_size
        left_uv = min(max(left_uv, 0.0), 1.0)
        top_uv = min(max(top_uv, 0.0), 1.0)
        right_uv = min(max(right_uv, 0.0), 1.0)
        bottom_uv = min(max(bottom_uv, 0.0), 1.0)
        rect_uv = InkAtlasClippingRectUV(Left=left_uv, Top=top_uv, Right=right_uv, Bottom=bottom_uv)
        p_name = PartName(value=f"{atlas_name}{i:02}")
        part = InkAtlasPart(clippingRectInPixels=InkAtlasClippingRect.empty(), clippingRectInUVCoords=rect_uv, partName=p_name)
        parts.append(part)
        x_offset += layout.max_width + layout.spacing
        if i % layout.grid_size == 0:
            x_offset = 0
            y_offset += layout.max_height + layout.spacing
    return parts


def generate_inkatlas(*, spacing: int = 1, in_dir:Path=INPUT_FOLDER, out_dir=OUTPUT_FOLDER, atlas_name = ATLAS_NAME):
    image_files = [file for file in in_dir.iterdir() if file.suffix == ".png"]
    images = [Image.open(file) for file in image_files]
    layout = AtlasLayout(images, spacing)
    layout_canvas = make_canvas_from_layout(layout)
    final_canvas = make_both_dims_power_of_two(layout_canvas)
    layout.final_canvas_size = final_canvas.size[0]
    final_canvas.save(out_dir / f"{atlas_name}.png")
    resized = final_canvas.resize((final_canvas.width // 2, final_canvas.height // 2))
    resized.save(out_dir / f"{atlas_name}_1080.png")
    data = empty_atlas_data2(out_dir, atlas_name)
    parts = make_parts_from_layout(layout, atlas_name)
    parts_json = [part.model_dump(mode="json", by_alias=True) for part in parts]
    data["Data"]["RootChunk"]["slots"]["Elements"][0]["parts"] = parts_json
    data["Data"]["RootChunk"]["slots"]["Elements"][1]["parts"] = parts_json
    with open(out_dir / f"{atlas_name}.inkatlas.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    generate_inkatlas()
