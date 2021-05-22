#!/bin/bash

sudo docker build -t plane-seat-website:latest ./plane-seat-booking-website/

sudo docker run --name website -d -p 80:80 plane-seat-website
