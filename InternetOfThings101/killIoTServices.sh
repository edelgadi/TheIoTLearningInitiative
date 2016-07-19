#!/bin/bash

for a in $(pidof python);
do
	kill -9 $a
done
for b in $(pidof mosquitto);
do
	kill -9 $b
done
