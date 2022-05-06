%if ! 0%{?gobuild:1}
%define gobuild(o:) GO111MODULE=off go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/openEuler/openEuler-hardened-ld '" -a -v -x %{?**};
%endif
%if ! 0%{?gotest:1}
%define gotest() GO111MODULE=off go test -buildmode pie -compiler gc -ldflags "${LDFLAGS:-} -extldflags '-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/openEuler/openEuler-hardened-ld '" %{?**};
%endif

Name:             grafana
Version:          7.5.15
Release:          1
Summary:          Metrics dashboard and graph editor
License:          Apache 2.0
URL:              https://grafana.org
# Source0 contains the tagged upstream sources
Source0:          https://github.com/grafana/grafana/archive/v%{version}/%{name}-%{version}.tar.gz
# Source1 contains the bundled Go and Node.js dependencies
Source1:          grafana-vendor-%{version}-1.tar.xz
# Source2 contains the precompiled frontend
Source2:          grafana-webpack-%{version}-1.tar.gz
# Source3 contains Grafana configuration defaults for distributions
Source3:          distro-defaults.ini
# Source4 contains the Makefile to create the vendor and webpack bundles
Source4:          Makefile
# Source5 contains the script to build the frontend
Source5:          build_frontend.sh
# Source6 contains the script to generate the list of bundled nodejs packages
Source6:          list_bundled_nodejs_packages.py
# Source7 contains the script to create the vendor and webpack bundles in a container
Source7:          create_bundles_in_container.sh

# Patches
Patch1:           001-wrappers-grafana-cli.patch
Patch2:           002-manpages.patch
# remove failing assertions due to a symlink
# BUILD/src/github.com/grafana/grafana -> BUILD/grafana-X.Y.Z
Patch3:           003-fix-dashboard-abspath-test.patch
Patch4:           004-remove-unused-dependencies.patch
Patch5:           005-fix-gtime-test-32bit.patch
Patch6:           006-remove-unused-frontend-crypto.patch
Patch7:           007-patch-unused-backend-crypto.patch
Patch11:          011-use-hmac-sha-256-for-password-reset-tokens.patch
Patch12:          012-support-go1.18.patch
Patch13:          013-CVE-2021-23648.patch
Patch14:          014-CVE-2022-21698.patch
Patch15:          015-CVE-2022-21698.vendor.patch

BuildRequires:    git systemd golang openEuler-rpm-config 

# omit golang debugsource, see BZ995136 and related
%global           dwz_low_mem_die_limit 0
%global           _debugsource_template %{nil}
%global           GRAFANA_USER %{name}
%global           GRAFANA_GROUP %{name}
%global           GRAFANA_HOME %{_datadir}/%{name}

# grafana-server service daemon uses systemd
%{?systemd_requires}
Requires(pre):    shadow-utils

Obsoletes:        grafana-cloudwatch < 7.3.6-1
Obsoletes:        grafana-elasticsearch < 7.3.6-1
Obsoletes:        grafana-azure-monitor < 7.3.6-1
Obsoletes:        grafana-graphite < 7.3.6-1
Obsoletes:        grafana-influxdb < 7.3.6-1
Obsoletes:        grafana-loki < 7.3.6-1
Obsoletes:        grafana-mssql < 7.3.6-1
Obsoletes:        grafana-mysql < 7.3.6-1
Obsoletes:        grafana-opentsdb < 7.3.6-1
Obsoletes:        grafana-postgres < 7.3.6-1
Obsoletes:        grafana-prometheus < 7.3.6-1
Obsoletes:        grafana-stackdriver < 7.3.6-1
Provides:         grafana-cloudwatch = 7.3.6-1
Provides:         grafana-elasticsearch = 7.3.6-1
Provides:         grafana-azure-monitor = 7.3.6-1
Provides:         grafana-graphite = 7.3.6-1
Provides:         grafana-influxdb = 7.3.6-1
Provides:         grafana-loki = 7.3.6-1
Provides:         grafana-mssql = 7.3.6-1
Provides:         grafana-mysql = 7.3.6-1
Provides:         grafana-opentsdb = 7.3.6-1
Provides:         grafana-postgres = 7.3.6-1
Provides:         grafana-prometheus = 7.3.6-1
Provides:         grafana-stackdriver = 7.3.6-1

