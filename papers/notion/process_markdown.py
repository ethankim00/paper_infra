### Process Markdown downloaded from notion

# Ideal Process
# - get my Statistics/ML table
# - list the most recent entries
# - choose which page to download
# - download the markdown file for that page
import os
import argparse
import subprocess
from typing import List
from datetime import datetime
from pathlib import Path


def get_datetime():
    """Get current datetime in minimal mistakes format"""
    date_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return date_string[:-1] + "-05:00"


class Markdown:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.stem = Path(self.file_path).stem.replace(" ", "%20")
        print(self.stem)
        with open(file_path, "r") as file:
            self.lines = file.readlines()

    def convert(self):
        self.process_header(self.lines)
        header = self.generate_header(self.title, self.tags)

        self.lines = self.fix_image_paths(self.lines)

        self.lines = self.lines[7:]
        self.lines = header + self.lines
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
            header.append("\t" + "- " + tag + "\n")
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
        filename = date_string + "-" + self.file_name + ".md"
        with open(filename, "w") as out:
            out.writelines(self.lines)


# pain points
# read export folder from downloads
# rename image folder
# replace %20 check
# move to website folder


# or use github api
posts_path = "~/Desktop/Website/ethankim00.github.io/_posts"
images_path = "~/Desktop/Website"
file_path = "./NoisyTune  65e31.md"
md_file = Markdown(file_path)
md_file.convert()
image_file_path = file_path[:-3]


subprocess.run(["mv", image_file_path, md_file.file_name + "/"])


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file_path",
        type=str,
        help="System path to markdown download",
        required=False,
    )
    parser.add_argument("--publish", type=bool, default=True)


temp_folder = Path(__file__).parent.joinpath("tmp")

if __name__ == "__main__":
    # default to reading latest file from dowloads folder
    args = parse()
    if not args.input_file_path:
        list_of_paths = Path("~/Downloads/").glob("*")
        folder_path = max(list_of_paths, key=lambda p: p.stat().st_ctime)
    else:
        folder_path = Path(args.input_file_path)

    # copy markdown and image folder to local temp
    dir_name = os.listdir(folder_path)
    subprocess.run("cp", folder_path.joinpath("*.md"), temp_folder.joinpath("_posts"))
    subprocess.run("cp", folder_path.joinpath(), temp_folder.joinpath("assets/images"))

    # run processing

    # push to github

    # delete temp files
