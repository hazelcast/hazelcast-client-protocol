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
import com.hazelcast.nio.Address;

import java.util.List;
import java.util.Map.Entry;

@GenerateCodec(id = TemplateConstants.PN_COUNTER_ID_GENERATOR_TEMPLATE_ID, name = "PNCounter", ns = "Hazelcast.Client.Protocol.Codec")
public interface PNCounterGeneratorCodecTemplate {

    /**
     * Query operation to retrieve the current value of the PNCounter.
     * <p>
     * The invocation will return the replica timestamps (vector clock) which
     * can then be sent with the next invocation to keep session consistency
     * guarantees.
     * The target replica is determined by the {@code targetReplica} parameter.
     * If smart routing is disabled, the actual member processing the client
     * message may act as a proxy.
     *
     * @param name              the name of the PNCounter
     * @param replicaTimestamps last observed replica timestamps (vector clock)
     * @param targetReplica     the target replica
     * @return the current value of the counter
     */
    @Request(id = 1, retryable = true, response = ResponseMessageConst.CRDT_TIMESTAMPED_LONG)
    @Since("1.6")
    Object get(String name, List<Entry<String, Long>> replicaTimestamps, Address targetReplica);

    /**
     * Adds a delta to the PNCounter value. The delta may be negative for a
     * subtraction.
     * <p>
     * The invocation will return the replica timestamps (vector clock) which
     * can then be sent with the next invocation to keep session consistency
     * guarantees.
     * The target replica is determined by the {@code targetReplica} parameter.
     * If smart routing is disabled, the actual member processing the client
     * message may act as a proxy.
     *
     * @param name              the name of the PNCounter
     * @param delta             the delta to add to the counter value, can be negative
     * @param getBeforeUpdate   {@code true} if the operation should return the
     *                          counter value before the addition, {@code false}
     *                          if it should return the value after the addition
     * @param replicaTimestamps last observed replica timestamps (vector clock)
     * @param targetReplica     the target replica
     * @return the value before the update if {@code getBeforeUpdate} is
     * {@code true}, otherwise the value after the update
     */
    @Request(id = 2, retryable = false, response = ResponseMessageConst.CRDT_TIMESTAMPED_LONG)
    @Since("1.6")
    Object add(String name, long delta, boolean getBeforeUpdate, List<Entry<String, Long>> replicaTimestamps, Address targetReplica);

    /**
     * Returns the configured number of CRDT replicas for the PN counter with
     * the given {@code name}.
     * The actual replica count may be less, depending on the number of data
     * members in the cluster (members that own data).
     *
     * @param name the name of the PNCounter
     * @return the configured replica count
     */
    @Request(id = 3, retryable = true, response = ResponseMessageConst.INTEGER)
    @Since("1.6")
    Object getConfiguredReplicaCount(String name);
}
