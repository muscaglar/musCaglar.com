---
title: "Displacing carbon atoms using LabVIEW"
date: 2018-12-01
summary: "A LabVIEW program that makes nanopores in graphene by electroporation, large enough for DNA to pass through."
kind: research
tags: [LabVIEW, Nanopores, Instrumentation]
figure: figure.svg
figure_caption: "One of the two electrodes, above a sheet of graphene, with one carbon atom leaving the lattice. Enough atoms displaced in one place make a pore."
cover: labview.png
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/LV_amoureux
aliases:
  - /posts_LV_Breakdown
  - /posts_LV_Breakdown.html
---

Perforating graphene has many applications, ranging from ionic transport to single-molecule sensing. In particular, we are interested in displacing a sufficient number of carbon atoms from graphene to create pores of 5 nm and above, allowing the passage of DNA through such pores to be sensed.

![Animation of a graphene membrane stretched across the tip of a capillary while a voltage is applied.](electroporation.gif "A voltage applied across the membrane displaces carbon atoms and opens a pore.")

![The front panel of the LabVIEW program, with signal generation, device settings, nanopore creation settings and live voltage and current traces.](labview.png "The front panel of the program.")
