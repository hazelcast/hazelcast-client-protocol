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

@GenerateCodec(id = TemplateConstants.CARDINALITY_ESTIMATOR_TEMPLATE_ID, name = "CardinalityEstimator",
        ns = "Hazelcast.Client.Protocol.Codec")
@Since("1.3")
public interface CardinalityEstimatorCodecTemplate {

    /**
     * Add a new hash in the estimation set. This is the method you want to
     * use to feed hash values into the estimator.
     *
     * @param name The name of CardinalityEstimator
     * @param hash 64bit hash code value to add
     *
     * @since 1.3
     */
    @Since("1.3")
    @Request(id = 1, retryable = false, response = ResponseMessageConst.VOID, partitionIdentifier = "name")
    void add(String name, long hash);


    /**
     * Estimates the cardinality of the aggregation so far.
     * If it was previously estimated and never invalidated, then the cached version is used.
     *
     * @param name The name of CardinalityEstimator
     *
     * @return the previous cached estimation or the newly computed one.
     * @since 1.3
     */
    @Since("1.3")
    @Request(id = 2, retryable = false, response = ResponseMessageConst.LONG, partitionIdentifier = "name")
    Object estimate(String name);

}
