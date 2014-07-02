USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make
PACKAGE_VERSION=0.0.2
TITLE=sal_mac_facts
PACKAGE_NAME=${TITLE}
REVERSE_DOMAIN=com.grahamgilbert
PAYLOAD=\
	pack-mac_facts
	
REPO_URL=https://github.com/grahamgilbert/grahamgilbert-mac_facts.git
INSTALL_PATH=${WORK_D}/usr/local/sal/facter/

pack-mac_facts: l_usr_local
	@sudo mkdir -p ${INSTALL_PATH}
	@sudo git clone ${REPO_URL} facts
	@sudo ${CP} -R facts/lib/facter/ ${INSTALL_PATH}
	@sudo chmod -R 755 ${INSTALL_PATH}
	@sudo chown root:wheel ${INSTALL_PATH}
	@sudo rm -rf facts