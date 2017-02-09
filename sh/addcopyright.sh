#!/bin/bash 
#add copyright information to C files and C++ filels without any copyright information 
for file in $( find ./ -type f -name "*.c" -o -name "*.cpp" -o -name "*.cc" -o -name "*.h" ) 
do
	grep "Copyright" $file > /dev/null
	if [ $? -ne 0 ] ;
	then
		sed -i '1i \/*******************************************************************************\n *  Copyright (c) 2011-2014 WuXi ClearClouds System, Ltd.\n *  All Rights Reserved.\n *\n *  Redistribution and use in source and binary forms with or without\n *  modification are permitted provided that: (1) source distributions\n *  retain this entire copyright notice and comment, and (2) distributions\n *  including binaries display the following acknowledgement: "This product\n *  includes software developed by WuXi ClearClouds System, Ltd. and its\n *  contributors" in the documentation or other materials provided with the\n *  distribution and in all advertising materials mentioning features or use\n *  of this software. Neither the name of the company nor the names of its\n *  contributors may be used to endorse or promote products derived from this\n *  software without specific prior written permission.\n *\n *  THIS SOFTWARE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR IMPLIED\n *  WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF\n *  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.\n *******************************************************************************/' $file
	fi
#update Date for files that have been added copyriht information	
	sed -i 's/Copyright (c) 2011-2014 WuXi/Copyright (c) 2011-2015 WuXi/' $file
done
echo "all C files hava been added copyright information"
echo "all C++ files hava been added copyright information"

