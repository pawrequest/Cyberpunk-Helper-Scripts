import math
import os
import re
import json
from typing import Literal

from PIL import Image, ImageOps

OUTPUT_FOlDER = r"D:\prdev\repos\canada\src\canada\source\raw\canada\images"
INPUT_FOLDER = r"D:\data\cp77\1024"
ATLAS_NAME = "randy"


def make_square(image: Image) -> Image:
    if image.width != image.height:
        size = max(image.width, image.height)
        new_image = Image.new(image.mode, (size, size), (0, 0, 0, 0))
        x_offset = (size - image.width) // 2
        y_offset = (size - image.height) // 2
        new_image.paste(image, (x_offset, y_offset))
        print("WARNING: Image not square, padding with transparency")
        return new_image
    return image


# def make_square(image: Image) -> Image:
#     if image.width == image.height:
#         return image
#     else:
#         size = max(image.width, image.height)
#         # Create a new blank canvas with the original image mode
#         new_image = Image.new(image.mode, (size, size), (0, 0, 0, 0))
#         # Calculate offsets to center the image
#         x_offset = (size - image.width) // 2
#         y_offset = (size - image.height) // 2
#         new_image.paste(image, (x_offset, y_offset))
#         print("WARNING: Image not square, padding with transparency")
#         return new_image


def make_both_dims_power_of_two(image: Image, threshold=10, resize:Literal['up', 'down']='up') -> Image:
    if not image.width == image.height:
        raise ValueError("Image dimensions are not equal")
    dim_size = image.width

    def next_power_of_two(n: int) -> int:
        return n if (n & (n - 1)) == 0 else 2 ** n.bit_length()

    def previous_power_of_two(n: int) -> int:
        # Find the previous power of two
        return 2 ** (n.bit_length() - 1)

    # def next_power_of_two(n: int) -> int:
    #     return n if (n & (n - 1)) == 0 else 2 ** n.bit_length()
    #
    # def previous_power_of_two(n: int) -> int:
    #     return 2 ** (n - 1).bit_length()

    next_po2 = next_power_of_two(dim_size)
    prev_po2 = previous_power_of_two(dim_size)
    if not any([dim_size == next_po2, dim_size == prev_po2]):
        print("WARNING: Image dimensions are not powers of two")

    dist_prev_po2 = dim_size - prev_po2
    dist_next_po2 = next_po2 - dim_size
    print(f"image_dim: {dim_size}, prev_po2: {prev_po2}, next_po2: {next_po2}, dist_prev_po2: {dist_prev_po2}, dist_next_po2: {dist_next_po2}")
    if dist_prev_po2 <= threshold:
        print(f"image is {dist_prev_po2} above previous power of two ({prev_po2}) - cropping")
        return image.crop((0, 0, prev_po2, prev_po2), )
    elif dist_next_po2 <= threshold:
        print(f"image is {dist_next_po2} below next power of two ({next_po2} - padding")
        return ImageOps.pad(image, (next_po2, next_po2), color=(0, 0, 0), centering=(0.5, 0.5))

    else:
        print(f"image is not close to next or previous power of two, resizing {resize} to {next_po2 if resize == 'up' else prev_po2}")
        if resize == 'up':
            return image.resize((next_po2, next_po2))
        elif resize == 'down':
            return image.resize((prev_po2, prev_po2))


    # def make_both_dims_power_of_two(image: Image, threshold=1) -> Image:
    #     width, height = image.width, image.height
    #
    #     def next_power_of_two(n: int) -> int:
    #         return n if (n & (n - 1)) == 0 else 2 ** n.bit_length()
    #
    #     new_width = next_power_of_two(width)
    #     new_height = next_power_of_two(height)
    #
    #     # Check if dimensions are very close to the next power of two
    #     if abs(new_width - width) <= threshold:
    #         new_width = width  # No resize needed
    #     if abs(new_height - height) <= threshold:
    #         new_height = height  # No resize needed
    #
    #     # If dimensions are not already powers of two
    #     if new_width != width or new_height != height:
    #         print("WARNING: Image dimensions are not powers of two, padding/cropping")
    #
    #         # If dimensions need to be increased, pad; if they need to be decreased, crop
    #         if new_width > width or new_height > height:
    #             return image.resize((new_width, new_height))
    #         else:
    #             return image.crop((0, 0, new_width, new_height))  # Crop if over the threshold
    #
    return image


# def make_both_dims_power_of_two(image: Image) -> Image:
#     width, height = image.width, image.height
#
#     def next_power_of_two(n: int) -> int:
#         return n if (n & (n - 1)) == 0 else 2 ** n.bit_length()
#
#     new_width = next_power_of_two(width)
#     new_height = next_power_of_two(height)
#
#     if new_width != width or new_height != height:
#         print("WARNING: Image dimensions are not powers of two, resizing")
#         return image.resize((new_width, new_height))
#     return image

