# ============================================================
#  Plant Stress Tolerance Indices — Multi-Trait Analysis
#  Author : Bala Subramanyam Sivarathri
#  Contact: balasubramanyamsivarathri@gmail.com
#  Ref    : Fernandez (1992), Fischer & Maurer (1978),
#           Rosielle & Hamblin (1981), Bouslama & Schapaugh (1984)
# ============================================================

# ---- 0. Required packages ----------------------------------
pkgs <- c("readxl", "openxlsx", "ggplot2", "reshape2",
          "ggcorrplot", "dplyr", "ggrepel")
for (p in pkgs) if (!requireNamespace(p, quietly = TRUE)) install.packages(p)

library(readxl)
library(openxlsx)
library(ggplot2)
library(reshape2)
library(ggcorrplot)
library(dplyr)
library(ggrepel)

# ============================================================
# 1. INPUT — read from Excel
#    Column naming rule:  TraitName_Yp  |  TraitName_Ys
#    Add as many trait pairs as needed; all are detected automatically.
# ============================================================
EXCEL_FILE <- "sample_data.xlsx"
SHEET_NAME <- "Data"

if (!file.exists(EXCEL_FILE))
  stop(paste("Excel file not found:", EXCEL_FILE,
             "\nWorking directory:", getwd()))

raw  <- read_excel(EXCEL_FILE, sheet = SHEET_NAME, skip = 3)  # skip title + trait-group rows
data <- as.data.frame(raw)
data <- data[complete.cases(data["Genotype"]), ]               # drop empty buffer rows

# --- auto-detect trait pairs (columns ending in _Yp with a matching _Ys) ---
yp_cols <- grep("_Yp$", colnames(data), value = TRUE)
ys_cols <- sub("_Yp$", "_Ys", yp_cols)
valid   <- ys_cols %in% colnames(data)

if (!any(valid))
  stop("No valid trait pairs found. Columns must follow the pattern TraitName_Yp / TraitName_Ys.")

yp_cols <- yp_cols[valid]
ys_cols <- ys_cols[valid]
traits  <- sub("_Yp$", "", yp_cols)

# convert all trait columns to numeric
for (col in c(yp_cols, ys_cols))
  data[[col]] <- suppressWarnings(as.numeric(data[[col]]))

cat(sprintf("\nLoaded %d genotypes | %d traits detected: %s\n\n",
            nrow(data), length(traits), paste(traits, collapse = ", ")))

# ============================================================
# 2. FUNCTION — compute all 8 indices for one trait
# ============================================================
compute_indices <- function(Genotype, Yp, Ys) {
  Yp_bar <- mean(Yp, na.rm = TRUE)
  Ys_bar <- mean(Ys, na.rm = TRUE)

  df <- data.frame(
    Genotype = Genotype,
    Yp       = Yp,
    Ys       = Ys,
    TOL      = Yp - Ys,
    MP       = (Yp + Ys) / 2,
    GMP      = sqrt(Yp * Ys),
    STI      = (Yp * Ys) / (Yp_bar^2),
    SSI      = (1 - Ys / Yp) / (1 - Ys_bar / Yp_bar),
    YSI      = Ys / Yp,
    HM       = (2 * Yp * Ys) / (Yp + Ys),
    YI       = Ys / Ys_bar
  )
  df$Rank_STI <- rank(-df$STI, na.last = "keep")
  df$Quadrant <- with(df, case_when(
    Yp >= Yp_bar & Ys >= Ys_bar ~ "Q1: Tolerant & High-yielding",
    Yp <  Yp_bar & Ys >= Ys_bar ~ "Q2: Tolerant & Low-yielding",
    Yp <  Yp_bar & Ys <  Ys_bar ~ "Q3: Sensitive & Low-yielding",
    Yp >= Yp_bar & Ys <  Ys_bar ~ "Q4: Sensitive & High-yielding"
  ))
  attr(df, "Yp_bar") <- Yp_bar
  attr(df, "Ys_bar") <- Ys_bar
  df
}

# ============================================================
# 3. RUN FOR ALL TRAITS
# ============================================================
idx_cols   <- c("TOL","MP","GMP","STI","SSI","YSI","HM","YI")
results    <- list()  # one data.frame per trait

