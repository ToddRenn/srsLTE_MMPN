#!/bin/bash

for file in ./Output_Files/*
do
	python3 reader.py ${file##*/} &
done
