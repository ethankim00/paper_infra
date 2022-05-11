### Process Markdown downloaded from notion

import os
import argparse
import subprocess
import logging
from typing import List
from datetime import datetime
from pathlib import Path


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def fetch_export(file_path: str = None) -> Path:
    # TODO deal with raw markdown files without images
    temp_folder = Path(__file__).parent.joinpath("tmp")
    folder_path = Path("../../../Downloads/")
    assert folder_path.is_dir()
    if not file_path:
        export_files = list(folder_path.glob("Export-*"))
        most_recent_folder = max(export_files, key=os.path.getctime)
        folder_path = Path(most_recent_folder)
    else:
        folder_path = folder_path.joinpath(file_path)
    markdown_path = next(folder_path.glob("*.md"))
    try:
        subprocess.run(["mv", markdown_path, temp_folder.joinpath("_posts")])
    except:
        pass
    subprocess.run(
        ["mv", next(folder_path.glob("*/")), temp_folder.joinpath("assets/images")]
    )
    logging.info("Copied Files to local temp directory")
    return Path(markdown_path.stem)


def get_datetime():
    """Get current datetime in minimal mistakes format"""
    date_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return date_string[:-1] + "-05:00"


class Markdown:
    def __init__(
        self, file_path: str, temp_folder: Path = Path(__file__).parent.joinpath("tmp")
    ):
        self.temp_folder = temp_folder
        self.file_path = (
            self.temp_folder.joinpath("_posts").joinpath(file_path).with_suffix(".md")
        )
        self.stem = Path(self.file_path).stem.replace(" ", "%20")
        with open(self.file_path, "r") as file:
            self.lines = file.readlines()

    def rename_image_files(self):
        image_dir = self.temp_folder.joinpath("assets").joinpath("images")
        print(image_dir)
        print(self.file_name)
        subprocess.run(
            [
                "mv",
                image_dir.joinpath(self.file_path.stem),
                image_dir.joinpath(self.file_name),
            ]
        )

    def remove_strikethroughs(self, lines: List[str]):
        """Remove strikethroughs from markdown"""
        for idx, line in enumerate(lines):
            if "::" in line:
                lines[idx] = ""
        return lines

    def convert(self):
        self.process_header(self.lines)
        header = self.generate_header(self.title, self.tags)
        self.lines = self.fix_image_paths(self.lines)
        self.lines = self.remove_strikethroughs(self.lines)
        self.lines = self.lines[7:]
        self.lines = header + self.lines
        self.rename_image_files()
        self.write()

    def process_header(self, lines: List[str]) -> List[str]:
        """Process header from notion markdown export to minimal mistakes format"""
        markdown_header = self.lines[:6]
        self.title = markdown_header[0].replace("\n", "").replace("#", "").strip()
        self.file_name = "".join(self.title.split())
        self.tags = markdown_header[5][6:].strip().split(", ")

    def generate_header(self, title: str, tags: List[str]):

        header = [
            "---\n",
            'title: "{}"\n'.format(title),
            "last_modified_at: {}\n".format(get_datetime()),
            "categories: {}\n".format("paper_review"),
            "tags:\n",
        ]
        for tag in tags:
            header.append("    " + "- " + tag + "\n")
        header.append("---\n")
        return header

    def fix_image_paths(self, lines: str):
        markdown_image_str = "]("
        for idx, line in enumerate(lines):
            if markdown_image_str in line:
                start_index = line.index(markdown_image_str) + len(markdown_image_str)
                line = (
                    line[:start_index]
                    + "/assets/images/{}".format(self.file_name)
                    + line[start_index:]
                )
                lines[idx] = line.replace(self.stem, "").replace("%20", " ")
        return lines

    def write(self):
        date_string = datetime.now().strftime("%Y-%m-%d")
        self.post_file_name = date_string + "-" + self.file_name + ".md"
        with open(
            self.temp_folder.joinpath("_posts").joinpath(self.post_file_name), "w"
        ) as out:
            out.writelines(self.lines)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file_path",
        type=str,
        help="System path to markdown download",
        required=False,
    )
    parser.add_argument("--publish", type=bool, default=True)
    return parser.parse_args()


temp_folder = Path(__file__).parent.joinpath("tmp")
if __name__ == "__main__":
    # default to reading latest file from dowloads folder
    args = parse()
    # copy markdown and image folder to local temp
    file_path = fetch_export(args.input_file_path)
    # file_path = Path("NoisyTune  65e31")
    print(file_path)
    # run processing
    md_file = Markdown(file_path)
    md_file.convert()
    # TODO directly push to github
    # TEMP manually move to website folder
    logging.info("Copying to website repo")
    file_name = md_file.file_name
    post_file_name = md_file.post_file_name
    temp_folder = Path(__file__).parent.joinpath("tmp")
    post_path = temp_folder.joinpath("_posts").joinpath(post_file_name)
    image_dir = temp_folder.joinpath("assets/images").joinpath(file_name)
    website_path = Path("../../Website/ethankim00.github.io/")
    website_post_path = website_path.joinpath("_posts").joinpath(post_file_name)
    website_image_path = website_path.joinpath("assets/images").joinpath(file_name)
    post_path.rename(website_post_path)
    image_dir.rename(website_image_path)
    temp_folder.joinpath("_posts").joinpath(file_path).with_suffix(".md").unlink()
