#!/bin/bash

NUMBTIMES=100
RUNVAR=0
while [[ $RUNVAR -lt $NUMBTIMES ]]
do
	python cmd.py
	RUNVAR=$RUNVAR-1
	echo titties
done
