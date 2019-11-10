library(ggplot2)

ggplot(subset(diamonds, color %in% c("D"))) +
 aes(x=carat) +
 aes(y=price) +
 facet_wrap(~cut) +
 geom_line() +
 ggsave("animation_2.pdf", width=4, height=3)
