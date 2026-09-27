---
title: "Home Assistant integration for a cloud-only air conditioner"
date: 2026-09-21
summary: "A Home Assistant integration for an air conditioner that can only be reached through the cloud service behind its maker's app."
kind: software
tags: [Python, Home Assistant]
status: ongoing
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/ha-aquarea-home
figure: figure.svg
figure_caption: "The path of one command from Home Assistant to the air conditioner. There is no local interface, so everything goes by way of the cloud service."
---

This is a custom integration that lets Home Assistant control an air conditioner. The air conditioner has no local interface, so every reading and every command goes through the cloud service behind the maker's app.

It provides a climate entity with power, mode, fan speed, swing and target temperature, and sensors for room temperature and Wi-Fi signal. The state is polled every 30 seconds, and again about two seconds after a command. The interval is fixed on purpose, to keep the load on somebody else's service small.

There is a test suite that runs without Home Assistant installed. The integration is unofficial, and it may break without notice if the service changes.
