import os

from haikunator import Haikunator
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import AppServicePlan, SkuDescription, Site

WEST_US = 'westus'
GROUP_NAME = 'azure-sample-group'
SERVER_FARM_NAME = 'sample-server-farm'
SITE_NAME = Haikunator().haikunate()


def example1():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    resource_client = ResourceManagementClient(credentials, subscription_id)
    web_client = WebSiteManagementClient(credentials, subscription_id)
    # Resource group
    print('Create Resource Group')
    resource_group_params = {'location': 'westus'}
    print_item(resource_client.resource_groups.create_or_update(
        GROUP_NAME, resource_group_params))

    #App service

    print('Create an App Service plan for your WebApp')

    service_plan_async_operation = web_client.app_service_plans.create_or_update(
        GROUP_NAME,
        SERVER_FARM_NAME,
        AppServicePlan(
            app_service_plan_name=SERVER_FARM_NAME,
            location=WEST_US,
            sku=SkuDescription(
                name='S1',
                capacity=1,
                tier='Standard'
            )
        )
    )
    service_plan = service_plan_async_operation.result()
    print_item(service_plan)

    #
    # Create a Site to be hosted on the App Service plan
    #
    print('Create a Site to be hosted on the App Service plan')
    site_async_operation = web_client.web_apps.create_or_update(
        GROUP_NAME,
        SITE_NAME,
        Site(
            location=WEST_US,
            server_farm_id=service_plan.id
        )
    )
    site = site_async_operation.result()
    print_item(site)

    # List Sites by Resource Group

    print('List Sites by Resource Group')
    for site in web_client.web_apps.list_by_resource_group(GROUP_NAME):
        print_item(site)
if __name__ == "__main__":
    example1()