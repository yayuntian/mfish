#!/bin/bash

IPCS_M=`ipcs -m | egrep "0x[0-9a-f]+ [0-9]+"`

if [ -n "$IPCS_M" ]; then
	NATTACHS="$(echo "$IPCS_M" | awk -F ' ' '{print $6}')"
	ARRAY_NATTACHS=(${NATTACHS// / })
	IPCS_COUNT=${#ARRAY_NATTACHS[@]}
	HANDLES="$(echo "$IPCS_M" | awk -F ' ' '{print $2}')"
	ARRAY_HANDLES=(${HANDLES// / })

	for (( i=0; i<$IPCS_COUNT; i++ ))
	do
		if test "${ARRAY_NATTACHS[$i]}" == "0"; then
			ipcrm -m ${ARRAY_HANDLES[$i]}
		fi
	done
fi
