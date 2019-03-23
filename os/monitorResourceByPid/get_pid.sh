ps fx|grep job_scripts/$1|grep -v 'grep'|awk '{print $1}' > $1.job.id
