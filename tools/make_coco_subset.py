import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Create a deterministic COCO subset annotation file.")
    parser.add_argument("--ann", required=True, help="Input COCO annotation json")
    parser.add_argument("--out", required=True, help="Output subset annotation json")
    parser.add_argument("--num", type=int, default=5000, help="Number of images")
    args = parser.parse_args()

    ann_path = Path(args.ann)
    out_path = Path(args.out)

    with ann_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    images = sorted(data["images"], key=lambda item: item["id"])[:args.num]
    image_ids = {image["id"] for image in images}
    annotations = [
        ann for ann in data["annotations"] if ann["image_id"] in image_ids
    ]

    subset = dict(data)
    subset["images"] = images
    subset["annotations"] = annotations

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(subset, f)

    print(
        "Saved {} images and {} annotations to {}".format(
            len(images), len(annotations), out_path))


if __name__ == "__main__":
    main()
