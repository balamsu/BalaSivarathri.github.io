"""
Generates  sample_data.xlsx  — the input template for stress_tolerance_indices.R
Run once:  python3 build_sample_excel.py
"""

from openpyxl import Workbook
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side, numbers
)
from openpyxl.utils import get_column_letter

wb = Workbook()

# ── colour palette ──────────────────────────────────────────────────────────
GREEN_DARK   = "1a5e38"   # MSU dark green
GREEN_MID    = "5a8a5e"
GREEN_LIGHT  = "c8e6c9"
YELLOW_LIGHT = "fff9c4"
GREY_LIGHT   = "f5f5f5"
WHITE        = "ffffff"

def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def border(style="thin"):
    s = Side(style=style)
    return Border(left=s, right=s, top=s, bottom=s)

def bold(size=11, color="000000"):
    return Font(bold=True, size=size, color=color)

def center(wrap=False):
    return Alignment(horizontal="center", vertical="center", wrap_text=wrap)

def left(wrap=False):
    return Alignment(horizontal="left", vertical="center", wrap_text=wrap)


# ════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Data
# ════════════════════════════════════════════════════════════════════════════
ws = wb.active
ws.title = "Data"
ws.sheet_view.showGridLines = False

# --- title row --------------------------------------------------------------
ws.merge_cells("A1:D1")
ws["A1"].value     = "Plant Stress Tolerance Indices — Input Data"
ws["A1"].font      = Font(bold=True, size=14, color=WHITE)
ws["A1"].fill      = fill(GREEN_DARK)
ws["A1"].alignment = center()
ws.row_dimensions[1].height = 28

# --- sub-header row ---------------------------------------------------------
ws.merge_cells("A2:D2")
ws["A2"].value     = (
    "Fill in Yp (non-stress) and Ys (stress) yield values for each genotype. "
    "Trait can be grain yield, biomass, or any stress-sensitive variable."
)
ws["A2"].font      = Font(italic=True, size=10, color="444444")
ws["A2"].fill      = fill(GREEN_LIGHT)
ws["A2"].alignment = left(wrap=True)
ws.row_dimensions[2].height = 32

# --- column headers ---------------------------------------------------------
headers = [
    ("A3", "Genotype",
     "Variety / line name or code"),
    ("B3", "Yp\n(Non-Stress Yield)",
     "Yield / trait value measured in the non-stress (favourable) environment"),
    ("C3", "Ys\n(Stress Yield)",
     "Yield / trait value measured under the stress environment"),
    ("D3", "Notes (optional)",
     "Any additional notes about this genotype"),
]

for cell_addr, label, comment_text in headers:
    c = ws[cell_addr]
    c.value     = label
    c.font      = bold(11, WHITE)
    c.fill      = fill(GREEN_MID)
    c.alignment = center(wrap=True)
    c.border    = border()
ws.row_dimensions[3].height = 40

# --- sample data rows -------------------------------------------------------
sample = [
    ("G1",  4.20, 2.80, ""),
    ("G2",  3.85, 2.60, ""),
    ("G3",  4.60, 2.50, "drought tolerant check"),
    ("G4",  3.50, 2.40, ""),
    ("G5",  4.10, 3.00, ""),
    ("G6",  5.00, 2.70, "high yielding check"),
    ("G7",  3.70, 2.20, "sensitive check"),
    ("G8",  4.80, 3.10, ""),
    ("G9",  4.30, 2.90, ""),
    ("G10", 3.95, 2.50, ""),
]

for i, (geno, yp, ys, note) in enumerate(sample, start=4):
    row_fill = fill(WHITE) if i % 2 == 0 else fill(GREY_LIGHT)
    for col, val in zip(["A", "B", "C", "D"], [geno, yp, ys, note]):
        c = ws[f"{col}{i}"]
        c.value     = val
        c.fill      = row_fill
        c.border    = border()
        c.alignment = center() if col in ("B", "C") else left()
        if col in ("B", "C"):
            c.number_format = "0.00"

# --- empty buffer rows (for user to add more genotypes) --------------------
for i in range(14, 24):
    row_fill = fill(WHITE) if i % 2 == 0 else fill(GREY_LIGHT)
    for col in ["A", "B", "C", "D"]:
        c = ws[f"{col}{i}"]
        c.fill   = row_fill
        c.border = border()
        c.alignment = center() if col in ("B", "C") else left()

# --- column widths ----------------------------------------------------------
ws.column_dimensions["A"].width = 18
ws.column_dimensions["B"].width = 20
ws.column_dimensions["C"].width = 20
ws.column_dimensions["D"].width = 30

# freeze header rows
ws.freeze_panes = "A4"


# ════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Index Reference
# ════════════════════════════════════════════════════════════════════════════
ref = wb.create_sheet("Index Reference")
ref.sheet_view.showGridLines = False

ref.merge_cells("A1:F1")
ref["A1"].value     = "Stress Tolerance Index Formulae & Interpretation"
ref["A1"].font      = Font(bold=True, size=14, color=WHITE)
ref["A1"].fill      = fill(GREEN_DARK)
ref["A1"].alignment = center()
ref.row_dimensions[1].height = 28

col_heads = ["Index", "Formula", "Desired Value", "Interpretation",
             "Reference", "Sensitivity to High Yp"]
for j, h in enumerate(col_heads, start=1):
    c = ref.cell(row=2, column=j, value=h)
    c.font      = bold(10, WHITE)
    c.fill      = fill(GREEN_MID)
    c.alignment = center(wrap=True)
    c.border    = border()
