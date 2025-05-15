# Model Experience
Here, you’ll find some of my experiences with different models.  
**Disclaimer:** Please use this information as a reference only... model performance can vary significantly depending on the specific task.  

## xAI  
- `grok-2-latest`  
    I didn’t find anything particularly special about this model. It sometimes struggles with structured output generation, especially when the output format is complex.  
    The root cause seems to be that the current structured output functionality in [LangChain](https://www.langchain.com/) relies on forcing tool calling. This means the Grok model may be struggling with tool invocation.  
    In some scenarios, I even observed it hallucinating tools that are similar to the ones I provided.
