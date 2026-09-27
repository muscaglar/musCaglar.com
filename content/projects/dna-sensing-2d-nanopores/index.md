---
title: "DNA sensing through 2D nanopores"
date: 2020-01-26
summary: "Finding DNA translocations in noisy nanopore current recordings: filtering, event detection and clustering."
kind: research
tags: [Python, Signal processing, Clustering, Nanopores]
figure: figure.svg
figure_caption: "A strand of DNA passing through a nanopore, beside the current measured across it. The current dips while the strand is in the pore, and that dip is what the analysis looks for in the noise."
cover: current-trace-analysis.png
links:
  - name: Python code on GitHub
    url: https://github.com/muscaglar/DNA
  - name: Matlab code on GitHub
    url: https://github.com/muscaglar/neroli
aliases:
  - /posts_DNA
  - /posts_DNA.html
---

DNA translocation through nanopores can be studied by applying a voltage and measuring the current — 'resistive pulse sensing'. In order to increase the resolution of such systems, nanopores in 2D membranes could be used; however, these are inherently noisy. With many terabytes of noisy data, a trained CNN could be used to detangle the translocations from the noise.

![Schematic: a strand of DNA is drawn through a nanopore while a voltage is applied across it and the current is measured.](resistive-pulse.png "Resistive pulse measurements for DNA translocations.")

![Four panels: the raw current trace, the filtered trace, peak finding, and mean thresholding.](current-trace-analysis.png "Current trace and analysis of DNA translocations through glass nanopores.")

![A single event shown raw, low-pass filtered, as a gradient and with features found, next to a typical event and two edge cases: folded DNA and knots.](event-filtering.png "Filtering of a single translocation event, and examples of edge cases.")

![Scatter plots of mean current depth against event duration, coloured by cluster, and a histogram of event charge deficit.](event-clustering.png "Grouping events by translocation area and depth with k-means clustering.")
