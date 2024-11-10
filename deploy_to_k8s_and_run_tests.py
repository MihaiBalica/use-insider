from kubernetes import client, config, utils
import time

# Load Kubernetes configuration
config.load_kube_config()

# Define deployment function
def deploy_resources():
    api = client.AppsV1Api()
    core_api = client.CoreV1Api()

    # Apply YAML files
    utils.create_from_yaml(k8s_client=api, yaml_file='k8s/testcase-controller-job.yaml')
    utils.create_from_yaml(k8s_client=api, yaml_file='k8s/chrome-node-deployment.yaml')
    utils.create_from_yaml(k8s_client=core_api, yaml_file='k8s/chrome-node-service.yaml')
    utils.create_from_yaml(k8s_client=api, yaml_file='k8s/selenium-hub-deployment.yaml')
    utils.create_from_yaml(k8s_client=core_api, yaml_file='k8s/selenium-hub-service.yaml')

    # Wait for Chrome Node Pod to be ready
    ready = False
    pod_list = []
    while not ready:
        pod_list = core_api.list_namespaced_pod(namespace="default", label_selector="app=chrome-node")
        ready = all([pod.status.phase == "Running" for pod in pod_list.items])
        print(f"Chrome Node Pod is not ready yet. Retrying in 5 seconds...")
        print(f"Pods: {pod_list.items}")
        time.sleep(5)

    print(f"Deployment is successful. Pods: {pod_list.items}")

if __name__ == '__main__':
    deploy_resources()