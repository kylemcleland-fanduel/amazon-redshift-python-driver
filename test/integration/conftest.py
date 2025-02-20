import configparser
import os
import sys

import pytest  # type: ignore

import redshift_connector

conf = configparser.ConfigParser()
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf.read(root_path + "/config.ini")


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # execute all other hooks to obtain the report object
#     outcome = yield
#     rep = outcome.get_result()
#
#     # we only look at actual failing test calls, not setup/teardown
#     if rep.when == "call" and rep.failed:
#         mode = "a" if os.path.exists("failures") else "w"
#         with open("failures", mode) as f:
#             f.write(rep.longreprtext + "\n")


def _get_default_connection_args():
    """
    Helper function defining default database connection parameter values.
    Returns
    -------

    """
    return {
        "database": conf.get("ci-cluster", "database"),
        "host": conf.get("ci-cluster", "host"),
        "port": conf.getint("default-test", "port"),
        "user": conf.get("ci-cluster", "test_user"),
        "password": conf.get("ci-cluster", "test_password"),
        "ssl": conf.getboolean("default-test", "ssl"),
        "sslmode": conf.get("default-test", "sslmode"),
        "region": conf.get("ci-cluster", "region"),
        "cluster_identifier": conf.get("ci-cluster", "cluster_identifier"),
    }


def _get_default_iam_connection_args():
    args = _get_default_connection_args()
    del args["host"]
    del args["port"]
    args["password"] = ""
    return args


@pytest.fixture(scope="class")
def db_kwargs():
    return _get_default_connection_args()


def db_groups():
    return conf.get("cluster-setup", "groups").split(sep=",")


@pytest.fixture(scope="class")
def perf_db_kwargs():
    db_connect = {
        "database": conf.get("performance-database", "database"),
        "host": conf.get("performance-database", "host"),
        "user": conf.get("performance-database", "user"),
        "password": conf.get("performance-database", "password"),
        "ssl": conf.getboolean("performance-database", "ssl"),
        "sslmode": conf.get("performance-database", "sslmode"),
    }

    return db_connect


@pytest.fixture(scope="class")
def okta_idp():
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user"),
        "password": conf.get("okta-idp", "password"),
        "iam": conf.getboolean("okta-idp", "iam"),
        "idp_host": conf.get("okta-idp", "idp_host"),
        "user": conf.get("okta-idp", "user"),
        "app_id": conf.get("okta-idp", "app_id"),
        "app_name": conf.get("okta-idp", "app_name"),
        "credentials_provider": conf.get("okta-idp", "credentials_provider"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def okta_browser_idp():
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user"),
        "password": conf.get("okta-browser-idp", "password"),
        "iam": conf.getboolean("okta-browser-idp", "iam"),
        "user": conf.get("okta-browser-idp", "user"),
        "credentials_provider": conf.get("okta-browser-idp", "credentials_provider"),
        "login_url": conf.get("okta-browser-idp", "login_url"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def azure_browser_idp():
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user"),
        "password": conf.get("azure-browser-idp", "password"),
        "iam": conf.getboolean("azure-browser-idp", "iam"),
        "user": conf.get("azure-browser-idp", "user"),
        "credentials_provider": conf.get("azure-browser-idp", "credentials_provider"),
        "idp_tenant": conf.get("azure-browser-idp", "idp_tenant"),
        "client_id": conf.get("azure-browser-idp", "client_id"),
        "client_secret": conf.get("azure-browser-idp", "client_secret"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def jumpcloud_browser_idp():
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user"),
        "password": conf.get("jumpcloud-browser-idp", "password"),
        "iam": conf.getboolean("jumpcloud-browser-idp", "iam"),
        "user": conf.get("jumpcloud-browser-idp", "user"),
        "credentials_provider": conf.get("jumpcloud-browser-idp", "credentials_provider"),
        "login_url": conf.get("jumpcloud-browser-idp", "login_url"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def ping_browser_idp():
    db_connect = {
        "iam": conf.getboolean("ping-one-idp", "iam"),
        "credentials_provider": conf.get("ping-one-idp", "credentials_provider"),
        "login_url": conf.get("ping-one-idp", "login_url"),
        "listen_port": conf.getint("ping-one-idp", "listen_port"),
        "idp_response_timeout": conf.getint("ping-one-idp", "idp_response_timeout"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def azure_idp():
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user"),
        "password": conf.get("azure-idp", "password"),
        "iam": conf.getboolean("azure-idp", "iam"),
        "user": conf.get("azure-idp", "user"),
        "credentials_provider": conf.get("azure-idp", "credentials_provider"),
        "idp_tenant": conf.get("azure-idp", "idp_tenant"),
        "client_id": conf.get("azure-idp", "client_id"),
        "client_secret": conf.get("azure-idp", "client_secret"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def adfs_idp():
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user"),
        "password": conf.get("adfs-idp", "password"),
        "iam": conf.getboolean("adfs-idp", "iam"),
        "user": conf.get("adfs-idp", "user"),
        "credentials_provider": conf.get("adfs-idp", "credentials_provider"),
        "idp_host": conf.get("adfs-idp", "idp_host"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def jwt_google_idp():
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user"),
        "iam": conf.getboolean("jwt-google-idp", "iam"),
        "password": conf.get("jwt-google-idp", "password"),
        "credentials_provider": conf.get("jwt-google-idp", "credentials_provider"),
        "web_identity_token": conf.get("jwt-google-idp", "web_identity_token"),
        "role_arn": conf.get("jwt-google-idp", "role_arn"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def jwt_azure_v2_idp():
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user"),
        "iam": conf.getboolean("jwt-azure-v2-idp", "iam"),
        "password": conf.get("jwt-azure-v2-idp", "password"),
        "credentials_provider": conf.get("jwt-azure-v2-idp", "credentials_provider"),
        "web_identity_token": conf.get("jwt-azure-v2-idp", "web_identity_token"),
        "role_arn": conf.get("jwt-azure-v2-idp", "role_arn"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture
def con(request, db_kwargs):
    conn = redshift_connector.connect(**db_kwargs)

    def fin():
        conn.rollback()
        try:
            conn.close()
        except redshift_connector.InterfaceError:
            pass

    request.addfinalizer(fin)
    return conn


@pytest.fixture
def cursor(request, con):
    cursor = con.cursor()

    def fin():
        cursor.close()

    request.addfinalizer(fin)
    return cursor


@pytest.fixture
def idp_arg(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def is_java():
    return "java" in sys.platform.lower()
