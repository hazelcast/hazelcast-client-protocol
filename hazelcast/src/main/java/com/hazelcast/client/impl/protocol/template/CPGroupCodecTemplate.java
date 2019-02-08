/*
 * Copyright (c) 2008-2019, Hazelcast, Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.hazelcast.client.impl.protocol.template;

import com.hazelcast.annotation.GenerateCodec;
import com.hazelcast.annotation.Request;
import com.hazelcast.annotation.Since;
import com.hazelcast.client.impl.protocol.constants.ResponseMessageConst;
import com.hazelcast.cp.internal.RaftGroupId;

@Since("1.8")
@GenerateCodec(id = TemplateConstants.CP_GROUP_TEMPLATE_ID, name = "CPGroup", ns = "Hazelcast.Client.Protocol.Codec")
public interface CPGroupCodecTemplate {

    /**
     * Creates a new CP group with the given name
     *
     * @param proxyName  The proxy name of this data structure instance
     *
     * @return           ID of the CP group that contains the CP object
     */
    @Request(id = 1, retryable = true, response = ResponseMessageConst.RAFT_GROUP_ID)
    Object createCPGroup(String proxyName);

    /**
     * Destroys the distributed object with the given name on the requested
     * CP group
     *
     * @param groupId     CP group id of this distributed object
     * @param serviceName The service of this distributed object
     * @param objectName  The name of this distributed object
     */
    @Request(id = 2, retryable = true, response = ResponseMessageConst.VOID)
    Object destroyCPObject(RaftGroupId groupId, String serviceName, String objectName);

}
