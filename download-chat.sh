#!/bin/bash

OUTDIR=chat

mkdir -p $OUTDIR

for i in 2335437810 2336692453 2338258978 2339376213; do
    json=$OUTDIR/${i}.json
    if [ ! -f "$json.gz" ]; then
        chat_downloader -o $json https://www.twitch.tv/videos/${i} > /dev/null &
    fi
done
wait
pigz -p 4 $OUTDIR/*.json
