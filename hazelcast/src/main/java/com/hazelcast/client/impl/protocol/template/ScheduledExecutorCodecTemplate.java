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
     * @param type type of schedule logic, values 0 for SINGLE_RUN, 1 for AT_FIXED_RATE
     * @param taskName The name of the task
     * @param task The data form of the Callable or Runnable task to be executed on that scheduler
     * @param initialDelayInMillis initial delay in milliseconds
     * @param periodInMillis period between each run in milliseconds
     */
    @Since("1.4")
    @Request(id = 2, retryable = true, response = ResponseMessageConst.VOID, partitionIdentifier = "taskName")
    void submitToPartition(String schedulerName, byte type, String taskName, Data task, long initialDelayInMillis, long periodInMillis);

    /**
     * Submits the task to a member for execution, member is provided in the form of an address.
     *
     * @param schedulerName The name of the scheduler.
     * @param address The address of the member where the task will get scheduled.
     * @param type type of schedule logic, values 0 for SINGLE_RUN, 1 for AT_FIXED_RATE
     * @param taskName The name of the task
     * @param task The data form of the Callable or Runnable task to be executed on that scheduler
     * @param initialDelayInMillis initial delay in milliseconds
     * @param periodInMillis period between each run in milliseconds
     */
    @Since("1.4")
    @Request(id = 3, retryable = true, response = ResponseMessageConst.VOID)
    void submitToAddress(String schedulerName, Address address, byte type, String taskName, Data task, long initialDelayInMillis, long periodInMillis);

    /**
     * Returns all scheduled tasks in for a given scheduler in the given member.
     *
     * @param schedulerName The name of the scheduler.
     * @return A list of scheduled task handlers used to construct the future proxies.
     */
    @Since("1.4")
    @Request(id = 4, retryable = true, response = ResponseMessageConst.ALL_SCHEDULED_TASK_HANDLERS)
    Object getAllScheduledFutures(String schedulerName);

    /**
     * Returns statistics of the task
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @return A snapshot of the task statistics
     */
    @Since("1.4")
    @Request(id = 5, retryable = true, response = ResponseMessageConst.SCHEDULED_TASK_STATISTICS, partitionIdentifier = "taskName")
    Object getStatsFromPartition(String schedulerName, String taskName);

    /**
     * Returns statistics of the task
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @param address The address of the member where the task will get scheduled.
     * @return A snapshot of the task statistics
     */
    @Since("1.4")
    @Request(id = 6, retryable = true, response = ResponseMessageConst.SCHEDULED_TASK_STATISTICS)
    Object getStatsFromAddress(String schedulerName , String taskName, Address address);

    /**
     * Returns the ScheduledFuture's delay in nanoseconds for the task in the scheduler.
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @return The remaining delay of the task formatted in nanoseconds.
     */
    @Since("1.4")
    @Request(id = 7, retryable = true, response = ResponseMessageConst.LONG, partitionIdentifier = "taskName")
    long getDelayFromPartition(String schedulerName , String taskName);

    /**
     * Returns the ScheduledFuture's delay in nanoseconds for the task in the scheduler.
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @param address The address of the member where the task will get scheduled.
     * @return The remaining delay of the task formatted in nanoseconds.
     */
    @Since("1.4")
    @Request(id = 8, retryable = true, response = ResponseMessageConst.LONG)
    long getDelayFromAddress(String schedulerName , String taskName, Address address);

    /**
     * Cancels further execution and scheduling of the task
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @param mayInterruptIfRunning  A boolean flag to indicate whether the task should be interrupted.
     * @return True if the task was cancelled
     */
    @Since("1.4")
    @Request(id = 9, retryable = true, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "taskName")
    boolean cancelFromPartition(String schedulerName, String taskName, boolean mayInterruptIfRunning);

    /**
     * Cancels further execution and scheduling of the task
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @param address The address of the member where the task will get scheduled.
     * @param mayInterruptIfRunning  A boolean flag to indicate whether the task should be interrupted.
     * @return True if the task was cancelled
     */
    @Since("1.4")
    @Request(id = 10, retryable = true, response = ResponseMessageConst.BOOLEAN)
    boolean cancelFromAddress(String schedulerName, String taskName, Address address, boolean mayInterruptIfRunning);

    /**
     * Checks whether a task as identified from the given handler is already cancelled.
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @return True if the task is cancelled
     */
    @Since("1.4")
    @Request(id = 11, retryable = true, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "taskName")
    boolean isCancelledFromPartition(String schedulerName, String taskName);

    /**
     * Checks whether a task as identified from the given handler is already cancelled.
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @param address The address of the member where the task will get scheduled.
     * @return True if the task is cancelled
     */
    @Since("1.4")
    @Request(id = 12, retryable = true, response = ResponseMessageConst.BOOLEAN)
    boolean isCancelledFromAddress(String schedulerName , String taskName, Address address);

    /**
     * Checks whether a task is done.
     * @see {@link java.util.concurrent.Future#cancel(boolean)}
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @return True if the task is done
     */
    @Since("1.4")
    @Request(id = 13, retryable = true, response = ResponseMessageConst.BOOLEAN, partitionIdentifier = "taskName")
    boolean isDoneFromPartition(String schedulerName , String taskName);

    /**
     * Checks whether a task is done.
     * @see {@link java.util.concurrent.Future#cancel(boolean)}
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @param address The address of the member where the task will get scheduled.
     * @return True if the task is done
     */
    @Since("1.4")
    @Request(id = 14, retryable = true, response = ResponseMessageConst.BOOLEAN)
    boolean isDoneFromAddress(String schedulerName , String taskName, Address address);

    /**
     * Fetches the result of the task ({@link java.util.concurrent.Callable})
     * The call will blocking until the result is ready.
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @return The result of the completed task, in serialized form ({@link Data}.
     */
    @Since("1.4")
    @Request(id = 15, retryable = true, response = ResponseMessageConst.DATA, partitionIdentifier = "taskName")
    Data getResultFromPartition(String schedulerName , String taskName);

    /**
     * Fetches the result of the task ({@link java.util.concurrent.Callable})
     * The call will blocking until the result is ready.
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @param address The address of the member where the task will get scheduled.
     * @return The result of the completed task, in serialized form ({@link Data}.
     */
    @Since("1.4")
    @Request(id = 16, retryable = true, response = ResponseMessageConst.DATA)
    Data getResultFromAddress(String schedulerName , String taskName, Address address);

    /**
     * Dispose the task from the scheduler
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     */
    @Since("1.4")
    @Request(id = 17, retryable = true, response = ResponseMessageConst.VOID, partitionIdentifier = "taskName")
    void disposeFromPartition(String schedulerName, String taskName);

    /**
     * Dispose the task from the scheduler
     *
     * @param schedulerName The name of the scheduler.
     * @param taskName The name of the task
     * @param address The address of the member where the task will get scheduled.
     */
    @Since("1.4")
    @Request(id = 18, retryable = true, response = ResponseMessageConst.VOID)
    void disposeFromAddress(String schedulerName , String taskName, Address address);
}
