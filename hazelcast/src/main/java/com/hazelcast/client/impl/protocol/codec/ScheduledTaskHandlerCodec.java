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

package com.hazelcast.client.impl.protocol.codec;

import com.hazelcast.annotation.Codec;
import com.hazelcast.client.impl.protocol.ClientMessage;
import com.hazelcast.client.impl.protocol.util.ParameterUtil;
import com.hazelcast.nio.Address;
import com.hazelcast.nio.Bits;
import com.hazelcast.scheduledexecutor.ScheduledTaskHandler;
import com.hazelcast.scheduledexecutor.impl.ScheduledTaskHandlerImpl;

@Codec(ScheduledTaskHandler.class)
public final class ScheduledTaskHandlerCodec {

    private ScheduledTaskHandlerCodec() {
    }

    public static ScheduledTaskHandler decode(ClientMessage clientMessage) {
        String schedulerName = clientMessage.getStringUtf8();
        String taskName = clientMessage.getStringUtf8();
        boolean isToAddress = clientMessage.getBoolean();
        if (isToAddress) {
            Address address = AddressCodec.decode(clientMessage);
            return ScheduledTaskHandlerImpl.of(address, schedulerName, taskName);
        } else {
            int partitionId = clientMessage.getInt();
            return ScheduledTaskHandlerImpl.of(partitionId, schedulerName, taskName);
        }
    }

    public static void encode(ScheduledTaskHandler scheduledTaskHandler, ClientMessage clientMessage) {
        clientMessage.set(scheduledTaskHandler.getSchedulerName());
        clientMessage.set(scheduledTaskHandler.getTaskName());
        Address address = scheduledTaskHandler.getAddress();
        boolean isToAddress = address != null;
        clientMessage.set(isToAddress);
        if (isToAddress) {
            AddressCodec.encode(address, clientMessage);
        } else {
            clientMessage.set(scheduledTaskHandler.getPartitionId());
        }
    }

    public static int calculateDataSize(ScheduledTaskHandler scheduledTaskHandler) {
        int dataSize = ParameterUtil.calculateDataSize(scheduledTaskHandler.getSchedulerName());
        dataSize += ParameterUtil.calculateDataSize(scheduledTaskHandler.getTaskName());
        // is to address field
        dataSize += Bits.BOOLEAN_SIZE_IN_BYTES;
        Address address = scheduledTaskHandler.getAddress();
        if (address != null) {
            dataSize += AddressCodec.calculateDataSize(address);
        } else {
            dataSize += Bits.INT_SIZE_IN_BYTES;
        }
        return dataSize;
    }
}
