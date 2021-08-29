from re import sub as re_sub
from elmabot import elmabot


@elmabot.handle(outgoing=True, pattern=r'.analyze_words( \d{1,4})?')
async def most_used_words(event):
    """
    `.analyze_words <opt:limit>`: Analyzes messages to find most used words.
    Set the optional <limit> to the number of messages you want to analyze.
    Default is 1000.
    """

    words = dict()
    input_limit = event.pattern_match.group(1) or 1000
    limit = int(input_limit)  # number of messages to analyze
    word_limit = 20

    analyzed = 0
    await event.edit("`processing messages...`")
    async for _message in elmabot.iter_messages(event.chat_id, limit=limit):
        analyzed += 1
        if analyzed % 200 == 0:
            await event.edit("{} messages processed.".format(analyzed))

        if _message.text:
            for word in re_sub(r"[^\w' ]", "", _message.text).split():
                words[word.lower()] = words.get(word.lower(), 0) + 1

    frequency = sorted(words, key=words.get, reverse=True)
    message = (
        "**{analyzed} messages processed in total. The frequency of use of "
        "{word_limit} most used words:**\n\n"
    ).format(analyzed=analyzed, word_limit=word_limit)

    for i in range(word_limit):
        _message = "{}. {} `({} times)` \n"
        message += _message.format(i+1, frequency[i], words[frequency[i]])

    await event.edit(message)
