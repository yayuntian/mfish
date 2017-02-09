from __future__ import print_function

import os
import sys
import json
from pyspark import SparkContext
from pyspark.sql import SQLContext

def tcp_server_conn():
    server_conns = {}
    context = sqlContext.sql("SELECT dst_ipv4, final_status, unknown_conn, count(final_status) as flows,"
                + " sum(client_latency_sec) as client_latency_sec, sum(client_latency_usec) as client_latency_usec, sum(server_latency_sec) as server_latency_sec,"
                + " sum(server_latency_usec) as server_latency_usec"
                + " FROM tcp where (final_status != 5 and final_status != 6) group by dst_ipv4, unknown_conn, final_status")
    context.show()
    context = context.toJSON().collect()
    for opt in context:
        tmp =  json.loads(opt)
        dst_ip = tmp["dst_ipv4"]
        status = tmp["final_status"]
        unknown_conn = tmp["unknown_conn"]
        flows = tmp["flows"]
        if dst_ip not in server_conns.keys():
            server_conns[dst_ip]={"server_latency_total":0,"client_latency_total":0,"counter":0,
                                                   "new":0,"closed":0,
                                                   "fin":0,"reset":0,"timeout":0,"scan":0,"syn_attack":0}
        info = server_conns[dst_ip]
        if unknown_conn == 0:
            info["counter"] += flows
            info["server_latency_total"] = flows * (tmp["server_latency_sec"] * 1000000 + tmp["server_latency_usec"])
            info["client_latency_total"] = flows * (tmp["client_latency_sec"] * 1000000 + tmp["client_latency_usec"])
        info["closed"] += flows
        if status == 1:
            info["scan"] += flows
        elif status == 2:
            info["syn_attack"] += flows
        elif status == 7:
            info["reset"] += flows
        elif status == 8:
            info["fin"] += flows
        if status in [1, 2, 3, 4]: 
            info["timeout"] += flows

    print(server_conns)
    return server_conns


def tcp_server():
    server_conns = tcp_server_conn()

    context = sqlContext.sql("SELECT dst_group_id , dst_ipv4, sum(in_bytes + out_bytes) as bytes_total, sum(in_bytes) as bytes_in, sum(out_bytes) as bytes_out,"
                + " sum(in_pkts + out_pkts) as packets_total, sum(in_pkts) as packets_in, sum(out_pkts) as packets_out, sum(retransmitted_in_pkts) as retransmitted_in,"
                + " sum(retransmitted_out_pkts) as retransmitted_out, sum(ooorder_in_pkts) as ooorder_in, sum(ooorder_out_pkts) as ooorder_out,"
                + " sum(tcp_window_size_zero) as tcp_window_size_zero FROM tcp group by dst_group_id, dst_ipv4")
   
    context.show()
    context = context.toJSON().collect()
    
    server = {}
    server["all"] = {}
    for opt in context:
        tmp = json.loads(opt)
        group_id = tmp["dst_group_id"]
        dst_ip = tmp["dst_ipv4"]
        if group_id not in server:
            server[group_id] = {}
        if dst_ip in server_conns:
            info = server_conns[dst_ip]
        else:
            info = {"server_latency_total":0, "client_latency_total":0, "counter":0,
                            "new":0, "closed":0, "fin":0, "reset":0, "timeout":0, "scan":0, "syn_attack":0}

        tmp["retransfer_rate"] = 0
        tmp["outoforder_rate"] = 0
        tmp["server_latency"] = 0
        tmp["client_latency"] = 0

        tmp["new"] = 0
        tmp["counter"] = info["counter"]
        tmp["server_latency_total"] = info["server_latency_total"]
        tmp["client_latency_total"] = info["client_latency_total"]
        tmp["closed"] = info["closed"]
        tmp["fin"] = info["fin"]
        tmp["reset"] = info["reset"]
        tmp["timeout"] = info["timeout"]
        tmp["scan"] = info["scan"]
        tmp["syn_attack"] = info["syn_attack"]

        if tmp["counter"] > 1:
            tmp["server_latency"] = tmp["server_latency_total"] / tmp["counter"]
            tmp["client_latency"] = tmp["client_latency_total"] / tmp["counter"]

        if tmp["packets_total"] > 1:
            tmp["retransfer_rate"] = (tmp['retransmitted_in'] + tmp['retransmitted_out'])*1.0 / tmp["packets_total"]
            tmp["outoforder_rate"] = (tmp['ooorder_in'] + tmp['ooorder_out'])*1.0 / tmp["packets_total"]
        
        server[group_id][dst_ip] = tmp

    print(server)
    with open("tcp_server.json", "w") as f:
        json.dump(server, f, indent=4)


