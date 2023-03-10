import requests
import json
import os
import config
import abc
from abc import ABC, abstractmethod


def get_access_token():
    try:
        login_url = "http://52.59.232.190/api/v1/login"
        login_payload = json.dumps({
            "email": "platform-owner@cosmicnode.com", "password": "password"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", login_url, headers=headers,
                                    data=login_payload)
        access_token = {"accessToken": response.json()["data"]["accessToken"]}
        headers.update(access_token)
        return headers

    except Exception as error:
        raise error


def get_payload_for_post_request(test_data_file_name: str):
    """
    load the test data for the given json path.
    :param test_data_file_name: test data file name
    :return: json dump
    """
    json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input',
                             test_data_file_name + '.json')
    if os.path.exists(json_path):
        with open(json_path) as json_file:
            return json.dumps(json.load(json_file))
    else:
        return None


def create_site_level(url: str, test_data_file_name: str):
    """
    Post request to create a site level
    :return: response object
    """
    payload = get_payload_for_post_request(test_data_file_name)
    response = requests.request("POST", url, headers=get_access_token(),
                                data=payload)
    return response


def delete_site_level(url: str, tenant_id: str, level_type_info_name: str):
    """
    Post request to delete a site level
    """
    url_with_tenant_id = f"{url}s?tenantId={tenant_id}"
    response = requests.request("GET", url_with_tenant_id,
                                headers=get_access_token())

    list_of_levels = response.json()["data"]["levelList"]

    levels = [level for level in list_of_levels if (
                (level['tenantId'] == tenant_id) and
                (level["levelTypeInfo"]["name"] == level_type_info_name))]

    for level in levels:
        url_del = f"{url}/?tenantId={tenant_id}"
        payload = json.dumps({"levelId": level["_id"]})
        requests.request("DELETE", url_del,
                         headers=get_access_token(), data=payload)


class Infinity(ABC):
    """
    Abstract class for infinity module
    """
    def __init__(self, dummy_data, api):
        self.dummy_data = dummy_data
        self.url = config.INFINITY_URL + "/" + api
        self._id = None

    @abstractmethod
    def create(self, payload=None):
        """
        create a dummy tenant for testing
        :return: response object of the post action
        """
        response = None
        if payload:
            payload = json.dumps(payload)
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        response_dict = response.json()["data"]
        self._id = response_dict["_id"]
        return response

    @abstractmethod
    def get_details(self, _id):
        """
        get the details of the newly create tenant
        :param _id: using the tenant id get the details of that tenant
        :return: response object with the tenant details
        """
        return requests.request("GET", self.url + "/" + _id,
                                headers=get_access_token())

    @abstractmethod
    def get_id(self):
        """
        return only the tenant id.
        :return: string of the tenant id
        """
        return self._id

    @abstractmethod
    def get_list(self, api):
        """
        get list of all the tenants
        :return: response object of tenant list
        """
        url = config.INFINITY_URL + "/" + api
        return requests.request("GET", url, headers=get_access_token())

    @abstractmethod
    def update(self, payload=None):
        """
        update existing tenant details
        :param payload: dict of the data to be updated
        :return: response object of updated tenant details
        """
        payload = json.dumps(payload)
        response = None
        if payload:
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        return response

    @abstractmethod
    def delete(self, key, value):
        """
        delete a tenant using tenant id
        :param key: payload key
        :param value: value string
        :return: response object
        """
        payload = json.dumps({
            f"{key}": value
        })
        return requests.request("DELETE", self.url, headers=get_access_token(),
                                data=payload)


