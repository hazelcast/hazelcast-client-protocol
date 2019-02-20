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

import java.util.UUID;

@Since("1.8")
@GenerateCodec(id = TemplateConstants.CP_SEMAPHORE_TEMPLATE_ID, name = "CPSemaphore", ns = "Hazelcast.Client.Protocol.Codec")
public interface CPSemaphoreCodecTemplate {

    /**
     * Initializes the ISemaphore instance with the given permit number, if not
     * initialized before.
     *
     * @param groupId       CP group id of this ISemaphore instance
     * @param name          Name of this ISemaphore instance
     * @param permits       Number of permits to initialize this ISemaphore
     *
     * @return              true if the ISemaphore is initialized with this call
     */
    @Request(id = 1, retryable = true, response = ResponseMessageConst.BOOLEAN)
    Object init(RaftGroupId groupId, String name, int permits);

    /**
     * Acquires the requested amount of permits if available, reducing
     * the number of available permits. If no enough permits are available,
     * then the current thread becomes disabled for thread scheduling purposes
     * and lies dormant until other threads release enough permits.
     *
     * @param groupId       CP group id of this ISemaphore instance
     * @param name          Name of this ISemaphore instance
     * @param sessionId     Session ID of the caller
     * @param threadId      ID of the caller thread
     * @param invocationUid UID of this invocation
     * @param permits       number of permits to acquire
     * @param timeoutMs     Duration to wait for permit acquire
     *
     * @return              true if requested permits are acquired,
     *                      false otherwise
     */
    @Request(id = 2, retryable = true, response = ResponseMessageConst.BOOLEAN)
    Object acquire(RaftGroupId groupId, String name, long sessionId, long threadId, UUID invocationUid, int permits,
                   long timeoutMs);

    /**
     * Releases the given number of permits and increases the number of
     * available permits by that amount.
     *
     * @param groupId       CP group id of this ISemaphore instance
     * @param name          Name of this ISemaphore instance
     * @param sessionId     Session ID of the caller
     * @param threadId      ID of the caller thread
     * @param invocationUid UID of this invocation
     * @param permits       number of permits to release
     *
     * @return              true
     */
    @Request(id = 3, retryable = true, response = ResponseMessageConst.BOOLEAN)
    Object release(RaftGroupId groupId, String name, long sessionId, long threadId, UUID invocationUid, int permits);

    /**
     * Acquires all available permits at once and returns immediately.
     *
     * @param groupId       CP group id of this ISemaphore instance
     * @param name          Name of this ISemaphore instance
     * @param sessionId     Session ID of the caller
     * @param threadId      ID of the caller thread
     * @param invocationUid UID of this invocation
     *
     * @return              number of acquired permits
     */
    @Request(id = 4, retryable = true, response = ResponseMessageConst.INTEGER)
    Object drain(RaftGroupId groupId, String name, long sessionId, long threadId, UUID invocationUid);

    /**
     * Increases or decreases the number of permits by the given value.
     *
     * @param groupId       CP group id of this ISemaphore instance
     * @param name          Name of this ISemaphore instance
     * @param sessionId     Session ID of the caller
     * @param threadId      ID of the caller thread
     * @param invocationUid UID of this invocation
     * @param permits       number of permits to increase / decrease
     *
     * @return              true
     */
    @Request(id = 5, retryable = true, response = ResponseMessageConst.BOOLEAN)
    Object change(RaftGroupId groupId, String name, long sessionId, long threadId, UUID invocationUid, int permits);

    /**
     * Returns the number of available permits.
     *
     * @param groupId       CP group id of this ISemaphore instance
     * @param name          Name of this ISemaphore instance
     *
     * @return              number of available permits
     */
    @Request(id = 6, retryable = true, response = ResponseMessageConst.INTEGER)
    Object availablePermits(RaftGroupId groupId, String name);

    /**
     * Returns true if the semaphore is JDK compatible
     *
     * @param proxyName     Name of the ISemaphore proxy
     *
     * @return              true if the semaphore is JDK compatible
     */
    @Request(id = 7, retryable = true, response = ResponseMessageConst.BOOLEAN)
    Object getSemaphoreType(String proxyName);

}
