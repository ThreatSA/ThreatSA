Intimacy analysis is essentially a mathematical method in which there is only one adjustable parameter, the attenuation factor. Therefore, we have analyzed the effect of attenuation factor on intimacy and the results are as follows:

|  | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 |
|----------|----------|----------|----------|----------|----------|----------|----------|----------|-----------|
| UNSW-NB15    |          |          |          |          |          |          |          |          |           |
| MSCAD    |          |          |          |          |          |          |          |          |           |



From the experimental results, it can be seen that the attenuation factor has less influence on the evaluation results, and the accuracy is higher than 97.5% on the UNSW dataset, and higher than 99% on the MSCAD dataset, both of which achieve optimal results when the attenuation factor is 0.4 or 0.5. 
The attack pattern of UNSW is simpler and most of the edges in the composed malicious traffic graph are directed from the attacker to the victim, i.e., no attenuation is required, so the attenuation factor in the path has less impact on it. MSCAD is a multi-step attack dataset, and the situation value of the second step of the attack is significantly higher than the first step, as shown in Fig. 3(b) in the paper. 
So the change of the situation value in the first stage part has less effect on the Frechen distance of the two lines, so the result is better.
