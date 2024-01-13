#! /bin/bash

source src/utilities.sh

main()
{
    install_posix_cac
}

install_posix_cac()
{
    option=''

    print_style "\n[POSIX CAC]-----------------------------------\n" "header"

    while [ "$option" != "y" ] && [ "$option" != "n" ]
    do
        print_style "Do you want to install CAC credentials? [y/n]\n" "info"
        read -r option
    done
    
    if [ "$option" = "y" ]; then
        get_posix_cac
    fi
}

get_posix_cac()
{
    # Download the GitHub repository
    git clone https://github.com/jacobfinton/posix_cac.git

    # Make the 'smartcard.sh' script executable
    chmod +x posix_cac/smartcard.sh

    # Run the 'smartcard.sh' script
    sudo ./posix_cac/smartcard.sh

    rm -rf posix_cac
}

main
