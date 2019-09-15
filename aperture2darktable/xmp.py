import os.path

XMP = """<?xml version="1.0" encoding="UTF-8"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:xap="http://ns.adobe.com/xap/1.0/"
    xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/"
    xap:Rating="{rating}"
    xmpMM:DerivedFrom="{fileName}">
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>"""

def generate_xmp_rating(image_filename, rating):
    return XMP.format(fileName=image_filename, rating=rating)

def xmp_filename(image_filename, version_no):
    if not version_no:
        return image_filename + ".xmp"
    else:
        name, ext = os.path.splitext(image_filename)
        return f"{name}_{version_no:02d}{ext}.xmp"

