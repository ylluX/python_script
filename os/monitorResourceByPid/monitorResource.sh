if [ $# -lt 1 ] || [ $1 == "-h" ] || [ $1 == "--help" ] || [ $1 == "-help" ]; then
echo "[monitor resource by job_id of qsub]: sh `basename $0` jobid"
echo "[monitor resource by pid]: sh `basename $0` -pid pid"
exit
elif [ $# -eq 1 ]; then
    echo "Monitor Node: $HOSTNAME"
    echo "Monitor CMD: sh `basename $0` $@"
    path=`pwd`
    host=`qstat|grep $1|awk '{print $8}'|cut -d@ -f2|sed 's/.local//g'`
    jobid=`qstat|grep $1|awk '{print $1}'`
    ssh -YT $host <<EOF
cd $path
sh /share/nas1/luyl/tools/monitorResourceByPid/get_pid.sh $jobid
python -u /share/nas1/luyl/tools/monitorResourceByPid/monitorResourceByPid.py $jobid.job.id
EOF
    sleep 5
    rm $jobid.job.id
elif [ $# -eq 2 ] && [ $1 == "-pid" ]; then
    echo "Monitor Node: $HOSTNAME"
    echo "Monitor CMD: sh `basename $0` $@"
    python -u /share/nas1/luyl/tools/monitorResourceByPid/monitorResourceByPid.py $2
else
    echo "Error: sh `basename $0` -h to see help information"
fi

