#!/bin/bash

clear

echo "calling the speech to text translator..."
#file="/home/sugandh/ir16/sound.wav";
python3.4 -c 'import speech_text; speech_text.translate("/home/sugandh/ir16/sound.wav")' > textfile.txt;
echo "writing text to file ..."

cat ~/ir16/textfile.txt|grep KQED > brand1.txt
text=`cat brand1.txt`;
#textfile.txt|grep brand2 > brand2.txt
export text
echo $text
python3.4 main.py $text brand1.txt;

