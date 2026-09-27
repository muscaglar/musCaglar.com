---
title: "A transistor made from a membrane"
date: 2018-02-06
summary: "MATLAB analysis of how a gate voltage changes ion flow through a membrane, and separate LabVIEW and C++ code that drives an amplifier."
kind: research
tags: [MATLAB, LabVIEW, Ion transport]
status: finished
links:
  - name: Analysis code on GitHub
    url: https://github.com/muscaglar/bluejeans
figure: figure.svg
figure_caption: "A schematic: source and drain either side of a membrane, and a gate as the third terminal. What is measured is how the ion current responds to the gate voltage."
---

A field-effect transistor controls a current with a voltage on a third terminal, the gate. Here the current is carried by ions in salt water passing through a membrane, and the measurement is how a gate voltage changes that flow.

Each recording holds four things: the current and voltage between source and drain, and the current and voltage at the gate. The MATLAB code splits a recording by gate voltage, fits a line to each current–voltage curve, and reports the resistance and the offsets from zero at each gate setting. It then works out how selective the membrane is for one kind of ion as the gate voltage changes.

A second repository holds LabVIEW classes that drive a multi-channel amplifier through a small C++ server, setting voltages and reading currents channel by channel. Both are finished and were uploaded as they stood.
