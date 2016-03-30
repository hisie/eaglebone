#!/bin/bash
export PYTHONPATH=$HOME/Documentos/proyectos/Drone:$HOME/Documentos/proyectos/Drone/drone
python $HOME/Documentos/proyectos/Drone/desktopRemoteControl/control.py "$@"
