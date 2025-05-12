def empty_atlas_data(xbm_relative, xbm_relative_1080):
    return {
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
                                    "$value": (f"{xbm_relative}"),
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
                                    "$value": (f"{xbm_relative_1080}"),
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


def empty_atlas_data2(output_folder_relative, atlas_name):
    xbm_relative = output_folder_relative / f"{atlas_name}.xbm"
    xbm_relative_1080 = output_folder_relative / f"{atlas_name}_1080.xbm"
    return {
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
                                    "$value": (f"{xbm_relative}"),
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
                                    "$value": (f"{xbm_relative_1080}"),
                                },
                                "Flags": "Soft",
                            },
                        },
                        empty_slot(),
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


def empty_slot():
    return {
        "$type": "inkTextureSlot",
        "parts": [],
        "slices": [],
        "texture": {"DepotPath": {"$type": "ResourcePath", "$storage": "uint64", "$value": "0"}, "Flags": "Soft"},
    }


# def part_data():
#     return {
#         "$type": "inkTextureAtlasMapper",
#         "clippingRectInPixels": {
#             "$type": "Rect",
#             "bottom": top_pixel + height,
#             "left": left_pixel,
#             "right": left_pixel + width,
#             "top": top_pixel,
#         },
#         "clippingRectInUVCoords": {
#             "$type": "RectF",
#             "Bottom": (top_pixel + height) / total_height,
#             "Left": left_pixel / total_width,
#             "Right": (left_pixel + width) / total_width,
#             "Top": top_pixel / total_height,
#         },
#         "partName": {"$type": "CName", "$storage": "string", "$value": name},
#     }