class Tenant(Infinity):
    """
    Used to create, read, update and delete a tenant from a given API.
    """
    def __init__(self):
        self.dummy_tenant_data = {
            "businessName": "cosmic12",
            "image": "https://infopark.in/assets/image"
                     "s/slider/homeBanner1.jpg",
            "description": "Lorem ipsum dolor sit amet, consec"
                           "tetur adipiscing elit, sed do eiusmod tempor",
            "logo": "image.png",
            "businessTheme": "themeBlack",
            "url": "http://sdjksgdhsd"
        }
        self.api = "tenant"
        super().__init__(dummy_data=self.dummy_tenant_data, api=self.api)
        self.tenant_id = None

    def create(self, payload=None):
        """
        create a dummy tenant for testing
        :return: response object of the post action
        """
        if payload:
            response = super().create(payload=payload)
        else:
            response = super().create(payload=self.dummy_tenant_data)
        self.tenant_id = self._id
        return response

    def get_details(self, tenant_id):
        """
        get the details of the newly create tenant
        :param tenant_id: using the tenant id get the details of that tenant
        :return: response object with the tenant details
        """
        return super().get_details(_id=tenant_id)

    def get_id(self):
        """
        return only the tenant id.
        :return: string of the tenant id
        """
        return self.tenant_id

    def get_list(self, api):
        """
        get list of all the tenants
        :param api:  to get list of tenants
        :return: response object of tenant list
        """
        return super().get_list(api=api)

    def update(self, payload=None):
        """
        update existing tenant details
        :param payload: dict of the data to be updated
        :return: response object of updated tenant details
        """
        if payload is None:
            payload = {
                "businessName": "cosmicN",
                "image": "https://infopark.in/assets/image"
                         "s/slider/homeBanner1.jpg",
                "description": "Lorem ipsum dolor sit amet, consectetur ad"
                               "ipiscing elit, sed do eiusmod tempor",
                "tenantId": self.tenant_id
            }
        return super().update(payload=payload)

    def delete(self, value, key="tenantId"):
        """
        delete a tenant using tenant id
        :param key: key of the json action
        :param value: string of tenant id
        :return: response object
        """
        return super().delete(key="tenantId", value=value)


class Tenants:
    """
    Used to create, read, update and delete a tenant from a given API.
    """
    def __init__(self):
        self.dummy_tenant_data = {
            "businessName": "cosmic12",
            "image": "https://infopark.in/assets/image"
                     "s/slider/homeBanner1.jpg",
            "description": "Lorem ipsum dolor sit amet, consec"
                           "tetur adipiscing elit, sed do eiusmod tempor",
            "logo": "image.png",
            "businessTheme": "themeBlack",
            "url": "http://sdjksgdhsd"
        }
        self.url = config.INFINITY_URL + "/tenant"
        self.tenant_id = None

    def create(self, payload=None):
        """
        create a dummy tenant for testing
        :return: response object of the post action
        """
        if payload:
            payload = json.dumps(payload)
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            dummy_tenant_data = json.dumps(self.dummy_tenant_data)
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=dummy_tenant_data)
        response_dict = response.json()["data"]
        self.tenant_id = response_dict["_id"]
        return response

    def get_tenant_details(self, tenant_id):
        """
        get the details of the newly create tenant
        :param tenant_id: using the tenant id get the details of that tenant
        :return: response object with the tenant details
        """
        return requests.request("GET", self.url + "/" + tenant_id,
                                headers=get_access_token())

    def get_id(self):
        """
        return only the tenant id.
        :return: string of the tenant id
        """
        return self.tenant_id

    @staticmethod
    def get_tenant_list():
        """
        get list of all the tenants
        :return: response object of tenant list
        """
        url = config.INFINITY_URL + "/tenants"
        return requests.request("GET", url, headers=get_access_token())

    def update_tenant(self, payload=None):
        """
        update existing tenant details
        :param payload: dict of the data to be updated
        :return: response object of updated tenant details
        """
        payload = json.dumps(payload)
        if payload:
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            payload = {
                "businessName": "cosmicN",
                "image": "https://infopark.in/assets/image"
                         "s/slider/homeBanner1.jpg",
                "description": "Lorem ipsum dolor sit amet, con"
                               "sectetur adipiscing elit, sed do eiusmod tempor",
                "tenantId": self.tenant_id
            }
            payload = json.dumps(payload)
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        return response

    def delete_tenant(self, tenant_id):
        """
        delete a tenant using tenant id
        :param tenant_id: string of tenant id
        :return: response object
        """
        payload = json.dumps({
            "tenantId": tenant_id
        })
        return requests.request("DELETE", self.url, headers=get_access_token(),
                                data=payload)


