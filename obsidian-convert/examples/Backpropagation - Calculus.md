---
subject: ML
tags:
- math/calculus
- ML/implementation/backpropogation
- summary
- 3b1b
- karpathy
---
# Single-dimensional example
The notation here is a little complicated and messy, so I'm not going to repeat it all. It's easiest to review in [the 3b1b video](https://youtu.be/tIeHLnjs5U8?t=90):
- [Timestamp for main overview](https://youtu.be/tIeHLnjs5U8?t=225)

In short, this is the overall calculation - 
$$\Delta C = \frac{\delta C} {\delta w^{(1)}} + \frac{\delta C} {\delta b^{(1)}} + \; ... + \frac{\delta C} {\delta w^{(L)}} + \frac{\delta C} {\delta w^{(L)}}$$ 
ie. the change in C is the change in C relative to each weight and bias. We're interested in the rate of change - the derivative - so we're calculating the derivative of the right side of that function.

We care about the change in the output $\delta C_0$ relative to the change in the given weight $\delta w^{(L)}$ ie. $\frac{ \delta C_0} {\delta w^{(L)}}$

Calculating this involves looking at three related ratios:
1) change in inputs to the previous node $\delta z^{(L)}$ relative to the change in weight for that node $\delta w^{(L)}$
2) change in the previous node $\delta a^{(L)}$ relative to the change in its inputs
3) change in the cost function $\delta C_0$ relative to the previous node

We take the derivative of these three components via the chain rule to get the derivative of our example $\frac{ \delta C_0} {\delta w^{(L)}}$

We then repeat this process, summing and averaging across all inputs
$$\frac {\delta C} {\delta w^{(L)}} = \frac 1 n \sum^{n-1}_{k=0} \frac{ \delta C_k} {\delta w^{(L)}}$$

Then, to calculate the bias, we repeat an almost identical process - exchanging $\frac {\delta z^{(L)}} {\delta w^{(L)}}$ for $\frac {\delta z^{(L)}} {\delta b^{(L)}}$ 

The derivative of $\frac {\delta z^{(L)}} {\delta b^{(L)}}$ is just 1, making this step trivial.

Finally, we have to check previous nodes. This is  effectively repeating steps 1 and 2. To understand this, remember what $z^{(L)}$ is.

$z^{(L)}$ has three components - the current weight $w^{(L)}$, the current bias $b^{(L)}$, and the previous node state $z^{(L-1)}$. 

So to calculate the sensitivity to change in that previous node $z^{(L-1)}$, you're looking at the previous weight $w^{(L-1)}$, the previous bias $b^{(L-1)}$, and the previous previous node state $z^{(L-2)}$. And so on - it's a recursive definition.

You repeat that loop all the way up the tree, finding each derivative and how much it contributes to the whole - that's backpropogation.

# Multi-dimensional changes
There's one significant change once you go beyond a linear network - previous nodes affect more than one node in the current (later) layer.

The fix? Sum the impacts of the previous layer across the current layer. Simple, intuitive, nice. [See summary here](https://youtu.be/tIeHLnjs5U8?t=540)

# More info
This is a nice quick summary for intuitive understanding, but it's a little mathy and abstract for implementation.

For a more practical resource, [Andrej Karpathy goes through implementing backprop in detail here,](https://www.youtube.com/watch?v=VMj-3S1tku0) while explaining basics like the chain rule.
