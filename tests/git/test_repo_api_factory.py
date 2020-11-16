import unittest
from unittest.mock import patch, MagicMock

from gitopscli.gitops_exception import GitOpsException
from gitopscli.git import GitRepoApiFactory, GitApiConfig


class GitRepoApiFactoryTest(unittest.TestCase):
    @patch("gitopscli.git.git_repo_api_factory.GithubGitRepoApiAdapter")
    def test_create_github(self, mock_github_adapter_constructor):
        mock_github_adapter = MagicMock()
        mock_github_adapter_constructor.return_value = mock_github_adapter

        git_repo_api = GitRepoApiFactory.create(
            config=GitApiConfig(username="USER", password="PASS", git_provider="github", git_provider_url=None,),
            organisation="ORG",
            repository_name="REPO",
        )

        self.assertEqual(git_repo_api, mock_github_adapter)

        mock_github_adapter_constructor.assert_called_with(
            username="USER", password="PASS", organisation="ORG", repository_name="REPO",
        )

    @patch("gitopscli.git.git_repo_api_factory.BitbucketGitRepoApiAdapter")
    def test_create_bitbucket(self, mock_bitbucket_adapter_constructor):
        mock_bitbucket_adapter = MagicMock()
        mock_bitbucket_adapter_constructor.return_value = mock_bitbucket_adapter

        git_repo_api = GitRepoApiFactory.create(
            config=GitApiConfig(
                username="USER", password="PASS", git_provider="bitbucket-server", git_provider_url="PROVIDER_URL",
            ),
            organisation="ORG",
            repository_name="REPO",
        )

        self.assertEqual(git_repo_api, mock_bitbucket_adapter)

        mock_bitbucket_adapter_constructor.assert_called_with(
            git_provider_url="PROVIDER_URL",
            username="USER",
            password="PASS",
            organisation="ORG",
            repository_name="REPO",
        )

    def test_create_bitbucket_missing_url(self):
        try:
            GitRepoApiFactory.create(
                config=GitApiConfig(
                    username="USER", password="PASS", git_provider="bitbucket-server", git_provider_url=None,
                ),
                organisation="ORG",
                repository_name="REPO",
            )
            self.fail("Expected a GitOpsException")
        except GitOpsException as ex:
            self.assertEqual("Please provide url for bitbucket!", str(ex))

    def test_create_unknown_provider(self):
        try:
            GitRepoApiFactory.create(
                config=GitApiConfig(
                    username="USER", password="PASS", git_provider="unknown-provider", git_provider_url="PROVIDER_URL",
                ),
                organisation="ORG",
                repository_name="REPO",
            )
            self.fail("Expected a GitOpsException")
        except GitOpsException as ex:
            self.assertEqual("Unknown git provider: unknown-provider", str(ex))
