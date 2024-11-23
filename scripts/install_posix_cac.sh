#! /bin/bash

source src/utilities.sh

main()
{
    EXIT_SUCCESS=0
    EXIT_FAILURE=1
    TEMP_DIR="/tmp"

    root_check
    process_check
    install_middleware
    opensc_install
    certificate_install

    print_style "\n***Complete***\n" "success"
    exit "$EXIT_SUCCESS"
}

# Check to ensure the script is executed as root
root_check ()
{
    if [ "$(id -u)" -ne 0 ] ;then
        print_style "\n***Must be run as root***\n" "danger"
        exit "$EXIT_FAILURE"
    fi
}

# Double checks that Google Chrome is closed before running anything else
process_check ()
{
    # shellcheck disable=SC2009
    if ps -A | grep -E "\<chrome\>"; then
        print_style "\n***Google Chrome must be closed to run***\n" "danger"
        exit "$EXIT_FAILURE"
    fi
}

# Install required pcsc middleware and remembers package manager.
install_middleware ()
{
    if type apt > /dev/null 2>&1; then # Debian
        PACKAGE_MANAGER="apt install"
        $PACKAGE_MANAGER pcscd pcsc-tools libccid libpcsclite1
    elif type pacman > /dev/null 2>&1; then # Arch
        PACKAGE_MANAGER="pacman -S"
        $PACKAGE_MANAGER pcsclite pcsc-tools ccid
    elif type yum > /dev/null 2>&1; then # Red-Hat legacy
        PACKAGE_MANAGER="yum install"
        $PACKAGE_MANAGER pcsc-lite pcsc-tools
    elif type dnf > /dev/null 2>&1; then # Red-Hat Future
        PACKAGE_MANAGER="dnf install"
        $PACKAGE_MANAGER pcsc-lite pcsc-tools
    elif type zypper > /dev/null 2>&1; then # OpenSUSE
        PACKAGE_MANAGER="zypper install"
        $PACKAGE_MANAGER pcsc-lite pcsc-ccid perl-pcsc pcsc-tools
    else
        print_style "***\nNo currently supported package manager available***" "danger"
        exit "$EXIT_FAILURE"
    fi
    # Ensures middleware is running
    systemctl enable pcscd
    systemctl restart pcscd

    print_style "\n***Middleware installed successfully***\n" "success"
}

opensc_install ()
{
    if $PACKAGE_MANAGER opensc; then
        print_style "\n***opensc installed successfully***\n" "success"
    else
        print_style "\n***Install did not to work***\n" "danger"
        exit $EXIT_FAILURE
    fi
}

# Installs DOD certificates
certificate_install ()
{
    VERSION_FILE="DoD_Approved_External_PKIs_Trust_Chains_v"
    # shellcheck disable=SC2125
    CERT_FILE="$VERSION_FILE"*"/_DoD/Intermediate_and_Issuing_CA_Certs"
    ZIP_FILE="unclass-dod_approved_external_pkis_trust_chains.zip"
    PKI_URL="https://dl.dod.cyber.mil/wp-content/uploads/pki-pke/zip/$ZIP_FILE"

    download_check
    browser_check

    print_style "\n***Broswer certificates installed***\n" "success"
}

# Determines programs on host and downloads/extracts certificates
download_check ()
{
    nettool_check

    unzip_check

    certutil_check
}

nettool_check ()
{
    if type wget > /dev/null; then
        print_style "\nwget is installed and will be used\n" "info"
        wget -qP "$TEMP_DIR" "$PKI_URL"
    elif type curl > /dev/null; then 
        print_style "\ncurl is installed and will be used\n" "info"
        curl -s "$PKI_URL" --output "$TEMP_DIR/$ZIP_FILE"
    else
        $PACKAGE_MANAGER wget
        print_style "\nwget has been installed\n" "info"
    fi
}

unzip_check ()
{
    # unzip check
    if type unzip > /dev/null; then
        print_style "\nunzip is installed and will be used\n" "info"
    else
        $PACKAGE_MANAGER unzip
        print_style "\nunzip has been installed\n" "info"
    fi

    # Extracts certs
    unzip "$TEMP_DIR/$ZIP_FILE" -d "$TEMP_DIR"
}

