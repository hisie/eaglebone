#!/bin/bash

echo Cambiando a $1

echo $1 > /sys/class/pwm/pwm3/duty_ns
echo $1 > /sys/class/pwm/pwm4/duty_ns
echo $1 > /sys/class/pwm/pwm5/duty_ns
echo $1 > /sys/class/pwm/pwm6/duty_ns