class LevelTemplates:
    """
    Used to create, read, update and delete a level template from a given API.
    """
    def __init__(self):
        tenant = Tenant()
        tenant.create()
        self.dummy_level_template_data = {
           "businessTypeName": "cosmic-temlate11"
        }
        self.tenant_id = tenant.get_id()
        self.url = config.INFINITY_URL + "/level-template?ten" \
                                         "antId=" + self.tenant_id
        self.level_template_id = None

    def create_level_template(self, payload=None):
        """
        create a dummy level_template for testing based on existing level
        :return: response object of the post action
        """
        if payload:
            payload = json.dumps(payload)
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            dummy_level_template_data = json.dumps(
                self.dummy_level_template_data
            )
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=dummy_level_template_data)
        response_dict = response.json()["data"]
        self.level_template_id = response_dict["_id"]
        return response

    def get_level_template_list(self):
        """
        get the list of the newly create level templates
        :return: response object with the level templates list
        """
        url = config.INFINITY_URL + "/level-templates?ten" \
                                    "antId=" + self.tenant_id
        return requests.request("GET", url,
                                headers=get_access_token())

    def get_level_template_id(self):
        """
        return only the level template id.
        :return: string of the level template id
        """
        return self.level_template_id

    def get_level_template_details(self):
        """
        get the details of the newly create level template
        :return: response object with the level template details
        """
        url = config.INFINITY_URL + "/level-template/:levelTe" \
                                    "mplateId?tenantId=" + self.tenant_id
        level_template_path = {
            "Path": "levelTemplateId=" + self.level_template_id
        }
        # TODO: get_level_template_details is not working
        payload = json.dumps(level_template_path)
        return requests.request("GET", url,
                                headers=get_access_token(),
                                data=payload)

    def update_level_template(self, payload=None):
        """
        update existing level template details
        :param payload: dict of the data to be updated
        :return: response object of updated level template details
        """
        payload = json.dumps(payload)
        if payload:
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            payload = {
                "_id": self.level_template_id,
                "businessTypeName": "template2",
                "status": "active"
            }
            payload = json.dumps(payload)
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        return response

    def delete_level_template(self, level_template_id):
        """
        delete a level using level template id
        :param level_template_id: string of level template id
        :return: response object
        """
        payload = json.dumps({
            "levelTemplateId": level_template_id
        })
        return requests.request("DELETE", self.url, headers=get_access_token(),
                                data=payload)


