#!/bin/bash

# Create the directory if it doesn't exist
mkdir -p ../../../data

# Run the wget commands

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=14QJsRopyPpezAjRZ7x57mwQoeBOetNhp' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=14QJsRopyPpezAjRZ7x57mwQoeBOetNhp" -O ../../../data/ZW3.msw_image.fits && rm -rf /tmp/cookies.txt

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1sbOq51-yFzljJbIas_d_YTpBgvLdxW__' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1sbOq51-yFzljJbIas_d_YTpBgvLdxW__" -O ../../../data/ZW3.msw_psf.fits && rm -rf /tmp/cookies.txt
