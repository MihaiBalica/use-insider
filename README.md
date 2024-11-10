# use-insider

## Test Case controller

The automated tests are executed in a test-case-controller container. The test-case-controller container is a 
Docker container that is based on image defined in the Dockerfile.testcase-controller in docker directory. 
The test-case-controller pod is started by the test-case-controller job in the `testcase-controller-job.yaml` file 
in k8s/ directory. Given that the test-case-controller is a job, it will run to completion and then exit, which is more
appropriate in behavior then the behavior of a pod.

The automated tests are using the pytest framework and remote selenium grid and chrome node. Chrome node can be scaled up
and the only limit is the HW resources. The test-case-controller can use the selenium grid to run the tests in parallel
on many chrome nodes.

#### script to build the test-case-controller image (build.sh)
```shell
#!/bin/bash
set -e

# Build testcase-controller image
if ! docker buildx build --platform "linux/amd64" -t balicamihai/testcase-controller:amd64-7 -f docker/Dockerfile.testcase-controller . --push; then
  echo "Failed to build testcase-controller image"
  exit 1
fi
```

### Test Case Controller Execution log 
This is executing the regression tests it finds, those annotated as regression. In this case there is only one test case
in `open_position_application_form_test.py` file. The test case is annotated with `@pytest.mark.regression`.
```shell
kubectl logs -f testcase-controller-pkjlc
============================= test session starts ==============================
platform linux -- Python 3.12.7, pytest-8.3.3, pluggy-1.5.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
rootdir: /app
configfile: pytest.ini
collecting ... collected 1 item

tests/open_position_application_form_test.py::test_open_position_application_form PASSED

============================== 1 passed in 38.74s ==============================
```

### Existing pods during test case controller execution
```shell
kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
chrome-node-688c98b864-7m6rn      1/1     Running   0          76s
otel-collector-64dfb476fd-tsfg8   1/1     Running   0          3h34m
selenium-hub-5f64c8c79d-z5xt2     1/1     Running   0          31m
testcase-controller-pkjlc         1/1     Running   0          16s
```

### Existing jobs after test case controller execution
```shell
kubectl get pods
NAME                              READY   STATUS      RESTARTS   AGE
chrome-node-688c98b864-7m6rn      1/1     Running     0          38m
otel-collector-64dfb476fd-tsfg8   1/1     Running     0          4h11m
selenium-hub-5f64c8c79d-z5xt2     1/1     Running     0          169m
testcase-controller-pkjlc         0/1     Completed   0          37m
```

### Various logs
#### docker build logs
```shell
$ bash build.sh 
[+] Building 46.0s (12/12) FINISHED                                                                                                                                                                                                                                        docker:default
 => [internal] load build definition from Dockerfile.testcase-controller                                                                                                                                                                                                             0.0s
 => => transferring dockerfile: 365B                                                                                                                                                                                                                                                 0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim-bullseye                                                                                                                                                                                                         1.0s
 => [auth] library/python:pull token for registry-1.docker.io                                                                                                                                                                                                                        0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                                                                    0.0s
 => => transferring context: 2B                                                                                                                                                                                                                                                      0.0s
 => [1/5] FROM docker.io/library/python:3.12-slim-bullseye@sha256:3207ac8a818335cc1c045ce5bcc3b1adf345ee80049d7734151489c66fc64414                                                                                                                                                   0.0s
 => [internal] load build context                                                                                                                                                                                                                                                    0.0s
 => => transferring context: 31.94kB                                                                                                                                                                                                                                                 0.0s
 => CACHED [2/5] WORKDIR /app                                                                                                                                                                                                                                                        0.0s
 => [3/5] COPY . /app                                                                                                                                                                                                                                                                0.1s
 => [4/5] RUN apt-get update && apt-get install -y     libx11-dev     libgdk-pixbuf2.0-0     && rm -rf /var/lib/apt/lists/*                                                                                                                                                         20.9s
 => [5/5] RUN pip install --no-cache-dir -r requirements.txt                                                                                                                                                                                                                        10.2s 
 => exporting to image                                                                                                                                                                                                                                                               0.3s 
 => => exporting layers                                                                                                                                                                                                                                                              0.3s 
 => => writing image sha256:09e8f128d698b526275f7eceaf0707ef99f87b0e9331271840d8333dd7d30dca                                                                                                                                                                                         0.0s 
 => => naming to docker.io/balicamihai/testcase-controller:amd64-7                                                                                                                                                                                                                   0.0s 
 => pushing balicamihai/testcase-controller:amd64-7 with docker                                                                                                                                                                                                                     11.0s 
 => => pushing layer c54855f443e1                                                                                                                                                                                                                                                    7.4s 
 => => pushing layer b3786cee971f                                                                                                                                                                                                                                                    6.9s
 => => pushing layer bd758b781295                                                                                                                                                                                                                                                    4.0s
 => => pushing layer 3a7f8482d57d                                                                                                                                                                                                                                                   10.6s
 => => pushing layer 5fc7a46f2b35                                                                                                                                                                                                                                                   10.6s
 => => pushing layer 509b6bb5437f                                                                                                                                                                                                                                                   10.6s
 => => pushing layer 13d5624ddcbd                                                                                                                                                                                                                                                   10.6s
 => => pushing layer ceffe60ed721                                                                                                                                                                                                                                                   10.6s
```

