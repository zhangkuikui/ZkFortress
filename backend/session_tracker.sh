#!/bin/bash

for i in $(seq 1 3);do
  has_process=`ps -ef |grep ssh|grep -v sshpass | grep $2 |awk '{ print $2}'`
  #has_process获取命令结果，是进程的pid
  if [ "$has_process" = '' ];then
      echo "没有连接"
      sleep 1
  else
       echo "-----要跟踪的进程是 $has_process -----"
       today=`date "+%Y_%m_%d"`
       #当前时间
       
       today_audit_dir="log/audit/$today"
       #日志存放路径
       
       echo "日志存放路径:$today_audit_dir"
       if [ -d $today_audit_dir ]
       then
          echo "------start tracking log------"
       else
           echo "目录不存在"
           echo "today dir:$today_audit_dir"
           mkdir $today_audit_dir
       fi
           

       strace -p $has_process -t -o $today_audit_dir/session_${1}_log -f
       
     break
  fi
done
