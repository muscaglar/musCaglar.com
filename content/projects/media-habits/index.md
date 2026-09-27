---
title: "Predicting ad blocker use from media habits"
date: 2020-01-30
summary: "A notebook that asks whether answers to a survey about media habits can predict who uses an ad blocker, comparing four kinds of model."
kind: tinkering
tags: [Python, Data analysis, Machine learning]
status: finished
figure: figure.svg
figure_caption: "Ten features for each person go to a forest of decision trees, which vote on one answer. Three trees stand in for the hundred in the notebook."
---

A single Jupyter notebook that works through a survey about people's media habits. It asks one question: whether you can tell that someone uses an ad blocker from what they watch and read, and from a few demographics.

Most of the notebook is wrangling. The answers arrive as a spreadsheet of coded columns, which I reduce to ten normalised features: live and streamed television, print and web news, magazines, social media use, education, gender, household earnings and age. Four approaches follow. Linear regression over every subset of the features finds no linear relationship. Logistic regression reaches about 60% accuracy. K-means gives no meaningful clusters. A random forest of a hundred trees does best, and is checked against a baseline with a ROC curve and a confusion matrix.

The notebook ends with what I would change: less lumping together of answers, and better handling of the free-text fields.
