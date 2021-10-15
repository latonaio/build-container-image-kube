# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import os
from aion.kanban import Kanban
from aion.logger import lprint
from aion.microservice import Options, main_decorator
from .gitcontroller import GitController
from .build_image import BuildImage

SERVICE_NAME = "build-container-image"
OAUTH_KEY = "XXXXXXXXXXXX"
OAUTH_SECRET = "XXXXXXXXXXXXXXXXXX"
CLONE_PATH = "/tmp/"

@main_decorator(SERVICE_NAME)
def main(opt):
    conn = opt.get_conn()
    num = opt.get_number()
    is_docker = opt.is_docker()

    # get cache kanban
    kanban = conn.set_kanban(SERVICE_NAME, num)

  #  for kanban in conn.get_kanban_itr(SERVICE_NAME, num):
    for _ in range(1):  # Debug
        # metadata = kanban.get_metadata()
        # repository = metadata.get("repository")
        # tag = metadata.get("tag")
        repository = "dependency-containers"
        tag = "master"
        context = "dependency-containers/deepstream-l4t"
        dockerfile = "dependency-containers/deepstream-l4t/Dockerfile"
        registry = "kube-registry:5000/"
        new_image_tag = "latest"

        path = CLONE_PATH + repository
        gc = GitController(OAUTH_KEY, OAUTH_SECRET)
        res = gc.clone(repository, tag, path)
        if res == None:
            print("Failed to clone a repository {}".format(repository))
        else:
            bi = BuildImage()
            dockerfile = CLONE_PATH + dockerfile
            context = CLONE_PATH + context
            new_image_name = os.path.basename(os.path.dirname(dockerfile))
            destination = registry + new_image_name + "/" + new_image_tag
            baseimage = bi.extract_base_image_from_dockerfile(dockerfile)
            print(baseimage)
            if baseimage == None:
                print("There is no base image")
                exit()
            try:
                image, tag = baseimage.split(":")
            except ValueError:
                print("tag is not set")
                image = baseimage
                tag = "latest"
            finally:
                bi.fetch_all_images_in_registry(registry)
                res = bi.exist_image_and_tag(image, tag)
#               res = bi.search_image_in_registry(image, tag, registry)
                if res:
                    baseimage = registry + baseimage
                    bi.rename_baseimage_in_dockerfile(dockerfile, baseimage)
                    print("dockerfile: " + dockerfile)
                    print("context: " + context)
                    print("destination: " + destination)
                    bi.build_push(dockerfile, context, destination)
                else:
                    print("There is not {}:{} in docker registry".format(image, tag))
"""
        conn.output_kanban(
            connection_key="image_built",
            metadata={
                "docker_registry_url": "localhost:XXXXX",
                "container_image": repository + ":" + tag
            }
        )
"""
