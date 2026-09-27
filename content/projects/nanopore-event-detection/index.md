---
title: "Finding single molecules in a current trace"
date: 2020-01-21
summary: "MATLAB code that finds the brief dips in current made when single molecules pass through a nanopore, and measures each one."
kind: software
tags: [MATLAB, Signal processing, Nanopores]
status: finished
links:
  - name: First version on GitHub
    url: https://github.com/muscaglar/coolwater
  - name: Second version on GitHub
    url: https://github.com/muscaglar/neroli
figure: figure.svg
figure_caption: "A current recording with one event in it. The code finds each dip that crosses the threshold and measures its depth and duration."
---

When a molecule such as DNA passes through a nanopore it blocks part of the ion current for a moment. The recording shows a steady current with short dips, and each dip is one molecule. This code finds the dips.

It reads the amplifier recordings, filters them, and removes sudden shifts in the current level, which cannot be a molecule passing. It then marks every dip that stands out from the baseline by more than a set amount and cuts out a short window around it. For each event the earlier version measures the depth, the duration and the area, which is the charge that did not flow; the later version no longer computes the area. The earlier version showed every candidate on screen and asked for a yes or no.

There are two versions because the second began as a copy of the first. The later one builds on an older code base from the research group, kept in its own folder. Both are MATLAB, tied to the file formats of the instruments I used, and finished.