# def make_both_dims_power_of_two(image: Image) -> Image:
#     width, height = image.width, image.height
#
#     # Compute next powers of two
#     new_width = 2 ** (width - 1).bit_length()
#     new_height = 2 ** (height - 1).bit_length()
#
#     # Pad only if aspect ratio will be affected
#     if (width != new_width or height != new_height) and (width / height != new_width / new_height):
#         print("WARNING: Image dimensions are not powers of two, padding to maintain aspect ratio")
#         target_size = (new_width, new_height)
#         padded_image = ImageOps.pad(image, target_size, color=(0, 0, 0))
#         return padded_image
#
#     return image
#

# def make_both_dims_power_of_two(image: Image):
#     width = image.width
#     height = image.height
#
#     new_width = 2 ** (width - 1).bit_length()
#     new_height = 2 ** (height - 1).bit_length()
#
#     if new_width != width or new_height != height:
#         print("WARNING: Image dimensions are not powers of two, resizing")
#         return image.resize((new_width, new_height))
#     return image

# def make_square(image: Image):
#     if not image.width == image.height:
#         size = max(image.width, image.height)
#         new_image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
#         new_image.paste(image, (0, 0))
#         print("WARNING imaage not square, resizing, aspect ratio may be affected")
#         return new_image
#     return image



