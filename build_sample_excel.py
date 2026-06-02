"""
Generates  sample_data.xlsx  — multi-trait input template for stress_tolerance_indices.R
Columns: Genotype | TraitName_Yp | TraitName_Ys  (one pair per trait, as many as needed)
Run once:  python3 build_sample_excel.py
"""

from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()

GREEN_DARK   = "1a5e38"
GREEN_MID    = "5a8a5e"
GREEN_LIGHT  = "c8e6c9"
BLUE_DARK    = "1a3a5e"
BLUE_MID     = "3a6a9e"
BLUE_LIGHT   = "c8d8f0"
GREY_LIGHT   = "f5f5f5"
WHITE        = "ffffff"
ORANGE_LIGHT = "fff3e0"

TRAIT_COLORS = [
    ("1a5e38", "c8e6c9"),   # green
    ("1a3a5e", "c8d8f0"),   # blue
    ("5e1a1a", "f0c8c8"),   # red
    ("5e4a1a", "f0e4c8"),   # brown
    ("3a1a5e", "dcc8f0"),   # purple
]

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
# SHEET 1 — Data  (multi-trait wide format)
# ════════════════════════════════════════════════════════════════════════════
ws = wb.active
ws.title = "Data"
ws.sheet_view.showGridLines = False

# --- sample traits (soybean-relevant) ---
traits = [
    "GrainYield",       # t ha-1
    "PlantHeight",      # cm
    "SPAD",             # chlorophyll index
    "SeedWeight",       # g per 100 seeds
    "Biomass",          # t ha-1
]

# Sample data  [Genotype, GY_Yp, GY_Ys, PH_Yp, PH_Ys, SPAD_Yp, SPAD_Ys, SW_Yp, SW_Ys, BM_Yp, BM_Ys]
sample = [
    ("G1",  4.20, 2.80,  92.0, 78.0,  44.2, 36.1,  18.5, 14.2,  8.10, 5.80),
    ("G2",  3.85, 2.60,  88.0, 74.0,  42.8, 33.5,  17.2, 12.8,  7.60, 5.20),
    ("G3",  4.60, 2.50,  95.0, 80.0,  45.6, 34.8,  19.0, 13.5,  8.90, 5.50),
    ("G4",  3.50, 2.40,  84.0, 70.0,  40.1, 32.0,  16.5, 12.1,  7.00, 4.90),
    ("G5",  4.10, 3.00,  90.0, 79.0,  43.5, 37.2,  18.0, 14.8,  7.90, 6.10),
    ("G6",  5.00, 2.70,  98.0, 82.0,  47.0, 35.5,  20.1, 13.9,  9.50, 5.60),
    ("G7",  3.70, 2.20,  86.0, 71.0,  41.3, 31.0,  16.8, 11.5,  7.20, 4.60),
    ("G8",  4.80, 3.10,  96.0, 83.0,  46.1, 38.0,  19.5, 15.2,  9.10, 6.30),
    ("G9",  4.30, 2.90,  91.0, 80.0,  44.8, 37.5,  18.3, 14.6,  8.30, 5.90),
    ("G10", 3.95, 2.50,  89.0, 75.0,  43.0, 33.8,  17.5, 12.6,  7.75, 5.10),
]

# total columns = 1 (Genotype) + 2 * len(traits)
total_cols = 1 + 2 * len(traits)

# --- title row (row 1) -------------------------------------------------------
ws.merge_cells(start_row=1, start_column=1,
               end_row=1,   end_column=total_cols)
ws.cell(1, 1).value     = "Plant Stress Tolerance Indices — Multi-Trait Input Data"
ws.cell(1, 1).font      = Font(bold=True, size=14, color=WHITE)
ws.cell(1, 1).fill      = fill(GREEN_DARK)
ws.cell(1, 1).alignment = center()
ws.row_dimensions[1].height = 28

# --- instruction row (row 2) -------------------------------------------------
ws.merge_cells(start_row=2, start_column=1,
               end_row=2,   end_column=total_cols)
ws.cell(2, 1).value = (
    "Add or rename trait columns following the pattern  TraitName_Yp  /  TraitName_Ys. "
    "Yp = non-stress value, Ys = stress value. The R script detects all pairs automatically."
)
ws.cell(2, 1).font      = Font(italic=True, size=10, color="444444")
ws.cell(2, 1).fill      = fill(GREEN_LIGHT)
ws.cell(2, 1).alignment = left(wrap=True)
ws.row_dimensions[2].height = 30

