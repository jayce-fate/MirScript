#!/bin/bash

Cur_Dir=$(cd "$(dirname "$0")";pwd)
cd $Cur_Dir

python3 exp_controller.py