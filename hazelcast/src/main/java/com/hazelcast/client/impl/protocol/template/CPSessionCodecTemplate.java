/*
 * Copyright (c) 2008-2018, Hazelcast, Inc. All Rights Reserved.
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
@GenerateCodec(id = TemplateConstants.CP_SESSION_TEMPLATE_ID, name = "CPSession", ns = "Hazelcast.Client.Protocol.Codec")
public interface CPSessionCodecTemplate {

    /**
     * Creates a session for the caller on the given CP group.
     *
     * @param groupId      ID of the CP group
     * @param endpointName Name of the caller HazelcastInstance
     *
     * @return             ID of the new session
     */
    @Request(id = 1, retryable = true, response = ResponseMessageConst.RAFT_SESSION_RESPONSE)
    Object createSession(RaftGroupId groupId, String endpointName);

    /**
     * Closes the given session on the given CP group
     *
     * @param groupId   ID of the CP group
     * @param sessionId ID of the session
     *
     * @return          true if the session is found & closed,
     *                  false otherwise.
     */
    @Request(id = 2, retryable = true, response = ResponseMessageConst.BOOLEAN)
    Object closeSession(RaftGroupId groupId, long sessionId);

    /**
     * Commits a heartbeat for the given session on the given cP group and
     * extends its session expiration time.
     *
     * @param groupId   ID of the CP group
     * @param sessionId ID of the session
     */
    @Request(id = 3, retryable = true, response = ResponseMessageConst.VOID)
    Object heartbeatSession(RaftGroupId groupId, long sessionId);

    /**
     * Generates a new ID for the caller thread. The ID is unique in the given
     * CP group.
     *
     * @param groupId      ID of the CP group
     *
     * @return             A unique ID for the caller thread
     */
    @Request(id = 4, retryable = true, response = ResponseMessageConst.LONG)
    Object generateThreadId(RaftGroupId groupId);

}
