from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from atlas_gen.inkatlas_builder import ImageGrid
from atlas_gen.json_gnerators import empty_atlas_data, empty_atlas_data2

MAX_W = 2048

OUTPUT_FOlDER = r"D:\prdev\repos\canada\src\canada\source\raw\canada\images"
INPUT_FOLDER = r"D:\data\cp77\2025-01-29\a\2\rs"
ATLAS_NAME = "randy"

INPUT_IMAGE_EXT = ".png"

INPUT_FOLDER = Path(INPUT_FOLDER)
OUTPUT_FOlDER = Path(OUTPUT_FOlDER)


if not OUTPUT_FOlDER.exists():
    OUTPUT_FOlDER.mkdir(parents=True)

if not INPUT_FOLDER.exists():
    raise FileNotFoundError(f"Input folder not found: {INPUT_FOLDER}")


@dataclass
class ImageDict:
    name: str
    path: Path
    image: Image


def check_output_folder(output_folder: Path) -> Path:
    if output_folder.name == "source":
        output_folder = output_folder / "raw"
    elif "archive" in output_folder.parts:
        output_folder = Path(*[part if part != "archive" else "raw" for part in output_folder.parts])
    if not output_folder.exists():
        output_folder.mkdir(parents=True)
    return output_folder


def main():
    print("INKATLAS GENERATOR INPUT: ")
    image_files = [file for file in (INPUT_FOLDER.iterdir()) if file.endswith(INPUT_IMAGE_EXT)]
    output_folder = check_output_folder(OUTPUT_FOlDER)
    output_folder_relative = Path(output_folder.as_posix().split("/raw", 1)[-1])
    data = empty_atlas_data2(output_folder_relative, ATLAS_NAME)


    image_dicts = [ImageDict(name=Path(file).stem, path=Path(file), image=Image.open(file)) for file in image_files]
    # images = [Image.open(_) for _ in png_files]

    gridPR = ImageGrid([_.image for _ in image_dicts])

    # Initialize variables
    gridOG = []


    # Paste each image onto the canvas and add its data to the JSON
    current_y = 0
    for row in gridOG:
        max_height_in_row = max(image_data["image"].height for image_data in row)
        current_x = 0
        for image_data in row:
            img = image_data["image"]
            name = image_data["name"]
            width = img.width
            height = img.height

            top_pixel = current_y + (max_height_in_row - height) // 2
            left_pixel = current_x
            current_x += width + 1  # Add 1 pixel spacing between images

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
        current_y += max_height_in_row + 1  # Add 1 pixel spacing between rows

    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Set the output file name
    output_file = os.path.join(output_folder, ATLAS_NAME + ".inkatlas.json")

    # Write everything to the .inkatlas.json
    with open(output_file, "w") as json_file:
        json.dump(data, json_file, indent=2)

    print(f"Data has been saved to {output_file}")

    # Save the combined image
    combined_image_path = os.path.join(output_folder, ATLAS_NAME + ".png")
    combined_image.save(combined_image_path)
    print(f"Combined image has been saved to {combined_image_path}")
    # Save the resized image with "_1080" suffix
    resized_image = combined_image.resize(
        (total_width // 2, total_height // 2), resample=None, box=None, reducing_gap=None
    )
    combined_image_path_1080 = combined_image_path.replace(".png", "_1080.png")
    resized_image.save(combined_image_path_1080)
    print(f"Combined image has been saved to {combined_image_path_1080}")


if __name__ == "__main__":
    main()
