# Development

Bug Bounty Bot is currently a small side project of mine. The long term goal being to track changes to programs and be paired with common offensive tooling leveraged on bounty programs such as Nuclei. Currently the project works off of bash scripts running in the background (e.g., a simple bash script running subdomain enumeration across multiple programs and outputting them to `/home/parzival/bugbounty`. The intention is to not have any secret sauce in terms of the bot. 

The long term goal for this project would be to pair the bot with hunting scripts and have it post output from tooling. For example, the bot would follow the following logic:

1. New subdomain is identified on Linux host.
2. Bot posts newly identified subdomains to a Discord channel.
3. Background scan kicks off for Linux host (think Nuclei). 
4. Juicy findings are output to Discord.
5. Whatever else I think of during development that I'd like to implement.
