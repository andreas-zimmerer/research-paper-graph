library(ggplot2)

ggplot(diamonds) +
 aes(x=carat) +
 aes(y=price) +
 facet_wrap(~cut) +
 geom_line() +
 ggsave("animation_1.pdf", width=4, height=3)
