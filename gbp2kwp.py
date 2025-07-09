#!/usr/bin/env python3
# pylint: disable=C0114,C0116,W0718

import argparse
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# without a leading / to avoid the need to .lstrip(os.sep)
KDE_WALLPAPER_DIR = 'usr/share/wallpapers'

def create_image_symlink(image: str, name: str, destdir: Path, dark: bool = False):
    installed_image = os.path.join(destdir, image.lstrip(os.sep))
    # hard-coded values in Plasma
    dimensions = ["1024x768", "1280x800", "1440x2960", "1920x1080", "5120x2880"]
    _, extension = os.path.splitext(image)
    symlink_dir = os.path.join(destdir, KDE_WALLPAPER_DIR, name, 'contents',
                               'images_dark' if dark else 'images')
    try:
        os.makedirs(symlink_dir, exist_ok=True)
        for d in dimensions:
            symlink_path = os.path.join(symlink_dir, f"{d}{extension}")
            if os.path.exists(symlink_path):
                os.remove(symlink_path)
            os.symlink(image, symlink_path)
            print(f"Symlinked {image} -> {symlink_path}")
    except Exception as e:
        print(f"ERROR: Could not create symlink: {e}", file=sys.stderr)


def create_metadata_json(name: str, directory: str, destdir: Path, metadata: dict):
    kplugin = {
        "KPlugin": {
            "Id": directory,
            "Name": name
        }
    }
    kplugin["KPlugin"].update(metadata)

    metadata_path = os.path.join(destdir, KDE_WALLPAPER_DIR, directory, 'metadata.json')
    try:
        with open(metadata_path, 'w', encoding='utf-8') as mjson:
            json.dump(kplugin, mjson, ensure_ascii=False, indent=4)
        print(f"Generated {metadata_path}")
    except Exception as e:
        print(f"ERROR: Could not write metadata.json: {e}", file=sys.stderr)


def create_kde_wallpaper(xml_data: str, metadata: dict, destdir: Path = '/'):
    try:
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"ERROR: Could not parse XML data: {e}", file=sys.stderr)
        sys.exit(1)

    for wallpaper in root.findall('wallpaper'):
        name_element = wallpaper.find('name')
        if name_element is None or not name_element.text:
            print("Skipping wallpaper with no name.")
            continue

        name = name_element.text.strip()
        sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        print(f"Processing wallpaper: '{name}'")

        filename = wallpaper.find('filename')
        if filename is None:
            print(f"WARNING: {name} wallpaper has no 'filename' element", file=sys.stderr)
            continue

        light_path = filename.text.strip()
        if light_path.lower().endswith('.xml'):
            print(f"Skipping timed background XML: '{light_path}'.")
            continue
        create_image_symlink(light_path, sanitized_name, destdir)

        filename_dark = wallpaper.find('filename-dark')
        if filename_dark is not None:
            dark_path = filename_dark.text.strip()
            create_image_symlink(dark_path, sanitized_name, destdir, dark=True)

        create_metadata_json(name, sanitized_name, destdir, metadata)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converts a GNOME wallpaper XML file into a KDE-compatible symlink structure."
    )
    parser.add_argument("gnome_xml_file", type=Path, help="Path to the GNOME wallpaper XML file")
    parser.add_argument("-d", "--destdir", type=Path, help="Destination directory prefix")
    parser.add_argument("-a", "--author", help="Author name for the metadata")
    parser.add_argument("-e", "--email", help="Author email for the metadata")
    parser.add_argument("-l", "--license", help="License for the metadata")
    args = parser.parse_args()

    try:
        with open(args.gnome_xml_file, 'r', encoding='utf-8') as f:
            gnome_xml_data = f.read()
    except Exception as e:
        print(f"Error: Unable to read GNOME wallpaper XML: {e}", file=sys.stderr)
        sys.exit(1)

    add_metadata = {}
    if args.author:
        author_info = {"Name": args.author}
        if args.email:
            author_info["Email"] = args.email
        add_metadata["Authors"] = [author_info]
    if args.license:
        add_metadata["License"] = args.license

    create_kde_wallpaper(gnome_xml_data, add_metadata, args.destdir)
