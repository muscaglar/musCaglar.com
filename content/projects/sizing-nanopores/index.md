---
title: "Sizing a nanopore from its resistance"
date: 2020-01-21
summary: "MATLAB analysis that estimates the diameter of a pore made in a membrane from the resistance measured before and after."
kind: research
tags: [MATLAB, Nanopores, Physics]
status: finished
links:
  - name: Thesis
    url: https://doi.org/10.17863/CAM.69569
figure: figure.svg
figure_caption: "Current against voltage at three stages: the bare capillary, the capillary sealed by a membrane, and the membrane after a pore is made. The change in slope between the last two gives the pore's resistance, and from that its diameter."
---

The size of a pore in a membrane can be estimated from how easily current passes through it. This is the code that does the estimate.

It takes three current–voltage measurements for each sample: the bare capillary, the capillary sealed by a membrane, and the same membrane after a pore has been made in it with a voltage. A straight-line fit to each gives a resistance. The difference between the sealed and the opened membrane is taken as the resistance of the pore, and a formula turns that into a diameter, using the conductivity of the solution and the thickness of the membrane. Other scripts compute the noise spectrum of the current at each of the three stages, and set pore size against ion selectivity.

The code is MATLAB, and finished.
