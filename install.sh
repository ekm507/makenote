#!/bin/bash

function msg() {
 local text="$1"
 local div_width="80"
 printf "%${div_width}s\n" ' ' | tr ' ' -
 printf "%s\n" "$text"
}

function main(){
  msg "install makenote for all users? (Y for all users, N for only you, type anything else to cancel) (y/n)"
  read -r answer
  case $answer in
        [Yy] ) install_path="/usr/share/makenote"
          install_user="root"
          exec_path="/usr/bin";;
        [Nn] ) install_path=$HOME"/.local/share/makenote"
          install_user="user"
          exec_path=$HOME"/.local/bin" ;;
        * ) echo "you cancelled installation.";
        exit;;
  esac


# check if directory makenote exists
 if [ -d $install_path ];then

   msg "directory makenote already exists. pulling new version"

   cd $install_path

   if [[ $install_user == "root" ]];then
     sudo git pull
   else
     git pull
   fi

   msg "makenote is updated!"

 else

    msg "cloning repo"

    if [[ $install_user == "root" ]];then

      sudo git clone https://github.com/ekm507/makenote.git $install_path
      msg "installing executable file"
      sudo cp $install_path/makenote.py $exec_path/makenote
      sudo chmod +x $exec_path/makenote
      msg "makenote is installed!"
    else
      git clone https://github.com/ekm507/makenote.git $install_path
      cp $install_path/makenote.py $exec_path/makenote
      chmod +x $exec_path/makenote
      msg "makenote is installed!"
    fi

 fi
}

main
