library(ggplot2)

ggplot(subset(diamonds, color %in% c("D"))) +
 aes(x=carat) +
 aes(y=price) +
 aes(col=clarity) +
 facet_wrap(~cut) +
 geom_line() +
 ggsave("animation_3.pdf", width=4, height=3)
