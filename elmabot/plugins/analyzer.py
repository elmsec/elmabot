from re import sub as re_sub
from elmabot import elmabot


@elmabot.handle(outgoing=True, pattern=r'^.analyze_words( \d{1,4})?')
async def most_used_words(event):
    """
    `.analyze_words <opt:limit>`: Analyzes messages to find most used words.
    Set the optional <limit> to the number of messages you want to analyze.
    Default is 1000.
    """

    STOP_WORDS = {
        # English
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
        "your", "yours", "yourself", "yourselves", "he", "him", "his",
        "himself", "she", "her", "hers", "herself", "it", "its", "itself",
        "they", "them", "their", "theirs", "themselves", "what", "which",
        "who", "whom", "this", "that", "these", "those", "am", "is", "are",
        "was", "were", "be", "been", "being", "have", "has", "had", "having",
        "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",
        "or", "because", "as", "until", "while", "of", "at", "by", "for",
        "with", "about", "against", "between", "into", "through", "during",
        "before", "after", "above", "below", "to", "from", "up", "down", "in",
        "out", "on", "off", "over", "under", "again", "further", "then",
        "once", "here", "there", "when", "where", "why", "how", "all", "any",
        "both", "each", "few", "more", "most", "other", "some", "such", "no",
        "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s",
        "t", "can", "will", "just", "don", "should", "now"

        # Turkish
        "acaba", "ama", "aslında", "az", "bazı", "belki", "biri", "birkaç",
        "birşey", "biz", "bu", "çok", "çünkü", "da", "daha", "de", "defa",
        "diye", "eğer", "en", "gibi", "hem", "hep", "hepsi", "her", "hiç",
        "için", "ile", "ise", "kez", "ki", "kim", "mı", "mu", "mü", "nasıl",
        "ne", "neden", "nerde", "nerede", "nereye", "niçin", "niye", "o",
        "sanki", "şey", "siz", "şu", "tüm", "ve", "veya", "ya", "yani"
    }

    frequency = dict()
    input_limit = event.pattern_match.group(1) or 1000
    limit = int(input_limit)  # number of messages to analyze
    word_limit = 10

    analyzed = 0
    await event.edit("`processing messages...`")
    async for _message in elmabot.iter_messages(event.chat_id, limit=limit):
        analyzed += 1
        if analyzed % 200 == 0:
            await event.edit("{} messages processed.".format(analyzed))

        if not _message.text:
            continue

        for word in re_sub(r"[^\w' ]", "", _message.text).split():
            if word in STOP_WORDS or word.isdigit():
                continue
            frequency[word.lower()] = frequency.get(word.lower(), 0) + 1

    # key=frequency.get sorts it by the item value (word frequency)
    words = sorted(frequency, key=frequency.get, reverse=True)
    message = (
        "**{analyzed} messages processed in total. The frequency of "
        "{word_limit} most used words:**\n\n"
    ).format(analyzed=analyzed, word_limit=word_limit)

    if len(frequency) < word_limit:
        word_limit = len(frequency)

    for i in range(word_limit):
        _message = "{}. {} `({} times)` \n"
        message += _message.format(i+1, words[i], frequency[words[i]])

    await event.edit(message)
