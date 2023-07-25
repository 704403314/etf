# !/bin/sh
pid=`/usr/sbin/lsof -i:8089 | awk 'NR>1 {print $2}'`
kill $pid
echo "kill pid ${pid}"
nohup python /root/www/web/etf/main.py &
echo "重启成功"
echo `date`
