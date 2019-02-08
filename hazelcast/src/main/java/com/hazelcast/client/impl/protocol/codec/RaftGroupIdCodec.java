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
import com.hazelcast.annotation.Since;
import com.hazelcast.client.impl.protocol.ClientMessage;
import com.hazelcast.client.impl.protocol.util.ParameterUtil;
import com.hazelcast.cp.internal.RaftGroupId;
import com.hazelcast.nio.Bits;

@Since("1.8")
@Codec(RaftGroupId.class)
public final class RaftGroupIdCodec {

    private RaftGroupIdCodec() {
    }

    public static RaftGroupId decode(ClientMessage clientMessage) {
        String name = clientMessage.getStringUtf8();
        long seed = clientMessage.getLong();
        long commitIndex = clientMessage.getLong();
        return new RaftGroupId(name, seed, commitIndex);
    }

    public static void encode(RaftGroupId groupId, ClientMessage clientMessage) {
        clientMessage.set(groupId.name()).set(groupId.seed()).set(groupId.id());
    }

    public static int calculateDataSize(RaftGroupId groupId) {
        return ParameterUtil.calculateDataSize(groupId.name()) + 2 * Bits.LONG_SIZE_IN_BYTES;
    }

}
