---
title: "Text to STL with a small language model"
date: 2025-06-10
summary: "An experiment in turning a short text description into a 3D mesh, using a small language model that writes constructive solid geometry."
kind: tinkering
tags: [Python, Language models, 3D geometry]
status: paused
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/txt2stl
figure: figure.svg
figure_caption: "Text goes to a language model, which writes a list of solid primitives and operations that becomes a mesh. The mesh is then compared with the real model it was meant to describe."
---

This was a short experiment: give a small language model a one-line description of an object and get a 3D mesh back. The model runs quantised on the CPU and is asked to answer in JSON as constructive solid geometry, a list of primitives such as cubes, spheres and cylinders and the operations that combine them. A converter builds the mesh with Open3D and writes an STL file.

To measure it I took models from the Thingi10K dataset, generated rough descriptions from their bounding boxes, and compared each generated mesh with the original by Chamfer distance and volume. The baseline run covered ten models. One gave no usable JSON. Of the other nine, seven scored below 0.002, one scored 0.006, and the best reached 0.17, where 1 is a perfect match. That is a poor result. Two things in the set-up work against it: the descriptions are vague, and the converter builds only the first primitive and ignores the operations.

There is a LoRA fine-tuning script too, but no result for a fine-tuned model. The work stops there.
