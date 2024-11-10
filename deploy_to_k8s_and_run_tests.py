from kubernetes import client, config, utils
import time

# Load Kubernetes configuration
config.load_kube_config()

# Define deployment function
def deploy_resources():
    api = client.AppsV1Api()
    core_api = client.CoreV1Api()
    batch_api = client.BatchV1Api()

    # Apply YAML files
    try:
        utils.create_from_yaml(k8s_client=core_api, yaml_file='k8s/otel-collector-config.yaml')
        utils.create_from_yaml(k8s_client=api, yaml_file='k8s/otel-collector.yaml')
        utils.create_from_yaml(k8s_client=core_api, yaml_file='k8s/otel-collector-service.yaml')
        utils.create_from_yaml(k8s_client=api, yaml_file='k8s/selenium-hub-deployment.yaml')
        utils.create_from_yaml(k8s_client=core_api, yaml_file='k8s/selenium-hub-service.yaml')
        utils.create_from_yaml(k8s_client=api, yaml_file='k8s/chrome-node-deployment.yaml')
        utils.create_from_yaml(k8s_client=core_api, yaml_file='k8s/chrome-node-service.yaml')
    except Exception as e:
        print(f"Error deploying selenium grid, chrome nodes or otel: {e}")
        return

    # Wait for Chrome Node Pod to be ready
    ready = False
    pod_list = []
    start_time = time.time()
    timeout = 300
    while not ready:
        pod_list = core_api.list_namespaced_pod(namespace="default", label_selector="app=chrome-node")
        ready = all([pod.status.phase == "Running" for pod in pod_list.items])

        if time.time() - start_time > timeout:
            print("Timeout reached. Chrome Node Pod is not ready.")
            return


        print(f"Chrome Node Pod is not ready yet. Retrying in 5 seconds...")
        print(f"Pods: {pod_list.items}")
        time.sleep(5)
    print(f"Deployment of was successful. Pods: {pod_list.items}")
    print(f"Can proceed with running tests")

    try:
        utils.create_from_yaml(k8s_client=batch_api, yaml_file='k8s/testcase-controller-job.yaml')
    except Exception as e:
        print(f"Error creating testcase-controller job: {e}")
        return

    print(f"Deployment was successful. Pods: {pod_list.items}")

if __name__ == '__main__':
    deploy_resources()