# vendored golang and node.js build dependencies
# this is for security purposes, if nodejs-foo ever needs an update,
# affected packages can be easily identified.
# Note: generated by the Makefile (see README.md)
Provides: bundled(golang(cloud.google.com/go/storage)) = 1.13.0
Provides: bundled(golang(github.com/BurntSushi/toml)) = 0.3.1
Provides: bundled(golang(github.com/VividCortex/mysqlerr)) = 0.0.0-20170204212430.6c6b55f8796f
Provides: bundled(golang(github.com/aws/aws-sdk-go)) = 1.37.20
Provides: bundled(golang(github.com/beevik/etree)) = 1.1.0
Provides: bundled(golang(github.com/benbjohnson/clock)) = 0.0.0-20161215174838.7dc76406b6d3
Provides: bundled(golang(github.com/bradfitz/gomemcache)) = 0.0.0-20190913173617.a41fca850d0b
Provides: bundled(golang(github.com/centrifugal/centrifuge)) = 0.13.0
Provides: bundled(golang(github.com/cortexproject/cortex)) = 1.4.1-0.20201022071705.85942c5703cf
Provides: bundled(golang(github.com/davecgh/go-spew)) = 1.1.1
Provides: bundled(golang(github.com/denisenkom/go-mssqldb)) = 0.0.0-20200910202707.1e08a3fab204
Provides: bundled(golang(github.com/facebookgo/inject)) = 0.0.0-20180706035515.f23751cae28b
Provides: bundled(golang(github.com/fatih/color)) = 1.10.0
Provides: bundled(golang(github.com/gchaincl/sqlhooks)) = 1.3.0
Provides: bundled(golang(github.com/getsentry/sentry-go)) = 0.10.0
Provides: bundled(golang(github.com/go-macaron/binding)) = 0.0.0-20190806013118.0b4f37bab25b
Provides: bundled(golang(github.com/go-macaron/gzip)) = 0.0.0-20160222043647.cad1c6580a07
Provides: bundled(golang(github.com/go-sourcemap/sourcemap)) = 2.1.3+incompatible
Provides: bundled(golang(github.com/go-sql-driver/mysql)) = 1.5.0
Provides: bundled(golang(github.com/go-stack/stack)) = 1.8.0
Provides: bundled(golang(github.com/gobwas/glob)) = 0.2.3
Provides: bundled(golang(github.com/golang/mock)) = 1.5.0
Provides: bundled(golang(github.com/golang/protobuf)) = 1.4.3
Provides: bundled(golang(github.com/google/go-cmp)) = 0.5.4
Provides: bundled(golang(github.com/google/uuid)) = 1.2.0
Provides: bundled(golang(github.com/gosimple/slug)) = 1.9.0
Provides: bundled(golang(github.com/grafana/grafana-aws-sdk)) = 0.4.0
Provides: bundled(golang(github.com/grafana/grafana-plugin-model)) = 0.0.0-20190930120109.1fc953a61fb4
Provides: bundled(golang(github.com/grafana/grafana-plugin-sdk-go)) = 0.88.0
Provides: bundled(golang(github.com/grafana/loki)) = 1.6.2-0.20201026154740.6978ee5d7387
Provides: bundled(golang(github.com/grpc-ecosystem/go-grpc-middleware)) = 1.2.2
Provides: bundled(golang(github.com/hashicorp/go-hclog)) = 0.15.0
Provides: bundled(golang(github.com/hashicorp/go-plugin)) = 1.4.0
Provides: bundled(golang(github.com/hashicorp/go-version)) = 1.2.1
Provides: bundled(golang(github.com/inconshreveable/log15)) = 0.0.0-20180818164646.67afb5ed74ec
Provides: bundled(golang(github.com/influxdata/influxdb-client-go/v2)) = 2.2.0
Provides: bundled(golang(github.com/jaegertracing/jaeger)) = 1.22.1-0.20210304164023.2fff3ca58910
Provides: bundled(golang(github.com/jmespath/go-jmespath)) = 0.4.0
Provides: bundled(golang(github.com/json-iterator/go)) = 1.1.10
Provides: bundled(golang(github.com/lib/pq)) = 1.9.0
Provides: bundled(golang(github.com/linkedin/goavro/v2)) = 2.10.0
Provides: bundled(golang(github.com/magefile/mage)) = 1.11.0
Provides: bundled(golang(github.com/mattn/go-isatty)) = 0.0.12
Provides: bundled(golang(github.com/mattn/go-sqlite3)) = 1.14.6
Provides: bundled(golang(github.com/mwitkow/go-conntrack)) = 0.0.0-20190716064945.2f068394615f
Provides: bundled(golang(github.com/opentracing/opentracing-go)) = 1.2.0
Provides: bundled(golang(github.com/patrickmn/go-cache)) = 2.1.0+incompatible
Provides: bundled(golang(github.com/pkg/errors)) = 0.9.1
Provides: bundled(golang(github.com/prometheus/client_golang)) = 1.9.0
Provides: bundled(golang(github.com/prometheus/client_model)) = 0.2.0
Provides: bundled(golang(github.com/prometheus/common)) = 0.18.0
Provides: bundled(golang(github.com/robfig/cron)) = 0.0.0-20180505203441.b41be1df6967
Provides: bundled(golang(github.com/robfig/cron/v3)) = 3.0.1
Provides: bundled(golang(github.com/russellhaering/goxmldsig)) = 1.1.0
Provides: bundled(golang(github.com/smartystreets/goconvey)) = 1.6.4
Provides: bundled(golang(github.com/stretchr/testify)) = 1.7.0
Provides: bundled(golang(github.com/teris-io/shortid)) = 0.0.0-20171029131806.771a37caa5cf
Provides: bundled(golang(github.com/timberio/go-datemath)) = 0.1.1-0.20200323150745.74ddef604fff
Provides: bundled(golang(github.com/ua-parser/uap-go)) = 0.0.0-20190826212731.daf92ba38329
Provides: bundled(golang(github.com/uber/jaeger-client-go)) = 2.25.0+incompatible
Provides: bundled(golang(github.com/unknwon/com)) = 1.0.1
Provides: bundled(golang(github.com/urfave/cli/v2)) = 2.3.0
Provides: bundled(golang(github.com/weaveworks/common)) = 0.0.0-20201119133501.0619918236ec
Provides: bundled(golang(github.com/xorcare/pointer)) = 1.1.0
Provides: bundled(golang(github.com/yudai/gojsondiff)) = 1.0.0
Provides: bundled(golang(go.opentelemetry.io/collector)) = 0.21.0
Provides: bundled(golang(golang.org/x/crypto)) = 0.0.0-20201221181555.eec23a3978ad
Provides: bundled(golang(golang.org/x/net)) = 0.0.0-20210119194325.5f4716e94777
Provides: bundled(golang(golang.org/x/oauth2)) = 0.0.0-20210113205817.d3ed898aa8a3
Provides: bundled(golang(golang.org/x/sync)) = 0.0.0-20201207232520.09787c993a3a
Provides: bundled(golang(golang.org/x/time)) = 0.0.0-20200630173020.3af7569d3a1e
Provides: bundled(golang(gonum.org/v1/gonum)) = 0.8.2
Provides: bundled(golang(google.golang.org/api)) = 0.40.0
Provides: bundled(golang(google.golang.org/grpc)) = 1.36.0
Provides: bundled(golang(gopkg.in/ini.v1)) = 1.62.0
Provides: bundled(golang(gopkg.in/ldap.v3)) = 3.0.2
Provides: bundled(golang(gopkg.in/macaron.v1)) = 1.4.0
Provides: bundled(golang(gopkg.in/mail.v2)) = 2.3.1
Provides: bundled(golang(gopkg.in/redis.v5)) = 5.2.9
Provides: bundled(golang(gopkg.in/square/go-jose.v2)) = 2.5.1
Provides: bundled(golang(gopkg.in/yaml.v2)) = 2.4.0
Provides: bundled(golang(xorm.io/core)) = 0.7.3
Provides: bundled(golang(xorm.io/xorm)) = 0.8.2
Provides: bundled(npm(@babel/core)) = 7.6.4
Provides: bundled(npm(@babel/plugin-proposal-nullish-coalescing-operator)) = 7.8.3
Provides: bundled(npm(@babel/plugin-proposal-optional-chaining)) = 7.8.3
Provides: bundled(npm(@babel/plugin-syntax-dynamic-import)) = 7.7.4
Provides: bundled(npm(@babel/preset-env)) = 7.7.4
Provides: bundled(npm(@babel/preset-react)) = 7.8.3
Provides: bundled(npm(@babel/preset-typescript)) = 7.8.3
Provides: bundled(npm(@emotion/core)) = 10.0.21
Provides: bundled(npm(@grafana/api-documenter)) = 7.11.2
Provides: bundled(npm(@grafana/api-extractor)) = 7.10.1
Provides: bundled(npm(@grafana/aws-sdk)) = 0.0.3
Provides: bundled(npm(@grafana/eslint-config)) = 2.3.0
Provides: bundled(npm(@grafana/slate-react)) = 0.22.9-grafana
Provides: bundled(npm(@popperjs/core)) = 2.5.4
Provides: bundled(npm(@reduxjs/toolkit)) = 1.5.0
Provides: bundled(npm(@rtsao/plugin-proposal-class-properties)) = 7.0.1-patch.1
Provides: bundled(npm(@sentry/browser)) = 5.25.0
Provides: bundled(npm(@sentry/types)) = 5.24.2
Provides: bundled(npm(@sentry/utils)) = 5.24.2
Provides: bundled(npm(@testing-library/jest-dom)) = 5.11.5
Provides: bundled(npm(@testing-library/react)) = 11.1.2
Provides: bundled(npm(@testing-library/react-hooks)) = 3.2.1
Provides: bundled(npm(@testing-library/user-event)) = 12.1.3
Provides: bundled(npm(@torkelo/react-select)) = 3.0.8
Provides: bundled(npm(@types/angular)) = 1.6.56
Provides: bundled(npm(@types/angular-route)) = 1.7.0
Provides: bundled(npm(@types/antlr4)) = 4.7.1
Provides: bundled(npm(@types/braintree__sanitize-url)) = 4.0.0
Provides: bundled(npm(@types/classnames)) = 2.2.7
Provides: bundled(npm(@types/clipboard)) = 2.0.1
Provides: bundled(npm(@types/common-tags)) = 1.8.0
Provides: bundled(npm(@types/d3)) = 5.7.2
Provides: bundled(npm(@types/d3-force)) = 1.2.1
Provides: bundled(npm(@types/d3-scale-chromatic)) = 1.3.1
Provides: bundled(npm(@types/debounce-promise)) = 3.1.3
Provides: bundled(npm(@types/enzyme)) = 3.10.3
Provides: bundled(npm(@types/enzyme-adapter-react-16)) = 1.0.6
Provides: bundled(npm(@types/file-saver)) = 2.0.1
Provides: bundled(npm(@types/hoist-non-react-statics)) = 3.3.1
Provides: bundled(npm(@types/is-hotkey)) = 0.1.1
Provides: bundled(npm(@types/jest)) = 26.0.12
Provides: bundled(npm(@types/jquery)) = 3.3.38
Provides: bundled(npm(@types/jsurl)) = 1.2.28
Provides: bundled(npm(@types/lodash)) = 4.14.123
Provides: bundled(npm(@types/lru-cache)) = 5.1.0
Provides: bundled(npm(@types/md5)) = 2.1.33
Provides: bundled(npm(@types/moment-timezone)) = 0.5.13
Provides: bundled(npm(@types/mousetrap)) = 1.6.3
Provides: bundled(npm(@types/node)) = 10.14.1
Provides: bundled(npm(@types/papaparse)) = 5.2.0
Provides: bundled(npm(@types/prismjs)) = 1.16.0
Provides: bundled(npm(@types/react)) = 16.9.9
Provides: bundled(npm(@types/react-beautiful-dnd)) = 12.1.2
Provides: bundled(npm(@types/react-dom)) = 16.9.2
Provides: bundled(npm(@types/react-grid-layout)) = 1.1.1
Provides: bundled(npm(@types/react-loadable)) = 5.5.2
Provides: bundled(npm(@types/react-redux)) = 7.1.7
Provides: bundled(npm(@types/react-select)) = 3.0.8
Provides: bundled(npm(@types/react-test-renderer)) = 16.9.1
Provides: bundled(npm(@types/react-transition-group)) = 4.2.3
Provides: bundled(npm(@types/react-virtualized-auto-sizer)) = 1.0.0
Provides: bundled(npm(@types/react-window)) = 1.8.1
Provides: bundled(npm(@types/redux-logger)) = 3.0.7
Provides: bundled(npm(@types/redux-mock-store)) = 1.0.2
Provides: bundled(npm(@types/reselect)) = 2.2.0
Provides: bundled(npm(@types/slate)) = 0.47.1
Provides: bundled(npm(@types/slate-plain-serializer)) = 0.6.1
Provides: bundled(npm(@types/slate-react)) = 0.22.5
Provides: bundled(npm(@types/testing-library__jest-dom)) = 5.9.5
Provides: bundled(npm(@types/testing-library__react-hooks)) = 3.1.0
Provides: bundled(npm(@types/tinycolor2)) = 1.4.1
Provides: bundled(npm(@types/uuid)) = 8.3.0
Provides: bundled(npm(@typescript-eslint/eslint-plugin)) = 4.15.0
Provides: bundled(npm(@typescript-eslint/parser)) = 4.15.0
Provides: bundled(npm(@welldone-software/why-did-you-render)) = 4.0.6
Provides: bundled(npm(@wojtekmaj/enzyme-adapter-react-17)) = 0.3.1
Provides: bundled(npm(abortcontroller-polyfill)) = 1.4.0
Provides: bundled(npm(angular)) = 1.8.2
Provides: bundled(npm(angular-bindonce)) = 0.3.1
Provides: bundled(npm(angular-mocks)) = 1.6.6
Provides: bundled(npm(angular-route)) = 1.8.2
Provides: bundled(npm(angular-sanitize)) = 1.8.2
Provides: bundled(npm(antlr4)) = 4.8.0
Provides: bundled(npm(autoprefixer)) = 9.7.4
Provides: bundled(npm(axios)) = 0.21.1
Provides: bundled(npm(babel-core)) = 7.0.0-bridge.0
Provides: bundled(npm(babel-jest)) = 26.6.3
Provides: bundled(npm(babel-loader)) = 8.0.6
Provides: bundled(npm(babel-plugin-angularjs-annotate)) = 0.10.0
Provides: bundled(npm(baron)) = 3.0.3
Provides: bundled(npm(brace)) = 0.11.1
Provides: bundled(npm(calculate-size)) = 1.1.1
Provides: bundled(npm(centrifuge)) = 2.6.4
Provides: bundled(npm(classnames)) = 2.2.6
Provides: bundled(npm(clean-webpack-plugin)) = 3.0.0
Provides: bundled(npm(clipboard)) = 2.0.4
Provides: bundled(npm(common-tags)) = 1.8.0
Provides: bundled(npm(core-js)) = 1.2.7
Provides: bundled(npm(css-loader)) = 3.4.2
Provides: bundled(npm(d3)) = 5.15.0
Provides: bundled(npm(d3-force)) = 1.2.1
Provides: bundled(npm(d3-scale-chromatic)) = 1.5.0
Provides: bundled(npm(dangerously-set-html-content)) = 1.0.6
Provides: bundled(npm(debounce-promise)) = 3.1.2
Provides: bundled(npm(emotion)) = 10.0.27
Provides: bundled(npm(enzyme)) = 3.11.0
Provides: bundled(npm(enzyme-to-json)) = 3.4.4
Provides: bundled(npm(es-abstract)) = 1.18.0-next.1
Provides: bundled(npm(es6-promise)) = 4.2.8
Provides: bundled(npm(es6-shim)) = 0.35.5
Provides: bundled(npm(eslint)) = 2.13.1
Provides: bundled(npm(eslint-config-prettier)) = 7.2.0
Provides: bundled(npm(eslint-plugin-jsdoc)) = 31.6.1
Provides: bundled(npm(eslint-plugin-no-only-tests)) = 2.4.0
Provides: bundled(npm(eslint-plugin-prettier)) = 3.3.1
Provides: bundled(npm(eslint-plugin-react)) = 7.22.0
Provides: bundled(npm(eslint-plugin-react-hooks)) = 4.2.0
Provides: bundled(npm(eventemitter3)) = 3.1.2
Provides: bundled(npm(expect.js)) = 0.3.1
Provides: bundled(npm(expose-loader)) = 0.7.5
Provides: bundled(npm(fast-text-encoding)) = 1.0.0
Provides: bundled(npm(file-loader)) = 5.0.2
Provides: bundled(npm(file-saver)) = 2.0.2
Provides: bundled(npm(fork-ts-checker-webpack-plugin)) = 1.0.0
Provides: bundled(npm(gaze)) = 1.1.3
Provides: bundled(npm(glob)) = 7.1.3
Provides: bundled(npm(hoist-non-react-statics)) = 2.5.5
Provides: bundled(npm(html-loader)) = 0.5.5
Provides: bundled(npm(html-webpack-harddisk-plugin)) = 1.0.1
Provides: bundled(npm(html-webpack-plugin)) = 3.2.0
Provides: bundled(npm(husky)) = 4.2.1
Provides: bundled(npm(immutable)) = 3.8.2
Provides: bundled(npm(is-hotkey)) = 0.1.4
Provides: bundled(npm(jest)) = 26.6.3
Provides: bundled(npm(jest-canvas-mock)) = 2.3.0
Provides: bundled(npm(jest-date-mock)) = 1.0.8
Provides: bundled(npm(jest-matcher-utils)) = 26.0.0
Provides: bundled(npm(jquery)) = 3.5.1
Provides: bundled(npm(jsurl)) = 0.1.5
Provides: bundled(npm(lerna)) = 3.22.1
Provides: bundled(npm(lint-staged)) = 10.0.7
Provides: bundled(npm(load-grunt-tasks)) = 5.1.0
Provides: bundled(npm(lodash)) = 4.17.21
Provides: bundled(npm(lru-cache)) = 4.1.5
Provides: bundled(npm(md5)) = 2.2.1
Provides: bundled(npm(memoize-one)) = 4.1.0
Provides: bundled(npm(mini-css-extract-plugin)) = 0.7.0
Provides: bundled(npm(mocha)) = 7.0.1
Provides: bundled(npm(module-alias)) = 2.2.2
Provides: bundled(npm(moment)) = 2.24.0
Provides: bundled(npm(moment-timezone)) = 0.5.28
Provides: bundled(npm(monaco-editor)) = 0.20.0
Provides: bundled(npm(monaco-editor-webpack-plugin)) = 1.9.0
Provides: bundled(npm(mousetrap)) = 1.6.5
Provides: bundled(npm(mousetrap-global-bind)) = 1.1.0
Provides: bundled(npm(mutationobserver-shim)) = 0.3.3
Provides: bundled(npm(ngtemplate-loader)) = 2.0.1
Provides: bundled(npm(nodemon)) = 2.0.2
Provides: bundled(npm(optimize-css-assets-webpack-plugin)) = 5.0.4
Provides: bundled(npm(papaparse)) = 5.3.0
Provides: bundled(npm(postcss-browser-reporter)) = 0.6.0
Provides: bundled(npm(postcss-loader)) = 3.0.0
Provides: bundled(npm(postcss-reporter)) = 6.0.1
Provides: bundled(npm(prettier)) = 2.0.5
Provides: bundled(npm(prismjs)) = 1.21.0
Provides: bundled(npm(prop-types)) = 15.7.2
Provides: bundled(npm(rc-cascader)) = 1.0.1
Provides: bundled(npm(re-resizable)) = 6.2.0
Provides: bundled(npm(react)) = 16.13.1
Provides: bundled(npm(react-beautiful-dnd)) = 13.0.0
Provides: bundled(npm(react-dom)) = 17.0.1
Provides: bundled(npm(react-grid-layout)) = 1.2.0
Provides: bundled(npm(react-highlight-words)) = 0.16.0
Provides: bundled(npm(react-hot-loader)) = 4.8.0
Provides: bundled(npm(react-loadable)) = 5.5.0
Provides: bundled(npm(react-popper)) = 2.2.4
Provides: bundled(npm(react-redux)) = 7.2.0
Provides: bundled(npm(react-reverse-portal)) = 2.0.1
Provides: bundled(npm(react-select-event)) = 5.1.0
Provides: bundled(npm(react-sizeme)) = 2.6.12
Provides: bundled(npm(react-split-pane)) = 0.1.89
Provides: bundled(npm(react-test-renderer)) = 16.10.2
Provides: bundled(npm(react-transition-group)) = 4.3.0
Provides: bundled(npm(react-use)) = 13.27.0
Provides: bundled(npm(react-virtualized-auto-sizer)) = 1.0.2
Provides: bundled(npm(react-window)) = 1.8.5
Provides: bundled(npm(redux)) = 3.7.2
Provides: bundled(npm(redux-logger)) = 3.0.6
Provides: bundled(npm(redux-mock-store)) = 1.5.4
Provides: bundled(npm(redux-thunk)) = 2.3.0
Provides: bundled(npm(regenerator-runtime)) = 0.11.1
Provides: bundled(npm(regexp-replace-loader)) = 1.0.1
Provides: bundled(npm(reselect)) = 4.0.0
Provides: bundled(npm(rimraf)) = 2.6.3
Provides: bundled(npm(rst2html)) = 1.0.4
Provides: bundled(npm(rxjs)) = 6.5.5
Provides: bundled(npm(rxjs-spy)) = 7.5.1
Provides: bundled(npm(sass)) = 1.27.0
Provides: bundled(npm(sass-lint)) = 1.12.1
Provides: bundled(npm(sass-loader)) = 8.0.2
Provides: bundled(npm(search-query-parser)) = 1.5.4
Provides: bundled(npm(sinon)) = 8.1.1
Provides: bundled(npm(slate)) = 0.47.8
Provides: bundled(npm(slate-plain-serializer)) = 0.7.10
Provides: bundled(npm(style-loader)) = 1.1.3
Provides: bundled(npm(terser-webpack-plugin)) = 1.4.5
Provides: bundled(npm(tether)) = 1.4.7
Provides: bundled(npm(tether-drop)) = 1.5.0
Provides: bundled(npm(tinycolor2)) = 1.4.1
Provides: bundled(npm(ts-jest)) = 26.4.4
Provides: bundled(npm(ts-node)) = 9.0.0
Provides: bundled(npm(tslib)) = 1.10.0
Provides: bundled(npm(tti-polyfill)) = 0.2.2
Provides: bundled(npm(typescript)) = 3.9.7
Provides: bundled(npm(uuid)) = 3.3.3
Provides: bundled(npm(visjs-network)) = 4.25.0
Provides: bundled(npm(webpack)) = 4.41.5
Provides: bundled(npm(webpack-bundle-analyzer)) = 3.6.0
Provides: bundled(npm(webpack-cleanup-plugin)) = 0.5.1
Provides: bundled(npm(webpack-cli)) = 3.3.10
Provides: bundled(npm(webpack-dev-server)) = 3.11.1
Provides: bundled(npm(webpack-merge)) = 4.2.2
Provides: bundled(npm(whatwg-fetch)) = 3.0.0
Provides: bundled(npm(zone.js)) = 0.7.8

