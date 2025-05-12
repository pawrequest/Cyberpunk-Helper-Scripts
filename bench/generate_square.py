import json
import math
from pathlib import Path

from PIL import Image

from atlas_gen.generate_inkatlasConformImages import make_both_dims_power_of_two
from atlas_gen.inkatlas_part import InkAtlasClippingRect, InkAtlasClippingRectUV, InkAtlasPart, PartName
from atlas_gen.json_gnerators import empty_atlas_data2

OUTPUT_FOLDER = r"D:\prdev\repos\canada\src\canada\source\raw\canada\images"
INPUT_FOLDER = r"D:\data\cp77\1024"
ATLAS_NAME = "randy"
OUTPUT_FOLDER = Path(OUTPUT_FOLDER)
INPUT_FOLDER = Path(INPUT_FOLDER)
'''
def make_canvas(images: list[Image], grid_size: int, max_width: int, max_height: int, spacing: int) -> tuple[Image, int]:
    orig_size = grid_size * max(max_width, max_height) + (grid_size - 1) * spacing
    canvas = Image.new("RGBA", (orig_size, orig_size), (0, 0, 0, 0))
    x_offset, y_offset = 0, 0
    for i, image in enumerate(images):
        canvas.paste(image, (x_offset, y_offset))
        x_offset += max_width + spacing
        if (i + 1) % grid_size == 0:
            x_offset = 0
            y_offset += max_height + spacing
    return canvas, orig_size


def make_rects(
    images: list[Image], grid_size: int, max_width: int, max_height: int, spacing: int, orig_size: int
) -> list[InkAtlasClippingRectUV]:
    rects = []
    x_offset, y_offset = 0, 0
    for i, _ in enumerate(images, start=1):
        left_uv = x_offset / orig_size
        top_uv = y_offset / orig_size
        right_uv = (x_offset + max_width) / orig_size
        bottom_uv = (y_offset + max_height) / orig_size
        if any([value < 0 or value > 1 for value in [left_uv, top_uv, right_uv, bottom_uv]]):
            ...


        rect = InkAtlasClippingRectUV(Left=left_uv, Top=top_uv, Right=right_uv, Bottom=bottom_uv)
        rects.append(rect)
        x_offset += max_width + spacing
        if i % grid_size == 0:
            x_offset = 0
            y_offset += max_height + spacing
    return rects


def main(spacing: int = 1):
    image_files = [file for file in INPUT_FOLDER.iterdir() if file.suffix == ".png"]
    images = [Image.open(file) for file in image_files]
    grid_size = math.ceil(math.sqrt(len(images)))
    max_width = max(image.width for image in images)
    max_height = max(image.height for image in images)
    layout_canvas, orig_size = make_canvas(images, grid_size, max_width, max_height, spacing)
    final_canvas = make_both_dims_power_of_two(layout_canvas)
    final_canvas.save(OUTPUT_FOLDER / f"{ATLAS_NAME}.png")
    resized = final_canvas.resize((final_canvas.width // 2, final_canvas.height // 2))
    resized.save(OUTPUT_FOLDER / f"{ATLAS_NAME}_1080.png")
    data = empty_atlas_data2(OUTPUT_FOLDER, ATLAS_NAME)
    rects = make_rects(images, grid_size, max_width, max_height, spacing, orig_size)
    parts = []

    for i, rect in enumerate(rects, start=1):
         p_name = PartName(value=f"{ATLAS_NAME}{i:02}")
         part = InkAtlasPart(clippingRectInUVCoords=rect, partName=p_name, clippingRectInPixels=InkAtlasClippingRect.empty())
         parts.append(part)
    parts_json = [_.model_dump(mode="json", by_alias=True) for _ in parts]
    data["Data"]["RootChunk"]["slots"]["Elements"][0]["parts"] = parts_json
    data["Data"]["RootChunk"]["slots"]["Elements"][1]["parts"] = parts_json
    with open(OUTPUT_FOLDER / f"{ATLAS_NAME}.inkatlas.json", "w") as f:
        json.dump(data, f, indent=2)
'''








