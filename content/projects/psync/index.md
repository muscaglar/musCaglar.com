---
title: "Psync"
date: 2026-09-23
summary: "An unofficial companion web app, with iOS and Android wrappers, for finding and booking classes at a fitness studio chain."
kind: software
tags: [JavaScript, Progressive web app, iOS, Android]
status: ongoing
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/psycle-booking
figure: figure.svg
figure_caption: "An invented week of classes drawn as a grid, days across and time of day down, with full classes dashed. The red one is the class that is booked."
---

Psync is an independent companion app for members of a chain of fitness studios. It shows one timetable across every studio, filtered in the browser, and lets a member book and cancel classes, pick a seat and manage waitlist places. It is not affiliated with or endorsed by that company.

It is a progressive web app in plain JavaScript, with no framework and no build step, wrapped with Capacitor for iOS and Android. It has no server of its own and keeps its data on the device. Waitlist offers are not claimed automatically, and a booking still queued when the app is next opened asks before it is sent.

The iOS app adds calendar sync, widgets, a Live Activity and reminders. The Android build is compiled in CI and I have not yet tried it on a phone. The tests run against a stubbed API, not the real booking system.
