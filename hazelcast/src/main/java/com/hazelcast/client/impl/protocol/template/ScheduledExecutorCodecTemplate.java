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
import com.hazelcast.annotation.Since;
import com.hazelcast.client.impl.protocol.constants.ResponseMessageConst;
import com.hazelcast.nio.Address;
import com.hazelcast.nio.serialization.Data;
import com.hazelcast.scheduledexecutor.ScheduledTaskHandler;

import java.util.List;
import java.util.concurrent.TimeUnit;

@GenerateCodec(id = TemplateConstants.SCHEDULED_EXECUTOR_TEMPLATE_ID, name = "ScheduledExecutor", ns = "Hazelcast.Client.Protocol.Codec")
@Since("1.3")
public interface ScheduledExecutorCodecTemplate {

    /**
     * Initiates an orderly shutdown in which previously submitted tasks are executed, but no new tasks will be accepted.
     * Invocation has no additional effect if already shut down.
     *
     * @param schedulerName Name of the scheduler.
     */
    @Request(id = 1, retryable = false, response = ResponseMessageConst.VOID)
    void shutdown(String schedulerName);

    /**
     * Returns true if this executor has been shut down.
     *
     * @param schedulerName Name of the scheduler.
     * @return true if this executor has been shut down
     */
    @Request(id = 2, retryable = false, response = ResponseMessageConst.BOOLEAN)
    Object isShutdown(String schedulerName);

    /**
     * Submits the task to partition for execution
     *
     * @param schedulerName The name of the scheduler.
     * @param taskDefinition  The task definition object.
     * @return the sequence for the submitted execution.
     */
    @Request(id = 3, retryable = true, response = ResponseMessageConst.VOID, partitionIdentifier = "partitionId")
    void submitToPartition(String schedulerName, Data taskDefinition);

    @Request(id = 4, retryable = true, response = ResponseMessageConst.VOID, partitionIdentifier = "partitionId")
    void submitToAddress(String schedulerName, Address address, Data taskDefinition);

    @Request(id = 5, retryable = true, response = ResponseMessageConst.LIST_SCHEDULED_TASK_HANDLER, partitionIdentifier = "partitionId")
    List<ScheduledTaskHandler> getAllScheduled(String schedulerName, Address address);

    @Request(id = 6, retryable = true, response = ResponseMessageConst.SCHEDULED_TASK_STATISTICS, partitionIdentifier = "partitionId")
    Object getStats(ScheduledTaskHandler handler);

    @Request(id = 7, retryable = true, response = ResponseMessageConst.LONG, partitionIdentifier = "partitionId")
    long getDelay(ScheduledTaskHandler handler, TimeUnit unit);

    @Request(id = 8, retryable = true, response = ResponseMessageConst.INTEGER, partitionIdentifier = "partitionId")
    int compareTo(ScheduledTaskHandler handler, Data delayed);

    @Request(id = 9, retryable = true, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "partitionId")
    boolean cancel(ScheduledTaskHandler handler, boolean mayInterruptIfRunning);

    @Request(id = 10, retryable = true, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "partitionId")
    boolean isCancelled(ScheduledTaskHandler handler);

    @Request(id = 11, retryable = true, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "partitionId")
    boolean isDone(ScheduledTaskHandler handler);

    @Request(id = 12, retryable = true, response = ResponseMessageConst.DATA, partitionIdentifier = "partitionId")
    Data getResultTimeout(ScheduledTaskHandler handler, long timeout, TimeUnit timeUnit);

    @Request(id = 13, retryable = true, response = ResponseMessageConst.VOID, partitionIdentifier = "partitionId")
    void dispose(ScheduledTaskHandler handler);
}