#
# def array_images_on_square_canvas(images: list[Image], spacing: int = 1) -> Image:
#     num_images = len(images)
#
#     # Calculate the smallest square dimension that can fit all images
#     grid_size = math.ceil(math.sqrt(num_images))  # The number of rows/columns in the square grid
#
#     # Determine the max width and height of the images to arrange them consistently
#     max_width = max(image.width for image in images)
#     max_height = max(image.height for image in images)
#
#     # Create a new blank square canvas large enough to fit all the images
#     canvas_size = grid_size * max(max_width, max_height) + (grid_size - 1) * spacing
#     canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
#
#     # Iterate through the images and paste them on the canvas
#     x_offset, y_offset = 0, 0
#     for i, image in enumerate(images):
#         # Paste the image at the correct offset
#         canvas.paste(image, (x_offset, y_offset))
#
#         # Move the offset to the next position in the grid
#         x_offset += max_width + spacing  # Add the width of the image and the spacing
#
#         # If we reached the end of a row, move to the next row
#         if (i + 1) % grid_size == 0:
#             x_offset = 0
#             y_offset += max_height + spacing  # Move down by the height of the images plus spacing
#
#     return canvas
#
#
# if __name__ == '__main__':
#     image_files = [file for file in INPUT_FOLDER.iterdir() if file.suffix==".png"]
#     images = [Image.open(file) for file in image_files]
#
#     atlas_image = array_images_on_square_canvas(images)
#     atlas_image = make_square(atlas_image)
#     atlas_image = make_both_dims_power_of_two(atlas_image)
#     atlas_image.save(OUTPUT_FOlDER / f"{ATLAS_NAME}.png")
#
#     for i, image in enumerate(images):
#         erct = InkAtlasClippingRectUV(
#
#         )

# Function to create the square canvas and return it
def make_canvas(images, grid_size: int, max_width: int, max_height: int, spacing: int) -> Image:
    # Calculate the canvas size
    canvas_size = grid_size * max(max_width, max_height) + (grid_size - 1) * spacing
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))

    x_offset, y_offset = 0, 0
    for i, image in enumerate(images, start=1):
        canvas.paste(image, (x_offset, y_offset))

        # Move the offset to the next position in the grid
        x_offset += max_width + spacing  # Add the width of the image and the spacing

        # If we reached the end of a row, move to the next row
        if i % grid_size == 0:
            x_offset = 0
            y_offset += max_height + spacing  # Move down by the height of the images plus spacing

    return canvas


# Function to calculate the clipping rectangles as relative percentages of the canvas
def make_parts(
    images: list[Image], grid_size: int, max_width: int, max_height: int, spacing: int, canvas_size: int
) -> list[InkAtlasPart]:
    rects = []
    parts = []
    x_offset, y_offset = 0, 0

    for i, image in enumerate(images, start=1):
        # Calculate relative position as a percentage of the canvas size
        left_percentage = x_offset / canvas_size
        top_percentage = y_offset / canvas_size
        right_percentage = (x_offset + max_width) / canvas_size
        bottom_percentage = (y_offset + max_height) / canvas_size
        if any(
            value < 0 or value > 1 for value in [left_percentage, top_percentage, right_percentage, bottom_percentage]
        ):
            ...

        rect = InkAtlasClippingRect(
            bottom=y_offset + max_height, left=x_offset, right=x_offset + max_width, top=y_offset
        )
        rect_uv = InkAtlasClippingRectUV(
            Left=left_percentage, Top=top_percentage, Right=right_percentage, Bottom=bottom_percentage
        )

        p_name = PartName(value=f"{ATLAS_NAME}{i:02}")

        part = InkAtlasPart(
            clippingRectInPixels=InkAtlasClippingRect.empty(), clippingRectInUVCoords=rect_uv, partName=p_name
        )

        parts.append(part)

        # Move the offset to the next position in the grid
        x_offset += max_width + spacing

        # If we reached the end of a row, move to the next row
        if i % grid_size == 0:
            x_offset = 0
            y_offset += max_height + spacing

    return parts


def main(spacing: int = 1):
    image_files = [file for file in INPUT_FOLDER.iterdir() if file.suffix == ".png"]
    images = [Image.open(file) for file in image_files]
    grid_size = math.ceil(math.sqrt(len(images)))  # The number of rows/columns in the square grid

    max_width = max(image.width for image in images)
    max_height = max(image.height for image in images)

    canvas = make_canvas(images, grid_size, max_width, max_height, spacing)
    canvas = make_both_dims_power_of_two(canvas)
    canvas.save(OUTPUT_FOLDER / f"{ATLAS_NAME}.png")

    resized = canvas.resize((canvas.width // 2, canvas.height // 2))
    resized.save(OUTPUT_FOLDER / f"{ATLAS_NAME}_1080.png")

    data = empty_atlas_data2(OUTPUT_FOLDER, ATLAS_NAME)
    parts = make_parts(images, grid_size, max_width, max_height, spacing, canvas.size[0])
    parts_json = [_.model_dump(mode="json", by_alias=True) for _ in parts]
    data["Data"]["RootChunk"]["slots"]["Elements"][0]["parts"] = parts_json
    data["Data"]["RootChunk"]["slots"]["Elements"][1]["parts"] = parts_json

    with open(OUTPUT_FOLDER / f"{ATLAS_NAME}.inkatlas.json", "w") as f:
        json.dump(data, f, indent=2)





if __name__ == "__main__":
    main()
