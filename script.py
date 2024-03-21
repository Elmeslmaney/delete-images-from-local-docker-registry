import requests

class DockerImageManager:
    def __init__(self, registry_url):
        self.registry_url = registry_url
        self.docker_registry_images = []

    def get_local_docker_images(self, repo_name):
        url = f"{self.registry_url}/v2/{repo_name}/tags/list"
        response = requests.get(url)
        images_list = response.json().get("tags", [])
        if images_list:
            for tag in images_list:
                docker_image = f"{repo_name}:{tag}"
                if docker_image not in self.images_to_keep:
                    self._delete_docker_image(repo_name, tag)
                self.docker_registry_images.append(f"{repo_name}:{tag}")
        return images_list

    def _delete_docker_image(self, repo_name, tag):
        digest = self._get_docker_image_digest(repo_name, tag)
        if digest:
            self._delete_docker_image_by_digest(repo_name, digest)

    def _delete_docker_image_by_digest(self, repo_name, digest):
        url = f"{self.registry_url}/v2/{repo_name}/manifests/{digest}"
        try:
            response = requests.delete(url)
            response.raise_for_status()
            print(f"Image with digest {digest} deleted successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def _get_docker_image_digest(self, repo_name, tag):
        url = f"{self.registry_url}/v2/{repo_name}/manifests/{tag}"
        headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.headers['Docker-Content-Digest']
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def delete_docker_image_registry(self):
        url = f"{self.registry_url}/v2/_catalog"
        response = requests.get(url)
        if response.status_code == 200:
            catalog = response.json().get("repositories", [])
            for repo in catalog:
                self.get_local_docker_images(repo)
        else:
            print(f"Failed to retrieve catalog from the registry. Status code: {response.status_code}")

    def load_images_to_keep(self, filename):
        with open(filename, 'r') as file:
            self.images_to_keep = [line.strip() for line in file]

# Example usage
registry_url = "http://192.168.1.116:5000"
images_to_keep_file = "images_to_keep.txt"

docker_image_manager = DockerImageManager(registry_url)
docker_image_manager.load_images_to_keep(images_to_keep_file)
docker_image_manager.delete_docker_image_registry()
print(docker_image_manager.docker_registry_images)
