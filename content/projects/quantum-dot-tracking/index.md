---
title: "Tracking quantum dots in neurons"
date: 2020-01-22
summary: "Notebooks that find quantum dots in microscope image sequences of neuronal cells and follow each dot's brightness from frame to frame."
kind: software
tags: [Python, Image analysis, Quantum dots]
status: finished
figure: figure.svg
figure_caption: "A stack of frames with a region drawn round each dot, and the brightness inside one region plotted frame by frame. The peaks in that trace are what the analysis looks for."
---

A set of Jupyter notebooks for getting a signal out of microscope image sequences of neuronal cells that contain quantum dots.

The first notebook uses trackpy to locate bright spots in every frame and link them into tracks. The later ones take a simpler route. The frames are combined into one image, which is thresholded, and a distance transform with a search for local maxima marks each dot. A circular region is placed round every dot and the pixel values inside it are summed frame by frame, which gives one brightness trace per dot. Peaks are then picked out of the traces above a fitted baseline. Side notebooks try blob detection and watershed segmentation for the same job.

It is research code: notebooks with fixed paths. The images are not in the repository.
