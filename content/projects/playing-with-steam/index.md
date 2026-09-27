---
title: "Playing with Steam"
date: 2020-02-01
period: "January – February 2020"
summary: "Looking for trends in Steam data: what sells, what gets played, and how players cluster."
kind: tinkering
tags: [Python, Clustering, Data analysis]
figure: figure.svg
figure_caption: "A sketch of games plotted by critic rating and units sold per day on sale, with a fitted line. The vertical scale is logarithmic."
cover: fig-1.png
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/playSteam
aliases:
  - /posts_steam
  - /posts_steam.html
---

Looking for trends in Steam data.

![Scatter plot of units sold against critic rating with a linear and an exponential fit; colour shows days on sale.](fig-1.png "Units sold, normalised by days on sale, against critic rating.")

![Three correlation matrices: the whole dataset, the top 20% of single-player gamers and the top 20% of multiplayer gamers.](fig-2.png "Correlation between friendships, groups and play time, for all players and for the most active single-player and multiplayer gamers.")

![Total playtime in days plotted for each band of critic rating.](fig-3.png "Total playtime against critic rating.")

![Play time by genre, play time for the ten most-played titles, and heat maps of cluster labels against game title.](fig-4-5.png "Play time by genre and by title, and how clusters of players map on to the most-played games.")
