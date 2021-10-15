# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from dockerfile_parse import DockerfileParser
from io import BytesIO
import json
import os
import pycurl
import subprocess
import sys
import time

EXECUTOR_PATH = "/kaniko/executor"
USER_NAME = "XXXX"
PASSWORD = "XXXX"

class BuildImage():
    def __init__(self):
        self.executor_path = EXECUTOR_PATH
        self.registry_images = []
        self.image_tags ={}
    
    def extract_base_image_from_dockerfile(self, dockerfile: str):
        """
        Dockerfileから使用するBase Imageを検索する

        Parameters
        ----------
        dockerfile: string
            Dockerfileのパス（Dockerfile名を含む）
        
        Returns
        ----------
        baseimage: list[string] (ex. l4t:latest)
            使用しているBase Image名とタグ
        """
        dfp = DockerfileParser(path=dockerfile)
        return dfp.baseimage
        
    def fetch_all_images_in_registry(self, 
                                    registry: str, 
                                    username=None, 
                                    password=None
                                    ) -> list:
        """
        Dockerレジストリ内の全てのイメージとタグを取得する

        Parameters
        ----------
        registry: string 
            DockerレジストリのURL
        username: string
            Dockerレジストリのユーザー名
        password: string
            Dockerレジストリのパスワード
    
        Returns
        ----------
        dict: {image: [tag]}
            Image名とタグ
        """
        url = registry + "v2/_catalog"
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(pycurl.USERPWD, 'XXX:XXX' %(USER_NAME, PASSWORD))
        c.setopt(c.WRITEDATA, buffer)
        try:
            c.perform()
            c.close()
        except pycurl.error as e:
            print(e)
            return None
        else:
            body = buffer.getvalue()
            res = json.loads(body)
            for r in res["repositories"]:
                self.registry_images.append(r)
            self._fetch_all_tags(registry, 
                                username, 
                                password, 
                                self.registry_images)
            return self.image_tags
    
    def _fetch_all_tags(self, 
                        registry: str, 
                        username: str, 
                        password: str,
                        repositories: list):
        """
        Dockerレジストリ内の全てのイメージとタグを取得する

        Parameters
        ----------
        registry: string 
            DockerレジストリのURL
        username: string
            Dockerレジストリのユーザー名
        password: string
            Dockerレジストリのパスワード
        repositories: list[string]
            検索対象のリポジトリ名
    
        Returns
        ----------
        dict: {image: [tag]}
            Image名とタグ
        """
        self.image_tags = {}
        for repo in repositories:
            url = registry + "v2/{}/tags/list".format(repo)
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(pycurl.USERPWD, 'XXX:XXX' %(USER_NAME, PASSWORD))
            c.setopt(c.WRITEDATA, buffer)
            try:
                c.perform()
                c.close()
            except pycurl.error as e:
                print(e)
                continue
            else:
                body = buffer.getvalue()
                res = json.loads(body)
                for r in res["tags"]:
                    self.image_tags.setdefault(repo, []).append(r)

    def exist_image_and_tag(self, image: str, tag: str) -> bool:
        """
        Dockerレジストリ内の全てのイメージとタグを取得する

        Parameters
        ----------
        image: string 
            検索するイメージ
        tag: string
            検索するタグ
    
        Returns
        ----------
        bool
        """
        if image in self.image_tags:
            if tag in self.image_tags[image]:
                return True
            else: 
                return False
        else:
            return False

    def search_image_in_registry(self, image: str, 
                                tag: str,
                                registry: str,
                                username=None,
                                password=None
                                ) -> bool:
        """
        Base ImageがDockerレジストリに存在するか、確認する

        Parameters
        ----------
        image: string
            検索するイメージ名
        tag: string
            検索するタグ
        registry: string
            検索対象のDocker RegistryのURL
        username: string
            Docker Registryのユーザー名
        password: string
            Docker Registryのパスワード

        Returns
        -------
        bool
            True, Falseのいずれかを返す
        """
        url = registry + "v2/{}/tags/list".format(image)
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(pycurl.USERPWD, 'XXX:XXX' %(USER_NAME, PASSWORD))
        c.setopt(c.WRITEDATA, buffer)
        try:
            c.perform()
            c.close()
            body = buffer.getvalue()
            # 対象のタグが検索結果に存在する場合はTrueを返す
            res = json.loads(body)
            print(type(res))
            print(res)
            for r in res["tags"]:
                if r == tag:
                    return True
            else:
                print("There isn't matched base image in docker registry")
                return False
        except pycurl.error as e:
            print(e)
            return False
    
    def rename_baseimage_in_dockerfile(self, dockerfile, baseimage):
        """
        DockerfileのBase Image名にリポジトリを追加する
        
        Parameters
        ----------
        dockerfile: string
            Dockerfileのパス（Dockerfile名を含む）
        baseimage: string
            新しいbaseimage名
        """
        dfp = DockerfileParser(path=dockerfile)
        dfp.baseimage = baseimage

    def build_push(self,
                   dockerfile: str,
                   context: str,
                   destination: str,
                   insecure=True,
                   skip_tls_verify=True):
        """
        Kanikoを用いて、コンテナイメージをビルドしレジストリにプッシュする
        ToDo: httpsへの対応

        Parameters
        ----------
        dockerfile: string
            ビルド対象のDockerfileのパス（Dockerfile名を含む）
        context: string
            ビルド対象のディレクトリのパス
        destination: string
            プッシュ先のレジストリのURL
        """
        command = "{} --dockerfile {} --context {} --destination {}".format(
            self.executor_path, dockerfile, context, destination)
        if insecure:
            command += " --insecure"
            command += " --insecure-pull"
        if skip_tls_verify:
            command += " --skip-tls-verify"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Failed to build and push image", file=sys.stderr)
