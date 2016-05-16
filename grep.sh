#!/bin/bash

clear

cat text_to_speech/$1|grep -i $2>  grepResult.txt
