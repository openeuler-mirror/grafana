%global grafana_arches %{lua: go_arches = {}
  for arch in rpm.expand("%{go_arches}"):gmatch("%S+") do
    go_arches[arch] = 1
  end
  for arch in rpm.expand("%{nodejs_arches}"):gmatch("%S+") do
    if go_arches[arch] then
      print(arch .. " ")
  end
end}

# Unbundle Grafana vendor sources and instead use BuildRequires
# on platforms that have enough golang devel support.

Name:             grafana
Version:          6.7.4
Release:          1%{?dist}
Summary:          Metrics dashboard and graph editor
License:          ASL 2.0
URL:              https://grafana.org

# Source0 contains the tagged upstream sources
Source0:          https://github.com/grafana/grafana/archive/v%{version}/%{name}-%{version}.tar.gz

# Source1 contains the front-end javascript modules bundled into a webpack
Source1:          grafana_webpack-%{version}.tar.gz

# Source2 contains Grafana configuration defaults for distributions
Source2:          distro-defaults.ini

# Source3 is the script to create the webpack from grafana sources
Source3:          make_grafana_webpack.sh

# Source4 is the script to generate the list of Go build dependencies:
Source4:          list_go_buildrequires.sh

# Source5 is the script to generate the list of bundled nodejs packages
Source5:          list_bundled_nodejs_packages.py

# Intersection of go_arches and nodejs_arches
ExclusiveArch:    aarch64 x86_64

# omit golang debugsource, see BZ995136 and related
%global           dwz_low_mem_die_limit 0
%global           _debugsource_template %{nil}

%global           GRAFANA_USER %{name}
%global           GRAFANA_GROUP %{name}
%global           GRAFANA_HOME %{_datadir}/%{name}

# grafana-server service daemon uses systemd
%{?systemd_requires}
Requires(pre):    shadow-utils

BuildRequires:    git, systemd, golang


# Declare all nodejs modules bundled in the webpack - this is for security
# purposes so if nodejs-foo ever needs an update, affected packages can be
# easily identified.
# Note: generated with the list_bundled_nodejs_packages.sh script (see README.md)
Provides: bundled(nodejs-@braintree/sanitize-url) = 4.0.0
Provides: bundled(nodejs-@grafana/slate-react) = 0.22.9-grafana
Provides: bundled(nodejs-@reduxjs/toolkit) = 1.2.1
Provides: bundled(nodejs-@torkelo/react-select) = 3.0.8
Provides: bundled(nodejs-@types/md5) = 2.1.33
Provides: bundled(nodejs-@types/react-loadable) = 5.5.2
Provides: bundled(nodejs-@types/react-virtualized-auto-sizer) = 1.0.0
Provides: bundled(nodejs-@types/uuid) = 3.4.7
Provides: bundled(nodejs-abortcontroller-polyfill) = 1.4.0
Provides: bundled(nodejs-angular) = 1.6.9
Provides: bundled(nodejs-angular-bindonce) = 0.3.1
Provides: bundled(nodejs-angular-native-dragdrop) = 1.2.2
Provides: bundled(nodejs-angular-route) = 1.6.6
Provides: bundled(nodejs-angular-sanitize) = 1.6.6
Provides: bundled(nodejs-baron) = 3.0.3
Provides: bundled(nodejs-brace) = 0.10.0
Provides: bundled(nodejs-calculate-size) = 1.1.1
Provides: bundled(nodejs-classnames) = 2.2.6
Provides: bundled(nodejs-clipboard) = 2.0.4
Provides: bundled(nodejs-core-js) = 1.2.7
Provides: bundled(nodejs-d3) = 5.15.0
Provides: bundled(nodejs-d3-scale-chromatic) = 1.5.0
Provides: bundled(nodejs-emotion) = 10.0.27
Provides: bundled(nodejs-eventemitter3) = 2.0.3
Provides: bundled(nodejs-fast-text-encoding) = 1.0.0
Provides: bundled(nodejs-file-saver) = 1.3.8
Provides: bundled(nodejs-hoist-non-react-statics) = 3.3.0
Provides: bundled(nodejs-immutable) = 3.8.2
Provides: bundled(nodejs-is-hotkey) = 0.1.4
Provides: bundled(nodejs-jquery) = 3.4.1
Provides: bundled(nodejs-lodash) = 3.10.1
Provides: bundled(nodejs-lru-cache) = 4.1.5
Provides: bundled(nodejs-marked) = 0.3.19
Provides: bundled(nodejs-md5) = 2.2.1
Provides: bundled(nodejs-memoize-one) = 4.1.0
Provides: bundled(nodejs-moment) = 2.24.0
Provides: bundled(nodejs-mousetrap) = 1.6.3
Provides: bundled(nodejs-mousetrap-global-bind) = 1.1.0
Provides: bundled(nodejs-nodemon) = 1.18.10
Provides: bundled(nodejs-papaparse) = 4.6.3
Provides: bundled(nodejs-prismjs) = 1.16.0
Provides: bundled(nodejs-prop-types) = 15.7.2
Provides: bundled(nodejs-rc-cascader) = 0.17.5
Provides: bundled(nodejs-re-resizable) = 6.2.0
Provides: bundled(nodejs-react) = 16.10.2
Provides: bundled(nodejs-react-dom) = 16.10.2
Provides: bundled(nodejs-react-grid-layout) = 0.17.1
Provides: bundled(nodejs-react-highlight-words) = 0.11.0
Provides: bundled(nodejs-react-loadable) = 5.5.0
Provides: bundled(nodejs-react-popper) = 1.3.3
Provides: bundled(nodejs-react-redux) = 7.1.1
Provides: bundled(nodejs-react-sizeme) = 2.5.2
Provides: bundled(nodejs-react-split-pane) = 0.1.89
Provides: bundled(nodejs-react-transition-group) = 2.6.1
Provides: bundled(nodejs-react-use) = 12.8.0
Provides: bundled(nodejs-react-virtualized-auto-sizer) = 1.0.2
Provides: bundled(nodejs-react-window) = 1.7.1
Provides: bundled(nodejs-redux) = 3.7.2
Provides: bundled(nodejs-redux-logger) = 3.0.6
Provides: bundled(nodejs-redux-thunk) = 2.3.0
Provides: bundled(nodejs-regenerator-runtime) = 0.11.1
Provides: bundled(nodejs-reselect) = 4.0.0
Provides: bundled(nodejs-rst2html) = 1.0.4
Provides: bundled(nodejs-rxjs) = 5.5.12
Provides: bundled(nodejs-search-query-parser) = 1.5.2
Provides: bundled(nodejs-slate) = 0.47.8
Provides: bundled(nodejs-slate-plain-serializer) = 0.7.10
Provides: bundled(nodejs-tether) = 1.4.5
Provides: bundled(nodejs-tether-drop) = 1.5.0
Provides: bundled(nodejs-tinycolor2) = 1.4.1
Provides: bundled(nodejs-tti-polyfill) = 0.2.2
Provides: bundled(nodejs-uuid) = 3.3.3
Provides: bundled(nodejs-whatwg-fetch) = 3.0.0
Provides: bundled(nodejs-xss) = 1.0.3


