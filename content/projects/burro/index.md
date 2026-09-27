---
title: "Burro, a way to choose where to live in a city"
date: 2026-09-25
summary: "A tool that ranks a city's neighbourhoods against stated preferences and the places to reach, and shows the sources behind its numbers."
kind: software
tags: [Python, TypeScript, Swift, Open data]
status: ongoing
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/burro
featured: true
figure: figure.svg
figure_caption: "A plan of a made-up city of twenty-four areas, with journeys drawn from two places to reach to one area. The area outlined in red is the one ranked first for that search."
---

Burro helps someone decide where in a city to rent, buy or stay before they start looking at properties. A search states what matters and the places to reach. Burro ranks neighbourhoods on a map and shows how each does on what was asked, with the source and date of the figures.

The ranking is arithmetic over published data, so the same question should give the same answer. Rules, or a language model where one is switched on, turn a sentence into structured preferences. The model is not used to rank places or to describe them from memory. Data sources are registered with their licence before they are fetched, and gaps are left as gaps.

I built it with coding assistants, which wrote most of the code. The engine, data pipeline, API and website are built, and were first deployed on a made-up city of 24 areas. A first build on a real city exists as a preview. Real journey times and checked neighbourhood names are still to do, and the iPhone app has not yet been run.
