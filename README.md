### ThreatSA

We propose ThreatSA, a system for network security situation assessment.
We evaluate the method on two network attack datasets: UNSW-NB15 and MSCAD.
There are four main phases in ThreatSA:
## Malicious Traffic Graph generation: 
The purpose is to transform the malicious traffic data in the sampling period into a malicious traffic graph. The nodes in thegraph are addresses, and the edges are malicious traffic between hosts. The input of this part is the labeled traffic dataset, and the output is the malicious traffic graph ofthe target network.

## Centrality Analysis
In this phase, after getting the malicious traffic graph, we calculate the centrality of each node in the graph. The nodes with the top n\% centrality will be selected as the central nodes. The input is the malicious traffic graph, and the outputs are central nodes and normal nodes.

## Intimacy Calculation
This phase needs to calculate the intimacy between the normal node and the central node as the security situation of each node in the sampling period. The inputs are the central nodes and normal nodes. The output is the intimacy result for each node.

## Situation Analysis
This phase draws the situation broken lines of each host to facilitate the analysis of the network situation. The input of this phase is the intimacy value of each node, and the output is the situation broken line.
<!--
**ThreatSA/ThreatSA** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->
