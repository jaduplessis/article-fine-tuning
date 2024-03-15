

base_message_a = """
I am preparing documents to provide to an LLM to fine tune it.  You are a text neutraliser. Your task is to take stylistic or expressive text as input and convert it into a neutral and plain version while preserving the core meaning and factual information.

Your purpose is to create the training data by transforming styled text into neutral text.

Constraint: The neutral text output should be in regular text format, NOT in HTML or markdown. If any code snippets are encountered, leave them exactly as they are.

"""

base_message_b = """

So you have pairs like:
{My text 1} → {Neutral text 1} 
{My text 2} → {Neutral text 2}

My text: ${MyText}

Neutral text:

"""

style_variation = [
  'Style: Vary the original vocabulary, tone and prose. Make it less serious. Convert it to a less coherent draft style.',
  'Style: Vary the original vocabulary, tone and prose. Make it more serious. Convert it to a more serious style.',
  'Style: Vary the original vocabulary, tone and prose. Make it read more like a legal document that drowns in legalese. I want to be asleep by the end of it.',
  'Style: Vary the original vocabulary, tone and prose. Make it more casual. Convert it to a more casual style. Consider using a bullet point format.',
]