# --- trait group header (row 3) — merged pairs per trait --------------------
ws.cell(3, 1).value     = ""
ws.cell(3, 1).fill      = fill(GREEN_DARK)
ws.cell(3, 1).border    = border()

for t_idx, trait in enumerate(traits):
    col_start = 2 + t_idx * 2          # 1-based
    col_end   = col_start + 1
    dark, light = TRAIT_COLORS[t_idx % len(TRAIT_COLORS)]
    ws.merge_cells(start_row=3, start_column=col_start,
                   end_row=3,   end_column=col_end)
    c = ws.cell(3, col_start)
    c.value     = trait
    c.font      = Font(bold=True, size=11, color=WHITE)
    c.fill      = fill(dark)
    c.alignment = center()
    c.border    = border()
ws.row_dimensions[3].height = 22

# --- column headers (row 4) — Genotype | Trait_Yp | Trait_Ys ... -----------
c = ws.cell(4, 1, "Genotype")
c.font      = bold(11, WHITE)
c.fill      = fill(GREEN_DARK)
c.alignment = center()
c.border    = border()

for t_idx, trait in enumerate(traits):
    dark, light = TRAIT_COLORS[t_idx % len(TRAIT_COLORS)]
    for sub, label in enumerate(["_Yp\n(Non-Stress)", "_Ys\n(Stress)"]):
        col = 2 + t_idx * 2 + sub
        c = ws.cell(4, col, trait + label)
        c.font      = Font(bold=True, size=10, color=WHITE)
        c.fill      = fill(dark)
        c.alignment = center(wrap=True)
        c.border    = border()
ws.row_dimensions[4].height = 38

# --- data rows (rows 5–14) --------------------------------------------------
for r_idx, row_data in enumerate(sample, start=5):
    row_fill = fill(WHITE) if r_idx % 2 == 0 else fill(GREY_LIGHT)
    for c_idx, val in enumerate(row_data, start=1):
        c = ws.cell(r_idx, c_idx, val)
        c.fill      = row_fill
        c.border    = border()
        c.alignment = center() if c_idx > 1 else left()
        if c_idx > 1:
            c.number_format = "0.00"
    ws.row_dimensions[r_idx].height = 18

# --- empty buffer rows (15–24) ----------------------------------------------
for r_idx in range(15, 25):
    row_fill = fill(WHITE) if r_idx % 2 == 0 else fill(GREY_LIGHT)
    for c_idx in range(1, total_cols + 1):
        c = ws.cell(r_idx, c_idx)
        c.fill      = row_fill
        c.border    = border()
        c.alignment = center() if c_idx > 1 else left()

# --- column widths ----------------------------------------------------------
ws.column_dimensions["A"].width = 14
for col_num in range(2, total_cols + 1):
    ws.column_dimensions[get_column_letter(col_num)].width = 16

ws.freeze_panes = "B5"   # freeze Genotype column + header rows


# ════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Index Reference  (same as before, unchanged)
# ════════════════════════════════════════════════════════════════════════════
ref = wb.create_sheet("Index Reference")
ref.sheet_view.showGridLines = False

ref.merge_cells("A1:F1")
ref["A1"].value     = "Stress Tolerance Index Formulae & Interpretation"
ref["A1"].font      = Font(bold=True, size=14, color=WHITE)
ref["A1"].fill      = fill(GREEN_DARK)
ref["A1"].alignment = center()
ref.row_dimensions[1].height = 28

col_heads = ["Index", "Formula", "Desired Value",
             "Interpretation", "Reference", "Sensitivity to High Yp"]
for j, h in enumerate(col_heads, start=1):
    c = ref.cell(2, j, h)
    c.font      = bold(10, WHITE)
    c.fill      = fill(GREEN_MID)
    c.alignment = center(wrap=True)
    c.border    = border()
ref.row_dimensions[2].height = 36