class LevelTypes:
    """
    Used to create, read, update and delete a level type from a given API.
    """
    def __init__(self):
        level_template = LevelTemplates()
        level_template.create_level_template()
        self.level_template_id = level_template.get_level_template_id()
        self.tenant_id = level_template.tenant_id
        self.url = config.INFINITY_URL + "/level-type?te" \
                                         "nantId=" + self.tenant_id
        self.level_type_id = None

    def create_level_type(self, payload=None):
        """
        create a dummy level_type for testing based on existing level
        :return: response object of the post action
        """
        if payload:
            payload = json.dumps(payload)
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            dummy_level_type_data = {
                "levelTemplateId": self.level_template_id,
                "type": "Sites",
                "field": [
                    {
                        "type": "text",
                        "name": "name",
                        "validationmessage": "Name is required",
                        "label": "Name",
                        "required": True
                    },
                    {
                        "type": "textarea",
                        "name": "description",
                        "validationmessage": "Description is required",
                        "label": "description",
                        "required": True
                    },
                    {
                        "type": "file",
                        "name": "image",
                        "validationmessage": "Image is required",
                        "label": "Image",
                        "required": True
                    }
                ]
            }

            dummy_level_type_data = json.dumps(
                dummy_level_type_data
            )
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=dummy_level_type_data)
        response_dict = response.json()["data"]
        self.level_type_id = response_dict["_id"]
        return response

    def get_level_type_list(self):
        """
        get the list of the newly create level types
        :return: response object with the level type list
        """
        # http://52.59.232.190/api/v1/level-types?tena
        # ntId=62c7bfc69b7ba0a29cd7bb4e
        # TODO: not able to get the list of level types
        #  based on the API description
        url = config.INFINITY_URL + "/level-types?tenantId=" + self.tenant_id
        return requests.request("GET", url,
                                headers=get_access_token())

    def get_level_type_id(self):
        """
        return only the level type id.
        :return: string of the level type id
        """
        return self.level_type_id

    def get_level_type_details(self):
        """
        get the details of the newly create level type
        :return: response object with the level type details
        """
        url = config.INFINITY_URL + "/level-type/:levelT" \
                                    "ypeId?tenantId=" + self.tenant_id
        level_template_path = {
            "Path": "levelTypeId=" + self.level_type_id
        }
        # TODO: get_level_type_details is not working
        payload = json.dumps(level_template_path)
        return requests.request("GET", url,
                                headers=get_access_token(),
                                data=payload)

    def update_level_type(self, payload=None):
        """
        update existing level type details
        :param payload: dict of the data to be updated
        :return: response object of updated level type details
        """
        payload = json.dumps(payload)
        if payload:
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            payload = {
                   "_id": self.level_type_id,
                   "type": "site",
                   "field": [
                           {
                               "type": "text",
                               "name": "name",
                               "validationmessage": "Name is required",
                               "label": "Name",
                               "required": True
                           },
                           {
                               "type": "textarea",
                               "name": "description",
                               "validationmessage": "Description is required",
                               "label": "description",
                               "required": True
                           },
                           {
                               "type": "file",
                               "name": "image",
                               "validationmessage": "Image is required",
                               "label": "Image",
                               "required": True
                           }
                       ]
                }
            payload = json.dumps(payload)
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        return response

    def delete_level_type(self, level_type_id):
        """
        delete a level using level type id
        :param level_type_id: string of level type id
        :return: response object
        """
        payload = json.dumps({
            "levelTypeId": level_type_id
        })
        return requests.request("DELETE", self.url, headers=get_access_token(),
                                data=payload)


