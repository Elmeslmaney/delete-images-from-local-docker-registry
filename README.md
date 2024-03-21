First, ensure that all services are up and running on each machine (both managers and workers). Then, on each machine, execute the following command to delete unused images:

```bash
docker image prune -a
```

Next, list all images on the machines (managers and workers) to create a list of images to be kept:

```bash
docker images --format '{{.Repository}}:{{.Tag}}'
```

Save the list of images and remove `managerip:5000/` from each image in the list, resulting in a format like this:

```
penta-app-resource-center:release.73

```

Update the `images_to_keep.txt` file with your list of images.

After deleting the unnecessary images, execute the registry container using the following command:

```bash
docker exec -it penta-b_registry sh
```

Within the container, run the following command to perform garbage collection:

```bash
registry garbage-collect -m /etc/docker/registry/config.yml
```

This sequence of steps ensures that only the necessary images are kept, and unnecessary images are deleted. Additionally, it performs garbage collection on the registry to reclaim space occupied by deleted images.
