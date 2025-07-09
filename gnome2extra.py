#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

def create_kde_symlinks(xml_data, output_base_dir, author, email, license):
    """
    Parses GNOME wallpaper XML and creates a KDE-compatible symlink structure.

    Args:
        xml_data (str): A string containing the GNOME wallpaper XML.
        output_base_dir (str): The path to the directory where the symlinks
                               will be created.
        author (str): The name of the author for the metadata.
        email (str): The email of the author for the metadata.
        license (str): The license for the metadata.
    """
    print(f"Creating output directory at: {output_base_dir}")
    os.makedirs(output_base_dir, exist_ok=True)

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"ERROR: Could not parse XML data: {e}", file=sys.stderr)
        sys.exit(1)

    # Iterate over each <wallpaper> entry in the XML
    for wallpaper in root.findall('wallpaper'):
        name_element = wallpaper.find('name')
        if name_element is None or not name_element.text:
            print("Skipping wallpaper with no name.")
            continue

        name = name_element.text.strip()
        # Remove special characters from a string to make a valid filename
        sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        print(f"\nProcessing wallpaper: '{name}'")

        # Find the light and dark mode filenames
        filename = wallpaper.find('filename')
        filename_dark = wallpaper.find('filename-dark')

        if filename is None:
            print("ERROR: {name} wallpaper has no 'filename' element")
            continue

        light_path = filename.text.strip()

        if light_path.lower().endswith('.xml'):
            print(f"  -> Found a timed wallpaper XML: '{source_path}'.")
            print("     - NOTE: This script does not process nested timed wallpapers.")
            continue

        # --- Create Directories ---
        wallpaper_dir = os.path.join(output_base_dir, sanitized_name)
        kde_image_dir = os.path.join(wallpaper_dir, 'contents', 'images')
        os.makedirs(kde_image_dir, exist_ok=True)

        # --- Create Symlinks ---
        _, extension = os.path.splitext(light_path)
        generic_filename = f"wallpaper{extension}"
        light_symlink_path = os.path.join(kde_image_dir, generic_filename)
        try:
            if os.path.exists(light_symlink_path): os.remove(light_symlink_path)
            os.symlink(light_path, light_symlink_path)
            print(f"     - Symlinked {light_path} -> {light_symlink_path}")
        except Exception as e:
            print(f"     - ERROR: Could not create symlink. {e}", file=sys.stderr)

        if filename_dark is not None:
            dark_path = filename_dark.text.strip()
            kde_dark_image_dir = os.path.join(wallpaper_dir, 'contents', 'images_dark')
            os.makedirs(kde_dark_image_dir, exist_ok=True)

            dark_symlink_path = os.path.join(kde_dark_image_dir, generic_filename)
            try:
                if os.path.exists(dark_symlink_path): os.remove(dark_symlink_path)
                os.symlink(dark_path, dark_symlink_path)
                print(f"     - Symlinked {dark_path} -> {dark_symlink_path}")
            except Exception as e:
                print(f"     - ERROR: Could not create symlink. {e}", file=sys.stderr)

        # --- Generate metadata.json ---
        metadata = {
            "KPlugin": {
                "Id": sanitized_name,
                "Name": name
            }
        }
        if author:
            author_info = {"Name": author}
            if email:
                author_info["Email"] = email
            metadata["KPlugin"]["Authors"] = [author_info]
        if license:
            metadata["KPlugin"]["License"] = license

        metadata_path = os.path.join(wallpaper_dir, 'metadata.json')
        try:
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
            print(f"     - Generated {metadata_path}")
        except Exception as e:
            print(f"     - ERROR: Could not write metadata.json. {e}", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converts a GNOME wallpaper XML file into a KDE-compatible symlink structure."
    )
    parser.add_argument(
        "gnome_xml_file",
        help="The path to the input GNOME wallpaper XML file."
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="The path to the directory where the wallpaper structure will be created."
    )
    parser.add_argument("--author", help="Author name for the metadata.")
    parser.add_argument("--email", help="Author email for the metadata.")
    parser.add_argument("--license", help="License for the metadata.")
    args = parser.parse_args()

    try:
        with open(args.gnome_xml_file, 'r', encoding='utf-8') as f:
            gnome_xml_data = f.read()
    except Exception as e:
        print(f"Error: Unable to read GNOME wallpaper XML: {e}", file=sys.stderr)
        sys.exit(1)

    create_kde_symlinks(gnome_xml_data, args.output, args.author, args.email, args.license)
