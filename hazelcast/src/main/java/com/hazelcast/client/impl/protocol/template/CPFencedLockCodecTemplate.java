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
@GenerateCodec(id = TemplateConstants.CP_FENCED_LOCK_TEMPLATE_ID, name = "CPFencedLock", ns = "Hazelcast.Client.Protocol.Codec")
public interface CPFencedLockCodecTemplate {

    /**
     * Acquires the given FencedLock on the given CP group. If the lock is
     * acquired, a valid fencing token (positive number) is returned. If not
     * acquired because of max reentrant entry limit, the call returns -1.
     * If the lock is held by some other endpoint when this method is called,
     * the caller thread is blocked until the lock is released. If the session
     * is closed between reentrant acquires, the call fails with
     * {@code LockOwnershipLostException}.
     *
     * @param groupId       CP group id of this FencedLock instance
     * @param name          Name of this FencedLock instance
     * @param sessionId     Session ID of the caller
     * @param threadId      ID of the caller thread
     * @param invocationUid UID of this invocation
     *
     * @return              a valid fencing token (positive number) if the lock
     *                      is acquired, otherwise -1.
     */
    @Request(id = 1, retryable = true, response = ResponseMessageConst.LONG)
    Object lock(RaftGroupId groupId, String name, long sessionId, long threadId, UUID invocationUid);

    /**
     * Attempts to acquire the given FencedLock on the given CP group.
     * If the lock is acquired, a valid fencing token (positive number) is
     * returned. If not acquired either because of max reentrant entry limit or
     * the lock is not free during the timeout duration, the call returns -1.
     * If the lock is held by some other endpoint when this method is called,
     * the caller thread is blocked until the lock is released or the timeout
     * duration passes. If the session is closed between reentrant acquires,
     * the call fails with {@code LockOwnershipLostException}.
     *
     * @param groupId       CP group id of this FencedLock instance
     * @param name          Name of this FencedLock instance
     * @param sessionId     Session ID of the caller
     * @param threadId      ID of the caller thread
     * @param invocationUid UID of this invocation
     * @param timeoutMs     Duration to wait for lock acquire
     *
     * @return              a valid fencing token (positive number) if the lock
     *                      is acquired, otherwise -1.
     */
    @Request(id = 2, retryable = true, response = ResponseMessageConst.LONG)
    Object tryLock(RaftGroupId groupId, String name, long sessionId, long threadId, UUID invocationUid, long timeoutMs);

    /**
     * Unlocks the given FencedLock on the given CP group. If the lock is
     * not acquired, the call fails with {@link IllegalMonitorStateException}.
     * If the session is closed while holding the lock, the call fails with
     * {@code LockOwnershipLostException}. Returns true if the lock is still
     * held by the caller after a successful unlock() call, false otherwise.
     *
     * @param groupId       CP group id of this FencedLock instance
     * @param name          Name of this FencedLock instance
     * @param sessionId     Session ID of the caller
     * @param threadId      ID of the caller thread
     * @param invocationUid UID of this invocation
     *
     * @return              true if the lock is still held by the caller after
     *                      a successful unlock() call, false otherwise.
     */
    @Request(id = 3, retryable = true, response = ResponseMessageConst.BOOLEAN)
    Object unlock(RaftGroupId groupId, String name, long sessionId, long threadId, UUID invocationUid);

    /**
     * Returns current lock ownership status of the given FencedLock instance.
     *
     * @param groupId       CP group id of this FencedLock instance
     * @param name          Name of this FencedLock instance
     *
     * @return              current ownership status of this FencedLock
     */
    @Request(id = 4, retryable = true, response = ResponseMessageConst.RAFT_LOCK_OWNERSHIP_STATE_RESPONSE)
    Object getLockOwnership(RaftGroupId groupId, String name);

}