class Level:
    """
    Used to create, read, update and delete a level from a given API.
    """
    def __init__(self):
        level_type = LevelTypes()
        level_type.create_level_type()
        self.level_type_id = level_type.get_level_type_id()
        self.tenant_id = level_type.tenant_id
        self.url = config.INFINITY_URL + "/level"
        self.level_id = None

    def create_level(self, payload=None):
        """
        create a dummy level for testing based on existing level
        :return: response object of the post action
        """
        # TODO: b'{"message":"required data field plan was missing. Pleas
        #  e refer to the documentation for this function."}'
        if payload:
            payload = json.dumps(payload)
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            dummy_level_data = {
               "levelTypeInfo": {
                   "name": "infopark-site",
                   "image": "http://app.pundreek.com/cos/assets/fpl2.jpg",
                   "description": "Lorem ipsum dolor sit amet, consectetur "
                                  "adipiscing elit, sed do eiusmod tempor"
               },
               "levelTypeId": self.level_type_id,
               "tenantId": self.tenant_id,
               "locationAddress": "infopark",
               "contact": "abc@gmail.com",
               "geoLocation": {
                       "latitude": 56.33,
                       "longitude": 54.12
                   }
            }

            dummy_level_data = json.dumps(
                dummy_level_data
            )
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=dummy_level_data)
        response_dict = response.json()["data"]
        self.level_id = response_dict["_id"]
        return response

    def get_level_list(self):
        """
        get the list of the newly create levels
        :return: response object with the level list
        """
        # TODO: not able to get the list of levels
        #  based on the API description
        url = config.INFINITY_URL + "/levels?tenantId=" + self.tenant_id
        return requests.request("GET", url,
                                headers=get_access_token())

    def get_level_id(self):
        """
        return only the level type id.
        :return: string of the level type id
        """
        return self.level_id

    def get_level_details(self):
        """
        get the details of the newly create level
        :return: response object with the level details
        """
        url = config.INFINITY_URL + "/level?tenantId=" + self.tenant_id
        level_template_path = {
            "Query": "ui = 1",
            "Path": "levelId=" + self.level_id
        }
        # TODO: get_level_details is not working
        payload = json.dumps(level_template_path)
        return requests.request("GET", url,
                                headers=get_access_token(),
                                data=payload)

    def update_level(self, payload=None):
        """
        update existing level details
        :param payload: dict of the data to be updated
        :return: response object of updated level details
        """
        payload = json.dumps(payload)
        if payload:
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            payload = {
               "_id": self.level_id,
               "levelTypeInfo": {
                   "name": "infopark-buildin",
                   "image": "http://app.pundreek.com/cos/assets/fpl2.jpg",
                   "description": "Lorem ipsum dolor sit amet, consectetu"
                                  "r adipiscing elit, sed do eiusmod tempor"
               }
            }

            payload = json.dumps(payload)
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        return response

    def delete_level(self, level_id):
        """
        delete a level using level id
        :param level_id: string of level id
        :return: response object
        """
        payload = json.dumps({
            "levelId": level_id
        })
        return requests.request("DELETE", self.url, headers=get_access_token(),
                                data=payload)


class LevelGateway:
    """
    Used to create, read, update and delete a level gateway from a given API.
    """
    def __init__(self):
        level = Level()
        level.create_level()
        self.level_id = level.get_level_id()
        self.tenant_id = level.tenant_id
        self.url = config.INFINITY_URL + "/level-gateway"
        self.level_gateway_id = None

    def create_level_gateway(self, payload=None):
        """
        create a dummy level gateway for testing based on existing level
        :return: response object of the post action
        """
        if payload:
            payload = json.dumps(payload)
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            dummy_level_data = {
               "tenantId": self.tenant_id,
               "levelId": self.level_id,
               "x": 100,
               "y": 200,
               "geoLocation": {
                   "latitude": 100,
                   "longitude": 200
               }
            }

            dummy_level_data = json.dumps(
                dummy_level_data
            )
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=dummy_level_data)
        response_dict = response.json()["data"]
        self.level_id = response_dict["_id"]
        return response

    def get_level_gateway_list(self):
        """
        get the list of the newly create level gateways
        :return: response object with the level gateway list
        """
        # TODO: not able to get the list of levels
        #  based on the API description
        url = config.INFINITY_URL + "/level-gateways" \
                                    "?tenantId=" + self.tenant_id
        return requests.request("GET", url,
                                headers=get_access_token())

    def get_level_gateway_id(self):
        """
        return only the level gateway id.
        :return: string of the level type id
        """
        return self.level_gateway_id

    def get_level_gateway_details(self):
        """
        get the details of the newly create level gateway
        :return: response object with the level gateway details
        """
        url = config.INFINITY_URL + "/level-gateway/:levelGatewa" \
                                    "yId?tenantId=" + self.tenant_id
        level_template_path = {
            "Path": "levelGatewayId=" + self.level_gateway_id
        }
        # TODO: get_level_gateway_details is not working
        payload = json.dumps(level_template_path)
        return requests.request("GET", url,
                                headers=get_access_token(),
                                data=payload)

    def update_level_gateway(self, payload=None):
        """
        update existing level gateway details
        :param payload: dict of the data to be updated
        :return: response object of updated level gateway details
        """
        payload = json.dumps(payload)
        if payload:
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            payload = {
               "_id": self.level_gateway_id,
               "name": "gateway15",
               "status": "active"
            }

            payload = json.dumps(payload)
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        return response

    def delete_level_gateway(self, level_gateway_id):
        """
        delete a level using level gateway id
        :param level_gateway_id: string of level gateway id
        :return: response object
        """
        payload = json.dumps({
            "levelGatewayId": level_gateway_id
        })
        return requests.request("DELETE", self.url, headers=get_access_token(),
                                data=payload)