for (trait in traits) {
  Yp   <- data[[paste0(trait, "_Yp")]]
  Ys   <- data[[paste0(trait, "_Ys")]]
  res  <- compute_indices(data$Genotype, Yp, Ys)
  results[[trait]] <- res

  cat(sprintf("══════════════ %s ══════════════\n", trait))
  cat(sprintf("  Mean Yp: %.3f  |  Mean Ys: %.3f\n",
              attr(res,"Yp_bar"), attr(res,"Ys_bar")))
  print(res[order(res$Rank_STI),
            c("Genotype","Yp","Ys","STI","GMP","SSI","YSI","Rank_STI","Quadrant")],
        digits = 3, row.names = FALSE)
  cat("\n")
}

# ============================================================
# 4. CROSS-TRAIT STI SUMMARY TABLE
# ============================================================
sti_summary <- Reduce(function(a, b) merge(a, b, by = "Genotype", all = TRUE),
  lapply(traits, function(t) {
    d <- results[[t]][, c("Genotype","STI")]
    colnames(d)[2] <- t
    d
  })
)
cat("══════════ Cross-Trait STI Summary ══════════\n")
print(sti_summary, digits = 3, row.names = FALSE)

# ============================================================
# 5. VISUALISATIONS
# ============================================================

# ---- helper: min-max scale --------------------------------------------------
minmax <- function(x) {
  r <- max(x, na.rm = TRUE) - min(x, na.rm = TRUE)
  if (r == 0) return(rep(0, length(x)))
  (x - min(x, na.rm = TRUE)) / r
}

# ---- 5a. Per-trait plots ----------------------------------------------------
for (trait in traits) {
  res    <- results[[trait]]
  Yp_bar <- attr(res, "Yp_bar")
  Ys_bar <- attr(res, "Ys_bar")

  # Biplot: Yp vs Ys coloured by STI
  p_bi <- ggplot(res, aes(x = Yp, y = Ys, colour = STI, label = Genotype)) +
    geom_point(size = 4) +
    geom_text_repel(size = 3.2) +
    scale_colour_gradient(low = "#d73027", high = "#1a9850") +
    geom_vline(xintercept = Yp_bar, linetype = "dashed", colour = "grey50") +
    geom_hline(yintercept = Ys_bar, linetype = "dashed", colour = "grey50") +
    labs(title    = paste(trait, "— Yp vs Ys Biplot"),
         subtitle = "Dashed lines = population means | green = high STI",
         x = paste(trait, "(Non-Stress)"),
         y = paste(trait, "(Stress)"),
         colour = "STI") +
    theme_bw(base_size = 11)

  ggsave(paste0(trait, "_biplot.png"), p_bi, width = 7, height = 5.5, dpi = 150)

  # Lollipop: STI ranking
  p_lol <- ggplot(res, aes(x = reorder(Genotype, STI), y = STI)) +
    geom_segment(aes(xend = Genotype, yend = 0), colour = "grey65") +
    geom_point(aes(colour = STI), size = 5) +
    scale_colour_gradient(low = "#d73027", high = "#1a9850") +
    coord_flip() +
    labs(title  = paste(trait, "— STI Ranking"),
         x = "Genotype", y = "STI", colour = "STI") +
    theme_bw(base_size = 11)

  ggsave(paste0(trait, "_lollipop.png"), p_lol, width = 6, height = 5, dpi = 150)
}

# ---- 5b. Scaled bar chart — all indices for each genotype (faceted by trait) ---
long_all <- do.call(rbind, lapply(traits, function(t) {
  df <- results[[t]] %>%
    select(Genotype, all_of(idx_cols)) %>%
    mutate(across(all_of(idx_cols), minmax))
  melt(df, id.vars = "Genotype", variable.name = "Index", value.name = "Value") %>%
    mutate(Trait = t)
}))

