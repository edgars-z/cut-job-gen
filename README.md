# cut-job-gen - Cutting Job Generator
<img src="/samples/svg/7A_320x450_to_2up_297x210_cut_job_with_3mm_deviation.svg" alt="Job Sample" height="300">

## Functionality
- Generates two-sided PDF and SVG print jobs in any desired format
- Possible to generate one-up and multi-up jobs
- Sheets un sub-sheets are clearly numbered and sheet sides identifiable
- Adds bleed around cut lines and crease lines to help identify deviations during testing
- Option to add registration mark in the desired position and size
- Option to shift the entire print job by a random distance in width and length directions. Shift amount and direction are clearly marked on each sub-sheet.

## Usage
1) [Clone this repository to VS Code](https://www.jcchouinard.com/git-clone-github-repository-vscode/)
2) [Set up a new Python virtual environment (.venv) and populate it with packages from "requirements.txt"](https://coderivers.org/blog/python-venv-vscode/)
3) Edit the script CONFIG parameters in "cut-job-gen.py" as desired.
4) Run. The script will generate the PDF in "/output" and an individual SVG for each sheet side in "/output/svg". SVG files can be tweaked in Inkscape if desired.