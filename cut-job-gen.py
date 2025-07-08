import os
import random
import shutil

import svgwrite

from svglib.svglib import svg2rlg

from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.lib.units import mm

# Define sizes in mm
sheet_width, sheet_length = 320, 450
finished_width, finished_length = 297, 420
bleed = 3

#Configure script
crop_marks = False
reg_mark = False
num_sheets = 5 # sheets are double sided (1 sheet = 2 pages)
random_deviation = True # random offset will be applied to each sheet
deviation_range = 3 # +/- mm



if(random_deviation):
    deviation_width = [0] + [round(random.uniform(-deviation_range, deviation_range),3) for _ in range(num_sheets-1)]
    deviation_length = [0] + [round(random.uniform(-deviation_range, deviation_range),3) for _ in range(num_sheets-1)]
else:
    deviation_width = [0] * num_sheets 
    deviation_length = [0] * num_sheets


# Set up folders and file names

if not os.path.exists("output"):
    os.makedirs("output")
if os.path.exists("output/svg"):
        # Delete old SVG files from previous runs
        for filename in os.listdir("output/svg"):
            file_path = os.path.join("output/svg", filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
else:
    os.makedirs("output/svg")

filename = str(sheet_width) + "x" + str(sheet_length) + "_template"
svg_pages = [] #List of pages to be converted to PDF

sheet_no = 0


for dev_w, dev_l in zip(deviation_width, deviation_length):
    sheet_no += 1
    for side in ["A", "B"]:
        svg_filename = "output/svg/" + str(sheet_no) + side + "_" + filename + ".svg"
        svg_pages.append(svg_filename)
        # Create SVG
        dwg = svgwrite.Drawing(svg_filename, size=(f"{sheet_width}mm", f"{sheet_length}mm"))

        # Need to flip deviation direction on the backside
        if side == "B":
            dev_w = - dev_w

        #Draw inner bleed box
        dwg.add(dwg.rect(insert=(f"{dev_w + (sheet_width - finished_width)/2 + bleed/2}mm", f"{dev_l + (sheet_length - finished_length)/2 + bleed/2}mm"),
                        size=(f"{finished_width - bleed}mm", f"{finished_length - bleed}mm"),
                        fill='none', stroke=svgwrite.rgb(0, 159, 228), stroke_width=f"{bleed}mm")) #blue

        #Draw outer bleed box
        dwg.add(dwg.rect(insert=(f"{dev_w + (sheet_width - finished_width)/2 - bleed/2}mm", f"{dev_l + (sheet_length - finished_length)/2 - bleed/2}mm"),
                        size=(f"{finished_width + bleed}mm", f"{finished_length + bleed}mm"),
                        fill='none', stroke=svgwrite.rgb(177, 6, 50), stroke_width=f"{bleed}mm")) #red

        # Draw splitlines on finished sheet to mark crease / fold positions
        splitlines = [1/4, 1/3, 1/2, 2/3, 3/4]
        for fraction in splitlines:
            dwg.add(dwg.line((f"{dev_w + (sheet_width - finished_width)/2}mm", f"{dev_l + (sheet_length - finished_length)/2 + finished_length * fraction}mm"),
                            (f"{dev_w + (sheet_width - finished_width)/2 + finished_width}mm", f"{dev_l + (sheet_length - finished_length)/2 + finished_length * fraction}mm"),
                            stroke=svgwrite.rgb(0, 159, 228), stroke_width=f"{bleed}mm")) #blue
            dwg.add(dwg.line((f"{dev_w + (sheet_width - finished_width)/2}mm", f"{dev_l + (sheet_length - finished_length)/2 + finished_length * fraction}mm"),
                            (f"{(dev_w + sheet_width - finished_width)/2 + finished_width}mm", f"{dev_l + (sheet_length - finished_length)/2 + finished_length * fraction}mm"),
                            stroke="black", stroke_dasharray="2,1", stroke_width="0.25mm")) #black dashed

        # Draw finished sheet outline
        dwg.add(dwg.rect(insert=(f"{dev_w + (sheet_width - finished_width)/2}mm", f"{dev_l + (sheet_length - finished_length)/2}mm"),
                        size=(f"{finished_width}mm", f"{finished_length}mm"),
                        fill='none', stroke="black", stroke_dasharray="2,1", stroke_width="0.25mm")) #black dashed

        # Add page number
        dwg.add(dwg.text(str(sheet_no) + side, 
                         insert=(f"{dev_w + (sheet_width - finished_width)/2 + finished_width/2}mm", f"{dev_l + (sheet_length - finished_length)/2 + finished_length/8}mm"),
                         text_anchor="middle",
                         font_size="60pt",
                         font_family="Verdana",
                         fill="black"))

        # Add deviation indicator
        if(random_deviation):
            # Define a marker for the arrowhead
            arrow = dwg.marker(id="arrow",
                   insert=(10, 5), size=(10, 10),
                   orient="auto", markerUnits="strokeWidth")
            arrow.add(dwg.path(d="M 0 0 L 10 5 L 0 10 z", fill="black"))
            dwg.defs.add(arrow)

            arrow_length = deviation_range * 10
            # Draw a line with the arrow marker at the end
            dwg.add(dwg.line(start=(f"{dev_w + (sheet_width - finished_width)/2 + finished_width - 1.5*arrow_length}mm", f"{dev_l + (sheet_length - finished_length)/2 + 1.5*arrow_length}mm"), 
                             end=(f"{dev_w + (sheet_width - finished_width)/2 + finished_width - 1.5*arrow_length + arrow_length*dev_w/deviation_range}mm", f"{dev_l + (sheet_length - finished_length)/2 + 1.5*arrow_length}mm"),
                            stroke="black", stroke_width="1mm",
                            marker_end=arrow.get_funciri()))
            
            dwg.add(dwg.line(start=(f"{dev_w + (sheet_width - finished_width)/2 + finished_width - 1.5*arrow_length}mm", f"{dev_l + (sheet_length - finished_length)/2 + 1.5*arrow_length}mm"), 
                    end=(f"{dev_w + (sheet_width - finished_width)/2 + finished_width - 1.5*arrow_length}mm", f"{dev_l + (sheet_length - finished_length)/2 + 1.5*arrow_length + arrow_length*dev_l/deviation_range}mm"),
                    stroke="black", stroke_width="1mm",
                    marker_end=arrow.get_funciri()))

        # Save SVG
        dwg.save()


# Create PDF canvas (output file)
c = canvas.Canvas("output/" + filename + ".pdf", pagesize=(sheet_width * mm, sheet_length * mm))

for svg_path in svg_pages:
    # Convert SVG to ReportLab Drawing
    drawing = svg2rlg(svg_path)
    renderPDF.draw(drawing, c, 0, 0)
    # Add new page
    c.showPage()

c.save()