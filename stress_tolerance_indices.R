# ============================================================
#  Plant Stress Tolerance Indices — Analysis Script
#  Author : Bala Subramanyam Sivarathri
#  Contact: balasubramanyamsivarathri@gmail.com
#  Ref    : Fernandez (1992), Fischer & Maurer (1978),
#           Rosielle & Hamblin (1981), Bouslama & Schapaugh (1984)
# ============================================================

# ---- 0. Required packages ----------------------------------
if (!requireNamespace("ggplot2",  quietly = TRUE)) install.packages("ggplot2")
if (!requireNamespace("reshape2", quietly = TRUE)) install.packages("reshape2")
if (!requireNamespace("ggcorrplot", quietly = TRUE)) install.packages("ggcorrplot")
if (!requireNamespace("dplyr",    quietly = TRUE)) install.packages("dplyr")
if (!requireNamespace("ggrepel",  quietly = TRUE)) install.packages("ggrepel")

library(ggplot2)
library(reshape2)
library(ggcorrplot)
library(dplyr)
library(ggrepel)

# ============================================================
# 1. INPUT DATA
#    Yp = yield (or trait value) under non-stress (potential)
#    Ys = yield (or trait value) under stress
#    Replace with your actual genotype data.
# ============================================================
data <- data.frame(
  Genotype = c("G1",  "G2",  "G3",  "G4",  "G5",
               "G6",  "G7",  "G8",  "G9",  "G10"),
  Yp       = c(4.20,  3.85,  4.60,  3.50,  4.10,
               5.00,  3.70,  4.80,  4.30,  3.95),   # non-stress environment
  Ys       = c(2.80,  2.60,  2.50,  2.40,  3.00,
               2.70,  2.20,  3.10,  2.90,  2.50)    # stress environment
)

# ============================================================
# 2. COMPUTE STRESS TOLERANCE INDICES
# ============================================================

# Population means
Yp_bar <- mean(data$Yp)
Ys_bar <- mean(data$Ys)

data <- data %>%
  mutate(
    # --- Rosielle & Hamblin (1981) ---
    TOL = Yp - Ys,                              # Tolerance
    MP  = (Yp + Ys) / 2,                        # Mean Productivity

    # --- Fernandez (1992) ---
    GMP = sqrt(Yp * Ys),                        # Geometric Mean Productivity
    STI = (Yp * Ys) / (Yp_bar^2),              # Stress Tolerance Index

    # --- Fischer & Maurer (1978) ---
    SSI = (1 - (Ys / Yp)) / (1 - (Ys_bar / Yp_bar)),  # Stress Susceptibility Index

    # --- Bouslama & Schapaugh (1984) ---
    YSI = Ys / Yp,                              # Yield Stability Index

    # --- Harmonic Mean (Kristin et al. 1993) ---
    HM  = (2 * Yp * Ys) / (Yp + Ys),

    # --- Yield Index ---
    YI  = Ys / Ys_bar                           # Yield Index
  )

# ============================================================
# 3. PRINT RESULTS TABLE
# ============================================================
cat("\n========== Stress Tolerance Indices ==========\n")
print(data, digits = 3, row.names = FALSE)

cat("\n--- Population means ---\n")
cat(sprintf("  Mean Yp (non-stress) : %.3f\n", Yp_bar))
cat(sprintf("  Mean Ys (stress)     : %.3f\n\n", Ys_bar))

# ============================================================
# 4. RANKING (based on STI — higher = more tolerant)
# ============================================================
data$Rank_STI <- rank(-data$STI)
data$Rank_GMP <- rank(-data$GMP)
data$Rank_MP  <- rank(-data$MP)

cat("--- Genotype rankings by STI (1 = most tolerant) ---\n")
print(data[order(data$Rank_STI), c("Genotype","STI","GMP","MP","SSI","YSI","Rank_STI")],
      digits = 3, row.names = FALSE)

# ============================================================
# 5. VISUALISATIONS
# ============================================================

# 5a. Bar chart of all indices (scaled 0–1 for comparability)
idx_cols <- c("TOL","MP","GMP","STI","SSI","YSI","HM","YI")

scaled <- data %>%
  select(Genotype, all_of(idx_cols)) %>%
  mutate(across(all_of(idx_cols), ~ (.x - min(.x)) / (max(.x) - min(.x))))

