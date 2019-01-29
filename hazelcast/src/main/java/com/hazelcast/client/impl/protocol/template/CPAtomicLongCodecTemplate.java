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
import com.hazelcast.nio.serialization.Data;

@Since("1.8")
@GenerateCodec(id = TemplateConstants.CP_ATOMIC_LONG_TEMPLATE_ID, name = "CPAtomicLong", ns = "Hazelcast.Client.Protocol.Codec")
public interface CPAtomicLongCodecTemplate {

    /**
     * Applies a function on the value, the actual stored value will not change
     *
     * @param groupId  CP group id of this IAtomicLong instance.
     * @param name     Name of this IAtomicLong instance.
     * @param function The function applied to the value and the value is not
     *                 changed.
     * @return The result of the function application.
     */
    @Request(id = 1, retryable = false, response = ResponseMessageConst.DATA)
    Object apply(RaftGroupId groupId, String name, Data function);

    /**
     * Alters the currently stored value by applying a function on it.
     *
     * @param groupId         CP group id of this IAtomicLong instance.
     * @param name            Name of this IAtomicLong instance.
     * @param function        The function applied to the currently stored value.
     * @param returnValueType 0 returns the old value, 1 returns the new value
     */
    @Request(id = 2, retryable = false, response = ResponseMessageConst.LONG)
    void alter(RaftGroupId groupId, String name, Data function, int returnValueType);

    /**
     * Atomically adds the given value to the current value.
     *
     * @param groupId  CP group id of this IAtomicLong instance.
     * @param name     Name of this IAtomicLong instance.
     * @param delta    The value to add to the current value
     *
     * @return the updated value, the given value added to the current value
     */
    @Request(id = 3, retryable = false, response = ResponseMessageConst.LONG)
    Object addAndGet(RaftGroupId groupId, String name, long delta);

    /**
     * Atomically sets the value to the given updated value only if the current
     * value the expected value.
     *
     * @param groupId  CP group id of this IAtomicLong instance.
     * @param name     Name of this IAtomicLong instance.
     * @param expected The expected value
     * @param updated  The new value
     *
     * @return true if successful; or false if the actual value
     *         was not equal to the expected value.
     */
    @Request(id = 4, retryable = false, response = ResponseMessageConst.BOOLEAN)
    Object compareAndSet(RaftGroupId groupId, String name, long expected, long updated);

    /**
     * Gets the current value.
     *
     * @param groupId  CP group id of this IAtomicLong instance.
     * @param name     Name of this IAtomicLong instance.
     *
     * @return The current value
     */
    @Request(id = 5, retryable = true, response = ResponseMessageConst.LONG)
    Object get(RaftGroupId groupId, String name);

    /**
     * Atomically adds the given value to the current value.
     *
     * @param groupId  CP group id of this IAtomicLong instance.
     * @param name     Name of this IAtomicLong instance.
     * @param delta    The value to add to the current value
     *
     * @return the old value before the add
     */
    @Request(id = 6, retryable = false, response = ResponseMessageConst.LONG)
    Object getAndAdd(RaftGroupId groupId, String name, long delta);

    /**
     * Atomically sets the given value and returns the old value.
     *
     * @param groupId  CP group id of this IAtomicLong instance.
     * @param name     Name of this IAtomicLong instance.
     * @param newValue The new value
     *
     * @return the old value
     */
    @Request(id = 7, retryable = false, response = ResponseMessageConst.LONG)
    Object getAndSet(RaftGroupId groupId, String name, long newValue);

}