ref.row_dimensions[2].height = 36

rows = [
    ("TOL",  "Yp − Ys",
     "Low",
     "Absolute yield reduction under stress; lower = more stable.",
     "Rosielle & Hamblin (1981)", "Insensitive"),
    ("MP",   "(Yp + Ys) / 2",
     "High",
     "Average productivity across both environments.",
     "Rosielle & Hamblin (1981)", "Sensitive"),
    ("GMP",  "√(Yp × Ys)",
     "High",
     "Geometric mean; penalises large differences between Yp and Ys.",
     "Fernandez (1992)", "Moderately sensitive"),
    ("STI",  "(Yp × Ys) / mean(Yp)²",
     "High",
     "Identifies genotypes with high yield under both conditions. "
     "STI > 1 = above average in both environments.",
     "Fernandez (1992)", "Sensitive"),
    ("SSI",  "(1 − Ys/Yp) / (1 − mean(Ys)/mean(Yp))",
     "Low  (< 1)",
     "Proportion of yield lost relative to population average. "
     "SSI < 1 = tolerant; SSI > 1 = sensitive.",
     "Fischer & Maurer (1978)", "Partially sensitive"),
    ("YSI",  "Ys / Yp",
     "High  (→ 1)",
     "Fraction of potential yield retained under stress. "
     "Closer to 1 = more tolerant.",
     "Bouslama & Schapaugh (1984)", "Insensitive"),
    ("HM",   "2·Yp·Ys / (Yp + Ys)",
     "High",
     "Harmonic mean; more sensitive to the lower of the two values.",
     "Kristin et al. (1993)", "Moderately sensitive"),
    ("YI",   "Ys / mean(Ys)",
     "High  (> 1)",
     "Relative stress yield compared to population mean. "
     "YI > 1 = above-average stress performance.",
     "Fischer & Maurer (1978)", "Insensitive"),
]

for i, row_data in enumerate(rows, start=3):
    row_fill = fill(WHITE) if i % 2 == 0 else fill(GREY_LIGHT)
    for j, val in enumerate(row_data, start=1):
        c = ref.cell(row=i, column=j, value=val)
        c.fill      = row_fill
        c.border    = border()
        c.alignment = center(wrap=True) if j in (1, 3, 5, 6) else left(wrap=True)
    ref.row_dimensions[i].height = 52

ref.column_dimensions["A"].width = 8
ref.column_dimensions["B"].width = 30
ref.column_dimensions["C"].width = 14
ref.column_dimensions["D"].width = 44
ref.column_dimensions["E"].width = 26
ref.column_dimensions["F"].width = 22


# ════════════════════════════════════════════════════════════════════════════
# SHEET 3 — How to Use
# ════════════════════════════════════════════════════════════════════════════
how = wb.create_sheet("How to Use")
how.sheet_view.showGridLines = False

how.merge_cells("A1:C1")
how["A1"].value     = "How to Use This Workbook with stress_tolerance_indices.R"
how["A1"].font      = Font(bold=True, size=13, color=WHITE)
how["A1"].fill      = fill(GREEN_DARK)
how["A1"].alignment = center()
how.row_dimensions[1].height = 28

steps = [
    ("Step 1", "Open the 'Data' sheet and replace the sample genotype names and "
               "values with your own.  Keep the column headers exactly as they are "
               "(Genotype, Yp, Ys)."),
    ("Step 2", "Yp = yield or trait value measured in the NON-STRESS environment.\n"
               "Ys = yield or trait value measured under the STRESS environment\n"
               "(drought, heat, salinity, waterlogging, etc.)."),
    ("Step 3", "Save the file as  sample_data.xlsx  in the same folder as the R script."),
    ("Step 4", "Open stress_tolerance_indices.R in RStudio (or any R IDE)."),
    ("Step 5", "Run the script.  It will:\n"
               "  • Read your data from this Excel file\n"
               "  • Calculate all 8 stress tolerance indices\n"
               "  • Print a ranked table to the Console\n"
               "  • Save results to  stress_tolerance_results.csv\n"
               "  • Save 4 publication-quality plots as PNG files"),
    ("Tip",    "You can add as many genotype rows as you need in the Data sheet.\n"
               "The R script handles any number of rows automatically."),
    ("Units",  "Yield is typically in t ha⁻¹ or g plant⁻¹, but any consistent unit works.\n"
               "All indices are unit-independent ratios or differences."),
    ("Required\nR packages",
               "readxl, ggplot2, reshape2, ggcorrplot, dplyr, ggrepel\n"
               "The script installs missing packages automatically on first run."),
]

for i, (label, text) in enumerate(steps, start=3):
    lc = how.cell(row=i, column=1, value=label)
    lc.font      = bold(10, WHITE)
    lc.fill      = fill(GREEN_MID)
    lc.alignment = center(wrap=True)
    lc.border    = border()

    tc = how.cell(row=i, column=2, value=text)
    tc.fill      = fill(WHITE) if i % 2 == 0 else fill(GREY_LIGHT)
    tc.alignment = left(wrap=True)
    tc.border    = border()
    how.row_dimensions[i].height = max(52, text.count("\n") * 18 + 26)

how.column_dimensions["A"].width = 18
how.column_dimensions["B"].width = 70
how.merge_cells("B1:C1")

wb.save("/home/user/BalaSivarathri.github.io/sample_data.xlsx")
print("sample_data.xlsx created successfully.")
