#!/bin/bash

echo setting alias...
echo  >> $HOME/.bashrc
echo \#python3 alias >> $HOME/.bashrc
echo alias python=\'python3\' >> $HOME/.bashrc
echo alias pip=\'pip3\' >> $HOME/.bashrc
source $HOME/.bashrc

echo updating and installing applications...
sudo apt update
sudo apt upgrade
sudo apt install vim
sudo apt install python3-opencv

echo installing python packages...
pip insatall pipenv

# echo setting git...
# git config --global user.name "YOUR NAME"
# git config --global user.email "YOUR EMAIL ADDRESS"
# git config --global core.editor vim
