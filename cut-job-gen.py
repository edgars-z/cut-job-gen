import svgwrite

from svglib.svglib import svg2rlg

from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.lib.units import mm

# Define sizes in mm
sheet_width, sheet_length = 320, 450
finished_width, finished_length = 297, 420
bleed = 3


# Create SVG
filename = "output/" + str(sheet_width) + "x" + str(sheet_length) + "_template"
svg_filename = filename + ".svg"
dwg = svgwrite.Drawing(svg_filename, size=(f"{sheet_width}mm", f"{sheet_length}mm"))

#Draw inner bleed box
dwg.add(dwg.rect(insert=(f"{(sheet_width - finished_width)/2 + bleed/2}mm", f"{(sheet_length - finished_length)/2 + bleed/2}mm"),
                size=(f"{finished_width - bleed}mm", f"{finished_length - bleed}mm"),
                fill='none', stroke=svgwrite.rgb(0, 159, 228), stroke_width=f"{bleed}mm")) #blue

#Draw outer bleed box
dwg.add(dwg.rect(insert=(f"{(sheet_width - finished_width)/2 - bleed/2}mm", f"{(sheet_length - finished_length)/2 - bleed/2}mm"),
                size=(f"{finished_width + bleed}mm", f"{finished_length + bleed}mm"),
                fill='none', stroke=svgwrite.rgb(177, 6, 50), stroke_width=f"{bleed}mm")) #red




# Draw splitlines on finished sheet to mark crease / fold positions
splitlines = [1/4, 1/3, 1/2, 2/3, 3/4]
for fraction in splitlines:
    dwg.add(dwg.line((f"{(sheet_width - finished_width)/2}mm", f"{(sheet_length - finished_length)/2 + finished_length * fraction}mm"),
                      (f"{(sheet_width - finished_width)/2 + finished_width}mm", f"{(sheet_length - finished_length)/2 + finished_length * fraction}mm"),
                      stroke=svgwrite.rgb(0, 159, 228), stroke_width=f"{bleed}mm")) #blue
    dwg.add(dwg.line((f"{(sheet_width - finished_width)/2}mm", f"{(sheet_length - finished_length)/2 + finished_length * fraction}mm"),
                      (f"{(sheet_width - finished_width)/2 + finished_width}mm", f"{(sheet_length - finished_length)/2 + finished_length * fraction}mm"),
                      stroke="black", stroke_dasharray="2,1", stroke_width="0.25mm")) #black dashed

# Draw finished sheet outline
dwg.add(dwg.rect(insert=(f"{(sheet_width - finished_width)/2}mm", f"{(sheet_length - finished_length)/2}mm"),
                size=(f"{finished_width}mm", f"{finished_length}mm"),
                fill='none', stroke="black", stroke_dasharray="2,1", stroke_width="0.25mm")) #black dashed

# Save SVG and covert to PDF
dwg.save()

#List of pages to be converted to PDF
svg_pages = [svg_filename, svg_filename]

# Create PDF canvas (output file)
c = canvas.Canvas(filename + ".pdf", pagesize=(sheet_width * mm, sheet_length * mm))

for svg_path in svg_pages:
    # Convert SVG to ReportLab Drawing
    drawing = svg2rlg(svg_path)
    renderPDF.draw(drawing, c, 0, 0)
    # Add new page
    c.showPage()

c.save()