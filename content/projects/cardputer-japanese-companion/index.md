---
title: "A Japanese study companion for the Cardputer"
date: 2026-09-27
summary: "The first slice of a Japanese study companion for the M5Stack Cardputer: a kana round, a hardware check and a romaji to kana converter."
kind: software
tags: [C++, Embedded, Japanese]
status: ongoing
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/japan_cardputer
figure: figure.svg
figure_caption: "The Cardputer in outline, with the a key marked on the keyboard and the hiragana あ on the screen. Romaji goes in at the keys and kana comes out on the screen."
---

This is the start of a Japanese study companion for the M5Stack Cardputer, a pocket computer with a small screen and a keyboard. So far there is a first slice of the app: a home screen, a menu, settings with four looks, and a kana round. It runs in a simulator on a computer.

Beside the app there is a hardware check with four pages. It reports the board, memory, battery and SD card, shows the same Japanese text at four font sizes, turns typed romaji into hiragana or katakana as the keys go down, and records three seconds from the microphone and plays them back. The converter from romaji to kana is plain C++ with no hardware in it, so it has unit tests that run on a computer. Another tool draws the 240 by 135 pixel screen on a computer with the device's own fonts.

It has not yet been run on a device.