%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.


%package cloudwatch
Requires: %{name} = %{version}-%{release}
Summary: Grafana cloudwatch datasource

%description cloudwatch
The Grafana cloudwatch datasource.

%package elasticsearch
Requires: %{name} = %{version}-%{release}
Summary: Grafana elasticsearch datasource

%description elasticsearch
The Grafana elasticsearch datasource.

%package azure-monitor
Requires: %{name} = %{version}-%{release}
Summary: Grafana azure-monitor datasource

%description azure-monitor
The Grafana azure-monitor datasource.

%package graphite
Requires: %{name} = %{version}-%{release}
Summary: Grafana graphite datasource

%description graphite
The Grafana graphite datasource.

%package influxdb
Requires: %{name} = %{version}-%{release}
Summary: Grafana influxdb datasource

%description influxdb
The Grafana influxdb datasource.

%package loki
Requires: %{name} = %{version}-%{release}
Summary: Grafana loki datasource

%description loki
The Grafana loki datasource.

%package mssql
Requires: %{name} = %{version}-%{release}
Summary: Grafana mssql datasource

%description mssql
The Grafana mssql datasource.

%package mysql
Requires: %{name} = %{version}-%{release}
Summary: Grafana mysql datasource

%description mysql
The Grafana mysql datasource.

%package opentsdb
Requires: %{name} = %{version}-%{release}
Summary: Grafana opentsdb datasource

%description opentsdb
The Grafana opentsdb datasource.

%package postgres
Requires: %{name} = %{version}-%{release}
Summary: Grafana postgres datasource

%description postgres
The Grafana postgres datasource.

%package prometheus
Requires: %{name} = %{version}-%{release}
Summary: Grafana prometheus datasource

%description prometheus
The Grafana prometheus datasource.

%package stackdriver
Requires: %{name} = %{version}-%{release}
Summary: Grafana stackdriver datasource

%description stackdriver
The Grafana stackdriver datasource.


%prep
%setup -q -T -D -b 0
%setup -q -T -D -b 1

# Set up build subdirs and links
mkdir -p %{_builddir}/src/github.com/grafana
ln -sf %{_builddir}/%{name}-%{version} \
    %{_builddir}/src/github.com/grafana/grafana

# remove some (apparent) development files, for rpmlint
rm -f public/sass/.sass-lint.yml public/test/.jshintrc

