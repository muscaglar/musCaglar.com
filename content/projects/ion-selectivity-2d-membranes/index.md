---
title: "Ion selectivity of two-dimensional membranes"
date: 2020-02-11
summary: "MATLAB analysis for measuring which ions pass through graphene and boron nitride membranes, from current–voltage curves."
kind: research
tags: [MATLAB, Physics, Ion transport]
status: finished
links:
  - name: Thesis
    url: https://doi.org/10.17863/CAM.69569
figure: figure.svg
figure_caption: "A membrane with a single pore between a strong salt solution and a weak one. When positive ions cross more easily than negative ones, a voltage builds up that can be measured."
---

This is the analysis code behind the ion transport part of my PhD. A membrane one atom or a few atoms thick separates two salt solutions of different strength. If the membrane lets one kind of ion through more easily than the other, a voltage appears across it, and the current–voltage curve no longer passes through zero.

The code takes each measured curve, finds the voltage at zero current, and fits that offset against the logarithm of the concentration on one side. The offset can also be given as a fraction of the ideal value from the Nernst equation. Further scripts repeat this for salts with doubly, triply and quadruply charged ions, and against the pH of the solutions. Experiments are looked up in a database.

It is written in MATLAB and builds on an older code base. The work is finished. Most of it was moved to Python at the end, and this is the working record.