### Chrome node logs
```shell
Starting Selenium Grid Node...
2024-11-10 14:56:49,995 INFO success: xvfb entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
2024-11-10 14:56:49,995 INFO success: vnc entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
2024-11-10 14:56:49,995 INFO success: novnc entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
Nov 10, 2024 2:56:50 PM org.openqa.selenium.grid.config.TomlConfig <init>
WARNING: Please use quotes to denote strings. Upcoming TOML parser will require this and unquoted strings will throw an error in the future
14:56:50.159 INFO [LoggingOptions.configureLogEncoding] - Using the system default encoding
14:56:50.164 INFO [OpenTelemetryTracer.createTracer] - Using OpenTelemetry for tracing
14:56:50.569 INFO [UnboundZmqEventBus.<init>] - Connecting to tcp://selenium-hub-service:4442 and tcp://selenium-hub-service:4443
14:56:50.660 INFO [UnboundZmqEventBus.<init>] - Sockets created
14:56:51.662 INFO [UnboundZmqEventBus.<init>] - Event bus ready
14:56:51.810 INFO [NodeServer.createHandlers] - Reporting self as: http://10.1.138.95:5555
14:56:51.833 INFO [NodeOptions.getSessionFactories] - Detected 2 available processors
14:56:51.920 INFO [NodeOptions.report] - Adding chrome for {"browserName": "chrome","browserVersion": "130.0","goog:chromeOptions": {"binary": "\u002fusr\u002fbin\u002fgoogle-chrome"},"platformName": "linux","se:containerName": "","se:noVncPort": 7900,"se:vncEnabled": true} 1 times
14:56:51.951 INFO [Node.<init>] - Binding additional locator mechanisms: relative
14:56:52.182 INFO [NodeServer$1.start] - Starting registration process for Node http://10.1.138.95:5555
14:56:52.183 INFO [NodeServer.execute] - Started Selenium node 4.26.0 (revision 69f9e5e): http://10.1.138.95:5555
14:56:52.197 INFO [NodeServer$1.lambda$start$1] - Sending registration event...
14:56:52.370 INFO [NodeServer.lambda$createHandlers$2] - Node has been added
14:57:26.547 INFO [LocalNode.newSession] - Session created by the Node. Id: 731dd54c8c71910e49f567b71c04b3ba, Caps: Capabilities {acceptInsecureCerts: false, browserName: chrome, browserVersion: 130.0.6723.91, chrome: {chromedriverVersion: 130.0.6723.91 (53ac07678369..., userDataDir: /tmp/.org.chromium.Chromium...}, fedcm:accounts: true, goog:chromeOptions: {debuggerAddress: localhost:42891}, networkConnectionEnabled: false, pageLoadStrategy: normal, platformName: linux, proxy: Proxy(), se:bidiEnabled: false, se:cdp: ws://selenium-hub-service:4..., se:cdpVersion: 130.0.6723.91, se:containerName: , se:noVncPort: 7900, se:vnc: ws://selenium-hub-service:4..., se:vncEnabled: true, se:vncLocalAddress: ws://10.1.138.95:7900, setWindowRect: true, strictFileInteractability: false, timeouts: {implicit: 0, pageLoad: 300000, script: 30000}, unhandledPromptBehavior: dismiss and notify, webauthn:extension:credBlob: true, webauthn:extension:largeBlob: true, webauthn:extension:minPinLength: true, webauthn:extension:prf: true, webauthn:virtualAuthenticators: true}
14:58:04.495 INFO [SessionSlot.stop] - Stopping session 731dd54c8c71910e49f567b71c04b3ba
```

