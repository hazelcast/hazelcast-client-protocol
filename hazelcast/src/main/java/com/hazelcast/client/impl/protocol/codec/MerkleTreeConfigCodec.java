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
import com.hazelcast.config.HotRestartConfig;
import com.hazelcast.config.MerkleTreeConfig;
import com.hazelcast.nio.Bits;

@Codec(MerkleTreeConfig.class)
@Since("2.0")
public final class MerkleTreeConfigCodec {

    private MerkleTreeConfigCodec() {
    }

    public static MerkleTreeConfig decode(ClientMessage clientMessage) {
        boolean enabled = clientMessage.getBoolean();
        int depth = clientMessage.getInt();
        MerkleTreeConfig config = new MerkleTreeConfig();
        config.setEnabled(enabled);
        config.setDepth(depth);
        return config;
    }

    public static void encode(MerkleTreeConfig config, ClientMessage clientMessage) {
        clientMessage.set(config.isEnabled())
                     .set(config.getDepth());
    }

    public static int calculateDataSize(MerkleTreeConfig config) {
        return Bits.BOOLEAN_SIZE_IN_BYTES + Bits.INT_SIZE_IN_BYTES;
    }
}
