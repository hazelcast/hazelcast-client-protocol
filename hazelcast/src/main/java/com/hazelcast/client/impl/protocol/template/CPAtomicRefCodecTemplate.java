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
import com.hazelcast.annotation.Nullable;
import com.hazelcast.annotation.Request;
import com.hazelcast.annotation.Since;
import com.hazelcast.client.impl.protocol.constants.ResponseMessageConst;
import com.hazelcast.cp.internal.RaftGroupId;
import com.hazelcast.nio.serialization.Data;

@Since("1.8")
@GenerateCodec(id = TemplateConstants.CP_ATOMIC_REF_TEMPLATE_ID, name = "CPAtomicRef", ns = "Hazelcast.Client.Protocol.Codec")
public interface CPAtomicRefCodecTemplate {

    /**
     * Applies a function on the value
     *
     * @param groupId         CP group id of this IAtomicReference instance.
     * @param name            The name of this IAtomicReference instance.
     * @param function        The function applied to the value.
     * @param returnValueType 0 returns no value, 1 returns the old value,
     *                        2 returns the new value
     * @param alter           Denotes whether result of the function will be
     *                        set to the IAtomicRefInstance
     *
     * @return                The result of the function application.
     */
    @Request(id = 1, retryable = false, response = ResponseMessageConst.DATA)
    Object apply(RaftGroupId groupId, String name, Data function, int returnValueType, boolean alter);

    /**
     * Alters the currently stored value by applying a function on it.
     *
     * @param groupId  CP group id of this IAtomicReference instance.
     * @param name     Name of this IAtomicReference instance.
     * @param oldValue The expected value
     * @param newValue The new value
     *
     * @return         true if successful; or false if the actual value
     *                 was not equal to the expected value.
     */
    @Request(id = 2, retryable = false, response = ResponseMessageConst.BOOLEAN)
    Object compareAndSet(RaftGroupId groupId, String name, @Nullable Data oldValue, @Nullable Data newValue);

    /**
     * Checks if the reference contains the value.
     *
     * @param groupId  CP group id of this IAtomicReference instance.
     * @param name     Name of this IAtomicReference instance.
     * @param value    The value to check (is allowed to be null).
     *
     * @return         true if the value is found, false otherwise.
     */
    @Request(id = 3, retryable = true, response = ResponseMessageConst.BOOLEAN)
    Object contains(RaftGroupId groupId, String name, @Nullable Data value);

    /**
     * Gets the current value.
     *
     * @param groupId  CP group id of this IAtomicReference instance.
     * @param name     Name of this IAtomicReference instance.
     *
     * @return         The current value
     */
    @Request(id = 5, retryable = true, response = ResponseMessageConst.DATA)
    Object get(RaftGroupId groupId, String name);

    /**
     * Atomically sets the given value
     *
     * @param groupId        CP group id of this IAtomicReference instance.
     * @param name           Name of this IAtomicReference instance.
     * @param newValue       The value to set
     * @param returnOldValue Denotes whether the old value is returned or not
     *
     * @return               the old value or null, depending on
     *                       the {@code returnOldValue} parameter
     */
    @Request(id = 6, retryable = false, response = ResponseMessageConst.DATA)
    Object set(RaftGroupId groupId, String name, @Nullable Data newValue, boolean returnOldValue);

}
