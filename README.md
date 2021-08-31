<p align="center">
  <img width="100" height="100" src="https://github.com/elmsec/elmabot/raw/main/logo.png">
</p>

<h1 align="center">ElmaBot</h1>
<p align="center">
  ElmaBot is an open-source user bot for the Telegram messaging service.
</p>

## 🎁 FEATURES

- 🔌 Dynamic plugin system and built-in plugins
- 🧩 Module system and built-in modules
- 🆘 Generating help documents from Docstrings
- 👋 Built-in, multilingual, smart automatic replies on your behalf
- 🧑‍🏭 Jobs system: Automatic actions / cron jobs with custom parsers (being rewritten, stay tuned)

These are just features that are unique. It has more ;)

## Disclaimer

```python
import disclaimer

# Please note that this project is not yet production-ready and is under heavy development. It still works well but be careful. It's your responsibility to use this software.

# Telegram may restrict or ban your account for misuse of their APIs with this software. I'm not responsible for any damage this software may cause. It's your responsibility. Avoid excessive use. Never come here to say "Telegram banned my account!". Don't use this software for spam purposes, otherwise your Telegram account will most likely be banned.
```

## 🗳 Installation

### Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/elmsec/elmabot)

### Manual

1. Clone the repo:

```
git clone https://github.com/elmsec/elmabot.git
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create an .env file and update its variables:

```
cp .env.example .env
vim .env
```

4. Start the bot:

```
python -m elmabot
```

## Built-in plugins

```
- analyzer
  - analyze_words <opt:limit>: Analyzes messages to find most used words. Set the optional <limit> to the number of messages you want to analyze. Default is 1000.

- chat
  - join_own_left_channel <channel_id>: Join to the channel specified with the <channel_id>. You can obtain this ID with the .own_left_channels command from the info module. See .help info.
  - quit: Leaves the current chat.

- eraser
  - del <opt:self>: Delete all the messages by starting from the reply. If the argument <self> is given, only deletes the messages sent by you.
  - << history_eraser >> This handler runs automatically on every outgoing message to keep the chat clean. For bot sides, it deletes all messages except the last n message. 'n' is an integer defined by you, see history_limit below.

- exclamations
  - << !commands >> For commands starting with !, this returns a corresponding answer defined in the strings.yaml[commands]

- fun
  - yell <text> <opt:interval>: Send the given text as T E X T with a typewriter effect. The interval is set to 0.3 by default.
  - asciiphoto: Converts the photo of the replied message to an ascii-style photo.
  - haha<ha\*>: Send random set of characters as much as occurrences of the 'ha' values in the given string. If the message is a reply, then the first one will be sent as a reply to that message.

- help
  - help <opt:plugin_name>: Sends the documentation of the given plugin name, otherwise shows a list of the plugins.

- info
  - chatid: Returns the ID of the current chat.
  - messageid: Returns the ID of the replied message.
  - userid: Returns the ID of the user who sent the specified message.
  - usernames OR .usernames+: Returns the list of your reserved usernames.
  - own_left_channels: Shows a list of your own channels you've left. In order to join one of these channels, use .join_own_left_channel <ID> from the chat module.

- jobs
  - job daemon (start|stop|toggle): Start/stop the job daemon
  - job list: Show a list of jobs you created
  - job (start|stop) <job name>: Start/stop a particular job
  - job delete <job name>: Delete a particular job
  - job add <fields in YAML format>: Add a new job

- promessage
  - edit <text>: Edits your message you've replied to with the given text.
  - fw <opt:limit>: Forwards messages by starting from the message you've replied to. <limit> is the number of messages that will be forwarded.
  - sd <seconds> <text>: Sends a self-destructing message.

- welcomer
  - << first_message >>: If the incoming message is the first message of a chat, this handler will send a message chosen randomly from the strings.yaml[dialogs][greetings][greetings_answers] to that chat.
  - << greeting >>: It does almost the same what << first_message>> does, with one exception. It's triggered when a new message containing a word from strings.yaml[dialogs][greetings] arrives.
```

## Roadmap

- [x] Support Heroku
- [ ] Tests (almost done)
- [ ] New Job parsers: PDFs, polls, SQLite DBs (almost done)
- [ ] Support DO Apps (in progress)
- [ ] Add plugin based configuration manager for local settings
