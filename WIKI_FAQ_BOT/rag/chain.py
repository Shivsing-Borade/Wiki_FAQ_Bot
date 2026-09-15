def get_response(
    question,
    retriever,
    prompt,
    chat_model,
    history
):

    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    messages = prompt.invoke({
        "context": context,
        "history": history,
        "question": question
    })

    response = chat_model.invoke(messages)

    return response.content