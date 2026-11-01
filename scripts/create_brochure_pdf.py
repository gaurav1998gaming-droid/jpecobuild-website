from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "JP-Ecobuild-Fly-Ash-Bricks-Brochure.pdf"
HERO_IMAGE = ROOT / "assets" / "gallery" / "brick-8.jpg"


def escape_pdf(value):
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def wrap(text, width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        candidate = (line + " " + word).strip()
        if len(candidate) > width and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


content = ["q", "0.969 0.980 0.965 rg", "0 0 595 842 re f", "Q"]


def rectangle(x, y, width, height, color):
    content.extend(["q", f"{color} rg", f"{x} {y} {width} {height} re f", "Q"])


def line(x1, y1, x2, y2, color, thickness=1):
    content.extend(["q", f"{color} RG", f"{thickness} w", f"{x1} {y1} m {x2} {y2} l S", "Q"])


def text(x, y, value, size=10, bold=False, color="0.09 0.22 0.18"):
    font = "F2" if bold else "F1"
    content.extend([
        "BT", f"/{font} {size} Tf", f"{color} rg", f"1 0 0 1 {x} {y} Tm",
        f"({escape_pdf(value)}) Tj", "ET",
    ])


def paragraph(x, y, value, width, size=10, leading=14, color="0.22 0.32 0.28", bold=False):
    for item in wrap(value, width):
        text(x, y, item, size=size, color=color, bold=bold)
        y -= leading
    return y


def image(x, y, width, height):
    content.extend(["q", f"{width} 0 0 {height} {x} {y} cm", "/Im1 Do", "Q"])


# Brand bar
rectangle(0, 778, 595, 64, "0.055 0.18 0.14")
rectangle(0, 778, 595, 5, "0.72 0.30 0.16")
text(42, 808, "JP Ecobuild Creations", 22, bold=True, color="1 1 1")
text(42, 790, "FLY ASH BRICKS  |  BULK SUPPLY  |  GHAZIABAD", 8, bold=True, color="0.86 0.95 0.88")
text(352, 810, "CALL / WHATSAPP", 7.5, bold=True, color="0.72 0.30 0.16")
text(352, 796, "+91 81719 59076", 12, bold=True, color="1 1 1")

# Hero: product message + real product photo
text(42, 738, "Build stronger. Build smarter.", 25, bold=True)
text(42, 714, "Reliable fly ash bricks for every project scale.", 11, bold=True, color="0.18 0.49 0.32")
paragraph(42, 686, "Consistent, dependable brick supply for homes, contractors and construction projects across Muradnagar, Ghaziabad and nearby areas.", 45, size=9.5, leading=13)
rectangle(42, 613, 122, 32, "0.91 0.95 0.91")
text(52, 632, "BULK SUPPLY", 8, bold=True, color="0.18 0.49 0.32")
text(52, 620, "For project needs", 7.5, color="0.22 0.32 0.28")
rectangle(174, 613, 122, 32, "0.99 0.94 0.90")
text(184, 632, "LOCAL DELIVERY", 8, bold=True, color="0.72 0.30 0.16")
text(184, 620, "Ghaziabad area", 7.5, color="0.35 0.25 0.19")
rectangle(324, 555, 229, 174, "1 1 1")
image(329, 560, 219, 164)
rectangle(329, 560, 219, 5, "0.72 0.30 0.16")
text(339, 574, "PRODUCT PHOTO  |  JP ECOBUILD", 7, bold=True, color="1 1 1")

# Product range cards
text(42, 570, "PRODUCT RANGE", 9, bold=True, color="0.18 0.49 0.32")
products = [
    (42, "01", "Regular Fly Ash Bricks", "For residential walls, partitions and general building work."),
    (214, "02", "Project Supply", "Reliable, consistent support for construction requirements."),
    (386, "03", "Bulk Orders", "Supply support for builders, contractors and larger projects."),
]
for x, number, title, description in products:
    rectangle(x, 479, 157, 72, "1 1 1")
    rectangle(x, 547, 157, 4, "0.72 0.30 0.16")
    text(x + 12, 527, number, 8, bold=True, color="0.72 0.30 0.16")
    text(x + 12, 510, title, 10, bold=True)
    paragraph(x + 12, 496, description, 25, size=7.8, leading=10, color="0.28 0.38 0.33")

# Icon-like benefit tiles
text(42, 449, "WHY CHOOSE FLY ASH BRICKS", 9, bold=True, color="0.18 0.49 0.32")
benefits = [
    (42, 392, "01", "Uniform dimensions", "Easier, neater masonry work."),
    (302, 392, "02", "Smooth finish", "Helps reduce finishing effort."),
    (42, 344, "03", "Sustainable material", "Fly ash based construction."),
    (302, 344, "04", "Project ready", "Suitable for bulk requirements."),
]
for x, y, number, title, description in benefits:
    rectangle(x, y, 251, 39, "0.92 0.96 0.92")
    rectangle(x + 10, y + 9, 22, 21, "0.18 0.49 0.32")
    text(x + 15, y + 16, number, 7, bold=True, color="1 1 1")
    text(x + 42, y + 23, title, 9, bold=True)
    text(x + 42, y + 11, description, 7.5, color="0.28 0.38 0.33")

# Details panel
text(42, 316, "PRODUCT & ORDER DETAILS", 9, bold=True, color="0.18 0.49 0.32")
rectangle(42, 238, 511, 60, "1 1 1")
rectangle(42, 238, 5, 60, "0.72 0.30 0.16")
text(61, 276, "Standard size", 9, bold=True)
text(61, 260, "9 x 4.5 x 3 inches", 11, bold=True, color="0.72 0.30 0.16")
line(215, 249, 215, 287, "0.85 0.89 0.85", 0.6)
text(232, 276, "Delivery & pricing", 9, bold=True)
text(232, 260, "Based on quantity and location", 9, color="0.28 0.38 0.33")
line(398, 249, 398, 287, "0.85 0.89 0.85", 0.6)
text(415, 276, "Serving", 9, bold=True)
text(415, 260, "Muradnagar, Ghaziabad & nearby", 8, color="0.28 0.38 0.33")

# Conversion-focused call-to-action
rectangle(42, 145, 511, 70, "0.055 0.18 0.14")
rectangle(42, 145, 8, 70, "0.72 0.30 0.16")
text(66, 186, "Need today's bulk price?", 17, bold=True, color="1 1 1")
text(66, 165, "Call or WhatsApp +91 81719 59076 for availability and delivery details.", 9.5, color="0.86 0.95 0.88")
rectangle(429, 160, 105, 36, "0.18 0.49 0.32")
text(443, 181, "WHATSAPP", 8, bold=True, color="1 1 1")
text(443, 168, "GET A QUOTE", 7.5, bold=True, color="0.86 0.95 0.88")

# Footer
line(42, 119, 553, 119, "0.72 0.80 0.75", 0.6)
text(42, 99, "jpecobuild.in  |  Bhikanpur, Muradnagar, Ghaziabad, Uttar Pradesh 201206", 8, color="0.30 0.42 0.36")
text(42, 80, "Please confirm project-specific requirements, availability and pricing before ordering.", 7.5, color="0.30 0.42 0.36")

stream = "\n".join(content).encode("latin-1")
hero_bytes = HERO_IMAGE.read_bytes()
objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 5 0 R /F2 6 0 R >> /XObject << /Im1 8 0 R >> >> /Annots [9 0 R] /Contents 4 0 R >>",
    b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
    b"<< /Title (JP Ecobuild Creations Fly Ash Bricks Product Brochure) /Author (JP Ecobuild Creations) >>",
    b"<< /Type /XObject /Subtype /Image /Width 1280 /Height 960 /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length " + str(len(hero_bytes)).encode("ascii") + b" >>\nstream\n" + hero_bytes + b"\nendstream",
    b"<< /Type /Annot /Subtype /Link /Rect [429 160 534 196] /Border [0 0 0] /A << /S /URI /URI (https://wa.me/918171959076) >> >>",
]

pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
offsets = [0]
for index, obj in enumerate(objects, start=1):
    offsets.append(len(pdf))
    pdf.extend(f"{index} 0 obj\n".encode("ascii"))
    pdf.extend(obj)
    pdf.extend(b"\nendobj\n")

xref_offset = len(pdf)
pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
pdf.extend(b"0000000000 65535 f \n")
for offset in offsets[1:]:
    pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
pdf.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R /Info 7 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii"))

OUTPUT.write_bytes(pdf)
print(f"Created {OUTPUT} ({len(pdf)} bytes)")
