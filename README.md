# Tumblr Tagging Semantic Relatedness
## About
This project contains files exploring a co-occurrence frequency analysis of Tumblr tags as an investigation of the ways that community drives language usage by using co-occurence as my metric of relatedness to prevent introducing researcher bias through the application of a hypothetical 'golden standard' of relatedness.

In plain English, what that means is that I'll be looking into the ways in which users of Tumblr use tags together as a way of understanding those words relatedness. By looking at the ways users themselves define and use words together I hope to avoid forcing language usage into my own understanding and to allow multiple forms of 'correct' word usage to exist simultaneously in the same system.

## Languages
This project has been built using Java, Javascript, Python2.7, and a tiny bit of C

You can expect to see a heavy usage of the SciKitLearn, PyTumblr, and D3.js libraries

SciKitLearn and PyTumblr can both be pip installed

## Premise
Basically I wanted to see if I could do unsupervised machine learning feature extraction by deconstructing and reimagining the way that K-Means works as a way to asymptotically approach a specific subset of tags that all shared similar meanings

Since language is so community driven in the TumblrVerse I was hoping that these breaks would fall along community lines and that further visualizations would visualize the ways in which communities interact.

##TODO:
* **Push up Java files so it will run again**
* Look into python foreign language injection and using pthreads in C to speed everything up
* Figure out how to separate overlapping tags in javascript for greater legibility in the visualizer
* Keep track of which users a tag belongs to as a way to further visualize clustering success
* Color code tag tesselations based on which user said that tag most
* Interface with Tumblr API to generate a map for a single user to show how they enteract with the network

