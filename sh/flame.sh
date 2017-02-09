#!/bin/sh


if [ $# -ne 1 ];then
echo "Usage: $0 name"
exit 1
fi

perf record -a -g -p `pgrep dfa_tcp` -e cycles -- sleep 30
perf script > $1.stacks1
stackcollapse-perf.pl $1.stacks1 > $1.folded1
flamegraph.pl $1.folded1 > $1.svg

#difffolded.pl -n out.folded1 2.folded1 | flamegraph.pl > diff.svg
