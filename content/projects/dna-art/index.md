---
title: "DNA art"
date: 2020-01-26
summary: "A small C++ program, with a Python notebook beside it, that paints a text file of genotype markers as an image, one pixel per letter."
kind: tinkering
tags: [C++, Python, Generative art]
status: paused
figure: figure.svg
figure_caption: "Each pair of letters in the list becomes two pixels, filled row by row. The side of the square image is set by the length of the list."
aliases:
  - /posts_dnaArt
  - /posts_dnaArt.html
---

A program that reads a text file of genotype markers and paints it as a picture. It began as a C++ project, which I came back to later.

The C++ version reads the file line by line and sizes a square image from the number of markers. Every letter has a fixed colour: one each for A, C, G and T, and two more for the other codes that turn up. Each marker has two letters and fills two pixels side by side, row after row, and the image is written out as an uncompressed TGA file. The Python notebook takes another view. It marks where the markers of one chromosome sit along its length and plots them as a band.

It is unfinished. In the current C++ source the drawing loop is commented out, and the program only prints an average for each of the first four chromosomes.
