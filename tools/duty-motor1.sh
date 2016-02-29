#!/bin/bash
echo Cambiando motor $1 a $2
echo $2 > /sys/class/pwm/pwm$1/duty_ns