### Selenium hub logs  -- only relevant part
```shell
kubectl logs selenium-hub-5f64c8c79d-z5xt2
2024-11-10 12:45:58,299 INFO Included extra file "/etc/supervisor/conf.d/selenium-grid-hub.conf" during parsing
2024-11-10 12:45:58,304 INFO RPC interface 'supervisor' initialized
2024-11-10 12:45:58,304 INFO supervisord started with pid 8
2024-11-10 12:45:59,306 INFO spawned: 'selenium-grid-hub' with pid 9
Starting Selenium Grid Hub...
2024-11-10 12:45:59,312 INFO success: selenium-grid-hub entered RUNNING state, process has stayed up for > than 0 seconds (startsecs)
Appending Selenium option: --log-level INFO
Appending Selenium option: --http-logs false
Appending Selenium option: --structured-logs false
Appending Selenium option: --reject-unsupported-caps false
Appending Selenium option: --session-request-timeout 300
Appending Selenium option: --session-retry-interval 15
Appending Selenium option: --healthcheck-interval 120
Appending Selenium option: --relax-checks true
Appending Selenium option: --bind-host false
Appending Selenium option: --config /opt/selenium/config.toml
Tracing is enabled
Classpath will be enriched with these external jars :  --ext /external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-exporter-otlp/1.43.0/opentelemetry-exporter-otlp-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/io/grpc/grpc-netty/1.68.0/grpc-netty-1.68.0.jar:/external_jars/https/repo1.maven.org/maven2/io/netty/netty-codec-http/4.1.114.Final/netty-codec-http-4.1.114.Final.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-sdk-trace/1.43.0/opentelemetry-sdk-trace-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-sdk-metrics/1.43.0/opentelemetry-sdk-metrics-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-sdk-logs/1.43.0/opentelemetry-sdk-logs-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-exporter-otlp-common/1.43.0/opentelemetry-exporter-otlp-common-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-exporter-sender-okhttp/1.43.0/opentelemetry-exporter-sender-okhttp-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-sdk-extension-autoconfigure-spi/1.43.0/opentelemetry-sdk-extension-autoconfigure-spi-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/io/grpc/grpc-api/1.68.0/grpc-api-1.68.0.jar:/external_jars/https/repo1.maven.org/maven2/io/netty/netty-codec-http2/4.1.110.Final/netty-codec-http2-4.1.110.Final.jar:/external_jars/https/repo1.maven.org/maven2/io/grpc/grpc-core/1.68.0/grpc-core-1.68.0.jar:/external_jars/https/repo1.maven.org/maven2/io/netty/netty-handler-proxy/4.1.110.Final/netty-handler-proxy-4.1.110.Final.jar:/external_jars/https/repo1.maven.org/maven2/com/google/guava/guava/33.2.1-android/guava-33.2.1-android.jar:/external_jars/https/repo1.maven.org/maven2/com/google/errorprone/error_prone_annotations/2.28.0/error_prone_annotations-2.28.0.jar:/external_jars/https/repo1.maven.org/maven2/io/perfmark/perfmark-api/0.27.0/perfmark-api-0.27.0.jar:/external_jars/https/repo1.maven.org/maven2/io/netty/netty-transport-native-unix-common/4.1.114.Final/netty-transport-native-unix-common-4.1.114.Final.jar:/external_jars/https/repo1.maven.org/maven2/io/grpc/grpc-util/1.68.0/grpc-util-1.68.0.jar:/external_jars/https/repo1.maven.org/maven2/io/netty/netty-common/4.1.114.Final/netty-common-4.1.114.Final.jar:/external_jars/https/repo1.maven.org/maven2/io/netty/netty-buffer/4.1.114.Final/netty-buffer-4.1.114.Final.jar:/external_jars/https/repo1.maven.org/maven2/io/netty/netty-transport/4.1.114.Final/netty-transport-4.1.114.Final.jar:/external_jars/https/repo1.maven.org/maven2/io/netty/netty-codec/4.1.114.Final/netty-codec-4.1.114.Final.jar:/external_jars/https/repo1.maven.org/maven2/io/netty/netty-handler/4.1.114.Final/netty-handler-4.1.114.Final.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-api/1.43.0/opentelemetry-api-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-sdk-common/1.43.0/opentelemetry-sdk-common-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-api-incubator/1.43.0-alpha/opentelemetry-api-incubator-1.43.0-alpha.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-exporter-common/1.43.0/opentelemetry-exporter-common-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/com/squareup/okhttp3/okhttp/4.12.0/okhttp-4.12.0.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-sdk/1.43.0/opentelemetry-sdk-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/com/google/code/findbugs/jsr305/3.0.2/jsr305-3.0.2.jar:/external_jars/https/repo1.maven.org/maven2/com/google/code/gson/gson/2.11.0/gson-2.11.0.jar:/external_jars/https/repo1.maven.org/maven2/com/google/android/annotations/4.1.1.4/annotations-4.1.1.4.jar:/external_jars/https/repo1.maven.org/maven2/org/codehaus/mojo/animal-sniffer-annotations/1.24/animal-sniffer-annotations-1.24.jar:/external_jars/https/repo1.maven.org/maven2/io/grpc/grpc-context/1.68.0/grpc-context-1.68.0.jar:/external_jars/https/repo1.maven.org/maven2/io/netty/netty-codec-socks/4.1.110.Final/netty-codec-socks-4.1.110.Final.jar:/external_jars/https/repo1.maven.org/maven2/com/google/guava/failureaccess/1.0.2/failureaccess-1.0.2.jar:/external_jars/https/repo1.maven.org/maven2/com/google/guava/listenablefuture/9999.0-empty-to-avoid-conflict-with-guava/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar:/external_jars/https/repo1.maven.org/maven2/org/checkerframework/checker-qual/3.42.0/checker-qual-3.42.0.jar:/external_jars/https/repo1.maven.org/maven2/com/google/j2objc/j2objc-annotations/3.0.0/j2objc-annotations-3.0.0.jar:/external_jars/https/repo1.maven.org/maven2/io/netty/netty-resolver/4.1.114.Final/netty-resolver-4.1.114.Final.jar:/external_jars/https/repo1.maven.org/maven2/io/opentelemetry/opentelemetry-context/1.43.0/opentelemetry-context-1.43.0.jar:/external_jars/https/repo1.maven.org/maven2/com/squareup/okio/okio/3.6.0/okio-3.6.0.jar:/external_jars/https/repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib-jdk8/1.9.10/kotlin-stdlib-jdk8-1.9.10.jar:/external_jars/https/repo1.maven.org/maven2/com/squareup/okio/okio-jvm/3.6.0/okio-jvm-3.6.0.jar:/external_jars/https/repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/1.9.10/kotlin-stdlib-1.9.10.jar:/external_jars/https/repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib-jdk7/1.9.10/kotlin-stdlib-jdk7-1.9.10.jar:/external_jars/https/repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib-common/1.9.10/kotlin-stdlib-common-1.9.10.jar:/external_jars/https/repo1.maven.org/maven2/org/jetbrains/annotations/13.0/annotations-13.0.jar
List arguments for OpenTelemetry:  -Dotel.resource.attributes=service.name=selenium-hub -Dotel.traces.exporter=otlp -Dotel.java.global-autoconfigure.enabled=true
Nov 10, 2024 12:45:59 PM org.openqa.selenium.grid.config.TomlConfig <init>
WARNING: Please use quotes to denote strings. Upcoming TOML parser will require this and unquoted strings will throw an error in the future
12:45:59.878 INFO [LoggingOptions.configureLogEncoding] - Using the system default encoding
12:45:59.883 INFO [OpenTelemetryTracer.createTracer] - Using OpenTelemetry for tracing
12:46:00.212 INFO [BoundZmqEventBus.<init>] - XPUB binding to [binding to tcp://*:4442, advertising as tcp://10.1.138.85:4442], XSUB binding to [binding to tcp://*:4443, advertising as tcp://10.1.138.85:4443]
12:46:00.285 INFO [UnboundZmqEventBus.<init>] - Connecting to tcp://10.1.138.85:4442 and tcp://10.1.138.85:4443
12:46:00.312 INFO [UnboundZmqEventBus.<init>] - Sockets created
12:46:01.314 INFO [UnboundZmqEventBus.<init>] - Event bus ready
12:46:02.107 INFO [Hub.execute] - Started Selenium Hub 4.26.0 (revision 69f9e5e): http://10.1.138.85:4444
12:46:26.090 INFO [Node.<init>] - Binding additional locator mechanisms: relative
12:46:26.458 INFO [GridModel.setAvailability] - Switching Node 53532aad-df11-4992-a39a-18690438b785 (uri: http://10.1.138.83:5555) from DOWN to UP
12:46:26.458 INFO [LocalDistributor.add] - Added node 53532aad-df11-4992-a39a-18690438b785 at http://10.1.138.83:5555. Health check every 120s
12:58:21.005 INFO [LocalDistributor.newSession] - Session request received by the Distributor: 
 [Capabilities {browserName: chrome, goog:chromeOptions: {args: [--disable-notifications, --disable-popup-blocking, --disable-infobars, --disable-extensions, --disable-gpu, --disable-dev-shm-usage, --no-sandbox, --start-maximized, --ignore-certificate-errors, --headless, --window-size=1920,1080], extensions: []}, pageLoadStrategy: normal}]
12:58:23.726 INFO [LocalDistributor.newSession] - Session created by the Distributor. Id: 4c836d0fce9ad06aad3175ccb29729e4 
 Caps: Capabilities {acceptInsecureCerts: false, browserName: chrome, browserVersion: 130.0.6723.91, chrome: {chromedriverVersion: 130.0.6723.91 (53ac07678369..., userDataDir: /tmp/.org.chromium.Chromium...}, fedcm:accounts: true, goog:chromeOptions: {debuggerAddress: localhost:41269}, networkConnectionEnabled: false, pageLoadStrategy: normal, platformName: linux, proxy: {}, se:bidiEnabled: false, se:cdp: ws://10.1.138.83:4444/sessi..., se:cdpVersion: 130.0.6723.91, se:containerName: , se:noVncPort: 7900, se:vnc: ws://10.1.138.83:4444/sessi..., se:vncEnabled: true, se:vncLocalAddress: ws://10.1.138.83:7900, setWindowRect: true, strictFileInteractability: false, timeouts: {implicit: 0, pageLoad: 300000, script: 30000}, unhandledPromptBehavior: dismiss and notify, webauthn:extension:credBlob: true, webauthn:extension:largeBlob: true, webauthn:extension:minPinLength: true, webauthn:extension:prf: true, webauthn:virtualAuthenticators: true}
12:58:48.890 INFO [Node.<init>] - Binding additional locator mechanisms: relative
12:58:49.592 INFO [GridModel.add] - Re-adding node with id f0771a86-3774-4b56-9025-ca73d1032c58 and URI http://10.1.138.83:5555.
12:58:49.594 INFO [GridModel.setAvailability] - Switching Node f0771a86-3774-4b56-9025-ca73d1032c58 (uri: http://10.1.138.83:5555) from DOWN to UP
12:58:49.594 INFO [LocalDistributor.add] - Added node f0771a86-3774-4b56-9025-ca73d1032c58 at http://10.1.138.83:5555. Health check every 120s
12:58:49.597 INFO [LocalDistributor.newSession] - Session request received by the Distributor: 
 [Capabilities {browserName: chrome, goog:chromeOptions: {args: [--disable-notifications, --disable-popup-blocking, --disable-infobars, --disable-extensions, --disable-gpu, --disable-dev-shm-usage, --no-sandbox, --start-maximized, --ignore-certificate-errors, --headless, --window-size=1920,1080], extensions: []}, pageLoadStrategy: normal}]
12:58:49.600 INFO [LocalSessionMap.remove] - Deleted session from local Session Map, Id: 4c836d0fce9ad06aad3175ccb29729e4
12:58:53.081 INFO [LocalDistributor.newSession] - Session created by the Distributor. Id: f1ac8bdcad8c0353c0813b124b8765c3 
 Caps: Capabilities {acceptInsecureCerts: false, browserName: chrome, browserVersion: 130.0.6723.91, chrome: {chromedriverVersion: 130.0.6723.91 (53ac07678369..., userDataDir: /tmp/.org.chromium.Chromium...}, fedcm:accounts: true, goog:chromeOptions: {debuggerAddress: localhost:45267}, networkConnectionEnabled: false, pageLoadStrategy: normal, platformName: linux, proxy: {}, se:bidiEnabled: false, se:cdp: ws://10.1.138.83:4444/sessi..., se:cdpVersion: 130.0.6723.91, se:containerName: , se:noVncPort: 7900, se:vnc: ws://10.1.138.83:4444/sessi..., se:vncEnabled: true, se:vncLocalAddress: ws://10.1.138.83:7900, setWindowRect: true, strictFileInteractability: false, timeouts: {implicit: 0, pageLoad: 300000, script: 30000}, unhandledPromptBehavior: dismiss and notify, webauthn:extension:credBlob: true, webauthn:extension:largeBlob: true, webauthn:extension:minPinLength: true, webauthn:extension:prf: true, webauthn:virtualAuthenticators: true}
```

