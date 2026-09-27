---
title: "Reading a voltage from the light of quantum dots"
date: 2020-01-21
summary: "MATLAB code that lines up the light emitted by quantum dots with the voltage applied to them and measures how the light responds."
kind: research
tags: [MATLAB, Quantum dots, Signal processing]
status: finished
links:
  - name: Thesis
    url: https://doi.org/10.17863/CAM.69569
figure: figure.svg
figure_caption: "The applied voltage, above, and the light from the dots, below, on a shared time axis. The light changes each time the voltage is switched; the size and speed of that change are what the code measures."
---

Quantum dots are small crystals that glow when lit by a laser. How brightly they glow depends on the electric field around them, so they can be used to read a voltage optically. Part of my PhD built a test platform to calibrate that response.

The code here processes and analyses gating experiments. Spectra are recorded frame by frame while a potentiostat steps or cycles the voltage across the sample. The code reads both sets of files, takes the peak height and peak wavelength from every spectrum, and lines the result up in time with the applied voltage. From that it works out the percentage change in light at each voltage step and, using a Fourier transform, how the light follows a voltage that is switched at different rates. The same routines were run on a dye as well as on the dots.

It is MATLAB, written for one set-up, and finished.