class FactoryGateway:
    """
    Used to create, read, update and delete a factory gateway from a given API.
    """
    def __init__(self):
        tenant = Tenant()
        tenant.create()
        self.tenant_id = tenant.get_id()
        self.url = config.INFINITY_URL + "/factory-gateway"
        self.factory_gateway_id = None

    def create_factory_gateway(self, payload=None):
        """
        create a dummy factory gateway for testing based on existing factory
        :return: response object of the post action
        """
        if payload:
            payload = json.dumps(payload)
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            dummy_factory_data = {
               "type": "gateway 10",
               "mac": "8C87CES0C5L2",
               "deviceAddress": 244,
               "deviceKey": "C2U968RTA36KLOU",
               "deviceToken": "xCvjoi87Ow2ht4",
               "fwVersion": 2.8,
               "ethernetIpAddress": "192.168.2.101",
               "mqttEnable": False
             }

            dummy_factory_data = json.dumps(
                dummy_factory_data
            )
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=dummy_factory_data)
        response_dict = response.json()["data"]
        self.factory_gateway_id = response_dict["_id"]
        return response

    def get_factory_gateway_list(self):
        """
        get the list of the newly create factory gateways
        :return: response object with the factory gateway list
        """
        # TODO: not able to get the list of factories
        #  based on the API description
        url = config.INFINITY_URL + "/factory-gateways" \
                                    "?tenantId=" + self.tenant_id
        return requests.request("GET", url,
                                headers=get_access_token())

    def get_factory_gateway_id(self):
        """
        return only the factory gateway id.
        :return: string of the factory type id
        """
        return self.factory_gateway_id

    def get_factory_gateway_details(self):
        """
        get the details of the newly create factory gateway
        :return: response object with the factory gateway details
        """
        url = config.INFINITY_URL + "/factory-gateway/:factory" \
                                    "GatewayId?tenantId=" + self.tenant_id
        factory_template_path = {
            "Path": "factoryGatewayId=" + self.factory_gateway_id
        }
        # TODO: get_factory_gateway_details is not working
        payload = json.dumps(factory_template_path)
        return requests.request("GET", url,
                                headers=get_access_token(),
                                data=payload)

    def update_factory_gateway(self, payload=None):
        """
        update existing factory gateway details
        :param payload: dict of the data to be updated
        :return: response object of updated factory gateway details
        """
        payload = json.dumps(payload)
        if payload:
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            payload = {
                   "_id": self.factory_gateway_id,
                   "deviceAddress": 24512,
                   "fwVersion": 2.1
                }

            payload = json.dumps(payload)
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        return response

    def delete_factory_gateway(self, factory_gateway_id):
        """
        delete a factory gateway using factory gateway id
        :param factory_gateway_id: string of factory gateway id
        :return: response object
        """
        payload = json.dumps({
            "factoryGatewayId": factory_gateway_id
        })
        return requests.request("DELETE", self.url, headers=get_access_token(),
                                data=payload)


class ControlApi:
    """
    Used to create, read, update and delete a zone profile from a given API.
    """
    def __init__(self):
        level = Level()
        level.create_level()
        self.level_id = level.get_level_id()
        self.tenant_id = level.tenant_id
        self.url = config.INFINITY_URL + "/mesh-command"

    def set_identifier(self, payload=None):
        """
        set identifier for the control API using tenant id and level id.
        :return: response object of the post action
        """
        if payload:
            payload = json.dumps(payload)
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            dummy_factory_data = {
               "identifier": "brightness_off",
               "tenantId": self.tenant_id,
               "levelId": self.level_id,
               "address": 32769,
               "onoff": 0
            }

            dummy_factory_data = json.dumps(
                dummy_factory_data
            )
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=dummy_factory_data)
        return response


