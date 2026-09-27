---
title: "voice-node, a voice assistant built to be read"
date: 2026-09-23
summary: "A voice assistant that only listens, thinks and talks: everything it can do comes from servers it is pointed at, through one guarded door."
kind: software
tags: [Python, Voice, Model Context Protocol]
status: ongoing
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/voice-node
featured: true
figure: figure.svg
figure_caption: "Hear, think, speak. Whatever the node does beyond talking leaves through one door."
---

voice-node is a voice assistant, written to be read and kept up by people who did not write it. It hears a wake word or a key press, captures what is said, works out an answer and speaks it. That is all it knows how to do by itself.

Everything else comes from connectors: Model Context Protocol servers that it is pointed at, and a few tools of its own, such as timers and volume. Point it at a server that controls a house and it controls a house. Point it at a notes server and it reads notes. Its source names no room, device or brand, and a test keeps it that way. The server it was written to speak to first is [haso-mcp](../haso-mcp/), which decides what may be done to a house.

{{< drawing file="architecture.svg" caption="The path of a turn, from the microphone to the loudspeaker. A sentence the servers know is answered on the fast path, before any model is asked. Every call to a tool, whoever proposes it, leaves through the one door." wide=true >}}

## One spine

Every part reports what happened, as an event. One pure function decides what happens next, and says so as effects. So the same node runs in a test, at a terminal and on a speaker, and a simulator plays a ten-second conversation in milliseconds, the same way twice.

## Safety that does not depend on the model

Every call to a tool passes one choke point. What kind of tool it is (one that reads, one that acts, one that reads what other people wrote) comes from my configuration, never from the server. Once a conversation has read text that other people wrote, it can no longer reach a tool that acts.

## Parts that can be changed

Speech to text, the chat model and text to speech each name their own provider. They mix freely: all three on one machine at home, all three hosted, or some of each.

A turn that went wrong can be marked by saying so. Marked turns become test cases, and can be replayed against another model as dry runs, to see what it would have done.

## Where it stands

An alpha, and mostly unproven. So far it has only been run by hand, with a key held down to talk.
