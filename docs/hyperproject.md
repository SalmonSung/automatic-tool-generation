# Why I Started **Create Data Scientist Agent**

The official reason? I believe data scientists should spend more time collecting meaningful data and connecting insights to the real world. When it comes to analysis, most people use similar approaches — either visualizing the data or feeding it into another machine learning model. These repetitive steps should be automised.

Given how powerful LLMs have become, it's clear that they can perform these routine tasks as well... and most of the time better than I can. So why not let them?

The personal reason? To be honest, I'm just tired of memorizing all the syntax for things like matplotlib or seaborn. If I build a tool, slap "AI" in the name, and make it do the boring parts for me, I can use it both at school and at work. And let’s face it... everyone loves something labeled "AI" these days, even if it's just another ChatGPT wrapper or a distilled version of a commercial LLM :P

## More Explanation

You might notice that this project currently only supports analyzing CSV files. If you’re familiar with machine learning, you might ask:  
**"Why not just train a model?"** — especially when there are so many great libraries optimized for tabular data.

Here’s the thing:

1. **Workplace constraints** — At my workplace, we have access to the data, but we’re not allowed to train or deploy models on it. That makes traditional machine learning approaches impractical.

2. **Limited validation data** — Sometimes, you simply don’t have a proper validation set. Without it, training a model can lead to misleading conclusions.

3. **Exploratory use cases** — There are many cases where you're not trying to build a predictive model at all. Maybe you're just looking for interesting correlations, anomalies, or patterns that might help another team or guide further investigation.

In these situations, a flexible LLM agent that can generate tailored analysis tools becomes incredibly useful — especially when it's fast, interactive, and doesn't require a full ML pipeline setup.