class ZoneProfile:
    """
    Used to create, read, update and delete a zone profile from a given API.
    """
    def __init__(self):
        tenant = Tenant()
        tenant.create()
        self.tenant_id = tenant.get_id()
        self.url = config.INFINITY_URL + "/zone-profile?ten" \
                                         "antId=" + self.tenant_id
        self.zone_profile_id = None

    def create_zone_profile(self, payload=None):
        """
        create a dummy zone profile for testing based on existing zone profile
        :return: response object of the post action
        """
        if payload:
            payload = json.dumps(payload)
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            dummy_zone_profile_data = {
               "name": "meeting room1",
               "controlType": "automatic",
               "sensor": {
                   "motion": {
                       "enabled": True,
                       "dimTime": 12,
                       "holdTime": 10
                   },
                   "daylight": {
                       "enabled": True,
                       "type": "ldr",
                       "ldrAdcThreshold": 3000,
                       "luxThreshold": 400,
                       "updateSteps": 2,
                       "updateInterval": 60
                   }
               },
               "powerOnLevel": 10,
               "maxLevel": 10
            }

            dummy_zone_profile_data = json.dumps(
                dummy_zone_profile_data
            )
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=dummy_zone_profile_data)
        response_dict = response.json()["data"]
        self.zone_profile_id = response_dict["_id"]
        return response

    def get_zone_profile_list(self):
        """
        get the list of the newly create zone profiles
        :return: response object with the zone profile list
        """
        # TODO: not able to get the list of factories
        #  based on the API description
        url = config.INFINITY_URL + "/zone-profiles" \
                                    "?tenantId=" + self.tenant_id
        return requests.request("GET", url,
                                headers=get_access_token())

    def get_zone_profile_id(self):
        """
        return only the zone profile id.
        :return: string of the zone profile type id
        """
        return self.zone_profile_id

    def get_zone_profile_details(self):
        """
        get the details of the newly create zone profile
        :return: response object with the zone profile details
        """
        url = config.INFINITY_URL + "/zone-profile/zoneProf" \
                                    "ileId?tenantId=" + self.tenant_id
        zone_profile_template_path = {
            "Path": "zoneProfileId=" + self.zone_profile_id
        }
        # TODO: get_zone_profile_details is not working
        payload = json.dumps(zone_profile_template_path)
        return requests.request("GET", url,
                                headers=get_access_token(),
                                data=payload)

    def update_zone_profile(self, payload=None):
        """
        update existing zone profile details
        :param payload: dict of the data to be updated
        :return: response object of updated zone profile details
        """
        payload = json.dumps(payload)
        if payload:
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            payload = {
               "_id": self.zone_profile_id,
               "name": "meeting room",
               "controlType": "automatic",
               "sensor": {
                   "motion": {
                       "enabled": True,
                       "dimTime": 12,
                       "holdTime": 10
                   },
                   "daylight": {
                       "enabled": True,
                       "type": "ldr",
                       "ldrAdcThreshold": 3000,
                       "luxThreshold": 400,
                       "updateSteps": 2,
                       "updateInterval": 60
                   }
               },
               "powerOnLevel": 10,
               "maxLevel": 10
            }

            payload = json.dumps(payload)
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        return response

    def delete_zone_profile(self, zone_profile_id):
        """
        delete a zone profile using zone profile id
        :param zone_profile_id: string of zone profile id
        :return: response object
        """
        payload = json.dumps({
            "zoneProfileId": zone_profile_id
        })
        return requests.request("DELETE", self.url, headers=get_access_token(),
                                data=payload)