certutil_check ()
{
    if type certutil > /dev/null; then
        print_style "\n***certutil is installed and will be used**\n" "info"
    else
        # Different packages for each system. Just allow them to fail and try the next currently
        $PACKAGE_MANAGER libnss3-tools 2> /dev/null
        $PACKAGE_MANAGER nss-tools 2> /dev/null
        $PACKAGE_MANAGER mozilla-nss-tools 2> /dev/null
        print_style "\n***Certutils has been installed***\n" "info"
    fi
}

ensure_nss_database_exists() {
    if [ ! -d "$HOME/.pki/nssdb" ]; then
        mkdir -p "$HOME/.pki/nssdb"
        certutil -d sql:"$HOME/.pki/nssdb" -N --empty-password
        print_style "\n***Created NSS database at $HOME/.pki/nssdb***\n" "info"
    fi

    for user_home in /home/*; do
        if [ -d "$user_home" ] && [ ! -d "$user_home/.pki/nssdb" ]; then
            mkdir -p "$user_home/.pki/nssdb"
            certutil -d sql:"$user_home/.pki/nssdb" -N --empty-password
            print_style "\n***Created NSS database at $user_home/.pki/nssdb***\n" "info"
        fi
    done
}

browser_check ()
{
    browser_installed=false

    print_style "\n***Looking for Google Chrome***\n" "info"
    # Currently supported browsers
    find_chrome

    if [ "$browser_installed" = true ]; then
        ensure_nss_database_exists
        module_import_certificates
    else
        print_style "\n***No version of Google Chrome installed***\n" "danger"

        exit "$EXIT_FAILURE"
    fi
}

find_chrome ()
{
    if type google-chrome > /dev/null; then
        print_style "\n***Found Google Chrome***\n" "info"
        browser_installed=true
    else
        print_style "\n***Google Chrome not found***\n" "warning"
    fi

     # TODO # Create database for future incase one does not exist
    # if [ ! -d "$HOME/.pki/nssdb" ]; then
    #     mkdir -p "$HOME/.pki/nssdb"
    #     certutil -d sql:"$HOME/.pki/nssdb" -N --empty-password
    # fi
}

module_import_certificates ()
{
    print_style "\n***Creating Module and Starting Import***\n" "info"
    find ~/.mozilla* /home/*/.mozilla* ~/.pki /home/*/.pki -name "cert9.db" > tmp
    while IFS= read -r nss_db
    do
        nss_dir=$(dirname "$nss_db");
        print_style "\n***Saving CAC Module into $nss_dir***\n" "info"

        # modutil -dbdir /home/my/sharednssdb -add "Example PKCS #11 Module" -libfile "/tmp/crypto.so" -mechanisms RSA:SHA256
     
        if find /usr/lib64/opensc-pkcs11.so > /dev/null 2>&1; then # Fedora, OpenSuse, Manjaro (Arch)
            sudo -u "$SUDO_USER" modutil -force -add "CAC Module" -dbdir sql:"$nss_dir" -libfile "/usr/lib64/opensc-pkcs11.so"
        elif find /usr/lib/opensc-pkcs11.so > /dev/null 2>&1; then
            sudo -u "$SUDO_USER" modutil -force -add 'CAC Module' -dbdir sql:"$nss_dir" -libfile "/usr/lib/opensc-pkcs11.so" 
        elif find /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so > /dev/null 2>&1; then # Ubuntu 18.04, Debian
            sudo -u "$SUDO_USER" modutil -force -add "CAC Module" -dbdir sql:"$nss_dir" -libfile "/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so"
        elif find /usr/lib/x86_64-linux-gnu/pkcs11/opensc-pkcs11.so > /dev/null 2>&1; then # Ubuntu 20.04
            sudo -u "$SUDO_USER" modutil -force -add "CAC Module" -dbdir sql:"$nss_dir" -libfile "/usr/lib/x86_64-linux-gnu/pkcs11/opensc-pkcs11.so"
        else
            print_style "\n***Error No module found: Please report this issue on Github***\n" "danger"
            exit "$EXIT_FAILURE"
        fi

        print_style "\n***Loading certificates into $nss_dir***\n" "info"
        # Import certificate into pki DB
        # shellcheck disable=SC2231
        for cert in ${TEMP_DIR}/${CERT_FILE}/*".cer"
        do
            echo "$cert"
            certutil -d sql:"$nss_dir" -A -t TC -n "$cert" -i "$cert"
        done
    done < tmp
    if [ ! -s tmp ]; then
        print_style "\n***No databases found***\n" "danger"
        exit $EXIT_FAILURE
    fi
    rm tmp
    print_style "\n***All certificates imported and CAC Module Added***\n" "success"

}

main