### Everything executed on a local Microk8s
```shell
$ microk8s status
microk8s is running
high-availability: no
  datastore master nodes: 127.0.0.1:19001
  datastore standby nodes: none
addons:
  enabled:
    dns                  # (core) CoreDNS
    ha-cluster           # (core) Configure high availability on the current node
    helm                 # (core) Helm - the package manager for Kubernetes
    helm3                # (core) Helm 3 - the package manager for Kubernetes
    hostpath-storage     # (core) Storage class; allocates storage from host directory
    ingress              # (core) Ingress controller for external access
    storage              # (core) Alias to hostpath-storage add-on, deprecated
  disabled:
    cert-manager         # (core) Cloud native certificate management
    cis-hardening        # (core) Apply CIS K8s hardening
    community            # (core) The community addons repository
    dashboard            # (core) The Kubernetes dashboard
    gpu                  # (core) Alias to nvidia add-on
    host-access          # (core) Allow Pods connecting to Host services smoothly
    kube-ovn             # (core) An advanced network fabric for Kubernetes
    mayastor             # (core) OpenEBS MayaStor
    metallb              # (core) Loadbalancer for your Kubernetes cluster
    metrics-server       # (core) K8s Metrics Server for API access to service metrics
    minio                # (core) MinIO object storage
    nvidia               # (core) NVIDIA hardware (GPU and network) support
    observability        # (core) A lightweight observability stack for logs, traces and metrics
    prometheus           # (core) Prometheus operator for monitoring and logging
    rbac                 # (core) Role-Based Access Control for authorisation
    registry             # (core) Private image registry exposed on localhost:32000
    rook-ceph            # (core) Distributed Ceph storage using Rook
```

### Order of deployment
1. `kubectl apply -f k8s/otel-collector-config.yaml`
2. `kubectl apply -f k8s/otel-collector.yaml`
3. `kubectl apply -f k8s/otel-collector-service.yaml`
4. `kubectl apply -f k8s/selenium-hub-deployment.yaml`
5. `kubectl apply -f k8s/selenium-hub-service.yaml`
6. `kubectl apply -f k8s/chrome-node-deployment.yaml`
7. `kubectl apply -f k8s/chrome-node-service.yaml`
8. And after all the above are running, `kubectl apply -f k8s/testcase-controller-job.yaml`

For monitoring the logs, the following command can be used:
```shell
# to get the job status
kubectl get jobs 
# to get the pod name
kubectl get pods
# to get the logs of the pod
kubectl logs -f testcase-controller-<_specific_pod_>
```
