/*
 * Copyright (c) 2008-2015, Hazelcast, Inc. All Rights Reserved.
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
import com.hazelcast.nio.serialization.Data;

@GenerateCodec(id = TemplateConstants.DURABLE_EXECUTOR_TEMPLATE_ID, name = "DurableExecutor", ns = "Hazelcast.Client.Protocol.Codec")
public interface DurableExecutorCodecTemplate {

    /**
     * Initiates an orderly shutdown in which previously submitted tasks are executed, but no new tasks will be accepted.
     * Invocation has no additional effect if already shut down.
     *
     * @param name Name of the executor.
     */
    @Request(id = 1, retryable = false, response = ResponseMessageConst.VOID, since = "1.1")
    void shutdown(String name);

    /**
     * Returns true if this executor has been shut down.
     *
     * @param name Name of the executor.
     * @return true if this executor has been shut down
     */
    @Request(id = 2, retryable = false, response = ResponseMessageConst.BOOLEAN, since = "1.1")
    Object isShutdown(String name);

    /**
     * Submits the task to partition for execution
     *
     * @param name        Name of the executor.
     * @param callable    The callable object to be executed.
     * @return the sequence for the submitted execution.
     */
    @Request(id = 3, retryable = true, response = ResponseMessageConst.INTEGER, partitionIdentifier = "partitionId", since = "1.1")
    Object submitToPartition(String name, Data callable);

    /**
     * Retrieves the result of the execution with the given sequence
     *
     * @param name        Name of the executor.
     * @param sequence    Sequence of the execution.
     * @return The result of the callable execution with the given sequence.
     */
    @Request(id = 4, retryable = true, response = ResponseMessageConst.DATA, partitionIdentifier = "partitionId", since = "1.1")
    Object retrieveResult(String name, int sequence);

    /**
     * Disposes the result of the execution with the given sequence
     *
     * @param name        Name of the executor.
     * @param sequence    Sequence of the execution.
     */
    @Request(id = 5, retryable = true, response = ResponseMessageConst.VOID, partitionIdentifier = "partitionId", since = "1.1")
    Object disposeResult(String name, int sequence);

    /**
     * Retrieves and disposes the result of the execution with the given sequence
     *
     * @param name        Name of the executor.
     * @param sequence    Sequence of the execution.
     * @return The result of the callable execution with the given sequence.
     */
    @Request(id = 6, retryable = true, response = ResponseMessageConst.DATA, partitionIdentifier = "partitionId", since = "1.1")
    Object retrieveAndDisposeResult(String name, int sequence);
}
