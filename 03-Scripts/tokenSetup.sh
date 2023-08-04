#!/bin/bash

#Functions declaration
TOKEN_FILE="/etc/DiscordImageGenerationBot/tkn"

source_token() {
    unset DISCORD_TOKEN
    source $TOKEN_FILE
    chmod 155 $TOKEN_FILE
    #echo $HOME
    #echo "source /etc/DiscordImageGenerationBot/tkn" >> $HOME/.bashrc 
    echo -e "\e[32mSuccessfully saved token. To be able to use the bot, please run this command (only once, except if your bashrc file can be reset) \e[0m"
    echo -e "\e[35m        echo \"source /etc/DiscordImageGenerationBot/tkn\" >> ~/.bashrc \e[0m"
    echo -e "\e[32mor add this line to your ~/.bashrc \e[0m"
    echo -e "\e[35m        source /etc/DiscordImageGenerationBot/tkn \e[0m"
    echo -e "\e[32mand source it. \e[0m"
}

create_token_file() {
    file=$TOKEN_FILE
    mkdir -p "${file%/*}"
    touch "$file"
    #touch /etc/DiscordImageGenerationBot/tkn
    echo "export DISCORD_TOKEN=$1" > $file
    chmod 777 $file
    source_token
}



echo -e "\e[33m*********************************\e[0m"
echo -e "\e[33mDiscord Image Generator Bot setup\e[0m"
echo -e "\e[33m*********************************\e[0m"
echo " "
echo -e "\e[1;31mWarning : this script will add your discord token in your bashrc file as an environment variable \e[0m"
echo " "
read -p "Do you want to continue (y|n) ? " warning_user_choice

case $warning_user_choice in
y)
    echo -e "\e[31mPlease provide your token (input is hidden) : \e[0m"
    read -s TOKEN
    create_token_file $TOKEN
    ;;
n)
    echo -e "\e[32mGreat choice.\e[0m"
    ;;
esac
