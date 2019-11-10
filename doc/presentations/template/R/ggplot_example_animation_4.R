library(ggplot2)

ggplot(subset(diamonds, color %in% c("D") & clarity %in% c("VVS2", "VVS1", "IF"))) +
 aes(x=carat) +
 aes(y=price) +
 aes(col=clarity) +
 facet_wrap(~cut) +
 geom_line() +
 ggsave("animation_4.pdf", width=4, height=3)
