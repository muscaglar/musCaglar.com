---
title: "haso-mcp, a policy server in front of Home Assistant"
date: 2026-09-23
summary: "A server that stands between voice assistants and a house: each client gets its own key, and the server decides what that key may do."
kind: software
tags: [Python, Model Context Protocol, Home Assistant, Security]
status: ongoing
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/haso-mcp
featured: true
figure: figure.svg
figure_caption: "The three tiers. What is small and easy to undo needs the key alone, what is wider needs a witness at a button, and what lies outside the wall is never done."
---

haso-mcp is a Model Context Protocol server that stands in front of Home Assistant. A voice assistant in a room, or a diagnostic tool on a laptop, never talks to the house itself. It talks to this server, with a key of its own that can be taken away, and the server alone holds the credential of the house. The voice assistant that was written to speak to it is [voice-node](../voice-node/).

It assumes that a client can be wrong or hostile: a language model that has read a poisoned web page, or a node that was stolen. So nothing a client says about itself counts. The server works out which things a request would touch, and decides on those.

{{< drawing file="architecture.svg" caption="The path of a request. It passes a gate, is resolved to the things it would touch, and is put to the policy. The decision is written down first. Only then does anything run, and only a fixed list of services can." wide=true >}}

## Three tiers

What is near, small and easy to undo needs the key alone: the lights of the client's own room, the volume, a set-point inside limits I chose. Anything wider needs a witness: a press of a button that the server sees for itself, through Home Assistant. Nothing a client sends can stand in for it. And some things are never done, for anyone: locks, alarms, doors, cameras.

## Easy to live with

A dry run decides a request in full and then stops. Yesterday's conversations can so be replayed against a new model, and compared by what each would have done, with nothing moved. "No, undo that" puts back what the last action changed, within five minutes.

Every decision is written to an audit log before anything runs. If the log cannot be written, nothing runs.

## Local, by design

The server listens on the machine it runs on and nowhere else. There is no remote access, no cloud relay and no companion app, and none is planned: to control a house through it you have to be in the room.

## Where it stands

An alpha. Its tests run the whole server in memory against a made-up house. Against a real one it has switched a light on and off, and answered a sentence about another room with silence. The rest is still to be proven.