%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.

%prep
%setup -q -T -D -b 0
%setup -q -T -D -b 1
rm -r plugins-bundled
%setup -q -T -D -b 2

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

# Set up build subdirs and links
mkdir -p %{_builddir}/src/github.com/grafana
ln -s %{_builddir}/%{name}-%{version} \
    %{_builddir}/src/github.com/grafana/grafana

%build
# Build the backend
cd %{_builddir}/src/github.com/grafana/grafana
export GOPATH=%{_builddir}

# see grafana-X.X.X/build.go
export LDFLAGS="-X main.version=%{version} -X main.buildstamp=${SOURCE_DATE_EPOCH}"
for cmd in grafana-cli grafana-server; do
    %gobuild -o %{_builddir}/bin/${cmd} ./pkg/cmd/${cmd}
done

%install
# dirs, shared files, public html, webpack
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_libexecdir}/%{name}
cp -a conf public plugins-bundled %{buildroot}%{_datadir}/%{name}

# wrappers
install -p -m 755 packaging/wrappers/grafana-cli %{buildroot}%{_sbindir}/%{name}-cli

# binaries
install -p -m 755 %{_builddir}/bin/%{name}-server %{buildroot}%{_sbindir}
install -p -m 755 %{_builddir}/bin/%{name}-cli %{buildroot}%{_libexecdir}/%{name}

