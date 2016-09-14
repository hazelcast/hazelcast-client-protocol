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
     * Aggregates the given hash which can result in a new estimation being available or not.
     *
     * @param hash 64bit hash code value to aggregate
     * @return boolean flag True, when a new estimate can be computed.
     * @since 1.3
     */
    @Request(id = 1, retryable = false, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "name")
    Object aggregate(String name, long hash);

    /**
     * Aggregates the given hash and estimates the cardinality afterwards in one go.
     *
     * @param hash 64bit hash code value to aggregate
     * @return long estimate, the newly computed estimate or previously cached one.
     * @since 1.3
     */
    @Request(id = 2, retryable = false, response = ResponseMessageConst.LONG, partitionIdentifier = "name")
    Object aggregateAndEstimate(String name, long hash);

    /**
     * Batch aggregation for an array of hash codes. Can result in a new estimation being available or not.
     *
     * @param hashes List of 64bit hash code values to aggregate
     * @return boolean flag True, when a new estimate can be computed.
     * @since 1.3
     */
    @Request(id = 3, retryable = false, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "name")
    Object aggregateAll(String name, long[] hashes);

    /**
     * Batch aggregation for an array of hash codes and estimates the cardinality afterwards in one go.
     *
     * @param hashes List of 64bit hash code values to aggregate
     * @return long estimate, the newly computed estimate or previously cached one.
     * @since 1.3
     */
    @Request(id = 4, retryable = false, response = ResponseMessageConst.LONG, partitionIdentifier = "name")
    Object aggregateAllAndEstimate(String name, long[] hashes);

    /**
     * Estimates the cardinality of the aggregation so far.
     * If it was previously estimated and never invalidated, then the cached version is used.
     *
     * @return Returns the previous cached estimation or the newly computed one.
     * @since 1.3
     */
    @Request(id = 5, retryable = false, response = ResponseMessageConst.LONG, partitionIdentifier = "name")
    Object estimate(String name);

}
