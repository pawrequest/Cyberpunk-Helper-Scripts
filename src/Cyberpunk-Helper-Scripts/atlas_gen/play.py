from pathlib import Path

from inkatlas_generator import main

OUTPUT_FOLDER = r"C:\prdev\mod\Cyberpunk-Helper-Scripts\data"
INPUT_FOLDER = r"D:\data\cp77\1024"
ATLAS_NAME = "randy"
OUTPUT_FOLDER = Path(OUTPUT_FOLDER)
INPUT_FOLDER = Path(INPUT_FOLDER)

if __name__ == '__main__':
    main(out_dir=OUTPUT_FOLDER, in_dir=INPUT_FOLDER, atlas_name=ATLAS_NAME)