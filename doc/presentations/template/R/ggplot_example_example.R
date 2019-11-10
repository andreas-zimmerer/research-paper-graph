library(ggplot2)
theme_set(theme_classic())

# Colorblind-friendly palette
cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

# Plot
ggplot(mpg) +
  aes(x=cty) +
  geom_density(aes(fill=factor(cyl)), alpha=0.8) +
  labs(title="Density plot") +
  labs(caption="Source: mpg") +
  labs(x="City Mileage") +
  labs(fill="# Cylinders") +
  scale_fill_manual(values=cbPalette) +
  facet_wrap(~ drv) + 
  labs(subtitle="City Mileage Grouped by Number of cylinders, split by drive type") +
  ggsave("example.pdf", width=4, height=3)
