---
title: "MoodCal, a mood calendar that fills itself in"
date: 2026-04-14
summary: "An iPhone app that estimates each day's mood from sleep, activity, heart-rate and calendar signals, and shows it on a calendar."
kind: software
tags: [Swift, SwiftUI, iOS]
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/mood-cal
figure: figure.svg
figure_caption: "An invented daily signal over a fourteen-day window, with its mean and today's reading. The app scores the distance from the mean, not the raw value."
---

MoodCal is an iPhone app that keeps a mood calendar without asking for an entry. It runs in the simulator on generated sample data. Each day it reads sleep, steps, heart-rate variability, resting heart rate and exercise minutes from HealthKit, and the hours of calendar events from EventKit. From these it estimates one of five moods, from "rough" to "great", and colours that day on a month grid.

The estimate is relative. Each signal is compared with its own mean over the previous fourteen days, turned into a z-score, clamped and weighted. Sleep counts most and exercise least. A lower resting heart rate counts as better, and a calendar that is unusually full or unusually empty counts against the day. With fewer than three days of history the answer is neutral. Any estimate can be corrected by hand, and the correction survives later refreshes.

It is written in SwiftUI with no third-party dependencies and makes no network requests. Entries are kept in a JSON file on the phone. There are no automated tests yet.
