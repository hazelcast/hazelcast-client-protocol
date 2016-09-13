/*
 * Copyright (c) 2008-2016, Hazelcast, Inc. All Rights Reserved.
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
import com.hazelcast.client.impl.protocol.ResponseMessageConst;

@GenerateCodec(id = TemplateConstants.CARDINALITY_ESTIMATOR_TEMPLATE_ID, name = "CardinalityEstimator",
        ns = "Hazelcast.Client.Protocol.Codec")
public interface CardinalityEstimatorCodecTemplate {

    /**
     * Applies a function on the value, the actual stored value will not change.
     *
     * @param name     The name of this IAtomicLong instance.
     * @param function The function applied to the value, the value is not changed.
     * @return The result of the function application.
     */
    @Request(id = 1, retryable = false, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "name")
    Boolean aggregate(String name, long hash);

    @Request(id = 2, retryable = false, response = ResponseMessageConst.LONG, partitionIdentifier = "name")
    Long aggregateAndEstimate(String name, long hash);

    @Request(id = 3, retryable = false, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "name")
    Boolean aggregateAll(String name, long[] hashes);

    @Request(id = 4, retryable = false, response = ResponseMessageConst.LONG, partitionIdentifier = "name")
    Long aggregateAllAndEstimate(String name, long[] hashes);

    @Request(id = 5, retryable = false, response = ResponseMessageConst.LONG, partitionIdentifier = "name")
    Long estimate(String name);

}
