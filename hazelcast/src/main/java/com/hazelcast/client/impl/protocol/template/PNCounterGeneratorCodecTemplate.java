/*
 * Copyright (c) 2008-2017, Hazelcast, Inc. All Rights Reserved.
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

@GenerateCodec(id = TemplateConstants.PN_COUNTER_ID_GENERATOR_TEMPLATE_ID, name = "PNCounter", ns = "Hazelcast.Client.Protocol.Codec")
public interface PNCounterGeneratorCodecTemplate {

    /**
     * Query operation to retrieve the current value of the PNCounter.
     *
     * @param name the name of the PNCounter
     * @return the current value of the counter
     */
    @Request(id = 1, retryable = true, response = ResponseMessageConst.LONG)
    @Since("1.6")
    Object get(String name);

    /**
     * Adds a delta to the PNCounter value. The delta may be negative for a
     * subtraction.
     *
     * @param name            the name of the PNCounter
     * @param delta           the delta to add to the counter value, can be negative
     * @param getBeforeUpdate {@code true} if the operation should return the
     *                        counter value before the addition, {@code false}
     *                        if it should return the value after the addition
     * @return the value before the update if {@code getBeforeUpdate} is
     * {@code true}, otherwise the value after the update
     */
    @Request(id = 2, retryable = false, response = ResponseMessageConst.LONG)
    @Since("1.6")
    Object add(String name, long delta, boolean getBeforeUpdate);
}
