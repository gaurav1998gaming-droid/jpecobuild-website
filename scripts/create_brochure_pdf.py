from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "JP-Ecobuild-Fly-Ash-Bricks-Brochure.pdf"


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
        "BT",
        f"/{font} {size} Tf",
        f"{color} rg",
        f"1 0 0 1 {x} {y} Tm",
        f"({escape_pdf(value)}) Tj",
        "ET",
    ])


def paragraph(x, y, value, width, size=10, leading=14, color="0.22 0.32 0.28", bold=False):
    for item in wrap(value, width):
        text(x, y, item, size=size, color=color, bold=bold)
        y -= leading
    return y


rectangle(0, 782, 595, 60, "0.07 0.21 0.17")
text(42, 808, "JP Ecobuild Creations", 22, bold=True, color="1 1 1")
text(42, 790, "FLY ASH BRICKS  |  BULK SUPPLY  |  GHAZIABAD", 8, bold=True, color="0.86 0.95 0.88")
text(350, 810, "Call / WhatsApp: +91 81719 59076", 8, color="1 1 1")
text(350, 796, "jpecobuildcreations@gmail.com", 8, color="0.86 0.95 0.88")

text(42, 740, "Fly Ash Bricks for Stronger Builds", 25, bold=True)
text(42, 719, "Reliable brick supply for homes, contractors and construction projects.", 11, bold=True, color="0.18 0.49 0.32")
line(42, 704, 553, 704, "0.18 0.49 0.32", 2)
paragraph(42, 682, "JP Ecobuild Creations supplies dependable fly ash bricks for residential, commercial and construction projects across Muradnagar, Ghaziabad and nearby areas.", 88, size=10)

text(42, 625, "PRODUCT RANGE", 9, bold=True, color="0.18 0.49 0.32")
products = [
    (588, "Regular Fly Ash Bricks", "For residential walls, partitions and general building work."),
    (542, "Project Requirement Supply", "Consistent supply support for project requirements."),
    (496, "Bulk Orders", "For builders, contractors and construction projects."),
]
for y, title, description in products:
    rectangle(42, y - 28, 511, 37, "1 1 1")
    text(57, y - 3, title, 10.5, bold=True)
    text(225, y - 3, description, 8.5, color="0.22 0.32 0.28")

text(42, 443, "WHY CHOOSE FLY ASH BRICKS", 9, bold=True, color="0.18 0.49 0.32")
rectangle(42, 274, 511, 148, "0.92 0.96 0.92")
text(57, 397, "Key Benefits", 12, bold=True)
benefits = [
    "Uniform shape and consistent dimensions for easier masonry work.",
    "Smooth surface that can help reduce finishing work.",
    "Fly ash based material for more sustainable construction.",
    "Bulk supply support for builders, contractors and projects.",
]
y = 377
for benefit in benefits:
    text(57, y, "- " + benefit, 9)
    y -= 19

text(57, 295, "Product & Order Details", 11, bold=True)
text(230, 295, "Standard size: 9 x 4.5 x 3 inches", 9)
text(230, 280, "Delivery and pricing depend on quantity and location.", 9)

rectangle(42, 176, 511, 70, "0.07 0.21 0.17")
text(57, 216, "Need a quote for your project?", 17, bold=True, color="1 1 1")
text(57, 194, "Call or WhatsApp +91 81719 59076 for availability, bulk pricing and delivery details.", 10, color="0.86 0.95 0.88")

line(42, 148, 553, 148, "0.72 0.80 0.75", 0.6)
text(42, 130, "Address: QC4X+R72, Bhikanpur, Muradnagar, Ghaziabad, Uttar Pradesh 201206", 8, color="0.30 0.42 0.36")
text(42, 112, "Website: jpecobuild.in", 8, color="0.30 0.42 0.36")
text(42, 88, "Please confirm project-specific requirements, availability and pricing before ordering.", 8, color="0.30 0.42 0.36")

stream = "\n".join(content).encode("latin-1")
objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> /Contents 4 0 R >>",
    b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
    b"<< /Title (JP Ecobuild Creations Fly Ash Bricks Product Brochure) /Author (JP Ecobuild Creations) >>",
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
pdf.extend(
    f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R /Info 7 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
)

OUTPUT.write_bytes(pdf)
print(f"Created {OUTPUT} ({len(pdf)} bytes)")
