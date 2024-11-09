prompt_template = """
    Generate a professional email response to a customer inquiry about [summarize customer's question here] based only on the provided context. If the question aligns with the context, answer using details relevant to ABC Company’s offerings, policies, or values found in the context.

    If the question does not align with the context, provide a generic response thanking the customer and encouraging them to reach out for more information, without using any information or assumptions beyond what is provided in the context.
    
    The response should include:
    A subject line that reflects the topic of the customer’s inquiry.
    A greeting to the customer with 
    If the question aligns with the context, start by thanking the customer for their inquiry. Provide a clear, informative response based only on the context, highlighting relevant aspects of ABC Company’s policies or offerings.
    If the question does not align with the context, reply with a generic message, such as: ‘Thank you for your inquiry. For more information about our services, please contact our customer support team.
    Keep the tone professional, friendly, and helpful.
    A closing e.g. "Best regards", "Thank you"
    Add signature at the end
    
    The response should not include:
    No mention about the context
    Any note about the question.
    No mention if the question is not aligned with the context.
    Response should not contain any other information that what is listed in the should include in response part
    
    Context:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}
    Question: {{question}}
    Answer:
    """

test_prompt = """
    Given the context information and not prior knowledge, answer the Question as a customer support and format the answer as a email reply.
    
    Context:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}
    
    Question: {{question}}
    Answer:
    """
