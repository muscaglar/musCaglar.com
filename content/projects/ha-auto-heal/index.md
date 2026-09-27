---
title: "Auto-Heal: reloading Home Assistant integrations that have gone dead"
date: 2026-07-14
summary: "A Home Assistant integration that reloads integrations whose entities have all gone unavailable, and says so when a reload cannot fix them."
kind: software
tags: [Python, Home Assistant]
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/ha-auto-heal
figure: figure.svg
figure_caption: "One integration over time: it goes unavailable, is reloaded after ten minutes and again an hour later, then handed to a person. The dashed line is what happens when a reload works."
---

Auto-Heal watches every integration in a Home Assistant installation. When everything an integration knows about has gone unavailable, it reloads that integration. When reloading does not help, it raises a repair notice, and a notification if one is set up, naming the device that needs its power switched off and on.

An integration is judged only on entities that were available in the last 24 hours, so a long-dead device can neither hide an outage nor raise a false alarm. By default it waits ten minutes, reloads, waits an hour, reloads once more, and then gives up and asks for help. Reloads are limited to one a minute overall, and an optional gate pauses healing while the whole network is down. It has had two releases.
