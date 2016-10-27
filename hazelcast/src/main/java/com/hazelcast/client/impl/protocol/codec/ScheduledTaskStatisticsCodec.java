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

package com.hazelcast.client.impl.protocol.codec;

import com.hazelcast.annotation.Codec;
import com.hazelcast.client.impl.protocol.ClientMessage;
import com.hazelcast.client.impl.protocol.util.ParameterUtil;
import com.hazelcast.scheduledexecutor.ScheduledTaskStatistics;
import com.hazelcast.scheduledexecutor.impl.ScheduledTaskStatisticsImpl;

import java.util.concurrent.TimeUnit;

@Codec(ScheduledTaskStatistics.class)
public final class ScheduledTaskStatisticsCodec {

    private ScheduledTaskStatisticsCodec() {
    }

    public static ScheduledTaskStatistics decode(ClientMessage clientMessage) {
        long createdAt = clientMessage.getLong();
        long firstRunStartNanos = clientMessage.getLong();
        long lastIdleTimeNanos = clientMessage.getLong();
        long lastRunEndNanos = clientMessage.getLong();
        long lastRunStartNanos = clientMessage.getLong();
        long totalIdleTimeNanos = clientMessage.getLong();
        long totalRuns = clientMessage.getLong();
        long totalRunTimeNanos = clientMessage.getLong();
        return new ScheduledTaskStatisticsImpl(totalRuns, createdAt, firstRunStartNanos, lastRunStartNanos,
                                                lastRunEndNanos, lastIdleTimeNanos, totalRunTimeNanos, totalIdleTimeNanos);
    }

    public static void encode(ScheduledTaskStatistics stats, ClientMessage clientMessage) {
        clientMessage.set(stats.getCreatedAt());
        clientMessage.set(stats.getFirstRunStart(TimeUnit.NANOSECONDS));
        clientMessage.set(stats.getLastIdleTime(TimeUnit.NANOSECONDS));
        clientMessage.set(stats.getLastRunEnd(TimeUnit.NANOSECONDS));
        clientMessage.set(stats.getLastRunStart(TimeUnit.NANOSECONDS));
        clientMessage.set(stats.getTotalIdleTime(TimeUnit.NANOSECONDS));
        clientMessage.set(stats.getTotalRuns());
        clientMessage.set(stats.getTotalRunTime(TimeUnit.NANOSECONDS));
    }

    public static int calculateDataSize(ScheduledTaskStatistics stats) {
        int dataSize = ClientMessage.HEADER_SIZE;
        return dataSize
                + ParameterUtil.calculateDataSize(stats.getCreatedAt())
                + ParameterUtil.calculateDataSize(stats.getFirstRunStart(TimeUnit.NANOSECONDS))
                + ParameterUtil.calculateDataSize(stats.getLastIdleTime(TimeUnit.NANOSECONDS))
                + ParameterUtil.calculateDataSize(stats.getLastRunEnd(TimeUnit.NANOSECONDS))
                + ParameterUtil.calculateDataSize(stats.getLastRunStart(TimeUnit.NANOSECONDS))
                + ParameterUtil.calculateDataSize(stats.getTotalIdleTime(TimeUnit.NANOSECONDS))
                + ParameterUtil.calculateDataSize(stats.getTotalRuns())
                + ParameterUtil.calculateDataSize(stats.getTotalRunTime(TimeUnit.NANOSECONDS));
    }
}
