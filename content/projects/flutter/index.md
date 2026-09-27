---
title: "Flutter, a slow light to breathe with"
date: 2026-09-23
summary: "An iPhone app whose torch or screen swells and fades like a slow breath, easing from eleven breaths a minute to six."
kind: software
tags: [Swift, SwiftUI, iOS]
status: ongoing
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/flutter_sleep
  - name: Code of the first version on GitHub
    url: https://github.com/muscaglar/snugBug
featured: true
figure: figure.svg
figure_caption: "Brightness against time across one session, drawn with far fewer breaths than a real one. The breaths lengthen from eleven a minute until the pace settles at six, and at the end the peaks sink to dark."
aliases:
  - /posts_snugBug
  - /posts_snugBug.html
---

Flutter is an iPhone app for bedtime. Its light brightens and dims at the pace of a slow breath. The light is the phone's own: the torch on the ceiling when the phone lies face down, or the screen when it lies face up. Flutter is only the app's name; it is written in Swift and has nothing to do with the Flutter framework.

A session starts at eleven breaths a minute and eases to six, then holds that pace. Over the last ninety seconds the top of each breath sinks to dark. A session begins when the phone is laid down and still, and ends when it is picked up. Brightness is worked out from the time elapsed, so a late tick cannot make it drift.

Flutter is the new version of SnugBug, a small app I once wrote over two days. SnugBug drove the torch through two breaths at the press of a button, on curves worked out in advance. Flutter is written afresh. It paces a whole session, uses the screen as well as the torch, and starts and stops by itself.

{{< drawing file="first-version.svg" caption="SnugBug, the first version: the intended brightness of the torch over two breaths. It rises for four seconds and falls for six, slowly at first." >}}

I keep the curve and the session rules as plain logic with their own tests, apart from the hardware code. The release checklist is still open, and several numbers are starting guesses. It has no network code.