%build
# Build the server-side binaries
cd %{_builddir}/src/github.com/grafana/grafana
%global archbindir bin/`go env GOOS`-`go env GOARCH`
echo _builddir=%{_builddir} archbindir=%{archbindir} gopath=%{gopath}
[ ! -d %{archbindir} ] && mkdir -p %{archbindir}

# non-modular build
export GOPATH=%{_builddir}:%{gopath}
export GO111MODULE=off; rm -f go.mod

# see grafana-X.X.X/build.go
export LDFLAGS="-X main.version=%{version} -X main.buildstamp=${SOURCE_DATE_EPOCH}"
for cmd in grafana-cli grafana-server; do
    go build -o %{archbindir}/${cmd} ./pkg/cmd/${cmd}
done

%install
# Fix up arch bin directories
[ ! -d bin/x86_64 ] && ln -sf linux-amd64 bin/x86_64
[ ! -d bin/i386 ] && ln -sf linux-386 bin/i386
[ ! -d bin/ppc64le ] && ln -sf linux-ppc64le bin/ppc64le
[ ! -d bin/s390x ] && ln -sf linux-s390x bin/s390x
[ ! -d bin/arm ] && ln -sf linux-arm bin/arm
[ ! -d bin/arm64 ] && ln -sf linux-arm64 bin/aarch64
[ ! -d bin/aarch64 ] && ln -sf linux-aarch64 bin/aarch64

# dirs, shared files, public html, webpack
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_libexecdir}/%{name}
cp -a conf public %{buildroot}%{_datadir}/%{name}

# wrappers
install -p -m 755 packaging/wrappers/grafana-cli %{buildroot}%{_sbindir}/%{name}-cli

# binaries
install -p -m 755 %{archbindir}/%{name}-server %{buildroot}%{_sbindir}
install -p -m 755 %{archbindir}/%{name}-cli %{buildroot}%{_libexecdir}/%{name}

# man pages

# config dirs
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/sysconfig

# config defaults
install -p -m 640 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/grafana.ini
install -p -m 640 conf/ldap.toml %{buildroot}%{_sysconfdir}/%{name}/ldap.toml
install -p -m 644 %{SOURCE2} %{buildroot}%{_datadir}/%{name}/conf/defaults.ini
install -p -m 644 packaging/rpm/sysconfig/grafana-server \
    %{buildroot}%{_sysconfdir}/sysconfig/grafana-server

# config database directory and plugins
install -d -m 750 %{buildroot}%{_sharedstatedir}/%{name}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{name}/plugins

# log directory
install -d %{buildroot}%{_localstatedir}/log/%{name}

# systemd service files
install -d %{buildroot}%{_unitdir} # only needed for manual rpmbuilds
install -p -m 644 packaging/rpm/systemd/grafana-server.service \
    %{buildroot}%{_unitdir}

# daemon run pid file config for using tmpfs
install -d %{buildroot}%{_tmpfilesdir}
echo "d %{_rundir}/%{name} 0755 %{GRAFANA_USER} %{GRAFANA_GROUP} -" \
    > %{buildroot}%{_tmpfilesdir}/%{name}.conf

%pre
getent group %{GRAFANA_GROUP} >/dev/null || groupadd -r %{GRAFANA_GROUP}
getent passwd %{GRAFANA_USER} >/dev/null || \
    useradd -r -g %{GRAFANA_GROUP} -d %{GRAFANA_HOME} -s /sbin/nologin \
    -c "%{GRAFANA_USER} user account" %{GRAFANA_USER}
exit 0

%preun
%systemd_preun grafana-server.service

%post
%systemd_post grafana-server.service
# create grafana.db with secure permissions on new installations
# otherwise grafana-server is creating grafana.db on first start
# with world-readable permissions, which may leak encrypted datasource
# passwords to all users (if the secret_key in grafana.ini was not changed)

# https://bugzilla.redhat.com/show_bug.cgi?id=1805472
if [ "$1" = 1 ] && [ ! -f %{_sharedstatedir}/%{name}/grafana.db ]; then
    touch %{_sharedstatedir}/%{name}/grafana.db
fi

# apply secure permissions to grafana.db if it exists
# (may not exist on upgrades, because users can choose between sqlite/mysql/postgres)
if [ -f %{_sharedstatedir}/%{name}/grafana.db ]; then
    chown %{GRAFANA_USER}:%{GRAFANA_GROUP} %{_sharedstatedir}/%{name}/grafana.db
    chmod 640 %{_sharedstatedir}/%{name}/grafana.db
fi

# required for upgrades
chmod 640 %{_sysconfdir}/%{name}/grafana.ini
chmod 640 %{_sysconfdir}/%{name}/ldap.toml

%postun
%systemd_postun_with_restart grafana-server.service