# man pages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 docs/man/man1/* %{buildroot}%{_mandir}/man1

# config dirs
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/dashboards
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/datasources
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/notifiers
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/plugins
install -d %{buildroot}%{_sysconfdir}/sysconfig

# config defaults
install -p -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/grafana.ini
install -p -m 640 conf/ldap.toml %{buildroot}%{_sysconfdir}/%{name}/ldap.toml
install -p -m 644 %{SOURCE3} %{buildroot}%{_datadir}/%{name}/conf/defaults.ini
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
# Test backend
cd %{_builddir}/src/github.com/grafana/grafana
export GOPATH=%{_builddir}

# in setting_test.go there is a unit test which checks if 10 days are 240 hours
# which is usually true except if the dayligt saving time change falls into the last 10 days, then it's either 239 or 241 hours...
# let's set the time zone to a time zone without daylight saving time
export TZ=GMT
rm -r pkg/macaron

%gotest ./pkg/...

%files
# binaries and wrappers
%{_sbindir}/%{name}-server
%{_sbindir}/%{name}-cli
%{_libexecdir}/%{name}

# config files
%config(noreplace) %{_sysconfdir}/sysconfig/grafana-server
%dir %{_sysconfdir}/%{name}
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/dashboards
%attr(0750, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/datasources
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/notifiers
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/plugins
%attr(0640, root, %{GRAFANA_GROUP}) %config(noreplace) %{_sysconfdir}/%{name}/grafana.ini
%attr(0640, root, %{GRAFANA_GROUP}) %config(noreplace) %{_sysconfdir}/%{name}/ldap.toml

# config database directory and plugins
%attr(0750, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}
%attr(-,    %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}/plugins

# shared directory and all files therein
%{_datadir}/%{name}
%attr(-, root, %{GRAFANA_GROUP}) %{_datadir}/%{name}/conf/*

# systemd service file
%{_unitdir}/grafana-server.service

# Grafana configuration to dynamically create /run/grafana/grafana.pid on tmpfs
%{_tmpfilesdir}/%{name}.conf

# log directory - grafana.log is created by grafana-server, and it does it's own log rotation
%attr(0755, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_localstatedir}/log/%{name}

# man pages for grafana binaries
%{_mandir}/man1/%{name}-server.1*
%{_mandir}/man1/%{name}-cli.1*

# other docs and license
%license LICENSE
%doc CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md GOVERNANCE.md ISSUE_TRIAGE.md MAINTAINERS.md NOTICE.md
%doc PLUGIN_DEV.md README.md ROADMAP.md SECURITY.md SUPPORT.md UPGRADING_DEPENDENCIES.md WORKFLOW.md


%changelog
* Fri May 6 2022 yaoxin <yaoxin30@h-partners.com> - 7.5.15-1
- Update to 7.5.15 for fix CVE-2022-21703,CVE-2022-21713

* Thu Mar 17 2022 yaoxin <yaoxin30@huawei.com> - 7.5.11-4
- Fix CVE-2022-21702

* Thu Jan 27 2022 wangkai <wangkai385@huawei.com> 7.5.11-3
- Fix CVE-2022-21673

* Wed Dec 15 2021 wangkai <wangkai385@huawei.com> 7.5.11-2
- Fix CVE-2021-43813

* Wed Nov 17 2021 wangkai <wangkai385@huawei.com> 7.5.11-1
- Upgrade to 7.5.11 for fix CVE-2021-39226

* Fri Sep 3 2021 Python_Bot <Python_Bot@openeuler.org> 7.3.6-1
- Update to version 7.3.6

* Tue Aug 11 2020 houjian <houjian@kylinos.cn> - 6.7.4-1
- Package init
