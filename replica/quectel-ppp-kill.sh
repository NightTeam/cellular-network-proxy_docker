#!/bin/sh

timeout=5
killall -15 pppd
sleep 1
killall -0 pppd
while [ $? -eq 0 ]; do
  timeout=$(expr $timeout - 1)
  if [ $timeout -eq 0 ]; then
    exit 1
  fi
  sleep 1
  killall -0 pppd
done

if [ $? -ne 0 ]; then
  killall -9 pppd
fi