index_rows = [
    ("TOL",  "Yp − Ys",                               "Low",
     "Absolute yield reduction under stress; lower = more stable.",
     "Rosielle & Hamblin (1981)",   "Insensitive"),
    ("MP",   "(Yp + Ys) / 2",                          "High",
     "Average productivity across both environments.",
     "Rosielle & Hamblin (1981)",   "Sensitive"),
    ("GMP",  "√(Yp × Ys)",                             "High",
     "Geometric mean; penalises large differences between Yp and Ys.",
     "Fernandez (1992)",            "Moderately sensitive"),
    ("STI",  "(Yp × Ys) / mean(Yp)²",                 "High",
     "Identifies genotypes with high yield under both conditions. STI > 1 = above average in both.",
     "Fernandez (1992)",            "Sensitive"),
    ("SSI",  "(1 − Ys/Yp) / (1 − mean(Ys)/mean(Yp))", "Low (< 1)",
     "Proportion lost relative to population. SSI < 1 = tolerant; SSI > 1 = sensitive.",
     "Fischer & Maurer (1978)",     "Partially sensitive"),
    ("YSI",  "Ys / Yp",                                "High (→ 1)",
     "Fraction of potential yield retained. Closer to 1 = more tolerant.",
     "Bouslama & Schapaugh (1984)", "Insensitive"),
    ("HM",   "2·Yp·Ys / (Yp + Ys)",                   "High",
     "Harmonic mean; more sensitive to the lower of the two values.",
     "Kristin et al. (1993)",       "Moderately sensitive"),
    ("YI",   "Ys / mean(Ys)",                          "High (> 1)",
     "Relative stress performance vs. population mean. YI > 1 = above-average stress yield.",
     "Fischer & Maurer (1978)",     "Insensitive"),
]
for i, row_data in enumerate(index_rows, start=3):
    rf = fill(WHITE) if i % 2 == 0 else fill(GREY_LIGHT)
    for j, val in enumerate(row_data, start=1):
        c = ref.cell(i, j, val)
        c.fill      = rf
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

how.merge_cells("A1:B1")
how["A1"].value     = "How to Use This Workbook with stress_tolerance_indices.R"
how["A1"].font      = Font(bold=True, size=13, color=WHITE)
how["A1"].fill      = fill(GREEN_DARK)
how["A1"].alignment = center()
how.row_dimensions[1].height = 28

steps = [
    ("Column naming\nrule",
     "Each trait needs exactly TWO columns: TraitName_Yp (non-stress) and TraitName_Ys (stress).\n"
     "Example: GrainYield_Yp | GrainYield_Ys\n"
     "The R script detects all pairs automatically — add as many traits as you need."),
    ("Step 1",
     "Replace or add trait column pairs in the 'Data' sheet following the naming rule above.\n"
     "Keep 'Genotype' as the first column."),
    ("Step 2",
     "Fill in Yp and Ys values for every genotype × trait combination.\n"
     "Leave a cell blank only if data is truly missing (the script skips missing values)."),
    ("Step 3",
     "Save the file as  sample_data.xlsx  in the same folder as the R script."),
    ("Step 4",
     "Open  stress_tolerance_indices.R  in RStudio and run it.\n"
     "The script will process ALL traits in one go automatically."),
    ("Outputs",
     "• stress_tolerance_results.xlsx — one sheet per trait + a cross-trait summary sheet\n"
     "• stress_tolerance_results.csv  — long-format CSV with all results\n"
     "• PNG plots for each trait (bar chart, biplot, lollipop)\n"
     "• One combined heatmap comparing STI across all traits"),
    ("Required\nR packages",
     "readxl, openxlsx, ggplot2, reshape2, ggcorrplot, dplyr, ggrepel\n"
     "All missing packages are installed automatically on first run."),
    ("Tip",
     "You can rename the sample traits (GrainYield, PlantHeight, etc.) to match your experiment.\n"
     "Any number of genotypes and any number of traits are supported."),
]

for i, (label, text) in enumerate(steps, start=3):
    lc = how.cell(i, 1, label)
    lc.font      = bold(10, WHITE)
    lc.fill      = fill(GREEN_MID)
    lc.alignment = center(wrap=True)
    lc.border    = border()

    tc = how.cell(i, 2, text)
    tc.fill      = fill(WHITE) if i % 2 == 0 else fill(GREY_LIGHT)
    tc.alignment = left(wrap=True)
    tc.border    = border()
    how.row_dimensions[i].height = max(52, text.count("\n") * 18 + 26)

how.column_dimensions["A"].width = 18
how.column_dimensions["B"].width = 72

wb.save("/home/user/BalaSivarathri.github.io/sample_data.xlsx")
print("sample_data.xlsx (multi-trait) created successfully.")
