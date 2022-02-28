### Process Markdown downloaded from notion

# Ideal Process
# - get my Statistics/ML table
# - list the most recent entries
# - choose which page to download
# - download the markdown file for that page
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
                lines[idx] = line.replace(self.stem, "")

        return lines

    def write(self):
        filename = self.file_name + ".md"
        with open(filename, "w") as out:
            out.writelines(self.lines)


md_file = Markdown("./Export-c7fc191c-c63d-4e33-ba68-6b44fb352857/Transforme 19732.md")
md_file.convert()
