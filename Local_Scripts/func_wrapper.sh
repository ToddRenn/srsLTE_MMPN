#!/usr/bin/bash

# This file contains the functions to be executed when
# starting C2I-Client.

# Functions
import_eml_file(){
        #This function clears old EML files from
        #JupiterDB directory and imports user-specified
        #EML into the JupiterDB directory.

	#Filepaths - DRY
	BASE="./infrastructure/jupiterdb"

        #Step 1. Remove old EML file(s)
        tput setaf 1
        echo "Removing old EML file(s)..."
	echo $(basename -a ${BASE}/*.eml)
	echo
        rm ${BASE}/*.eml 2> /dev/null

        #Step 2. Import new EML file(s)
        tput setaf 6
        read -a EML_FILES -p "Enter EML file(s) to import: "
        for EML_FILE in "${EML_FILES[@]}"
        do
                cp ${BASE}/modelfiles/${EML_FILE} ${BASE}

                #Check if file exists
                if [[ "${?}" -ne 0 ]]
                then
                        tput setaf 9
                        echo "### Failed to import ${EML_FILE}"
			tput sgr0
                	exit 1
		else
                        tput setaf 10
                        echo "### Imported ${EML_FILE}"
			tput sgr0
                fi
        done

	#Step 3. Profit$$$
}

set_title(){
	PS1="\[\e]2;${@}\a\]>[${@} ]$ "
}

start_jupiter_server(){
        # This function initializes JupiterDB
        # Note, may require additional troubleshooting...
	./server/jupiter-server | tee log.file
	set_title "Jupiter DB"
}

start_plugins(){
        # This function starts the minimum plugins
	./plugins/run-minimum-plugins.sh
	set_title "Plugins"
}

start_c2i(){
        # This function opens C2I-C
        ./client/c2i admin admin
	set_title "C2I Client"
}

start_smac(){
	# This function starts SMAC Commander
	./utilities/smac-commander/smac-commander
}