%check
cd %{_builddir}/src/github.com/grafana/grafana
export GOPATH=%{_builddir}:%{gopath}
# remove tests currently failing - these two are due to a symlink
# BUILD/src/github.com/grafana/grafana -> BUILD/grafana-6.6.1
rm -f pkg/services/provisioning/dashboards/file_reader_linux_test.go
rm -f pkg/services/provisioning/dashboards/file_reader_test.go
export GO111MODULE=off
go test ./pkg/...


%files
# binaries and wrappers
%{_sbindir}/%{name}-server
%{_sbindir}/%{name}-cli
%{_libexecdir}/%{name}

# config files
%dir %{_sysconfdir}/%{name}
%config(noreplace) %attr(640, root, %{GRAFANA_GROUP}) %{_sysconfdir}/%{name}/grafana.ini
%config(noreplace) %attr(640, root, %{GRAFANA_GROUP}) %{_sysconfdir}/%{name}/ldap.toml
%config(noreplace) %{_sysconfdir}/sysconfig/grafana-server

# Grafana configuration to dynamically create /run/grafana/grafana.pid on tmpfs
%{_tmpfilesdir}/%{name}.conf

# config database directory and plugins
%attr(750, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}
%attr(-, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}/plugins

# shared directory and all files therein, except some datasources
%{_datadir}/%{name}

# built-in datasources that are sub-packaged
%global dsdir %{_datadir}/%{name}/public/app/plugins/datasource
%exclude %{dsdir}/cloudwatch 
%exclude %{dsdir}/elasticsearch 
%exclude %{dsdir}/graphite
%exclude %{dsdir}/grafana-azure-monitor-datasource
%exclude %{dsdir}/influxdb
%exclude %{dsdir}/loki
%exclude %{dsdir}/mssql
%exclude %{dsdir}/mysql
%exclude %{dsdir}/opentsdb
%exclude %{dsdir}/postgres
%exclude %{dsdir}/prometheus
%exclude %{dsdir}/stackdriver

%dir %{_datadir}/%{name}/conf
%attr(-, root, %{GRAFANA_GROUP}) %{_datadir}/%{name}/conf/*

# systemd service file
%{_unitdir}/grafana-server.service

# log directory - grafana.log is created by grafana-server, and it does it's own log rotation
%attr(0755, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_localstatedir}/log/%{name}

# man pages for grafana binaries

# other docs and license
%license LICENSE
%doc CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md NOTICE.md
%doc PLUGIN_DEV.md README.md ROADMAP.md UPGRADING_DEPENDENCIES.md

#
# datasources split out into subpackages
#
%files cloudwatch
%{_datadir}/%{name}/public/app/plugins/datasource/cloudwatch
%doc %{_datadir}/%{name}/public/app/plugins/datasource/cloudwatch/README.md

%files elasticsearch
%{_datadir}/%{name}/public/app/plugins/datasource/elasticsearch
%doc %{_datadir}/%{name}/public/app/plugins/datasource/elasticsearch/README.md

%files azure-monitor
%{_datadir}/%{name}/public/app/plugins/datasource/grafana-azure-monitor-datasource

%files graphite
%{_datadir}/%{name}/public/app/plugins/datasource/graphite
%doc %{_datadir}/%{name}/public/app/plugins/datasource/graphite/README.md

%files influxdb
%{_datadir}/%{name}/public/app/plugins/datasource/influxdb
%doc %{_datadir}/%{name}/public/app/plugins/datasource/influxdb/README.md

%files loki
%{_datadir}/%{name}/public/app/plugins/datasource/loki
%doc %{_datadir}/%{name}/public/app/plugins/datasource/loki/README.md

%files mssql
%{_datadir}/%{name}/public/app/plugins/datasource/mssql
%doc %{_datadir}/%{name}/public/app/plugins/datasource/mssql/README.md

%files mysql
%{_datadir}/%{name}/public/app/plugins/datasource/mysql
%doc %{_datadir}/%{name}/public/app/plugins/datasource/mysql/README.md

%files opentsdb
%{_datadir}/%{name}/public/app/plugins/datasource/opentsdb
%doc %{_datadir}/%{name}/public/app/plugins/datasource/opentsdb/README.md

%files postgres
%{_datadir}/%{name}/public/app/plugins/datasource/postgres
%doc %{_datadir}/%{name}/public/app/plugins/datasource/postgres/README.md

%files prometheus
%{_datadir}/%{name}/public/app/plugins/datasource/prometheus
%doc %{_datadir}/%{name}/public/app/plugins/datasource/prometheus/README.md

%files stackdriver
%{_datadir}/%{name}/public/app/plugins/datasource/stackdriver
%doc %{_datadir}/%{name}/public/app/plugins/datasource/stackdriver/README.md


%changelog
* Tue Aug 11 2020 houjian <houjian@kylinos.cn> - 6.7.4-1
- Package init