p_facet <- ggplot(long_all, aes(x = Genotype, y = Value, fill = Index)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_brewer(palette = "Set2") +
  facet_wrap(~ Trait, ncol = 2) +
  labs(title    = "Scaled Stress Tolerance Indices — All Traits",
       subtitle = "Indices normalised to [0,1] within each trait",
       x = "Genotype", y = "Scaled Value", fill = "Index") +
  theme_bw(base_size = 10) +
  theme(axis.text.x  = element_text(angle = 45, hjust = 1),
        strip.text    = element_text(face = "bold"))

ggsave("all_traits_bar_chart.png", p_facet,
       width = 5 * min(length(traits), 2), height = 4 * ceiling(length(traits) / 2),
       dpi = 150)

# ---- 5c. Cross-trait STI heatmap -------------------------------------------
sti_mat <- as.data.frame(sti_summary)
rownames(sti_mat) <- sti_mat$Genotype
sti_mat$Genotype  <- NULL
sti_long <- melt(as.matrix(sti_mat), varnames = c("Genotype","Trait"),
                 value.name = "STI")

p_heat <- ggplot(sti_long, aes(x = Trait, y = Genotype, fill = STI)) +
  geom_tile(colour = "white", linewidth = 0.5) +
  geom_text(aes(label = round(STI, 2)), size = 3) +
  scale_fill_gradient2(low = "#d73027", mid = "white", high = "#1a9850",
                       midpoint = median(sti_long$STI, na.rm = TRUE)) +
  labs(title = "STI Heatmap — All Traits × All Genotypes",
       x = "Trait", y = "Genotype", fill = "STI") +
  theme_bw(base_size = 11) +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

ggsave("cross_trait_STI_heatmap.png", p_heat, width = 8, height = 6, dpi = 150)

# ============================================================
# 6. EXPORT RESULTS
# ============================================================

# --- 6a. Long-format CSV (all traits combined) ------------------------------
long_csv <- do.call(rbind, lapply(traits, function(t) {
  cbind(Trait = t, results[[t]])
}))
write.csv(long_csv, "stress_tolerance_results.csv", row.names = FALSE)

# --- 6b. Excel workbook — one sheet per trait + cross-trait summary ---------
wb_out <- createWorkbook()

# header style helpers
hs <- createStyle(fontColour = "#FFFFFF", fgFill = "#1a5e38",
                  halign = "CENTER", textDecoration = "Bold", border = "TopBottomLeftRight")
ds <- createStyle(border = "TopBottomLeftRight", halign = "CENTER")
alt_fill <- createStyle(fgFill = "#f5f5f5", border = "TopBottomLeftRight", halign = "CENTER")

for (trait in traits) {
  addWorksheet(wb_out, trait)
  df_out <- results[[trait]]
  writeData(wb_out, trait, df_out, headerStyle = hs)
  addStyle(wb_out, trait, ds,      rows = 2:(nrow(df_out)+1), cols = 1:ncol(df_out), gridExpand = TRUE)
  addStyle(wb_out, trait, alt_fill, rows = seq(3, nrow(df_out)+1, 2), cols = 1:ncol(df_out), gridExpand = TRUE)
  setColWidths(wb_out, trait, cols = 1:ncol(df_out), widths = "auto")
}

# Cross-trait summary sheet
addWorksheet(wb_out, "Cross-Trait STI")
writeData(wb_out, "Cross-Trait STI", sti_summary, headerStyle = hs)
addStyle(wb_out, "Cross-Trait STI", ds, rows = 2:(nrow(sti_summary)+1),
         cols = 1:ncol(sti_summary), gridExpand = TRUE)
setColWidths(wb_out, "Cross-Trait STI", cols = 1:ncol(sti_summary), widths = "auto")

saveWorkbook(wb_out, "stress_tolerance_results.xlsx", overwrite = TRUE)

# ---- summary message -------------------------------------------------------
cat("══════════════════════════════════════════════\n")
cat("Results saved to:\n")
cat("  stress_tolerance_results.csv\n")
cat("  stress_tolerance_results.xlsx\n")
cat(sprintf("Plots saved: %d trait biplots, %d lollipops,\n",
            length(traits), length(traits)))
cat("  all_traits_bar_chart.png, cross_trait_STI_heatmap.png\n\n")

# ============================================================
# INDEX FORMULAE REFERENCE
# ============================================================
# TOL = Yp - Ys                                (Rosielle & Hamblin 1981)
# MP  = (Yp + Ys) / 2                          (Rosielle & Hamblin 1981)
# GMP = sqrt(Yp * Ys)                          (Fernandez 1992)
# STI = (Yp * Ys) / mean(Yp)^2                (Fernandez 1992)
# SSI = (1 - Ys/Yp) / (1 - mean(Ys)/mean(Yp)) (Fischer & Maurer 1978)
# YSI = Ys / Yp                                (Bouslama & Schapaugh 1984)
# HM  = 2*Yp*Ys / (Yp + Ys)                   (Kristin et al. 1993)
# YI  = Ys / mean(Ys)                          (Fischer & Maurer 1978)
