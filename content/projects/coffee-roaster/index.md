---
title: "Kahve, a roasting workstation for a small coffee roaster"
date: 2026-09-20
summary: "Local-first software that logs and adjusts a small drum coffee roaster over Bluetooth, with a live browser cockpit and a simulator."
kind: software
tags: [Python, TypeScript, Bluetooth, Coffee roasting]
status: ongoing
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/kahve
featured: true
figure: figure.svg
figure_caption: "Exhaust-air temperature over one roast: a fast climb, the thermostat's saw-tooth around the setpoint, then cooling. The roaster measures the air leaving the drum, not the beans."
---

Kahve is software for a small drum coffee roaster. It talks to the roaster over Bluetooth, records every roast and shows a live view in the browser: exhaust-air temperature, its rate of rise, fan and drum settings, and phase timers. Roasts are stored locally in SQLite and export as plain JSON.

The roaster has one temperature sensor, and it measures the air leaving the drum, not the beans. Kahve labels it that way everywhere. It can also adjust setpoint, time, fan and drum, and step through a profile's schedule. By design, heat only starts with a button press at the machine.

The backend is Python and the cockpit is React. It was built against a simulator first, so the tests never touch hardware. It is at version 0.6.0. It has driven a few real roasts; remote control is still being tested.