def tcp_conn():
    tcp_conns = {}
    context = sqlContext.sql("SELECT dst_group_id , final_status, unknown_conn, count(final_status) as flows,"
                + " sum(client_latency_sec) as client_latency_sec, sum(client_latency_usec) as client_latency_usec, sum(server_latency_sec) as server_latency_sec,"
                + " sum(server_latency_usec) as server_latency_usec"
                + " FROM tcp where (final_status != 5 and final_status != 6) group by dst_group_id, unknown_conn, final_status")
    context.show()
    context = context.toJSON().collect()
    for opt in context:
        tmp =  json.loads(opt)
        group_id = tmp["dst_group_id"]
        status = tmp["final_status"]
        unknown_conn = tmp["unknown_conn"]
        flows = tmp["flows"]
        if group_id not in tcp_conns.keys():
            tcp_conns[group_id] = {"server_latency_total":0,"client_latency_total":0,"counter":0,
                            "new":0,"closed":0,"fin":0,"reset":0,"timeout":0,"scan":0,"syn_attack":0}
        tcp_conn_info = tcp_conns[group_id]
        if unknown_conn == 0:
            tcp_conn_info["counter"] += flows
            tcp_conn_info["server_latency_total"] = flows * (tmp["server_latency_sec"] * 1000000 + tmp["server_latency_usec"])
            tcp_conn_info["client_latency_total"] = flows * (tmp["client_latency_sec"] * 1000000 + tmp["client_latency_usec"])
        tcp_conn_info["closed"] += flows
        if status == 1:
            tcp_conn_info["scan"] += flows
        elif status == 2:
            tcp_conn_info["syn_attack"] += flows
        elif status == 7:
            tcp_conn_info["reset"] += flows
        elif status == 8:
            tcp_conn_info["fin"] += flows
        if status in [1, 2, 3, 4]: 
            tcp_conn_info["timeout"] += flows

    print(tcp_conns)
    return tcp_conns
 

def tcp_info():
    tcp_conns = tcp_conn()

    context = sqlContext.sql("SELECT dst_group_id , sum(in_bytes + out_bytes) as bytes_total, sum(in_bytes) as bytes_in, sum(out_bytes) as bytes_out,"
                + " sum(in_pkts + out_pkts) as packets_total, sum(in_pkts) as packets_in, sum(out_pkts) as packets_out, sum(retransmitted_in_pkts) as retransmitted_in,"
                + " sum(retransmitted_out_pkts) as retransmitted_out, sum(ooorder_in_pkts) as ooorder_in, sum(ooorder_out_pkts) as ooorder_out,"
                + " sum(tcp_window_size_zero) as tcp_window_size_zero FROM tcp group by dst_group_id")
   
    context.show()
    #context.registerTempTable("tcp_info")
    context = context.toJSON().collect()
    
    tcp = {}
    tcp["all"] = {}
    for opt in context:
        tmp = json.loads(opt)
        group_id = tmp["dst_group_id"]
        if group_id in tcp_conns:
            tcp_conn_info = tcp_conns[group_id]
        else:
            tcp_conn_info = {"server_latency_total":0, "client_latency_total":0, "counter":0,
                            "new":0, "closed":0, "fin":0, "reset":0, "timeout":0, "scan":0, "syn_attack":0}

        tmp["retransfer_rate"] = 0
        tmp["outoforder_rate"] = 0
        tmp["server_latency"] = 0
        tmp["client_latency"] = 0

        tmp["new"] = 0
        tmp["counter"] = tcp_conn_info["counter"]
        tmp["server_latency_total"] = tcp_conn_info["server_latency_total"]
        tmp["client_latency_total"] = tcp_conn_info["client_latency_total"]
        tmp["closed"] = tcp_conn_info["closed"]
        tmp["fin"] = tcp_conn_info["fin"]
        tmp["reset"] = tcp_conn_info["reset"]
        tmp["timeout"] = tcp_conn_info["timeout"]
        tmp["scan"] = tcp_conn_info["scan"]
        tmp["syn_attack"] = tcp_conn_info["syn_attack"]

        if tmp["counter"] > 1:
            tmp["server_latency"] = tmp["server_latency_total"] / tmp["counter"]
            tmp["client_latency"] = tmp["client_latency_total"] / tmp["counter"]

        if tmp["packets_total"] > 1:
            tmp["retransfer_rate"] = (tmp['retransmitted_in'] + tmp['retransmitted_out'])*1.0 / tmp["packets_total"]
            tmp["outoforder_rate"] = (tmp['ooorder_in'] + tmp['ooorder_out'])*1.0 / tmp["packets_total"]
        
        tcp[group_id] = tmp

    print(tcp)
    with open("tcp_info.json", "w") as f:
        json.dump(tcp, f, indent=4)


