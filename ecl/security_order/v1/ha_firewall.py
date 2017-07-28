from ecl.security_order import security_order_service
from ecl import resource2
from ecl import exceptions
from ecl import utils


class HAFirewall(resource2.Resource):
    resource_key = None
    resources_key = None
    base_path = '/API/SoEntryFGHA'
    service = security_order_service.SecurityOrderService()

    # Capabilities
    allow_create = True
    allow_get = True
    allow_delete = True
    allow_list = True
    allow_update = True

    # Properties
    #: Tenant ID of the owner (UUID).
    tenant_id = resource2.Body('tenant_id')
    #: List of following objects.
    #: operatingmode: Set "FW" or "UTM" to this value.
    #: licensekind: Set "02" or "08" as FW/UTM plan.
    #: azgroup: Availability Zone.
    gt_host = resource2.Body('gt_host')
    #: A: Create Single Constitution Device.
    sokind = resource2.Body('sokind', alternate_id=True)
    #: Messages are displayed in Japanese or English depending on this value.
    #: ja: Japanese, en: English. Default value is "en".
    locale = resource2.Body('locale')
    #: This value indicates normal or abnormal. 1:normal, 2:abnormal.
    code = resource2.Body('code')
    #: This message is shown when error has occurred.
    message = resource2.Body('message')
    #: Identification ID of Service Order.
    soid = resource2.Body('soId')
    #: This value indicates normal or abnormal. 1:normal, 2:abnormal.
    status = resource2.Body('status')
    #: Number of devices.
    records = resource2.Body('records')
    #: Device list.
    rows = resource2.Body('rows')
    #: List of device objects.
    devices = resource2.Body('devices')

    def list(self, session, locale=None):
        tenant_id = session.get_project_id()
        uri = '/API/ScreenEventFGHADeviceGet?tenant_id=%s' % tenant_id
        if locale is not None:
            uri += '&locale=%s' % locale
        headers = {'Content-Type': 'application/json'}
        resp = session.get(uri, endpoint_filter=self.service, headers=headers)
        body = resp.json()
        devices = []
        for row in body['rows']:
            device = {
                'internal_use': row['cell'][0],
                'rows': row['cell'][1],
                'ha_id': row['cell'][2],
                'hostname': row['cell'][3],
                'menu': row['cell'][4],
                'plan': row['cell'][5],
                'redundancy': row['cell'][6],
                'availability_zone': row['cell'][7],
                'zone_name': row['cell'][8],
                'link1network_id': row['cell'][9],
                'link1subnet_id': row['cell'][10],
                'link1ip': row['cell'][11],
                'link2network_id': row['cell'][12],
                'link2subnet_id': row['cell'][13],
                'link2ip': row['cell'][14],
            }
            devices.append(device)
        body.update({'devices': devices})
        self._translate_list_response(resp, body, has_body=True)
        return self

    def _translate_list_response(self, response, body, has_body=True):
        if has_body:
            if self.resource_key and self.resource_key in body:
                body = body[self.resource_key]

            body = self._filter_component(body, self._body_mapping())
            self._body.attributes.update(body)
            self._body.clean()

        headers = self._filter_component(response.headers,
                                         self._header_mapping())
        self._header.attributes.update(headers)
        self._header.clean()
