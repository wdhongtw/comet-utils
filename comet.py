#!/usr/bin/env python

# Copyright (C) 2016 Weida Hong <wdhongtw@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import argparse
from xml.etree import ElementTree as ET

class CoMet:

    tags_list = [
        "title", "description", "series", "issue", "volume", "publisher",
        "date", "genre", "character", "isVersionOf", "price", "format",
        "language", "rating", "rights", "identifier", "pages", "creator",
        "writer", "penciller", "editor", "coverDesigner", "letterer",
        "inker", "colorist", "coverImage", "lastMark", "readingDirection"]
    tags = {
        "title", "description", "series", "issue", "volume", "publisher",
        "date", "genre", "character", "isVersionOf", "price", "format",
        "language", "rating", "rights", "identifier", "pages", "creator",
        "writer", "penciller", "editor", "coverDesigner", "letterer",
        "inker", "colorist", "coverImage", "lastMark", "readingDirection"}
    repeatable_tags = {
        "genre", "character", "creator", "writer", "penciller", "editor",
        "letterer", "inker", "colorist"}
    nonrepetable_tags = tags - repeatable_tags
    required_tags = {"title"}

    xml_prolog = "<?xml version=\"1.1\" encoding=\"UTF-8\"?>\n"
    namespace = {
        "xmlns:comet": "http://www.denvog.com/comet/",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": "http://www.denvog.com http://www.denvog.com/comet/comet.xsd"}

    def __init__(self):
        self.meta = {}
        for tag in CoMet.nonrepetable_tags:
            self.meta[tag] = None
        for tag in CoMet.repeatable_tags:
            self.meta[tag] = []
        for tag in CoMet.required_tags:
            pass
        self.meta["title"] = "Untitled Comic"
        return

    def to_xml(self):
        metaroot = ET.Element("comet")

        for tag in CoMet.nonrepetable_tags:
            if self.meta[tag] != None:
                element = ET.SubElement(metaroot, tag)
                element.text = self.meta[tag]
                element.tail = "\n"

        for repeat_tag in CoMet.repeatable_tags:
            for tag_data in self.meta[repeat_tag]:
                element = ET.SubElement(metaroot, repeat_tag)
                element.text = tag_data
                element.tail = "\n"

        metaroot = CoMet.__sort(metaroot)

        metaroot.attrib = CoMet.namespace
        metaroot.text = "\n"
        metaroot.tail = "\n"

        self.xml_string = ET.tostring(metaroot, encoding="unicode")
        return self.xml_string

    def from_xml(self, xml):
        metaroot = ET.fromstring(xml)
        for child in metaroot:
            if child.tag in CoMet.nonrepetable_tags:
                self.meta[child.tag] = child.text
            elif child.tag in CoMet.repeatable_tags:
                self.meta[child.tag].append(child.text)
        return

    def __sort(metaroot):
        temp_metaroot = ET.Element("comet")
        for tagname in CoMet.tags_list:
            for child in metaroot.findall(tagname):
                metaroot.remove(child)
                temp_metaroot.append(child)
        return temp_metaroot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", help="Input file",
        default=None, type=argparse.FileType("r"))
    parser.add_argument("-o", "--outfile", help="Output file",
        default=sys.stdout, type=argparse.FileType("w"))

    args = parser.parse_args()

    comet = CoMet()
    if args.infile != None:
        xml_content = args.infile.read()
        comet.from_xml(xml_content)
    else:
        comet.meta["title"] = "Batman: The Widening Gyre, Part One: Turning and Turning"
        comet.meta["date"] = "2009-08-26"
        comet.meta["coverImage"] = "BatmanWideningCover.jpg"
        comet.meta["character"].append("Batmen")
        comet.meta["character"].append("Joker")

    args.outfile.write(CoMet.xml_prolog)
    args.outfile.write(comet.to_xml())
    return 0

if __name__ == '__main__':
    sys.exit(main())