def main():
    while True:
        icon_folder = INPUT_FOLDER
        # Check for quotes which will break the input path
        if (icon_folder.startswith('"') or icon_folder.startswith("'")) and (
            icon_folder.endswith('"') or icon_folder.endswith("'")
        ):
            # Remove the quotes
            icon_folder = icon_folder[1:-1]
        if icon_folder.endswith("\\"):
            icon_folder = icon_folder[-1]

        files_in_folder = os.listdir(icon_folder)

        # Check if the icon folder contains at least one .png file
        png_files = [file for file in files_in_folder if file.endswith(".png")]

        break  # Exit the loop if the folder contains at least one .png file

    output_folder = OUTPUT_FOlDER

    # Check for quotes which will break the input path
    if (output_folder.startswith('"') or output_folder.startswith("'")) and (
        output_folder.endswith('"') or output_folder.endswith("'") or output_folder.endswith("\\")
    ):
        # Remove the quotes
        output_folder = output_folder[1:-1]

    if output_folder.endswith("source"):
        output_folder = os.path.join(output_folder, "raw")
    elif "\\archive" in output_folder:
        output_folder = output_folder.replace("\\archive", "\\raw")

    if "raw" not in output_folder:
        raise ValueError("The output folder must contain a 'raw' folder")

    atlas_name = ATLAS_NAME

    # Load each image to get its dimensions
    images = []
    for png_file in png_files:
        image_path = os.path.join(icon_folder, png_file)
        try:
            img = Image.open(image_path)
            images.append({"path": image_path, "image": img, "name": os.path.splitext(png_file)[0]})
        except Exception as e:
            print("INKATLAS GENERATOR ERROR: ")
            print("-----------------------------------------------------------------------------------------------")
            print("")
            print(f"     Error opening image {png_file}: {e}")
            print("")
            print("-----------------------------------------------------------------------------------------------")
            print("")

    # Calculate the maximum width of the combined image
    max_width = 2048

    # Initialize variables
    grid = []
    current_row = []
    current_width = 0
    max_height_in_row = 0

    # Iterate through each image
    for image_data in images:
        img = image_data["image"]
        width = img.width
        height = img.height

        # Check if adding the current image exceeds the maximum width
        if current_width + width <= max_width:
            # Add the image to the current row
            current_row.append(image_data)
            current_width += width
            if len(current_row) > 1:
                current_width += 1  # Add 1 pixel spacing between images

            max_height_in_row = max(max_height_in_row, height)
        else:
            # Add the current row to the grid and start a new row
            grid.append(current_row)
            current_row = [image_data]
            current_width = width  # Add 1 pixel spacing between images
            if len(current_row) > 1:
                current_width += 1

            max_height_in_row = height

    # Add the last row to the grid
    if current_row:
        grid.append(current_row)

    # Calculate the total height of the combined image
    total_height = (
        sum(max(image_data["image"].height for image_data in row) for row in grid) + len(grid) - 1
    )  # Add spacing between rows

    # Ensure total height is an even number
    total_height += total_height % 2

    total_width = 0
    for row in grid:
        row_width = (
            sum(image_data["image"].width for image_data in row) + len(row) - 1
        )  # Calculate the total width of images in the current row
        total_width = max(total_width, row_width)  # Update the total width if the current row width is greater

    # Ensure total width does not exceed the maximum width
    total_width = min(total_width, max_width)

    # Ensure total width is an even number
    total_width += total_width % 2

    # Create a blank canvas to paste images onto
    combined_image = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))
    raw_index = re.sub(r".*?" + re.escape("raw"), "", output_folder, 1)
    if raw_index is not None:
        atlas_xbm = os.path.join(raw_index, atlas_name + ".xbm")
        atlas_xbm_1080 = atlas_xbm.replace(".xbm", "_1080.xbm")
    # JSON data
    data = {
        "Header": {
            "WolvenKitVersion": "8.13.0-nightly.2024-03-17",
            "WKitJsonVersion": "0.0.8",
            "GameVersion": 2120,
            "ExportedDateTime": "2024-03-18T04:38:07.1672443Z",
            "DataType": "CR2W",
            "ArchiveFileName": "",
        },
        "Data": {
            "Version": 195,
            "BuildVersion": 0,
            "RootChunk": {
                "$type": "inkTextureAtlas",
                "activeTexture": "StaticTexture",
                "cookingPlatform": "PLATFORM_None",
                "dynamicTexture": {
                    "DepotPath": {"$type": "ResourcePath", "$storage": "uint64", "$value": "0"},
                    "Flags": "Default",
                },
                "dynamicTextureSlot": {
                    "$type": "inkDynamicTextureSlot",
                    "parts": [],
                    "texture": {
                        "DepotPath": {"$type": "ResourcePath", "$storage": "uint64", "$value": "0"},
                        "Flags": "Default",
                    },
                },
                "isSingleTextureMode": 1,
                "parts": [],
                "slices": [],
                "slots": {
                    "Elements": [
                        {
                            "$type": "inkTextureSlot",
                            "parts": [],
                            "slices": [],
                            "texture": {
                                "DepotPath": {
                                    "$type": "ResourcePath",
                                    "$storage": "string",
                                    "$value": (f"{atlas_xbm}"),
                                },
                                "Flags": "Soft",
                            },
                        },
                        {
                            "$type": "inkTextureSlot",
                            "parts": [],
                            "slices": [],
                            "texture": {
                                "DepotPath": {
                                    "$type": "ResourcePath",
                                    "$storage": "string",
                                    "$value": (f"{atlas_xbm_1080}"),
                                },
                                "Flags": "Soft",
                            },
                        },
                    ]
                },
                "texture": {
                    "DepotPath": {"$type": "ResourcePath", "$storage": "string", "$value": ""},
                    "Flags": "Default",
                },
                "textureResolution": "UltraHD_3840_2160",
            },
            "EmbeddedFiles": [],
        },
    }

    # Paste each image onto the canvas and add its data to the JSON
    current_y = 0
    for row in grid:
        max_height_in_row = max(image_data["image"].height for image_data in row)
        current_x = 0
        for image_data in row:
            img = image_data["image"]
            name = image_data["name"]
            width = img.width
            height = img.height

            top_pixel = current_y + (max_height_in_row - height) // 2
            left_pixel = current_x

            combined_image.paste(img, (left_pixel, top_pixel))

            if len(row) > 1:
                current_x += width + 1  # Add 1 pixel spacing between images IF MULTIPLE IMAGES IN ROW

            # Add image data to JSON
            part_data = {
                "$type": "inkTextureAtlasMapper",
                "clippingRectInPixels": {
                    "$type": "Rect",
                    "bottom": top_pixel + height,
                    "left": left_pixel,
                    "right": left_pixel + width,
                    "top": top_pixel,
                },
                "clippingRectInUVCoords": {
                    "$type": "RectF",
                    "Bottom": (top_pixel + height) / total_height,
                    "Left": left_pixel / total_width,
                    "Right": (left_pixel + width) / total_width,
                    "Top": top_pixel / total_height,
                },
                "partName": {"$type": "CName", "$storage": "string", "$value": name},
            }

            # Append part data to parts array
            data["Data"]["RootChunk"]["slots"]["Elements"][0]["parts"].append(part_data)
            data["Data"]["RootChunk"]["slots"]["Elements"][1]["parts"].append(part_data)

        if len(grid) > 1:
            current_y += max_height_in_row + 1  # Add 1 pixel spacing between rows IF MULTIPLE ROWS

    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Set the output file name
    output_file = os.path.join(output_folder, atlas_name + ".inkatlas.json")

    # Write everything to the .inkatlas.json
    with open(output_file, "w") as json_file:
        json.dump(data, json_file, indent=2)

    print(f"Data has been saved to {output_file}")

    # Save the combined image
    combined_image_path = os.path.join(output_folder, atlas_name + ".png")
    combined_image = make_square(combined_image)
    combined_image = make_both_dims_power_of_two(combined_image)
    combined_image.save(combined_image_path)
    print(f"Combined image has been saved to {combined_image_path}")
    # Save the resized image with "_1080" suffix
    resized_image = combined_image.resize(
        (total_width // 2, total_height // 2), resample=None, box=None, reducing_gap=None
    )
    resized_image = make_square(resized_image)
    resized_image = make_both_dims_power_of_two(resized_image)

    combined_image_path_1080 = combined_image_path.replace(".png", "_1080.png")
    resized_image.save(combined_image_path_1080)
    print(f"Combined image has been saved to {combined_image_path_1080}")


if __name__ == "__main__":
    main()
