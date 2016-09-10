#!/usr/bin/env python

import os
import sys
import argparse
from xml.etree import ElementTree as ET

class CoMet:

    tags = {"title", "description", "series", "issue", "volume", "publisher",
            "date", "genre", "character", "isVersionOf", "price", "format",
            "language", "rating", "rights", "identifier", "pages", "creator",
            "writer", "penciller", "editor", "coverDesigner", "letterer",
            "inker", "colorist", "coverImage", "lastMark", "readingDirection"}
    repeatable_tags = {"genre", "character", "creator", "writer", "penciller",
            "editor", "letterer", "inker", "colorist"}
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
        metaroot.attrib = CoMet.namespace
        metaroot.text = "\n"
        metaroot.tail = "\n"

        for tag in CoMet.nonrepetable_tags:
            if self.meta[tag] != None:
                element = ET.SubElement(metaroot, tag)
                element.text = self.meta[tag]
                element.tail = "\n"

        for repeat_tag in CoMet.repeatable_tags:
            for tag_data in self.meta[repeat_tag]:
                element = ET.SubElement(metaroot, tag)
                element.text = tag_data
                element.tail = "\n"

        self.xml_string = ET.tostring(metaroot, encoding="unicode")
        return self.xml_string

def main():
    comet = CoMet()
    comet.meta["title"] = "Batman: The Widening Gyre, Part One: Turning and Turning"
    comet.meta["date"] = "2009-08-26"
    comet.meta["coverImage"] = "BatmanWideningCover.jpg"
    comet.meta["character"].append("Batmen")
    comet.meta["character"].append("Joker")

    print(CoMet.xml_prolog, end="")
    print(comet.to_xml(), end="")

if __name__ == '__main__':
    sys.exit(main())
