---
title: "Roughly: meal estimates as a range"
date: 2026-09-23
summary: "A phone app that turns a described or photographed meal into calories, as a low-to-high range rather than one number, plus macros."
kind: software
tags: [Swift, Kotlin, Python, Language models]
status: ongoing
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/roughly
figure: figure.svg
figure_caption: "Three items in a meal, each with its own low-to-high calorie range, add up to the range shown for the meal. The dot is the estimate, and the range reaches further above it than below."
---

Roughly is a food notebook for the phone. A meal is typed, spoken or photographed in ordinary words, and the app answers with calories as a low-to-high range, plus protein, carbohydrate and fat. There are no accounts and no server of mine. On a recent iPhone the estimate can run entirely on the device. Otherwise it goes straight from the phone to a language model, with a key the person supplies.

The estimator is a fixed cascade. A language model splits the description into items and portions. A curated offline food table prices what it can, and the model estimates the rest. Plain code then attaches the calorie range, which widens with uncertainty about the portion and the source. The widths were calibrated against a set of everyday meals.

The logic is written and measured once in Python, then generated or parity-tested into Swift for the iPhone app and Kotlin for an Android port. The Android port has not yet been run on a phone.
