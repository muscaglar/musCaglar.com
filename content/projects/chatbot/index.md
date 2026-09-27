---
title: "Chatbot experiments"
date: 2020-02-03
summary: "Study notes in code: a perceptron and a small neural network in C++, and notebooks on text classification, PyTorch and a chatbot."
kind: tinkering
tags: [C++, Python, Machine learning, NLP]
status: paused
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/chatBot
figure: figure.svg
figure_caption: "The small network from the C++ part: one input, five sigmoid units and one output, trained to follow a sine wave."
aliases:
  - /posts_chatBot
  - /posts_chatBot.html
---

A folder of exercises, made while finding my way round natural language processing and neural networks. Much of it follows published tutorials, with my own notes added along the way.

The C++ part holds two small programs. One is a single-layer perceptron class that learns AND and OR. The other, adapted from a published example, is a network with one input, five sigmoid units and one output, trained by gradient descent on twenty samples of a sine wave.

The Python notebooks cover more ground: tokenising, stemming and tagging text with NLTK, a sentiment classifier in which five models vote, first steps in PyTorch on digits, photographs and news articles, and the data preparation for a sequence-to-sequence chatbot built from pairs of public forum comments and replies. The chatbot stops there. The training files are written but no model is trained in the notebook.