class DeviceProfile:
    """
    Used to create, read, update and delete a device profile from a given API.
    """
    def __init__(self):
        tenant = Tenant()
        tenant.create()
        self.tenant_id = tenant.get_id()
        self.url = config.INFINITY_URL + "/device-profile?ten" \
                                         "antId=" + self.tenant_id
        self.device_profile_id = None
        self.metric_data_properties_id = None
        self.channel_ids = None

    def create_device_profile(self, payload=None):
        """
        create a dummy device profile for testing based on existing device profile
        :return: response object of the post action
        """
        if payload:
            payload = json.dumps(payload)
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            dummy_device_profile_data = {
               "name": "light12-cosmic",
               "versionNumber": 1.1,
               "deviceType": "sensor",
               "productId": 2,
               "channelNos": 2,
               "channelIds": [
                   "62fb4e63815a07ed70025fdc",
                   "62fb4e74815a07ed70025fe0"
               ],
               "properties": {
                   "dimming_type": "PWM/0-10V/Digital/DALI (In bot"
                                   "h device profile and device details",
                   "module_type": null,
                   "module_vendor": null,
                   "chip_type": null,
                   "radioType": "BLE"
               },
               "metricDataPropertiesIds": [
                   self.metric_data_properties_id
               ]
            }

            dummy_device_profile_data = json.dumps(
                dummy_device_profile_data
            )
            response = requests.request("POST", self.url,
                                        headers=get_access_token(),
                                        data=dummy_device_profile_data)
        response_dict = response.json()["data"]
        self.device_profile_id = response_dict["_id"]
        self.channel_ids = response_dict["channelIds"]
        return response

    def get_device_profile_list(self):
        """
        get the list of the newly create device profiles
        :return: response object with the device profile list
        """
        # TODO: not able to get the list of factories
        #  based on the API description
        url = config.INFINITY_URL + "/device-profiles" \
                                    "?tenantId=" + self.tenant_id
        return requests.request("GET", url,
                                headers=get_access_token())

    def get_device_profile_id(self):
        """
        return only the device profile id.
        :return: string of the device profile type id
        """
        return self.device_profile_id

    def get_device_profile_details(self):
        """
        get the details of the newly create device profile
        :return: response object with the device profile details
        """
        url = config.INFINITY_URL + "/device-profile/:devic" \
                                    "eProfileId??tenantId=" + self.tenant_id
        device_profile_template_path = {
            "Path": "deviceProfileId=" + self.device_profile_id
        }
        # TODO: get_device_profile_details is not working
        payload = json.dumps(device_profile_template_path)
        return requests.request("GET", url,
                                headers=get_access_token(),
                                data=payload)

    def update_device_profile(self, payload=None):
        """
        update existing device profile details
        :param payload: dict of the data to be updated
        :return: response object of updated device profile details
        """
        payload = json.dumps(payload)
        if payload:
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        else:
            payload = {
               "_id": "6304856cb1f8a5d1657ae3ab",
               "name": "light12-cosmic",
               "versionNumber": 1.1,
               "deviceType": "sensor",
               "productId": 4,
               "children": false,
               "channelNos": 3,
               "channelIds": self.channel_ids,
               "properties": {
                   "dimming_type": "PWM/0-10V/Digital/DALI (In both de"
                                   "vice profile and device details",
                   "module_type": null,
                   "module_vendor": null,
                   "chip_type": null,
                   "radioType": "BLE"
               },
               "metricDataPropertiesIds": [
                   self.metric_data_properties_id
               ]
            }

            payload = json.dumps(payload)
            response = requests.request("PUT", self.url,
                                        headers=get_access_token(),
                                        data=payload)
        return response

    def delete_device_profile(self, device_profile_id):
        """
        delete a device profile using device profile id
        :param device_profile_id: string of device profile id
        :return: response object
        """
        payload = json.dumps({
            "deviceProfileId": device_profile_id
        })
        return requests.request("DELETE", self.url, headers=get_access_token(),
                                data=payload)
