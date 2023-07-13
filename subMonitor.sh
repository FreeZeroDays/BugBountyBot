#!/bin/bash
## prereq - have Chaos' Client from Project Discovery installed.
### go install -v github.com/projectdiscovery/chaos-client/cmd/chaos@latest

# hardcode your api key because what's the worst that could happen
export CHAOS_KEY="CHAOS_KEY"
file="$1"

while getopts ":h" option; do
   case $option in
      h) # display Help
         echo "./domainhunt.sh /path/to/domains"
         exit;;
   esac
done

while IFS= read -r line; do
    ~/go/bin/./chaos -d $line -o $line-subdomains
done < $file
