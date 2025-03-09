# not essentialy a prompt template
# but rather a template to supply and wrap document retrieved to assistnat

CONTEXT_RETRIEVAL_MAGIC_WORD = "[MAGIC] - CONTEXT RETRIEVAL"

# pylint: disable=unnecessary-lambda-assignment
CONTEXT_DOCUMENT = (
    lambda content: f"""
<Document>
{content}
</Document>
"""
)

CONTEXT_ASSISTANT_CONTENT = (
    lambda documents: f"""
{CONTEXT_RETRIEVAL_MAGIC_WORD}
I've retrieved the following information from the knowledge base that's relevant to your query:

<Documents>
{"\n".join([CONTEXT_DOCUMENT(documents) for documents in documents])}
</Document>

I'll use this information to answer your question.
"""
)