def tcp_dst_port():
    context = sqlContext.sql("SELECT dst_group_id, dst_port, sum(in_bytes + out_bytes) as total_bytes, sum(in_bytes) as bytes_in, sum(out_bytes) as bytes_out FROM tcp group by dst_group_id, dst_port")
   
    context.show()

    context.registerTempTable("tcp_dst_port")
    output = {}

    for group_id in total_groups:
        output[group_id.dst_group_id] = {}
        for opt in total_dst_ports:
            topN_sql = "select dst_port, total_bytes, bytes_in, bytes_out from tcp_dst_port where dst_group_id = %s and dst_port = %s" % (group_id.dst_group_id, opt.dst_port)
            topN_collect = sqlContext.sql(topN_sql).toJSON().collect()
            tmp = list(json.loads(x) for x in topN_collect)
            if not tmp:
                continue
            output[group_id.dst_group_id][opt.dst_port] = tmp[0]
    print(output)
    with open("tcp_dst_port.json", "w") as f:
        json.dump(output, f, indent=4)


def tcp_proto():
    urls = sqlContext.sql("SELECT dst_group_id, l7_proto, sum(in_bytes + out_bytes) as total_bytes, sum(in_bytes) as bytes_in, sum(out_bytes) as bytes_out FROM tcp group by dst_group_id, l7_proto")
   
    urls.show()

    urls.registerTempTable("tcp_proto")
    output = {}

    for group_id in total_groups:
        output[group_id.dst_group_id] = {}
        for opt in total_l7_protos:
            topN_sql = "select total_bytes, bytes_in, bytes_out from tcp_proto where dst_group_id = %s and l7_proto = %s" % (group_id.dst_group_id, opt.l7_proto)
            topN_collect = sqlContext.sql(topN_sql).toJSON().collect()
            tmp = list(json.loads(x) for x in topN_collect)
            if not tmp:
                continue
            output[group_id.dst_group_id][opt.l7_proto] = tmp[0]
    print(output)
    with open("tcp_proto.json", "w") as f:
        json.dump(output, f, indent=4)
    

if __name__ == "__main__":
    sc = SparkContext(appName="TcpSQL")
    sqlContext = SQLContext(sc)

    # A JSON dataset is pointed to by path.
    # The path can be either a single text file or a directory storing text files.
    if len(sys.argv) < 2:
        #path = "file://" + os.path.join(os.environ['SPARK_HOME'], "examples/src/main/resources/people.json")
        path = "file://" + "/usr/spark-1.4.1-bin-hadoop2.6/tcp.json"
    else:
        path = sys.argv[1]
    # Create a DataFrame from the file(s) pointed to by path
    df = sqlContext.read.json(path).cache()
    total_groups = df.select("dst_group_id").distinct().dropna().collect()
    total_l7_protos = df.select("l7_proto").distinct().dropna().collect()
    total_dst_ports = df.select("dst_port").distinct().dropna().collect()
   
    # Register this DataFrame as a table.
    df.registerTempTable("tcp")
    tcp_proto()
    tcp_dst_port()
    tcp_info()
    tcp_server()
    sc.stop()
