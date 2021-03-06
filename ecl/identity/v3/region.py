# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ecl.identity import identity_service
from ecl import resource


class Region(resource.Resource):
    resource_key = 'region'
    resources_key = 'regions'
    base_path = '/regions'
    service = identity_service.IdentityService()

    # capabilities
    allow_create = True
    allow_retrieve = True
    allow_update = True
    allow_delete = True
    allow_list = True
    patch_update = True

    # Properties
    #: User-facing description of the region. *Type: string*
    description = resource.prop('description')
    #: ID of parent region, if any. *Type: string*
    parent_region_id = resource.prop('parent_region_id')
