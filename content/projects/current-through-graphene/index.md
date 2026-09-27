---
title: "Current through graphene: can we do better than Ohm's law?"
date: 2019-09-01
summary: "Using Bayesian statistics to choose a model for charge flow across defects in graphene, then fitting it to experimental data."
kind: research
tags: [Python, R, Bayesian statistics, Regression]
figure: figure.svg
figure_caption: "A sketch of current against voltage, with the straight line of Ohm's law and a curved model drawn through the same points. The points are illustrative."
cover: bayes-linear.png
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/GHK_fit
aliases:
  - /posts_GHK
  - /posts_GHK.html
---

Bayesian statistics is used to determine a favourable model for the charge flow across defects in graphene. Following this, R is used to perform non-linear regression to fit to experimental data and extract fitting statistics.

![Left: a cloud of posterior samples for two parameters with contour lines. Right: data points with a fitted straight line and a shaded uncertainty band.](bayes-linear.png "Posterior samples for the two parameters of a linear model, and the resulting fit with its uncertainty band.")
