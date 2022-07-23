
# Owl
An open source Discord - IRC link written in Python. 

## To-do
 - [x] Discord
 - [x] IRC
 - [ ] Slack
 - [ ] Microsoft Teams
 - [ ] Matrix
 - [ ] Mentions
 - [ ] TLS IRC
 - [ ] IRC NickServ authentication
 - [x] Docker support
 - [x] Example Docker compose
 - [x] Publish Docker container on Docker Hub or GitHub 

## Configuration
Set these environment variables: 
 Variable            | Description                      | Values
---------------------|----------------------------------|-----------------------------------------
`IrcEnabled`         | Enable the IRC client            | `True` or `False`
`IrcServer`          | IRC server for connection        | A hostname or IP address
`IrcPort`            | IRC port                         | The port for the IRC server (non-TLS)
`IrcChannel`         | IRC channel to read/send from/to | An IRC channel (Like `#linux`)
`IrcBotnick`         | Nick name for the bot            | A valid IRC nick
`DiscordEnabled`     | Enable the Discord client        | `True` or `False`
`DiscordToken`       | Discord bot token                | A valid token for a Discord bot
`DiscordWebhook`     | Discord webhook URL (used for sending messages to the Discord server) | A URL
`DiscordGuild`       | Discord guild to send/read messages to/from  | A Discord Snowflake
`DiscordChannel`     | Discord channel to send/read message to/from | Also a Discord Snowflake

## Installation
### Using Docker
#### Using Docker Hub
```
docker pull betapictoris/owl
docker run -e [YOUR CONFIG] -d betapictoris/owl
```
Instead of running off the command line it is recommened to use a [compose file](https://github.com/BetaPictoris/owl/tree/dev/docker)

#### Building the container
```bash
git clone git@github.com:BetaPictoris/owl.git   # Clone the repo
cd owl                                          # Change your working directory into the
docker build --tag owl:build                    # Build the Docker image. 
docker run -e [YOUR CONFIG] -d owl:build        # Run the Docker container. 
```  

### Manual
```bash
git clone git@github.com:BetaPictoris/owl.git   # Clone the repo
cd owl/src                                      # Change your working directory into the source directory 
python3 Owl.py                                  # Run the script
```


