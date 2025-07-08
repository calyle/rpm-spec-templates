#!/usr/bin/env python3

"""
:Author: Jo Carllyle
:Copyright: 2024 Jo Carllyle
:License: MIT
:Info: Automatically build packages by copr api
:Thanks: https://github.com/akdev1l/copr-build
"""

from os import getenv, path, makedirs
from time import sleep

import pandas as pd
from github import Github, Repository
from logging import getLogger, basicConfig, INFO
from copr.v3 import Client
from pandas import Series


basicConfig(level=INFO)
logger = getLogger(__name__)


def get_latest_version(row: Series, github: Github) -> str:
    mode = row.get("mode")
    if mode == "commit":
        return github.get_repo(
            f'{row.get("author")}/{row.get("repo name")}').get_branch(row.get("branch")).commit.sha[0:7]
    elif mode == "release":
        return github.get_repo(f'{row.get("author")}/{row.get("repo name")}').get_latest_release().tag_name
    elif mode == "tag":
        return github.get_repo(f'{row.get("author")}/{row.get("repo name")}').get_tags()[0].name
    else:
        return ''


def config_copr() -> None:
    copr_api_token_cfg = getenv('COPR_API_TOKEN_CONFIG')
    copr_cfg_path = path.expanduser("~/.config/copr")
    copr_cfg_dir = path.dirname(copr_cfg_path)

    if copr_api_token_cfg is None and not path.exists(copr_cfg_path):
        logger.error("you need to pass the COPR API configuration as COPR_API_TOKEN_CONFIG")
        exit(1)

    if not path.isdir(copr_cfg_dir):
        logger.info(f"creating {copr_cfg_path}")
        makedirs(copr_cfg_dir)

    if not path.exists(copr_cfg_path):
        with open(copr_cfg_path, "w") as copr_cfg_file:
            logger.info(f"writing credentials to {copr_cfg_path}")
            copr_cfg_file.write(copr_api_token_cfg)
    else:
        logger.info("detected existing config, avoiding overwrite")


def copr_builder(copr_client: Client, owner: str, project_name: str, package_name: str) -> None:
    copr_client.package_proxy.build(owner, project_name, package_name)


def commit_changes(
        repo: Repository,
        package_name: str,
        old_content: str,
        new_content: str,
        csv_path: str) -> None:
    commit_msg = f'chore: update package {package_name} to {new_content.split(",")[1]}'
    csv_content = repo.get_contents(csv_path)
    content = csv_content.decoded_content.decode('utf-8')
    updated_content = content.replace(old_content, new_content)
    repo.update_file(
        path=csv_path,
        message=commit_msg,
        content=updated_content,
        sha=csv_content.sha
    )


def runner():
    github_token = getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN NOT FOUND")
    gh = Github(github_token)
    repo = gh.get_repo('calyle/rpm-spec-templates')

    csv_path = '.github/pkgs_info.csv'
    df = pd.read_csv(csv_path, dtype=str)

    config_copr()
    owner = getenv("OWNER")
    copr_client = Client.create_from_config_file()
    for _, row in df.iterrows():
        try:
            old_content = f'{row.get("author")},{row.get("latest version")}'
            new_content = f'{row.get("author")},{get_latest_version(row, gh)}'
            if new_content == old_content:
                continue
            copr_builder(copr_client, owner, row.get("project name"), row.get("package name"))
            logger.info(f'Build {row.get("package name")} by copr')
            commit_changes(repo, row.get("package name"), old_content, new_content, csv_path)
            logger.info(f'Update version of package {row.get("package name")}')
            sleep(3)
        except Exception as e:
            logger.error(f'{e}')
        finally:
            continue


if __name__ == '__main__':
    runner()
