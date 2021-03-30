# Faceit Integration for Streamlabs Chatbot

- [Faceit Integration for Streamlabs Chatbot](#faceit-integration-for-streamlabs-chatbot)
    * [What is this script?](#what-is-this-script)
    * [Getting Started](#getting-started)
        + [Prerequisites](#prerequisites)
        + [Download and Installation](#download-and-installation)
            - [Install this script](#install-this-script)
                * [From Streamlabs Chatbot](#from-streamlabs-chatbot)
                * [Copying Files](#copying-files)
        + [Initial Setup](#initial-setup)
    * [Usage](#usage)
        + [Elo Check Command](#elo-check-command)

## What is this script?

This is a script made to integrate StreamLabs Chatbot with FACEIT's REST API, so it's easier for the streamer to get
information of his account, e.g. His ELO

## Getting Started

Here's a short guide to get you up and running in a quick way.

### Prerequisites

In order to use this script you would need to do some things first. An account
at [FACEIT Developer Portal](https://developers.faceit.com/), there you can create an APP in
the [App Studio](https://developers.faceit.com/apps) and get an API Key for that app.

### Download and Installation

**DISCLAIMER: This section is still under definition as we don't have a publishing pipeline for this nor a the script
has been published on SLCB Discord forum.**

Download the last version of this script either from the [Streamlabs Chatbot Discord](https://discord.gg/xFcsxft)
channel **scripts** or from the [releases](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/releases)
page of [this repo](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration).

#### Install this script

There are two ways you can install this script, in both of them we assume you already configured
the [Scripts Tab](https://streamlabs.com/content-hub/post/chatbot-scripts-desktop).

##### From Streamlabs Chatbot

- Open Streamlabs Chatbot
- Go to Scripts Tab
- Click on the import button
- Select the ZIP file you just downloaded

##### Copying Files

- Open an explorer window
- Navigate to C:/Users/$YOURUSER/AppData/Roaming/Streamlabs/Services/Scripts
- Uncompress the ZIP file you just downloaded into that folder
- In Streamlabs Chatbot's Scripts tab click on "Reload Scripts" button.

### Initial Setup

Now that you have the script installed, in Streamlabs Chatbot's Scripts tab click on "Faceit Integration" and the
settings for this script should display to the right side of your screen.

You'll see there is an empty field asking for your FACEIT API Key. Introduce there the key you got in
the [prerequisites](#prerequisites) step. Note that this API Key is mandatory to fill for the chatbot to communicate
with FACEIT's API

## Usage

Here you will find brief explanation on how to use the features of this script.

### Elo Check Command

For this command to work it is **MANDATORY** to fill the FACEIT user's default nickname. You can fill it on "Elo Check
Command"
tab in this script's settings.

Here's a table with the parameters for this script.

| Label         | Type   | Description                                                                        | Default                                                                       | Mandatory |
| ------------- | ------ | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | --------- |
| Command       | text   | The text that should trigger the Faceit ELO check                                  | !elo                                                                          |           |
| Nickname      | text   | This is the user the command is going to check when no param is included           |                                                                               | YES       |
| Permission    | select | The group of users that can use this command                                       | everyone                                                                      |           |
| Specific User | text   | This field should only be filled when using the user_specific permission           |                                                                               |           |
| Cooldown      | slider | How long the command should go on for.                                             | 30                                                                            |           |
| Message       | text   | The message that will be sent to chat when using the command.                      | $username, the Faceit ELO for $arg1 is $value                                 |           |
| Error Message | text   | The message that will be sent to chat when using the command and there's an error. | $username, nice try, but $arg1's ELO is under a rock, 'cause I can't find it. |           |

You see there are some $args in the default texts, you can use them in your own custom messages they are parsed as
follows.

| Argument      | Description                                                     |
| ------------- | --------------------------------------------------------------- |
| **$username** | The user that called this command                               |
| **$arg1**     | The user whose elo is being checked. By default is **Nickname** |
| **$elo**      | The value for ELO the script has found                          |
| **$level**    | The value for Level the script has found                        |

Let's illustrate them with an example:

When called without arguments.

```
SomeGoatUser: !elo
MyGoatBot: SomeGoatUser, the Faceit ELO for (----- here goes Nickname ----) is 102.
```

When called with argument.

```
SomeGoatUser: !elo AnotherGoatUser
MyGoatBot: SomeGoatUser, the Faceit ELO for AnotherGoatUser is 42.
```

When called with an argument but this argument is a Faceit user that doesn't exist.

```
SomeGoatUser: !elo AnotherGoatUser
MyGoatBot: SomeGoatUser, nice try, but AnotherGoatUser's ELO is under a rock, 'cause I can't find it.
```

### Session Start Command

Here's a table with the parameters for this script.

Label         | Type   | Description                                                                        | Default                                                                       | Mandatory |
| ------------- | ------ | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | --------- |
| Command       | text   | The text that should trigger the Faceit Session Check command                                  | !startsession                                                                         |           |
| Permission    | select | The group of users that can use this command                                       | moderator                                                                      |           |
| Specific User | text   | This field should only be filled when using the user_specific permission           |                                                                               |           |
| Cooldown      | slider | How long the command should go on for.                                             | 72000 (20 hours)                                                                       |           |
| Message       | text   | The message that will be sent to chat when using the command.                      | $username, we've played $total_matches games, won $won_matches, lost $lost_matches and this session elo balance is $elo_balance.                                |           |
| Error Message | text   | The message that will be sent to chat when using the command and there's an error. | Oh, dear, $username, something went wrong trying to get this session's data. Try it again later and if the issue persists contact the streamer.|           |

You see there are some $args in the default texts, you can use them in your own custom messages they are parsed as
follows.

| Argument      | Description                                                     |
| ------------- | --------------------------------------------------------------- |
| **$username** | The user that called this command

### Session Check Command

For this command to work it is **MANDATORY** to fill the FACEIT user's default nickname. You can fill it on "Session
Check Command" tab in this script's settings.

Here's a table with the parameters for this script.

Label         | Type   | Description                                                                        | Default                                                                       | Mandatory |
| ------------- | ------ | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | --------- |
| Command       | text   | The text that should trigger the Faceit Session Check command                                  | !session                                                                         |           |
| Nickname      | text   | This is the user the command is going to check           |                                                                               | YES       |
| Permission    | select | The group of users that can use this command                                       | everyone                                                                      |           |
| Specific User | text   | This field should only be filled when using the user_specific permission           |                                                                               |           |
| Cooldown      | slider | How long the command should go on for.                                             | 30                                                                            |           |
| Message       | text   | The message that will be sent to chat when using the command.                      | $username, we've played $total_matches games, won $won_matches, lost $lost_matches and this session elo balance is $elo_balance.                                |           |
| Error Message | text   | The message that will be sent to chat when using the command and there's an error. | Oh, dear, $username, something went wrong trying to get this session's data. Try it again later and if the issue persists contact the streamer.|           |

You see there are some $args in the default texts, you can use them in your own custom messages they are parsed as
follows.

| Argument      | Description                                                     |
| ------------- | --------------------------------------------------------------- |
| **$username** | The user that called this command                               |
| **$total_matches**     | The total number of matches played on the current session |
| **$won_matches**      | The number of matches won on the current session                       |
| **$lost_matches**    | The number of matches lost on the current session                        |