long <- melt(scaled, id.vars = "Genotype",
             variable.name = "Index", value.name = "Value")

p_bar <- ggplot(long, aes(x = Genotype, y = Value, fill = Index)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_brewer(palette = "Set2") +
  labs(title    = "Scaled Stress Tolerance Indices by Genotype",
       subtitle = "All indices normalised to [0, 1] for visual comparison",
       x = "Genotype", y = "Scaled Index Value", fill = "Index") +
  theme_bw(base_size = 12) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

print(p_bar)
ggsave("sti_bar_chart.png", p_bar, width = 10, height = 5, dpi = 150)

# 5b. Biplot: Yp vs Ys coloured by STI
p_biplot <- ggplot(data, aes(x = Yp, y = Ys, colour = STI, label = Genotype)) +
  geom_point(size = 4) +
  geom_text_repel(size = 3.5) +
  scale_colour_gradient(low = "#d73027", high = "#1a9850") +
  geom_vline(xintercept = Yp_bar, linetype = "dashed", colour = "grey50") +
  geom_hline(yintercept = Ys_bar, linetype = "dashed", colour = "grey50") +
  labs(title    = "Yp vs Ys Biplot — Stress Tolerance Index (STI)",
       subtitle = "Dashed lines = population means; green = high STI",
       x = "Yield under Non-Stress (Yp)",
       y = "Yield under Stress (Ys)",
       colour = "STI") +
  theme_bw(base_size = 12)

print(p_biplot)
ggsave("sti_biplot.png", p_biplot, width = 7, height = 6, dpi = 150)

# 5c. Correlation heatmap among indices
cor_mat <- cor(data[, idx_cols], use = "complete.obs")

p_corr <- ggcorrplot(cor_mat,
  method    = "circle",
  type      = "lower",
  lab       = TRUE,
  lab_size  = 3,
  colors    = c("#d73027", "white", "#1a9850"),
  title     = "Correlation Among Stress Tolerance Indices",
  ggtheme   = theme_bw(base_size = 11))

print(p_corr)
ggsave("sti_correlation.png", p_corr, width = 7, height = 6, dpi = 150)

# 5d. STI lollipop chart
p_lollipop <- ggplot(data, aes(x = reorder(Genotype, STI), y = STI)) +
  geom_segment(aes(xend = Genotype, yend = 0), colour = "grey60") +
  geom_point(aes(colour = STI), size = 5) +
  scale_colour_gradient(low = "#d73027", high = "#1a9850") +
  coord_flip() +
  labs(title  = "Stress Tolerance Index (STI) — Genotype Ranking",
       x = "Genotype", y = "STI", colour = "STI") +
  theme_bw(base_size = 12)

print(p_lollipop)
ggsave("sti_lollipop.png", p_lollipop, width = 7, height = 5, dpi = 150)

# ============================================================
# 6. CLASSIFICATION (quadrant method — Fernandez 1992)
#    Q1 high Yp & high Ys → tolerant & high yielding (ideal)
#    Q2 low  Yp & high Ys → tolerant but low yielding
#    Q3 low  Yp & low  Ys → sensitive & low yielding
#    Q4 high Yp & low  Ys → sensitive but high yielding under no-stress
# ============================================================
data <- data %>%
  mutate(
    Quadrant = case_when(
      Yp >= Yp_bar & Ys >= Ys_bar ~ "Q1: Tolerant & High-yielding",
      Yp <  Yp_bar & Ys >= Ys_bar ~ "Q2: Tolerant & Low-yielding",
      Yp <  Yp_bar & Ys <  Ys_bar ~ "Q3: Sensitive & Low-yielding",
      Yp >= Yp_bar & Ys <  Ys_bar ~ "Q4: Sensitive & High-yielding"
    )
  )

cat("\n--- Fernandez (1992) Quadrant Classification ---\n")
print(data[, c("Genotype","Yp","Ys","STI","Quadrant")],
      row.names = FALSE)

# ============================================================
# 7. EXPORT FULL RESULTS
# ============================================================
write.csv(data, "stress_tolerance_results.csv", row.names = FALSE)
cat("\nResults saved to  : stress_tolerance_results.csv\n")
cat("Plots saved to    : sti_bar_chart.png, sti_biplot.png,\n")
cat("                    sti_correlation.png, sti_lollipop.png\n\n")

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
