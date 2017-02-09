#/bin/sh

help()
{
	echo ""
	echo "help:"
        echo "$0 -[i|s] <num|ip   string>      convert ip   format"
	echo "$0 -[d|t] <num|\"time string\">  convert time format"
	echo "$0 -[n]   <num>                  convert port"
	echo "$0 -[p]   <from>  <to>           get all num from <from> to <to>"
	echo "$0 -[q]   <strfrom> <strto>      get all ip string from <strfrom> to <strto>"
	echo ""
        exit
}


num2ip()
{
	num=$1
	num=$((num &0xffffffff))
	a=$((num>>24))
	b=$((num>>16 &0xff))
	c=$((num>>8 &0xff))
	d=$((num&0xff))
	numhex=`printf %X $num`
	echo ""
	echo "IPv4 convert: " 
	echo "$1 $num 0x$numhex --> $a.$b.$c.$d"
	echo ""
}

ip2num()
{
	ipstr=$1
	a=`echo $ipstr | awk -F'.' '{print $1}'`
	b=`echo $ipstr | awk -F'.' '{print $2}'`
	c=`echo $ipstr | awk -F'.' '{print $3}'`
	d=`echo $ipstr | awk -F'.' '{print $4}'`

	netuint=$(((d<<24) + (c<<16) + (b<<8) + a))
	hstuint=$(((a<<24) + (b<<16) + (c<<8) + d))

	netint=$netuint
	hstint=$hstuint
	#echo $netuint $hstuint	
	neth=$((netuint &0x80000000 >>31))
	hsth=$((hstuint &0x80000000 >>31))
	#echo $neth $hsth
	if [ $neth -eq 1 ]
	then
		netint=-$((0xffffffff - netuint + 1))
	fi
	if [ $hsth -eq 1 ]
	then
		hstint=-$((0xffffffff - hstuint + 1))
	fi

	nethex=`printf %X $netuint`
	hsthex=`printf %X $hstuint`

	echo ""
	echo "IPv4 convert:"
	echo "           unsigned        signed         hex            string"
	echo "convert  : $netuint        $netint        0x$nethex      $d.$c.$b.$a"
	echo "original : $hstuint        $hstint        0x$hsthex      $ipstr"
	
	echo ""
}

num2time()
{
	num=$1
	echo ""
	echo "time convert:"
	time1=`date -d "1970-01-01 UTC $num seconds"`
	time2=`date -d "1970-01-01 UTC $num seconds" "+%Y-%m-%d %H:%M:%S"`
	echo "$num --> $time2"
	echo "$num --> $time1"
	echo ""	
}

time2num()
{
	#maybe 2010-01-01 08:08:08, so $@
	time="$@"
	echo ""
	echo "time convert:"
	num=`date -d "$time" +%s`
	echo "$time --> $num"
	echo ""	
}

port()
{
        num=$1
        num=$((num &0xffff))
        a=$((num>>8))
        b=$((num &0xff))
        numhex=`printf %X $num`
	ret=$(((b<<8)+a))
        echo ""
        echo "Port convert: "
        echo "$1 $num 0x$numhex --> $ret"
        echo ""
}

getNumRange()
{
	ipfint=$1
	iptint=$2

        curr=$ipfint
        until [ $curr -gt $iptint ]
        do
                echo $curr
                curr=`expr $curr + 1`
        done

        curr=$ipfint
        until [ $curr -lt $iptint ]
        do
                echo $curr
                curr=`expr $curr - 1`
        done	
}

getStringRange()
{
	ipstrf=$1
	af=`echo $ipstrf | awk -F'.' '{print $1}'`
	bf=`echo $ipstrf | awk -F'.' '{print $2}'`
	cf=`echo $ipstrf | awk -F'.' '{print $3}'`
	df=`echo $ipstrf | awk -F'.' '{print $4}'`
	ipfint=$(((af<<24) + (bf<<16) + (cf<<8) + df))

	ipstrt=$2
	at=`echo $ipstrt | awk -F'.' '{print $1}'`
	bt=`echo $ipstrt | awk -F'.' '{print $2}'`
	ct=`echo $ipstrt | awk -F'.' '{print $3}'`
	dt=`echo $ipstrt | awk -F'.' '{print $4}'`
	iptint=$(((at<<24) + (bt<<16) + (ct<<8) + dt))

	curr=$ipfint
	until [ $curr -gt $iptint ]
	do
		num=$curr
		num=$((num &0xffffffff))
		a=$((num>>24))
		b=$((num>>16 &0xff))
		c=$((num>>8 &0xff))
		d=$((num&0xff))
		echo "$a.$b.$c.$d"
		curr=`expr $curr + 1`
	done

	curr=$ipfint
        until [ $curr -lt $iptint ]
	do
                num=$curr
                num=$((num &0xffffffff))
                a=$((num>>24))
                b=$((num>>16 &0xff))
                c=$((num>>8 &0xff))
                d=$((num&0xff))
                echo "$a.$b.$c.$d"
		
                curr=`expr $curr - 1`
        done

}


if [ $# -lt 2 ]
then
        help
fi

if [ "$1" = "-i" ]
then
	num2ip $2
elif [ "$1" = "-s" ]
then
	ip2num $2
elif [ "$1" = "-d" ]
then
	num2time $2
elif [ "$1" = "-t" ]
then
	time2num $2
elif [ "$1" = "-n" ]
then
	port $2
elif [ "$1" = "-p" ]
then
	getNumRange $2 $3
elif [ "$1" = "-q" ]
then
	getStringRange $2 $3
else
	help
fi	
