# About
If you want to enhance protection of your Discord server, you can consider using this OTP bot. It will provide an additional layer of security for your Discord server.

![Sample](data/sample.jpg)

## Setup
Get the bot token from the Discord Developers Console with the necessary permissions, ensure that you include slash command permissions. Afterwards, get the Twilio account SID, auth token and phone number, and add that to your config.py file. Additionally, insert the Verified Role ID for your server into config.py and you're all set.

## Workflow
When a server member uses the "/verify" command, they will be prompted to enter their phone number. The bot will then send a 6-digit OTP to their phone number via SMS. Members can use this OTP to complete the verification process. Once verified, they will be assigned the role specified in the "config.py" file.

No worries, members can only use the "/verify" command once every 5 minutes to prevent misuse of the feature.

## Note
- I assume you have a basic understanding of Python/Discord.py.
- This is a fully open-source project, and you have permission to freely copy, modify, and distribute it.