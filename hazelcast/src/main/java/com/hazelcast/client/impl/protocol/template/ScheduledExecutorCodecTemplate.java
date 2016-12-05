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

@GenerateCodec(id = TemplateConstants.SCHEDULED_EXECUTOR_TEMPLATE_ID, name = "ScheduledExecutor", ns = "Hazelcast.Client.Protocol.Codec")
@Since("1.4")
public interface ScheduledExecutorCodecTemplate {

    /**
     * Initiates an orderly shutdown in which previously submitted tasks are executed, but no new tasks will be accepted.
     * Invocation has no additional effect if already shut down.
     *
     * @param schedulerName Name of the scheduler.
     * @param address The cluster member where the shutdown for this scheduler will be sent.
     */
    @Since("1.4")
    @Request(id = 1, retryable = false, response = ResponseMessageConst.VOID)
    void shutdown(String schedulerName, Address address);

    /**
     * Submits the task to partition for execution, partition is chosen based on multiple criteria of the given task.
     *
     * @param schedulerName The name of the scheduler.
     * @param taskDefinition  The data form of the Callable or Runnable task to be executed on that scheduler
     */
    @Since("1.4")
    @Request(id = 2, retryable = true, response = ResponseMessageConst.VOID, partitionIdentifier = "partitionId")
    void submitToPartition(String schedulerName, Data taskDefinition);

    /**
     * Submits the task to a member for execution, member is provided in the form of an address.
     *
     * @param schedulerName The name of the scheduler.
     * @param taskDefinition  The data form of the Callable or Runnable task to be executed on that scheduler
     * @param address The address of the member where the task will get scheduled.
     */
    @Since("1.4")
    @Request(id = 3, retryable = true, response = ResponseMessageConst.VOID, partitionIdentifier = "partitionId")
    void submitToAddress(String schedulerName, Address address, Data taskDefinition);

    /**
     * Returns all scheduled tasks in for a given scheduler in the given member.
     *
     * @param schedulerName The name of the scheduler.
     * @param address  The address of the member to do the lookup.
     * @return A list of scheduled task handlers used to construct the future proxies.
     */
    @Since("1.4")
    @Request(id = 4, retryable = true, response = ResponseMessageConst.LIST_SCHEDULED_TASK_HANDLER,
            partitionIdentifier = "partitionId")
    Object getAllScheduledFutures(String schedulerName, Address address);

    /**
     * Returns statistics associated with the given task handler.
     *
     * @param handlerUrn The resource handler URN of the task
     * @return A snapshot of the task statistics as identified from the given handler.
     */
    @Since("1.4")
    @Request(id = 5, retryable = true, response = ResponseMessageConst.SCHEDULED_TASK_STATISTICS,
            partitionIdentifier = "partitionId")
    Object getStats(String handlerUrn);

    /**
     * Returns the ScheduledFuture's for the task in the scheduler as identified from the given handler.
     *
     * @param handlerUrn The resource handler URN of the task
     * @param timeUnitName A string representing time unit information.
     *                     <br/> Allowed values:
     *                     <ul>
     *                         <li>"NANOSECONDS"</li>
     *                         <li>"MICROSECONDS"</li>
     *                         <li>"MILLISECONDS"</li>
     *                         <li>"SECONDS"</li>
     *                         <li>"MINUTES"</li>
     *                         <li>"HOURS"</li>
     *                         <li>"DAYS"</li>
     *                     </ul>
     * @return The remaining delay of the task formatted in the give TimeUnit.
     */
    @Since("1.4")
    @Request(id = 6, retryable = true, response = ResponseMessageConst.LONG, partitionIdentifier = "partitionId")
    long getDelay(String handlerUrn, String timeUnitName);

    /**
     * Cancels further execution and scheduling of the task as identified from the given handler.
     *
     * @param handlerUrn The resource handler URN of the task
     * @param mayInterruptIfRunning  A boolean flag to indicate whether the task should be interrupted.
     * @return True if the task was cancelled
     */
    @Since("1.4")
    @Request(id = 7, retryable = true, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "partitionId")
    boolean cancel(String handlerUrn, boolean mayInterruptIfRunning);

    /**
     * Checks whether a task as identified from the given handler is already cancelled.
     *
     * @param handlerUrn The resource handler URN of the task
     * @return True if the task is cancelled
     */
    @Since("1.4")
    @Request(id = 8, retryable = true, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "partitionId")
    boolean isCancelled(String handlerUrn);

    /**
     * Checks whether a task as identified from the given handler is done.
     * @see {@link java.util.concurrent.Future#cancel(boolean)}
     *
     * @param handlerUrn The resource handler URN of the task
     * @return True if the task is done
     */
    @Since("1.4")
    @Request(id = 9, retryable = true, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "partitionId")
    boolean isDone(String handlerUrn);

    /**
     * Fetches the result of the task ({@link java.util.concurrent.Callable}) as identified from the given handler.
     * The call will blocking until the result is ready.
     *
     * @param handlerUrn The resource handler URN of the task
     * @return The result of the completed task, in serialized form ({@link Data}.
     */
    @Since("1.4")
    @Request(id = 10, retryable = true, response = ResponseMessageConst.DATA, partitionIdentifier = "partitionId")
    Data getResult(String handlerUrn);

    /**
     * Dispose the task from the scheduler, as identified from the given handler.
     *
     * @param handlerUrn The resource handler URN of the task
     */
    @Since("1.4")
    @Request(id = 11, retryable = true, response = ResponseMessageConst.VOID, partitionIdentifier = "partitionId")
    void dispose(String handlerUrn);
}
