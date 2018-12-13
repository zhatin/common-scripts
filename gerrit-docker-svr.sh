docker run -h ldap-host --name ldap-service -v /home/gerrit/review_site/ldap/database:/var/lib/ldap -v /home/gerrit/review_site/ldap/config:/etc/ldap/slapd.d -e LDAP_ORGANISATION="webyun" -e LDAP_DOMAIN="webyun.cn" -e LDAP_ADMIN_PASSWORD="webyun@123" -d osixia/openldap

docker run --name phpldapadmin-service --hostname phpldapadmin-host -p 6443:443 --link ldap-service:ldap-host --env PHPLDAPADMIN_LDAP_HOSTS=ldap-host --detach osixia/phpldapadmin


docker run -d --name gerrit-service --hostname gerrit-host -v /home/gerrit/review_site:/var/gerrit/review_site -p 8080:8080 -p 29418:29418 -v /etc/localtime:/etc/localtime:ro -e GERRIT_INIT_ARGS='--install-plugin=download-commands' -e WEBURL=http://10.28.27.63:8080 --link ldap-service:ldap-host -e AUTH_TYPE=LDAP -e LDAP_SERVER=ldap://ldap-host -e LDAP_ACCOUNTBASE='DC=webyun,DC=cn' openfrontier/gerrit


docker run -d --name jenkins-service --hostname jenkins-host -p 8090:8080 -p 50000:50000 --link gerrit-service:gerrit-host -v /home/jenkins:/var/jenkins_home jenkins/jenkins:lts


mvn install:install-file   -DgroupId=org.artofsolving.jodconverter   -DartifactId=jodconverter-core   -Dpackaging=jar   -Dversion=3.0-beta-4   -Dfile=/var/jenkins_home/jars/jodconverter-core-3.0-beta-4.jar   -DgeneratePom=true

mvn install:install-file   -DgroupId=com.artofsolving   -DartifactId=jodconverter   -Dpackaging=jar   -Dversion=2.2.2   -Dfile=/var/jenkins_home/jars/jodconverter-2.2.2.jar   -DgeneratePom=true

mvn install:install-file   -DgroupId=org.hyperic   -DartifactId=sigar   -Dpackaging=jar   -Dversion=1.6.4   -Dfile=/var/jenkins_home/jars/sigar-1.6.4.jar   -DgeneratePom=true


docker run -d \
  -p 5000:5000 \
  --restart=always \
  --name registry-service \
  --hostname registry-host  -v /var/registry:/var/lib/registry \
  registry:2


